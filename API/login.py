import os
import shutil
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re

def login(url, username, password, session=None):
	if session is None:
		session = requests.Session()

	url = re.sub(r'(https?://[^/]+)(/.*)', r'\1', url)

	print(f'Logging in to {url} as {username}...')

	url = f'{url}/login?do_login'

	data = MultipartEncoder(
		fields=
			{
				'post-type': 'login',
				'username': username,
				'password': password
			}
	)

	response = session.post(url, data=data.to_string(), headers={'Content-Type': data.content_type})

	print(response, response.status_code, response.reason, response.url)

	return session

def get_data(url, session):
	url = re.sub(r'(https?://[^/]+)(/.*)', r'\1', url)

	print(f'Getting data from {url}...')

	url = f'{url}/dl_data'

	response = session.get(url)

	return response



if __name__ == '__main__':
	# check for cli arguments
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', 
						help='URL of the API', 
						default='http://127.0.0.1:45454',
						# required=False
						)
	parser.add_argument('--username', 
						help='Username', 
						default='Test_user',
						# required=False
						)
	parser.add_argument('--password', 
						help='Password', 
						default='TEST',
						# required=False
						)

	args = parser.parse_args()

	URL = args.url
	username = args.username
	password = args.password

	session = login(URL, username, password)

	dl_data = get_data(URL, session)
	# get filename from headers
	filename = dl_data.headers['Content-Disposition'].split('=', 1)[-1]
	if filename[0] == '"':
		filename = filename[1:-1]

	with open(filename, 'wb') as f:
		f.write(dl_data.content)


	# extract in folder with same name
	import zipfile
	os.makedirs("Backup/" + filename.split('.')[0], exist_ok=True)
	with zipfile.ZipFile(filename, 'r') as zip_ref:
		zip_ref.extractall(filename.split('.')[0])

	# delete the zip file and temp folder inside it
	os.remove(filename)
	shutil.rmtree(filename.split('.')[0] + "/temp")