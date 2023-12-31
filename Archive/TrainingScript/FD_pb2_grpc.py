# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import FD_pb2 as FD__pb2


class ModelServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadFile = channel.stream_unary(
                '/ModelService/UploadFile',
                request_serializer=FD__pb2.Chunk.SerializeToString,
                response_deserializer=FD__pb2.UploadFileResponse.FromString,
                )
        self.DiffModel = channel.unary_unary(
                '/ModelService/DiffModel',
                request_serializer=FD__pb2.HashValue.SerializeToString,
                response_deserializer=FD__pb2.HashCompared.FromString,
                )
        self.sendWeight = channel.unary_unary(
                '/ModelService/sendWeight',
                request_serializer=FD__pb2.sentWeights.SerializeToString,
                response_deserializer=FD__pb2.weightResponse.FromString,
                )
        self.getModel = channel.unary_unary(
                '/ModelService/getModel',
                request_serializer=FD__pb2.startValue.SerializeToString,
                response_deserializer=FD__pb2.initialModel.FromString,
                )


class ModelServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UploadFile(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DiffModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sendWeight(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ModelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadFile': grpc.stream_unary_rpc_method_handler(
                    servicer.UploadFile,
                    request_deserializer=FD__pb2.Chunk.FromString,
                    response_serializer=FD__pb2.UploadFileResponse.SerializeToString,
            ),
            'DiffModel': grpc.unary_unary_rpc_method_handler(
                    servicer.DiffModel,
                    request_deserializer=FD__pb2.HashValue.FromString,
                    response_serializer=FD__pb2.HashCompared.SerializeToString,
            ),
            'sendWeight': grpc.unary_unary_rpc_method_handler(
                    servicer.sendWeight,
                    request_deserializer=FD__pb2.sentWeights.FromString,
                    response_serializer=FD__pb2.weightResponse.SerializeToString,
            ),
            'getModel': grpc.unary_unary_rpc_method_handler(
                    servicer.getModel,
                    request_deserializer=FD__pb2.startValue.FromString,
                    response_serializer=FD__pb2.initialModel.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ModelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ModelService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UploadFile(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/ModelService/UploadFile',
            FD__pb2.Chunk.SerializeToString,
            FD__pb2.UploadFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DiffModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ModelService/DiffModel',
            FD__pb2.HashValue.SerializeToString,
            FD__pb2.HashCompared.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sendWeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ModelService/sendWeight',
            FD__pb2.sentWeights.SerializeToString,
            FD__pb2.weightResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ModelService/getModel',
            FD__pb2.startValue.SerializeToString,
            FD__pb2.initialModel.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
