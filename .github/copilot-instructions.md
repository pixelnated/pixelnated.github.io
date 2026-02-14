# Copilot Instructions for pixelnated.github.io

## Project Overview
This is a Jekyll-based personal blog hosted on GitHub Pages using the **minima** theme. Posts are written in Markdown and automatically deployed on push to `main`.

## Architecture

- **Theme**: Minima (customized via `_layouts/`, `_includes/`, `css/override.css`)
- **Syntax Highlighting**: Uses highlight.js (NOT Jekyll's built-in Rouge/Kramdown) – see [_includes/head.html](_includes/head.html)
- **Post Titles**: Derived automatically from first H2 header via `jekyll-titles-from-headings` plugin; filename-based if no header exists

## Creating New Posts

1. Add files to `_posts/` with naming: `YYYY-MM-DD-slug-title.md`
2. Start with an H2 (`##`) header for the title (no front matter title needed)
3. Use tags in front matter (defaults to `Other` if omitted):
   ```yaml
   ---
   tags: PowerShell
   ---
   ```

## Code Blocks

Kramdown's syntax highlighter is **disabled** in `_config.yml`. Use fenced code blocks with these supported languages:
- `tsql` – T-SQL with SSMS-style highlighting
- `powershell` – PowerShell scripts
- `plaintext` – No highlighting

To add a new language: download the highlight.js language file to `js/highlightjs/languages/` and register it in [_includes/head.html](_includes/head.html).

## Key Customizations

| Feature | Location |
|---------|----------|
| Social share buttons | [_includes/sharelinks.html](_includes/sharelinks.html) |
| Post navigation (prev/next) | [_includes/navlinks.html](_includes/navlinks.html) |
| Navigation/share styling | [css/override.css](css/override.css) |
| Highlight.js styles | `js/highlightjs/styles/` (github.css + ssms.css loaded) |

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Site builds to `_site/` (gitignored). Preview at `http://localhost:4000`.

## CI/CD & Automation

- **Deployment**: GitHub Pages auto-builds on push to `main`
- **GitHub Actions**: Workflows in `.github/workflows/`
- When creating workflows, target `ubuntu-latest` with `actions/checkout@v4` and Jekyll build via `bundle exec jekyll build`

### Active Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [fix-broken-links.yml](.github/workflows/fix-broken-links.yml) | Weekly (Sunday 6AM UTC) or manual | Scans posts for broken external links and replaces with Wayback Machine archives |

The link fixer script at [.github/scripts/fix_broken_links.py](.github/scripts/fix_broken_links.py) skips common social/video sites to avoid false positives and creates a PR for review.

## File Conventions

- **No front matter `layout:`** needed for posts – defaults to `post` layout via `_config.yml` defaults
- **Archive page** at [archive.md](archive.md) groups posts by tags
- Social links configured in `_config.yml` (twitter, github, linkedin, etc.)
