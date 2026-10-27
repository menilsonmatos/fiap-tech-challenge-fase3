import argparse, json, hashlib
from pathlib import Path
import pandas as pd
import joblib
from src.preprocessing.features import validate_data
from src.modeling.training import fit_model
from src.evaluation.metrics import evaluate

ROOT = Path(__file__).resolve().parents[1]

def load():
    path = ROOT / 'data/processed/dados_analiticos_municipais.json'
    manifest = json.loads((ROOT / 'data/manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256(path.read_bytes()).hexdigest() != manifest['dataset_sha256']:
        raise ValueError('Hash dos dados difere do manifesto')
    frame = pd.DataFrame(json.loads(path.read_text(encoding='utf-8')))
    validate_data(frame)
    return frame

def main():
    parser = argparse.ArgumentParser(description='Reprodução acadêmica da Fase 3')
    parser.add_argument('command', choices=['verify', 'train', 'evaluate', 'cross-validate', 'explain', 'profiles', 'plot-pr', 'show-final'])
    parser.add_argument('--model', choices=['logistica', 'boosting'], default='logistica')
    parser.add_argument('--artifact', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT/'work/modelo_reproduzido.joblib')
    args = parser.parse_args()
    if args.command == 'show-final':
        print((ROOT/'reports/avaliacao-final/resultados_teste.json').read_text(encoding='utf-8'))
        return
    frame = load()
    if args.command == 'verify':
        assert len(frame) == 5450 and frame.n.sum() == 1610754
        print(frame.groupby('conjunto')[['n', 'alfabetizados', 'nao_alfabetizados']].sum().to_string())
        return
    train = frame[frame.conjunto.eq('treino')].copy()
    val = frame[frame.conjunto.eq('validacao')].copy()
    if args.command == 'train':
        if args.output.exists():
            raise FileExistsError('Escolha saída nova; não sobrescrever modelos entregues')
        params = {'n_estimators':160, 'max_depth':3} if args.model=='boosting' else {}
        pipe = fit_model(train, args.model, args.model=='boosting', params)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipe, args.output)
        print(str(args.output.resolve()))
    elif args.command == 'evaluate':
        path = args.artifact or ROOT/'models/logistica_referencia.joblib'
        pipe = joblib.load(path)
        print(json.dumps(evaluate(val, pipe.predict_proba(val)[:,1]), indent=2))
    elif args.command == 'cross-validate':
        from src.modeling.cross_validation import run
        print(json.dumps(run(train), indent=2))
    elif args.command == 'explain':
        from src.evaluation.explain import run
        print(run(frame, ROOT, ROOT/'work/shap_reproduzido.json'))
    elif args.command == 'profiles':
        from src.modeling.profiles import run
        print(json.dumps(run(frame), indent=2))
    elif args.command == 'plot-pr':
        from src.visualization.charts import validation_pr
        pipe=joblib.load(ROOT/'models/logistica_referencia.joblib')
        path=ROOT/'work/validacao_pr.png'
        validation_pr(val,pipe.predict_proba(val)[:,1],path)
        print(str(path))

if __name__ == '__main__':
    main()
