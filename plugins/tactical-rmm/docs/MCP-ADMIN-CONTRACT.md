# Kommende brukeradministrasjon via chat

**Status: Under utvikling.** Brukeren har presisert at administratorer i Keycloak-gruppen `management` skal kunne bestille opprettelse, kopiering/kobling og fornyelse av personlige Tactical-nøkler i chatten. Selve nøkkelverdien skal forbli mellom Tactical og MCP. Denne leveransen forbereder skills og dokumentasjon; den implementerer ingen MCP-verktøy, serverfunksjon eller adminside.

## Ønsket serverflyt

1. MCP validerer token og autentisert identitet ved hver beskyttet operasjon. Selvbetjening begrenses til egen konto; administrasjon av andre krever management-medlemskap fra betrodd identitetskilde. Oppgitt gruppe, aktør eller målidentitet fra modellen er ikke autorisasjon.
2. Et avgrenset brukeroppslag løser målbruker til fast Keycloak-`sub` eller en intern referanse med samme faste kobling. Navn og e-post er bare søkehjelp.
3. MCP oppretter eller henter riktig personlig nøkkel i Tactical, innenfor dokumenterte administratorrettigheter og støtten Tactical faktisk har. Nøkkelen skal tilhøre riktig målbruker; management-tilgang skal ikke gjøre den til en felles administratornøkkel.
4. MCP lagrer nøkkelen direkte i den beskyttede koblingen på serveren. Den sendes aldri som tool-input, tool-output, chattekst, modelltilgjengelig UI-innhold, URL, logg eller feildetalj.
5. Resultatet til chatten inneholder bare ikke-hemmelige brukerreferanser, handlingsstatus og eventuelt operasjonsreferanse. Serveren kan returnere en SSO-beskyttet administrasjons-URL med målbrukerreferanse, uten tilgangsgivende hemmeligheter.
6. En egen statuskontroll bekrefter lagring og eventuell validering av tilgangen uten å hente nøkkelverdien. Drift som bruker den personlige koblingen beholder vanlig personlig tilgangshåndheving.

Dette er en funksjonskontrakt for serverutviklingen, uten foreslåtte verktøynavn eller oppdiktede API-parametere. Faktisk verktøykatalog, støttede Tactical-operasjoner, grupperepresentasjon, feilformat og adminopprinnelse må dokumenteres og verifiseres når serveren leverer funksjonen.

## Førstegangsoppsett etter SSO

Et dokumentert, lesende statussvar må kunne hentes etter SSO, også når personlig Tactical-kobling mangler. Svaret må skille mellom manglende kobling, eksisterende kobling, bekreftet fungerende tilgang og avvist tilgang. Det må oppgi faktisk, SSO-beskyttet setup-URL uten nøkkel eller tilgangsgivende token. En generell 403 er ikke en manglende-kobling-status.

Oppsettsiden må være brukbar for egen konto uten management-medlemskap når selvbetjening tilbys. Management kreves ved tilgang til andre. Statusverktøyet og oppsettssiden må ikke bli blokkert av at brukeren ennå ikke har den personlige nøkkelen som siden skal hjelpe med å koble.

Oppsettsskillen finnes i pakken fra 1.2.0. En faktisk setup-sti er fortsatt ikke verifisert. MCP-protokolladressen er ikke en erstatning for en setup-side.

## Delvis feil og fornyelse

Serveren må skille mellom at nøkkelen er opprettet i Tactical, at koblingen er lagret i MCP, og at tilgang eventuelt er validert. Hvis lagring feiler etter opprettelse, må serveren holde oversikt over operasjonen og støtte trygg gjenoppretting. Ikke opprett enda en nøkkel ved et blindt nytt forsøk. Statusoppslag og eventuell idempotens må ha dokumentert atferd.

Ved rotasjon må rekkefølgen for opprettelse, lagring, kontroll og tilbakekall være dokumentert. Tilbakekall skal ikke skjules i en operasjon som bare lover å legge til en kobling. Eksisterende nøkkel må ikke tilbakekalles før dokumenterte vilkår og brukerens bestilling tillater det. Hvis Tactical ikke støtter operasjonen, returner en tydelig begrensning eller en bekreftet lenke for manuell, beskyttet administrasjon.

Audit bør registrere autentisert aktør, målbruker, handling, tidspunkt og resultat, uten nøkkelverdi. Ikke bruk en nøkkelbærende lenke eller et hentehåndtak som gir tilgang til hemmeligheten som modelltilgjengelig mellomlager.

## Gjenstående akseptanse på serveren

- En management-testbruker kan administrere riktig målbruker; en vanlig bruker og en uten management-medlemskap blir avvist. Falsk gruppe/aktør fra verktøyargumenter gir ikke tilgang.
- To brukere med like navn kan ikke forveksles ved endring. Vanlig RMM-drift bytter ikke til den administrerte brukerens identitet.
- Nøkkelopprettelse/kobling og rotasjon verifiseres med egne testidentiteter, ikke ansattes aktive koblinger.
- Rå nøkkel finnes ikke i verktøykall, svar, feil, logger, URL-er eller modelltilgjengelig UI. Å skjule den bare i sluttmeldingen er utilstrekkelig.
- Timeout og feil mellom opprettelse og lagring gir kontrollerbar tilstand uten blind duplisering. Test også ugyldig token, tilbakekalt gruppetilgang, avvist Tactical-tilgang og feil parametere.
- Adminlenker krever SSO og tilgangskontroll ved åpning; lenken gir ingen tilgang alene.

Alle serverakseptansetester ovenfor er **utestet** i pluginpakken. Ingen aktiv nøkkel ble opprettet, lest, rotert eller lagret under pakkeutviklingen.
