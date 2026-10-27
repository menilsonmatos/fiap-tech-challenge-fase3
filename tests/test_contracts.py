import unittest
import numpy as np
import pandas as pd
from src.preprocessing.features import validate_data, NUMERIC, EDUCATION, FORBIDDEN
from src.modeling.training import compress_as_binary

def example():
    return pd.DataFrame([dict(id_municipio='0000001', sigla_uf='AA', conjunto='treino',
                              n=10, alfabetizados=7, nao_alfabetizados=3)])

class DataContracts(unittest.TestCase):
    def test_positive_class_is_not_literate(self):
        _, y, w=compress_as_binary(example())
        self.assertEqual(float(w[y==1].sum()),3)
        self.assertEqual(float(w[y==0].sum()),7)

    def test_inconsistent_or_duplicate_context_is_rejected(self):
        bad=example();bad.loc[0,'n']=11
        with self.assertRaises(ValueError):validate_data(bad)
        with self.assertRaises(ValueError):validate_data(pd.concat([example(),example()]))

    def test_no_target_or_identifiers_in_predictors(self):
        self.assertFalse(set(NUMERIC+EDUCATION)&FORBIDDEN)
        self.assertNotIn('alfabetizados',NUMERIC+EDUCATION)

if __name__=='__main__':unittest.main()
