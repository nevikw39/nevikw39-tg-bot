import logging

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler)

from restricted import restricted

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

RESULT, = range(1)


def eval(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please input experssion to evaluate.\n/cancel to end conversation.')

    return RESULT


@restricted
def result(update: Update, context: CallbackContext) -> int:
    try:
        update.message.reply_text(str(eval(update.message.text)))
    except Exception as e:
        update.message.reply_text(str(e))
        logger.error(e)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('End of Conversation.')
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('eval', eval)],
    states={
        RESULT: [MessageHandler(Filters.text, result)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
