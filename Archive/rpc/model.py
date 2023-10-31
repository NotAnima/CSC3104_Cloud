import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle

data = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv')

data_class_0 = data[data['Diabetes_012'] == 0].sample(n=30000, random_state=42)
# data_class_1 = data[data['Diabetes_012'] == 1]
data_class_2 = data[data['Diabetes_012'] == 2]

# Combine the balanced data
new_data = pd.concat([data_class_0, data_class_2])

# Shuffle the dataset to ensure it's properly mixed
new_data = new_data.sample(frac=1, random_state=42).reset_index(drop=True)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(new_data.drop('Diabetes_012', axis=1))

X = scaled_features
y = new_data['Diabetes_012']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)

rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train, y_train)

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