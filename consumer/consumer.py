import os
import json
import time

from kafka import KafkaConsumer
from dotenv import load_dotenv


load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER") or "localhost:9092"


class KafkaConsumerService:
    def __init__(self, bootstrap_servers, topic_name):
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.consumer = None

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
                auto_offset_reset="earliest",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
            return consumer
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}")
            return None

    def consume_messages(self):
        try:
            for message in self.consumer:
                print(
                    f"Received message: {message.value} from topic: {message.topic}, partition: {message.partition}, offset: {message.offset}",
                    flush=True,
                )
        except KeyboardInterrupt:
            print("Consumer stopped.")
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
