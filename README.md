# telegram_bot_jokes

To start the bot 
add bot token in chatbot_tutorial/views.py

download and launch ngrok 
type cmd 
ngrok http 8000

Set your webhook by sending a 'POST' request to the Telegram API
https://api.telegram.org/bot<bot_token>/setWebhook?url=<ngrok_url>/telebot-joke-impress-ai/

when responase is webhook is set then bot is ready to intract
