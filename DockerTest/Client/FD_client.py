from __future__ import print_function

import logging

import grpc
import FD_pb2
import FD_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = FD_pb2_grpc.ModelServiceStub(channel)

    with open("test.tflite", "rb") as f:
        chunk_size = 1024 * 1024  # 1MB
        response = stub.UploadFile(generate_chunks(f, chunk_size))
        print(response.message)

def generate_chunks(file, chunk_size):
    while True:
        chunk = file.read(chunk_size)
        if len(chunk) == 0:
            return
        yield FD_pb2.Chunk(content=chunk)

if __name__ == "__main__":
    run()
