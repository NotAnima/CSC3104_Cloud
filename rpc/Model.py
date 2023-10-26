import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier with controlled parameters for faster training
    log_reg_model = LogisticRegression(random_state=42, max_iter=1000)
    log_reg_model.fit(X_train, y_train)

    return log_reg_model

    # # Make predictions on the test set
    # y_pred = log_reg_model.predict(X_test)

    # # Calculate the model performance
    # accuracy = accuracy_score(y_test, y_pred)  # for classification
    # classification_rep = classification_report(y_test, y_pred)
    # conf_matrix = confusion_matrix(y_test, y_pred)

    # print("Accuracy")
    # print(accuracy)

    # print("Classification Report:")
    # print(classification_rep)

    # print("Confusion Matrix:")
    # print(conf_matrix)

def save_model(model):
    with open("rpc/model.pkl", "wb") as file:
        pickle.dump(model, file)

def get_model():
    data = read_data('diabetes_012_health_indicators_BRFSS2015.csv')
    model = load_model(data)
    save_model(model)

get_model()