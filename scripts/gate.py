"""Gate do grupo: não aceita relatório ausente, inválido ou erro do scanner."""
import json
import sys
from pathlib import Path

def evaluate(folder):
    folder=Path(folder)
    sast=json.loads((folder/'njsscan.json').read_text(encoding='utf-8-sig'))
    sca=json.loads((folder/'npm-audit.json').read_text(encoding='utf-8-sig'))
    if not isinstance(sast,dict) or not all(k in sast for k in ('nodejs','templates','errors')):
        raise ValueError('Formato SAST inválido')
    if sast['errors']:
        raise ValueError('O njsscan registrou erro de execução')
    if 'error' in sca or sca.get('auditReportVersion') != 2:
        raise ValueError('O npm audit não produziu um relatório válido')
    counts={'sast_high':0,'sast_moderate':0,'sast_low':0}
    findings=[]
    for category in ('nodejs','templates'):
        for rule,data in sast[category].items():
            severity=data['metadata']['severity'].upper()
            mapping={'ERROR':'high','WARNING':'moderate','INFO':'low'}
            if severity not in mapping:
                raise ValueError('Severidade SAST desconhecida: '+severity)
            count=len(data['files'])
            counts['sast_'+mapping[severity]]+=count
            findings.append({'regra':rule,'nivel_original':severity,'nivel_gate':mapping[severity].upper(),'ocorrencias':count,'cwe':data['metadata'].get('cwe','')})
    vulnerability_counts=sca['metadata']['vulnerabilities']
    for key in ('high','critical','moderate','low'):
        value=vulnerability_counts[key]
        if not isinstance(value,int) or value<0:
            raise ValueError('Contagem SCA inválida')
        counts['sca_'+key]=value
    blocked=bool(counts['sast_high']+counts['sca_high']+counts['sca_critical'])
    return {'alvo':folder.name,'status':'BLOQUEADO' if blocked else 'APROVADO','exit_code':1 if blocked else 0,'politica':'SAST ERROR = HIGH por decisão do grupo; SCA HIGH/CRITICAL bloqueiam','contagens':counts,'achados_sast':findings}

def main():
    if len(sys.argv)!=2:
        print('Uso: python scripts/gate.py reports/inseguro'); return 2
    try:
        result=evaluate(sys.argv[1])
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print('ERRO: não foi possível avaliar os relatórios: '+str(exc)); return 2
    Path(sys.argv[1],'gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result['exit_code']
if __name__=='__main__':
    sys.exit(main())
