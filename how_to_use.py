import boto3
import json
import requests

### Make sure you installed following tools
#sudo apt-get install python3
#sudo pip3 install boto3 requests 

encoded_scopes = 'uid'



def get_token():
	boto3.setup_default_session(profile_name='default')
	client = boto3.client('s3')
	transfer = boto3.s3.transfer.S3Transfer(client)
	transfer.download_file('mint_bucket', "ro2key/client.json", "./client.json")
	transfer.download_file('mint_bucket', 'ro2key/user.json', './user.json')


	with open('./user.json', 'r') as f:
	    r = f.read()
	    jsonFile = json.loads(r)
	    application_username = jsonFile['application_username']
	    application_password = jsonFile['application_password']

	with open('./client.json', 'r') as f:
		r = f.read()
		jsonFile = json.loads(r)
		client_id = jsonFile['client_id']
		client_secret = jsonFile['client_secret']    



	data = {"grant_type": "password", "username": application_username, "password": application_password, "scope": encoded_scopes}
	url = 'https://auth.example.org/oauth2?realm=services'
	req = requests.post(url, data=data, auth=(client_id, client_secret))

	response = json.loads(req.text)
	return response['access_token']



def get_credentials(access_token):
	headers = {
	    'Authorization': 'Bearer {0}'.format(access_token)
	}

	#url where ro2key is running
	url = 'http://localhost:8080/get_key/S3BucketReadOnly'

	req = requests.get(url, headers=headers)
	return req.text

#Usage
print(get_credentials(get_token()))
