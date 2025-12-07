import gym

import os
os.add_dll_directory("C://Users//28449//.mujoco//mujoco210//bin")
import sys
sys.path.append('.')
import mujoco_py

import d4rl 


env_id = 'antmaze-large-diverse-v2'
try:
    # render_mode='human' 表示将直接打开一个窗口进行可视化
    env = gym.make(env_id, render_mode='human')
    print(f"成功加载环境: {env_id}")
except Exception as e:
    print(f"加载环境失败: {e}")
    # 退出，如果环境加载失败
    exit()

# 2. 初始化环境
observation, info = env.reset()

# 3. 运行 Agent（这里使用一个随机策略作为演示）
num_episodes = 5
max_steps_per_episode = 500 # AntMaze 的一个 episode 通常较长

print("\n开始运行 Agent...")
for episode in range(num_episodes):
    observation, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0
    step = 0

    while not terminated and not truncated and step < max_steps_per_episode:
        # 随机选择一个动作
        action = env.action_space.sample() 
        
        # 执行动作
        observation, reward, terminated, truncated, info = env.step(action)
        
        # 渲染环境
        # 当 env.make(render_mode='human') 时，env.render() 会更新可视化窗口
        env.render()
        
        total_reward += reward
        step += 1

    print(f"Episode {episode + 1}: 步数={step}, 总奖励={total_reward:.2f}")

# 4. 关闭环境
env.close()
print("\n环境已关闭。")