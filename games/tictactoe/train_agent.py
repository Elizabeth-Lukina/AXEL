from tictactoe_logic import QLearningAgent, make_move, check_winner, is_draw, available_moves, State

def train_and_save(agent_path="agent.pkl", episodes=120000):
    agent = QLearningAgent(alpha=0.9, gamma=0.5, epsilon=0.3)
    decay = (0.3-0.05)/(episodes-1)
    for i in range(episodes):
        agent.epsilon = max(0.05, 0.3 - decay*i)
        state: State = (0,)*9
        player = 1
        hist = []
        while True:
            action = agent.choose_action(state)
            next_state = make_move(state, action, player)
            hist.append((state,action,player))
            winner = check_winner(next_state)
            if winner or is_draw(next_state):
                r1 = 1 if winner==1 else -1 if winner==2 else 0.5
                r2 = 1 if winner==2 else -1 if winner==1 else 0.5
                last_next = None
                for s,a,p in reversed(hist):
                    r = r1 if p==1 else r2
                    agent.update(s,a,r,last_next)
                    last_next = s
                break
            state = next_state
            player = 2 if player==1 else 1
    agent.save(agent_path)
    print("Q-таблица сохранена в", agent_path)

if __name__=="__main__":
    train_and_save()

# alpha (коэффициент обучения) —
# Насколько сильно обновляется старая Q-оценка новыми данными.
# 1.0 → всегда берём только новое значение.
# 0.0 → ничего не меняем.#
# 0.5 → берём среднее между старым и новым.
#
# gamma (дисконтирование будущей награды) —
# Учитывает, насколько ценны будущие ходы по сравнению с текущими.
# 1.0 → ценим будущее как настоящее.#
# 0.0 → оцениваем только текущую награду.
# 0.9 → будущее почти так же важно, как настоящее.
#
# epsilon (вероятность случайного хода) —
# Управляет балансом исследования (exploration) и эксплуатации (exploitation).
# 1.0 → всегда ходим случайно.#
# 0.0 → всегда выбираем лучший известный ход.
# 0.2 → 20% случайных ходов, 80% — лучший ход.