import json
import jwt
import logging
import os
import requests
from azure.cosmos import CosmosClient, PartitionKey
import azure.functions as func
from time import time


def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  # Get token from request params
  token = req.params.get('token')
  print(token)

  # Get access token from linked in
  payload = {'grant_type': 'authorization_code', 'code': token, 'client_id':'863gl16an25sq9', 'client_secret':os.environ["LINKEDIN_CLIENT_SECRET"], 'redirect_uri':os.environ["LINKEDIN_REDIRECT_URI"]}
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  r = requests.post("https://www.linkedin.com/oauth/v2/accessToken", headers=headers, data=payload)
  print(r.text)
  j = json.loads(r.text)
  linkedInToken = j['access_token']

  # Get email for user
  headers = {"Authorization": "Bearer " + linkedInToken}
  r = requests.get("https://api.linkedin.com/v2/clientAwareMemberHandles?q=members&projection=(elements*(primary,type,handle~))", headers=headers)
  print(r.text)
  j = json.loads(r.text)
  email = j['elements'][0]['handle~']['emailAddress']
  print(email)

  # Get UID, name
  r = requests.get("https://api.linkedin.com/v2/me", headers=headers)
  print(r.text)
  j = json.loads(r.text)
  firstName = j['localizedFirstName']
  lastName = j['localizedLastName']
  userId = j['id']
  print(firstName + " " + lastName + " " + userId)

  # Create access/refresh JWT with expiration (as string)
  accessToken = jwt.encode({
      'userId': userId,
      'exp': time() + 5000000
    }, os.environ["JWT_ENCODING_SECRET"], algorithm='HS256').decode()

  # Store/Update user
  url = 'https://rmc-cosmosdb.documents.azure.com:443/'
  key = os.environ['COSMOS_ACCOUNT_KEY']
  client = CosmosClient(url, credential=key)
  database_name = 'rmc'
  #database = client.create_database(database_name)
  database = client.get_database_client(database_name)
  container_name = 'users'
  #container = database.create_container(id=container_name, partition_key=PartitionKey(path="/id"))
  container = database.get_container_client(container_name)
  
  user = {
    'id' : userId,
    'firstName' : firstName,
    'lastName' : lastName,
    'linkedInToken' : linkedInToken,
    'email' : email
  }
  container.upsert_item(body=user)

  # Return JWT
  return func.HttpResponse(
    "Login Successful",
    status_code=200,
      headers={
        'Set-Cookie': f"AccessToken={accessToken}; HttpOnly; Path=/; Max-Age=5000000; SameSite=Strict" # TODO: Secure;
      }
  )
