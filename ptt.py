import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CMD, LST, ADD, ADD_ARGS, REMOVE, REMOVE_ARGS, QUERY, QUERY_ARGS = range(8)


def ptt(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['add', 'lst', 'remove', 'query']]

    update.message.reply_text(
        'Please choose a subcommand.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )

    return CMD


def cmd(update: Update, context: CallbackContext) -> int:
    return {"add": ADD, "lst": LST, "remove": REMOVE, "query": QUERY}[update.message.text]


def lst(update: Update, context: CallbackContext) -> int:
    try:
        db.cur.execute("SELECT id FROM ptt")
        update.message.reply_text(db.cur.fetchall())
    except Exception as e:
        update.message.reply_text(e)

    return ConversationHandler.END


def add(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please input ids.')

    return ADD_ARGS


def add_args(update: Update, context: CallbackContext) -> int:
    try:
        for id in update.message.text.split('\n'):
            db.cur.execute(f"INSERT INTO ptt VALUES ({id})")
        db.conn.commit()
        update.message.reply_text("Succesfully added.")
    except Exception as e:
        update.message.reply_text(e)

    return ConversationHandler.END


def remove(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please input ids.')

    return ADD_ARGS


def remove_args(update: Update, context: CallbackContext) -> int:
    try:
        for id in update.message.text.split('\n'):
            db.cur.execute(f"DELETE FROM ptt WHERE id = {id}")
        db.conn.commit()
        update.message.reply_text("Succesfully added.")
    except Exception as e:
        update.message.reply_text(e)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END


db.cur.execute("CREATE TABLE IF NOT EXISTS ptt (id text PRIMARY KEY)")
db.conn.commit()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ptt', ptt)],
    states={
        CMD: [MessageHandler(Filters.regex('^(add|lst|remove|query)$'), cmd)],
        LST: [MessageHandler(Filters.text, lst)],
        ADD: [MessageHandler(Filters.text, add)],
        ADD_ARGS: [MessageHandler(Filters.text, add_args)],
        REMOVE: [MessageHandler(Filters.text, remove)],
        REMOVE_ARGS: [MessageHandler(Filters.text, remove_args)],
        # QUERY: [MessageHandler(Filters.text, query)],
        # QUERY_ARGS: [MessageHandler(Filters.text, query_args)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
