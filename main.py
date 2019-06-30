import argparse

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
from rasa_core.channels.telegram import TelegramOutput


# Telegram bot API base url
BASE_URL = 'https://api.telegram.org/bot'

# Current Telegram chat
current_chat = None

# Inits Flask
app = Flask(__name__)

# Create a new CLI parser
parser = argparse.ArgumentParser(description='RASA integration with Telegram')
parser.add_argument('--token', type=str, help='Telegram API bot token')
parser.add_argument('--tunnel', type=str, help='URL for the Ngrok tunnel')

# Parse input args
args = parser.parse_args()


# Accept Telegram messages
# The '/' route receives the POST and GET requests from Telegram
@app.route('/', methods=['POST', 'GET'])
def index():
    global current_chat

    if request.method == 'POST':

        # Get message data
        msg = request.get_json()
        chat_id, message = parse_msg(msg)
        current_chat = chat_id

        # Get RASA response and send through the API
        response_messages = rasa_response(message)
        send_message(chat_id, response_messages)

        # Set the message to be returned
        return Response('OK', status=200)
    else:
        return 'Hello!'


# Accept info messages from a client
# The '/info' route receives the POST request from an external server
@app.route('/info', methods=['POST'])
def info():
    messages = []
    chat_id = current_chat

    # Get message data
    r = request.get_json()
    response_data = r['response']
    messages.append(response_data)

    # Create a Telegram response
    telegram_output = TelegramOutput(access_token=args.token)

    for message in messages:
        telegram_output.send_message(chat_id=chat_id, text=message)

    return Response('OK', status=200)


# Extract the chat id and text from a given message
# Returns both values
def parse_msg(message):
    global current_chat
    current_chat = message['message']['chat']['id']
    txt = message['message']['text']
    return current_chat, txt


# Send message through the Telegram API
def send_message(chat_id, messages=None):
    telegram_output = TelegramOutput(access_token=args.token)

    if messages is None:
        messages = []

    # RASA responded
    # Sent the messages through the Telegram API
    if messages:
        for message in messages:
            telegram_output.send_message(chat_id=chat_id, text=message)

    return True


# Get response using RASA
# The handle_message method is responsible for processing the message
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

    # Set the tunnel to Telegram
    tunnel_url = BASE_URL + args.token + '/setWebhook?url=' + args.tunnel
    r = requests.get(tunnel_url)
    print('Telegram Webhook: ' + r.json()['description'])


# Entry point
if __name__ == '__main__':

    # Load RASA models
    print('Loading RASA models...')
    agent = rasa_config()

    # Setup Ngrok
    print('\nSetting the Telegram Ngrok webhook...')
    ngrok_config()

    # Setup Flask
    print('\nStarting the Flask server...')
    app.run()
