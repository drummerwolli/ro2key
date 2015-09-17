#!/usr/bin/env python3
import connexion
import logging
import os
import string
import random
import boto3

client = boto3.client('sts')
arn_prefix = os.environ.get('ARN_PREFIX')


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_key(role_name):
    try:
        response = client.assume_role(
            RoleArn=arn_prefix + "/" + role_name,
            RoleSessionName=id_generator()
        )
        key = {}
        key['AccessKeyId'] = response['Credentials']['AccessKeyId']
        key['SecretAccessKey'] = response['Credentials']['SecretAccessKey']
        key['SessionToken'] = response['Credentials']['SessionToken']
        return key
    except:
        return 'Access Denied', 403


logging.basicConfig(level=logging.INFO)
api_args = {'auth_url': os.environ.get('AUTH_URL'), 'tokeninfo_url': os.environ.get('TOKENINFO_URL')}
app = connexion.App(__name__, port=8080, debug=True, server='gevent')
app.add_api('swagger.yaml', arguments=api_args)
application = app.app

if __name__ == '__main__':
    app.run()
