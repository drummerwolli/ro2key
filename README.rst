====================================================
IAM-Role based rotatable AWS access key REST Service
====================================================

Ro2Key (Role-based rotatable key) is a REST service to generate AWS ``Temporary Security Credentials`` via AWS STS ``AssumeRole`` API using the `Connexion`_ Python library.

Connexion is a framework on top of Flask_ to automagically handle your REST API requests based on `Swagger 2.0 Specification`_ files in YAML.


Running with Docker
====================

You can build the example application as a Docker image and run it:

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
===================

You can deploy this docker image with `Senza`_ using ``ro2key.yaml``:

.. code-block:: bash

    $ docker build -t pierone.example.org/teamid/ro2key:0.1 .
    $ docker push pierone.example.org/teamid/ro2key:0.1
    $ senza create ro2key.yaml 1 \
                   DockerImage=pierone.example.org/teamid/ro2key:0.1 \
                   ApplicationID=app_id \
                   MintBucket=zalando-stups-mint-123456789-eu-west-1 \
                   ScalyrAccountKey=SOME_SCALYR_KEY \
                   RolesArnPrefix="arn:aws:iam::123456789:role" \
                   TargetRole=S3ReadOnly \
                   AuthURL="https://token.auth.example.org/access_token" \
                   TokenInfoURL="https://auth.example.org/oauth2/tokeninfo" \
                   HostedZone="teamid.example.org." \
                   SSLCertificateId="arn:aws:iam::123456789:server-certificate/example-org"


.. _Connexion: https://pypi.python.org/pypi/connexion
.. _Flask: http://flask.pocoo.org/
.. _Swagger 2.0 Specification: https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md
.. _/ui/: http://localhost:8080/ui/
.. _Senza: https://stups.io/senza/
