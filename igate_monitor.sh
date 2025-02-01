#!/bin/bash

# to get chatID /start your new Bot and get API TOKEN than from browser point to
# https://api.telegram.org/botYOUR-API-TOKEN/getUpdates

# insert here your API TOKEN from Telegram/BotFather
API_TOKEN=""
# insert here your CHAT ID
CHAT_ID=""


# new line in telegram
# nl="%0A"

# you need curl
curl -s -X POST https://api.telegram.org/bot$API_TOKEN/sendMessage -d chat_id=$CHAT_ID -d parse_mode="HTML" -d text="$1" > /dev/null
