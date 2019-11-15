import os
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

from OpenSSL import crypto
from confluent_kafka import Producer


def heroku_kafka_producer(extra_config = {}):
    cert_file = NamedTemporaryFile(suffix='.crt', delete=False)
    cert_file.write(os.environ['KAFKA_CLIENT_CERT'].encode('utf-8'))
    cert_file.flush()

    key_file = NamedTemporaryFile(suffix='.key', delete=True)
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, os.environ['KAFKA_CLIENT_CERT_KEY'])
    pwd = str(os.urandom(33))
    key_enc = crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key,
                                     cipher='DES-EDE3-CBC',
                                     passphrase=pwd.encode())
    key_file.write(key_enc)
    key_file.flush()

    trust_file = NamedTemporaryFile(suffix='.crt', delete=False)
    trust_file.write(os.environ['KAFKA_TRUSTED_CERT'].encode('utf-8'))
    trust_file.flush()

    kafka_brokers = get_kafka_brokers()

    config = {
        'bootstrap.servers': kafka_brokers,
        'security.protocol': 'ssl',
        'ssl.ca.location': trust_file.name,
        'ssl.certificate.location': cert_file.name,
        'ssl.key.location': key_file.name,
        'ssl.key.password': pwd
    }

    producer_config = {**config, **extra_config}
    producer = Producer(producer_config)

    # Files will automatically be deleted when closed
    cert_file.close()
    key_file.close()
    trust_file.close()

    return producer


def get_kafka_brokers():
    if not os.environ.get('KAFKA_URL'):
        raise RuntimeError('The KAFKA_URL config variable is not set.')

    return ','.join(['{}:{}'.format(parsedUrl.hostname, parsedUrl.port) for parsedUrl in
                     [urlparse(url) for url in os.environ.get('KAFKA_URL').split(',')]])
