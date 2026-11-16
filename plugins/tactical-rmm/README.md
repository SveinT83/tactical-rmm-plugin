# Tactical RMM

Versjon 1.3.0-rc.2 · Trønder Data · teknisk navn `tactical-rmm`.

Selvstendig plugin med eksisterende HTTPS MCP-endepunkt, personlig Keycloak/SSO og tre norske skills. Den tidligere personlige ChatGPT-pluginen er slettet og brukes ikke som avhengighet. Original Tactical RMM-logo følger pakken.

- [Oppsett, SSO og trygg setup-lenke](skills/tactical-rmm-setup/SKILL.md)
- [Tactical-drift og native REST-kontrakter](skills/tactical-rmm/SKILL.md)
- [Personlig tilgang og management-administrasjon](skills/tactical-rmm-admin/SKILL.md)
- [Installasjon, OAuth, arbeidsområde og GitHub-synk](docs/WORKSPACE.md)
- [Nøkkeladministrasjon og testgrenser](docs/ADMIN.md)

Kandidaten bruker MCP 0.4.0s faktiske kontrakt: generell API-oppdagelse/utførelse og seks dedikerte tilgangsverktøy. Kildeinventaret klassifiserer 291 tekniker-REST-operasjoner. Innlogget funksjon og full brukerrettighetsdekning er ikke live-verifisert av pakken. Interaktiv terminal, native livestrømmer og fjernskrivebord krever fortsatt egne sesjonsintegrasjoner i MCP.

## Første installasjon

Administrator konfigurerer eksisterende OAuth-klient `tactical-chatgpt` og eventuell klienthemmelighet i vertens beskyttede oppsett. Ingen hemmelighet følger pakken. Teknikeren bruker deretter egen SSO/MFA. GitHub-import kan ha Desktop only-begrensning; faktisk nettleserinstallasjon må godkjennes før nettleserstøtte påstås.

## Utvikling fra kilde

I repoets rot (`/var/Projects/plugin Tactical RMM` på utviklingsverten):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.lock
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py
.venv/bin/python scripts/prelaunch.py --save
```

Utviklingsskript og testbevis ligger i kilde-repoet, ikke i installasjonsarkivet. Arkivet inneholder én plugin med både `mcp.json` og Codex-kompatibilitet. Opprett/installér bare én logisk forbindelse til samme server, og opprett ingen ny MCP-server eller Keycloak-klient.
