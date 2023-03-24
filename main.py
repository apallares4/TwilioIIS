import os
from flask import Flask, request, Response, abort
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
import json
import requests
load_dotenv()

app = Flask(__name__)


@app.route('/incoming/sms', methods=['POST'])
def incoming_sms():
    validator = RequestValidator(os.getenv('TWILIO_AUTH_TOKEN'))
    valid = validator.validate(request.url, request.form, request.headers.get('X-Twilio-Signature'))
    if not valid: 
        abort(400)
    
    r = send_github_request(request.form.get('Body'))
    return Response()
    

def send_github_request(message):
    owner = os.getenv('GITHUB_OWNER')
    repo = os.getenv('GITHUB_REPO')
    token = os.getenv('GITHUB_TOKEN')
    authorization_token = f"Bearer {token}"
    headers = { "Accept": "application/vnd.github+json", "Authorization": authorization_token }

    url = f"https://api.github.com/repos/apallares4/smsrep/dispatches"
    payload = {'event_type': 'twilio_sms', 'client_payload': {'message': message }}

    r = requests.post(url, headers=headers, data=json.dumps(payload))

    if r.status_code == 204:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run()
