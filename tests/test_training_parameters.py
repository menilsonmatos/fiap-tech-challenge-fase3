import unittest
import numpy as np
import pandas as pd
from src.modeling.training import fit_model
from src.preprocessing.features import NUMERIC, make_preprocessor


def example():
    n = 24
    x = np.linspace(-2, 2, n)
    frame = pd.DataFrame({name: x + i * .1 for i, name in enumerate(NUMERIC)})
    frame['id_municipio'] = [f'{i:07d}' for i in range(n)]
    frame['sigla_uf'] = np.where(np.arange(n) % 2, 'AA', 'BB')
    frame['conjunto'] = 'treino'
    frame['n'] = 10
    frame['nao_alfabetizados'] = np.round(1 + 8 / (1 + np.exp(-x))).astype(int)
    frame['alfabetizados'] = 10 - frame.nao_alfabetizados
    return frame


class TrainingParameters(unittest.TestCase):
    def test_regularization_override_fits_and_changes_coefficients(self):
        frame = example()
        params = {'C': .01, 'max_iter': 3000, 'tol': 1e-8}
        original = dict(params)
        strong = fit_model(frame, params=params)
        weak = fit_model(frame, params={'C': 10, 'max_iter': 3000, 'tol': 1e-8})
        self.assertEqual(params, original)
        self.assertEqual(strong.named_steps['model'].C, .01)
        self.assertLess(np.linalg.norm(strong.named_steps['model'].coef_),
                        np.linalg.norm(weak.named_steps['model'].coef_))
        self.assertFalse(np.allclose(strong.predict_proba(frame), weak.predict_proba(frame)))

    def test_overrides_work_for_other_families(self):
        for family, params in [('random_forest', {'n_estimators': 5, 'n_jobs': 1}),
                               ('boosting', {'n_estimators': 5, 'learning_rate': .1})]:
            with self.subTest(family=family):
                pipe = fit_model(example(), family=family, params=params)
                self.assertEqual(pipe.named_steps['model'].n_estimators, 5)
                self.assertTrue(np.isfinite(pipe.predict_proba(example())).all())

    def test_custom_features_reject_target_and_do_not_fit_holdout(self):
        with self.assertRaises(ValueError):
            make_preprocessor(numeric_features=NUMERIC + ['nao_alfabetizados'])
        frame = example()
        frame['conjunto'] = 'validacao'
        with self.assertRaises(ValueError):
            fit_model(frame, params={'C': .1})


if __name__ == '__main__':
    unittest.main()
