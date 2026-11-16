# Tactical RMM

Versjon 1.4.0 · Trønder Data.

Én SSO-plugin med tre norske ferdigheter og original Tactical-logo. GitHub-kilden
overtar samme registrerte plugin, slik at tilknyttede kontoer kan beholdes.
Teknisk navn `dev-6afafd3b578c8191a62956239872dd3b` må samsvare med registreringen;
visningsnavnet er **Tactical RMM**.

- [Oppsett og SSO](skills/tactical-rmm-setup/SKILL.md)
- [Drift og native API](skills/tactical-rmm/SKILL.md)
- [Personlig tilgang og management](skills/tactical-rmm-admin/SKILL.md)
- [Arbeidsområde, synk og opprydding](docs/WORKSPACE.md)

Bruk egen Keycloak-konto. Klienten bruker PKCE S256 uten klienthemmelighet.
Management kan klargjøre personlig Tactical-tilgang på MCP-serveren; manglende
nøkkelkobling håndteres på den beskyttede oppsettsiden, aldri ved å lime inn nøkler i chat.

Arbeidsområdesynk og personlig tilgang etter GitHub-overtakelsen må kontrolleres.
Full rettighetsisolasjon og interaktiv GUI-paritet er ikke dokumentert av en pakketest.
