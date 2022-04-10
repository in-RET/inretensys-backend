import paho.mqtt.client as mqtt
import jsons
import atexit

from .log import HsnLogger
log = HsnLogger()


from .config import set_init_function_args_as_instance_args


class HsnMqttConnectionConfig(object):
    def __init__(
        self,
        host : str = 'localhost',
        port : int = 22,
        keepalive : int = 60,
        username : str = '',
        password : str = '',
        log : bool = False,
        identifier : str = 'mqtt_client'
    ):
        set_init_function_args_as_instance_args(self, locals())

    format = {
        'host' : 'str:256',
        'port' : 'int:1:65535:1',
        'keepalive' : 'int:1:3600:1',
        'username' : 'str:256',
        'password' : 'str:4096',
        'log' : 'bool',
        'identifier' : 'str:256'
    }


class HsnMqttHandler(object):
    __mqtt_topics = None
    __mqtt_connected = None

    def __init__(
        self,
        mqtt_config : HsnMqttConnectionConfig,
        *args,
        **kwargs
    ) -> None:
        self.__mqtt_topics = {}
        self.__mqtt_connected = False

        self.__mqtt_id = mqtt_config.identifier

        self.__mqtt = mqtt.Client(self.__mqtt_id)

        if len(mqtt_config.username)>0 and len(mqtt_config.password)>0:
            self.__mqtt.username_pw_set(mqtt_config.username, mqtt_config.password)

        self.__mqtt.on_connect = self.__mqtt_on_connect
        self.__mqtt.on_disconnect = self.__mqtt_on_disconnect
        self.__mqtt.on_message = self.__mqtt_on_message
        
        if mqtt_config.log:
            self.__mqtt.on_log = self.__mqtt_on_log

        assert(mqtt_config.host is not None)

        self.__mqtt.connect(
            mqtt_config.host,
            mqtt_config.port,
            mqtt_config.keepalive
        )

        atexit.register(self.mqtt_loop_stop)

    def __mqtt_on_connect(self, client, userdata, flags, rc):
        for key in self.__mqtt_topics:
            self.__mqtt.subscribe(key)

        self.__mqtt_connected = True
        if log:
            log.info(f'{self.__mqtt_id} connected to mqtt broker')

    def __mqtt_on_disconnect(self, client, userdata, rc):
        self.__mqtt_connected = False
        if log:
            log.info(f'{self.__mqtt_id} disconnected from mqtt broker')

    def __mqtt_on_message(self, client, userdata, msg):
        if msg.topic in self.__mqtt_topics:
            self.__mqtt_topics[msg.topic](jsons.loads(msg.payload))

    def __mqtt_on_log(self, client, userdata, level, msg):
        if log:
            log.trace(f'{self.__mqtt_id} mqtt log: {msg}')

    def mqtt_loop_start(self):
        self.__mqtt.loop_start()

    def mqtt_loop_stop(self):
        self.__mqtt.loop_stop()

    @property
    def mqtt_is_connected(self):
        return self.__mqtt_connected

    def mqtt_subscribe(self, topic, callback):
        self.__mqtt_topics[topic] = callback
        self.__mqtt.subscribe(topic)

    def mqtt_publish(self, topic, data=None):
        topic = f'{self.__mqtt_id}/{topic}'
        
        if self.mqtt_is_connected:
            self.__mqtt.publish(topic, jsons.dumps(data))

    def mqtt_unsubscribe(self, topic : str):
        topic = f'{self.__mqtt_id}/{topic}'
        
        if topic in self.__mqtt_topics:
            del self.__mqtt_topics[topic]
            self.__mqtt.unsubscribe(topic)

    def mqtt_on_topic(self, topic : str):
        topic = f'{self.__mqtt_id}/{topic}'

        def decorator(f):
            self.mqtt_subscribe(topic, f)
            return f
        
        return decorator