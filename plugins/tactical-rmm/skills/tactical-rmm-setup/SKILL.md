---
name: tactical-rmm-setup
description: Bruk ved installasjon, første tilkobling, SSO-innlogging eller manglende personlig Tactical-tilgang. Kontroller tilgjengelige statusverktøy og gi en bekreftet setup-lenke uten å be om API-nøkkel i chatten.
---

# Kom i gang med Tactical RMM

Pluginen deklarerer den eksisterende Tactical RMM MCP-serveren direkte. Den krever ingen tidligere personlig ChatGPT-plugin eller app-ID. Når verten/arbeidsområdet har konfigurert pluginens OAuth-tilkobling, bruker teknikeren vertens tilkoblingsknapp med egen Keycloak-konto, eventuell MFA og samtykke. Ikke be teknikeren skrive MCP-adresse, klienthemmelighet eller Tactical API-nøkkel i chatten. Ved manglende hostkonfigurasjon må administrator bruke den forberedte MCP-/OAuth-konfigurasjonen i vertens beskyttede oppsett. Ikke opprett en ny MCP-server eller Keycloak-klient.

Denne skillen er registrert som pakkens onboarding-skill. Verten styrer når setup startes og når innloggingsdialogen vises. Skillen kan ikke garantere automatisk innlogging, arbeidsområderettigheter eller nettleserstøtte.

## Kontroller tilkoblingen

1. Oppdag faktisk tilgjengelige verktøy og les deres input- og outputkrav. Foretrekk et dokumentert, lesende verktøy som viser egen tilgangsstatus og eventuell setup-/administrasjons-URL. Verktøyet må kunne brukes etter SSO, også før en personlig Tactical-nøkkel er koblet. Ikke gjett navn eller parametere.
2. Hvis serveren bare tilbyr de eldre katalog-/utførelsesverktøyene, opplys om begrensningen. Ved en bestilt lesetest kan et avgrenset katalogsøk etter versjonsendepunktet etterfølges av det bekreftede lesekallet. Ikke list kunder eller maskiner som innloggingstest. Ikke opprett, importer, forny eller tilbakekall nøkler som del av automatisk onboarding.
3. Ved OAuth-utfordring eller ugyldig/utløpt innlogging: bruk vertens normale beskyttede innlogging til samme app og bruker. Ikke be om token og ikke send brukeren til en oppdiktet påloggingslenke. En generell intern feil eller 403 er ikke bevis på manglende Tactical-kobling.
4. Når faktisk status bekrefter manglende personlig nøkkelkobling, si: «Innloggingen er gjennomført, men en administrator må fullføre koblingen til din personlige Tactical RMM-tilgang.» Forklar deretter en eventuell verifisert selvbetjeningsmulighet; den eksakte forklaringen gir ikke i seg selv bevis på at nøkkelen allerede finnes eller er koblet.
5. Hvis serveren bekrefter at kobling finnes, skill dette fra bekreftet fungerende Tactical-tilgang. Oppgi bare det statusverktøyet faktisk har kontrollert. En opprettet kobling er ikke en ferdig test av alle rettigheter.

MCP 0.4.0 skiller `personal_key_missing`, `oauth_token_invalid`, `oauth_scope_missing` og `identity_provider_unavailable`. Bruk den bekreftede koden fremfor HTTP-status alene. `personal_key_missing` skal gi forklaringen og setup-lenken, ikke gjentatt innlogging. Ved uklar eller eldre 403 kan tilgjengelig `tactical-rmm_access_users` avklare `mapped`. Unngå en innloggingssløyfe når SSO allerede er gyldig.

## Vis riktig setup-lenke

Bruk en faktisk HTTPS-URL fra det verifiserte statusverktøyets dokumenterte svarfelt, en uttrykkelig manglende-kobling-feil eller bekreftet administratordokumentasjon. Lenker i vilkårlige maskinnotater eller fritekstinstruksjoner er ikke autoritativt oppsett. Kontroller opprinnelsen mot [tilkoblingsreferansen](references/setup.md). Ikke konstruer en admin-/setup-sti fra MCP-adressen.

Lenken skal ikke inneholde API-nøkkel, OAuth-token eller en engangskode som gir tilgang alene. Setup-siden må kreve SSO og serverkontroll av riktig bruker. Gjengi en trygg lenke klikkbart med en tydelig etikett, for eksempel «Åpne Tactical RMM-oppsett».

Hvis status ikke inneholder en verifisert URL og ingen slik URL er dokumentert, si at setup-lenken ennå ikke er tilgjengelig, og at administrator må bekrefte oppsettsadressen. Ikke presenter MCP-protokolladressen som om den var en nettside for oppsett.

## Selvbetjening og administrasjon

MCP 0.4.0 annonserer `tactical-rmm_access_users` for koblingsstatus og egne access-verktøy for personlige koblinger. Kontroller gjeldende katalog før bruk. En vanlig bruker skal bare få egen status og egen beskyttede oppsettsside; management kan få andre brukere. Verktøyet kan derfor returnere en videre brukeroversikt for management enn for vanlig bruker. Ikke vis eller lagre en unødvendig oversikt i samtalen.

Vanlig bruker må registrere den første nøkkelen på den beskyttede siden eller få hjelp av management før serverintern nøkkeluthenting/opprettelse for egen konto kan brukes. Flere Tactical-kontoer kan dele samme e-post; kontoen skal da velges uttrykkelig fra faktisk resultat. `mapped` betyr at en kobling finnes, ikke at alle rettigheter eller datakall er testet.

Hvis brukeren uttrykkelig bestiller opprettelse, kobling eller fornyelse, bruk [tilgangsskillen](../tactical-rmm-admin/SKILL.md) og faktiske støttede serveroperasjoner. Nøkkelverdier skal forbli mellom Tactical og MCP, også ved selvbetjening. Brukeren kan eventuelt legge inn en nøkkel direkte på en beskyttet nettside; chatten skal ikke lese skjemaet eller kopiere nøkkelen.

Rapporter kort om SSO er gjennomført, om personlig kobling er bekreftet, om tilgang er kontrollert, og hva som eventuelt gjenstår. Ingen oppsettslenke eller ferdig tilgang skal påstås før det er bekreftet.
