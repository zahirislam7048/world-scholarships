# Deploying higherstudyinfo.com

`tools/build_site.py` builds the static site into `site/` (home page, one page per dataset, `sitemap.xml`, `robots.txt`). Every page's `<head>` includes `tools/site_head.html` (Google site verification + Google Analytics `G-WY2KEFM167`).

On every push to `main` (including the weekly data update), `.github/workflows/deploy.yml` builds the site and uploads `site/` to cPanel over FTP. It can also be run by hand from the repo's **Actions** tab → **Deploy site to cPanel** → **Run workflow**.

## One-time setup

1. **Domain → hosting:** in the registrar, point `higherstudyinfo.com` at the cPanel host (the host's nameservers, or an A record to the server IP). Skip if the domain was bought from the same host.
2. **FTP account:** cPanel → **FTP Accounts** → create one whose directory is `public_html` (or use the main cPanel account).
3. **GitHub secrets:** repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| secret | value |
|---|---|
| `FTP_SERVER` | FTP host from cPanel (e.g. `ftp.higherstudyinfo.com`) |
| `FTP_USERNAME` | FTP username (e.g. `deploy@higherstudyinfo.com`) |
| `FTP_PASSWORD` | FTP password |
| `FTP_SERVER_DIR` | optional. `./` if the FTP account's directory **is** `public_html`; default `public_html/` (main cPanel account) |
| `FTP_PROTOCOL` | optional. Default `ftps`; set `ftp` only if the host has no FTP over TLS |

4. Run the workflow once from the **Actions** tab, then open https://higherstudyinfo.com.
5. **Google Search Console:** verify with the meta tag (already on every page), then submit `https://higherstudyinfo.com/sitemap.xml`.
