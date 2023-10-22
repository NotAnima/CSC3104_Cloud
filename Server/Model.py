import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
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

    # Split the data into training and testing sets (80% train, 20% test), stratify to ensure equal proportions of class 0,1,2 diabetes indicator for the test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Initialize the Random Forest Classifier with controlled parameters for faster training
    rf_model = RandomForestClassifier(n_estimators=10, max_depth=10, random_state=42, class_weight='balanced')
    rf_model.fit(X_train, y_train)

    return rf_model

    # y_pred_rf = rf_model.predict(X_test)

    # classification_metrics_rf = classification_report(y_test, y_pred_rf)
    # conf_matrix_rf = confusion_matrix(y_test, y_pred_rf)

    # print("Classification Report:")
    # print(classification_metrics_rf)

    # print("Confusion Matrix:")
    # print(conf_matrix_rf)

def save_model(model):
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

data = read_data('diabetes_012_health_indicators_BRFSS2015.csv')
model = load_model(data)
save_model(model)