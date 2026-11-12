# SEO playbook — H4 EnergyPilot

Site builder: `python3 scripts/build_site.py --preview` for local preview (noindex). To publish: configure `SITE_URL=https://YOUR-VERIFIED-DOMAIN` and `SEO_PUBLIC=1`, then run `python3 scripts/build_site.py`.

## Implemented
- HTML content pre-rendered in three distinct languages (`/pt-BR/`, `/en/`, `/es/`), each page with unique title, description and headings.
- Self-canonical and reciprocal hreflang incl. x-default; sitemap `<xhtml:link>` includes self and translations.
- SoftwareApplication structured data with truthful feature claims and no invented ratings/prices.
- Open Graph + Twitter metadata, social preview SVG, favicon, accessible navigation.
- robots.txt disallows indexing until a real HTTPS domain is explicitly configured; canonical and sitemap are also set only for that real domain.
- Sitemap includes localized homepage and about pages (not API routes).

## Manual activation
Do not activate the Pages publishing workflow until both repository variables are set. The workflow is manual (`workflow_dispatch`) by design.

1. Publish the GitHub repository and configure GitHub Pages in repo Settings > Pages > GitHub Actions.
2. Set repository Variables `SITE_URL` (real HTTPS URL, includes path if Pages project site) and `SEO_PUBLIC=1`.
3. Verify generated `dist/robots.txt`, `sitemap.xml`, title, meta robots, self canonical and hreflang.
4. Claim the domain or URL prefix in Google Search Console and optionally Bing Webmaster Tools.
5. Submit `/sitemap.xml` and monitor coverage, performance and Core Web Vitals.
6. Add meaningful localized articles with expert review before scaling programmatic SEO; do not create thin/duplicated pages.

SEO implementation cannot guarantee indexing, ranking, or a particular traffic level.

Note for GitHub **project** Pages: `robots.txt` located under a repository path does not control the origin-wide robots policy. Use the HTML robots directive on all pages until the real site URL is configured; a root-level `robots.txt` requires an origin-level hosting setup.

- Marketing CSS uses system fonts (no third-party font/CDN calls).
