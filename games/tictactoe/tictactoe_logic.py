from __future__ import annotations
import random
import pickle
from typing import Tuple, List, Dict, Optional

State = Tuple[int,...]
Action = int

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]


def check_winner(state: State) -> int:
    for a,b,c in WIN_LINES:
        if state[a] == state[b] == state[c] != 0:
            return state[a]
    return 0

def is_draw(state: State) -> bool:
    return 0 not in state and check_winner(state)==0

def available_moves(state: State) -> List[Action]:
    return [i for i,v in enumerate(state) if v==0]

def make_move(state: State, action: Action, player: int) -> State:
    s = list(state)
    s[action] = player
    return tuple(s)

def render_board(state: State) -> str:
    sym = {0:'·', 1:'X', 2:'O'}
    return "\n".join(" ".join(sym[state[3*r+c]] for c in range(3)) for r in range(3))


class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q: Dict[Tuple[State, Action], float] = {}

    def get_Q(self, state: State, action: Action) -> float:
        return self.Q.get((state, action), 0.0)

    def choose_action(self, state: State) -> Action:
        moves = available_moves(state)
        if not moves: raise ValueError("Нет ходов")
        if random.random() < self.epsilon:
            return random.choice(moves)
        qs = [self.get_Q(state,a) for a in moves]
        max_q = max(qs)
        best = [a for a,q in zip(moves,qs) if q==max_q]
        return random.choice(best)

    def best_action(self, state: State) -> Action:
        moves = available_moves(state)
        qs = [self.get_Q(state,a) for a in moves]
        max_q = max(qs)
        best = [a for a,q in zip(moves,qs) if q==max_q]
        return random.choice(best)

    def update(self, state: State, action: Action, reward: float, next_state: Optional[State]):
        old = self.get_Q(state, action)
        if next_state is None or not available_moves(next_state):
            target = reward
        else:
            max_next = max(self.get_Q(next_state,a) for a in available_moves(next_state))
            target = reward + self.gamma * max_next
        self.Q[(state,action)] = old + self.alpha*(target-old)

    def save(self, path: str):
        with open(path,"wb") as f:
            pickle.dump(self.Q,f)

    @staticmethod
    def load(path: str) -> "QLearningAgent":
        with open(path,"rb") as f:
            Q = pickle.load(f)
        agent = QLearningAgent()
        agent.Q = Q
        return agent
