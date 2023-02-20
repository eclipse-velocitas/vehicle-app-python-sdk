# -*- coding: utf-8 -*-
# Copyright (c) 2022-2023 Robert Bosch GmbH and Microsoft Corporation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

# Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hvac.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nhvac.proto\x12\x18sdv.edge.comfort.hvac.v1\"H\n\x12SetAcStatusRequest\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".sdv.edge.comfort.hvac.v1.AcStatus\"\x12\n\x10SetAcStatusReply\",\n\x15SetTemperatureRequest\x12\x13\n\x0btemperature\x18\x01 \x01(\x02\"\x15\n\x13SetTemperatureReply*\x1b\n\x08\x41\x63Status\x12\x07\n\x03OFF\x10\x00\x12\x06\n\x02ON\x10\x01\x32\xe1\x01\n\x04Hvac\x12g\n\x0bSetAcStatus\x12,.sdv.edge.comfort.hvac.v1.SetAcStatusRequest\x1a*.sdv.edge.comfort.hvac.v1.SetAcStatusReply\x12p\n\x0eSetTemperature\x12/.sdv.edge.comfort.hvac.v1.SetTemperatureRequest\x1a-.sdv.edge.comfort.hvac.v1.SetTemperatureReplyb\x06proto3')

_ACSTATUS = DESCRIPTOR.enum_types_by_name['AcStatus']
AcStatus = enum_type_wrapper.EnumTypeWrapper(_ACSTATUS)
OFF = 0
ON = 1


_SETACSTATUSREQUEST = DESCRIPTOR.message_types_by_name['SetAcStatusRequest']
_SETACSTATUSREPLY = DESCRIPTOR.message_types_by_name['SetAcStatusReply']
_SETTEMPERATUREREQUEST = DESCRIPTOR.message_types_by_name['SetTemperatureRequest']
_SETTEMPERATUREREPLY = DESCRIPTOR.message_types_by_name['SetTemperatureReply']
SetAcStatusRequest = _reflection.GeneratedProtocolMessageType('SetAcStatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETACSTATUSREQUEST,
  '__module__' : 'hvac_pb2'
  # @@protoc_insertion_point(class_scope:sdv.edge.comfort.hvac.v1.SetAcStatusRequest)
  })
_sym_db.RegisterMessage(SetAcStatusRequest)

SetAcStatusReply = _reflection.GeneratedProtocolMessageType('SetAcStatusReply', (_message.Message,), {
  'DESCRIPTOR' : _SETACSTATUSREPLY,
  '__module__' : 'hvac_pb2'
  # @@protoc_insertion_point(class_scope:sdv.edge.comfort.hvac.v1.SetAcStatusReply)
  })
_sym_db.RegisterMessage(SetAcStatusReply)

SetTemperatureRequest = _reflection.GeneratedProtocolMessageType('SetTemperatureRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETTEMPERATUREREQUEST,
  '__module__' : 'hvac_pb2'
  # @@protoc_insertion_point(class_scope:sdv.edge.comfort.hvac.v1.SetTemperatureRequest)
  })
_sym_db.RegisterMessage(SetTemperatureRequest)

SetTemperatureReply = _reflection.GeneratedProtocolMessageType('SetTemperatureReply', (_message.Message,), {
  'DESCRIPTOR' : _SETTEMPERATUREREPLY,
  '__module__' : 'hvac_pb2'
  # @@protoc_insertion_point(class_scope:sdv.edge.comfort.hvac.v1.SetTemperatureReply)
  })
_sym_db.RegisterMessage(SetTemperatureReply)

_HVAC = DESCRIPTOR.services_by_name['Hvac']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACSTATUS._serialized_start=203
  _ACSTATUS._serialized_end=230
  _SETACSTATUSREQUEST._serialized_start=40
  _SETACSTATUSREQUEST._serialized_end=112
  _SETACSTATUSREPLY._serialized_start=114
  _SETACSTATUSREPLY._serialized_end=132
  _SETTEMPERATUREREQUEST._serialized_start=134
  _SETTEMPERATUREREQUEST._serialized_end=178
  _SETTEMPERATUREREPLY._serialized_start=180
  _SETTEMPERATUREREPLY._serialized_end=201
  _HVAC._serialized_start=233
  _HVAC._serialized_end=458
# @@protoc_insertion_point(module_scope)
