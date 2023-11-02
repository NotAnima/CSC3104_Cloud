from __future__ import print_function

import logging, schedule, time, datetime, random, grpc, FD_pb2, FD_pb2_grpc, diabetes
import pandas as pd
channel = grpc.insecure_channel("localhost:50051")
stub = FD_pb2_grpc.ModelServiceStub(channel)

def scheduled_task():
    global model, weights, bias
    try:
        # Load training model
        print("Training model chosen")
        trainModel = diabetes.load_model("trainingModel.pkl")
    except:
        print("Reference model chosen")
        # If no training model ready yet, use reference model
        trainModel = diabetes.load_model("referenceModel.pkl")

    # Extract weights, bias, shape
    weights, bias, shape = diabetes.extract_weights_and_biases(trainModel)
    sent_weights = FD_pb2.sentWeights(weights=weights,bias=bias,shape=shape)
    response = stub.sendWeight(sent_weights)

    # Reconstruct the latest received model
    model = diabetes.train_base_model(response.weights, response.bias, response.shape)
    # Update the local model and reload
    diabetes.save_model(model, "referenceModel.pkl")
    model = diabetes.load_model("referenceModel.pkl")

    #Calculate hash to see the difference
    time = getTime()
    hashResult = diabetes.calculate_md5("referenceModel.pkl")
    print("Current hash: " + str(hashResult) + " calculated at " + time)

    # Your background task logic goes here
    print("Model sent for training!")
    

def getModel():
    result = FD_pb2.startValue(number=1)
    response = stub.getModel(result)

    # Reconstruct the weights into a model
    model = diabetes.train_base_model(response.weights, response.bias, response.shape)
    # Save the model locally
    diabetes.save_model(model, "referenceModel.pkl")
    print("Initial model setup complete")
    return model

# Initialise first model from server
model = getModel()

def run():
    global model
    # List used for store all the simulated patients
    trainingPatient = []
    for i in range(0,100):
        person = createPerson(i)
        trainingPatient.append(person)
    trainingData = pd.DataFrame(trainingPatient)
    model = diabetes.train_existing_model(model, trainingData)
    diabetes.save_model(model, "trainingModel.pkl")

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

# Schedule the task to run every 5 minutes
schedule.every(7).seconds.do(run)
schedule.every(30).seconds.do(scheduled_task)

def getTime():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

if __name__ == "__main__":
    # # Create a thread for the background task
    # task_thread = threading.Thread(target=run_scheduled_task)
    # task_thread.daemon = True  # Set as daemon to allow clean exit

    # # Start the background task thread
    # task_thread.start()

    while True:
        schedule.run_pending()  # Check and run scheduled tasks
        time.sleep(1) 
