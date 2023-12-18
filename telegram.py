import requests
from config import config
test_bot_token = config.get('test_bot_token')
test_bot_chatID = config.get('test_bot_chatID')


def telegram_bot_sendtext(bot_message, parse_mode='Markdown',
                          bot_token=test_bot_token, bot_chatID=test_bot_chatID, debug=True):
    send_text = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=%s&text=%s' % (
        bot_token, bot_chatID, parse_mode, bot_message)
    response = requests.get(send_text)
    # msg = response.json()
    print(response.text) if debug else None
    

if __name__ == '__main__':
    telegram_bot_sendtext('test msg. pls ignore')
