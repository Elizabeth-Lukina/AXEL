from tictactoe_logic import QLearningAgent, make_move, check_winner, is_draw, available_moves, State

def train_and_save(agent_path="agent.pkl", episodes=90000):
    agent = QLearningAgent(alpha=0.5, gamma=0.9, epsilon=0.2)
    decay = (0.2-0.02)/(episodes-1)
    for i in range(episodes):
        agent.epsilon = max(0.02, 0.2 - decay*i)
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
