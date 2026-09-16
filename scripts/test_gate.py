"""Confere a política e a reação a falhas, usando os relatórios do laboratório."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from gate import evaluate

ROOT=Path(__file__).resolve().parents[1]

class GateTest(unittest.TestCase):
    def test_versao_insegura_bloqueia(self):
        result=evaluate(ROOT/'reports/inseguro')
        self.assertEqual(result['exit_code'],1)
        self.assertEqual(result['contagens']['sast_high'],3)
        self.assertEqual(result['contagens']['sca_high'],1)

    def test_versao_corrigida_passou_na_data_registrada(self):
        self.assertEqual(evaluate(ROOT/'reports/corrigido')['exit_code'],0)

    def test_relatorio_ausente_nao_passa(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(OSError):
                evaluate(directory)

    def test_erro_do_scanner_nao_passa(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            sast=json.loads((ROOT/'reports/corrigido/njsscan.json').read_text(encoding='utf-8'))
            sast['errors']=['Falha de análise']
            (folder/'njsscan.json').write_text(json.dumps(sast),encoding='utf-8')
            (folder/'npm-audit.json').write_bytes((ROOT/'reports/corrigido/npm-audit.json').read_bytes())
            with self.assertRaises(ValueError):
                evaluate(folder)

    def test_critical_sca_bloqueia_sem_alertas_sast(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            (folder/'njsscan.json').write_bytes((ROOT/'reports/corrigido/njsscan.json').read_bytes())
            sca=json.loads((ROOT/'reports/corrigido/npm-audit.json').read_text(encoding='utf-8'))
            sca['metadata']['vulnerabilities']['critical']=1
            (folder/'npm-audit.json').write_text(json.dumps(sca),encoding='utf-8')
            self.assertEqual(evaluate(folder)['exit_code'],1)

if __name__=='__main__':
    unittest.main(verbosity=2)
