# import gymnasium as gym
try:
    from stable_baselines3 import PPO
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
# from stable_baselines3.common.env_util import make_vec_env
# from index import register_custom_env

# Register the custom environment
# register_custom_env()

# Create an instance of the custom environment
# env = make_vec_env('MyCustomEnv-v0', n_envs=1)

# Train the agent using PPO
# model = PPO('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps=10000)
#
# # Save the trained model
# model.save("ppo_my_custom_env")

# Test the trained agent
# env = gym.make('MyCustomEnv-v0')
# obs, info = env.reset(seed=42)
# for _ in range(100):
#     print(_)
#     action, _states = model.predict(obs)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#         obs, info = env.reset()
# env.close()
