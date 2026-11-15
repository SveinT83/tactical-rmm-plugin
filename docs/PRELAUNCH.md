# Før-lanseringstest mot MCP 0.3.2

Testkandidat: `1.3.0-rc.1` på grenen `test/mcp-0.3.2`. `main` beholder 1.2.0. Ingen lansering eller import i arbeidsområdet er godkjent av denne testen.

## Utført her

`scripts/prelaunch.py --save` kontrollerer pakken, leser offentlig OAuth-/MCP-metadata og validerer verktøyskjemaene. Det leser den offentlige innloggingssiden, kontrollerer OAuth-avvisning for access users/keys uten legitimasjon og kontrollerer at intern admin-backend ikke er offentlig tilgjengelig.

Fem automatiserte kontroller bestod mot server `0.3.2-admin-repair`. Rapporten ligger i [evidence/prelaunch-readonly.json](evidence/prelaunch-readonly.json). Ingen nøkkeloperasjoner, kundedata eller maskinhandlinger ble kjørt. Testskriptet aksepterer ingen token/nøkkel, følger ikke redirects for disse kontrollene og leser ikke svarbody fra et tilgangsverktøykall.

20 lokale tester bestod. Codex CLI installerte testkandidaten, og alle 18 installerte filer samsvarte med kilden. Testinstallasjonen ble fjernet etterpå. [Pakkerapporten](evidence/prelaunch-package.json) inneholder arkivets sjekksum og egne testgrenser; CLI-installasjon beviser ikke tilkobling eller skillutførelse i ChatGPT.

Utvalgt MCP-kilde og dokumentasjon ble hentet fra GitHub på commit `66b31ef1853f157dc71c887f80c6d73823163fef`. Dette er en kildegjennomgang, ikke en egen kjøring av MCP-prosjektets servertester. Serverutviklingens rapporterte tester holdes atskilt fra tester utført her.

## Funn som er tatt inn i skillene

- Den faktiske setup-adressen er `https://tactical-mcp.tronderdata.no/admin/`.
- Seks dedikerte access-verktøy er tilgjengelige i katalogen, med personlig OAuth.
- `tactical_user_id` må velges når flere Tactical-kontoer deler e-post og eksisterende verifisert kobling ikke avgjør kontoen.
- Førstegangskobling for vanlig bruker skjer på siden eller med management-hjelp. Profil-e-post alene gir ingen serverintern nøkkeluthenting.
- `idempotency_key`, fremtidig RFC3339-utløp innen 366 dager, nøkkel-ID og eksplisitt unlink/revoke er nødvendige krav. Noen krav er bare dokumentert i beskrivelser/servervalidering og ikke fullt uttrykt i JSON-skjemaet.
- En generell 403 med OAuth-utfordring kan også skyldes utilgjengelig personlig kobling. Skillene skal kontrollere `mapped` og ikke starte en blind innloggingssløyfe.
- Native nøkkeladministrasjon kan logges på operatørnøkkelens eier i Tactical. MCP-loggen må brukes for faktisk SSO-aktør og målbruker; handlingen skal ikke fremstilles som logget på målbrukeren.

## Innloggede tester som gjenstår

Brukeren har opplyst at eksisterende Tactical-tilkobling er valgt og SSO er fullført. De personlige Tactical-verktøyene ble likevel ikke tilgjengelige i denne pågående chatten. Jeg har ikke hentet eller kopiert et OAuth-token fra nettleser, fil, en annen chat eller et annet miljø, og har ikke brukt gatewayen som alternativ identitet.

Når den eksisterende direkte tilkoblingen er tilgjengelig som verktøy i en ny melding eller samtale, kjør et avgrenset eget statusoppslag og et bekreftet lesekall, for eksempel versjon. Rapporter bare nødvendig status og eventuelle antall. Ikke kjør nøkkelendringer eller maskinhandlinger som en standardtest.

Deretter kreves egne testidentiteter med vanlig rolle og management, inkludert en uten førstegangskobling, for rettighets- og isolasjonstest. Skriveflyter krever avtalt testmiljø og uttrykkelig testbestilling. [Funksjonsdekningen](FUNCTIONAL-COVERAGE.md) må også fullføres for kravet om hele brukerens Tactical-funksjonsflate.

## Ikke bevist av denne testen

Personlig OAuth-flyt, faktisk nøkkelstatus for en bruker, rolleisolasjon, serverintern nøkkellivssyklus, korrekt brukerlogging, full UI-funksjonsdekning, arbeidsområdeimport, automatisk onboarding og ChatGPT-nettleserbruk er ikke godkjent av de fem uautentiserte kontrollene. Lanseringsstatus er derfor **ikke godkjent**.
