# New Coin Bot

Monitors for newly coins or tokens listed on CoinGecko and pushes out via Telegram and/or command line.

# Installation

## Download

```
git clone https://github.com/shadowandy/new-coin-bot.git ~/new-coin-bot
```

## Install Python dependencies

```
pip3 install -r requirements.txt
```

# Running it

## Configuration.cfg

In order to use Telegram notification, you will have to sign up for a Telegram bot. You can easily Google for the instructions to do so. You will need to identify the chatid for the Telegram bot to push updates to.

To start configuring the bot

```
cd ~/new-coin-bot
nano configuration.cfg
```

Within the `configuration.cfg`, paste the following contents and edit it to reflect your desired settings.

```cfg
[base]
console_logs             : false
logs_file                : run.log
coins_list               : db_coinslist.json
coins_store              : db_coinstore.json
delay                    : 0.5
refresh_interval_minutes : 10
save_interval_minutes    : 30

[telegram]
enable_telegram          : false
token                    : <telegram_bot_token>
chatid                   : <telegram chat_id>
description_trim         : 1000
```

## Running the bot

Once everything is configured. You can simply trigger the bot to run by using the following command.

```
python3 main.py
```

To run it periodically, you will have to make use of scheduler like crontab. For example, running at the 6th, 26th and 46th minute of the hour. You can do the following:

```
6,26,46 * * * * /usr/bin/python3 /home/<username>/new-coin-bot/main.py 2>&1
```
