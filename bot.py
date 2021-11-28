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

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("register", self.register))
        dispatcher.add_handler(CommandHandler("unregister", self.unregister))
        dispatcher.add_handler(CommandHandler("help", self.help))
        dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

        self.updater = updater
        updater.start_polling()
        updater.idle()

    def start(self, update: Update, context: CallbackContext):
        # TODO mensagem mais explicativa
        response = "Oi!"

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def register(self, update: Update, context: CallbackContext):
        chat = update.effective_chat.id

        if chat not in self.registered_chats:
            self.registered_chats.append(chat)
        context.bot.send_message(chat_id=chat, text="Registrado com sucesso!")

    def unregister(self, update: Update, context: CallbackContext):
        chat = update.effective_chat.id

        self.registered_chats.remove(chat)
        context.bot.send_message(chat_id=chat, text="Removido do registro.")

    def help(self, update: Update, context: CallbackContext):
        # TODO mensagem
        response = "Mensagem explicando a usar o bot."

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def unknown(self, update: Update, context: CallbackContext):
        response = "Desculpe, não sei como te ajudar. Tente /help."

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


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
