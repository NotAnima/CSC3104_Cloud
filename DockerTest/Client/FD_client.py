from __future__ import print_function

import logging

import grpc, hashlib, json
import FD_pb2
import FD_pb2_grpc, diabetes

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = FD_pb2_grpc.ModelServiceStub(channel)
    trainingFile = calculate_md5("test.tflite")
    response = stub.DiffModel(FD_pb2.HashValue(clientHash=trainingFile))
    print("The hash between client and server is " + str(response.HashResult))

    weight = [
        [-0.18551107, -0.18695389, -0.13650731, -0.25427159,  0.00655888, -0.00074342,
        -0.02001863,  0.00551356,  0.00950881,  0.01496266,  0.06868512,  0.00186195,
        -0.03734685, -0.2999962,  -0.01257621,  0.03924137, -0.02078656, -0.06429077,
        -0.25543536,  0.03958357,  0.08161512],
        [-0.00405342,  0.0865385,   0.03067712,  0.08823974, -0.0099468,  -0.0254473,
        -0.02836771,  0.00969986,  0.00238824, -0.01438119,  0.03315813, -0.01654704,
        0.06415427,  0.02260267,  0.04842956, -0.01228478, -0.01324827, -0.00168692,
        0.12140731, -0.04593265, -0.05102965],
        [ 0.18956449,  0.10041539,  0.10583018,  0.16603185,  0.00338792,  0.02619073,
        0.04838634, -0.01521342, -0.01189706, -0.00058147, -0.10184325,  0.01468509,
        -0.02680742,  0.27739354, -0.03585335, -0.02695659,  0.03403483,  0.06597769,
        0.13402805,  0.00634908, -0.03058547]
    ]

    bias = [2.1623476, -1.93714368, -0.22520392]
    sent_weights = FD_pb2.sentWeights()
    for w in weight:
        sent_weights.weights.extend(w)
    sent_weights.bias.extend(bias)
    response = stub.sendWeight(sent_weights)

    model = diabetes.train_base_model(response.weights, response.bias, response.shape)

    # with open("test.tflite", "rb") as f:
    #     chunk_size = 1024 * 1024  # 1MB
    #     response = stub.UploadFile(generate_chunks(f, chunk_size))
    #     print(response.message)

def generate_chunks(file, chunk_size):
    while True:
        chunk = file.read(chunk_size)
        if len(chunk) == 0:
            return
        yield FD_pb2.Chunk(content=chunk)

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


if __name__ == "__main__":
    run()
