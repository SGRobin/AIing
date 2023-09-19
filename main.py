import gymnasium as gym

env = gym.make("LunarLander-v2", render_mode="human")

observation, info = env.reset(seed=42)
for _ in range(100):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    if terminated or truncated:
        observation, info = env.reset()
env.close()
