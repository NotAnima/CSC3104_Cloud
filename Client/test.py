# Just checking what are the weights and bias for the current model
import diabetes, grpc, FD_pb2, FD_pb2_grpc

model = diabetes.load_model("model.pkl")
weight, bias, shape = diabetes.extract_weights_and_biases(model)

print(weight)
print(bias)

# channel = grpc.insecure_channel("localhost:50051")
# stub = FD_pb2_grpc.ModelServiceStub(channel)
# result = FD_pb2.startValue(number=1)
# response = stub.getModel(result)

# # print(response.weights)
# # print(response.bias)

# # Reconstruct the weights into a model
# model = diabetes.train_base_model(response.weights, response.bias, response.shape)

# def inspect_object_attributes(obj):
#     for attr_name in dir(obj):
#         # Filter out built-in attributes
#         if not attr_name.startswith("__"):
#             attr_value = getattr(obj, attr_name)
#             print(f"Attribute Name: {attr_name}, Type: {type(attr_value)}")

# Assuming your LogisticRegression object is named 'model'
# inspect_object_attributes(model)

# Save the model locally
# diabetes.save_model(model)