from concurrent import futures
import grpc, FD_pb2, FD_pb2_grpc, datetime

class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):

    def UploadFile(self, request_iterator, context):
        name = createName()
        with open(f"/storage/{name}", "wb") as f:
            for chunk in request_iterator:
                f.write(chunk.content)
        print("File received")
        return FD_pb2.UploadFileResponse(message="File received")

def createName():
    received_file = "received_file"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{received_file}_{timestamp}.tflite"
    return file_name

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FD_pb2_grpc.add_ModelServiceServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
