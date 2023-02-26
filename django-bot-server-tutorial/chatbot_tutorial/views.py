import json
import random

import requests
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .models import CountJokeModel
from .serializers import CountJokeSerializer

def get_message_from_request(request):

    received_message = {}
    decoded_request = json.loads(request.body.decode('utf-8'))

    if 'message' in decoded_request:
        received_message = decoded_request['message'] 
        received_message['chat_id'] = received_message['from']['id'] # simply for easier reference

    return received_message


def send_messages(message, token):
    # Ideally process message in some way. For now, let's just respond
    jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""THis is fun""",
                    """THis isn't fun"""] 
    }
    joke_title = []
    for key in jokes:
        joke_title.append(key)

    keyboard = [joke_title]
    reply_markup = {"keyboard" : keyboard}

    post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)

    result_message = {}         # the response needs to contain just a chat_id and text field for  telegram to accept it
    result_message['chat_id'] = message['chat_id']
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
        result_message['reply_markup'] = reply_markup
        joke = 'fat'

    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
        result_message['reply_markup'] = reply_markup
        joke = 'stupid'

    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])
        result_message['reply_markup'] = reply_markup
        joke = 'dumb'
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
        result_message['reply_markup'] = reply_markup

    count = 1
    db_joke_var = str(joke) + "_count"
    cjm = CountJokeModel.objects.filter(user_chat_id=message['chat_id']).first()
    raw_data = {'user_chat_id' : message['chat_id'],
                'user_id' : message['from']['id'],
                'first_name' : message['from']['first_name'],
                }
    
    if cjm:
        raw_data['fat_count'] = cjm.fat_count
        raw_data['dumb_count'] = cjm.dumb_count
        raw_data['stupid_count'] = cjm.stupid_count
        if db_joke_var == "fat_count":
            count += cjm.fat_count
        elif db_joke_var == "dumb_count":
            count += cjm.dumb_count
        elif db_joke_var == "stupid_count":
            count+= cjm.stupid_count
        
        raw_data[db_joke_var] = count
        cjm = CountJokeSerializer(cjm, data = raw_data)
        if cjm.is_valid():
            cjm.save()
            print("sucess")
        else:
            print("error saving in db")
            print(cjm.errors)
            
    else:
        raw_data['fat_count'] = 0
        raw_data['dumb_count'] = 0
        raw_data['stupid_count'] = 0
        raw_data[db_joke_var] = count
        cjm = CountJokeSerializer(data = raw_data)

        if cjm.is_valid():
            cjm.save()
            print("sucess")
        else:
            print("error saving in db")
            print(cjm.errors)
            
    response_msg = json.dumps(result_message)
    status = requests.post(post_message_url, headers={
        "Content-Type": "application/json"}, data=response_msg)


class TelegramBotView(generic.View):

    # csrf_exempt is necessary because the request comes from the Telegram server.
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    # Post function to handle messages in whatever format they come
    def post(self, request, *args, **kwargs):
        TELEGRAM_TOKEN = '<telegram-bot-token>'
        message = get_message_from_request(request)
        send_messages(message, TELEGRAM_TOKEN)
        return HttpResponse()
    
    def get(self, *args, **kwargs):
        return HttpResponse()

