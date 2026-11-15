# Akseptanse: hele brukerens Tactical-funksjonsflate

Kravet fra brukeren er at hver person skal kunne gjøre alt vedkommende har rettigheter til i Tactical RMM gjennom MCP. Dette er et akseptansemål, ikke en påstand om verifisert dekning i dagens pakke.

En operasjon må kontrolleres gjennom hele kjeden: faktisk arbeidsflyt i installert Tactical-versjon, tilgjengelig API eller annen støttet integrasjon, MCP-verktøy og parametere, korrekt personlig autorisasjon, utførelse og verifiserbart resultat. Antall verktøy eller genererte endepunkter er ikke et dekningsmål alene.

## Områder som må gjennomgås

Dette er en arbeidsliste, som må kompletteres mot det faktiske installerte grensesnittet og brukerens rettigheter. Radene er ikke en komplett inventarliste eller bekreftelse på at en gitt funksjon er tilgjengelig for enhver bruker.

| Område | Hva som må kartlegges | Status fra denne chatten |
| --- | --- | --- |
| Kunder og lokasjoner | Søk, visning og tillatte endringer | Tidligere katalogtreff; innlogget test av gjeldende versjon mangler |
| Maskiner og inventar | Status, detaljer, metadata og tillatte endringer | Tidligere katalogtreff; funksjonsdekning utestet |
| Varsler og sjekker | Lesing, håndtering og kjøring | Tidligere katalogtreff; handlinger ikke testet i produksjon |
| Oppgaver og automasjon | Konfigurasjon, kjøring, historikk og resultat | Tidligere katalogtreff; komplett arbeidsflyt utestet |
| Skript og kommandoer | Bibliotek, kontekst, utførelse, timeout og resultat | Kommandoskjema testet lokalt; ingen produksjonskjøring |
| Patching og omstart | Status, godkjenning, kjøring og oppfølging | Katalogtreff for Windows-oppdateringer; ingen produksjonsendring |
| Programvare og systemdrift | Faktiske installerte UI-handlinger og API-/verktøystøtte | Utestet |
| Fjernfunksjoner og interaktive flater | Faktisk støtte for relevante fjern-/terminal-/filflyter der de finnes | Utestet; ikke antatt dekket av generell HTTP-utførelse |
| Rapporter, historikk og eksport | Faktiske visninger, data og nedlastinger | Utestet |
| Brukere, roller og innstillinger | Tillatte konto- og systemfunksjoner | Utestet som samlet Tactical-område |
| Personlige MCP-koblinger | Status, metadata, opprettelse, kobling, rotasjon, frakobling og tilbakekall | Katalog og kilde gjennomgått; innlogget livssyklus utestet |
| Personlige rettigheter | Tillatt handling, avvist handling og isolasjon per rolle | Ingen egne rolleidentiteter testet fra denne chatten |
| Deployment-policy | Om ekstra MCP-/route-/skrivebegrensninger hindrer ellers tillatte Tactical-handlinger | Må bekreftes; ikke endret for å få tester til å bestå |

## Bevis som kreves per arbeidsflyt

Registrer konkret UI-handling, nødvendig rolle/rettighet, støttet MCP-operasjon, parametere og dokumentert eksempel uten hemmeligheter, forventet status, eventuelle asynkrone jobber, kontroll av sluttresultat og testidentitet/-miljø. Bruk statusene bekreftet, utestet, manglende støtte og blokkert av deployment-policy.

Manglende API-/transportstøtte må løses i MCP eller dokumenteres som et reelt avvik. En skill skal ikke finne på et verktøy eller omgå en avvisning. Hvis Tactical tillater handlingen, men MCP ikke gjør det, skal rapporten vise denne forskjellen fremfor å hevde at brukeren mangler Tactical-rettigheter.

Skriveflyter, restart, patching og nøkkellivssyklus skal testes i et avtalt testmiljø med egne testidentiteter/-maskiner. De kjøres ikke på aktive kundemaskiner eller ansattes koblinger som en generell tilkoblingstest.

## Lanseringsstatus

**Full dekning er ikke bekreftet.** Nåværende før-lanseringstest gir bevis for pakketilstand, katalog, offentlig innloggingsside og OAuth-avvisning. Den godkjenner ikke funksjonsdekning eller brukerrettighetsisolasjon. MCP utvikles fortsatt; kjør testen på nytt mot den endelige katalogen og fullfør rolle-/arbeidsflyttestene før dette akseptansemålet kan godkjennes.
