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
