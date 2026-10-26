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

select('#color-change').addEventListener('click', () => {
  select('#style-result').style.color = '#9c2348';
});
select('#size-change').addEventListener('input', (event) => {
  select('#style-result').style.fontSize = event.target.value + 'px';
  select('#size-result').textContent = event.target.value + ' px';
});
select('#class-change').addEventListener('click', (event) => {
  const active = select('#style-result').classList.toggle('highlight');
  event.currentTarget.setAttribute('aria-pressed', String(active));
});
select('#reset-style').addEventListener('click', () => {
  const result = select('#style-result');
  result.style.color = '';
  result.style.fontSize = '20px';
  result.classList.remove('highlight');
  select('#size-change').value = '20';
  select('#size-result').textContent = '20 px';
  select('#class-change').setAttribute('aria-pressed', 'false');
});
