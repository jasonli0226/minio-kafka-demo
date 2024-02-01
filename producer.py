import json
import time

from kafka import KafkaProducer


def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=["172.1.0.30:9092"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        return producer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None


def run_producer():
    print("running producer...")

    max_retries = 5
    retry_count = 0
    producer = None

    while retry_count < max_retries:
        producer = create_producer()
        if producer:
            break
        retry_count += 1
        time.sleep(5)  # Wait for 5 seconds before retrying

    if producer:
        print("producer is found")
        for i in range(1, 10):
            print(f"{i=}")
            producer.send("my-topic", {"number": i})

        producer.flush()  # To avoid messages stuck.
    else:
        print("Failed to connect to Kafka after multiple retries. Exiting.")


if __name__ == "__main__":
    run_producer()
