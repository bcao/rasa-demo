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
import time
import asyncio
from dateutil import relativedelta, parser
import logging
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction #, REQUESTED_SLOT
from rasa_sdk.events import Form, AllSlotsReset, SlotSet, Restarted, EventType
from rasa_sdk.events import ReminderScheduled, ReminderCancelled

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

class ActionCancelLeave(Action):
    def name(self):
        return "action_cancel_leave"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_cancel_leave")
        return [AllSlotsReset()]

class ActionCancelLeaveEmailYes(Action):
    def name(self):
        return "action_cancel_leave_email_yes"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_cancel_leave_email_done")

        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EMAIL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )
        # await asyncio.sleep(5)
        # dispatcher.utter_message(template="utter_email_done")

        return [reminder]

class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_email_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_email_done")

        return []


class LeaveForm(FormAction):
    """Leave form..."""

    birthday = True

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "leave_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["leave_type", "start_time", "end_time", "confirm"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "start_time": [
                self.from_entity(entity="DATE"),
                self.from_entity(entity="start_time")
            ],
            "end_time": [
                self.from_entity(entity="DATE"),
                self.from_entity(entity="end_time")
            ],
            "confirm": [
                self.from_intent(value=True, intent="affirm"),
                self.from_intent(value=False, intent="deny"),
            ],
        }

    def submit(self, dispatcher, tracker, domain):
        if tracker.get_slot("confirm"):
            if self.birthday:
                dispatcher.utter_message(template="utter_ticket_created")
                #dispatcher.utter_message(template="utter_goodbye_birthday")
                #self.birthday = False
            else:
                dispatcher.utter_message(template="utter_ticket_created")
            SlotSet("confirm", None)
            return [AllSlotsReset()]
        else:
            dispatcher.utter_message(template="utter_goodbye")
            self.birthday = True
            return [AllSlotsReset()]

class ActionRestarted(Action): 	
    def name(self): 		
        return 'action_restarted' 	
    def run(self, dispatcher, tracker, domain): 
        return[Restarted()] 

class ActionSlotReset(Action): 	
    def name(self): 		
        return 'action_slot_reset' 	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]