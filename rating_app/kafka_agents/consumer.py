from kafka import KafkaConsumer
import json
from django.conf import settings
from tasks import process_rating


def consume_ratings():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='rating-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        rating_data = message.value
        process_rating.delay(rating_data)
