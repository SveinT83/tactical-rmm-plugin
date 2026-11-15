# Bekreftet tilkobling og oppsettsadresse

Eksisterende app-ID er `asdk_app_6af232dfb75c81919191e1ab5b5fd9c0`. Den refereres av pakken; plugininstallasjon oppretter ingen ny MCP-server eller Keycloak-klient.

MCP-endepunkt: `https://tactical-mcp.tronderdata.no/chatgpt/mcp`.
Issuer: `https://auth.tronderdata.no/realms/tronderdata`.
Forhåndsregistrert klient: `tactical-chatgpt`.
MCP-scope: `tactical-rmm`.

Bekreftet tjenesteopprinnelse for oppsettslenker: `https://tactical-mcp.tronderdata.no` med vanlig HTTPS-port. Dette bekrefter bare domenet, ikke at en setup-rute finnes. **Ingen setup-/adminsti er foreløpig verifisert.** Hvis MCP bruker en separat administrasjonsopprinnelse, må den verifiseres og legges til dokumentasjonen før lenker dit presenteres som offisielt oppsett.

Hent alltid faktisk sti/URL fra et dokumentert statussvar eller bekreftet administratordokumentasjon. Avvis URL-er med innebygde påloggingsopplysninger, ukjent opprinnelse eller tilgangsgivende hemmeligheter. Ikke gjett en `/setup`- eller `/admin`-adresse.

En vanlig bruker skal bare få egen oppsettsstatus og selvbetjening som serveren tillater. `management` skal kreves ved administrasjon av andre. Begge kontroller må håndheves på serveren ved hver beskyttet forespørsel.
