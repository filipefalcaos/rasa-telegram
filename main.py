from subprocess import Popen, call, DEVNULL
import argparse
import time

# Requests HTTP lib
import requests

# Flask server imports
from flask import Flask
from flask import request
from flask import Response

# RASA core imports
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig


# Telegram bot API base url
BASE_URL = 'https://api.telegram.org/bot'

# Create a new CLI parser
parser = argparse.ArgumentParser(description='RASA integration with Telegram')
parser.add_argument('--token', type=str, help='Telegram API bot token')

# Parse input args
args = parser.parse_args()

# Inits Flask
app = Flask(__name__)


# Accept Telegram messages
# The '/' route receives the POST and GET requests from Telegram
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        # Get message data
        msg = request.get_json()
        chat_id, message = parse_msg(msg)

        # Get RASA response and send through the API
        response_messages = rasa_response(message)
        send_message(chat_id, response_messages)

        return Response('OK', status=200)
    else:
        return 'Hello!'


# Extract the chat id and text from a given message
# Returns both values
def parse_msg(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    return chat_id, txt


# Send message through the Telegram API
def send_message(chat_id, messages=None):
    url = BASE_URL + args.token + '/sendMessage'

    if messages is None:
        messages = []

    # RASA responded
    # Sent the messages through the Telegram API
    if messages:
        for message in messages:
            payload = {'chat_id': chat_id, 'text': message}
            requests.post(url, json=payload)

    return True


# Get response using RASA
def rasa_response(message):

    # Get RASA responses for a given message
    responses = agent.handle_message(message)
    text = []

    # RASA responded
    if responses:
        for response in responses:
            text.append(response['text'])

    return text


# Load trained models
# Returns the agent created based on the trained models
def rasa_config():

    # Set the actions endpoint
    action_endpoint = EndpointConfig(url='http://localhost:5055/webhook')

    # Load the trained RASA models
    interpreter = RasaNLUInterpreter('./models/rasa-telegram-app/nlu')
    return Agent.load('./models/rasa-telegram-app/core', interpreter=interpreter, action_endpoint=action_endpoint)


# Sets the Ngrok configuration
# Starts Ngrok and sets a new tunnel to Telegram
def ngrok_config():

    # Kill running Ngrok processes
    command = 'pkill ngrok'
    call(command, shell=True)

    # Spawn a new Ngrok process
    command = 'ngrok http 5000'
    Popen(command, shell=True, stderr=DEVNULL, stdout=DEVNULL)

    # Get the list of HTTP tunnels
    while True:
        time.sleep(1)
        r = requests.get('http://localhost:4040/api/tunnels')
        r = r.json()
        tunnels = r['tunnels']

        # Ngrok successfully set the tunnels
        if len(tunnels) > 0:
            break

    # Get the current tunnel
    curr_tunnel = tunnels[0]['public_url']

    # Set the tunnel to Telegram
    tunnel_url = BASE_URL + args.token + '/setWebhook?url=' + curr_tunnel
    requests.get(tunnel_url)


# Entry point
if __name__ == '__main__':

    # Load RASA models
    print('Loading RASA models...')
    agent = rasa_config()

    # Setup Ngrok and Flask
    print('\nStarting the Flask server...')
    ngrok_config()
    app.run()
