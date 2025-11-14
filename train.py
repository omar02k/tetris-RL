import os
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from tetrisEnv import TetrisEnv

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)

    env = TetrisEnv(do_render=True)
    env = Monitor(env)  # episode logging for training stats

    # DQN agent
    model = DQN(
        "MlpPolicy",
        env,
        learning_rate=1e-4,
        buffer_size=100000,
        exploration_fraction=0.5,
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
    model.learn(total_timesteps=int(5e5), progress_bar=True)

    # Save trained model
    model.save("models/dqn_tetris")
    env.close()
