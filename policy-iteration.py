"""
  @author Victor I. Afolabi
  A.I. Engineer & Software developer
  javafolabi@gmail.com
  
  Created on 10 December, 2017 @ 8:51 PM.
  
  Copyright © 2017. Victor. All rights reserved.
"""
import sys
import gym
import numpy as np


def run_episode(env, policy, **kwargs):
    gamma = kwargs.get('gamma', None)
    T = kwargs.get('T', 1000)
    render = kwargs.get('render', False)
    total_rewards = 0
    state = env.reset()
    for t in range(T):
        if render:
            env.render()
        action = policy[state]
        state, reward, done, _ = env.step(action)
        total_rewards += pow(gamma, t) * reward if gamma else reward
        if done:
            break
    return total_rewards


def eval_policy(env, policy, episodes=100):
    scores = [run_episode(env, policy, T=episodes)
              for _ in range(episodes)]
    return np.mean(scores)


def extract_policy(env, V, n_states, n_actions, **kwargs):
    gamma = kwargs.get('gamma', 0.99)
    policy = np.zeros(shape=[n_states])
    for s in range(n_states):
        V_sa = np.zeros(shape=[n_actions])
        for a in range(n_actions):
            for transition in env.env.P[s][a]:
                p, r, s_, _ = transition
                V_sa[a] += p * (r + gamma * V[s_])
        policy[s] = np.argmax(V_sa)
    return policy


def policy_to_value(env, policy, n_states, **kwargs):
    gamma = kwargs.get('gamma', 0.99)
    eps = kwargs.get('eps', 1e-20)
    max_iter = kwargs.get('max_iter', 10000)
    # Utility for following the policy
    V = np.zeros(shape=[n_states])
    for t in range(max_iter):
        v = np.copy(V)
        for s in range(n_states):
            a = policy[s]
            for transition in env.env.P[s][a]:
                p, s_, r, _ = transition
                V[s] += p * (r + gamma * v[s_])
        # Convergence
        if np.sum(np.fabs(v - V)) <= eps:
            sys.stdout.write(f'\rPolicy\'s value converged @ {t+1:,}')
            sys.stdout.flush()
            break
    return V


def policy_iteration(env, n_states, n_actions, **kwargs):
    gamma = kwargs.get('gamma', 0.99)

if __name__ == '__main__':
    env_name = 'frozenLake8x8-v0'
    env = gym.make(env_name)
    # Hyperparameters
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    episodes = 100
