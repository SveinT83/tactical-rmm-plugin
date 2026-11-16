# Én Tactical RMM-plugin med SSO og GitHub-oppdateringer

## Verifisert nå

Brukeren har delt den eksisterende SSO-pluginen til arbeidsområdet. Plugin Creator
bekrefter scope `WORKSPACE`, discoverability `LISTED` og workspace-ID
`c32d88fa-1324-44b1-9fce-9d7a166164a4`. Ingen ny plugin er opprettet av migreringen.

| Identitet | Verifisert verdi |
| --- | --- |
| Kanonisk plugin-ID | `plugin_asdk_app_6afafd3b578c8191a62956239872dd3b` |
| Teknisk navn | `dev-6afafd3b578c8191a62956239872dd3b` |
| App-ID | `asdk_app_6afafd3b578c8191a62956239872dd3b` |
| Release før GitHub-overtakelse | `PluginRelease_9e484e010ab8819183571e5bfec67887`, versjon 1.0.0 |

Kildemetadata og `.app.json` er lest direkte og registrert i
[evidensfilen](evidence/sso-registration.json). Brukeren bekrefter fungerende
personlig SSO. Keycloak er offentlig klient med påkrevd PKCE S256 og ingen
klienthemmelighet. Eldre personlige/deklarerte klientreferanser skal ikke brukes.

## Klargjort GitHub-kilde

Versjon 1.4.0 bruker den kanoniske pluginens faktiske ID som marketplace-`pluginId`.
Marketplace- og manifestnavn samsvarer nøyaktig med registreringen. Visningsnavnet
blir Tactical RMM. Samme appbinding er bevart; tre ferdigheter og original logo
følger kilden. Ingen ekstra wrapper eller rå MCP-deklarasjon er med.

Den tidligere wrapper-hjelperen `scripts/bind_app.py` er fjernet. Validatoren
avviser manglende/feil `pluginId`, en annen teknisk identitet, personlig/feil
arbeidsområde, andre app-ID-er og ekstra marketplace-oppføringer.

## Gjenstående handlinger i arbeidsområdet

1. Administrator bruker **Synkroniser nå** på eksisterende marketplace, branch `main`.
2. Les importresultatet. Det må vise at samme eksisterende SSO-plugin-ID nå
   styres fra GitHub. Kontroller versjon 1.4.0, visningsnavn, logo, tre ferdigheter
   og tilknyttet konto. En kilde-push eller lokal klientkontroll er ikke denne testen.
3. Test et avgrenset lesekall med den kanoniske pluginen i ny chat.
4. Ta gammel wrapper `Plugin_960c953284a0819184889146d979392f` ut av bruk og fjern
   den gamle oppføringen gjennom støttet administrasjon. Den etterlates som
   **No longer in source**, og slettes ikke automatisk ved synk. Ikke slett hele
   markedsplassen eller den kanoniske SSO-pluginen/kontokoblingen.
5. Kontroller at ansatte bare finner og bruker én Tactical RMM-plugin. Bekreft
   personlig kontotilkobling og Tactical-rettigheter med testidentiteter.

Verktøyene her kan ikke utføre workspace-sync eller slette/deaktivere en hel
arbeidsområdeoppføring. Disse handlingene er ikke rapportert utført. Installerte
kopier og arbeidsområdeoppføringer er ulike; en personlig avinstallering alene
ville ikke oppfylle målet om én oppføring for alle ansatte.

Kilde: https://learn.chatgpt.com/docs/enterprise/plugin-management#move-an-existing-plugin-to-github-management .
