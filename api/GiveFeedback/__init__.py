import json
import jwt
import logging
import os
from azure.cosmos import CosmosClient, PartitionKey
from time import time
from http.cookies import SimpleCookie
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')
  url = 'https://rmc-cosmosdb.documents.azure.com:443/'
  key = os.environ['COSMOS_ACCOUNT_KEY']
  client = CosmosClient(url, credential=key)
  database_name = 'rmc'
  #database = client.create_database(database_name)
  database = client.get_database_client(database_name)
  container_name = 'feedback'
  #container = database.create_container(id=container_name, partition_key=PartitionKey(path="/id"))
  container = database.get_container_client(container_name)

  req_body = req.get_json()
  toId = req_body.get('ToId')

  cookie = SimpleCookie()
  cookie.load(req.headers['Cookie'])
  accessToken = cookie['AccessToken'].value
  decodedAccessToken = jwt.decode(accessToken, os.environ["JWT_ENCODING_SECRET"], algorithms=['HS256'])
  fromId = decodedAccessToken['userId']
  exp = decodedAccessToken['exp']
  nowTime = time()

  if exp < nowTime:
    return func.HttpResponse(
      "Expired token",
      status_code=401
    )

  newFeedback = {
    'id' : f"{fromId}||{toId}",
    'toId' : toId,
    'fromId' : fromId,
    'lastEditDate' : nowTime,
    'createDate' : nowTime,
    'body' : {
      'Technical': int(req_body.get('Technical')),
      'Leadership': int(req_body.get('Leadership')),
      'Communication': int(req_body.get('Communication'))
    }
  }
  container.upsert_item(body=newFeedback)

  return func.HttpResponse(
    "Successfully uploaded feedback.",
    status_code=200
  )
