from time import sleep
from yolo_interface import check_masked
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
)
import threading


class Bot:
    def __init__(self):
        self.registered_chats = []
        self.updater = None

    def run(self):
        updater = Updater(token="2121563163:AAFfR67OdkZnbsnlIKoi_WMSMcBXm_OvcyE")
        dispatcher = updater.dispatcher

        start_handler = CommandHandler("start", self.start)
        dispatcher.add_handler(start_handler)
        register_handler = CommandHandler("register", self.register)
        dispatcher.add_handler(register_handler)

        self.updater = updater
        updater.start_polling()
        updater.idle()

    def start(self, update: Update, context: CallbackContext):
        response = "Oi!"

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def register(self, update: Update, context: CallbackContext):
        chat = update.effective_chat.id

        self.registered_chats.append(chat)
        context.bot.send_message(chat_id=chat, text="Registrado com sucesso!")


def init_watcher(bot: Bot):
    try:
        while True:
            found, msg = check_masked()

            if found:
                for chat in bot.registered_chats:
                    if bot.updater is None:
                        continue

                    bot.updater.bot.send_message(chat_id=chat, text=msg)
            
            sleep(3)

    except KeyboardInterrupt:
        return


def main():
    bot = Bot()
    watcher_thread = threading.Thread(target=init_watcher, args=(bot,), daemon=True)
    watcher_thread.start()
    bot.run()


if __name__ == "__main__":
    main()
