from concurrent import futures
import grpc
import FD_pb2
import FD_pb2_grpc

class FileTransferServicer(FD_pb2_grpc.ModelServiceServicer):

    def UploadFile(self, request_iterator, context):
        with open("received_file", "wb") as f:
            for chunk in request_iterator:
                f.write(chunk.content)
        return FD_pb2.UploadFileResponse(message="File received")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FD_pb2_grpc.add_ModelServiceServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
