from kafka import KafkaProducer
import json
from django.conf import settings

import logging
logger = logging.getLogger("kafka")
logger.setLevel(logging.DEBUG)

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_rating(rating_data):
    try:
        producer.send(settings.KAFKA_TOPIC, rating_data)
        producer.flush()
    except Exception as e:
        logger.error(f"Failed to send message to Kafka: {e}")
