from pathlib import Path
import json
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from src.preprocessing.features import NUMERIC, EDUCATION

def run(frame):
    train=frame[frame.conjunto.eq('treino')]
    features=NUMERIC+EDUCATION
    pre=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())])
    x=pre.fit_transform(train[features]);results=[]
    for k in [3,4,5]:
        model=KMeans(n_clusters=k,n_init=20,random_state=42).fit(x)
        results.append({'k':k,'silhouette':float(silhouette_score(x,model.labels_,sample_size=2000,random_state=42)),
                        'counts':np.bincount(model.labels_).tolist()})
    return {'candidates':results,'selected_k':max(results,key=lambda r:r['silhouette'])['k'],
            'pca_explained_variance_ratio':PCA(2).fit(x).explained_variance_ratio_.tolist(),
            'target_used':False,'test_used':False}
