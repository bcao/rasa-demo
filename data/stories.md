## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## ask for leave
* greet
    - utter_greet
* ask_for_leave
    - leave_form
    - form{"name": "leave_form"}
    - form{"name": null}
* goodbye

## ask for leave 2
* greet
    - utter_greet
* ask_for_leave
    - leave_form
    - form{"name": "leave_form"}
    - form{"name": null}
* affirm
    - utter_goodbye_birthday

## ask for leave 3
* greet
    - utter_greet
* ask_for_leave
    - leave_form
    - form{"name": "leave_form"}
    - form{"name": null}
* goodbye
    - utter_goodbye

## cancel leave
* greet
  - utter_greet
* cancel_leave
  - utter_cancel_leave
* cancel_leave_yes
  - utter_cancel_leave_confirm
* cancel_leave_email_yes
  - utter_cancel_leave_email_done


## ask leave and cancel leave
* greet
    - utter_greet
* ask_for_leave
    - leave_form
    - form{"name": "leave_form"}
    - form{"name": null}
* goodbye
    - utter_goodbye
* cancel_leave
  - utter_cancel_leave
* cancel_leave_yes
  - utter_cancel_leave_confirm
* cancel_leave_email_yes
  - utter_cancel_leave_email_done