from kafka import KafkaProducer
import json
from django.conf import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_rating(rating_data):
    producer.send(settings.KAFKA_TOPIC, rating_data)
    producer.flush()