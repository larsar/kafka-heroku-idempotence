import os

from dotenv import load_dotenv

from kafka import heroku_kafka_producer

load_dotenv()

p = heroku_kafka_producer({'enable.idempotence': True})
p.produce('{}idempotence-test-topic'.format(os.environ['KAFKA_PREFIX']), 'Hello...this message will never be delivered')
p.flush()
print("Done")
