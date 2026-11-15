# Tactical RMM

Versjon 1.3.0-rc.1 · Trønder Data · teknisk navn `tactical-rmm`.

Pluginen inneholder norske skills for oppsett, drift og personlig tilgang, samt en referanse til eksisterende Tactical RMM-app. Den bruker personlig Keycloak-innlogging, eventuell MFA og egne Tactical-rettigheter. Gi en avgrenset bestilling med kunde, lokasjon og maskin. Skillene oppdager faktiske verktøy og parameterkrav, respekterer eksisterende godkjenningsregler og rapporterer faktisk resultat.

**Utrullingsstatus:** Arbeidsområdets tilgang til appen, faktisk GitHub-import og ChatGPT-nettleserbruk er utestet. En `.app.json`-referanse beviser ikke nettleserstøtte. MCP 0.3.2 annonserer tilgangsverktøyene, og setup-siden `/admin/` er bekreftet. Innlogget funksjon, rolleisolasjon og faktisk nøkkellivssyklus er ikke testet fra denne chatten.

- [Arbeidsområde, GitHub-import, nettlesertest, Sync now og tilbakeføring](docs/WORKSPACE.md)
- [OAuth og administratorens nøkkelkobling](docs/ADMIN.md)
- [Norsk driftsskill](skills/tactical-rmm/SKILL.md)
- [Oppsettsskill](skills/tactical-rmm-setup/SKILL.md), registrert som onboarding: SSO og bekreftede setup-lenker uten nøkkelverdier i chatten.
- [Administrasjonsskill](skills/tactical-rmm-admin/SKILL.md) for kommende management-verktøy: bestill opprettelse og kobling av personlig tilgang uten at nøkkelverdien går gjennom chatten.
- [Krav til kommende MCP-administrasjon](docs/MCP-ADMIN-CONTRACT.md); katalog og kilde er gjennomgått, mens innlogget funksjon gjenstår å teste.
- [Original Tactical RMM-logo](assets/README.md), brukt som pluginlogo og ikon.

## Lokal utvikling fra kilde

I kilde-repoets rot (`/var/Projects/plugin Tactical RMM` på utviklingsverten):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.lock
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py
```

Utviklingsskript og testbevis ligger i kilde-repoet; de er ikke kjøretidskrav eller del av installasjonsarkivet. Fra samme vert som Codex-klienten kan kilde-marketplace registreres med `codex plugin marketplace add '/var/Projects/plugin Tactical RMM' --json` og pluginen installeres med `codex plugin add tactical-rmm@tronder-data-tactical-rmm --json`. Kontroller verktøy og skill i en ny chat før et avgrenset lesekall.

Ikke send API-nøkler, klienthemmeligheter eller token i chatten. Pluginpakken oppretter ingen server eller OAuth-klient. MCP-serverkode har separat utrulling.
