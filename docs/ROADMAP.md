# H4 EnergyPilot — Commercial readiness backlog

## Implemented
- [x] Accessible marketing page and local demo in three languages
- [x] Canonical URLs, language alternates, static sitemap, robots, JSON-LD, Open Graph tags
- [x] Tenant-filtered API endpoints with admin/editor/viewer roles and SHA-256 token digests
- [x] Automated API and SEO tests
- [x] Dockerfile and isolated, non-root app process
- [x] GitHub Actions tests and optional Pages release

## Blockers for production/commercial scale
- [ ] OIDC enterprise identity and least-privilege role administration
- [ ] Alembic/PostgreSQL migrations, row-level security, secrets vault
- [ ] Distributed queues and rate limits, retries and idempotency
- [ ] Signed audit trail, log retention policy, PII inventory and DPA
- [ ] Usage metering, plan enforcement, invoice and payment webhooks
- [ ] Load and chaos tests, rollback/DR exercises, infrastructure as code
- [ ] Accessibility manual verification, legal review, penetration test and customer pilots
- [ ] Custom domain, Search Console ownership verification and production SEO monitoring

**The repo is complete as a documented MVP starter, NOT a production-ready business SaaS.**
