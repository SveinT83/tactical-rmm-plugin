# Én Tactical RMM-plugin med SSO og GitHub-synk

Versjon 1.4.0 overtar den registrerte SSO-pluginen
`plugin_asdk_app_6afafd3b578c8191a62956239872dd3b` i Trønder Data-arbeidsområdet.
Markedsplassen bruker denne faktiske `pluginId` og registreringens tekniske navn
`dev-6afafd3b578c8191a62956239872dd3b`. Ingen ekstra wrapper skal opprettes.
Nativt manifest peker til den opprinnelige `.app.json`; rå MCP-deklarasjoner er fjernet.

## Administrator

Synkroniser eksisterende marketplace fra repoet
`https://github.com/SveinT83/tactical-rmm-plugin`, branch `main`, tom Path.
Kontroller importresultatet, samme SSO-plugin-ID, versjon 1.4.0, tre ferdigheter,
original logo og **Tilknyttede kontoer**. Brukeren bekrefter at SSO fungerer før
GitHub-overtakelsen; kontotilkobling etter synk må fortsatt kontrolleres.

Arbeidsområdescope og synlighet er bekreftet med Plugin Creator. GitHub-import
bevarer eksisterende innstillinger; deling og installasjonspolicy administreres
i ChatGPT og påføres ikke automatisk fra repoets policyfelt.

Den tidligere wrapperen `Plugin_960c953284a0819184889146d979392f` har ingen plass i
sluttleveransen. Etter sync blir den etterlatt som **No longer in source**.
Ta den ut av bruk og fjern den gamle oppføringen etter at SSO-pluginen er kontrollert.
Ikke slett hele markedsplassen; det kan slette importerte plugins.
Ikke fjern den nye SSO-pluginen eller dens underliggende kontokobling.

## Ansatte

Installer **Tactical RMM**, velg **Koble til konto** ved behov og fullfør personlig
Keycloak SSO med eventuell MFA. Ingen manuell MCP-registrering eller klienthemmelighet
skal være nødvendig for ansatte. En eksisterende konto skal gjenbrukes.

Når egen Tactical-kobling mangler, bruk den bekreftede beskyttede siden
`https://tactical-mcp.tronderdata.no/admin/`. Management kan klargjøre andre brukere;
vanlige brukere kan bare administrere egen tilgang slik MCP tillater.

OAuth bruker eksisterende `tactical-chatgpt`, tokenmetode `none`, PKCE S256,
issuer `https://auth.tronderdata.no/realms/tronderdata` og scope `tactical-rmm`.
MCPs separate konfidensielle introspeksjonsklient beholdes.

## Oppdatering og tilbakeføring

Fremtidige pakkeoppdateringer går til samme plugin-ID gjennom GitHub `main` og
Sync now. Serverkode distribueres separat. Ikke anta at en pågående chat laster
nye ferdigheter; kontroller i en ny chat. Bevar den kanoniske plugin-ID-en ved
rettelser; ikke opprett en ny plugin eller gå tilbake til den slettede appen.
Ved behov brukes en gjennomgått ny kildeversjon som fortsatt bevarer samme
registrering. Pakketilbakeføring reverserer ikke allerede utførte Tactical-handlinger.

Kilde: https://learn.chatgpt.com/docs/enterprise/plugin-management .
