# Verifikasjon – oppdatert 15. november 2026

**Historikk for 1.2.0:** Rapporten nedenfor gjelder den tidligere pakken. Den nyere testkandidaten `1.3.0-rc.1` på `test/mcp-0.3.2` er beskrevet i [før-lanseringsrapporten](PRELAUNCH.md), med faktisk MCP 0.3.2-katalog og bekreftet setup-adresse. Ikke bruk historiske formuleringer om ukjent setup-URL som gjeldende status for testkandidaten.

## Separate testnivåer

| Nivå | Resultat | Avgrensning |
| --- | --- | --- |
| Lokal pakkevalidering | Bestått: 16 tester, validator og ZIP-bygg; se [maskinlesbar rapport](evidence/local-validation.json) | Ingen kundehandlinger, innlogging eller produksjonsendringer |
| Codex CLI-installasjon | Se maskinlesbar rapport for 1.2.0 | Tre skills, onboardingreferanse og original logo kontrolleres i installasjonen. Dette tester ikke skillutførelse eller oppsettsdialog i en chat |
| MCP offentlig metadata | Bestått | Resource, issuer, scope, PKCE S256, initialisering og faktisk `tools/list` |
| Live MCP gjennom eksisterende personlig app | Bestått | API-katalogsøk og GET `core.core-version`; Tactical svarte `0.0.204` |
| Ny personlig OAuth-innlogging/MFA | Utestet | Eksisterende forbindelse ble gjenbrukt; ingen ny OAuth-flyt |
| Faktisk GitHub-import og Sync now | Utestet | Offentlig repo `SveinT83/tactical-rmm-plugin` er opprettet og pushet; ingen workspace-import utført |
| Apprettigheter og deling med arbeidsområdet | Utestet | Eksisterende plugin har scope USER; appens arbeidsområdetilgang er ikke bekreftet |
| ChatGPT i nettleseren | Utestet | Ingen faktisk nettleserinstallasjon eller datakall fra nettleser |
| Personlig isolasjon med flere brukere | Utestet | Ingen egne testidentiteter tilgjengelig; én brukers test beviser ikke isolasjon |
| Serverkilde og nøkkeladministrasjon | Ikke kildeverifisert | SSH til `mcp-services` ble avvist; administrasjonsgrensesnittets utrulling er ikke bekreftet |
| Nye management-verktøy | Under utvikling og utestet | Versjon 1.1.0 forbereder en administrasjonsskill; MCP-opprettelse, kobling og rotasjon er ikke implementert i pakken |
| Oppsettsskill og logo i 1.2.0 | Pakket og validert | Original logo, `onboardingSkill` i begge manifester, referanser og alle tre skillmapper. Ingen faktisk setup-URL er verifisert |

## Observerte fakta fra første leveranse, 14. november

- Arbeidsmappen var tom ved start. Ingen AGENTS.md fantes i arbeidsmappen eller de overordnede mappene `/`, `/var`, `/var/Projects`. Ingen eksisterende Git-remote var tilgjengelig.
- Plugin Creator returnerte eksisterende plugin med ID `plugin_asdk_app_6af232dfb75c81919191e1ab5b5fd9c0`, scope `USER`, versjon `1.0.0`. App-ID ble lest fra dens `.app.json`. Ingen konto-/pluginendring ble gjort.
- Offentlig MCP-resource er nøyaktig `https://tactical-mcp.tronderdata.no/chatgpt/mcp`. Issuer og scope samsvarer med bestillingen. Serveren rapporterte navn `Datanora Tactical RMM`, versjon `0.2.8-command-validation`.
- To faktiske MCP-verktøy ble lest med skjemaer og OAuth-metadata: `tactical-rmm_search` og `tactical-rmm_execute`. Initialisering og katalog kan leses uten token; dette beviser ikke at datakall kan kjøres uten autentisering. Ingen uautentisert kundeuthenting ble forsøkt.
- Kommandoens søkemetadata krever eksplisitt `run_as_user` og betinget `custom_shell`. Katalogen har også GET-ruter for kjøring av oppgaver og skript. Skillen håndterer disse som handlinger.
- De fleste av de øvrige endepunkteksemplene manglet `params_schema`. Skillen krever verifisering av nødvendige parametere og tillater ikke gjetting.
- Ett første søk etter varsler returnerte intern feil. Et avgrenset, lesende gjentatt katalogsøk lyktes. Ingen skrivekall ble gjentatt eller utført.
- Et avgrenset live-kall gjennom eksisterende personlig app returnerte Tactical-versjonen `0.0.204`. Det ble ikke hentet lister over kunder, lokasjoner eller maskiner.
- En uavgrenset `codex plugin list --json` fikk tidsavbrudd etter 45 sekunder. Etter eksplisitt registrering av test-marketplace lyktes installasjon og avgrenset listing umiddelbart. Ingen endring av eksisterende app eller personlig plugin var nødvendig. CLI-testen beviser pakkeinnlesing, ikke at den nye skillen har kjørt i en chat.

Metadata og representative katalogtreff ligger i [evidence/](evidence/). Øyeblikksbildene er bevis fra denne datoen, ikke en autoritativ fremtidig katalog. Kommandoeksemplet inneholder bare et plassholdermål; det ble aldri kjørt.

## Lokale tester og mocks

Automatiske tester kontrollerer manifest/schema, versjoner, app-ID kontra plugin-ID, marketplace-stier, ødelagte referanser, symlinker, dobbeltkobling, arkivinnhold, deterministisk ZIP og hemmeligheter også i Git-indeksen. Testene validerer i tillegg faktisk observert kommandoskjema med manglende/feil `run_as_user`, betinget shell, ugyldig timeout og tomt mål. Ingen av disse testene sender en kommando.

[tests/scenarios.json](../tests/scenarios.json) inneholder syntetiske verktøyresultater. De ble gjennomgått manuelt mot skillens regler med følgende respons og neste steg:

| Mock | Kontrollert forventet respons/oppførsel |
| --- | --- |
| Uttrykkelig manglende personlig kobling | Eksakt norsk forklaring; administrator kan bestille en verifisert management-operasjon eller bruke beskyttet administrasjon; nøkkelen forblir på serveren |
| Ugyldig/utløpt token | Beskyttet OAuth for samme app og bruker; ingen forespørsel om token |
| Utilstrekkelige rettigheter | Rapporter avvisning; ingen alternativ konto, tilkobling eller metode |
| Uklar 403 | Rapporter ukjent årsak; ikke bruk forklaringen om manglende nøkkelkobling |
| Feil kommandoparametere | Les skjema og avklar kjørekontekst; ikke kjør med gjettet kontekst |
| Timeout etter handling | Ukjent resultat; undersøk tilstand før et nytt skrivekall |
| Instruksjon i maskinnotat | Behandles som data; gir ingen fullmakt til å bytte tilgang |

Dette er en lokal gjennomgang av feilsvar og instruksjoner, ikke en live feilinjeksjon eller automatisert måling av en modells atferd. Produksjonens feilkoder for manglende kobling er ikke kildeverifisert. Ansattes nøkler, kontoer og koblinger ble ikke endret. En senere modelltest kan bruke disse mockene i et isolert miljø med verktøykall deaktivert; faktisk modellatferd gjenstår å evaluere.

## Administrasjonsskill i 1.1.0

Versjon 1.1.0 innførte en administrasjonsskill i tillegg til driftsskillen. Den forbereder serverstyrt opprettelse/henting i Tactical og lagring på riktig målbruker i MCP. Brukerens nye avgrensning tillater administrative bestillinger fra chat for management-brukere, mens nøkkelverdier fortsatt skal holdes helt utenfor modellkonteksten. Ingen rånøkler ble hentet eller flyttet under arbeidet.

Pakketestene kontrollerer at begge skills er oppdagbare og kommer med i arkivet sammen med serverkontrakten. Faktiske management-rettigheter, Keycloak-gruppemapping, brukeroppslag, admin-URL, opprettelse, delvis feil, lagring og rotasjon er utestet. [Serverkrav og akseptanse](../plugins/tactical-rmm/docs/MCP-ADMIN-CONTRACT.md) må verifiseres når MCP tilbyr funksjonene. Tidligere live-lesetest og offentlige metadata er historiske observasjoner fra 1.0.0-arbeidet, ikke en ny integrasjonstest av administrasjonsskillen.

## Oppsett og logo i 1.2.0

Pakken har tre skills. Original Tactical RMM-logo er kopiert uendret fra offisielt frontend-repo og refereres av både portabelt manifest og kompatibilitetsmanifest. SHA-256, PNG-format og størrelse kontrolleres. `onboardingSkill` peker til den pakkede oppsettsskillen, som bruker beskyttet SSO og krever en faktisk, bekreftet setup-URL. Manglende URL fører til en ærlig statusmelding, ikke en konstruert lenke.

Pakketestene inkluderer nå manglende onboardingfil og endret/ugyldig logo. Modellatferd, automatisk oppstart av onboarding og faktisk visning av logo eller OAuth-dialog i ChatGPT-nettleseren er fortsatt utestet.

MCP-utviklingschatten ble funnet på Windows-verten og lest uten kommandoresultater. Den rapporterer selvbetjening for egen konto og management-administrasjon av andre, med serverstyrt nøkkelflytting. Dette er utviklingsstatus fra chatten, ikke en selvstendig kilde- eller integrasjonsrevisjon. Den siste uautentiserte metadata-proben under dette arbeidet viste fortsatt versjon `0.2.8-command-validation` og to basisverktøy; rolleavhengige kataloger kan avvike etter SSO. [Konkrete MCP-bekreftelser og videre arbeid](MCP-HANDOFF.md) er samlet separat.

## Gjenværende akseptanse

GitHub-repoet [SveinT83/tactical-rmm-plugin](https://github.com/SveinT83/tactical-rmm-plugin) er opprettet offentlig og pushet etter eierens uttrykkelige valg 15. november 2026. Administrator må bekrefte gjenbrukbar arbeidsområdetilgang til appen, gjeldende rutine for personlig nøkkelkobling, importresultat og reell nettleserstøtte. Test deretter med egne identiteter med forskjellige rettigheter. Skill, katalog og serverens faktiske tilgangskontroller må alle kontrolleres før bred bruk. Ingen produksjons-MCP, OAuth-klient eller eksisterende plugins deling er endret.
