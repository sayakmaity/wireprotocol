# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"\x18\n\x04User\x12\x10\n\x08username\x18\x01 \x01(\t\"%\n\x08UserList\x12\x19\n\x05users\x18\x01 \x03(\x0b\x32\n.chat.User\"1\n\rLoginResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"9\n\x15\x43reateAccountResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"9\n\x15\x44\x65leteAccountResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"&\n\x13ListAccountsRequest\x12\x0f\n\x07pattern\x18\x01 \x01(\t\")\n\x14ListAccountsResponse\x12\x11\n\tusernames\x18\x01 \x03(\t\"9\n\x07Message\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\"7\n\x13SendMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xe4\x02\n\x0b\x43hatService\x12*\n\x05Login\x12\n.chat.User\x1a\x13.chat.LoginResponse\"\x00\x12+\n\x06Logout\x12\n.chat.User\x1a\x13.chat.LoginResponse\"\x00\x12:\n\rCreateAccount\x12\n.chat.User\x1a\x1b.chat.CreateAccountResponse\"\x00\x12:\n\rDeleteAccount\x12\n.chat.User\x1a\x1b.chat.DeleteAccountResponse\"\x00\x12G\n\x0cListAccounts\x12\x19.chat.ListAccountsRequest\x1a\x1a.chat.ListAccountsResponse\"\x00\x12;\n\x0bSendMessage\x12\r.chat.Message\x1a\x19.chat.SendMessageResponse\"\x00\x30\x01\x62\x06proto3')



_USER = DESCRIPTOR.message_types_by_name['User']
_USERLIST = DESCRIPTOR.message_types_by_name['UserList']
_LOGINRESPONSE = DESCRIPTOR.message_types_by_name['LoginResponse']
_CREATEACCOUNTRESPONSE = DESCRIPTOR.message_types_by_name['CreateAccountResponse']
_DELETEACCOUNTRESPONSE = DESCRIPTOR.message_types_by_name['DeleteAccountResponse']
_LISTACCOUNTSREQUEST = DESCRIPTOR.message_types_by_name['ListAccountsRequest']
_LISTACCOUNTSRESPONSE = DESCRIPTOR.message_types_by_name['ListAccountsResponse']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_SENDMESSAGERESPONSE = DESCRIPTOR.message_types_by_name['SendMessageResponse']
User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.User)
  })
_sym_db.RegisterMessage(User)

UserList = _reflection.GeneratedProtocolMessageType('UserList', (_message.Message,), {
  'DESCRIPTOR' : _USERLIST,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.UserList)
  })
_sym_db.RegisterMessage(UserList)

LoginResponse = _reflection.GeneratedProtocolMessageType('LoginResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOGINRESPONSE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.LoginResponse)
  })
_sym_db.RegisterMessage(LoginResponse)

CreateAccountResponse = _reflection.GeneratedProtocolMessageType('CreateAccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCOUNTRESPONSE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.CreateAccountResponse)
  })
_sym_db.RegisterMessage(CreateAccountResponse)

DeleteAccountResponse = _reflection.GeneratedProtocolMessageType('DeleteAccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEACCOUNTRESPONSE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.DeleteAccountResponse)
  })
_sym_db.RegisterMessage(DeleteAccountResponse)

ListAccountsRequest = _reflection.GeneratedProtocolMessageType('ListAccountsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTACCOUNTSREQUEST,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.ListAccountsRequest)
  })
_sym_db.RegisterMessage(ListAccountsRequest)

ListAccountsResponse = _reflection.GeneratedProtocolMessageType('ListAccountsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTACCOUNTSRESPONSE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.ListAccountsResponse)
  })
_sym_db.RegisterMessage(ListAccountsResponse)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.Message)
  })
_sym_db.RegisterMessage(Message)

SendMessageResponse = _reflection.GeneratedProtocolMessageType('SendMessageResponse', (_message.Message,), {
  'DESCRIPTOR' : _SENDMESSAGERESPONSE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:chat.SendMessageResponse)
  })
_sym_db.RegisterMessage(SendMessageResponse)

_CHATSERVICE = DESCRIPTOR.services_by_name['ChatService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USER._serialized_start=20
  _USER._serialized_end=44
  _USERLIST._serialized_start=46
  _USERLIST._serialized_end=83
  _LOGINRESPONSE._serialized_start=85
  _LOGINRESPONSE._serialized_end=134
  _CREATEACCOUNTRESPONSE._serialized_start=136
  _CREATEACCOUNTRESPONSE._serialized_end=193
  _DELETEACCOUNTRESPONSE._serialized_start=195
  _DELETEACCOUNTRESPONSE._serialized_end=252
  _LISTACCOUNTSREQUEST._serialized_start=254
  _LISTACCOUNTSREQUEST._serialized_end=292
  _LISTACCOUNTSRESPONSE._serialized_start=294
  _LISTACCOUNTSRESPONSE._serialized_end=335
  _MESSAGE._serialized_start=337
  _MESSAGE._serialized_end=394
  _SENDMESSAGERESPONSE._serialized_start=396
  _SENDMESSAGERESPONSE._serialized_end=451
  _CHATSERVICE._serialized_start=454
  _CHATSERVICE._serialized_end=810
# @@protoc_insertion_point(module_scope)