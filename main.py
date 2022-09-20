#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging
from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    InlineQueryHandler
)
from ten import ten

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
MAIN_MENU = 0
GAME = 1
# Callback data


main_menu_keyboard = [
    [
        InlineKeyboardButton("❌跟机器人玩🤖", callback_data="with_robot"),
    ],
    [
        InlineKeyboardButton("👥跟朋友玩⭕️", switch_inline_query="@XOtenbot"),
    ],
    [
        InlineKeyboardButton("帮助", callback_data="help"),
    ],
]

def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("选择选项：", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return MAIN_MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="选择选项：", reply_markup=reply_markup)
    return MAIN_MENU


def with_robot(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("返回", callback_data="main"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="❌还没实现！❌", reply_markup=reply_markup
    )
    return MAIN_MENU

def help_msg(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("返回", callback_data="main"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="一段说明文字。。", reply_markup=reply_markup
    )
    return MAIN_MENU

def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="bye bye!")
    return ConversationHandler.END


big_ox_game_keyboard = [
    [
        InlineKeyboardButton("⬜️", callback_data="big_1_1"),InlineKeyboardButton("⬜️", callback_data="big_1_2"),InlineKeyboardButton("⬜️", callback_data="big_1_3")
    ],
    [
        InlineKeyboardButton("⬜️", callback_data="big_2_1"),InlineKeyboardButton("⬜️", callback_data="big_2_2"),InlineKeyboardButton("⬜️", callback_data="big_2_2")
    ],
    [
        InlineKeyboardButton("⬜️", callback_data="big_3_1"),InlineKeyboardButton("⬜️", callback_data="big_3_2"),InlineKeyboardButton("⬜️", callback_data="big_3_3")
    ],
]

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="❌",
            input_message_content=InputTextMessageContent("测试"),
            reply_markup = InlineKeyboardMarkup(big_ox_game_keyboard)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="⭕️",
            input_message_content=InputTextMessageContent("另一个"),
            reply_markup = InlineKeyboardMarkup(big_ox_game_keyboard)
        ),
    ]

    update.inline_query.answer(results)

def big_table(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.edit_message_text(text="11111",
        reply_markup = InlineKeyboardMarkup(big_ox_game_keyboard))
    return GAME


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(with_robot, pattern='^with_robot$'),
                CallbackQueryHandler(help_msg, pattern='^help$'),
                CallbackQueryHandler(start_over, pattern='^main$'),
                # CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                # CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                # CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            GAME: [
                CallbackQueryHandler(start_over, pattern='^restart$'),
                CallbackQueryHandler(end, pattern='^end$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(CallbackQueryHandler(big_table, pattern="^big_\d_\d"))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()