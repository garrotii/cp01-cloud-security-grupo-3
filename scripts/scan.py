"""Mesma execução no container e no GitHub Actions, sem esconder erros."""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('alvo',choices=['inseguro','corrigido'])
args=p.parse_args()
root=Path(__file__).resolve().parents[1]
os.chdir(root)
folder=Path('reports')/args.alvo
folder.mkdir(parents=True,exist_ok=True)
for name in ('njsscan.json','njsscan.sarif','npm-audit.json','gate.json'):
    (folder/name).unlink(missing_ok=True)
target=Path('targets')/args.alvo
env=os.environ.copy()
env.update({'SEMGREP_SEND_METRICS':'off','SEMGREP_ENABLE_VERSION_CHECK':'0','PYTHONIOENCODING':'utf-8'})
env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
# Permite usar o npm local do ambiente de preparação, sem mudar o comando da aula.
npm=[env['CP_NPM_NODE'],env['CP_NPM_CLI']] if 'CP_NPM_CLI' in env else (['npm.cmd'] if os.name=='nt' else ['npm'])
scanner=[sys.executable,'scripts/njsscan_local.py'] if os.name=='nt' else [sys.executable,'-m','njsscan']
commands=[
 ('njsscan-json',scanner+[str(target),'--json','-o',str(folder/'njsscan.json')],None),
 ('njsscan-sarif',scanner+[str(target),'--sarif','-o',str(folder/'njsscan.sarif')],None),
 ('npm-audit',npm+['audit','--json','--audit-level=high','--ignore-scripts'],target),
]
record={'data_utc':datetime.now(timezone.utc).isoformat(),'alvo':args.alvo,'ambiente':sys.platform,'python':sys.version.split()[0],'adaptacao_windows':os.name=='nt','execucoes':[]}
for name,command,cwd in commands:
    start=time.perf_counter()
    r=subprocess.run(command,cwd=cwd,env=env,text=True,encoding='utf-8',errors='replace',capture_output=True)
    duration=round(time.perf_counter()-start,3)
    if name=='npm-audit':
        (folder/'npm-audit.json').write_text(r.stdout,encoding='utf-8')
    (folder/(name+'.txt')).write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
    record['execucoes'].append({'ferramenta':name,'segundos':duration,'exit_code':r.returncode})
    print(f'{name}: terminou em {duration}s, código {r.returncode}')
    # 0 = sem alertas, 1 = alertas. Outros códigos são falha do scanner.
    if r.returncode not in (0,1):
        (folder/'execucao.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
        print('Falha do scanner. Consulte o relatório de execução.'); sys.exit(2)
    expected={'njsscan-json':'njsscan.json','njsscan-sarif':'njsscan.sarif','npm-audit':'npm-audit.json'}[name]
    if not (folder/expected).is_file() or not (folder/expected).stat().st_size:
        print('Falha: o scanner não gerou o relatório esperado.'); sys.exit(2)
(folder/'execucao.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r=subprocess.run([sys.executable,'scripts/gate.py',str(folder)],env=env)
sys.exit(r.returncode)
