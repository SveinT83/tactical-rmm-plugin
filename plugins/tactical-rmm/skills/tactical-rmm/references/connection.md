# Tilkobling og feilhåndtering

Verifisert offentlig metadata 14. november 2026:

| Felt | Verdi |
| --- | --- |
| MCP | `https://tactical-mcp.tronderdata.no/chatgpt/mcp` |
| Transport | Streamable HTTP |
| OAuth-issuer | `https://auth.tronderdata.no/realms/tronderdata` |
| Scope | `tactical-rmm` |
| Eksisterende forhåndsregistrerte klient | `tactical-chatgpt` |

Pakken deklarerer endepunktet direkte i `mcp.json` og kompatibilitetsfilen `.mcp.json`, med OAuth-modus `provided`, klient-ID `tactical-chatgpt` og `client_secret_basic`. Ingen ID fra den slettede personlige ChatGPT-pluginen kreves. En administrator konfigurerer eventuell klienthemmelighet i vertens beskyttede oppsett; den finnes aldri i pakken eller chatten. Teknikeren bruker deretter personlig SSO. Web-/arbeidsområdeinstallasjonen må fortsatt sluttkontrolleres i ChatGPT.

| Observasjon | Oppførsel |
| --- | --- |
| Feil bekrefter uttrykkelig manglende personlig nøkkelkobling | Bruk den eksakte norske forklaringen fra skillen; administrator må håndtere koblingen på serversiden. |
| 401 / ugyldig eller utløpt token / OAuth-utfordring | Bruk vertens beskyttede OAuth-flyt for samme app og bruker. Ikke be om token eller nøkler. |
| 403, rettigheter uttrykkelig utilstrekkelige | Forklar avvisningen uten å bytte identitet, app eller tilgangsmetode. |
| Generell 403 med ukjent årsak | Rapportér avvist tilgang og ukjent årsak; ikke påstå manglende nøkkelkobling. |
| Parameterfeil / JSON-RPC invalid params | Les gjeldende skjema og rett input før nytt forsøk innenfor bestillingen. Ikke gjett ukjente krav. |
| Timeout / intern feil etter en handling | Resultat kan være ukjent. Undersøk tilstand før gjentakelse. |
| Ingen synlige verktøy | Kontroller installasjon, apprettigheter og synkroniseringsrapport; prøv ny chat ved behov. Ikke opprett dublettapp. |

Ingen stabil feilkode for manglende kobling er kildeverifisert i denne leveransen. Bruk serverens uttrykkelige feilmelding, ikke en oppdiktet kode eller HTTP-status alene. En tillatelsesfeil skal ikke omtolkes til en autentiseringsfeil for å prøve en annen konto.
