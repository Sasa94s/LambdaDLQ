import json
import os
from time import time
from uuid import uuid4

import boto3
from logger import get_logger


QUEUE_NAME = os.environ.get('QUEUE_NAME')
RAISE_ERROR_FLAG = os.environ.get('RAISE_ERROR_FLAG')
logger = get_logger()


def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    sqs_queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
    msg_text = 'Hello from mySQSPusher Lambda! - ts[{}]'.format(time())

    try:
        if RAISE_ERROR_FLAG == 'Y':
            raise Exception

        rid = 'rid-{}'.format(str(uuid4()))
        code = '200'
        msg = sqs.send_message(QueueUrl=sqs_queue_url,
                               MessageBody=json.dumps({'Message': msg_text}),
                               MessageAttributes={
                                   'ErrorMessage': {
                                       'DataType': 'String',
                                       'StringValue': json.dumps({'Message': msg_text})
                                   },
                                   'RequestID': {
                                       'DataType': 'String',
                                       'StringValue': rid
                                   },
                                   'ErrorCode': {
                                       'DataType': 'Number',
                                       'StringValue': code
                                   }
                               })

        logger.info('Pushed Message: "{}"'.format(msg))
    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500
        }

    return {
        'statusCode': 200,
        'body': json.dumps(msg_text)
    }
