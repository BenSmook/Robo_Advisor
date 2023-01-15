from datetime import datetime
from dateutil.relativedelta import relativedelta


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }



def get_slots(intent_request):
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response




def recommend_portfolio(intent_request):
    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

def validate_age(age,intent_request):
    if not isinstance(age, int):
        return build_validation_result(
            False,
            "age",
            "Age should be a number, please try again.",
        )
    if age < 0:
        return build_validation_result(
            False,
            "age",
            "Newborns shouldn't be worried about retirement",
        )
    elif age >= 65:
        return build_validation_result(
            False,
            "age",
            "Sorry, should've thought about retirement a long time ago"
        )
    return build_validation_result(True, None, None)

def validate_investment(investmentAmount, intent_request):
    if investmentAmount is not None:
        investmentAmount = parse_int(investmentAmount)
        if investmentAmount < 5000:
            return build_validation_result(
                False,
                "investmentAmount",
                "Amount attempted to be invested is to low."
                "Investments must be more than $5000.")
    return build_validation_result(True, none, none)

def recommend_portfolio:
     if riskLevel == 'none':
            recommendation = "100% bonds (AGG), 0% equities (SPY)"
        elif riskLevel == 'low':
            recommendation = "60% bonds (AGG), 40% equities (SPY)"
        elif riskLevel == "medium":
            recommendation = "40% bonds (AGG), 60% equities (SPY)"
        elif riskLevel == 'high': 
            recommendation = "20% bonds (AGG), 80% equities (SPY)"
        else:
            recommendation = "Please check your risk_level and start again"
        return recommendation




def dispatch(intent_request):
    tent_name = intent_request["currentIntent"]["name"]

   
    if intent_name == "recommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")



def lambda_handler(event, context):
    return dispatch(event)