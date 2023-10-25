from concurrent import futures
import logging
import os

import grpc
import federated_pb2
import federated_pb2_grpc

import Model

class Federated(federated_pb2_grpc.FederatedServicer):
    def SendModel(self, request, context):
        file_name = 'rpc/model.pkl'
        if check_file_exists(file_name):
            with open(file_name, "rb") as file:
                model_data = file.read()
        else:
            Model.get_model()
            with open(file_name, "rb") as file:
                model_data = file.read()

        return federated_pb2.ModelReply(data=model_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    federated_pb2_grpc.add_FederatedServicer_to_server(Federated(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def check_file_exists(filename):
    return os.path.isfile(filename)

if __name__ == '__main__':
    logging.basicConfig()
    serve()