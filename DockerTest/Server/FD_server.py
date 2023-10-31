from concurrent import futures
import grpc, FD_pb2, FD_pb2_grpc, datetime, hashlib, diabetes, threading,time
import numpy as np
# Global variable to hold all the aggregated data
weights = []
bias = []
model = diabetes.load_model("model.pkl")

class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):

    def UploadFile(self, request_iterator, context):
        name = createName()
        with open(f"/storage/{name}", "wb") as f:
            for chunk in request_iterator:
                f.write(chunk.content)
        print("File received")
        return FD_pb2.UploadFileResponse(message="File received")
    
    def DiffModel(self, request_iterator, context):
        localHash = calculate_md5("model.pkl")
        if (request_iterator.clientHash != localHash):
            HashDiff = True
        else:
            HashDiff = False
        return FD_pb2.HashCompared(HashResult=HashDiff)
    
    def sendWeight(self, request_iterator, context):
        global weights, bias,model
        shape = 0
        proper_weight = np.array(request_iterator.weights).reshape(shape)
        weights.append(proper_weight)
        bias.append(request_iterator.bias)

        if(len(weights) > 3):
            new_weights, new_bias = diabetes.average_weights_and_biases(weights,bias)
            model = diabetes.train_average_model(new_weights, new_bias)
            weights = []
            bias = []
        else:
            new_weights, new_bias, shape = diabetes.extract_weights_and_biases(model)


        return FD_pb2.weightResponse(weights=new_weights,bias=new_bias,shape=shape)
    
    def getModel(self, request_iterator, context):
        global model
        weight, bias, shape = diabetes.extract_weights_and_biases(model)

        return FD_pb2.initialModel(weights=weight,bias=bias,shape=shape)

def createName():
    received_file = "received_file"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{received_file}_{timestamp}.tflite"
    return file_name

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FD_pb2_grpc.add_ModelServiceServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
