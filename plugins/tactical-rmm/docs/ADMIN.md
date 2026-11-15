# Personlig tilgang og nøkkeladministrasjon

## Bekreftet kontrakt

MCP `0.3.2-admin-repair` annonserer seks `tactical-rmm_access_*`-verktøy. Den beskyttede siden er `https://tactical-mcp.tronderdata.no/admin/`. Katalogen, utvalgte kildefiler og den uautentiserte innloggingssiden er kontrollert fra pluginprosjektet. Innlogget funksjon og rolleisolasjon er ikke selvstendig live-testet her.

Teknikeren bruker egen Keycloak/SSO-konto og eventuell MFA. Appen refererer til den eksisterende OAuth-klienten `tactical-chatgpt`, issuer `https://auth.tronderdata.no/realms/tronderdata` og scope `tactical-rmm`. Kildedokumentasjonen oppgir authorization code, PKCE S256 og `client_secret_basic`. Klienthemmelighet, klientpolicy og ny full OAuth-flyt er ikke lest eller endret av pluginutviklingen.

Vanlige Tactical-datakall bruker nøkkelen koblet til autentisert, fast Keycloak-`sub`. E-post og navn brukes til oppslag og ekstra kontroll, ikke som erstatning for identiteten. Ingen annen persons nøkkel brukes som reserve for vanlig RMM-drift.

## Førstegangsoppsett

Vanlige brukere uten en verifisert personlig kobling må registrere en nøkkel de allerede har på den beskyttede siden, eller få hjelp av management. SSO og e-post alene gir ikke serverintern rett til å hente eller opprette den første nøkkelen. Når management fullfører koblingen på forhånd, kan teknikeren bruke pluginen med SSO uten selv å håndtere nøkkelen.

På tilgangssiden velges riktig SSO-person og riktig Tactical-konto. Flere aktive Tactical-kontoer kan ha samme e-post; valgt konto og nøkkelens faktiske eier må da stemme. Nøkkelen kan legges inn direkte i sidens passordfelt, uten chat eller nettleserautomatisering som gjør den tilgjengelig for modellen.

En generell 403 eller en OAuth-utfordringsheader bekrefter ikke alene manglende kobling. Kildekoden kan returnere generell 403 ved utilgjengelig personlig nøkkelfil. Bruk bekreftet koblingsstatus fra access-verktøyet før årsaken fastslås; `mapped` sier bare at koblingen finnes.

## Selvbetjening og management

Vanlig bruker begrenses til egen faste identitet og kontoen serveren kan verifisere. Administrasjon av andre krever gjeldende management-medlemskap. MCP-utviklingens dokumentasjon oppgir kontroll mot en fast Keycloak-gruppe-ID og kontroll på nytt ved hver beskyttet forespørsel. Faktisk tilbakekall/rolleisolasjon er ikke testet fra pluginchatten.

Bruk de dedikerte verktøyene til metadata, kobling, opprettelse, rotasjon og fjerning. [Tilgangsskillens referanse](../skills/tactical-rmm-admin/references/access-tools.md) beskriver verifiserte parametere. Modellen skal aldri hente selve nøkkelen for å sende den videre i neste verktøykall.

Skriveoperasjoner krever unik idempotens-ID. Nye/roterte nøkler krever fremtidig RFC3339-utløp innen 366 dager. Ved ukjent resultat må status undersøkes før et nytt skriveforsøk. Rotasjon beholder gammel nøkkel som standard; frakobling og tilbakekall er ulike operasjoner.

## Revisjon og grenser

Vanlige RMM-datakall registreres på den personlige nøkkelens eier. Native nøkkeladministrasjon bruker ifølge serverkilden en beskyttet operatørnøkkel og kan vise dens eier i Tactical. MCPs lokale revisjonslogg registrerer faktisk SSO-aktør og målbruker. Ikke påstå at nøkkeladministrasjon logges som målbrukeren.

Ingen nøkkelverdier skal finnes i verktøyinput/-output, chat, URL, feildetaljer eller åpne logger. Ingen aktive koblinger, produksjonsnøkler eller kundemaskiner er endret av pluginens før-lanseringstest. Test på egne identiteter før livssyklus- eller isolasjonstester godkjennes. Serverkode og deployment har en separat prosess fra pluginpakken.
