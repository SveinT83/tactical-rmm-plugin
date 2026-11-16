# Valideringsschema

`plugin.schema.json` er hentet uendret fra [Agent Plugins 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) 14. november 2026. Den versjonerte kopien lar pakkens tester kjøre uten nettverk. Schemaets `extensions` er åpne; `scripts/validate.py` kontrollerer derfor også prosjektets appreferanse, OpenAI-presentasjon, kompatibilitet og filstier eksplisitt.

Ved formatoppdatering: vurder gjeldende offisiell dokumentasjon, gjennomgå schema-diff og tilpass tester og pakke samlet. Ikke oppgrader schema eller registrer en ny tilkobling som en automatisk del av et bygg.

Validator og bygg støtter også BookStacks native appformat uten portabelt rotmanifest. Da kontrolleres `.codex-plugin/plugin.json`, obligatorisk `.app.json`, registreringsmetadata og fravær av parallelle MCP-deklarasjoner. Denne grenen bruker ikke det portable rotmanifestets schema. Støtten aktiverer ingen registrering av seg selv. Se [SSO-overgangen](../docs/SSO-CONNECTION.md).

## MCP og OpenAI OAuth-utvidelsen

`mcp.schema.json` er hentet uendret fra Agent Plugins 1.0.0 16. november 2026. OpenAIs offisielle pakkedokumentasjon beskriver `extensions.com.openai.auth` per server, mens den publiserte portable JSON-schema-filen foreløpig ikke tillater `extensions` i serverobjektene. Validatoren kontrollerer derfor standard transportprojeksjon mot det uendrede offisielle schemaet og kontrollerer den dokumenterte OpenAI-utvidelsen separat, inkludert eksakt provided-klient og fravær av hemmeligheter. Dette er ikke en påstand om at hele filen validerer mot det nakne portable schemaet i en klient uten OpenAI-støtte.

Kilde: https://developers.openai.com/plugins/build/plugins#configure-mcp-authentication . Den faktiske ChatGPT-importen og OAuth-dialogen må fortsatt testes; schema-/CLI-kontroll alene beviser ikke nettleserstøtte.
