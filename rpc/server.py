from concurrent import futures
import logging

import grpc
import federated_pb2
import federated_pb2_grpc

class Federated(federated_pb2_grpc.FederatedServicer):
    pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    federated_pb2_grpc.add_FederatedServicer_to_server(Federated(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()