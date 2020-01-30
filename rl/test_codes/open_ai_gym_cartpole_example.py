import gym
env = gym.make('CartPole-v0')

input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n

print(input_dim)
print(output_dim)


for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        print(observation)
        print('observation', type(observation))
        action = env.action_space.sample()
        print('action', type(action))
        observation, reward, done, info = env.step(action)
        print('reward', type(reward))
        print('info', info)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()