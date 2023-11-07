from concurrent import futures
import grpc, FD_pb2, FD_pb2_grpc, datetime, hashlib, diabetes
import numpy as np
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle
import os

# SQLAlchemy setup
DATABASE_URI = 'postgresql://user:password@postgres-service:5432/mydatabase'  # Replace with your actual database URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

weights = []
bias = []

# Define a Model class to store model data
class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    referencepickle = Column(Text, nullable=False)  # Store the path to the pickle file

    def __init__(self, referencepickle):
        self.timestamp = datetime.now()
        self.referencepickle = referencepickle

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)

class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):
    def sendWeight(self, request_iterator, context):
        global weights, bias
        session = Session()
        proper_weight = np.array(request_iterator.weights).reshape(request_iterator.shape)
        # Add to track
        weights.append(proper_weight)
        bias.append(request_iterator.bias)
        if(len(weights) > 3):
            new_weights, new_bias = diabetes.average_weights_and_biases(proper_weight, request_iterator.bias)
            model = diabetes.train_average_model(new_weights, new_bias)
            data = pickle.dump(model)

            # Show hash
            model_hash = diabetes.calculate_md5("model.pkl")
            print("Current hash: " + model_hash)
            weights = []
            bias = []

            # Save the model to the database
            db_model = Model(timestamp=datetime.datetime.now(), referencepickle=data)
            session.add(db_model)
            session.commit()
        else:
            # If not just return the existing model
            print("Not enough data, returning existing model")

        # Extract out the weights for usage
        new_weights, new_bias, shape = diabetes.extract_weights_and_biases(model)

        return FD_pb2.weightResponse(weights=new_weights, bias=new_bias, shape=shape)
    
    def getModel(self, request, context):
        session = Session()
        # Retrieve the latest model from the database
        db_model = session.query(Model).order_by(Model.id.desc()).first()
        if db_model:
            # Load the model from the pickle reference
            with open(db_model.referencepickle, 'rb') as f:
                model = pickle.load(f)
            weight, bias, shape = diabetes.extract_weights_and_biases(model)
        else:
            # If no model in the database, use a default one
            model = diabetes.load_model("model.pkl")
            weight, bias, shape = diabetes.extract_weights_and_biases(model)

        return FD_pb2.initialModel(weights=weight, bias=bias, shape=shape)

def serve():
    print("Starting up server v0.5")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FD_pb2_grpc.add_ModelServiceServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    print("System startup successfully")

if __name__ == "__main__":
    serve()
