from django.core.management.base import BaseCommand
from rating_app.kafka_agents.consumer import consume_ratings


class Command(BaseCommand):
    help = 'Starts the Kafka consumer to process ratings.'

    def handle(self, *args, **kwargs):
        consume_ratings()
