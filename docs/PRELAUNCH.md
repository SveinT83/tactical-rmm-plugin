# Før-lanseringstest mot MCP 0.4.0

## Gjeldende pakkekobling 1.4.0

SSO-pluginen er nå verifisert som WORKSPACE/LISTED i Trønder Data. Brukeren bekrefter personlig innlogging. Kildeversjon 1.4.0 overtar den kanoniske pluginen via `pluginId`; ingen ekstra wrapper opprettes. Faktisk lokal klient finner tre ferdigheter, én registrert app og en kontolenke, uten separat MCP-deklarasjon. Dette er kilde-/klientkontroll før workspace-sync, ikke bekreftet GitHub-overtakelse i ChatGPT. Se [migreringsplan](SINGLE-PLUGIN-MIGRATION.md) og [faktisk registrering](evidence/sso-registration.json). Eldre avsnitt nedenfor beskriver tidligere kandidater.

## Gjeldende OAuth-oppsett: rc.4, 16. november 2026

`tactical-chatgpt` er endret til offentlig authorization-code-klient med påkrevd
PKCE S256. Pluginen bruker `tokenEndpointAuthMethod: none` uten klienthemmelighet.
Førkontrollen fant null aktive og frakoblede sesjoner. Kjørende MCP ble undersøkt:
intern tokenkontroll bruker separat `tactical-mcp-introspection`; ingen kjørende
container hadde `tactical-chatgpt` som miljøvariabelverdi. Dette utelukker ikke
andre, ikke kartlagte eksterne konfigurasjoner. Callback, scopes, mappere og
øvrige klientinnstillinger ble bevart; privat tilbakeføringskopi finnes på Keycloak-serveren.

Fem direkte OAuth-kontroller bestod: S256 når innloggingsskjemaet, manglende PKCE
og plain avvises, ukjent callback avvises, og tokenendepunktet godtar offentlig
klientidentifikasjon uten hemmelighet før en ugyldig testkode avvises med
`invalid_grant`. Ingen ekte autorisasjonskode, brukertoken eller kundehandling
ble brukt. De fem eksisterende lesende MCP-kontrollene består også.
Se [migreringsrapporten](evidence/public-oauth-migration.json).

Dette fullfører ikke den manglende ChatGPT-appbindingen eller personlig SSO.
Eldre rapporttekst under beskriver tidligere kandidater, ikke dagens klienttype.

## Ny installasjonsobservasjon 16. november 2026

Arbeidsområdeimporten av rc.2 viser MCP-server og tre skills, men ingen kontoknapp. `scripts/check_client.py` reproduserer manglende appbinding med faktisk lokal klient: tre skills, null registrerte apper og null oppdagede MCP-servere. Det siste er klientens lokale resultat; arbeidsområdets admin-side viser en MCP-deklarasjon. Ingen av observasjonene bekrefter en brukbar OAuth-tilkobling. Rapportene under er tidligere pakketester og serverkontroller, ikke bestått innlogging.

Rc.3 retter oppsettsteksten og legger til klientkontrollen. Kontrollen forventes fortsatt å feile til en verifisert registrert Tactical-app er bundet til pakken. SSO og ChatGPT-nettleser er fortsatt ikke godkjent.

Oppdatert 16. november 2026. Kandidat `1.3.0-rc.2` distribueres fra `main` for import. Testene ble opprinnelig kjørt på kandidatgrenen før sammenslåing. Ingen ChatGPT-opplasting, lansering eller produksjonsendring er utført av denne testen.

## Selvstendig pakke etter slettet personlig plugin

Brukeren bekreftet at den gamle personlige ChatGPT-pluginen er slettet. Kandidaten har derfor ingen `.app.json` eller gammel app-/plugin-ID som avhengighet. `mcp.json` og Codex-kompatibel `.mcp.json` beskriver samme eksisterende MCP-endepunkt med provided-klienten `tactical-chatgpt`, `client_secret_basic` og scope `tactical-rmm`.

Ingen klienthemmelighet følger pakken. Den konfigureres én gang i vertens beskyttede oppsett av administrator ved den nye installasjonen; teknikeren bruker deretter SSO/MFA. Det er ikke nødvendig å gjenskape den gamle pluginen for å ferdigstille eller teste kildepakken.

## Tester utført her

- **23 lokale tester:** manifester, referanser, tre skills, logo, selvstendig MCP-konfigurasjon, avvist DCR/konfigurasjonsavvik, arkiv og hemmelighetsskanning. Testharnessen nekter skriveverktøy og leser ingen body fra tilgangsverktøykall.
- **Fem direkte lesende kontroller mot produksjons-MCP:** offentlig katalog, setup-innloggingsside, OAuth-avvisning for access users/keys uten legitimasjon og skjerming av intern admin-backend. Ingen kundedata eller gyldige skrivekall ble hentet/kjørt.
- **Isolerte serverkildetester:** MCP, HTTP-klient og administrasjon ble kjørt på Linux med Go 1.26.6 fra en ren kildekopi på commit `5b4d4322fb6a86a17ca25a800e9ee98845e08652`. Alle fire testpakker bestod, med 115 beståtte test-/deltesthendelser og ingen hoppede tester. Ingen produksjonslegitimasjon ble gitt til testprosessen. Dette er mock-/kildetester, ikke innloggede kall mot produksjon.
- **Statisk native inventar:** 328 unike metode-/sti-operasjoner, 291 klassifiserte tekniker-REST-operasjoner og 37 ekskluderte operasjoner med begrunnelse. Alle eksklusjoner hadde forklaring. Dette er ikke en kjøring av samtlige operasjoner.

Se [lesende live-rapport](evidence/prelaunch-readonly.json), [pakkerapport](evidence/prelaunch-package.json), [serverkildetester](evidence/mcp-source-tests-0.4.0.json) og [inventarkontroll](evidence/native-inventory-audit.json).

## Tilpasninger i skillene

Skillene bruker hele den faktisk annonserte MCP-flaten: search/execute og seks access-verktøy. De beskriver native query/JSON-body, DELETE-body, støttede fil-/multipart-/chunk-formater, offentlige parameternavn, kontovalg, idempotens og strukturerte feil.

MCP 0.4.0 skiller ugyldig SSO, manglende scope, Keycloak-feil og `personal_key_missing`. Rettighetskandidater i generiske 403-feil fremstilles ikke som bekreftede manglende rettigheter. Ved ukjent skriveutfall undersøkes tilstand før nytt forsøk. Rånøkler går aldri gjennom modellen.

Ved flere Tactical-kontoer med lik e-post skal `tactical_user_id` velges fra faktisk resultat. Vanlig bruker uten førstegangskobling bruker beskyttet side eller management-hjelp; e-postlikhet alene gir ikke serverintern nøkkeluthenting. Nøkkeladministrasjonens operatørlogging skilles fra vanlig personlig RMM-logging.

## Tester som først kan gjøres ved installasjon

Siden den tidligere ChatGPT-registreringen er slettet, finnes ingen innlogget tilkobling for kandidaten i denne chatten. Ingen token er hentet fra nettleser, filer, andre chatter eller gateway som omvei. Ny personlig OAuth, faktisk koblingsstatus, rolleisolasjon og nøkkellivssyklus er derfor ikke live-testet her.

Ved første installasjon kontrolleres vertens beskyttede OAuth-oppsett, SSO/MFA, logo, onboarding, alle tre skills, de faktiske verktøyene og et avgrenset personlig lesekall. Bruk egne testidentiteter for vanlig rolle og management, inkludert en uten førstegangskobling. Nøkkelhandlinger og maskinskriving krever eget testmiljø og konkret testbestilling.

GitHub-import med MCP kan bli Desktop only. Nettleserstøtte må kontrolleres i faktisk ChatGPT-arbeidsområde etter den støttede opprettelses-/importflyten; lokale tester eller en ZIP beviser ikke dette. [Arbeidsområdeveiledningen](../plugins/tactical-rmm/docs/WORKSPACE.md) beskriver nødvendige neste steg.

## Lanseringsgrense

Full brukerrettighetsisolasjon og GUI-paritet er ikke godkjent. Interaktiv terminal, native livestrømmer og fjernskrivebord krever fortsatt egne sesjonsintegrasjoner i MCP. [Dekningsrapporten](FUNCTIONAL-COVERAGE.md) skiller registrerte REST-kontrakter fra faktisk testet og manglende funksjon. Kandidaten er klar for sluttkontroll av installasjon, ikke en erklæring om full lanseringsgodkjenning.
