# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: federated.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x66\x65\x64\x65rated.proto\x12\x03rpc\"\x1c\n\x0cModelRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x1d\n\nModelReply\x12\x0f\n\x07message\x18\x01 \x01(\t2>\n\tFederated\x12\x31\n\tSendModel\x12\x11.rpc.ModelRequest\x1a\x0f.rpc.ModelReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'federated_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MODELREQUEST']._serialized_start=24
  _globals['_MODELREQUEST']._serialized_end=52
  _globals['_MODELREPLY']._serialized_start=54
  _globals['_MODELREPLY']._serialized_end=83
  _globals['_FEDERATED']._serialized_start=85
  _globals['_FEDERATED']._serialized_end=147
# @@protoc_insertion_point(module_scope)
