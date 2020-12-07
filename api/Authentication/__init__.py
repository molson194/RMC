import logging
import os
import requests
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    code = req.params.get('code')
    print(code)
    payload = {'grant_type': 'authorization_code', 'code': code, 'client_id':'863gl16an25sq9', 'client_secret':os.environ["LINKEDIN_CLIENT_SECRET"], 'redirect_uri':os.environ["LINKEDIN_REDIRECT_URI"]}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post("https://www.linkedin.com/oauth/v2/accessToken", headers=headers, data=payload)
    print(r.content)
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
