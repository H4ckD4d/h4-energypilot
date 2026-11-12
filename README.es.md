# H4 EnergyPilot — Inteligência em eficiência energética

**Criador / Creator / Creador: Chris Cruz — [@H4ckD4d](https://github.com/H4ckD4d)**

Proyecto abierto con API inicial funcional, demo y SEO multilingüe.

## Why / Por quê / Por qué
Las mejores decisiones energéticas empiezan con datos transparentes. Compare consumo, tarifas y escenarios en informes reproducibles sin prometer ahorros no verificados.

## Start / Iniciar / Empezar

```bash
python3 -m pip install -e './apps/api[test]'
python3 -m pytest apps/api/tests -q
python3 scripts/build_site.py --preview
python3 scripts/check_seo.py site/dist
```

API (`H4_TENANTS` with SHA-256 demo credentials) must be configured before use. Run `python3 scripts/bootstrap_keys.py` locally; never commit output.

## Documentation
- [Architecture](docs/ARCHITECTURE.md) · [SEO](docs/SEO.md) · [Roadmap](docs/ROADMAP.md)
- [Storytelling](docs/STORYTELLING.es.md) · [Contributing](docs/CONTRIBUTING.es.md)

## Limitations
Technical starter, not a production or certified service. No paying customers, rankings, partnerships or service-level guarantees are claimed.

MIT license. **Chris Cruz — @h4ckd4d.**
