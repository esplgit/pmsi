import traceback
import requests
import logging
import threading
import time
import json
from telegram import telegram_bot_sendtext
from config import config

isTest = True

appid = config.get('appid')
headers = json.loads(config.get('headers'))
pms_url = config.get('pms_url')
debug = bool(config.get('debug'))
debug1 = bool(config.get('debug1'))

bot_token = config.get('bot_token')
bot_chatID = config.get('bot_chatID')
if isTest:
    bot_token = config.get('test_bot_token')
    bot_chatID = config.get('test_bot_chatID')
sleep10 = float(config.get('sleep10'))
sleep30 = float(config.get('sleep30'))
sleep300 = float(config.get('sleep300'))
# telegram_bot_sendtext("test message! Please ignore", bot_chatID="-416676425")

def worker(args):
    while not args['stop']:
        try:
            res = requests.get(pms_url, headers=headers)
            logging.debug(res.text) if debug else None
            assert res.ok
            time.sleep(30)
        except Exception as e:
            error_code = str(e)
            print(error_code)
            telegram_bot_sendtext("Connection failure to EIS Service", bot_token=bot_token, bot_chatID=bot_chatID)
            time.sleep(sleep300)
            # TODO: check error
            # send tg and email


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    info = {'stop': False}
    thread = threading.Thread(target=worker, args=(info,))
    thread.start()
    while True:
        try:
            logging.debug(f'Appid:{appid}: PMS service Monitor is Working ...') if debug1 else None
            time.sleep(sleep10)
        except KeyboardInterrupt:
            info['stop'] = True
            break
        except Exception as e:
            error_code = str(e)
            print(error_code)
            telegram_bot_sendtext(f"Appid:{appid}: EIC monitoring system failure", bot_token=bot_token, bot_chatID=bot_chatID)
            

    thread.join()
if __name__ == '__main__':
    main()
