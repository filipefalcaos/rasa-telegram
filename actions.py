from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Text
from rasa_core_sdk import Action


# ActionCallAPI class
class ActionCallAPI(Action):

    def name(self) -> Text:
        return 'action_schedule'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Call third party api here")
