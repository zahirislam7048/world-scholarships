# Deploying higherstudyinfo.com (cPanel Git Version Control)

`tools/build_site.py` builds the static site into `site/` (home page, one page per dataset, `sitemap.xml`, `robots.txt`). Every page's `<head>` includes `tools/site_head.html` (Google site verification + Google Analytics `G-WY2KEFM167`).

On every push to `main` (including the weekly data update), `.github/workflows/deploy.yml` rebuilds `site/` and commits it to `main`. cPanel pulls `main` and the root `.cpanel.yml` copies `site/` into the domain's document root `~/higherstudyinfo.com/`; nothing is pushed to the server from GitHub, so no FTP password is stored anywhere.

## One-time setup

The repository is public, so cPanel clones it over HTTPS with no key.

1. **Domain:** point `higherstudyinfo.com` at the cPanel host (the host's nameservers). Skip if the domain was bought from the same host.
2. **Clone in cPanel:** cPanel → **Git™ Version Control** → **Create**:
   - Clone URL: `https://github.com/zahirislam7048/world-scholarships.git`
   - Repository Path: `repositories/world-scholarships`
   - Repository Name: `world-scholarships`
   → **Create**. Keep the checked-out branch as **`main`**.
3. **First deploy:** **Manage** → **Pull or Deploy** → **Update from Remote** → **Deploy HEAD Commit**. Open https://higherstudyinfo.com.
4. **Google Search Console:** verify with the meta tag (already on every page), then submit `https://higherstudyinfo.com/sitemap.xml`.

## Automatic updates

- The GitHub Action also runs **daily** (06:23 Asia/Dhaka) and rebuilds `site/`, so deadlines that have passed drop off and the counts stay current.
- Pages show “সর্বশেষ যাচাই” = the date in `data/LAST_CHECKED`, which the weekly update writes every time it checks the data (even if nothing changed).
- Country and search pages also hide passed deadlines in the visitor's browser.

## Updating the live site

A cPanel **Cron Job** (once per hour) pulls `main` and copies `site/` into the document root, so the weekly update reaches the live site within about an hour:

```
cd ~/repositories/world-scholarships && git pull -q origin main && /bin/cp -R site/. ~/higherstudyinfo.com/
```

To update right away instead: cPanel → **Git™ Version Control** → **Manage** → **Pull or Deploy** → **Update from Remote** → **Deploy HEAD Commit**.

## .htaccess and 404 page

The build copies `tools/static/.htaccess` into `site/`, so every deploy overwrites `~/higherstudyinfo.com/.htaccess`. It sets the custom 404 page (`/404.html`), redirects http and www to `https://higherstudyinfo.com`, and turns on compression and browser caching. Every block is wrapped in `<IfModule>`. If the site ever shows a 500 error or a redirect loop after a deploy, rename `~/higherstudyinfo.com/.htaccess` in cPanel File Manager and report it — then fix `tools/static/.htaccess`. Put any cPanel-specific directives in `tools/static/.htaccess`, not in the live file.
