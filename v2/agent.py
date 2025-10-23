import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque
from helper import plot_progress
from figure import Figure
from game import GameEnv


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
GAMMA = 0.9

EPSILON_START = 1.0     # Valeur initiale d'epsilon
EPSILON_DECAY = 0.997   # Taux de décroissance d'epsilon
MIN_EPSILON = 0.15      # Valeur minimale d'epsilon
EXPLORATION_PHASE_EPISODES = 300 # Nombre d'épisodes où epsilon reste à EPSILON_START
TARGET_UPDATE = 100


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        mid_size = hidden_size // 2
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.norm1 = nn.LayerNorm(hidden_size)
        self.fc2 = nn.Linear(hidden_size, mid_size)
        self.norm2 = nn.LayerNorm(mid_size)
        self.dropout = nn.Dropout(p=0.1)
        self.fc3 = nn.Linear(mid_size, output_size)

    def forward(self, x):
        x = F.relu(self.norm1(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.norm2(self.fc2(x)))
        x = self.dropout(x)
        x = self.fc3(x)
        return x


class DQNAgent:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.n_games = 0
        self.epsilon = EPSILON_START
        self.gamma = GAMMA
        self.memory = deque(maxlen=MAX_MEMORY)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Utilisation du périphérique : {self.device}")

        self.model = Linear_QNet(input_size, 512, output_size).to(self.device)
        self.target_model = Linear_QNet(input_size, 512, output_size).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()

        self.optimizer = optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self._train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self._train_step(state, action, reward, next_state, done)

    def _train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(np.array(state), dtype=torch.float).to(self.device)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float).to(self.device)
        action = torch.tensor(np.array(action), dtype=torch.long).to(self.device)
        reward = torch.tensor(np.array(reward), dtype=torch.float).to(self.device)
        done = torch.tensor(np.array(done), dtype=torch.bool).to(self.device)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = torch.unsqueeze(done, 0)

        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.target_model(next_state[idx]))
            target[idx][action[idx]] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

    def get_action(self, state):
        if self.n_games < EXPLORATION_PHASE_EPISODES:
            current_epsilon = EPSILON_START
        else:
            self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)
            current_epsilon = self.epsilon

        final_move = 0
        if random.random() < current_epsilon:
            final_move = random.randint(0, self.output_size - 1)
        else:
            state0 = torch.tensor(np.array(state), dtype=torch.float).to(self.device)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()
        return final_move

    def update_target_model(self):
        """Copie les poids du modèle principal vers le modèle cible."""
        self.target_model.load_state_dict(self.model.state_dict())
    
    def save_model(self, file_name='dqn_model.pth'):
        """Sauvegarde le modèle principal."""
        torch.save(self.model.state_dict(), file_name)
    
    def load_model(self, file_name='dqn_model.pth'):
        """Charge le modèle principal."""
        self.model.load_state_dict(torch.load(file_name))
        self.update_target_model()

def train():
    figure = Figure("../datasets/1_example.json")
    game = GameEnv(figure, clone=False, show=False)
    state_size = game.get_state().shape[0]
    action_size = game.n_actions
 
    agent = DQNAgent(state_size, action_size)
 
    scores = []
    mean_scores = []
    actions_taken_list = []
    total_score = 0
    record_score = 0
    episode = 0
 
    while True:
        episode += 1
        game.reset()
        state_old = game.get_state()
 
        game_over = False
        while not game_over:
            final_action_idx = agent.get_action(state_old)
            reward, game_over, score = game.play_step(final_action_idx)
            state_new = game.get_state()
 
            agent.train_short_memory(state_old, final_action_idx, reward, state_new, game_over)
 
            agent.remember(state_old, final_action_idx, reward, state_new, game_over)
 
            state_old = state_new
 
        agent.n_games += 1
        agent.train_long_memory()
 
        if agent.n_games % TARGET_UPDATE == 0:
            agent.update_target_model()
 
        scores.append(score)
        actions_taken_list.append(len(game._actions_history))
        total_score += score
        mean_score = total_score / agent.n_games
        mean_scores.append(mean_score)
 
        if score > record_score:
            record_score = score
            agent.save_model('./saves/best_model.pth')
 
        print(f'Episode {episode}, Score: {score}, Record: {record_score}, Actions: {len(game._actions_history)}, Epsilon: {agent.epsilon:.2f}')
 
        plot_progress(scores, mean_scores, actions_taken_list)
 
        if episode > 20000:
            print("Entraînement terminé.")
            break
 
if __name__ == '__main__':
    train()