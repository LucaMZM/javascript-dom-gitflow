const fs = require('fs');
const {chromium} = require('playwright');
const destination = process.env.QA_OUTPUT || require('path').resolve(__dirname, '../evidencias/aplicacion/qa.json');
(async () => {
 const report = {date:new Date().toISOString(),url:process.env.QA_URL || 'http://localhost:8080',checks:[],errors:[]};
 const browser = await chromium.launch({...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {}),headless:true});
 const page = await browser.newPage({viewport:{width:1280,height:900}});
 page.on('pageerror', e => report.errors.push({kind:'pageerror',message:e.message}));
 page.on('console', m => {if(m.type()==='error') report.errors.push({kind:'console',message:m.text()});});
 async function check(name,fn){try{await fn();report.checks.push({name,pass:true});}catch(e){report.checks.push({name,pass:false,error:e.message});}}
 function assert(value,message){if(!value) throw Error(message);}
 try {
 await page.goto(report.url,{waitUntil:'networkidle'});
 await check('textContent conserva HTML com a text sense executar-lo',async()=>{
 const value='<img src=x onerror="window.qaExecuted=true"> <strong>Hola</strong>';
 await page.fill('#new-text',value); await page.click('#apply-text');
 assert(await page.locator('#text-result').textContent()===value,'Text alterat');
 assert(await page.locator('#text-result *').count()===0,'HTML interpretat');
 assert(!await page.evaluate(()=>window.qaExecuted),'S’ha executat contingut');
 });
 await check('innerHTML interpreta la plantilla fixa',async()=>{await page.click('#apply-html');assert(await page.locator('#html-result strong').textContent()==='Hola, DOM!','Falta estructura strong');});
 await check('setAttribute i getAttribute title',async()=>{await page.fill('#attribute-text','Títol verificat per QA');await page.click('#set-attr');assert(await page.locator('#demo-link').getAttribute('title')==='Títol verificat per QA','title incorrecte');await page.click('#read-attr');assert(await page.locator('#attr-result').textContent()==='Títol verificat per QA','Lectura incorrecta');});
 await check('disabled alterna en els dos sentits',async()=>{assert(await page.locator('#target-button').isDisabled(),'Valor inicial');await page.click('#toggle-disabled');assert(await page.locator('#target-button').isEnabled(),'No activa');await page.click('#toggle-disabled');assert(await page.locator('#target-button').isDisabled(),'No desactiva');});
 await check('color CSS visible',async()=>{await page.click('#color-change');assert(await page.locator('#style-result').evaluate(e=>getComputedStyle(e).color)==='rgb(156, 35, 72)','Color incorrecte');});
 await check('mida CSS i indicador',async()=>{await page.locator('#size-change').fill('36');assert(await page.locator('#style-result').evaluate(e=>getComputedStyle(e).fontSize)==='36px','Mida incorrecta');assert(await page.locator('#size-result').textContent()==='36 px','Indicador incorrecte');});
 await check('classe CSS i aria-pressed',async()=>{await page.click('#class-change');assert(await page.locator('#style-result').evaluate(e=>e.classList.contains('highlight')),'Classe absent');assert(await page.locator('#class-change').getAttribute('aria-pressed')==='true','Estat accessible incorrecte');await page.click('#class-change');assert(!await page.locator('#style-result').evaluate(e=>e.classList.contains('highlight')),'Classe no eliminada');});
 await check('restabliment complet dels estils',async()=>{await page.click('#class-change');await page.click('#reset-style');assert(await page.locator('#style-result').evaluate(e=>e.style.color===''&&e.style.fontSize==='20px'&&!e.classList.contains('highlight')),'Estils no restablits');assert(await page.locator('#size-change').inputValue()==='20','Control no restablit');assert(await page.locator('#class-change').getAttribute('aria-pressed')==='false','ARIA no restablit');});
 await check('tots els ancoratges interns tenen destinació',async()=>{const missing=await page.evaluate(()=>[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.href));assert(missing.length===0,JSON.stringify(missing));});
 for(const width of [390,768,1280]) await check(`responsive ${width}px sense desbordament horitzontal`,async()=>{await page.setViewportSize({width,height:900});await page.waitForTimeout(50);const sizes=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));assert(sizes.scroll<=sizes.viewport,JSON.stringify(sizes));});
 if(await page.locator('#reset-content').count()){
 await check('hotfix compta punts de codi Unicode i text buit',async()=>{await page.fill('#new-text','Hola 👋');await page.click('#apply-text');assert(await page.locator('#text-count').textContent()==='6 caràcters aplicats','Comptador Unicode incorrecte');await page.fill('#new-text','');await page.click('#apply-text');assert(await page.locator('#text-count').textContent()==='0 caràcters aplicats','Comptador buit incorrecte');});
 await check('hotfix restablix contingut i comptador',async()=>{await page.fill('#new-text','Prova del comptador');await page.click('#apply-text');assert(await page.locator('#text-count').textContent()==='19 caràcters aplicats','Comptador incorrecte');await page.click('#apply-html');await page.click('#reset-content');assert(await page.locator('#text-result').textContent()==='Este text canviarà.','Resultat no restablit');assert(await page.locator('#new-text').inputValue()==='Hola, JavaScript!','Entrada no restablida');assert(await page.locator('#html-result').textContent()==='Encara no hi ha format.','HTML no restablit');assert(await page.locator('#html-result *').count()===0,'Format residual');assert(await page.locator('#text-count').textContent()==='0 caràcters aplicats','Comptador no restablit');});
 }
 const urls=await page.locator('a[href^="http"]').evaluateAll(elements=>[...new Set(elements.map(a=>a.href))]);
 report.externalLinks=[];for(const url of urls){try{const response=await page.request.get(url,{timeout:20000});report.externalLinks.push({url,status:response.status(),finalUrl:response.url(),ok:response.ok()});}catch(error){report.externalLinks.push({url,ok:false,error:error.message});}}
 await check('cap error JavaScript ni error de consola',async()=>assert(report.errors.length===0,JSON.stringify(report.errors)));
 } finally {await browser.close();report.localTestsPassed=report.checks.every(c=>c.pass)&&report.errors.length===0;report.externalLinksPassed=(report.externalLinks||[]).every(link=>link.ok);report.passed=report.localTestsPassed&&report.externalLinksPassed;fs.mkdirSync(require('path').dirname(destination),{recursive:true});fs.writeFileSync(destination,JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));process.exitCode=report.localTestsPassed?0:1;}
})().catch(e=>{console.error(e);process.exitCode=1});
