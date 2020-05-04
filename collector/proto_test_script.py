from analytics_schema.events import test_pb2
from analytics_schema import options_pb2
from analytics_schema import track_event_pb2


a = track_event_pb2.TrackEvent()


if __name__ == '__main__':
    b = track_event_pb2.TrackEvent()
    event_message = test_pb2.TestMessage(
        test='123'
    )
    b.WhichOneof('event')
    b.Test.CopyFrom(event_message)
    options = b.Test.DESCRIPTOR.GetOptions().Extensions[options_pb2.table_meta]
    table_name = options.NAME
    table_engine = options.WhichOneof('ENGINE')
    engine_params = getattr(options, table_engine)
    print(table_name, table_engine, engine_params)
