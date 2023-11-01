from __future__ import print_function

import logging, schedule, time, datetime, threading, random, grpc, FD_pb2, FD_pb2_grpc, diabetes
import pandas as pd
channel = grpc.insecure_channel("dereknan.click:50051")
stub = FD_pb2_grpc.ModelServiceStub(channel)

def scheduled_task():
    global model, weights, bias
    try:
        # Load training model
        trainModel = diabetes.load_model("trainingModel.pkl")
    except:
        # If no training model ready yet, use reference model
        trainModel = diabetes.load_model("referenceModel.pkl")

    # Extract weights, bias, shape
    weights, bias, shape = diabetes.extract_weights_and_biases(trainModel)
    sent_weights = FD_pb2.sentWeights(weights=weights,bias=bias,shape=shape)
    response = stub.sendWeight(sent_weights)

    # Reconstruct the latest received model
    model = diabetes.train_base_model(response.weights, response.bias, response.shape)

    # Update the local model
    diabetes.save_model(model, "referenceModel.pkl")
    # Your background task logic goes here
    print("Scheduled task executed!")

def run():
    # List used for store all the simulated patients
    trainingPatient = []
    for i in range(0,5):
        person = createPerson()
        trainingPatient.append(person)
    trainingData = pd.DataFrame(trainingPatient)
    model = diabetes.train_existing_model(model, trainingData)
    diabetes.save_model(model, "trainingModel.pkl")
    

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

def createPerson():
    practicePatient = {}
    attributes = ["Diabetes","HighBP", "HighChol","CholCheck", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "DiffWalk", "Sex"]
    practicePatient["BMI"] = random.uniform(12, 98)
    practicePatient["PhysHlth"] = random.uniform(0, 30)
    practicePatient["Age"] = random.uniform(1, 13)

    for attribute in attributes:
        practicePatient[attribute] = random.uniform(0,1)
    
    return practicePatient

# Schedule the task to run every 5 minutes
schedule.every(10).seconds.do(run)
schedule.every(30).seconds.do(scheduled_task)

# Create a threaded schedule task
def run_scheduled_task():
    while True:
        schedule.run_pending()  # Check and run scheduled tasks
        time.sleep(1) 

if __name__ == "__main__":
    # Create a thread for the background task
    task_thread = threading.Thread(target=run_scheduled_task)
    task_thread.daemon = True  # Set as daemon to allow clean exit

    # Start the background task thread
    task_thread.start()

    run()
