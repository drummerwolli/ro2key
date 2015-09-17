#!/bin/bash

### Make sure you installed following tools
#sudo apt-get install jq python3
#sudo pip3 install awscli

TEST_ROLE=S3BucketReadOnly
APP_URL=http://localhost:8080
OAUTH2_URL=https://auth.example.org/oauth2

### IF BERRY IS RUNNING: do not need to download json here
MINT_PATH=s3://mint_bucket/ro2key
aws s3 cp $MINT_BUCKET/client.json .
aws s3 cp $MINT_BUCKET/user.json .
### IF BERRY IS RUNNING: you should change to berry folder

application_username=$(jq -r .application_username user.json)
application_password=$(jq -r .application_password user.json)
client_id=$(jq -r .client_id client.json)
client_secret=$(jq -r .client_secret client.json)

encoded_scopes="uid"

encoded_application_password=$(python3 -c "import urllib.parse; print(urllib.parse.quote_plus('$application_password'))")

access_token=$(curl -u "$client_id:$client_secret" --silent -d "grant_type=password&username=$application_username&password=$encoded_application_password&scope=$encoded_scopes" $OAUTH2_URL\?realm\=/services | jq .access_token -r)

key=$(curl --insecure --request GET --header "Authorization: Bearer $access_token" $APP_URL/get_key/$TEST_ROLE)

export AWS_ACCESS_KEY_ID=$(echo $key | jq .AccessKeyId -r)
export AWS_SECRET_ACCESS_KEY=$(echo $key | jq .SecretAccessKey -r)
export AWS_SESSION_TOKEN=$(echo $key | jq .SessionToken -r)
export AWS_DEFAULT_REGION="eu-west-1"

###
# now you can use awscli to test your temporary access credential, such as:
# $ aws s3 ls s3://some_bucket/
###
