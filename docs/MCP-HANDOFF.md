# MCP: undersøkt status og hva som må bekreftes

**Historisk notat for 1.2.0.** Nyere kilde- og live-kontroll av MCP 0.4.0 finnes i [PRELAUNCH.md](PRELAUNCH.md). Setup-URL og tilgangskatalog er nå bekreftet for testkandidaten. Den tidligere personlige pluginen er slettet etter brukerens bekreftelse; kandidaten deklarerer remote MCP direkte og krever ingen gammel app-ID. Full brukerfunksjonsdekning er fortsatt utestet; se [akseptansemålet](FUNCTIONAL-COVERAGE.md).

Pluginpakke: Tactical RMM 1.2.0. Oppdatert 15. november 2026, Europe/Oslo.

## Hva som er undersøkt

- Ingen Tactical MCP-kilde ble funnet i `/var/Projects` eller `/opt/mcp/tacticalrmm` på denne Linux-verten. Tidligere SSH-forsøk til `mcp-services` ble avvist.
- Codex-prosjektet **MCP - Tactical RMM** finnes på Windows-verten `local`, i `C:\Users\svein\Documents\ChatGPT\Tactical RMM - MPC`. Det er en annen vert enn denne pakkens `nexum-dev`.
- Den aktive chatten **Finn ChatGPT TacticalRMM-tilkobling**, ID `01a1c0b5-d4cc-73e1-ab78-991be3fc5587`, ble lest uten kommandoresultater. Den rapporterer utvikling av selvbetjening, management-administrasjon, oppslag/kobling/opprettelse/fornyelse/fjerning av nøkler og overføring på serversiden. Den beskriver at tilbakekall er separat fra fjerning av MCP-kobling og at gammel nøkkel beholdes som standard ved fornyelse.
- Chatten rapporterer lokale servertester. Disse er **rapportert av MCP-chatten**, ikke kjørt eller kildevalidert her. Full serverkilde på Windows er ikke lest fra denne Linux-verten. Ingen melding ble sendt til eller endringer gjort i den aktive MCP-chatten.
- Offentlig metadata-probe i dette arbeidet returnerte fortsatt serverversjon `0.2.8-command-validation` og de to basisverktøyene `tactical-rmm_search` og `tactical-rmm_execute`. Dette er en uautentisert metadataobservasjon. En rolleavhengig katalog kan vise andre verktøy etter SSO; den nye funksjonen er derfor ikke avkreftet, men er **ikke bekreftet** av denne testen.

Den kjørende serverens siste metadataøyeblikksbilde finnes i `docs/evidence/public-metadata.json`. Tidligere personlig versjonslesing finnes separat i `docs/evidence/live-read.json`; den beviser ikke ny onboarding eller administrasjon.

## Rettet i pluginpakken

Original logo fra Tactical RMMs offisielle frontend-repo er inkludert uendret og referert fra begge manifesters `logo` og `composerIcon`. Kilde og sjekksum følger filen.

En oppsettsskill er registrert som `onboardingSkill` i både portabelt manifest og Codex-kompatibilitetsmanifest. Den bruker vertens beskyttede OAuth-flyt og viser bare en faktisk, verifisert setup-URL. Den forteller at URL-en ikke er tilgjengelig dersom MCP ennå ikke gir en slik URL. Den utgir ikke MCP-protokolladressen for å være en setup-side.

Tilgangsskillen skiller mellom egen selvbetjening og management-administrasjon av andre. Nøkler skal opprettes/hentes og lagres på serveren; ingen nøkkel skal returneres til modellen for å kopieres videre. Manglende kobling, rettighetsavvisning og ukjent resultat behandles separat.

## Dette må MCP-utviklingen levere eller bekrefte

| Punkt | Nødvendig bekreftelse |
| --- | --- |
| Faktisk utrulling | Hvilken versjon/commit er satt i drift på det eksisterende MCP-endepunktet? Lokal bygging er ikke utrulling. |
| Faktisk verktøykatalog | Navn, input-/outputskjema, OAuth-scope og annotasjoner for status, brukeroppslag, nøkkelmetadata, kobling, opprettelse, fornyelse, frakobling og eventuelt tilbakekall. Skillene finner faktiske navn; ingen nye navn er gjettet i pakken. |
| Status før første nøkkel | Etter gyldig SSO skal brukeren kunne lese egen koblingsstatus og setup-URL også uten en personlig Tactical-nøkkel. Dette må ikke fanges av en generell nøkkelkontroll før statusverktøyet får kjøre. |
| Manglende kobling | Dokumentert status/feil som skiller manglende personlig kobling fra ugyldig token, utilstrekkelige rettigheter og andre 403-feil. Ingen nøkkelverdier i svar eller feil. |
| Setup-URL | Eksakt HTTPS-URL, eventuelle brukerreferanser og bekreftet opprinnelse. `https://tactical-mcp.tronderdata.no` er kjent tjenesteopprinnelse, men ingen setup-sti er verifisert. Et annet admin-domene må bekreftes før det legges inn som betrodd. |
| Selvbetjening | Vanlig bruker begrenses til egen faste Keycloak-identitet ved hver forespørsel. E-post/navn brukes bare til søk eller ekstra kontroll, aldri som erstatning for fast identitetskobling. |
| Management | Administrasjon av andre krever faktisk, betrodd gruppemedlemskap ved hver forespørsel. Avklar hvilken kanonisk gruppe-ID/sti som brukes og hvordan tilbakekall får effekt. Chatpåstander og verktøyargumenter gir ingen rolle. |
| Nøkkeloverføring | Eksisterende nøkler identifiseres med metadata; rånøkkelen overføres bare internt mellom Tactical og MCP. Kontroller også feilmeldinger, logger, URL-er og UI-resultater til modellen. |
| Riktig eier | En opprettet/koblet nøkkel skal tilhøre den verifiserte målbrukeren i Tactical. Normal RMM-drift skal fortsatt bruke den innloggede teknikerens personlige kobling. |
| Fornyelse og fjerning | Bekreft standarden for gammel nøkkel, forskjellen mellom frakobling og tilbakekall, samt eventuell påvirkning på andre integrasjoner. Ingen implisitt tilbakekalling under en ren koblingsoperasjon. |
| Delvis feil | Opprettet i Tactical, lagret i MCP og validert tilgang må kunne skilles. Status og eventuell idempotens må hindre blind duplisering etter timeout eller lagringsfeil. |

## Klar melding å bruke i MCP-chatten

> Pluginpakken heter nå Tactical RMM, teknisk navn tactical-rmm, versjon 1.2.0. Den har original logo og egne skills for onboarding, drift og tilgangsadministrasjon. Bekreft hva som faktisk er deployet, og lever en oppdatert kontrakt med faktiske verktøynavn, parameter-/resultatskjemaer, scope og eksakt SSO-beskyttet setup-URL. Status og setup-lenke må fungere etter SSO også før personlig Tactical-nøkkel finnes. Vanlige brukere skal bare håndtere egen konto, management skal kunne håndtere andre. Opprettelse/henting av nøkkel i Tactical og lagring på målbrukeren i MCP skal skje internt på serveren, uten nøkkelverdier i verktøyinput/-output, chat, URL eller logger. Bekreft forskjellen mellom kobling, fornyelse, frakobling og tilbakekall, og hvordan status/idempotens håndterer delvis feil. Rapporter hva som er kilde-/lokaltestet, live-testet og fortsatt utestet. Bruk egne testidentiteter; ikke endre aktive ansattes koblinger som test. Ikke opprett en ny ChatGPT-app eller OAuth-klient for pluginpakken.

## Etter at MCP har bekreftet dette

Oppdater pakken med bekreftet setup-opprinnelse/-URL, faktisk feilsemantikk og eventuelle nødvendige instruksjoner fra verktøyskjemaene. Kjør offentlig metadata-probe, lokale tester og et avgrenset personlig lesekall på nytt. Test med egne roller før vanlig utrulling.

Arbeidsområdeadministrator må dessuten bekrefte gjenbrukbar tilgang til den eksisterende registrerte appen, importere fra [SveinT83/tactical-rmm-plugin](https://github.com/SveinT83/tactical-rmm-plugin) med tom Path og branch `main`, og teste i en ny ChatGPT-nettlesersamtale. Det siste kan ikke bevises med lokal CLI-installasjon. Repoet ble opprettet offentlig etter eierens uttrykkelige valg 15. november 2026.
