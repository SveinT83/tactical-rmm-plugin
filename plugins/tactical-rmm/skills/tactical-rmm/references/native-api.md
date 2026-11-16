# Native REST-kontrakt fra MCP 0.4.0

Referansen bygger på gjennomgått MCP-kilde og dens produksjonsskjema fra 15. november 2026. Offentlig MCP-initialisering er observert som `0.4.0-native-api`. Det beviser ikke at alle operasjoner er kjørt fra pluginen eller at alle brukere har rettighetene som kreves.

## Oppdag den faktiske operasjonen

Bruk `tactical-rmm_search` og les effektiv metode/sti, offentlig `endpoint_id` og parameternavn, `params_schema`, `parameters`, `request_body`, `schema_definitions`, `source_hints`, `request_options` og tilgjengelighets-/rettighetshint. Søk kan også oppgi dekningssummer og gjenværende mangler.

Kildeinventaret har 328 HTTP-operasjoner: 291 er klassifisert som tekniker-REST, mens 37 er agent-/installerprotokoll eller egne innloggingsflyter. Serverdokumentasjonen oppgir 293 register-ID-er fordi to eldre statusruter beholdes med separate autentiseringskrav. Dette er registrert kontrakt, ikke 293 ferdig testede handlinger eller full GUI-dekning.

Eldre ID-er kan være beholdt med korrigert HTTP-metode og `/tasks/` i stedet for `/autotasks/`. Bruk aktuell effektiv rute fra søket. Ikke forsøk nye metoder/stier etter en feil. `native_route_binding` kan beskrive en eksplisitt agent-/policy-rute som serveren binder til en kanonisk opprettelsesrute; ikke legg inn et motstridende mål i body.

`source_hints.body_fields` og rettighetskandidater kan være ufullstendige. De betyr ikke at alle felter er skrivbare eller påkrevde. Et skjema med sti-/query-parametere er heller ikke en full body-kontrakt. Verifiser nødvendige felt før en handling.

## Query, body og filer

- Behold offentlige sti-parametere utenfor body og bruk navnene serveren eksponerer.
- `_query` er et eksplisitt query-objekt på alle verb. Lister gir gjentatte query-verdier.
- `_body` er hele JSON-bodyen, inkludert lister og DELETE-body. Ikke bland `_body` med flate body-felt.
- Vanlige flate JSON-parametere er fortsatt støttet der kontrakten beskriver dem. Ikke gjett mellom formatene etter et usikkert skriveutfall.
- `_request` kan overføre data i minnet ved dokumenterte fil-/rapporteringsoperasjoner. Den gir ikke rett til å lese lokale serverfiler, velge annen host eller overstyre autentisering.

Dokumenterte binære chunks bruker `content_type: application/octet-stream`, `data_base64` og bare tillatte headere som `Content-Range`. Opprett og kontroller den faktiske native overføringssesjonen først. Følg `chunk_size`, `accepted_offset`, `committed_offset` og `can_put` i resultatet; ikke send samme eller neste chunk blindt etter timeout.

Multipart støttes bare der kontrakten annonserer det, med `content_type: multipart/form-data`, strengfelter i `fields` og filer med `name`, `filename` og `data_base64`. Grensene er 512 KiB for en tillatt chunk/forespørsel og åtte multipart-filer; følg også mer presise grenser fra gjeldende skjema. Rapporteringsressurser bruker filnavnet som native formnøkkel og kan ha `parentPath` som ekstern mappe, ikke lokal disksti.

Bruk bare innhold som brukeren har gitt fullmakt til å overføre. Binære resultater kan komme som base64 med begrensede overføringsheadere. Ikke skriv store binære innhold eller hemmeligheter i chatten.

## Strukturerte feil

Les `error_code`, `http_status`, `missing_fields`, `field_errors` og eventuell renset `upstream_message`. Skill OAuth-feil fra en ugyldig personlig Tactical-nøkkel og fra ruter som krever native sesjon.

| Kode/observasjon | Oppførsel |
| --- | --- |
| `personal_key_missing` | SSO lyktes, men personlig nøkkel mangler/kan ikke brukes. Gi den eksakte forklaringen fra skillen og bekreftet setup-lenke. |
| `oauth_token_invalid` | Bruk normal beskyttet innlogging til samme app. |
| `oauth_scope_missing` | Forklar manglende scope uten å omgå kontrollen. |
| `identity_provider_unavailable` | Keycloak-verifisering feilet; ikke påstå at en Tactical-handling er utført. |
| `validation_failed` | Forklar bekreftede feltkrav; ikke gjenta med gjettede felt. |
| `permission_or_scope_denied` | Vis relevante hint. Når `missing_permissions_verified` er false, er eksakt manglende rettighet ikke bekreftet. Klasser og kandidater er ikke bekreftede mangler. |
| `resource_or_feature_unavailable` | En 404 alene skiller ikke feil ID, skjult scope, funksjon eller lisens. Oppgi hva som er ukjent. |
| Native autentisering, metodefeil, konflikt, størrelse, encoding eller rategrense | Forklar faktisk årsak uten å skifte identitet eller gjette nye metoder. |

Når `action_outcome_unknown` er satt, eller ved transport-/5xx-feil etter en handling, undersøk faktisk status og historikk før nytt skriveforsøk. En feilbeskjed betyr ikke nødvendigvis at ingen endring skjedde. Ikke gjengi rå upstream-feil eller verdier serveren har maskert.

## Kjente sesjonsmangler

Interaktiv WebSocket-utdata, vedvarende terminal og dashboardstrømmer krever en egen personlig native sesjonsintegrasjon. Vanlig REST-kjøring av kommando/skript er ikke en interaktiv terminal. Fjernskrivebord krever MeshCentral-klient/-sesjon; lest integrasjonsmetadata betyr ikke at MCP kan vise eller styre skrivebordet.

Rapporter disse som konkrete dekningsmangler når brukeren bestiller funksjonen. Ikke lov full GUI-paritet, bruk en delt administratorøkt eller fall tilbake til en annen identitet for å skjule mangelen.
