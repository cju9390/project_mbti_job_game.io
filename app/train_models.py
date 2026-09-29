import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv('16P_preprocessed.csv', encoding='utf-8-sig')
q_cols = df.columns[1:61].tolist()

TRAIT_INDICES = {
    'EI': [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56],
    'NS': [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57],
    'TF': [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58],
    'JP': [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59],
}

labels = {
    'EI': df['Personality'].str[0].map({'E': 1, 'I': 0}).values,
    'NS': df['Personality'].str[1].map({'N': 1, 'S': 0}).values,
    'TF': df['Personality'].str[2].map({'T': 1, 'F': 0}).values,
    'JP': df['Personality'].str[3].map({'J': 1, 'P': 0}).values,
}

models = {}
for trait, indices in TRAIT_INDICES.items():
    feat_idx = [i - 1 for i in indices]
    X = df[q_cols].values[:, feat_idx]
    y = labels[trait]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    xgb = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1,
                        eval_metric='logloss', random_state=42)
    xgb.fit(X_train, y_train)
    acc = accuracy_score(y_test, xgb.predict(X_test))
    print(f'{trait} 정확도: {acc:.1%}')

    models[trait] = {
        'model': xgb,
        'feature_indices': feat_idx,
    }

with open('models.pkl', 'wb') as f:
    pickle.dump(models, f)

print('모델 저장 완료: models.pkl')
