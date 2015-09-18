====================================================
IAM-Role based rotatable AWS access key REST Service
====================================================

Ro2Key: Role-based rotatable key (role to key) is a REST service to generate AWS ``Temporary Security Credentials`` by AWS STS ``AssumeRole`` API using the `Connexion`_ Python library.

``Ro2Key`` is designed to enable the access of AWS resources from ``robot users`` in a secure way under `STUPS`_ framework, it generates a ``Temporary Security Credentials`` by HTTPS call when the caller provides a valid OAuth2 token, and send the credentials back as a JSON string.


When should I use it
====================

Normally you should not generate ``Temporary Security Credentials`` to external robot users, you should implement one or more STUPS-appliance as HTTPS-proxy to call AWS APIs (to execute the AWS operations).

But for some use case, such as syncing bunch of data between two locations, a HTTPS-proxy between each other will be a huge bottleneck and brings a lot of problems, such as latency, incomplete data transfer or handling any other kind of error by transferring huge amount of data.

Such as:

- Use Case 1: sync a lot of huge files between external data center and AWS S3 periodically by robot user (as for example cron job, not manully by human user with `Mai`_)

  - you can run ``Ro2Key`` on your AWS S3's account, with IAM role that has Get*/Put* permissions on target buckets

* Use Case 2: sync buckets with a lot of huge files between different AWS accounts periodically by robot user (as for example cron job, not manully by human user with `Mai`_)

  - you can run ``Ro2Key`` on one of your AWS account, with IAM role that has Get*/Put* permissions on target buckets

Then you can run a script as cron job or with any other job scheduling tools, and use AWS CLI or call AWS APIs to transfer data directly from the data source.


Running with Docker
===================

Note that AWS STS ``AssumeRole`` API is only able to be called from an EC2 instance with delegated IAM role, that means to run a functional test you need to deploy this application on an AWS EC2 instance, by local test you can only check if the application is running successfully within the docker container, but you will not be able to get AWS ``Temporary Security Credentials`` by AWS STS ``AssumeRole`` API.

So we suggest you build the Docker image from Dockerfile and run it on an EC2 instance with delegated IAM role, named for example ``S3MintReadOnly``:

.. code-block:: bash

    $ docker build -t ro2key .
    $ docker run -d \
                 -e AUTH_URL=https://token.auth.example.org/access_token \
                 -e TOKENINFO_URL=https://auth.example.org/oauth2/tokeninfo \
                 -e ARN_PREFIX=arn:aws:iam::123456789:role \
                 -p 8080:8080 \
                 ro2key
    $ ./how_to_use.sh # chage the variables to your settings


Deploying with Senza
====================

At first create an ``IAM role`` with delegate permissions, in following example we will create an IAM role with ReadOnly permission on S3 Mint Bucket.

The name of IAM role is ``S3MintReadOnly``.

.. code-block:: bash

    $ DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    $ aws iam create-role --role-name S3MintReadOnly --assume-role-policy-document file://$DIR/policy_trust.json
    $ aws iam put-role-policy --role-name S3MintReadOnly --policy-name MintBucketReadOnly --policy-document file://$DIR/policy_bucket_readonly.json ### change the ARN of mint bucket in policy_bucket_readonly.json to yours
    $ aws iam put-role-policy --role-name S3MintReadOnly --policy-name AssumeRoleByItSelf --policy-document file://$DIR/policy_assumerole.json ### change the ARN of role in policy_assumerole.json if you changed the role name


Then you can deploy this docker image on AWS EC2 instances with `Senza`_ using ``ro2key.yaml``, note that you must deploy this appliance with that IAM role which you want to generate the ``Temporary Security Credentials`` with, here we take the IAM role ``S3MintReadOnly`` which was created from above example.

.. code-block:: bash

    $ docker build -t pierone.example.org/teamid/ro2key:0.1 .
    $ docker push pierone.example.org/teamid/ro2key:0.1
    $ senza create ro2key.yaml 1 \
                   DockerImage=pierone.example.org/teamid/ro2key:0.1 \
                   ApplicationID=app_id \
                   MintBucket=mint-123456789-eu-west-1 \
                   ScalyrAccountKey=SOME_SCALYR_KEY \
                   RolesArnPrefix="arn:aws:iam::123456789:role" \
                   TargetRole=S3MintReadOnly \
                   AuthURL="https://token.auth.example.org/access_token" \
                   TokenInfoURL="https://auth.example.org/oauth2/tokeninfo" \
                   HostedZone="teamid.example.org." \
                   SSLCertificateId="arn:aws:iam::123456789:server-certificate/example-org"

Now you can get a ``Temporary Security Credentials`` for the IAM role ``S3MintReadOnly`` by REST call:

.. code-block:: bash

    $ curl --insecure --request GET --header "Authorization: Bearer YOUR_OAUTH2_TOKEN" https://ro2key.teamid.example.org/get_key/S3MintReadOnly

The file ``how_to_use.sh`` gives you an example how to use the credentials from S3 Mint Bucket or from `Berry`_ to get the temporary access keys with HTTP calls.

.. _Connexion: https://pypi.python.org/pypi/connexion
.. _STUPS: https://stups.io/
.. _Mai: https://stups.io/mai/
.. _Senza: https://stups.io/senza/
.. _Berry: https://stups.io/berry/
