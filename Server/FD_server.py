from concurrent import futures
import grpc, FD_pb2, FD_pb2_grpc, datetime, diabetes, pickle
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import environ
from datetime import datetime
# Global variable to hold all the aggregated data
weights = []
bias = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']

db = SQLAlchemy(app)

def initDB():
    # Initialise the first model into the DB
    with open("model.pkl", "rb") as f:
        pickleBin = f.read()
        pickleObject = globalmodel(pickleBin)
        db.session.add(pickleObject)
        db.session.commit()

class globalmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.Text, nullable=False)
    picklefile = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, picklefile):
        self.timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.picklefile = picklefile


class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):
    # Send either same or aggregated model
    def sendWeight(self, request_iterator, context):
        global weights, bias
        globalQuery = globalmodel.query.filter_by().all()
        globalQuery = globalQuery[-1] # get the latest entry
        referencePickle = globalQuery.picklefile
        model = pickle.loads(referencePickle)

        proper_weight = np.array(request_iterator.weights).reshape(request_iterator.shape)
        weights.append(proper_weight)
        bias.append(request_iterator.bias)

        # Verbose for logging
        time = getTime()
        print("Received weights: " + time)
        print(proper_weight)
        print("\n")
        print("Received Bias")
        print(request_iterator.bias)

        # If received more than 3 training data, aggregate it
        if(len(weights) > 3):
            print("Aggregating new model..." + time)
            hashResult = diabetes.calculate_md5("model.pkl")

            # Train the model
            print("Hash before training: " + str(hashResult))
            new_weights, new_bias = diabetes.average_weights_and_biases(weights,bias)
            model = diabetes.train_average_model(new_weights, new_bias)

            # Reload model
            pickleObject = globalmodel(model)
            db.session.add(pickleObject)
            db.session.commit()

            # Clear out models
            weights = []
            bias = []

            # Show new weights and bias
            print("New weights: " + time)
            print(new_weights)
            print("\n")
            print("New Bias")
            print(new_bias)
        else:
            # If not just return the existing model
            print("Not enough data, returning existing model: " + time)
            
        # Extract out the weights for usage
        new_weights, new_bias, shape = diabetes.extract_weights_and_biases(model)

        return FD_pb2.weightResponse(weights=new_weights,bias=new_bias,shape=shape)
    
    # Get model for first time initialisation of the client
    def getModel(self, request_iterator, context):
        time = getTime()
        print("Sending model: " + time)
        globalQuery = globalmodel.query.filter_by().all()
        globalQuery = globalQuery[-1] # get the latest entry
        referencePickle = globalQuery.picklefile
        model = pickle.loads(referencePickle)
        weight, bias, shape = diabetes.extract_weights_and_biases(model)

        return FD_pb2.initialModel(weights=weight,bias=bias,shape=shape)

def getTime():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def serve():
    print("Starting up server v0.4")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FD_pb2_grpc.add_ModelServiceServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    print("System startup succesfully")

if __name__ == "__main__":
    serve()
