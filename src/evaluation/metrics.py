import numpy as np
from sklearn.metrics import (average_precision_score, roc_auc_score, precision_score,
    recall_score, f1_score, brier_score_loss, confusion_matrix)
from src.modeling.training import compress_as_binary

def evaluate(frame, probability, threshold=.5):
    _, y, w = compress_as_binary(frame)
    p = np.r_[probability, probability]
    pred = p >= threshold
    cm = confusion_matrix(y, pred, labels=[0, 1], sample_weight=w).astype(int)
    assert cm.sum() == frame.n.sum()
    return {
        'students': int(w.sum()), 'AP': float(average_precision_score(y, p, sample_weight=w)),
        'ROC_AUC': float(roc_auc_score(y, p, sample_weight=w)),
        'precision': float(precision_score(y, pred, sample_weight=w, zero_division=0)),
        'recall': float(recall_score(y, pred, sample_weight=w, zero_division=0)),
        'F1': float(f1_score(y, pred, sample_weight=w, zero_division=0)),
        'Brier': float(brier_score_loss(y, p, sample_weight=w)),
        'TN': int(cm[0, 0]), 'FP': int(cm[0, 1]), 'FN': int(cm[1, 0]), 'TP': int(cm[1, 1]),
    }
