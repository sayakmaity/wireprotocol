# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chatapp.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatapp.proto\"+\n\x07Request\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"9\n\x07Message\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\"\x14\n\x04User\x12\x0c\n\x04text\x18\x01 \x01(\t\".\n\nPendingRes\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0f\n\x07isEmpty\x18\x02 \x01(\x08\x32h\n\x0b\x43hatService\x12\x19\n\x04\x43hat\x12\x08.Message\x1a\x05.User\"\x00\x12\x1b\n\x06Packet\x12\x08.Request\x1a\x05.User\"\x00\x12!\n\x06Listen\x12\x08.Request\x1a\x0b.PendingRes\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatapp_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=17
  _REQUEST._serialized_end=60
  _MESSAGE._serialized_start=62
  _MESSAGE._serialized_end=119
  _USER._serialized_start=121
  _USER._serialized_end=141
  _PENDINGRES._serialized_start=143
  _PENDINGRES._serialized_end=189
  _CHATSERVICE._serialized_start=191
  _CHATSERVICE._serialized_end=295
# @@protoc_insertion_point(module_scope)
