import iothub_client
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
import time

communication_protocol = IoTHubTransportProvider.MQTT

connection_string = "HostName=xxxx;DeviceId=xxx;SharedAccessKey=xxxx"

device_id="ESP8266"
messageId=1

message_format = '{\"deviceId\": %s,\"messageId\": %d, \"aZ\": %f, \"gps_lat_dir\" : %s, \"gps_lat_val\": %s, \"gps_lon_dir\":%s, \"gps_lon_val\":%s}'

client=None
request_count = 0
response_count = 0
ack_received=False

def iothub_message_callback(message, result, user_context):
    global response_count
    response_count = response_count + 1
    print ( "[ IoT Hub ] Response ( %s )" % (result) )

def iothub_client_init():
    global client
    try:
        client = IoTHubClient(connection_string, communication_protocol)
        print "[ IoT Client ] Initialization Successful"
    except:
        print "[ IoT Client ] Initialization Failed"

def frame_message(device_id, message_id, sensor_value, gps_lat, gps_lon):
    msg_payload = message_format % (device_id, message_id, sensor_value, "N", gps_lat, "E", gps_lon)
    return msg_payload 

def iothub_client_send(msg_payload):
    global request_count
    try:
        message = IoTHubMessage(msg_payload)
        print( "[ IoT Client ] Transmitting Message ( %s )" % message.get_string() )
        request_count = request_count + 1
        client.send_event_async(message, iothub_message_callback, None)
        while response_count < request_count:
            time.sleep(1)

    except IoTHubError as error:
        print ( "[ IoT Client ] Unknown error thrown from IoT Hub ( %s )" % error )
        return

if __name__ == '__main__':
    a_z = 10.0
    iothub_client_init()
    msg_payload = frame_message(device_id, messageId, a_z, "0.0", "0.0")
    iothub_client_send(msg_payload)

