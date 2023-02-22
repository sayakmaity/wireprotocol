# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chatapp_pb2 as chatapp__pb2


class ChatServiceStub(object):
    """The chat service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Chat = channel.unary_unary(
                '/ChatService/Chat',
                request_serializer=chatapp__pb2.Message.SerializeToString,
                response_deserializer=chatapp__pb2.User.FromString,
                )
        self.Packet = channel.unary_unary(
                '/ChatService/Packet',
                request_serializer=chatapp__pb2.Request.SerializeToString,
                response_deserializer=chatapp__pb2.User.FromString,
                )
        self.ListenToPendingMessages = channel.unary_unary(
                '/ChatService/ListenToPendingMessages',
                request_serializer=chatapp__pb2.Request.SerializeToString,
                response_deserializer=chatapp__pb2.PendingMsgsResponse.FromString,
                )


class ChatServiceServicer(object):
    """The chat service definition.
    """

    def Chat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Packet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListenToPendingMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Chat': grpc.unary_unary_rpc_method_handler(
                    servicer.Chat,
                    request_deserializer=chatapp__pb2.Message.FromString,
                    response_serializer=chatapp__pb2.User.SerializeToString,
            ),
            'Packet': grpc.unary_unary_rpc_method_handler(
                    servicer.Packet,
                    request_deserializer=chatapp__pb2.Request.FromString,
                    response_serializer=chatapp__pb2.User.SerializeToString,
            ),
            'ListenToPendingMessages': grpc.unary_unary_rpc_method_handler(
                    servicer.ListenToPendingMessages,
                    request_deserializer=chatapp__pb2.Request.FromString,
                    response_serializer=chatapp__pb2.PendingMsgsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatService(object):
    """The chat service definition.
    """

    @staticmethod
    def Chat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Chat',
            chatapp__pb2.Message.SerializeToString,
            chatapp__pb2.User.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Packet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Packet',
            chatapp__pb2.Request.SerializeToString,
            chatapp__pb2.User.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListenToPendingMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/ListenToPendingMessages',
            chatapp__pb2.Request.SerializeToString,
            chatapp__pb2.PendingMsgsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
