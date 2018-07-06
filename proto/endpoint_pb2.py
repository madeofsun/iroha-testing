# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: endpoint.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import block_pb2 as block__pb2
import queries_pb2 as queries__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import responses_pb2 as responses__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='endpoint.proto',
  package='iroha.protocol',
  syntax='proto3',
  serialized_pb=_b('\n\x0e\x65ndpoint.proto\x12\x0eiroha.protocol\x1a\x0b\x62lock.proto\x1a\rqueries.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0fresponses.proto\"d\n\rToriiResponse\x12+\n\ttx_status\x18\x01 \x01(\x0e\x32\x18.iroha.protocol.TxStatus\x12\x0f\n\x07tx_hash\x18\x02 \x01(\x0c\x12\x15\n\rerror_message\x18\x03 \x01(\t\"\"\n\x0fTxStatusRequest\x12\x0f\n\x07tx_hash\x18\x01 \x01(\x0c*\xc0\x01\n\x08TxStatus\x12\x1f\n\x1bSTATELESS_VALIDATION_FAILED\x10\x00\x12 \n\x1cSTATELESS_VALIDATION_SUCCESS\x10\x01\x12\x1e\n\x1aSTATEFUL_VALIDATION_FAILED\x10\x02\x12\x1f\n\x1bSTATEFUL_VALIDATION_SUCCESS\x10\x03\x12\r\n\tCOMMITTED\x10\x04\x12\x0f\n\x0bMST_EXPIRED\x10\x05\x12\x10\n\x0cNOT_RECEIVED\x10\x06\x32\xea\x01\n\x0e\x43ommandService\x12<\n\x05Torii\x12\x1b.iroha.protocol.Transaction\x1a\x16.google.protobuf.Empty\x12H\n\x06Status\x12\x1f.iroha.protocol.TxStatusRequest\x1a\x1d.iroha.protocol.ToriiResponse\x12P\n\x0cStatusStream\x12\x1f.iroha.protocol.TxStatusRequest\x1a\x1d.iroha.protocol.ToriiResponse0\x01\x32\x9f\x01\n\x0cQueryService\x12<\n\x04\x46ind\x12\x15.iroha.protocol.Query\x1a\x1d.iroha.protocol.QueryResponse\x12Q\n\x0c\x46\x65tchCommits\x12\x1b.iroha.protocol.BlocksQuery\x1a\".iroha.protocol.BlockQueryResponse0\x01\x62\x06proto3')
  ,
  dependencies=[block__pb2.DESCRIPTOR,queries__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,responses__pb2.DESCRIPTOR,])

_TXSTATUS = _descriptor.EnumDescriptor(
  name='TxStatus',
  full_name='iroha.protocol.TxStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATELESS_VALIDATION_FAILED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATELESS_VALIDATION_SUCCESS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATEFUL_VALIDATION_FAILED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATEFUL_VALIDATION_SUCCESS', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMMITTED', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MST_EXPIRED', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_RECEIVED', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=247,
  serialized_end=439,
)
_sym_db.RegisterEnumDescriptor(_TXSTATUS)

TxStatus = enum_type_wrapper.EnumTypeWrapper(_TXSTATUS)
STATELESS_VALIDATION_FAILED = 0
STATELESS_VALIDATION_SUCCESS = 1
STATEFUL_VALIDATION_FAILED = 2
STATEFUL_VALIDATION_SUCCESS = 3
COMMITTED = 4
MST_EXPIRED = 5
NOT_RECEIVED = 6



_TORIIRESPONSE = _descriptor.Descriptor(
  name='ToriiResponse',
  full_name='iroha.protocol.ToriiResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tx_status', full_name='iroha.protocol.ToriiResponse.tx_status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tx_hash', full_name='iroha.protocol.ToriiResponse.tx_hash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='iroha.protocol.ToriiResponse.error_message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=108,
  serialized_end=208,
)


_TXSTATUSREQUEST = _descriptor.Descriptor(
  name='TxStatusRequest',
  full_name='iroha.protocol.TxStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tx_hash', full_name='iroha.protocol.TxStatusRequest.tx_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=210,
  serialized_end=244,
)

_TORIIRESPONSE.fields_by_name['tx_status'].enum_type = _TXSTATUS
DESCRIPTOR.message_types_by_name['ToriiResponse'] = _TORIIRESPONSE
DESCRIPTOR.message_types_by_name['TxStatusRequest'] = _TXSTATUSREQUEST
DESCRIPTOR.enum_types_by_name['TxStatus'] = _TXSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ToriiResponse = _reflection.GeneratedProtocolMessageType('ToriiResponse', (_message.Message,), dict(
  DESCRIPTOR = _TORIIRESPONSE,
  __module__ = 'endpoint_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.ToriiResponse)
  ))
_sym_db.RegisterMessage(ToriiResponse)

TxStatusRequest = _reflection.GeneratedProtocolMessageType('TxStatusRequest', (_message.Message,), dict(
  DESCRIPTOR = _TXSTATUSREQUEST,
  __module__ = 'endpoint_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.TxStatusRequest)
  ))
_sym_db.RegisterMessage(TxStatusRequest)



_COMMANDSERVICE = _descriptor.ServiceDescriptor(
  name='CommandService',
  full_name='iroha.protocol.CommandService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=442,
  serialized_end=676,
  methods=[
  _descriptor.MethodDescriptor(
    name='Torii',
    full_name='iroha.protocol.CommandService.Torii',
    index=0,
    containing_service=None,
    input_type=block__pb2._TRANSACTION,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Status',
    full_name='iroha.protocol.CommandService.Status',
    index=1,
    containing_service=None,
    input_type=_TXSTATUSREQUEST,
    output_type=_TORIIRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StatusStream',
    full_name='iroha.protocol.CommandService.StatusStream',
    index=2,
    containing_service=None,
    input_type=_TXSTATUSREQUEST,
    output_type=_TORIIRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_COMMANDSERVICE)

DESCRIPTOR.services_by_name['CommandService'] = _COMMANDSERVICE


_QUERYSERVICE = _descriptor.ServiceDescriptor(
  name='QueryService',
  full_name='iroha.protocol.QueryService',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=679,
  serialized_end=838,
  methods=[
  _descriptor.MethodDescriptor(
    name='Find',
    full_name='iroha.protocol.QueryService.Find',
    index=0,
    containing_service=None,
    input_type=queries__pb2._QUERY,
    output_type=responses__pb2._QUERYRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FetchCommits',
    full_name='iroha.protocol.QueryService.FetchCommits',
    index=1,
    containing_service=None,
    input_type=queries__pb2._BLOCKSQUERY,
    output_type=responses__pb2._BLOCKQUERYRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_QUERYSERVICE)

DESCRIPTOR.services_by_name['QueryService'] = _QUERYSERVICE

# @@protoc_insertion_point(module_scope)
