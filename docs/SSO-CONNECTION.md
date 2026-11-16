# SSO fra ChatGPT via Keycloak og eksisterende MCP

Flyt: **Tactical RMM-plugin → personlig Keycloak SSO → MCP → Tactical RMM**.
Registreringen er allerede opprettet og delt med Trønder Data. Ingen ansatt
skal opprette en egendefinert MCP-server eller håndtere klienthemmelighet.

Kanonisk SSO-plugin:
`plugin_asdk_app_6afafd3b578c8191a62956239872dd3b`.
Den er verifisert som `WORKSPACE` og `LISTED` i riktig arbeidsområde.
Brukeren har bekreftet fungerende personlig innlogging før GitHub-overtakelsen.

Kildeversjon 1.4.0 overtar denne samme pluginen med marketplace-`pluginId`.
Det er ingen separat GitHub-wrapper i sluttleveransen. Administrator synkroniserer
fra `main`, kontrollerer samme plugin-ID og tilknyttet konto, og tar deretter den
gamle wrapperen ut av bruk. Se [migreringsplanen](SINGLE-PLUGIN-MIGRATION.md).

Faktisk klient har returnert denne kontolenken:
[Koble til Tactical RMM](https://chatgpt.com/apps/mcp---tactical-rmm/asdk_app_6afafd3b578c8191a62956239872dd3b).
En eksisterende konto skal gjenbrukes; en ny bruker velger Koble til og fullfører
egen Keycloak-innlogging med eventuell MFA. Dette erstatter ikke MCPs personlige
Tactical-nøkkelkobling. Management kan klargjøre den på forhånd.

OAuth-klienten er `tactical-chatgpt`, offentlig authorization-code-klient med
påkrevd PKCE S256 og tokenautentisering `none`. Scope er `tactical-rmm`, med
OIDC-identitetsscope `openid profile email` og valgfri `offline_access`.
Callback er den eksisterende eksakte
`https://chatgpt.com/connector_platform_oauth_redirect`.
Introspeksjon bruker egen konfidensiell serverklient og er beholdt.

Manglende personlig Tactical-kobling håndteres på den beskyttede siden
`https://tactical-mcp.tronderdata.no/admin/`. API-nøkler, token og passord skal
ikke inn i chat, kilde eller verifikasjonsrapporter.

Kilder: [GitHub-overtakelse](https://learn.chatgpt.com/docs/enterprise/plugin-management),
[OAuth](https://developers.openai.com/plugins/build/auth).
