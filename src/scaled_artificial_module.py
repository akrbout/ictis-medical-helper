import pandas as pd
import os
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier


def scaled_artificial_module(client_simptoms: str) -> str:
    # Загрузка данных
    df = pd.read_csv("datasets/dataset.csv")

    # Загрузка весов
    weights = pd.read_csv('datasets/Symptom-severity.csv').set_index('Symptom')['weight'].to_dict()

    # Преобразование данных о симптомах в список
    symptoms = df.iloc[:, 1:].values.tolist()

    # Замена пропущенных значений на пустые строки
    for row in symptoms:
        for i in range(len(row)):
            if isinstance(row[i], float):
                row[i] = ""

    # Переводим симптомы в множества для каждой строки
    symptoms = [set(filter(None, symptom)) for symptom in symptoms]

    # Создаем объект MultiLabelBinarizer для кодирования симптомов
    mlb = MultiLabelBinarizer()
    symptoms_encoded = mlb.fit_transform(symptoms)

    # Умножаем закодированные симптомы на их веса
    for i in range(symptoms_encoded.shape[1]):
        symptom = mlb.classes_[i]
        if symptom in weights:
            symptoms_encoded[:, i] *= weights[symptom]

    # Сопоставляем симптомы с болезнями
    X = symptoms_encoded
    y = df['Disease']

    # Создание и обучение модели
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Получение симптомов от пользователя
    input_symptoms = client_simptoms.split(', ')
    input_symptoms_encoded = mlb.transform([input_symptoms])

    # Умножаем закодированные симптомы на их веса
    for i in range(input_symptoms_encoded.shape[1]):
        symptom = mlb.classes_[i]
        if symptom in weights:
            input_symptoms_encoded[:, i] *= weights[symptom]

    # Предсказание болезни
    prediction = model.predict(input_symptoms_encoded)

    # Выбираем наилучшее предсказание
    return prediction[0]
