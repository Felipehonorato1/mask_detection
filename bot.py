from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
)
import logging


class Bot:
    def __init__(self):
        self.registered_chats = []
        self.updater = None
        self.init_bot()

    def init_bot(self):
        updater = Updater(token="2121563163:AAFfR67OdkZnbsnlIKoi_WMSMcBXm_OvcyE")
        dispatcher = updater.dispatcher

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

        start_handler = CommandHandler("start", self.start)
        dispatcher.add_handler(start_handler)
        register_handler = CommandHandler("register", self.register)
        dispatcher.add_handler(register_handler)

        updater.start_polling()
        updater.idle()

        self.updater = updater

    def start(self, update: Update, context: CallbackContext):
        response = "Oi!"

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def register(self, update: Update, context: CallbackContext):
        chat = update.effective_chat.id

        self.registered_chats.append(chat)
        context.bot.send_message(chat_id=chat, text="Registrado com sucesso!")
        print(self.registered_chats)


def main():
    bot = Bot()


if __name__ == "__main__":
    main()
