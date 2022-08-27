import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, Filters, MessageHandler, TypeHandler


ask_reply_markup = ReplyKeyboardMarkup([['Подбросить монетку', 'Случайное число']], resize_keyboard=True)


def ask_what_to_do(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Что нужно сделать?',
                             reply_markup=ask_reply_markup)


def get_coin_side():
    return 'Орёл' if random.randint(0, 1) == 1 else 'Решка'


coin_inline_keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Подбросить ещё раз", callback_data='flip_a_coin_again')]
    ])


def flip_a_coin(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(get_coin_side(), reply_markup=coin_inline_keyboard_markup)


def flip_a_coin_again(update: Update, context: CallbackContext) -> None:
    text = f'{get_coin_side()}\nОтредактировано: {datetime.datetime.now().isoformat()}'
    update.callback_query.edit_message_text(text=text, reply_markup=coin_inline_keyboard_markup)


def get_random_number():
    return random.randint(0, 100)


number_inline_keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Сгенерировать новое", callback_data='new_random_number')]
    ])


def random_number(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(get_random_number(), reply_markup=number_inline_keyboard_markup)


def new_random_number(update: Update, context: CallbackContext) -> None:
    text = f'{get_random_number()}\nОтредактировано: {datetime.datetime.now().isoformat()}'
    update.callback_query.edit_message_text(text=text, reply_markup=number_inline_keyboard_markup)


def main() -> None:
    updater = Updater("YOUR_BOT_TOKEN")

    updater.dispatcher.add_handler(CallbackQueryHandler(flip_a_coin_again, pattern='^flip_a_coin_again'))
    updater.dispatcher.add_handler(CallbackQueryHandler(new_random_number, pattern='^new_random_number'))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.update.message & Filters.text('Подбросить монетку'), flip_a_coin))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.update.message & Filters.text('Случайное число'), random_number))
    updater.dispatcher.add_handler(TypeHandler(Update, ask_what_to_do))

    updater.start_polling()

    print('Started')

    updater.idle()


if __name__ == "__main__":
    main()
