# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: FD.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08\x46\x44.proto\"\x18\n\x05\x43hunk\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\"%\n\x12UploadFileResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\tHashValue\x12\x12\n\nclientHash\x18\x01 \x01(\t\"\"\n\x0cHashCompared\x12\x12\n\nHashResult\x18\x01 \x01(\x08\";\n\x0bsentWeights\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0f\n\x07weights\x18\x02 \x03(\x02\x12\x0c\n\x04\x62ias\x18\x03 \x03(\x02\">\n\x0eweightResponse\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0f\n\x07weights\x18\x02 \x03(\x02\x12\x0c\n\x04\x62ias\x18\x03 \x03(\x02\"<\n\x0cinitialModel\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0f\n\x07weights\x18\x02 \x03(\x02\x12\x0c\n\x04\x62ias\x18\x03 \x03(\x02\"\x1c\n\nstartValue\x12\x0e\n\x06number\x18\x01 \x01(\x05\x32\xb8\x01\n\x0cModelService\x12+\n\nUploadFile\x12\x06.Chunk\x1a\x13.UploadFileResponse(\x01\x12&\n\tDiffModel\x12\n.HashValue\x1a\r.HashCompared\x12+\n\nsendWeight\x12\x0c.sentWeights\x1a\x0f.weightResponse\x12&\n\x08getModel\x12\x0b.startValue\x1a\r.initialModelb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'FD_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CHUNK']._serialized_start=12
  _globals['_CHUNK']._serialized_end=36
  _globals['_UPLOADFILERESPONSE']._serialized_start=38
  _globals['_UPLOADFILERESPONSE']._serialized_end=75
  _globals['_HASHVALUE']._serialized_start=77
  _globals['_HASHVALUE']._serialized_end=108
  _globals['_HASHCOMPARED']._serialized_start=110
  _globals['_HASHCOMPARED']._serialized_end=144
  _globals['_SENTWEIGHTS']._serialized_start=146
  _globals['_SENTWEIGHTS']._serialized_end=205
  _globals['_WEIGHTRESPONSE']._serialized_start=207
  _globals['_WEIGHTRESPONSE']._serialized_end=269
  _globals['_INITIALMODEL']._serialized_start=271
  _globals['_INITIALMODEL']._serialized_end=331
  _globals['_STARTVALUE']._serialized_start=333
  _globals['_STARTVALUE']._serialized_end=361
  _globals['_MODELSERVICE']._serialized_start=364
  _globals['_MODELSERVICE']._serialized_end=548
# @@protoc_insertion_point(module_scope)