import logging
import os

from telegram.ext import (Updater, MessageHandler, Filters)

import ptt
from db import conn

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Command not found.")


def main() -> None:
    """Run the bot."""

    updater = Updater(os.environ["TOKEN"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(ptt.conv_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ["PORT"]),
                          url_path=os.environ["TOKEN"],
                          webhook_url="https://nevikw39-tg-bot.herokuapp.com/" + os.environ["TOKEN"])

    updater.idle()


if __name__ == '__main__':
    main()
    conn.close()
