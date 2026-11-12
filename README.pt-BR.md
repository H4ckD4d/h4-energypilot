# H4 EnergyPilot — Inteligência em eficiência energética

**Criador / Creator / Creador: Chris Cruz — [@H4ckD4d](https://github.com/H4ckD4d)**

Projeto aberto com API funcional, demonstração e SEO em três idiomas.

## Why / Por quê / Por qué
Decisões melhores começam com dados de consumo transparentes. Compare consumo, tarifa e cenários em relatórios reproduzíveis, sem prometer economias não verificadas.

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
- [Storytelling](docs/STORYTELLING.pt-BR.md) · [Contributing](docs/CONTRIBUTING.pt-BR.md)

## Limitations
Technical starter, not a production or certified service. No paying customers, rankings, partnerships or service-level guarantees are claimed.

MIT license. **Chris Cruz — @h4ckd4d.**
