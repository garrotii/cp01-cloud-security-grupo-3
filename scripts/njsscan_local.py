"""Ponte local para Windows. As regras, resultados e exportadores são do njsscan.

libsast 3.1.8 pula a análise semântica no Windows. Aqui chamamos o mesmo
Semgrep que a função original chama no Linux, usando a versão oficial Windows.
O container e o GitHub Actions usam njsscan normal, sem esta ponte.
"""
import os
import sys
from pathlib import Path

os.environ['PATH']=str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH','')
if os.name=='nt':
    from libsast.core_sgrep import helpers, semantic_sgrep
    def invoke_windows(paths,scan_rules):
        command=['semgrep','scan','--metrics=off','--disable-version-check',
                 '--quiet','--no-rewrite-rule-ids','--json','--config',scan_rules]
        return helpers._invoke_semgrep_batched(command,[p.as_posix() for p in paths])
    semantic_sgrep.invoke_semgrep=invoke_windows
from njsscan.__main__ import main
if __name__=='__main__':
    main()
