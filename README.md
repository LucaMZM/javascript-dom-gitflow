# JavaScript DOM i Git Flow

Pràctica 1 — Sistemes de control de versions. Luca Mazmishvili (LucaMZM).
Professor: enminqui2.

Aplicació educativa en valencià, sense dependències de producció.
Servir amb `npm start` i obrir http://localhost:8080.

Les tres persones de l'enunciat es simulen exclusivament als missatges de commit.
L'autoria Git real es conserva. Les branques es creen abans del treball i les
fusions es realitzen amb `--no-ff`.

Documentació: https://lucamzm.github.io/javascript-dom-gitflow/
Aplicació publicada: https://lucamzm.github.io/javascript-dom-gitflow/app/

## Referència de partida
HTML5 Boilerplate v9.0.1, https://github.com/h5bp/html5-boilerplate.
S'adapten la plantilla HTML i els estils base; es conserven les llicències.
L'enunciat original s'ha localitzat i revisat durant el procés. La referència
al docent s'actualitza a enminqui2. La base visual conserva capçalera,
navegació, contingut central i peu.

## Project i comprovacions
https://github.com/users/LucaMZM/projects/1

Les proves del DOM es troben en `tests/dom.cjs`. Requereixen Playwright només
per al desenvolupament; l'aplicació publicada no necessita cap dependència.
Executar amb `node tests/dom.cjs` després d'iniciar el servidor local.
Les eixides autèntiques es conserven en `evidencias/terminal/` i les captures
de navegador en les subcarpetes d'evidències.
