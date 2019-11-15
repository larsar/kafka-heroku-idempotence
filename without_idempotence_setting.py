from kafka import heroku_kafka_producer
from dotenv import load_dotenv
import os

load_dotenv()

p = heroku_kafka_producer()
p.produce('{}idempotence-test-topic'.format(os.environ['KAFKA_PREFIX']), 'Hello....this is working')
p.flush()
print("Done")
