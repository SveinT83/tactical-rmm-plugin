# Valideringsschema

`plugin.schema.json` er hentet uendret fra [Agent Plugins 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) 14. november 2026. Den versjonerte kopien lar pakkens tester kjøre uten nettverk. Schemaets `extensions` er åpne; `scripts/validate.py` kontrollerer derfor også prosjektets appreferanse, OpenAI-presentasjon, kompatibilitet og filstier eksplisitt.

Ved formatoppdatering: vurder gjeldende offisiell dokumentasjon, gjennomgå schema-diff og tilpass tester og pakke samlet. Ikke oppgrader schema eller registrer en ny tilkobling som en automatisk del av et bygg.
