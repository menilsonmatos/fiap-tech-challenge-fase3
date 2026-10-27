from pathlib import Path
import unittest,json
import joblib
from src.cli import load,ROOT
from src.evaluation.metrics import evaluate

class Reproduction(unittest.TestCase):
    def test_split_and_frozen_validation_metrics(self):
        data=load()
        self.assertEqual(int(data.n.sum()),1610754)
        self.assertEqual(data.id_municipio.nunique(),5450)
        for name in ['treino','validacao','teste']:
            self.assertEqual(data[data.conjunto.eq(name)].sigla_uf.nunique(),25)
        val=data[data.conjunto.eq('validacao')]
        model=joblib.load(ROOT/'models/logistica_referencia.joblib')
        m=evaluate(val,model.predict_proba(val)[:,1])
        self.assertAlmostEqual(m['AP'],0.5404577078097648,places=10)
        self.assertEqual((m['TN'],m['FP'],m['FN'],m['TP']),(167705,22367,98471,32096))

    def test_final_protocol_is_frozen_without_scoring_test(self):
        result=json.loads((ROOT/'reports/avaliacao-final/resultados_teste.json').read_text(encoding='utf-8'))
        self.assertTrue(result['test_closed'])
        self.assertTrue(result['no_post_test_tuning'])
        self.assertTrue(result['model_unchanged'])

if __name__=='__main__':unittest.main()
