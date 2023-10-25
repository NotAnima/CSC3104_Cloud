# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import federated_pb2 as federated__pb2


class FederatedStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendModel = channel.unary_unary(
                '/rpc.Federated/SendModel',
                request_serializer=federated__pb2.ModelRequest.SerializeToString,
                response_deserializer=federated__pb2.ModelReply.FromString,
                )


class FederatedServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FederatedServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendModel': grpc.unary_unary_rpc_method_handler(
                    servicer.SendModel,
                    request_deserializer=federated__pb2.ModelRequest.FromString,
                    response_serializer=federated__pb2.ModelReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc.Federated', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Federated(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.Federated/SendModel',
            federated__pb2.ModelRequest.SerializeToString,
            federated__pb2.ModelReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
