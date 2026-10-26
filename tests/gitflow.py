#!/usr/bin/env python3
"""Read-only audit of this practice's Git Flow topology."""
import subprocess,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
checks=[]
def git(*args):
 p=subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True)
 if p.returncode: raise RuntimeError(p.stderr.strip())
 return p.stdout.strip()
def sha(ref): return git('rev-parse',ref)
def parents(ref): return git('show','-s','--format=%P',ref).split()
def check(name,actual,expected=True): checks.append(dict(name=name,actual=actual,expected=expected,pass_=actual==expected))
def ancestor(ref,branch): return subprocess.run(['git','merge-base','--is-ancestor',ref,branch],cwd=ROOT).returncode==0
features=[('feature/contingutHTML','3c786f4','70ce7aa'),('feature/atributsHTML','70ce7aa','d4b7b6f'),('feature/estilsCSS','d4b7b6f','8201996')]
for branch,base,merge in features:
 check(branch+' parent inicial',parents(branch)[0],sha(base))
 pp=parents(merge)
 check(merge+' té dos pares',len(pp),2)
 check(merge+' primer pare develop previ',pp[0],sha(base))
 check(merge+' segon pare feature',pp[1],sha(branch))
for branch in ['main','develop']:
 check('release/v1.0 ancestre '+branch,ancestor('release/v1.0',branch))
 check('hotfix/milloresV_1_0 ancestre '+branch,ancestor('hotfix/milloresV_1_0',branch))
check('hotfix naix de v1.0',parents('hotfix/milloresV_1_0')[0],sha('v1.0^{}'))
for ref in ['3c277c4','6d9b2ba','d0c5a2c','80e5ffb']:
 check(ref+' merge té dos pares',len(parents(ref)),2)
for tag in ['v1.0','v1.0.1']:
 check(tag+' és etiqueta anotada',git('cat-file','-t',tag),'tag')
check('v1.0 i v1.0.1 diferents',sha('v1.0^{}')!=sha('v1.0.1^{}'))
for file in ['app.js','index.html','style.css','package.json']:
 check(file+' idèntic main i develop',sha('main:'+file),sha('develop:'+file))
expected=['main','develop','feature/contingutHTML','feature/atributsHTML','feature/estilsCSS','release/v1.0','hotfix/milloresV_1_0','gh-pages']
remotes=git('for-each-ref','--format=%(refname:short)','refs/remotes/origin/').splitlines()
check('huit branques de seguiment remot',sorted(remotes),sorted('origin/'+x for x in expected))
remote_heads=git('ls-remote','--heads','origin').splitlines()
check('huit branques publicades',sorted(line.split()[1] for line in remote_heads),sorted('refs/heads/'+x for x in expected))
report={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':[{('pass' if k=='pass_' else k):v for k,v in item.items()} for item in checks],'localRefs':git('show-ref').splitlines(),'remoteHeads':remote_heads,'notes':['L’auditoria consulta Git sense modificar branques ni commits.','Els commits documentals locals poden estar pendents del pròxim push.']}
report['passed']=all(c['pass'] for c in report['checks'])
output=ROOT/'evidencias/git/audit.json';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if report['passed'] else 1)
