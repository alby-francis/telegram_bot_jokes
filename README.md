# telegram_bot_jokes

To start the bot 
Install all required dependencies -
cd Telebot\django-bot-server-tutorial
pip install -r requirements.txt 

Add bot token in chatbot_tutorial/views.py on line 121

Download postgres

Make migration for the db by typing cmd -
python manage.py makemigration
python manage.py migrate

Start the server by cmd -
python manage.py runserver

Download and launch ngrok 
type cmd -
ngrok http 8000
copy the ngrok forwarding url to use for webhook

Set your webhook by sending a 'POST' request to the Telegram API
https://api.telegram.org/bot<bot_token>/setWebhook?url=<ngrok_url>/telebot-joke-impress-ai/

when responase is webhook is set then the bot is ready to intract
