#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram.ext import Updater

import ptt
import db

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""

    updater = Updater(os.environ["TOKEN"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(ptt.conv_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ["PORT"]),
                          url_path=os.environ["TOKEN"],
                          webhook_url="https://nevikw39-tg-bot.herokuapp.com/" + os.environ["TOKEN"])

    updater.idle()


if __name__ == '__main__':
    main()
    db.cur.close()
    db.conn.close()
