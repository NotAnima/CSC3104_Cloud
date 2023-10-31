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
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

def train_base_model_with_csv(data):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data.drop('Diabetes_012', axis=1))

    X = scaled_features
    y = data['Diabetes_012']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(X_train[0])
    print(type(X_train))
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
    return y_pred

weight = [
    [-0.18551107, -0.18695389, -0.13650731, -0.25427159,  0.00655888, -0.00074342,
     -0.02001863,  0.00551356,  0.00950881,  0.01496266,  0.06868512,  0.00186195,
     -0.03734685, -0.2999962,  -0.01257621,  0.03924137, -0.02078656, -0.06429077,
     -0.25543536,  0.03958357,  0.08161512],
    [-0.00405342,  0.0865385,   0.03067712,  0.08823974, -0.0099468,  -0.0254473,
     -0.02836771,  0.00969986,  0.00238824, -0.01438119,  0.03315813, -0.01654704,
      0.06415427,  0.02260267,  0.04842956, -0.01228478, -0.01324827, -0.00168692,
      0.12140731, -0.04593265, -0.05102965],
    [ 0.18956449,  0.10041539,  0.10583018,  0.16603185,  0.00338792,  0.02619073,
      0.04838634, -0.01521342, -0.01189706, -0.00058147, -0.10184325,  0.01468509,
     -0.02680742,  0.27739354, -0.03585335, -0.02695659,  0.03403483,  0.06597769,
      0.13402805,  0.00634908, -0.03058547]
]

bias = [2.1623476, -1.93714368, -0.22520392]

client1_weight = weight
client1_bias = bias

client2_weight = weight
client2_bias = bias

client3_weight = weight
client3_bias = bias

client4_weight = weight
client4_bias = bias

client5_weight = weight
client5_bias = bias

all_client_weights = [client1_weight, client2_weight, client3_weight, client4_weight, client5_weight]
all_client_biases = [client1_bias, client2_bias, client3_bias, client4_bias, client5_bias]

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

# average_weights, average_biases = average_weights_and_biases(all_client_weights, all_client_biases)

def train_base_model(average_weights, average_biases):

    model = LogisticRegression(random_state=42, max_iter=1000)
    model.coef_ = average_weights
    model.intercept_ = average_biases

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

data = read_data("diabetes_15_columns.csv")
model = train_base_model_with_csv(data)
save_model(model)