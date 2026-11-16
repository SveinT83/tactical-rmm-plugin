# Tactical RMM

**Trønder Data · 1.3.0-rc.4 · testkandidat mot MCP 0.4.0**

Pluginpakke med tre norske skills og deklarasjon av eksisterende `https://tactical-mcp.tronderdata.no/chatgpt/mcp`. Den slettede personlige ChatGPT-pluginen brukes ikke som avhengighet. Ingen ny MCP-server eller Keycloak-klient opprettes.

**Kjent installasjonsfeil:** Arbeidsområdeimporten viser MCP-server og skills, men mangler «Koble til / Legg til konto». Versjon 1.3.0-rc.3 retter veiledningen; den oppretter ikke SSO-koblingen. BookStack bruker en registrert app som denne pakken foreløpig mangler. Eksisterende arbeidsområdeplugin skal beholdes. Faktisk Tactical-appregistrering må verifiseres før den kan bindes til pakken; ikke bruk den slettede appens ID.

[Konkret engangsoppsett for administrator og overgang til BookStacks koblingsformat](docs/SSO-CONNECTION.md). Utviklingsverktøyene støtter nå denne overgangen; aktiv pakke endres først når den faktiske MCP-registreringen er lest tilbake.

Repo: [SveinT83/tactical-rmm-plugin](https://github.com/SveinT83/tactical-rmm-plugin). Kandidaten distribueres fra `main` for import i ChatGPT. Versjonen er fortsatt en testkandidat; personlig OAuth og nettleserflyt sluttkontrolleres ved installasjon.

## Innhold

- `plugins/tactical-rmm/plugin.json`: portabel identitet, versjon, logo og onboarding.
- `plugins/tactical-rmm/mcp.json`: eksisterende remote MCP og dokumentert OpenAI OAuth-konfigurasjon.
- `.codex-plugin/plugin.json` og `.mcp.json` inne i pluginmappen: Codex-kompatibilitet for samme logiske tilkobling.
- `skills/tactical-rmm-setup`, `skills/tactical-rmm` og `skills/tactical-rmm-admin`: oppsett, drift og personlig tilgang.
- `.agents/plugins/marketplace.json`: repo-marketplace for arbeidsområdeimport.
- `docs/`, `scripts/` og `tests/`: testbevis og utviklingsverktøy; ikke en ny server.

Original Tactical RMM-logo følger pakken med kilde og sjekksum. Nøkler, token og OAuth-klienthemmelighet følger aldri kilde eller arkiv.

## Før installasjon

Administrator må først få den registrerte ChatGPT-appkoblingen på plass, med den eksisterende OAuth-klienten `tactical-chatgpt` uten klienthemmelighet, med PKCE S256. Pakken beskriver `provided` og `none`; den oppretter ikke en ny klient og kan ikke erstatte appregistrering eller beskyttet hemmelighetskonfigurasjon. Målet er at teknikeren deretter bruker egen SSO/MFA og samtykke via kontoknappen.

Mangler personlig Tactical-kobling, viser skillen bekreftet forklaring og lenken `https://tactical-mcp.tronderdata.no/admin/`. Management kan klargjøre ansatte slik at de bare trenger SSO. Første nøkkel for en vanlig bruker registreres direkte på den beskyttede siden eller av management, aldri gjennom chatten.

GitHub-import kan bli merket **Desktop only** selv med HTTPS MCP. Nettleserstøtte kan derfor ikke godkjennes fra en lokal test. [Installasjonsveiledningen](plugins/tactical-rmm/docs/WORKSPACE.md) beskriver arbeidsområdeimport, én gangs OAuth-oppsett og nødvendig støttet webflyt hvis importen blir Desktop only. Ingen ChatGPT-opplasting er gjort av dette prosjektet.

## Tester og bygg

Python 3.10+ brukes bare til utvikling:

```bash
cd '/var/Projects/plugin Tactical RMM'
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.lock
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py
.venv/bin/python scripts/check_client.py
.venv/bin/python scripts/prelaunch.py --save
```

Arkiv: `dist/tactical-rmm-1.3.0-rc.4.zip`, med SHA-256-fil. Det inneholder én plugin. Bygget leser arkivet tilbake og skanner kilde, Git-indeks og arkiv for kjente hemmelighetsmønstre.

[Schema-notatet](schemas/README.md) forklarer separat kontroll av portable transportfelt og OpenAIs dokumenterte OAuth-utvidelse. Ingen full ChatGPT-import eller personlig OAuth-flyt er påstått bestått av skjemakontroll.

Lokal Codex-installasjon kan gjøres med:

```bash
codex plugin marketplace add '/var/Projects/plugin Tactical RMM' --json
codex plugin add tactical-rmm@tronder-data-tactical-rmm --json
codex plugin list --marketplace tronder-data-tactical-rmm --json
```

`check_client.py` bruker faktisk klient uten å installere eller logge inn. Den skal finne tre skills, én registrert app med ChatGPT-kontolenke og ingen separat MCP-server. Den feiler foreløpig fordi appbindingen mangler; beståtte pakketester opphever ikke denne feilen. Kontroller faktiske verktøy i en ny chat etter at appbindingen er rettet. Ingen kundekommandoer, patching, restart eller nøkkelendringer brukes som generell tilkoblingstest. [Før-lanseringsrapporten](docs/PRELAUNCH.md) skiller lokale pakketester, isolerte serverkildetester, lesende live-kontroller og tester som fortsatt gjenstår.

## Funksjonsdekning

Skillene bruker de faktiske search/execute-verktøyene og de seks access-verktøyene, inkludert native body/query, filer, idempotens, kontovalg og strukturerte feil. Kildeinventaret er kontrollert: 328 operasjoner, 291 klassifiserte tekniker-REST-operasjoner og 37 begrunnede eksklusjoner. Registrert kontrakt betyr ikke at alle produksjonsoperasjoner eller brukerrettigheter er testet.

Målet er at brukeren skal kunne gjøre alt vedkommende har rettigheter til i Tactical RMM. Interaktiv terminal, native livestrømmer og fjernskrivebord mangler fortsatt egne sesjonsintegrasjoner i MCP; dette er ikke skjult av en skill. Se [dekningsoversikten](docs/FUNCTIONAL-COVERAGE.md).

## GitHub, oppdatering og tilbakeføring

For import: Source `https://github.com/SveinT83/tactical-rmm-plugin`, tom Path og Branch `main`. Arbeidsområdeadministrator setter roller, installasjons- og autentiseringspolicy i ChatGPT.

Oppdater begge manifester, konfigurasjoner og endringslogg samlet. Kjør tester før push, og bruk deretter **Sync now** i arbeidsområdets marketplace-administrasjon. Kontroller rapport, versjon og faktiske skills/verktøy i en ny chat; en pågående samtale kan kreve ny oppstart.

MCP-koden har separat utrulling. Pakkesynk endrer ikke serverkode, personlige nøkkelkoblinger eller allerede utførte handlinger. Lagre kjent fungerende commit før oppgradering; bruk en gjennomgått revert/ny pakkeversjon eller støttet import av kjent commit ved tilbakeføring. Ikke slett marketplace som rollback.

Kilder: [OpenAI-pakkeformat](https://developers.openai.com/plugins/build/plugins), [GitHub-import](https://learn.chatgpt.com/docs/enterprise/plugin-management), [OAuth](https://developers.openai.com/plugins/build/auth). Prosjektspesifikke kilde-/live-observasjoner finnes i testrapporten.
