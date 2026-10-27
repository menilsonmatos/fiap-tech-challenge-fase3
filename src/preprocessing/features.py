from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

NUMERIC = [
    'log1p_populacao_2022', 'log1p_densidade_hab_km2_2022',
    'log1p_pib_por_habitante_reais_2021', 'participacao_agropecuaria_2021',
    'participacao_industria_2021', 'participacao_servicos_2021',
]
EDUCATION = [
    'media_escolar_alunos_turma_AI_2022', 'media_escolar_alunos_turma_2ano_2022',
    'media_escolar_docentes_superior_AI_2022', 'percentual_escolas_rurais_2022',
]
FORBIDDEN = {'id_municipio', 'id_aluno', 'id_escola', 'proficiencia',
             'taxa_alfabetizacao', 'atingiu_meta', 'gap_meta_pp', 'ranking_vulnerabilidade'}

def make_preprocessor(enriched=False):
    columns = NUMERIC + (EDUCATION if enriched else [])
    assert not set(columns) & FORBIDDEN
    return ColumnTransformer([
        ('num', Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True)),
                          ('scale', StandardScaler())]), columns),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['sigla_uf']),
    ], sparse_threshold=0)

def validate_data(frame):
    required = {'id_municipio', 'sigla_uf', 'conjunto', 'n', 'alfabetizados', 'nao_alfabetizados'}
    if not required <= set(frame):
        raise ValueError('Colunas obrigatórias ausentes')
    if frame.id_municipio.duplicated().any():
        raise ValueError('Município duplicado: risco de multiplicação na junção')
    if not (frame.n == frame.alfabetizados + frame.nao_alfabetizados).all():
        raise ValueError('Contagens das classes não reconciliam')
    if not frame[['n', 'alfabetizados', 'nao_alfabetizados']].ge(0).all().all():
        raise ValueError('Contagem negativa')
    if not frame.conjunto.isin(['treino', 'validacao', 'teste']).all():
        raise ValueError('Conjunto inválido')
