from sklearn.metrics import precision_score, recall_score, precision_recall_curve, auc, recall_score, f1_score, roc_auc_score, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression



recall_logreg_prepro15 = recall_score(y_test, y_pred)
print(recall_logreg_prepro15)
