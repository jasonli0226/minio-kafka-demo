import os
import json
import time
import pandas as pd

from kafka import KafkaConsumer
from dotenv import load_dotenv
from minio.event import Event

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER") or "localhost:9092"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") or ""
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") or ""
MINIO_SERVER = os.getenv("MINIO_SERVER") or "localhost:9000"


class KafkaConsumerService:
    def __init__(self, bootstrap_servers: list[str], topic_name: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.consumer: KafkaConsumer = None

        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            self.consumer = self.create_consumer()
            if self.consumer:
                break
            retry_count += 1
            time.sleep(5)  # Wait for 5 seconds before retrying

        if self.consumer is None:
            print("Failed to connect to Kafka after multiple retries. Exiting.")
            return

        self.consumer.subscribe([self.topic_name])

    def create_consumer(self):
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset="latest",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
            return consumer
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}")
            return None

    def message_handler(self, message: dict):
        try:
            print(
                f"Received message: {message.value} from topic: {message.topic}, partition: {message.partition}, offset: {message.offset}",
                flush=True,
            )

            event = Event.from_dict(message.value)
            df = pd.read_csv(
                f"s3://{event.key}",
                storage_options={
                    "key": AWS_ACCESS_KEY_ID,
                    "secret": AWS_SECRET_ACCESS_KEY,
                    "client_kwargs": {"endpoint_url": MINIO_SERVER},
                },
            )
            print("downloaded csv", flush=True)
            print(df.head(), flush=True)

        except TypeError as e:
            print(str(e), flush=True)
        except Exception as e:
            print(str(e), flush=True)

    def consume_messages(self):
        try:
            for message in self.consumer:
                self.message_handler(message)
        finally:
            self.consumer.close()


# Usage
if __name__ == "__main__":
    bootstrap_servers = [KAFKA_SERVER]  # Replace with your Kafka broker addresses
    topic_name = "my-topic"  # Replace with your Kafka topic

    # Create the Kafka consumer service
    consumer_service = KafkaConsumerService(bootstrap_servers, topic_name)

    # Start consuming messages
    consumer_service.consume_messages()
