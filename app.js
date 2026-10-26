'use strict';
// Cada funcionalitat s'incorpora des de la seua branca de treball.

const select = (selector) => document.querySelector(selector);
select('#apply-text').addEventListener('click', () => {
  // textContent evita interpretar HTML escrit per l'usuari.
  select('#text-result').textContent = select('#new-text').value;
});
select('#apply-html').addEventListener('click', () => {
  // Només s'interpreta una plantilla fixa de confiança.
  select('#html-result').innerHTML = '<strong>Hola, DOM!</strong> Ara amb format.';
});

select('#set-attr').addEventListener('click', () => {
  select('#demo-link').setAttribute('title', select('#attribute-text').value);
  select('#attr-result').textContent = 'Atribut title actualitzat.';
});
select('#read-attr').addEventListener('click', () => {
  select('#attr-result').textContent = select('#demo-link').getAttribute('title');
});
select('#toggle-disabled').addEventListener('click', () => {
  const button = select('#target-button');
  button.disabled = !button.disabled;
  select('#prop-result').textContent = 'disabled = ' + button.disabled;
});
