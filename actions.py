# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Dict, Text, Any, List, Union, Optional
import datetime
from dateutil import relativedelta, parser
import logging
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import Form, AllSlotsReset, SlotSet, Restarted, EventType

logger = logging.getLogger(__name__)


# class CustomFormAction(FormAction):
#     def name(self):
#         return ""

#     def request_next_slot(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: Dict[Text, Any],
#     ) -> Optional[List[EventType]]:
#         """Request the next slot and utter template if needed,
#             else return None"""

#         for slot in self.required_slots(tracker):
#             if self._should_request_slot(tracker, slot):
#                 logger.debug(f"Request next slot '{slot}'")
#                 dispatcher.utter_message(
#                     template=f"utter_ask_{self.name()}_{slot}", **tracker.slots
#                 )
#                 return [SlotSet(REQUESTED_SLOT, slot)]

#         return None


class LeaveForm(FormAction):
    """Leave form..."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "leave_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["start_time", "end_time", "confirm"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "start_time": [
                self.from_entity(entity="DATE")
            ],
            "end_time": [
                self.from_entity(entity="DATE"),
            ],
            "confirm": [
                self.from_intent(value=True, intent="affirm"),
                self.from_intent(value=False, intent="deny"),
            ],
        }

    def submit(self, dispatcher, tracker, domain):
        # start_time = tracker.get_slot("start_time")
        # end_time = tracker.get_slot("end_time")
        if tracker.get_slot("confirm"):
            dispatcher.utter_message(template="utter_goodbye")
            return []
        else:
            dispatcher.utter_message(template="utter_goodbye")
            return [AllSlotsReset()]
