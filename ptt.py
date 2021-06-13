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
import restricted

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CMD, ADD, REMOVE, QUERY = range(4)


def ptt(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['add', 'lst', 'remove']]

    update.message.reply_text(
        'Please choose a subcommand.'
        '/cancel to end conversation.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )

    return CMD


def cmd(update: Update, context: CallbackContext) -> int:
    if update.message.text == "lst":
        try:
            db.cur.execute("SELECT id FROM ptt")
            update.message.reply_text(
                '\n'.join([i[0] for i in db.cur.fetchall()]),
                reply_markup=ReplyKeyboardRemove(),)
        except Exception as e:
            db.conn.rollback()
            update.message.reply_text(str(e),
                                      reply_markup=ReplyKeyboardRemove(),)

        return ConversationHandler.END
    elif update.message.text == "add":
        update.message.reply_text(
            'Please input ids.\n/cancel to end conversation.',
            reply_markup=ReplyKeyboardRemove(),)
        return ADD
    elif update.message.text == "remove":
        update.message.reply_text(
            'Please input ids.\n/cancel to end conversation.',
            reply_markup=ReplyKeyboardRemove(),)
        return REMOVE


@restricted.restricted
def add(update: Update, context: CallbackContext) -> int:
    try:
        db.cur.executemany("INSERT INTO ptt (id) VALUES (%s)", [
                           (i.strip(),) for i in update.message.text.split('\n')])
        db.conn.commit()
        update.message.reply_text("Succesfully added.")
    except Exception as e:
        db.conn.rollback()
        update.message.reply_text(str(e))

    return ConversationHandler.END


@restricted.restricted
def remove(update: Update, context: CallbackContext) -> int:
    try:
        db.cur.executemany("DELETE FROM ptt WHERE id = %s", [
                           (i.strip(),) for i in update.message.text.split('\n')])
        db.conn.commit()
        update.message.reply_text("Succesfully removed.")
    except Exception as e:
        db.conn.rollback()
        update.message.reply_text(str(e))

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END


db.cur.execute("CREATE TABLE IF NOT EXISTS ptt (id text PRIMARY KEY)")
db.conn.commit()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ptt', ptt)],
    states={
        CMD: [MessageHandler(Filters.regex('^(add|lst|remove|query)$'), cmd)],
        ADD: [MessageHandler(Filters.text, add)],
        REMOVE: [MessageHandler(Filters.text, remove)],
        # QUERY: [MessageHandler(Filters.text, query)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
