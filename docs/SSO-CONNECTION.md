# SSO fra ChatGPT via Keycloak og eksisterende MCP

Innloggingen skal følge denne kjeden: **ChatGPT → Keycloak → MCP → Tactical RMM**.
Teknikeren skal bare installere pluginen og koble til sin egen jobbkonto.
MCP håndterer personlig Tactical-tilgang på serveren.

«App» i `.app.json` er ChatGPTs registrerte MCP-kontotilkobling. Det er ikke
en ny Tactical-applikasjon eller en ny server. BookStack-pakken bruker denne
typen registrering. En rå MCP-deklarasjon i GitHub-pakken gir foreløpig ikke
samme innlogging i den observerte arbeidsområdeinstallasjonen.

## Administrator gjør dette én gang i ChatGPT

1. Åpne [Plugins](https://chatgpt.com/plugins) i det samme arbeidsområdet som
   den eksisterende Tactical RMM-pluginen. La den importerte pluginen stå.
2. Velg **+ → Add custom MCP server / Legg til egendefinert MCP-server**.
3. Fyll inn **Tactical RMM** som navn og
   `https://tactical-mcp.tronderdata.no/chatgpt/mcp` som serveradresse.
4. Velg **OAuth**. Hvis skjemaet har innstillinger for forhåndsregistrert
   klient, bruk klient-ID `tactical-chatgpt`, tokenmetode `client_secret_basic`
   og scope `tactical-rmm`. Hvis flere scope må skrives i ett felt, bruk
   `openid profile email tactical-rmm`. Eventuell eksisterende klienthemmelighet
   fylles bare inn i ChatGPTs beskyttede felt. Ikke send den i chatten.
5. Fullfør registreringen med **Create as a plugin / Opprett som plugin** og
   personlig SSO dersom ChatGPT ber om det. Dette registrerer tilkoblingen til
   den eksisterende serveren; det oppretter ingen ny MCP-server eller Keycloak-klient.
6. Kopier nettleseradressen til den opprettede MCP-registreringens detaljside og
   send den i utviklingschatten. Den dokumenterte registreringen har en ID som
   begynner med `plugin_asdk_app`. Dette er ikke den GitHub-importerte
   `Plugin_960c953284a0819184889146d979392f`, og ingen hemmelighet skal følge lenken.

Hvis menyvalget ikke finnes, stopp før en annen import opprettes. Beskriv hvilke
valg som faktisk vises. Hvis klienthemmeligheten ikke er tilgjengelig, må
MCP-/Keycloak-administrator legge den inn direkte i det beskyttede feltet.
Ved en redirect-feil må identitetsadministrator godkjenne den eksakte callback-URI-en
ChatGPT viser for den eksisterende klienten, uten å gjette eller bruke jokertegn.

## Utviklingsarbeid etter registreringen

Les registreringens metadata og `.app.json` med Plugin Creator. Kontroller
MCP-adresse, faktisk app-ID, scope og samme arbeidsområde før bindingen endres.
Ikke utled en app-ID fra den GitHub-importerte pluginens ID.

`scripts/bind_app.py` forbereder en kandidat fra en kvittering med disse feltene,
kopiert fra den verifiserte registreringen: `plugin_id`, `scope`, `workspace_id`,
`mcp_url` og `app_manifest`. Kvitteringen skal bare inneholde offentlig metadata.
Skriptet validerer verdier og kandidat, men kan ikke bevise at en oppgitt
registrering finnes; derfor kreves først faktisk kildeavlesning i ChatGPT.

Overgangen bruker BookStacks native format: `.codex-plugin/plugin.json` peker
på `.app.json`; det portable rotmanifestet og begge rå MCP-filer fjernes for
å unngå at de skjuler appkoblingen. Ferdigheter, original logo, standardprompt,
marketplace-identitet og eksisterende arbeidsområdeplugin bevares.

Oppdater også gjeldende versjon, README, installasjonsveiledning og endringslogg
før publisering. Stadielegg tilsiktede filslettinger før validatorens Git-indeksskann.
Kjør `scripts/validate.py`, unittest, bygg og `scripts/check_client.py`.
Klientkontrollen skal finne tre skills, én registrert app med ChatGPT-kontolenke
og ingen parallell MCP-deklarasjon. Dette tester bare pakkekoblingen.

Push den gjennomgåtte endringen til `main`. Synk eksisterende marketplace,
kontroller at arbeidsområdets medlemmer har tilgang til den registrerte
tilkoblingen, og test deretter «Koble til konto» → Keycloak i en ny ChatGPT-chat.
En eventuell ekstra katalogoppføring fra registreringen kan ikke antas å
forsvinne automatisk; ikke slett den underliggende tilkoblingen pakken trenger.
SSO og personlig Tactical-tilgang godkjennes først etter faktiske lesetester.

Kilder: [OpenAIs registreringsflyt](https://developers.openai.com/plugins/build/plugins#create-and-test-a-plugin-locally-with-an-mcp-server),
[GitHub-import og appreferanser](https://learn.chatgpt.com/docs/enterprise/plugin-management#reference-an-existing-app-with-appjson),
[OAuth og eksakt callback](https://developers.openai.com/plugins/build/auth#redirect-url).
