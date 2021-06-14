from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext

LIST_OF_ADMINS = {692286133}


def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text(
                "Sorry, but it seems that you have no permission to perform this operation.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped
