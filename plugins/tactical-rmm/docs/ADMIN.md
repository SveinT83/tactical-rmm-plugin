# Administrator: autentisering og personlige nøkler

## Arkitektur og ansvar

Teknikeren autentiserer sin egen konto mot issuer `https://auth.tronderdata.no/realms/tronderdata` med authorization code, PKCE S256 og eventuell MFA. Eksisterende forhåndsregistrerte klient er `tactical-chatgpt`; nødvendig MCP-scope er `tactical-rmm`.

MCP-endepunktet er `https://tactical-mcp.tronderdata.no/chatgpt/mcp`. Serveren skal validere token for hvert datakall, bruke autentisert, fast Keycloak-`sub` til å finne en personlig Tactical-nøkkel, og utføre Tactical-kallet med denne nøkkelen. Tactical håndhever nøkkelens eiers rettigheter. Dette er eierens oppgitte arkitektur; kildekoden og alle valideringsgrenene er ikke revidert i denne leveransen. Ett vellykket personlig datakall beviser ikke hele arkitekturen eller isolasjon mellom brukere.

Ikke bruk e-post, visningsnavn, chatoppgitt identitet eller Keycloak-token som en Tactical API-nøkkel. Ingen annen persons nøkkel eller felles administratortilgang brukes som reserve for personlig RMM-drift.

Brukeren har utvidet bestillingen: administratorer med verifisert Keycloak-gruppe `management` skal kunne bestille opprettelse og kobling av personlige nøkler via chat. MCP-utviklingschatten rapporterer også selvbetjening for egen konto. Nøkkelverdien håndteres bare på serversiden mellom Tactical og MCP. Tilgangsskillen forbereder disse arbeidsflytene; faktiske MCP-verktøy er ikke verifisert mot kjørende server eller implementert i pluginpakken. Se [kommende serverkontrakt](MCP-ADMIN-CONTRACT.md).

## Status for nøkkeladministrasjon

**Administrasjonsgrensesnittet og MCP-administrasjonsverktøyene er under utvikling. Utrulling er ikke bekreftet.**

Eier oppga serverkilden `/opt/mcp/tacticalrmm` og rutinedokumentasjonen `/opt/mcp/tacticalrmm/DIRECT-CHATGPT.md` på `mcp-services`. Mappen finnes ikke lokalt. Lesende SSH-forsøk fra utviklingsverten ble avvist med `Permission denied (publickey)`. Ingen kilde, hemmelighetsfil eller aktiv nøkkelkobling ble lest eller endret. Det er derfor ingen konkret registreringskommando, administrasjonslenke eller skjermprosedyre som kan oppgis som verifisert her.

Før første nye tekniker tas i bruk må en autorisert serveradministrator gjennomgå gjeldende `DIRECT-CHATGPT.md` via sin etablerte tilgang og bekrefte faktisk administrasjonsrutine. Når management-verktøyene er levert og testet, kan chatten starte den dokumenterte serveroperasjonen; frem til da brukes bare verifisert eksisterende administrasjon. Oppdater denne dokumentasjonen med rutinen når den er verifisert. Ikke be teknikeren levere nøkkelen i ChatGPT.

Følgende er krav til administrasjonen, **ikke en påstått tilgjengelig fremgangsmåte**:

- Registrering må knytte teknikerens personlige Tactical-tilgang til riktig, fast Keycloak-`sub`, gjennom beskyttet serveradministrasjon. Aktørens identitet og målbrukerens identitet må holdes atskilt.
- Utskifting må bevare riktig identitetskobling og stenge gammel nøkkel etter gjeldende rutine.
- Fjerning må stenge tilgangen ved fratredelse eller tilbakekall uten reserveidentitet.
- Hemmeligheter skal ikke havne i terminalhistorikk, åpne logger, Git, pakker eller chat.

MCP må kontrollere autentisert identitet for hver beskyttet tilgangshandling, begrense selvbetjening til egen konto og kreve management-tilgang ved administrasjon av andre. Opprettelse/henting i Tactical og lagring i MCP skal ikke kreve at modellen leser eller sender nøkkelverdien videre. Tilbakekall og delvis feil må ha dokumentert oppførsel. Oppsetts-/adminlenker skal kreve SSO og ikke gi tilgang alene. En statusfunksjon og en bekreftet setup-URL må være tilgjengelig etter SSO også før personlig Tactical-nøkkel er koblet.

Ingen av disse serveroperasjonene implementeres av pluginpakken. Ikke endre aktive ansattes koblinger for testing; bruk egne testidentiteter eller lokale feilsvar.

## OAuth-konfigurasjon

Gjenbruk eksisterende app og klient. Ikke velg DCR eller CIMD, opprett ny klient eller endre produksjonsredirecter som del av denne leveransen. `config/connection.json` er en administratorreferanse med `provided`/`clientId`, ikke en automatisk appregistrering.

Offentlig discovery bekrefter issuer, MCP-resource, scope og S256, samt at issuer annonserer flere metoder for token-endepunktet. Det viser ikke hvilken metode klienten `tactical-chatgpt` faktisk er konfigurert for. Behold eksisterende konfigurasjon; ikke velg en metode på grunnlag av issuerens støtteliste alene. Klientens PKCE-policy, hemmelighet og redirect-liste ble ikke lest. Et faktisk nytt innloggingsforløp er utestet.

Hvis et senere godkjent administratorarbeid krever OAuth-oppsett, bruk [OpenAIs autentiseringsdokumentasjon](https://developers.openai.com/plugins/build/auth), og kopier faktisk redirect-URI fra appens administrasjonsside. Eventuell klienthemmelighet håndteres bare i beskyttet konfigurasjon. Arbeidsområdets tilgang til appen og hver teknikers personlige innlogging er separate forhold.

## Avvisninger

Ved uttrykkelig bekreftet manglende nøkkelkobling brukes:

«Innloggingen er gjennomført, men en administrator må fullføre koblingen til din personlige Tactical RMM-tilgang.»

Generell 403 kan også bety manglende Tactical-rettigheter eller en annen tilgangsbegrensning. Undersøk bekreftet årsak med redigert diagnostikk; ikke vis token, nøkler, rå kommandoer eller unødvendige personopplysninger. Ikke bytt identitet eller tilkobling for å omgå avvisningen.
