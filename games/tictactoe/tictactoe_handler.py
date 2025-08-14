from telebot import types
from .tictactoe_logic import QLearningAgent, available_moves, make_move, check_winner, is_draw, render_board
agent = QLearningAgent.load("games/tictactoe/agent.pkl")
games = {}  # user_id -> state

def make_board_buttons(state):
    kb = types.InlineKeyboardMarkup()
    buttons = []
    for i, v in enumerate(state):
        if v == 0:
            buttons.append(types.InlineKeyboardButton(text="·", callback_data=str(i)))
        else:
            text = "X" if v == 1 else "O"
            buttons.append(types.InlineKeyboardButton(text=text, callback_data="noop"))
    for r in range(3):
        kb.row(*buttons[3*r:3*r+3])
    return kb

def register_games_handlers(bot, agent: QLearningAgent):
    @bot.message_handler(func=lambda m: m.text == "🎲 Поиграем?")
    def start_game(msg):
        user_id = msg.from_user.id
        games[user_id] = (0,)*9
        bot.send_message(
            user_id,
            "Игра крестики-нолики! Ты X.\nВыбери клетку:",
            reply_markup=make_board_buttons(games[user_id])
        )

    @bot.callback_query_handler(func=lambda c: True)
    def process_move(query):
        user_id = query.from_user.id
        if user_id not in games:
            bot.answer_callback_query(query.id, "Начни игру командой /tictactoe")
            return
        state = games[user_id]
        if query.data == "noop":
            bot.answer_callback_query(query.id, "Клетка занята!")
            return
        idx = int(query.data)
        # Ход человека
        state = make_move(state, idx, 1)
        winner = check_winner(state)
        if winner:
            bot.edit_message_text(f"Ты выиграл!\n\n{render_board(state)}",
                                  user_id, query.message.message_id)
            del games[user_id]
            return
        if is_draw(state):
            bot.edit_message_text(f"Ничья!\n\n{render_board(state)}",
                                  user_id, query.message.message_id)
            del games[user_id]
            return
        # Ход бота
        bot_action = agent.best_action(state)
        state = make_move(state, bot_action, 2)
        winner = check_winner(state)
        if winner:
            bot.edit_message_text(f"AXEL победил!\n\n{render_board(state)}",
                                  user_id, query.message.message_id)
            del games[user_id]
            return
        if is_draw(state):
            bot.edit_message_text(f"Ничья!\n\n{render_board(state)}",
                                  user_id, query.message.message_id)
            del games[user_id]
            return
        # Продолжаем игру
        games[user_id] = state
        bot.edit_message_text("Твой ход:", user_id, query.message.message_id,
                              reply_markup=make_board_buttons(state))
