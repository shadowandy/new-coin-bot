import json, time, requests, os, urllib.parse
from pycoingecko import CoinGeckoAPI
from tabulate import tabulate

from config.config import config
from logs import logger


def parsecoin(coin_detail, type='regular'):
    if type == 'header':
        return ('name', 'network', 'categories', 'url', 'homepage', 'Price (USD)', 'Date')
    logger.info(f"Parsing coin - {coin_detail['id']} ({type})")
    id, name, network = coin_detail['id'], coin_detail['name'], coin_detail['asset_platform_id']
    categories = ', '.join(coin_detail['categories'])
    url = f'https://www.coingecko.com/en/coins/' + id
    homepage = coin_detail['links']['homepage'][0]
    price_usd = 0
    try:
        price_usd = coin_detail['market_data']['current_price']['usd']
    except Exception as e:
        logger.error(str(e))
    time_epoch, time_human = int(time.time()), time.strftime('%d-%b-%Y %X %Z')
    if type == 'JSON':
        coin = {}
        coin['id'] = id
        coin['name'] = name
        coin['network'] = network
        coin['categories'] = categories
        coin['url'] = url
        coin['homepage'] = homepage
        #coin['description'] = description
        coin['price'] = price_usd
        coin['epoch'] = time_epoch
        coin['time'] = time_human
        return coin
    else:
        return (name, network, categories, url, homepage, price_usd, time_human)


def telegram_bot_sendtext(bot_message):
    logger.info(f'Sending Telegram message')
    bot_token = config.telegram_token
    bot_chatID = config.telegram_chatid
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def telegram_bot_sendcoin(coin_detail):
    coin = parsecoin(coin_detail, 'JSON')
    description = coin_detail['description']['en']
    trim = int(config.description_trim)
    if len(description) > trim:
        description = description[:trim] + f' ...'
    description = urllib.parse.quote(description)
    message = f"*{coin['name']} ({coin['network']})*\n*Categories:* {coin['categories']}\n\n*Links:* [CoinGecko]({coin['url']}), [Homepage]({coin['homepage']})\n*Price:* US${coin['price']}\n*Desc:* {description}"
    telegram_bot_sendtext(message)


def file_to_json(filename):
    logger.info(f'Loading file to JSON - {filename}')
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(file_name, 'r') as file:
             return json.load(file)
    except IOError as e:
        logger.error(str(e))
        return []


def json_to_file(filename, json_content):
    logger.info(f'Saving JSON to file - {filename}')
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(file_name, 'w') as file:
             json.dump(json_content, file)
    except IOError as e:
        logger.error(str(e))


def main():
    cg = CoinGeckoAPI()
    # Loading previous run data
    logger.info(f'Loading previous data')
    coins_list_old = file_to_json(config.coins_list)

    # Getting the latest data from coingecko
    message = f'Getting new coins listing'
    logger.info(message)
    print(message)

    coins_list_new = []
    cg_coins_list = cg.get_coins_list()
    for coin in cg_coins_list:
        coins_list_new.append({coin['id']:coin['name']})
    coins_list_new = json.loads(json.dumps(coins_list_new, sort_keys=True))

    # Determining if there are differences
    logger.info(f'Identifying differences')
    coins_diff = []
    if coins_list_new != coins_list_old:
        coins_diff = [x for x in coins_list_new + coins_list_old if x not in coins_list_new or x not in coins_list_old]

    # Identifying the differences

    coin_store = []
    coin_table = []

    if len(coins_diff) > 0:
        # Load list of previous "new" coins
        logger.info(f'Loading past identified coins')
        coin_store = file_to_json(config.coins_store)

        new_coins = [id for coin in coins_diff for id in coin]

        for coin_id in new_coins:
            logger.info(f'Identifying new coin - {coin_id}')
            if coin_id not in coin_store:
                coin_detail = cg.get_coin_by_id(coin_id)
                coin_table.append(parsecoin(coin_detail))
                coin_store.append(parsecoin(coin_detail, 'JSON'))
                telegram_bot_sendcoin(coin_detail)
                time.sleep(float(config.delay))

        # Saving it for the next run
        logger.info(f'Saving CoinGecko coins list for next run')
        json_to_file(config.coins_list, coins_list_new)

    if len(coin_table) > 0:
        coin_table.insert(0, parsecoin(None, 'header'))
        print(tabulate(coin_table, headers='firstrow', floatfmt='.5f', showindex='always', tablefmt='grid'))
        logger.info(f'Saving list of new coins')
        json_to_file(config.coins_store, coin_store)
    else:
        message = f'No new coins identified'
        logger.info(message)
        print(message)


if __name__ == "__main__":
    main()
