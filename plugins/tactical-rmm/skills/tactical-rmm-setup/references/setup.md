# Bekreftet tilkobling og oppsettsadresse

Eksisterende app-ID er `asdk_app_6af232dfb75c81919191e1ab5b5fd9c0`. Den refereres av pakken; plugininstallasjon oppretter ingen ny MCP-server eller Keycloak-klient.

MCP-endepunkt: `https://tactical-mcp.tronderdata.no/chatgpt/mcp`.
Issuer: `https://auth.tronderdata.no/realms/tronderdata`.
Forhåndsregistrert klient: `tactical-chatgpt`.
MCP-scope: `tactical-rmm`.

Bekreftet oppsettsadresse: `https://tactical-mcp.tronderdata.no/admin/`. Den er dokumentert i MCP-kilden og dens uautentiserte innloggingsside er lest over HTTPS. Dette beviser ikke at en bestemt bruker er innlogget eller har en gyldig kobling. Bekreftet tjenesteopprinnelse er `https://tactical-mcp.tronderdata.no` med vanlig HTTPS-port. Hvis MCP senere bruker en annen opprinnelse, må den verifiseres før lenker dit presenteres som offisielt oppsett.

Bruk den bekreftede adressen over eller en nyere, verifisert URL fra dokumentert statussvar/administratordokumentasjon. Avvis URL-er med innebygde påloggingsopplysninger, ukjent opprinnelse eller tilgangsgivende hemmeligheter. Ikke gjett andre setup-ruter.

En vanlig bruker skal bare få egen oppsettsstatus og selvbetjening som serveren tillater. `management` skal kreves ved administrasjon av andre. Begge kontroller må håndheves på serveren ved hver beskyttet forespørsel.

`tactical-rmm_access_users` viser koblingsstatus; `mapped` bekrefter bare lagret kobling, ikke full Tactical-tilgang. Vanlig bruker uten verifisert første kobling registrerer nøkkelen på siden eller får hjelp av management. Førstegangsopprettelse via serverens privilegerte nøkkelfunksjoner krever riktig fullmakt; e-postlikhet alene er ikke nok.
