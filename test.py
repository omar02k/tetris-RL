import time
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from tetrisEnv import TetrisEnv

if __name__ == '__main__':
    env = Monitor(TetrisEnv(do_render=True))
    model = DQN.load("models/dqn_tetris", env=env)
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=False)
    print(f"Mean reward over 10 episodes: {mean_reward:.2f}")

    # live demo episode
    obs, _ = env.reset()
    done = False
    total_reward = 0

    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        time.sleep(0.05)  # slows down rendering for visibility
    
    print(f"Episode finished with total reward: {total_reward}")
    env.close()
