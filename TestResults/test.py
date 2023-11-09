import diabetes, random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

def read_data(path):
    file_path = path
    data = pd.read_csv(file_path)

    return data

def createPerson(personNum):
    practicePatient = {}
    attributes = ["HighBP", "HighChol","CholCheck", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "DiffWalk", "Sex"]
    practicePatient["BMI"] = float(random.randint(12, 98))
    practicePatient["PhysHlth"] = float(random.randint(0, 30))
    practicePatient["Age"] = float(random.randint(1, 13))
    # To ensure there's at least 1 of each type for the model to train
    practicePatient["Diabetes"] = float(personNum % 2)

    for attribute in attributes:
        practicePatient[attribute] = float(random.randint(0,1))
    
    # print(practicePatient)
    return practicePatient

data = read_data("diabetes_15_columns.csv")
model = diabetes.load_model("referenceModel.pkl")

scaler = StandardScaler()
scaled_features = scaler.fit_transform(data.drop('Diabetes_012', axis=1))

X = scaled_features
y = data['Diabetes_012']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# answer = model.predict(X_test)
diabetes.test_model(model, X_test, y_test)


