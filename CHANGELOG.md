# Endringslogg

## 1.3.0-rc.3 – 2026-11-16

- Oppsettsskillen skiller manglende ChatGPT-kontotilkobling fra manglende personlig Tactical-nøkkel. Den sender ikke teknikeren til Codex eller manuell MCP-registrering.
- Ny kontroll med faktisk klient oppdager om pakken mangler registrert app og kontolenke. Kontrollen feiler for denne kandidaten; SSO-flyten er fortsatt ikke levert.
- Dokumentert at GitHub-synk bare henter publiserte endringer. Eksisterende arbeidsområdeplugin beholdes; registrert OAuth-app må verifiseres før appbinding kan legges til.

## 1.3.0-rc.2 – 2026-11-16

- Selvstendig remote MCP-konfigurasjon med eksisterende endepunkt og provided OAuth-klient; bindingen til den slettede personlige pluginen er fjernet.
- Tilpasset MCP `0.4.0-native-api`, inkludert native query/body, binær/multipart-overføring, kontraktshint og strukturerte feil.
- Statiske inventarkontroller bekrefter 328 operasjoner, 291 klassifiserte tekniker-REST-operasjoner og 37 begrunnede eksklusjoner.
- Kjente mangler for interaktiv terminal, live-strømmer og fjernskrivebord holdes synlige; full GUI-dekning er ikke påstått.
- Isolerte MCP-/klient-/admintester kjørt fra kilde på Linux uten produksjonslegitimasjon. Ny personlig OAuth og ChatGPT-nettleser sluttkontrolleres ved installasjon.

## 1.3.0-rc.1 – 2026-11-15

- Testkandidat på egen gren for MCP `0.3.2-admin-repair`; ingen automatisk lansering til `main`.
- Faktiske access-verktøy og betingede parametere dokumentert, inkludert `tactical_user_id` ved flere kontoer med samme e-post.
- Bekreftet setup-URL og dokumentert førstegangskobling for vanlige brukere versus management.
- Skillene unngår å tolke generell 403 som manglende kobling eller utløpt innlogging uten bekreftet status.
- Lesende før-lanseringsskript med kontroller uten legitimasjon, samt tester av skriptets skrive- og svarbegrensninger.
- Full funksjonsdekning innen hver brukers Tactical-rettigheter er akseptansemålet; dette er ennå ikke dokumentert eller godkjent.

## 1.2.0 – 2026-11-15

- Original Tactical RMM-logo fra offisielt repo, med kilde og sjekksum, lagt til som logo og composer-ikon.
- Ny norsk oppsettsskill registrert i begge manifests `onboardingSkill`.
- SSO, manglende-kobling-status og bekreftede setup-lenker håndteres uten gjetting av URL eller nøkkelverdier i chat.
- Tilgangsskillen støtter beskrevet selvbetjening for egen konto og management-administrasjon av andre; faktisk serverstøtte må fortsatt verifiseres.
- MCP-utviklingschat og kjørende offentlig katalog undersøkt hver for seg. Konkrete gjenstående krav og testgrenser dokumentert.

## 1.1.0 – 2026-11-14

- Ny norsk administrasjonsskill for kommende management-verktøy og SSO-beskyttede administrasjonslenker.
- Arbeidsflyt for opprettelse/henting i Tactical og kobling til riktig bruker i MCP, uten nøkkelverdier i verktøyinput, verktøyresultater eller chat.
- Dokumenterte serverkrav for management-autorisasjon, fast målidentitet, rotasjon, delvis feil og kontroll før gjentakelse.
- Tidligere generelt forbud mot administrasjonsverktøy er erstattet med den bestilte, serverstyrte administrasjonsflyten. Vanlig RMM-drift beholder personlig identitet.
- Serverfunksjonene er fortsatt under utvikling og er ikke implementert eller live-testet av pluginpakken.

## 1.0.0 – 2026-11-14

- Første pakke med visningsnavn Tactical RMM og utgiver Trønder Data.
- Agent Plugins 1.0, Codex-kompatibilitet og GitHub-marketplace.
- Norsk driftsskill og referanse til verifisert eksisterende app.
- Lokal validering, avgrenset metadata-probe, bygging og dokumentasjon.
- Arbeidsområdedeling, nettleserimport og flerbrukerisolasjon gjenstår å teste.
