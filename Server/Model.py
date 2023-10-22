import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

def read_data(path):
    file_path = path
    data = pd.read_csv(file_path)

    return data

def load_model(data):
    # Standardize the features (mean=0 and variance=1), which is a requirement for many ML models
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data.drop('Diabetes_012', axis=1))  # exclude target variable

    # Define features and target
    X = scaled_features
    y = data['Diabetes_012']

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Logistic Regression model
    logistic_model = LogisticRegression(random_state=42, max_iter=10000)  # to ensure convergence
    logistic_model.fit(X_train, y_train)

    return logistic_model

    # y_pred = logistic_model.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # print(f"Accuracy: {accuracy}\n")
    # class_report = classification_report(y_test, y_pred, zero_division=1)
    # print(f"Classification Report:\n{class_report}\n")

def save_model(model):
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

data = read_data('diabetes_012_health_indicators_BRFSS2015.csv')
model = load_model(data)
save_model(model)