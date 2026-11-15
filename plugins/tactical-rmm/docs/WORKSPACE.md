# Arbeidsområde og nettleser

## Valgt kobling

Hovedpakken har en skill og `.app.json`; den deklarerer ingen server i `mcp.json` eller `.mcp.json`. App-ID-en `asdk_app_6af232dfb75c81919191e1ab5b5fd9c0` er lest fra `.app.json` i eksisterende plugin via Plugin Creator. Den er ikke utledet ved å endre et ID-prefiks.

| Identifikator | Betydning |
| --- | --- |
| `tactical-rmm` | Stabilt teknisk navn på den nye kildepakken |
| `plugin_asdk_app_6af232dfb75c81919191e1ab5b5fd9c0` | Eksisterende **personlig** plugin, scope USER bekreftet |
| `asdk_app_6af232dfb75c81919191e1ab5b5fd9c0` | Verifisert registrert app som pakken refererer til |
| `tactical-chatgpt` | Forhåndsregistrert OAuth-klient hos Keycloak, oppgitt av eier |
| Ny arbeidsområde-plugin-ID | Tildeles ved faktisk arbeidsområdeimport; ikke kjent ennå |

Marketplace oppgir ikke `pluginId`: den personlige pluginen skal ikke brukes som om den allerede tilhører arbeidsområdet. Eksisterende plugin, deling og OAuth-konfigurasjon er ikke endret.

## Administratorsteg før kollegaer kan bruke pakken

Kontroller i riktig arbeidsområde at den **eksisterende** registrerte appen kan gjøres tilgjengelig for aktuelle roller, med eksisterende OAuth-oppsett. Pakken gir ingen nye rettigheter. Behold klienten `tactical-chatgpt`, MCP-scope `tactical-rmm` og personlig autentisering. Hvis brukergrensesnittet krever klienthemmeligheten, må autorisert administrator håndtere den gjennom beskyttet konfigurasjon, uten chat eller Git.

Scope USER er bekreftet for den gamle pluginen; arbeidsområdets tilgang til selve appen er ikke bekreftet. Hvis appen ikke kan gjenbrukes i arbeidsområdet med eksisterende registrering, stans utrullingen og avklar støttet administratormigrering med plattformeier. Ikke registrer en dublettapp, erstatt ID-en med en gjettet verdi eller utvid eksisterende deling som del av pakkeutviklingen. Dersom en annen faktisk app-ID senere godkjennes, oppdater begge dokumentasjonen og validatorens forventede ID etter verifisering.

### GitHub-import

Etter at eier, repo og synlighet er valgt, skal administrator ha lesetilgang fra sin GitHub-konto.

1. Åpne **Admin → Plugins → Add → Import marketplace**.
2. **Source:** faktisk repo-URL. **Path:** tom, siden `.agents/plugins/marketplace.json` ligger under repoets rot. Oppgi eventuell godkjent branch/tag/commit separat.
3. Importer, les resultatrapporten og kontroller navnet **Tactical RMM**, versjonen og appavhengigheten.
4. Sett roller, installasjons- og autentiseringspolicy i arbeidsområdet; repoets policy gjelder lokal testing og erstatter ikke disse innstillingene.
5. La en tekniker koble sin egen konto og gjennomfør en lesende nettlesertest.

[OpenAIs importveiledning](https://learn.chatgpt.com/docs/enterprise/plugin-management) beskriver formatet, tilgangskravene og menyene. Arkivopplasting er ikke hovedløpet for deling; repoimporten gir GitHub-synkronisering.

## Nettleserstøtte: konkret begrensning og akseptanse

OpenAI opplyser at importerte plugins med MCP-serverdeklarasjoner, også eksterne HTTPS-servere, kan bli **Desktop only**. En `.app.json`-referanse alene fjerner ikke denne begrensningen. Se [Desktop-only plugins](https://learn.chatgpt.com/docs/enterprise/plugin-management#desktop-only-plugins).

Appreferansen i denne pakken er den dokumenterte måten å gjenbruke en registrert app på, men er ikke et bevis på at GitHub-importen fungerer i nettleseren. Støtte må bekreftes i det faktiske arbeidsområdet:

- Åpne ChatGPT i nettleseren i riktig arbeidsområde, kontroller installasjon og eventuell **Desktop only**-merking.
- Start en ny chat, velg Tactical RMM og kontroller at både norsk skill og de to MCP-verktøyene er tilgjengelige.
- Fullfør personlig Keycloak-innlogging og eventuell MFA i normal OAuth-flyt.
- Gjør ett avgrenset, bekreftet lesekall, for eksempel versjon. Kontroller resultatet og eventuelle avvisninger.
- Gjenta isolasjonstesten med to egne testidentiteter før flerbrukerisolasjon påstås verifisert.

**Hvis pakken blir Desktop only eller appen er utilgjengelig:** Nettleserleveransen er ikke godkjent. Registrer konkret importdiagnostikk og avklar med arbeidsområde-/plattformadministrator om den eksisterende appen kan gjenbrukes i en støttet webtilgjengelig arbeidsområdeplugin. Skill-pakken kan fortsatt vedlikeholdes i GitHub; ikke lov at den kombinerte pluginen fungerer før ny nettlesertest er bestått. Ikke bytt til en lokal løsning uten å informere brukeren. Denne leveransen endrer ingen registrering, publisering eller deling for å omgå begrensningen.

## Oppdatering og tilbakeføring

Skill- og manifestendringer gjennomgås i Git. Øk `version` i både rotmanifestet og kompatibilitetsmanifestet, og oppdater `CHANGELOG.md`. Kjør validator, tester, bygg og hemmelighetsskanning før push. Nytt innhold i marketplace kan også bli importert; behold kun godkjente oppføringer.

Administrator åpner **Admin → Plugins → Marketplaces**, velger kilden og bruker **Sync now**. Kontroller rapporten også når overordnet status viser fullført. Sjekk versjonen, lastet skill og faktiske verktøy i en ny chat. En pågående chat er ikke garantert å laste nye skills eller verktøy på nytt.

Pakkesynkronisering ruller ikke ut MCP-kode og endrer ikke OAuth eller serverens nøkkeladministrasjon. Nye serververktøy må først være deployet gjennom serverens separate prosess. Les deretter faktisk `tools/list`, vurder skill/parametere og gjennomfør en avgrenset lesetest. Offentlig metadata-probe tester bare katalogen, ikke personlig tilgang.

Lagre kjent fungerende Git-commit og testresultat før oppgradering. Ved feil kan administrator peke importen til den kjente commit-en, eller en gjennomgått Git-revert kan rulle tilbake innholdet med ny, høyere pakkeversjon. Synkroniser og test igjen. Ikke slett marketplace for å rulle tilbake: det kan slette importerte plugins. Gjenoppretting av pluginpakken ruller ikke tilbake MCP-server eller kundemaskinhandlinger.
