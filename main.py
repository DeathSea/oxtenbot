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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InlineQueryResultPhoto, InputTextMessageContent, User
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    InlineQueryHandler,
    InvalidCallbackData
)
from tg_ten import tg_ten,TEN_PLAYER_1,TEN_PLAYER_2,TEN_ALL_FILL,TEN_INV_MOVE,TEN_KEEP_GOING,TEN_PLAYER1_WIN,TEN_PLAYER2_WIN,TEN_INV_PLAYER

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
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

GAME_STATE_A = 1
GAME_STATE_B = 2
GAME_STATE_C = 3
GAME_STATE_D = 4
GAME_STATE_E = 5
GAME_STATE_F = 6
GAME_STATE_G = 7

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query
    username = query.from_user.first_name

    tgten = tg_ten()

    x_keyboard = []
    o_keyboard = []
    for i in range(3):
        l = []
        ll = []
        for j in range(3):
            l.append(InlineKeyboardButton("⬜️", callback_data=(tgten, (i, j), (query.from_user, TEN_PLAYER_2), GAME_STATE_B)))
            ll.append(InlineKeyboardButton("⬜️", callback_data=(tgten, (i, j), (TEN_PLAYER_1, query.from_user), GAME_STATE_C)))
        x_keyboard.append(l)
        o_keyboard.append(ll)
    
    results = [
        InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url="https://telegra.ph/file/73bf938912c533307874d.png",
            thumb_url="https://telegra.ph/file/73bf938912c533307874d.png",
            title="❌",
            description="https://telegra.ph/file/73bf938912c533307874d.png",
            reply_markup = InlineKeyboardMarkup(x_keyboard),
            input_message_content = InputTextMessageContent(f"❌ {username} 👈\n⭕️ ?\n全局棋局：\n{tgten.tg_global_state()}\n当前棋局：\n{tgten.tg_all_state()}\n请选择大棋盘：")
        ),
        InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url="https://telegra.ph/file/ea9e9b7873bc6960d102e.png",
            thumb_url="https://telegra.ph/file/ea9e9b7873bc6960d102e.png",
            title="⭕️",
            description="https://telegra.ph/file/ea9e9b7873bc6960d102e.png",
            reply_markup = InlineKeyboardMarkup(o_keyboard),
            input_message_content=InputTextMessageContent(f"❌ ? 👈\n⭕️ {username}\n全局棋局：\n{tgten.tg_global_state()}\n当前棋局：\n{tgten.tg_all_state()}\n请选择大棋盘：")
        ),
    ]

    update.inline_query.answer(results)

#
#  state\action                    |            player 1 select               |                player 2 select          | other player 
# state A game start init          |                   A                      |                    B                    |     B
# state B player 1 start play      |                   D                      |                    F                    |     F
# state C player 2 start play      |                   F                      |                    E                    |     F
# state D player 1 continue select | full -> C, no full -> E, game over -> G  |                    F                    |     F
# state E player 2 continue select |                   F                      | full -> B, no full -> D, game over -> G |     F
# state F invalid move             |
# state G game over                |
def game_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    tgten = query.data[0]
    location = query.data[1]
    play = query.data[2]
    game_state = query.data[3]

    if type(play[0]) != User and type(play[1]) != User:
        query.answer("内部错误", show_alert=True)
        return

    player1_name = "?"
    if type(play[0]) == User:
        player1_name = play[0].first_name + " " + "👈" if tgten.cur_player == play[0].id else ""
    player2_name = "?"
    if type(play[1]) == User:
        player2_name = play[1].first_name + " " + "👈" if tgten.cur_player == play[1].id else ""

    operation_user = query.from_user

    if game_state == GAME_STATE_B or game_state == GAME_STATE_C:
        if operation_user == play[0] or operation_user == play[1]:
            if tgten.global_state[location[0]][location[1]] != 0:
                query.edit_message_text("不能走这")
                query.answer()
                return
            next_game_state = GAME_STATE_D if operation_user == play[0] else GAME_STATE_E
            tgten.location = location
            keyboard = []
            for i in range(3):
                l = []
                for j in range(3):
                    l.append(InlineKeyboardButton(tgten.get_tg_tag(tgten.all_state[location[0]][location[1]][i][j]), callback_data=(tgten, (i, j), play, next_game_state)))
                keyboard.append(l)

            query.edit_message_text(text=f"❌ {player1_name}\n⭕️ {player2_name}\n全局棋局：\n{tgten.tg_global_state()}\n当前棋局：\n{tgten.tg_all_state()}\n请选择小棋盘：",
                reply_markup = InlineKeyboardMarkup(keyboard))
            query.answer()
        else:
            query.answer("你不能走！", show_alert=True)
    elif game_state == GAME_STATE_D or game_state == GAME_STATE_E:
        if game_state == GAME_STATE_D and operation_user != play[0] and type(play[0]) == User:
            query.answer("你不能走！", show_alert=True)
            return
        if game_state == GAME_STATE_E and operation_user != play[1] and type(play[1]) == User:
            query.answer("你不能走！", show_alert=True)
            return 
        if operation_user != play[0] and operation_user != play[1]:
            query.answer("你不能走！", show_alert=True)
            return

        if type(play[0]) != User and game_state == GAME_STATE_D:
            play = (operation_user, play[1])
        if type(play[1]) != User and game_state == GAME_STATE_E:
            play = (play[0], operation_user)

        (next_location, state) = tgten.set_cur_move(query.from_user.id, location)
        if state == TEN_PLAYER1_WIN or state == TEN_PLAYER2_WIN:
            query.edit_message_text(f"游戏结束，玩家{player1_name if state == TEN_PLAYER1_WIN else player2_name}赢了")
            query.answer()
            return
        if state == TEN_INV_MOVE or state == TEN_INV_PLAYER:
            query.answer("不能走这",show_alert=True)
            return
        if state == TEN_ALL_FILL:
            query.edit_message_text(f"游戏结束，没有赢家")
            query.answer()
            return


        player1_name = "?"
        if type(play[0]) == User:
            player1_name = play[0].first_name + " " + "👈" if tgten.cur_player == play[0].id else ""
        player2_name = "?"
        if type(play[1]) == User:
            player2_name = play[1].first_name + " " + "👈" if tgten.cur_player == play[1].id else ""

        if next_location == [-1, -1]:
            next_game_state = GAME_STATE_B if operation_user == play[1] else GAME_STATE_C
            keyboard = []
            for i in range(3):
                l = []
                for j in range(3):
                    l.append(InlineKeyboardButton(tgten.get_tg_tag(tgten.global_state[i][j]), callback_data=(tgten, (i, j), play, next_game_state)))
                keyboard.append(l)

            query.edit_message_text(text=f"❌ {player1_name}\n⭕️ {player2_name}\n全局棋局：\n{tgten.tg_global_state()}\n当前棋局：\n{tgten.tg_all_state()}\n下一步不可用，请选择大棋盘：",
                reply_markup = InlineKeyboardMarkup(keyboard))
            query.answer()
            return
        else:
            tgten.location = next_location
            already_select = f"你只能走在第{tgten.location[0] + 1}, {tgten.location[1] + 1}格大棋盘上\n";

            next_game_state = GAME_STATE_E if operation_user == play[0] else GAME_STATE_D
            keyboard = []
            for i in range(3):
                l = []
                for j in range(3):
                    l.append(InlineKeyboardButton(tgten.get_tg_tag(tgten.all_state[location[0]][location[1]][i][j]), callback_data=(tgten, (i, j), play, next_game_state)))
                keyboard.append(l)

            query.edit_message_text(text=f"❌ {player1_name}\n⭕️ {player2_name}\n全局棋局：\n{tgten.tg_global_state()}\n当前棋局：\n{tgten.tg_all_state()}\n{already_select}请选择小棋盘：",
                reply_markup = InlineKeyboardMarkup(keyboard))
            query.answer()

    return 1

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
    dispatcher.add_handler(CallbackQueryHandler(game_start, pattern=type(())))
    dispatcher.add_handler(CallbackQueryHandler(lambda u,c:u.callback_query.answer(text='Button is no longer valid', show_alert=True), pattern=InvalidCallbackData))
    #dispatcher.add_handler(CallbackQueryHandler(test))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()