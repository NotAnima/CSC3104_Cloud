import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle

def read_data(path):
    file_path = path
    data = pd.read_csv(file_path)

    return data

def save_model(model):
    with open("rpc/updated_model.pkl", "wb") as file:
        pickle.dump(model, file)

def load_model(file_path):
    with open(file_path, "rb") as file:
        model = pickle.load(file)
    return model

def train_existing_model(model, data):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data.drop('Diabetes_012', axis=1))

    X = scaled_features
    y = data['Diabetes_012']

    model.fit(X, y)

    return model

def extract_weights_and_biases(model):
    weights = model.coef_
    biases = model.intercept_
    return weights, biases
