from typing import Text
from rasa_core_sdk import Action


# ActionCallAPI class
class ActionCallAPI(Action):

    def name(self) -> Text:
        return 'action_schedule'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Call third party api here")
