#!/usr/bin/env python3
"""
Scan markdown posts for broken external links and replace them with Wayback Machine archives.
"""

import re
import time
from pathlib import Path

import requests

POSTS_DIR = Path("_posts")
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)')
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


def process_file(filepath: Path) -> list[tuple[str, str]]:
    """Process a single markdown file, returning list of (original, replacement) tuples."""
    content = filepath.read_text(encoding="utf-8")
    replacements = []
    
    for match in LINK_PATTERN.finditer(content):
        link_text = match.group(1)
        url = match.group(2)
        
        if should_skip_url(url):
            continue
        
        print(f"  Checking: {url}")
        
        if is_link_broken(url):
            print(f"  ⚠️  Broken: {url}")
            wayback_url = get_wayback_url(url)
            
            if wayback_url:
                print(f"  ✅ Found archive: {wayback_url}")
                original = f"[{link_text}]({url})"
                replacement = f"[{link_text}]({wayback_url})"
                replacements.append((original, replacement))
            else:
                print(f"  ❌ No archive found for: {url}")
        
        # Rate limiting to be nice to servers
        time.sleep(1)
    
    return replacements


def main():
    """Main entry point."""
    if not POSTS_DIR.exists():
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    total_fixes = 0
    
    for filepath in POSTS_DIR.glob("*.md"):
        print(f"\nProcessing: {filepath.name}")
        replacements = process_file(filepath)
        
        if replacements:
            content = filepath.read_text(encoding="utf-8")
            for original, replacement in replacements:
                content = content.replace(original, replacement)
            filepath.write_text(content, encoding="utf-8")
            total_fixes += len(replacements)
            print(f"  Fixed {len(replacements)} link(s)")
    
    print(f"\n{'='*50}")
    print(f"Total links fixed: {total_fixes}")


if __name__ == "__main__":
    main()
