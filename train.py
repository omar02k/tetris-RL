import os
import torch as th
import torch.nn as nn
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from tetrisEnv import TetrisEnv


class TetrisCNN(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim=128):
        # observation space shape is (H, W, C) = (24, 10, 1)
        super().__init__(observation_space, features_dim)
        n_input_channels = observation_space.shape[-1]
        self.cnn = nn.Sequential(
            # Input: (N, 1, 24, 10)
            nn.Conv2d(n_input_channels, 32, kernel_size=3, stride=1, padding=1), # -> (N, 16, 24, 10)
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1), # -> (N, 32, 24, 10)
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2), # -> (N, 64, 12, 5)
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1), # -> (N, 64, 12, 5)
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2), # -> (N, 64, 6, 2)
            nn.Flatten(),
        )

        # compute the output of the conv layers
        with th.no_grad():
            dummy_input = th.as_tensor(observation_space.sample()[None]).float()
            dummy_input = dummy_input.permute(0, 3, 1, 2)

            flat_size = self.cnn(dummy_input).shape[1]

        self.linear = nn.Sequential(
            nn.Linear(flat_size, features_dim),
            nn.ReLU()
        )

    def forward(self, observations):
        observations = observations.permute(0, 3, 1, 2)
        return self.linear(self.cnn(observations))


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)

    env = TetrisEnv(do_render=True)
    env = Monitor(env)  # episode logging for training stats

    policy_kwargs = dict(
        features_extractor_class=TetrisCNN,
        features_extractor_kwargs=dict(features_dim=128),
    )

    # DQN agent
    model = DQN(
        "CnnPolicy",
        env,
        policy_kwargs=policy_kwargs,
        learning_rate=5e-4,
        buffer_size=100000,
        exploration_fraction=0.2,
        exploration_final_eps=0.02,
        batch_size=32,
        train_freq=4,
        target_update_interval=1000,
        gamma=0.99,
        verbose=1,
        gradient_steps=1,
        tensorboard_log="./tetris_tensorboard/"
    )

    # Train model
    model.learn(total_timesteps=int(1e6), progress_bar=True)

    # Save trained model
    model.save("models/dqn_tetris")
    env.close()
