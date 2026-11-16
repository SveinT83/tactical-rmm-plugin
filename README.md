# Tactical RMM

**Trønder Data · 1.4.0 · én SSO-plugin overtatt av GitHub**

Pakken overtar den eksisterende SSO-pluginen i Trønder Data-arbeidsområdet ved
hjelp av `pluginId` i markedsplassen. Den oppretter ingen ekstra wrapper.
Appkoblingen og SSO-identiteten beholdes, sammen med tre norske ferdigheter og
original Tactical RMM-logo. Brukeren bekrefter at personlig SSO fungerer.

| Identitet | Verdi |
| --- | --- |
| Eksisterende SSO-plugin | `plugin_asdk_app_6afafd3b578c8191a62956239872dd3b` |
| Teknisk navn i manifest og markedsplass | `dev-6afafd3b578c8191a62956239872dd3b` |
| Visningsnavn | Tactical RMM |
| App-ID | `asdk_app_6afafd3b578c8191a62956239872dd3b` |
| Git-kilde | `https://github.com/SveinT83/tactical-rmm-plugin`, branch `main`, tom Path |

Det tekniske navnet må samsvare nøyaktig med eksisterende registrering for at
importen skal overta samme plugin. Pluginmappen heter fortsatt `plugins/tactical-rmm`.
En portabel rotmanifest eller rå MCP-deklarasjon kan skjule appkoblingen i den
kontrollerte klienten; pakken bruker derfor bare nativt manifest og `.app.json`.

## Fullføre overgangen

1. Administrator velger **Synkroniser nå** på den eksisterende markedsplassen.
2. Kontroller importresultatet: samme SSO-plugin-ID som over, versjon 1.4.0,
   Tactical-logo, tre ferdigheter og **Tilknyttede kontoer**. Eksisterende konto
   skal beholdes. Git-push alene bekrefter ikke dette.
3. Start en ny chat med denne pluginen og kontroller personlig tilgang med et
   avgrenset lesekall. Ikke bruk kundehandlinger eller nøkkelendringer som test.
4. Den gamle wrapperen `Plugin_960c953284a0819184889146d979392f` blir etterlatt
   som **No longer in source**. Ta den ut av bruk og fjern den gamle oppføringen
   gjennom arbeidsområdets støttede administrasjon etter at ny plugin er kontrollert.
   Ikke slett hele markedsplassen eller den kanoniske SSO-pluginen.

Ansatte skal installere én Tactical RMM-plugin og koble til egen Keycloak-konto.
Management kan klargjøre personlig Tactical-tilgang på MCP-serveren på forhånd.
Hvis en personlig nøkkelkobling mangler, viser skillen den beskyttede oppsettsiden.
Ingen passord, token eller API-nøkler skal inn i chat eller Git.

## Validering og bygg

```bash
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -q
.venv/bin/python scripts/check_client.py
.venv/bin/python scripts/build.py
```

Klientkontrollen skal finne tre ferdigheter, én registrert app med kontolenke og
null separate MCP-servere. Dette kontrollerer pakkekoblingen, ikke fullført
arbeidsområdesynk eller alle brukerrettigheter. Bygget lager én plugin i
`dist/tactical-rmm-1.4.0.zip`. [Migreringsplanen](docs/SINGLE-PLUGIN-MIGRATION.md)
og [SSO-veiledningen](docs/SSO-CONNECTION.md) beskriver kontrollene som gjenstår.

Keycloak bruker den eksisterende offentlige klienten `tactical-chatgpt`,
authorization code og påkrevd PKCE S256, uten klienthemmelighet. MCPs interne
introspeksjonsklient er separat og beholdt.

MCP-koden har egen utrulling. Registrerte native REST-operasjoner er ikke bevis
på full GUI-paritet; interaktive sesjonsintegrasjoner er fortsatt en egen oppgave.
Se [funksjonsdekning](docs/FUNCTIONAL-COVERAGE.md).

Kilde: [OpenAIs GitHub-overtakelse](https://learn.chatgpt.com/docs/enterprise/plugin-management#move-an-existing-plugin-to-github-management).
