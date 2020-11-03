import os
import logging
from datetime import datetime
from kafka import KafkaProducer
from kafka import KafkaConsumer


logger = logging.getLogger('solution2')
logger.setLevel(logging.DEBUG)
logFormat = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
logStreamHandler = logging.StreamHandler()
logStreamHandler.setFormatter(logFormat)
logger.addHandler(logStreamHandler)


def main():
    kafka_bootstrap_servers = get_kafka_bootstrap_servers()
    kafka_input_topic = get_env('KAFKA_INPUT_TOPIC')
    logger.info(f"KAFKA_INPUT_TOPIC={kafka_input_topic}")
    kafka_output_topic = get_env('KAFKA_OUTPUT_TOPIC')
    logger.info(f"KAFKA_OUTPUT_TOPIC={kafka_output_topic}")

    logger.info(f"Connecting to {kafka_bootstrap_servers}")
    consumer = KafkaConsumer(kafka_input_topic,
                             bootstrap_servers=kafka_bootstrap_servers,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='solution2',
                             value_deserializer=lambda x: x.decode("utf-8"))
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                             value_serializer=lambda x: str(x).encode('utf-8'))
    for message in consumer:
        data = message.value
        logger.debug(f"recieved data = {data}")
        dt = datetime.fromtimestamp(float(data)/1000.0)
        rfc_time = dt.isoformat()
        logger.debug(f"sending data = {rfc_time}")
        producer.send(kafka_output_topic, value=rfc_time)


def get_kafka_bootstrap_servers() -> list:
    bootstap_string = get_env('KAFKA_BOOTSTAP_SERVERS')
    return bootstap_string.split(',')


def get_env(env) -> str:
    env_value = os.getenv(env)
    if not env_value:
        logger.error(
            f"{env} environment variable is not defined. Exiting...")
        exit(1)
    return env_value


if __name__ == "__main__":
    main()
