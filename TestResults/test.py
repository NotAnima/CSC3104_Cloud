import diabetes, random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from os import environ

def read_data(path):
    file_path = path
    data = pd.read_csv(file_path)

    return data

if (environ['MODEL'] != None):
    modelFile = environ['MODEL']
    fileLocation = "/model/" + modelFile
else:
    fileLocation = "model.pkl"


data = read_data("diabetes_15_columns.csv")
model = diabetes.load_model(fileLocation)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(data.drop('Diabetes_012', axis=1))

X = scaled_features
y = data['Diabetes_012']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# answer = model.predict(X_test)
diabetes.test_model(model, X_test, y_test)


