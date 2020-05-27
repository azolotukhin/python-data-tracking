from analytics_schema import options_pb2
from google.protobuf.descriptor import FieldDescriptor


class UnknownMessageError(ValueError):
    pass


class UnknownFieldError(ValueError):
    pass


TYPES_MAPPING = {
    FieldDescriptor.TYPE_DOUBLE: 'Float64',
    FieldDescriptor.TYPE_FLOAT: 'Float32',
    FieldDescriptor.TYPE_INT64: 'Int64',
    FieldDescriptor.TYPE_UINT64: 'UInt64',
    FieldDescriptor.TYPE_INT32: 'Int32',
    FieldDescriptor.TYPE_FIXED64: 'Int64',
    FieldDescriptor.TYPE_FIXED32: 'Int32',
    FieldDescriptor.TYPE_BOOL: 'UInt8',
    FieldDescriptor.TYPE_STRING: 'String',
    FieldDescriptor.TYPE_BYTES: 'String',
    FieldDescriptor.TYPE_UINT32: 'UInt32',
    FieldDescriptor.TYPE_ENUM: 'String',
    FieldDescriptor.TYPE_SFIXED32: 'Int32',
    FieldDescriptor.TYPE_SFIXED64: 'Int64',
    FieldDescriptor.TYPE_SINT32: 'Int32',
    FieldDescriptor.TYPE_SINT64: 'Int64',
}


def convert_proto_type_to_click_house_type(field_descriptor: FieldDescriptor) -> str:
    if field_descriptor.message_type:
        message_name = field_descriptor.message_type.name
        raise UnknownMessageError(f"Can't convert field with type message of {message_name} to Clickhouse type")

    field_meta = field_descriptor.GetOptions().Extensions[options_pb2.field_meta]
    if field_meta.clickhouse_data_type:
        ch_type = field_meta.clickhouse_data_type
    else:
        try:
            ch_type = TYPES_MAPPING[field_descriptor.type]
        except KeyError:
            raise UnknownFieldError(f"Can't convert field with type {field_descriptor.type} to Clickhouse type")

    if field_descriptor.label == FieldDescriptor.LABEL_REPEATED:
        return f'Array({ch_type})'

    return ch_type

