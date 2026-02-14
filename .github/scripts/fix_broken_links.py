#!/usr/bin/env python3
"""
Scan markdown posts for broken external links and replace them with Wayback Machine archives.
Also restores original links if they become working again.

Format for archived links:
  [link text](wayback_url)<!-- original: https://original.url -->
"""

import re
import time
from pathlib import Path

import requests

POSTS_DIR = Path("_posts")

# Pattern for regular markdown links
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)')

# Pattern for archived links with original URL comment
ARCHIVED_PATTERN = re.compile(
    r'\[([^\]]+)\]\((https?://web\.archive\.org/[^)]+)\)<!-- original: (https?://[^\s]+) -->'
)

WAYBACK_API = "https://archive.org/wayback/available"

# Skip these domains (usually reliable or cause false positives)
SKIP_DOMAINS = {
    "github.com",
    "twitter.com",
    "x.com",
    "linkedin.com",
    "youtube.com",
    "archive.org",
    "web.archive.org",
}


def is_link_broken(url: str, timeout: int = 10) -> bool:
    """Check if a URL returns a non-success status code."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        # Some servers don't support HEAD, fall back to GET
        if response.status_code == 405:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
        return response.status_code >= 400
    except requests.RequestException:
        return True


def get_wayback_url(url: str) -> str | None:
    """Query the Wayback Machine API for an archived version of the URL."""
    try:
        response = requests.get(WAYBACK_API, params={"url": url}, timeout=10)
        data = response.json()
        snapshot = data.get("archived_snapshots", {}).get("closest")
        if snapshot and snapshot.get("available"):
            return snapshot["url"]
    except (requests.RequestException, ValueError):
        pass
    return None


def should_skip_url(url: str) -> bool:
    """Check if URL should be skipped based on domain."""
    for domain in SKIP_DOMAINS:
        if domain in url:
            return True
    return False


def check_and_restore_archived_links(content: str) -> tuple[str, int]:
    """Check archived links and restore originals if now working."""
    restored_count = 0
    
    for match in ARCHIVED_PATTERN.finditer(content):
        link_text = match.group(1)
        wayback_url = match.group(2)
        original_url = match.group(3)
        
        print(f"  Checking archived original: {original_url}")
        
        if not is_link_broken(original_url):
            print(f"  🔄 Restored (now working): {original_url}")
            archived_link = f"[{link_text}]({wayback_url})<!-- original: {original_url} -->"
            restored_link = f"[{link_text}]({original_url})"
            content = content.replace(archived_link, restored_link)
            restored_count += 1
        else:
            print(f"  ⏸️  Still broken, keeping archive")
        
        time.sleep(1)
    
    return content, restored_count


def check_and_archive_broken_links(content: str) -> tuple[str, int]:
    """Check regular links and archive broken ones."""
    archived_count = 0
    replacements = []
    
    for match in LINK_PATTERN.finditer(content):
        link_text = match.group(1)
        url = match.group(2)
        
        # Skip if already an archive link or in skip list
        if should_skip_url(url) or "web.archive.org" in url:
            continue
        
        print(f"  Checking: {url}")
        
        if is_link_broken(url):
            print(f"  ⚠️  Broken: {url}")
            wayback_url = get_wayback_url(url)
            
            if wayback_url:
                print(f"  ✅ Archived: {wayback_url}")
                original = f"[{link_text}]({url})"
                # Store original URL in HTML comment for future restoration
                replacement = f"[{link_text}]({wayback_url})<!-- original: {url} -->"
                replacements.append((original, replacement))
            else:
                print(f"  ❌ No archive found for: {url}")
        
        time.sleep(1)
    
    for original, replacement in replacements:
        content = content.replace(original, replacement)
        archived_count += 1
    
    return content, archived_count


def process_file(filepath: Path) -> tuple[int, int]:
    """Process a single markdown file. Returns (archived_count, restored_count)."""
    content = filepath.read_text(encoding="utf-8")
    original_content = content
    
    # First, check if any archived links can be restored
    content, restored_count = check_and_restore_archived_links(content)
    
    # Then, check for new broken links to archive
    content, archived_count = check_and_archive_broken_links(content)
    
    # Only write if content changed
    if content != original_content:
        filepath.write_text(content, encoding="utf-8")
    
    return archived_count, restored_count


def main():
    """Main entry point."""
    if not POSTS_DIR.exists():
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    total_archived = 0
    total_restored = 0
    
    for filepath in POSTS_DIR.glob("*.md"):
        print(f"\nProcessing: {filepath.name}")
        archived, restored = process_file(filepath)
        total_archived += archived
        total_restored += restored
        
        if archived:
            print(f"  📦 Archived {archived} broken link(s)")
        if restored:
            print(f"  🔄 Restored {restored} working link(s)")
    
    print(f"\n{'='*50}")
    print(f"Total archived: {total_archived}")
    print(f"Total restored: {total_restored}")


if __name__ == "__main__":
    main()
