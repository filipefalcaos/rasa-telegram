from time import sleep
from typing import Text
from rasa_core_sdk import Action


# ActionCallAPI class
# Calls an external API and presents a message to the user
class ActionCallAPI(Action):

    # Action name: action_call
    def name(self) -> Text:
        return 'action_call'

    # Action entry point
    def run(self, dispatcher, tracker, domain):

        # Get the user's message
        # This message should be sent to the external REST API
        message = tracker.latest_message.get('text')
        api_response = self.call_api(message)
        
        # Call the API here and then dispatch a message or return an intent
        dispatcher.utter_message(api_response)

    # Call the API here
    # This method "simulates" a long API call by sleeping for 3 seconds
    # You should handle the API response here and return the message that should be presented to the user
    @staticmethod
    def call_api(user_message):
        sleep(3)
        return 'We do not have an answer for you yet, but we will get back back to you soon ;)'
