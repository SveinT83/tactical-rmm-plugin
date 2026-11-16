# Én Tactical RMM-plugin med SSO og GitHub-oppdateringer

Dette erstatter den tidligere planen om en GitHub-wrapper som inkluderer en
separat SSO-plugin. Brukeren har valgt én kanonisk SSO-plugin, overtatt av GitHub,
med navn Tactical RMM og de tre eksisterende ferdighetene.

## Verifisert registrering 16. november 2026

Plugin Creator har lest den nye registreringens metadata og begge kildefiler:

- Plugin-ID: `plugin_asdk_app_6afafd3b578c8191a62956239872dd3b`.
- Teknisk navn: `dev-6afafd3b578c8191a62956239872dd3b`.
- App-ID: `asdk_app_6afafd3b578c8191a62956239872dd3b`.
- Scope/discoverability: `USER` / `PRIVATE`.
- Versjon: `1.0.0`. Brukeren bekrefter fungerende personlig SSO.

Det er foreløpig en personlig registrering. Ikke bruk denne plugin-ID-en som
`pluginId` i arbeidsområdets markedsplass før arbeidsområdescope er bekreftet.
OpenAIs GitHub-overtakelse krever samme arbeidsområde og nøyaktig teknisk navn.

## Neste steg

1. Administrator gjør SSO-koblingen tilgjengelig for Trønder Data gjennom
   arbeidsområdets publiseringsflyt. Hvis det opprettes en ny arbeidsområde-ID,
   må den leses fra faktisk metadata; ikke anta at den personlige ID-en beholdes.
2. Les metadata og kilde på nytt. Kontroller `WORKSPACE`, riktig workspace-ID,
   faktisk teknisk navn, plugin-ID, app-ID og versjon.
3. Klargjør GitHub-overtakelse med verifisert `pluginId` og samme tekniske navn
   i markedsplass og manifest. Bevar den kanoniske appkoblingen og SSO-oppsettet.
   Ikke opprett en ny wrapper. `scripts/bind_app.py` implementerer den eldre
   wrapper-overgangen og skal ikke kjøres uendret for denne migreringen.
4. Kontroller ferdigheter, logo, metadata, bygg og faktisk klient. Push ferdig
   kilde til `main`; administrator synkroniserer og kontrollerer at samme
   kanoniske plugin-ID nå styres fra GitHub og fortsatt har tilknyttede kontoer.
5. Ta den gamle importerte wrapperen
   `Plugin_960c953284a0819184889146d979392f` ut av bruk som en separat handling.
   Fjernet marketplace-entry etterlater workspace-kopien som «No longer in source»;
   den blir ikke automatisk slettet. Ikke slett hele markedsplassen eller den
   nye underliggende SSO-koblingen.

Intern publisering og arbeidsområdetilgang kan ikke utføres med de tilgjengelige
Plugin Creator-verktøyene her. Ingen GitHub-overtakelse eller opprydding i
arbeidsområdet er utført ennå. Klienten i Keycloak er allerede offentlig,
med PKCE S256 og uten behov for klienthemmelighet.

Kilder: [GitHub-overtakelse](https://learn.chatgpt.com/docs/enterprise/plugin-management#move-an-existing-plugin-to-github-management),
[publisering i arbeidsområdet](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt).
