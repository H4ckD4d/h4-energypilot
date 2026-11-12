# H4 EnergyPilot — Architecture

**Creator: Chris Cruz (@h4ckd4d)**

- `site/`: pre-rendered crawlable multilingual marketing pages; static and CDN-friendly.
- `apps/api/`: Python FastAPI + SQLAlchemy with a scoped resource store, audit events, SHA-256 demo token authentication, roles admin/editor/viewer.
- `scripts/build_site.py`: static page and SEO asset generation from explicit configuration.
- `scripts/check_seo.py`: consistency validation of canonicals, hreflang, robots and sitemap.
- `scripts/publish-all.sh`: creates separate GitHub repositories using a user's authenticated gh CLI.

## Security boundary
Marketing pages do not invoke private APIs; on-page calculators are client-side synthetic demonstrations. API is private pilot code, not a production internet endpoint. There is no external crawling or third-party data exfiltration.

## Growth path
PostgreSQL migrations + database row-level policies, enterprise OIDC, signed audit log, background jobs, quotas, billing and subscription entitlements, monitoring, multi-zone backup/restores, load testing and support SLOs.
