from sklearn.metrics import precision_recall_curve
from src.modeling.training import compress_as_binary
import numpy as np

def validation_pr(frame,probability,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    _,y,w=compress_as_binary(frame)
    precision,recall,_=precision_recall_curve(y,np.r_[probability,probability],sample_weight=w)
    fig,ax=plt.subplots(figsize=(8,5))
    ax.step(recall,precision,where='post')
    ax.axhline(np.average(y,weights=w),color='gray',ls='--')
    ax.set(xlabel='Recall — não alfabetizados',ylabel='Precisão',title='Validação — logística de referência',xlim=(0,1),ylim=(0,1))
    fig.tight_layout();output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(output,dpi=160);plt.close(fig)
