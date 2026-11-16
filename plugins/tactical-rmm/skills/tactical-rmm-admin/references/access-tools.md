# Bekreftet katalog: MCP 0.4.0

Følgende er lest fra den kjørende MCP-serverens `tools/list` 16. november 2026. Les alltid gjeldende skjema før bruk; tabellen er et øyeblikksbilde. Vertens navnerom kan komme foran verktøynavnet.

| Verktøy | Virkning og krav |
| --- | --- |
| `tactical-rmm_access_users` | Les SSO-brukere, `mapped` og mulige `tactical_users`. Vanlig bruker ser egen konto; management kan se andre. |
| `tactical-rmm_access_keys` | Les nøkkelmetadata for valgt person/konto. Returnerer ingen nøkkelverdier. |
| `tactical-rmm_access_assign` | Hent eksisterende nøkkel internt og lagre kobling. Krever `idempotency_key` og eid `key_id`. |
| `tactical-rmm_access_create` | Opprett og koble personlig nøkkel. Krever `idempotency_key` og `expiration`. Beholder eksisterende nøkler. |
| `tactical-rmm_access_rotate` | Opprett og koble erstatningsnøkkel. Krever `idempotency_key` og `expiration`. Gammel nøkkel beholdes som standard. |
| `tactical-rmm_access_remove` | Krever `idempotency_key` og uttrykkelig `mode`: `unlink` fjerner MCP-koblingen; `revoke` tilbakekaller angitt eid `key_id`. |

`subject` er fast Keycloak-bruker-ID fra faktisk brukeroppslag. Utelat den for egen konto i henhold til skjemaet. `tactical_user_id` er et numerisk konto-ID fra `tactical_users`; det må velges uttrykkelig når samme e-post finnes på flere Tactical-kontoer og eksisterende verifisert kobling ikke avgjør valget. Ikke velg den første kontoen eller anta at samme e-post betyr samme konto.

Alle skriveoperasjoner krever en unik `idempotency_key` med 16–128 tegn uten blanktegn. Gjenbruk uendret ID og uendrede parametere bare for samme operasjon etter at status er undersøkt; bruk aldri en ny ID som blind retry av et ukjent resultat. Før en ny skriveoperasjon etter timeout skal `access_keys` og eventuell kvittering undersøkes.

`expiration` skal være en uttrykkelig valgt fremtidig RFC3339-tid, høyst 366 dager frem. Bruk dokumentert organisasjonspolicy eller allerede valgt utløp. Hvis ingen slik føring finnes, må ønsket utløp avklares før opprettelse/rotasjon.

`revoke_old` er boolsk og har standard `false`. `true` er bare tillatt for en tidligere MCP-opprettet nøkkel, innenfor brukerens bestilling. Ved «fjern» må `unlink` versus `revoke` være avklart. Beskriv relevant virkning på andre integrasjoner før tilbakekall.

Noen betingede krav står i beskrivelser/servervalidering fremfor i JSON-skjemaets `required`: `key_id` ved assign og revoke, samt idempotenslengde og utløpsgrenser. Følg også disse kravene. Et JSON-skjema som godtar input beviser ikke at serveren vil godta det.

Vanlig bruker uten en verifisert førstegangskobling må registrere egen nøkkel på den beskyttede tilgangssiden eller få hjelp av management. SSO og profil-e-post alene gir ikke rett til serverintern førstegangsuthenting eller opprettelse. Management kan utføre førstegangsoppsett for riktig målbruker.

Beskyttet side: `https://tactical-mcp.tronderdata.no/admin/`. Siden er kildebekreftet og dens offentlige innloggingsvisning er lest over HTTPS. En HTTP 200 på denne siden er ikke bevis på innlogget tilgang.

Vanlige RMM-datakall følger den personlige nøkkelens eier. Native nøkkeladministrasjon bruker en beskyttet operatørnøkkel og kan være logget på dens eier i Tactical; MCPs lokale revisjonslogg registrerer SSO-aktør og målbruker. Ikke påstå at en administrativ nøkkeloperasjon logges som målbrukeren.
