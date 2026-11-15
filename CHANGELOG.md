# Endringslogg

## 1.2.0 – 2026-11-15

- Original Tactical RMM-logo fra offisielt repo, med kilde og sjekksum, lagt til som logo og composer-ikon.
- Ny norsk oppsettsskill registrert i begge manifests `onboardingSkill`.
- SSO, manglende-kobling-status og bekreftede setup-lenker håndteres uten gjetting av URL eller nøkkelverdier i chat.
- Tilgangsskillen støtter beskrevet selvbetjening for egen konto og management-administrasjon av andre; faktisk serverstøtte må fortsatt verifiseres.
- MCP-utviklingschat og kjørende offentlig katalog undersøkt hver for seg. Konkrete gjenstående krav og testgrenser dokumentert.

## 1.1.0 – 2026-11-14

- Ny norsk administrasjonsskill for kommende management-verktøy og SSO-beskyttede administrasjonslenker.
- Arbeidsflyt for opprettelse/henting i Tactical og kobling til riktig bruker i MCP, uten nøkkelverdier i verktøyinput, verktøyresultater eller chat.
- Dokumenterte serverkrav for management-autorisasjon, fast målidentitet, rotasjon, delvis feil og kontroll før gjentakelse.
- Tidligere generelt forbud mot administrasjonsverktøy er erstattet med den bestilte, serverstyrte administrasjonsflyten. Vanlig RMM-drift beholder personlig identitet.
- Serverfunksjonene er fortsatt under utvikling og er ikke implementert eller live-testet av pluginpakken.

## 1.0.0 – 2026-11-14

- Første pakke med visningsnavn Tactical RMM og utgiver Trønder Data.
- Agent Plugins 1.0, Codex-kompatibilitet og GitHub-marketplace.
- Norsk driftsskill og referanse til verifisert eksisterende app.
- Lokal validering, avgrenset metadata-probe, bygging og dokumentasjon.
- Arbeidsområdedeling, nettleserimport og flerbrukerisolasjon gjenstår å teste.
