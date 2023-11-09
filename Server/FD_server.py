from concurrent import futures
import grpc, FD_pb2, FD_pb2_grpc, datetime, hashlib, diabetes
import numpy as np
# Global variable to hold all the aggregated data
weights = []
bias = []
model = diabetes.load_model("model.pkl")

class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):
    def sendWeight(self, request_iterator, context):
        global weights, bias,model
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
            diabetes.save_model(model, "model.pkl")
            model = diabetes.load_model("model.pkl")

            hashResult = diabetes.calculate_md5("model.pkl")
            print("Hash after training: " + str(hashResult))
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
    
    def getModel(self, request_iterator, context):
        time = getTime()
        print("Sending model: " + time)
        global model
        weight, bias, shape = diabetes.extract_weights_and_biases(model)

        return FD_pb2.initialModel(weights=weight,bias=bias,shape=shape)

def getTime():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def serve():
    print("Starting up server v1.0")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FD_pb2_grpc.add_ModelServiceServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    print("System startup succesfully")

if __name__ == "__main__":
    serve()
