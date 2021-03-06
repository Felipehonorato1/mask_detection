from pathlib import Path
from time import sleep
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
)
import yolo_interface
import threading
import logging
import argparse


class Bot:
    def __init__(self):
        # List of telegram users registered to receive notifications
        self.registered_chats = []
        # Object which allows control of bot
        self.updater = None

    def run(self, token: str):
        # Wrappers for telegram API
        updater = Updater(token=token)
        dispatcher = updater.dispatcher

        # Set up basic logging (prints bot-related info to console)
        # Might clash with yolo's logger, but nothing app-breaking
        logging.basicConfig(format="%(message)s", level=logging.INFO)

        # Add available commands
        # first arg is command as typed in telegram (i.e. "/start"), second is which function gets called
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("register", self.register))
        dispatcher.add_handler(CommandHandler("unregister", self.unregister))
        dispatcher.add_handler(CommandHandler("help", self.help))
        # Filter will recognize unknown commands
        dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

        # Set updater property
        self.updater = updater
        # Initialize bot
        updater.start_polling()
        # Keeps bot running until ctrl c
        updater.idle()

    # Default message on first contact
    def start(self, update: Update, context: CallbackContext):
        response =  "Olá, eu sou um robô que monitora "
        response += "pessoas sem máscara 😷 vistas a partir de sua câmera!\n\n"
        response += "Para saber como me usar, digite /help." 

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    # Adds user to registered chats list
    def register(self, update: Update, context: CallbackContext):
        chat = update.effective_chat.id

        if chat not in self.registered_chats:
            self.registered_chats.append(chat)
        context.bot.send_message(chat_id=chat, text="Registrado com sucesso!")

    # Removes user from registered chats list
    def unregister(self, update: Update, context: CallbackContext):
        chat = update.effective_chat.id

        response =  "Você não será mais notificado "
        response += "(pode levar alguns segundos pra entrar em efeito)."

        self.registered_chats.remove(chat)
        context.bot.send_message(chat_id=chat, text=response)

    # User manual
    def help(self, update: Update, context: CallbackContext):
        response =  "Se você deseja receber uma mensagem sempre que uma pessoa sem máscara for detectada "
        response += "em sua câmera, use o comando /register.\n\n"
        response += "Caso deseje parar de receber essas mensagens, use o comando /unregister.\n\n"
        response += "Para exibir essa mensagem novamente, basta digitar /help!\n\n"
        response += "Simples, não? :)"

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    # Default answer for unknown commands
    def unknown(self, update: Update, context: CallbackContext):
        response = "Desculpe, não conheço esse comando. Tente procurar ajuda com /help!"

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


# Sends a message to all registered users when somebody is found maskless
def init_watcher(bot: Bot):
    while True:
        try:
            # Asks yolo interface if anything was found and if so, what was found
            found, msg, imgs = yolo_interface.check_masked()

            if found:
                # Send a message to every registered user
                for chat in bot.registered_chats:
                    # Error handling
                    if bot.updater is None:
                        break

                    # Send picture
                    for img in imgs:
                        bot.updater.bot.send_photo(chat_id=chat, photo=open("crops/" + img, "rb"))
                    # Send message
                    bot.updater.bot.send_message(chat_id=chat, text=msg)

            # Waits five seconds until next check
            sleep(5)

        # Cleanly exits infinite loop on ctrl c
        except KeyboardInterrupt:
            break


# Adds command line arguments to program
def parse_args():
    parser = argparse.ArgumentParser()
    
    # Argument for bot token
    parser.add_argument("token", type=str, help="bot token acquired from @BotFather")
    parser.add_argument('--source', type=str, default="0", help='file/dir/URL/glob, 0 for webcam')
    
    args = parser.parse_args()
    return args


def main():
    # Gets command line arguments
    args = parse_args()

    # Create bot object
    # Must come before running watcher as it is passed as an argument to it
    bot = Bot()

    # Start yolo on separate thread (so we can run other code while it runs in the background)
    yolo_thread = threading.Thread(target=yolo_interface.init_yolo, args=(args.source,), daemon=True)
    yolo_thread.start()
    
    # Run watcher on separate thread (so we can run other code while it watches in the background)
    watcher_thread = threading.Thread(target=init_watcher, args=(bot,), daemon=True)
    watcher_thread.start()
    
    # Actually initializes bot on telegram
    # Must come after running watcher because it holds the program (updater.idle())
    # Bot must run on main thread
    bot.run(args.token)


if __name__ == "__main__":
    main()
