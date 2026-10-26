import subprocess,sys,pathlib,json,datetime
root=pathlib.Path(__file__).resolve().parents[1]
name=sys.argv[1]; cmd=sys.argv[2:]
r=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
p=root/'evidencias/terminal'/f'{name}.txt'
state=subprocess.run(['git','status','--short','--branch'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
head=subprocess.run(['git','rev-parse','HEAD'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
s=f'Data UTC: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n$ '+__import__('shlex').join(cmd)+f'\n{r.stdout}\nCodi de retorn: {r.returncode}\n$ git status --short --branch\n{state.stdout}\nHEAD: {head.stdout}'
p.write_text(s);print(s)
with (root/'evidencias/registre.jsonl').open('a') as f:f.write(json.dumps({'id':name,'command':cmd,'returncode':r.returncode,'file':str(p.relative_to(root))})+'\n')
sys.exit(r.returncode)
