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

## Updating the live site

After the weekly update (or any push to `main`), wait for the **Actions** run to finish, then in cPanel → **Git™ Version Control** → **Manage** → **Pull or Deploy**:
1. **Update from Remote**
2. **Deploy HEAD Commit**
