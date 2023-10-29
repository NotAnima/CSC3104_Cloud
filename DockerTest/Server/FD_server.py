from concurrent import futures
import grpc, FD_pb2, FD_pb2_grpc, datetime, hashlib, diabetes

# Global variable to hold all the aggregated data
weights = {}
bias = {}

class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):

    def UploadFile(self, request_iterator, context):
        name = createName()
        with open(f"/storage/{name}", "wb") as f:
            for chunk in request_iterator:
                f.write(chunk.content)
        print("File received")
        return FD_pb2.UploadFileResponse(message="File received")
    
    def DiffModel(self, request_iterator, context):
        localHash = calculate_md5("Dockerfile")
        if (request_iterator.clientHash != localHash):
            HashResult = True
        else:
            HashResult = False
        return FD_pb2.HashCompared(HashResult=HashResult)
    
    def sendWeight(self, request_iterator, context):
        global weights, bias
        # diabetes.average_weights_and_biases()
        print(request_iterator.clientID)
        if(request_iterator.clientID not in weights):
            weights[request_iterator.clientID] = request_iterator.weights
            bias[request_iterator.clientID] = request_iterator.bias
        message = "Weights received"

        # If there are x number of received items, start to aggregate

        return FD_pb2.weightResponse(message=message)

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
