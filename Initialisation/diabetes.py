import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle, hashlib
from joblib import dump, load

def read_data(path):
    file_path = path
    data = pd.read_csv(file_path)

    return data

def save_model(model, name):
    with open(name, "wb") as file:
        pickle.dump(model, file)

def train_base_model_with_csv(data):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data.drop('Diabetes_012', axis=1))

    X = scaled_features
    y = data['Diabetes_012']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)

    return model

def test_model(model, X_test, y_test):

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print("Accuracy")
    print(accuracy)

    print("Classification Report:")
    print(classification_rep)

    print("Confusion Matrix:")
    print(conf_matrix)

# Simulating average for weights and biases across 5 clients

def make_prediction(model, X_test):
    y_pred = model.predict(X_test)
    prediction = int(y_pred[0])
    # the prediction keeps coming back as 0 though...
    if (prediction == 0):
        answer = "do not have Diabetes"
    elif (prediction == 1):
        answer = "have Pre-Diabetes"
    elif (prediction == 2):
        answer = "have Diabetes"
    return answer

def extract_weights_and_biases(model):
    weights = model.coef_
    biases = model.intercept_
    flattened_weights = weights.flatten().tolist()
    shape = list(weights.shape)

    return flattened_weights, biases, shape

def train_existing_model(model, data):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data.drop('Diabetes', axis=1))

    X = scaled_features
    y = data['Diabetes']

    model.fit(X, y)

    return model

def average_weights_and_biases(all_client_weights, all_client_biases):
    """
    This function takes in the weights and biases from all clients and computes the average.
    The input should be lists of numpy arrays, where each numpy array corresponds to a client's data.

    :param all_client_weights: List of numpy arrays, where each array contains the weights from one client.
    :param all_client_biases: List of numpy arrays, where each array contains the biases from one client.
    :return: A tuple of numpy arrays representing the averaged weights and biases.
    """

    # We stack the arrays for easier averaging
    stacked_weights = np.stack(all_client_weights)
    stacked_biases = np.stack(all_client_biases)

    # Compute the average along the first dimension of the stack (i.e., across clients)
    average_weights = np.mean(stacked_weights, axis=0)
    average_biases = np.mean(stacked_biases, axis=0)

    return average_weights, average_biases

def train_average_model(average_weights, average_biases):
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.classes_ = np.array([0,2])
    model.coef_ = average_weights
    model.intercept_ = average_biases
    return model

def train_base_model(average_weights, average_biases, shape):
    weights = np.array(average_weights).reshape(shape)
    bias = np.array(average_biases)
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.classes_ = np.array([0,2])
    model.coef_ = weights
    model.intercept_ = bias
    return model

def load_model(file_path):
    with open(file_path, "rb") as file:
        model = pickle.load(file)
    return model

def reshape_data(data):
    data = np.array(data)
    data_reshaped = data.reshape(1, -1)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data_reshaped)
    return scaled_features

# Check if the model is different
def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()
