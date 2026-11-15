# MCP 0.3.2: kontrakt og gjenværende akseptanse

Dette er kontrakten som er observert i offentlig verktøykatalog og gjennomgått i utvalgt MCP-kilde. Det er ikke en godkjenning av innlogget funksjon, flerbrukerisolasjon eller full dekning av Tactical RMM.

## Observerte deler

- HTTPS-endepunktet er `https://tactical-mcp.tronderdata.no/chatgpt/mcp` og oppsettssiden er `https://tactical-mcp.tronderdata.no/admin/`.
- Katalogen har basisverktøyene search/execute og seks access-verktøy for brukere, nøkkelmetadata, kobling, opprettelse, rotasjon og fjerning.
- Alle annonserer OAuth med scope `tactical-rmm`. Access users/keys er lesende; andre access-operasjoner endrer tilstand.
- `subject` identifiserer fast SSO-person. `tactical_user_id` velger riktig native konto når e-post ikke er entydig. ID-er hentes fra faktiske resultater.
- Nøkkelverdier behandles internt på serveren. Skillen skal ikke bruke det generelle API-verktøyet til å flytte rånøkler.
- Management kan administrere andre. Vanlige brukeres serverinterne nøkkeloperasjoner krever eksisterende verifisert kobling; førstegangsoppsett skjer på siden eller med hjelp fra management.
- Idempotens, utløp, kontovalidering og valg mellom unlink/revoke må følges også når begrensningen bare er beskrevet i verktøyteksten og servervalideringen.

Se [parameterreferansen](../skills/tactical-rmm-admin/references/access-tools.md) og [administratorveiledningen](ADMIN.md).

## Gjenværende live-akseptanse

1. Les egen koblingsstatus etter personlig SSO, også for en egen testidentitet uten førstegangskobling. Bekreft riktig setup-lenke uten å tolke enhver 403 som manglende kobling.
2. Test vanlig rolle og management med egne identiteter. En vanlig bruker skal ikke få andre brukeres data eller handlinger, og fjernet gruppetilgang skal håndteres etter dokumentert policy.
3. Kontroller riktig Tactical-konto ved like e-postadresser. Uautorisert identitetsbytte og nøkkel fra feil konto må avvises.
4. Test nøkkelopprettelse, kobling, rotasjon, frakobling og tilbakekall bare på testidentiteter etter en uttrykkelig testbestilling. Skill mellom opprettet i Tactical, lagret i MCP og validert tilgang.
5. Kontroller idempotens, delvis feil og kvitteringer uten blind gjentakelse. Verifiser at rånøkler ikke returneres eller logges.
6. Test faktisk installasjon, apprettigheter, SSO, onboarding og verktøytilgjengelighet i ChatGPT-nettleseren. En lokal pakkeinstallasjon beviser ikke dette.

## Hele brukerens funksjonsflate

Akseptansemålet er at en bruker kan utføre alt vedkommende har rettigheter til i Tactical RMM via MCP. Det krever en oversikt over faktiske UI-arbeidsflyter, aktuelle API-/verktøyoperasjoner, parametere, retur-/jobbstatus og brukerrettigheter. Ekstra deployment-begrensninger må synliggjøres som egne avvik. En generell API-katalog alene er ikke bevis på full dekning.

Pluginens før-lanseringsskript tester bare lesende oppdagelse og uautentiserte avvisninger. Ingen av live-akseptansetestenes nøkkelhandlinger er utført av dette prosjektet.
