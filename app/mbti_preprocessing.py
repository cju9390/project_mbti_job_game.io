import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

try:
    df = pd.read_csv('16P.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('16P.csv', encoding='cp1252')

mbti_counts = df['Personality'].value_counts()
print("--- MBTI 유형별 데이터 개수 ---")
print(mbti_counts)

print("\n--- 결측치 확인 ---")
print(df['Personality'].isnull().sum())

print("\n--- MBTI 유형별 비율 (%) ---")
print(df['Personality'].value_counts(normalize=True) * 100)

scale_map = {
    -3: -1.0,
    -2: -0.5,
    -1: -0.5,
     0:  0.0,
     1:  0.5,
     2:  0.5,
     3:  1.0
}

question_cols = df.columns[1:-1]
for col in question_cols:
    df[col] = df[col].map(scale_map)

df.to_csv('16P_preprocessed.csv', index=False, encoding='utf-8-sig')
print('전처리 완료: 16P_preprocessed.csv 저장됨')
