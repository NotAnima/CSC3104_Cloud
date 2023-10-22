from __future__ import print_function

import logging

import grpc
import federated_pb2
import federated_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = federated_pb2_grpc.FederatedStub(channel)
        pass

if __name__ == '__main__':
    logging.basicConfig()
    run()