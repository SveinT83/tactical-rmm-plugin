# Installere, dele og oppdatere Tactical RMM

## Bekreftet feil ved arbeidsområdeinstallasjon

Versjon 1.3.0-rc.2 ble importert, men viste MCP-server uten «Koble til / Legg til konto». Den faktiske klientkontrollen fant tre skills og ingen registrert app. `1.3.0-rc.3` retter oppsettsteksten og legger til en kontroll som fanger manglende appbinding. SSO-koblingen er fortsatt ikke levert. En vellykket synk eller pakketest er ikke en godkjenning av innlogging.

Behold eksisterende GitHub-styrte arbeidsområdeplugin. Ikke slett marketplace eller installer en ekstra kopi for å feilsøke. For samme kontoflyt som BookStack må en faktisk registrert Tactical-app verifiseres og knyttes til pakken. App-ID må leses fra registreringen; den slettede personlige appen kan ikke gjenbrukes uten ny verifikasjon. Etter binding må faktisk klient vise app og kontolenke; deretter testes SSO i ChatGPT-nettleseren.

## Selvstendig plugin

Pakken deklarerer `https://tactical-mcp.tronderdata.no/chatgpt/mcp` som remote Streamable HTTP MCP. Den har tre norske skills, original Tactical-logo og ingen binding til den slettede personlige ChatGPT-pluginen. En ny eller fortsatt tilgjengelig appregistrering må verifiseres før kontotilkoblingen kan ferdigstilles.

`mcp.json` er den portable konfigurasjonen. `.mcp.json` og `.codex-plugin/plugin.json` er kompatibilitetsfiler for Codex-klienter. Begge beskriver samme logiske forbindelse; de skal ikke opprette to servere. Eksisterende MCP-hosting og autentisering beholdes.

## Én gangs administratoroppsett

Autentiseringskonfigurasjonen bruker den eksisterende forhåndsregistrerte Keycloak-klienten `tactical-chatgpt`, `none` og scope `tactical-rmm`. Issuer er `https://auth.tronderdata.no/realms/tronderdata`. Ikke velg DCR/CIMD eller opprett ny Keycloak-klient.

Klienten er offentlig og krever PKCE S256. Velg tokenautentisering `none` / Ingen og la klienthemmelighet stå tom. Den separate konfidensielle klienten `tactical-mcp-introspection` brukes bare internt av MCP til tokenkontroll og skal ikke endres eller brukes i ChatGPT-skjemaet.

Bruk faktisk redirect-URI som verten viser og som den eksisterende Keycloak-klienten tillater. Ikke gjett eller endre produksjonens callback-liste under pakkeutviklingen. Hvis en ny callback må godkjennes, håndteres det separat av MCP-/identitetsadministrator.

Deretter bruker teknikeren egen SSO, eventuell MFA og samtykke. En manglende personlig Tactical-kobling gir bekreftet status og lenke til `https://tactical-mcp.tronderdata.no/admin/`. Management kan utføre førstegangsoppsett for andre. En vanlig bruker kan legge inn egen nøkkel på den beskyttede siden; ingen nøkkel limes inn i chatten.

## GitHub-import og nettleserstøtte

Repo: `https://github.com/SveinT83/tactical-rmm-plugin`.
Marketplace: `.agents/plugins/marketplace.json`, relativt til repoets rot.
Importgren: `main`, med kandidat 1.3.0-rc.4 for MCP 0.4.0. Kandidatstatus betyr at personlig OAuth og faktisk nettleserinstallasjon fortsatt skal sluttkontrolleres.

Arbeidsområdeadministrator bruker Admin → Plugins → Add → Import marketplace, repo-URL som Source, tom Path og valgt branch/commit. Les importresultatet og sett arbeidsområdets rolle-/installasjons-/autentiseringsinnstillinger. GitHub-import gir ikke automatisk rettigheter i Tactical.

**Viktig plattformgrense:** OpenAI dokumenterer at GitHub-importerte plugins som deklarerer MCP-servere kan merkes Desktop only, også med HTTPS. En lokal CLI-test beviser derfor ikke ChatGPT-nettleserstøtte. Se https://learn.chatgpt.com/docs/enterprise/plugin-management#desktop-only-plugins .

Hvis importen gir Desktop only, er nettleserleveransen ikke godkjent. En ZIP-opplasting er heller ikke bevis på at en registrert OAuth-app eller kontoknapp blir opprettet. Den eksisterende importerte pluginen kan ikke erstattes via Plugin Creator; kildeendringer skal inn gjennom GitHub. ChatGPTs dokumenterte registreringsflyt for en remote MCP-tilkobling er Plugins → Add custom MCP server. Eventuell nødvendig registrering utføres én gang av administrator, med eksisterende MCP-endepunkt og OAuth-klient, før den verifiserte appbindingen legges til i denne pakken. Den enkelte teknikeren skal bare koble til kontoen sin.

Hvis plattformen genererer en appbinding som skal brukes ved videre GitHub-styring, må faktisk app-/arbeidsområde-plugin-ID leses tilbake og verifiseres før den legges i kildepakken. Ikke gjett en ID og ikke anta at en appreferanse alene fjerner Desktop only. En eventuell flytting av eksisterende arbeidsområdeplugin til GitHub må bruke riktig scope og nøyaktig backend-identitet fra det nye oppsettet. Denne registreringen/importen er ikke utført av pakkeutviklingen.

Kilder: https://developers.openai.com/plugins/build/plugins og https://learn.chatgpt.com/docs/enterprise/plugin-management .

## Endelig test i ChatGPT

Kontroller ny installasjon i riktig arbeidsområde og en ny nettlesersamtale: logo, tre skills, onboarding, personlig OAuth, egen koblingsstatus og et avgrenset lesekall. Bruk egne testidentiteter for management og vanlig rolle før isolasjon påstås verifisert. Skrive-/nøkkeltester krever avtalt testmiljø; kundemaskiner og aktive ansattes koblinger brukes ikke som generell tilkoblingstest.

## Sync og tilbakeføring

Oppdater manifestversjoner, endringslogg og dokumentasjon samlet, og kjør lokale tester før push til `main`. Administrator bruker Admin → Plugins → Marketplaces → valgt kilde → Sync now, leser rapporten og kontrollerer versjon, skills og faktisk verktøykatalog i en ny chat. Lokale, upubliserte endringer kan ikke hentes ved synk. En vellykket synk oppretter ikke den manglende OAuth-appregistreringen. Pågående samtaler er ikke garantert å laste nye komponenter på nytt.

MCP-koden har separat utrulling. En pluginoppdatering erstatter ikke backend eller endrer personlige nøkler. Ved serverendring må katalog, skjema og relevante lesekall kontrolleres igjen.

Lagre kjent fungerende commit og testresultat før oppgradering. Rull eventuelt tilbake kilde med en gjennomgått revert og ny pakkeversjon, eller importer kjent commit etter vertens støttede flyt. Synkroniser og test igjen. Ikke slett marketplace som tilbakeføring; det kan slette importerte plugins. Tilbakeføring av pakken reverserer ikke allerede utførte Tactical-handlinger.
