# Deploying higherstudyinfo.com (cPanel Git Version Control)

`tools/build_site.py` builds the static site into `site/` (home page, one page per dataset, `sitemap.xml`, `robots.txt`, `.cpanel.yml`). Every page's `<head>` includes `tools/site_head.html` (Google site verification + Google Analytics `G-WY2KEFM167`).

On every push to `main` (including the weekly data update), `.github/workflows/deploy.yml` builds the site and commits it to the **`deploy`** branch. cPanel pulls that branch; nothing is pushed to the server from GitHub, so no FTP password is stored anywhere.

## One-time setup

1. **Domain:** point `higherstudyinfo.com` at the cPanel host (the host's nameservers). Skip if the domain was bought from the same host.
2. **SSH key in cPanel:** cPanel → **SSH Access** → **Manage SSH Keys** → **Generate a New Key** (leave the passphrase empty) → **Manage** → **Authorize**. Then **View/Download** the *public* key (`id_rsa.pub`) and copy it.
3. **Deploy key in GitHub:** repo → **Settings** → **Deploy keys** → **Add deploy key** → paste the public key, title `cPanel`, leave *Allow write access* unticked → **Add key**.
4. **Clone in cPanel:** cPanel → **Git™ Version Control** → **Create**:
   - Clone URL: `git@github.com:zahirislam7048/world-scholarships.git`
   - Repository Path: `repositories/world-scholarships`
   - Repository Name: `world-scholarships`
   → **Create**. Then **Manage** → **Basic Information** → Checked-Out Branch: **`deploy`** → **Update**.
5. **First deploy:** **Manage** → **Pull or Deploy** → **Deploy HEAD Commit**. The `.cpanel.yml` in the branch copies the site into `public_html/`. Open https://higherstudyinfo.com.
6. **Google Search Console:** verify with the meta tag (already on every page), then submit `https://higherstudyinfo.com/sitemap.xml`.

## Updating the live site

After the weekly update (or any push to `main`), wait for the **Actions** run to finish, then in cPanel → **Git™ Version Control** → **Manage** → **Pull or Deploy**:
1. **Update from Remote**
2. **Deploy HEAD Commit**
