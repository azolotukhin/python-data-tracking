from analytics_schema import options_pb2
from google.protobuf.descriptor import FieldDescriptor


class UnknownMessageError(ValueError):
    pass


class UnknownFieldError(ValueError):
    pass


def convert_proto_type_to_click_house_type(field_descriptor: FieldDescriptor) -> str:

    is_repeated = field_descriptor.label == FieldDescriptor.LABEL_REPEATED

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

    if field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
        cls = field_descriptor.message_type._concrete_class
        if cls is options_pb2.DateField:
            ch_type = 'Date'
        elif cls is options_pb2.DateTimeField:
            ch_type = 'DateTime'
        else:
            raise UnknownMessageError(f'Can\'t convert field with type message of {cls.__name__} to Clickhouse type')
    elif field_descriptor.type in TYPES_MAPPING:
        ch_type = TYPES_MAPPING[field_descriptor.type]
    else:
        raise UnknownFieldError(f'Can\'t convert field with type {field_descriptor.type} to Clickhouse type')

    if is_repeated:
        return f'Array({ch_type})'

    return ch_type

