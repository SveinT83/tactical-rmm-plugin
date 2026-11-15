# Tactical RMM

Pluginpakke fra **Trønder Data**, versjon **1.3.0-rc.1**, med norsk oppsetts-, drifts- og tilgangsskill og gjenbruk av eksisterende Tactical RMM-app. Teknisk navn er `tactical-rmm`.

Pakken er laget for import gjennom arbeidsområdets GitHub-marketplace. Den oppretter ingen MCP-server, Keycloak-klient eller ny app. Endepunktet er `https://tactical-mcp.tronderdata.no/chatgpt/mcp`, og teknikeren bruker egen Keycloak-innlogging og egne Tactical-rettigheter.

Testkandidaten utvikles på grenen `test/mcp-0.3.2`; `main` beholdes som 1.2.0 frem til gjennomgang. Før-lanseringstesten er ikke en lanseringsgodkjenning.

Offentlig kilde-repo: [SveinT83/tactical-rmm-plugin](https://github.com/SveinT83/tactical-rmm-plugin).
Ved arbeidsområdeimport brukes **Source** `https://github.com/SveinT83/tactical-rmm-plugin`, tom **Path** og **Branch** `main`. Marketplace-filen er `.agents/plugins/marketplace.json` i repoets rotstruktur. Import og nettleserbruk er fortsatt ikke testet.

**Status:** Lokal kilde og installasjonsarkiv er levert. Eksisterende personlig app er testet med ett avgrenset datakall. Tilgang til appen i arbeidsområdet, faktisk GitHub-import og ChatGPT-nettleserbruk er ikke verifisert. `.app.json` gir ikke i seg selv nettleserstøtte. Se [teststatus](docs/VERIFICATION.md) og [nettleser og arbeidsområde](plugins/tactical-rmm/docs/WORKSPACE.md).

## Innhold

```text
.agents/plugins/marketplace.json   # Marketplace for hele repoet
plugins/tactical-rmm/
  plugin.json                     # Agent Plugins 1.0, versjon og presentasjon
  .codex-plugin/plugin.json       # Synkronisert kompatibilitetsmanifest
  .app.json                       # Verifisert eksisterende app-ID
  assets/                         # Original Tactical RMM-logo og kildehenvisning
  README.md                       # Bruk og utvikling fra kilde
  docs/                           # Arbeidsområde og administrator
  skills/tactical-rmm/            # Norsk skill, referanse og agentmetadata
  skills/tactical-rmm-admin/      # Kommende management-flyt uten rånøkler i chat
  skills/tactical-rmm-setup/      # Onboarding, SSO og bekreftede setup-lenker
config/connection.json            # Administratorreferanse, ikke ny tilkobling
docs/                            # Bevis og teststatus
schemas/                         # Offisiell manifest-JSON-schema for offline-test
scripts/                         # Validering, offentlig metadata-probe og bygg
tests/                           # Pakketester, kommando-skjema og syntetiske feilsvar
```

`dist/` genereres lokalt og skal ikke spores i Git. ZIP-filen inneholder én plugin med skjulte kompatibilitetsfiler; marketplace-filen ligger i repoet og skal ikke ligge i pluginarkivet.

## Lokal validering og bygging

Krever Python 3.10 eller nyere. Python er bare utviklingsverktøy; pluginen har ingen lokal server eller kjøretidsavhengighet.

```bash
cd '/var/Projects/plugin Tactical RMM'
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.lock
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py
```

Arkiv: `dist/tactical-rmm-1.3.0-rc.1.zip`, med separat SHA-256-fil. Bygget validerer kilde og leser tilbake arkivet. Skjemavalideringen bruker den medfølgende offisielle schema-filen; nettverk er ikke nødvendig etter installasjon av utviklingsavhengighetene. Hemmelighetsskanningen dekker kildefiler, Git-sporede filer og innholdet i Git-indeksen. Den er regelbasert og erstatter ikke gjennomgang før push.

Valgfri, lesende offentlig metadata-test:

```bash
.venv/bin/python scripts/probe.py
# Oppdater det versjonerte metadataøyeblikksbildet etter gjennomgang:
.venv/bin/python scripts/probe.py --save
```

Proben leser OAuth-discovery, MCP-initialisering og `tools/list`. Den gjør ingen `tools/call`, krever ingen nøkler/token og tester ikke personlig OAuth. Nye verktøy listes som krav om gjennomgang; manglende basisverktøy eller avvikende OAuth-metadata gir feil. Nye funksjoner blir ikke godkjent automatisk av proben.

## Test med Codex

Fra en terminal på samme vert som Codex-klienten:

```bash
codex plugin marketplace add '/var/Projects/plugin Tactical RMM' --json
codex plugin add tactical-rmm@tronder-data-tactical-rmm --json
codex plugin list --marketplace tronder-data-tactical-rmm --json
```

CLI-kommandoene er kontrollert mot `codex-cli 0.167.0`. Hvis den lokale klienten har en annen versjon, les `codex plugin --help`. Test i en ny chat, velg Tactical RMM og kontroller at skillen og appverktøyene faktisk vises. En lokal pakkeinstallasjon beviser ikke at appen er tilgjengelig eller autentisert. Bruk vanlig beskyttet OAuth-flyt for samme bruker dersom verten ber om innlogging.

Start med «Finn endepunktet for Tactical-versjon, og les versjonen uten å gjøre endringer». Katalogen bekreftet `core.core-version` som GET `/core/version/` under leveransen, men finn det på nytt før bruk. Ikke kjør kommandoer, skript, restart eller patching som test. [Mocks og testgrenser](docs/VERIFICATION.md) beskriver feilsituasjonene.

## Arbeidsområde, bruk og oppdateringer

1. Gjennomgå endringer og push til `main` i [SveinT83/tactical-rmm-plugin](https://github.com/SveinT83/tactical-rmm-plugin). Repoet er offentlig etter eierens uttrykkelige valg, og lokal `origin` peker til dette repoet.
2. En arbeidsområdeadministrator importerer repoet og kontrollerer apprettigheter etter [arbeidsområdedokumentasjonen](plugins/tactical-rmm/docs/WORKSPACE.md).
3. Hver tekniker autentiserer sin egen konto. Administrator fullfører eventuell personlig nøkkelkobling på serversiden etter [administratordokumentasjonen](plugins/tactical-rmm/docs/ADMIN.md).
4. Ved drift: finn riktig kunde, lokasjon og maskin, gi en avgrenset bestilling og kontroller rapportert resultat. Skillen følger vertens godkjenningsregler.
5. Ved endring: oppdater versjon i begge manifester, endringslogg og relevante bevis; kjør tester og bygg før push. Bruk arbeidsområdets **Sync now**, les rapporten og kontroller ny versjon, skill og verktøy i en ny chat. [Oppdatering og tilbakeføring](plugins/tactical-rmm/docs/WORKSPACE.md) beskriver resten.

Pluginpakken distribuerer instruksjoner og appreferanse. MCP-serverens kode og nøkkelkoblinger har separat drift og utrulling.

## Kommende administrasjon fra chat

Tilgangsskillen forbereder bestillinger om egen tilgang og management-administrasjon av andre, som «Opprett og koble Tactical-tilgang for Ola». MCP må kontrollere egen identitet ved selvbetjening og `management` fra betrodd SSO-identitet ved administrasjon av andre, opprette/hente nøkkelen i Tactical og lagre den på riktig bruker direkte på serversiden. Verken tool-input, tool-output eller samtalen skal inneholde selve nøkkelverdien. Chatten mottar bare status og eventuelt en SSO-beskyttet administrasjonslenke.

MCP 0.3.2 annonserer de seks faktiske tilgangsverktøyene, og den beskyttede adressen `https://tactical-mcp.tronderdata.no/admin/` er bekreftet i kilde og ved HTTPS-lesing av innloggingssiden. Innlogget funksjon og nøkkellivssyklus er ikke testet fra denne chatten. Skillen implementerer ingen serverfunksjon. [Serverkravene](plugins/tactical-rmm/docs/MCP-ADMIN-CONTRACT.md) beskriver hva som må leveres og testes før flyten kan brukes. Ingen aktive brukere eller nøkler er endret.

## Førstegangsoppsett og logo

`onboardingSkill` er satt i begge manifester og peker til oppsettsskillen. Den forklarer SSO, kontrollerer faktisk tilgjengelige statusfunksjoner og viser bare en verifisert, beskyttet setup-URL ved manglende personlig kobling. Den kildebekreftede setup-stien er `/admin/`. Verten styrer når oppsett og OAuth-dialog startes; automatisk oppstart og nettleserstøtte må testes i riktig arbeidsområde.

Original Tactical RMM-logo er lagt inn uendret som både `logo` og `composerIcon`, med [kilde og sjekksum](plugins/tactical-rmm/assets/README.md). Se [MCP-status og konkret videre arbeid](docs/MCP-HANDOFF.md) for det som er undersøkt og det MCP må bekrefte.

## Kilder

Kontrollert 14. november 2026: [OpenAI-pakkeformat](https://developers.openai.com/plugins/build/plugins), [GitHub-import og synkronisering](https://learn.chatgpt.com/docs/enterprise/plugin-management), [OAuth](https://developers.openai.com/plugins/build/auth), [Agent Plugins-schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). Prosjektspesifikke observasjoner og begrensninger finnes i [verifikasjonsrapporten](docs/VERIFICATION.md).

## Før lansering

Kjør `.venv/bin/python scripts/prelaunch.py --save` for pakke-, katalog-, innloggingsside- og OAuth-avvisningstester. Skriptet aksepterer ingen legitimasjon, gjør ingen skrivekall og leser ingen svarbody fra tilgangsverktøyene. Det beviser ikke personlig SSO eller rettighetsisolasjon. Se [før-lanseringstesten](docs/PRELAUNCH.md) og [funksjonsdekningen](docs/FUNCTIONAL-COVERAGE.md).

Funksjonsmålet er at enhver bruker skal kunne utføre alt vedkommende har rettigheter til i Tactical RMM gjennom MCP. Hele funksjonsflaten må dokumenteres og testes; åtte MCP-verktøy og en generell API-katalog er ikke bevis på full dekning.
