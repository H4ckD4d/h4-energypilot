# H4 EnergyPilot

**Creator / Criador: Chris Cruz — [@h4ckd4d](https://github.com/H4ckD4d)**

Análise de consumo elétrico e cenários de economia para negócios.

[Português](README.pt-BR.md) · [English](README.en.md) · [Español](README.es.md)

## What works
- Offline-generated, mobile-friendly SEO marketing site with three *real* localizations and a browser demonstration.
- API endpoints for core H4 EnergyPilot workflows, role-based demo tokens, tenant isolation, logs and automated tests.
- GitHub Actions CI, optional GitHub Pages workflow, contributions, Red Team engineering practices and creator storytelling.

## Quick test
```bash
python3 -m pip install -e './apps/api[test]'
./scripts/test-all.sh
```

## GitHub Pages and indexing
Use Settings > Pages > GitHub Actions, set `SITE_URL` (actual public HTTPS site address) and `SEO_PUBLIC=1` as repository variables; see [SEO setup](docs/SEO.md). Preview builds are noindex by design.

**This is a complete MVP repository, not an enterprise-ready SaaS or an accessibility/energy/compliance certification.**

## Browser demo

```bash
python3 scripts/build_site.py --preview
./scripts/serve-site.sh
```

Open `http://127.0.0.1:8080/pt-BR/` locally. The public landing pages and demo can be hosted as static files; no customer data is transmitted to the API by the browser demo.

## Private pilot API

```bash
python3 scripts/bootstrap_keys.py
```

Privately export the generated `H4_TENANTS` environment value, then run `./scripts/dev-api.sh`. API endpoints are available at `http://127.0.0.1:8000/docs` locally, not as a public production service.
