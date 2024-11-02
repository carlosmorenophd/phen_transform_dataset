import pika
from envparse import env
import jsonpickle
from os import getcwd
from src.transforms.utils import TransformDataset
from transforms.operation import TransformNormalize
from transforms.transform import Transform, TransformEnum
from transforms.normalize import Normalize, NormalizeEnum
from transforms.valid.row import RowValid, RowValidEnum


def send() -> None:
    print(getcwd())
    env.read_envfile('.env')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=env('RABBITMQ_HOST', cast=str),
            port=env('RABBITMQ_PORT', cast=int),
            credentials=pika.PlainCredentials(
                username=env('RABBITMQ_USER', cast=str),
                password=env('RABBITMQ_PASS', cast=str),
            )
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    message = TransformDataset(
        source_file_name="source",
        destiny_file_name="destiny",
        actions=[
            TransformNormalize(
                column="GRAIN_YIELD:(t/ha):avg",
                transform=Transform(transform_enum=TransformEnum.PASS),
                normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE),
            ),
            TransformNormalize(
                column='SOWING_DATE:(date)',
                transform=Transform(transform_enum=TransformEnum.FORCE_ONE),
                normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
            )],
        remove_rows=[
            RowValid(
                column="GRAIN_YIELD:(t/ha):avg",
                valid=RowValidEnum.VALUE_OR_REMOVE
            ),
            RowValid(
                column="SOWING_DATE:(date)",
                valid=RowValidEnum.VALUE_OR_REMOVE
            ),
        ]
    )

    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=jsonpickle.encode(message),
    )
    print('Send message')
    connection.close()
