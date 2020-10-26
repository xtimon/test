import os
import logging
import time
from time import sleep
from kafka import KafkaProducer

logger = logging.getLogger('solution1')
logger.setLevel(logging.INFO)
logFormat = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
logStreamHandler = logging.StreamHandler()
logStreamHandler.setFormatter(logFormat)
logger.addHandler(logStreamHandler)


def main():
    kafka_bootstrap_servers = get_kafka_bootstrap_servers()
    kafka_topic = get_kafka_topic()
    logger.info(f"Connecting to {kafka_bootstrap_servers}")
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                             value_serializer=lambda x: str(x).encode('utf-8'))
    while True:
        producer.send(kafka_topic, value=time.time() * 1000)
        sleep(1)


def get_kafka_bootstrap_servers() -> list:
    bootstap_string = os.getenv('KAFKA_BOOTSTAP_SERVERS')
    if not bootstap_string:
        logger.error(
            "KAFKA_BOOTSTAP_SERVERS environment variable is not defined. Exiting...")
        exit(1)
    return bootstap_string.split(',')


def get_kafka_topic() -> str:
    topic = os.getenv("KAFKA_TOPIC")
    if not topic:
        logger.error(
            "KAFKA_TOPIC environment variable is not defined. Exiting...")
        exit(1)
    return topic


if __name__ == "__main__":
    main()
