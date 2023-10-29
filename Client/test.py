import diabetes
import pandas as pd

answeredList = []
model = diabetes.load_model("model.pkl")
print(diabetes.calculate_md5("model.pkl"))
practicePatient1 = {'Diabetes': 0.0, 'HighBP': 1.0, 'HighChol': 1.0, 'CholCheck': 1.0, 'BMI': 21.0, 'Smoker': 1.0, 'Stroke': 1.0, 'HeartDiseaseorAttack': 1.0, 'PhysActivity': 1.0, 'Fruits': 1.0, 'Veggies': 1.0, 'HvyAlcoholConsump': 1.0, 'PhysHlth': 1.0, 'DiffWalk': 1.0, 'Sex': 1.0, 'Age': 5.0}
practicePatient2 = {'Diabetes': 1.0, 'HighBP': 1.0, 'HighChol': 1.0, 'CholCheck': 1.0, 'BMI': 21.0, 'Smoker': 1.0, 'Stroke': 1.0, 'HeartDiseaseorAttack': 1.0, 'PhysActivity': 1.0, 'Fruits': 1.0, 'Veggies': 1.0, 'HvyAlcoholConsump': 1.0, 'PhysHlth': 1.0, 'DiffWalk': 1.0, 'Sex': 1.0, 'Age': 5.0}
practicePatient3 = {'Diabetes': 2.0, 'HighBP': 1.0, 'HighChol': 1.0, 'CholCheck': 1.0, 'BMI': 21.0, 'Smoker': 1.0, 'Stroke': 1.0, 'HeartDiseaseorAttack': 1.0, 'PhysActivity': 1.0, 'Fruits': 1.0, 'Veggies': 1.0, 'HvyAlcoholConsump': 1.0, 'PhysHlth': 1.0, 'DiffWalk': 1.0, 'Sex': 1.0, 'Age': 5.0}
answeredList.append(practicePatient1)
answeredList.append(practicePatient2)
answeredList.append(practicePatient3)
trainingData = pd.DataFrame(answeredList)
# # Send data for training
model = diabetes.train_existing_model(model, trainingData)
diabetes.save_model(model)
# Reload model
model = diabetes.load_model("model.pkl")
# REMOVE EVERYTHING ABOVE
print(diabetes.calculate_md5("model.pkl"))
