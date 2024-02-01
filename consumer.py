import json
import time

from kafka import KafkaConsumer


# Function to create a Kafka consumer
def create_consumer():
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=["172.1.0.30:9092"],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
        )

        return consumer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None


def run_consumer():
    print("running consumer")

    max_retries = 5
    retry_count = 0
    consumer = None

    while retry_count < max_retries:
        consumer = create_consumer()
        if consumer:
            break
        retry_count += 1
        time.sleep(5)  # Wait for 5 seconds before retrying

    print(f"{retry_count}")

    if consumer:
        print("consumer is found")
        consumer.subscribe(topics="my-topic")

        for message in consumer:
            print(
                "{}:{}:{}: key={} value={}".format(
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    message.value,
                )
            )
    else:
        print("Failed to connect to Kafka after multiple retries. Exiting.")


if __name__ == "__main__":
    print("main")
    run_consumer()
else:
    print("error")
