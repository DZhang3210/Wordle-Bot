import gymnasium as gym
import numpy as np
import random
from gymnasium import spaces
from createPrefix import createPrefix, prefixCheck

class MyCustomEnv(gym.Env):
    def __init__(self):
        super(MyCustomEnv, self).__init__()
        self.words, self.prefix = createPrefix()  # wordList(for random), prefixTree
        self.currentPrefix = self.prefix  # traverse prefixTree to guarantee valid word

        self.action_space = spaces.Discrete(26)  # Output only one character
        # kom observations + gar observations + currentWord + currIndex
        low = np.array([-1] * 26 + [-1] * 5 + [-1] * 5 + [0])
        high = np.array([1] * 26 + [25] * 5 + [25] * 5 + [4])
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.int32)

        self.word = [0] * 5
        self.guessWord = [-1] * 5
        self.kom = [-1] * 26
        self.gar = [-1] * 5
        self.index = 0
        self.guessIndex = 0
        self.current_obs = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        w = self.words[int(random.random() * len(self.words))]
        self.word = [ord(c) - ord('a') for c in w]

        self.guessWord = [-1] * 5
        self.kom = [-1] * 26
        self.gar = [-1] * 5
        self.index = 0
        self.guessIndex = 0

        self.current_obs = np.array(self.kom + self.gar + self.guessWord + [self.index], dtype=np.int32)
        return self.current_obs, {}

    def step(self, action):
        char = int(action)  # integer from 0-25
        done = False
        info = {}
        rInfo = {"m": 0, "e": 0, "p": 0}  # [found missing, found exist, found in-place]
        reward = 0

        # Automatically exits if the character isn't inside the prefixTree
        if char not in self.currentPrefix:
            reward = -100
            info = {'error': 'Invalid char'}
            return self.current_obs, reward, done, info

        # If that index is known, highly prioritize matching it
        if self.gar[self.index] != -1:
            if char != self.gar[self.index]:
                reward = -10
            else:
                reward = 5
        elif self.kom[char] == -1:
            reward = 1
        elif self.kom[char] == 0:
            reward = -1
        elif self.kom[char] == 1:
            reward = 0.8

        # If it's not the end, update guessWord + index
        if self.index < 4:
            self.guessWord[self.index] = char
            self.index += 1
            self.currentPrefix = self.currentPrefix[char]
        # Verify
        else:
            if self.guessWord == self.word:
                reward = 10
                done = True
                info = {"result": "word found"}
                self.current_obs = np.array(self.kom + self.gar + self.guessWord + [self.index], dtype=np.int32)
                return self.current_obs, reward, done, info
            else:
                # Check if words either are in-place, found, or missing
                for i, c in enumerate(self.guessWord):
                    if self.guessWord[i] == self.word[i]:
                        if self.gar[i] == -1:
                            rInfo["p"] += 1
                            self.gar[i] = c
                    elif c in self.word:
                        if self.kom[c] == -1:
                            rInfo["e"] += 1
                            self.kom[c] = 1
                    else:
                        rInfo["m"] += 1
                        self.kom[c] = max(-1, self.kom[c])

                # Reset index, guessWord, and guessIndex
                self.index = 0
                self.guessWord = [-1] * 5
                self.guessIndex += 1
                self.currentPrefix = self.prefix
                reward += rInfo["p"] * 2 + rInfo["e"] * 1 + rInfo["m"] * -0.5
                # If we exhaust all our guesses, set done = true
                if self.guessIndex >= 6:
                    done = True

        self.current_obs = np.array(self.kom + self.gar + self.guessWord + [self.index], dtype=np.int32)
        return self.current_obs, reward, done, info

    def render(self, mode='human'):
        print(f"Current observation: {self.current_obs}")

    def close(self):
        pass

def register_custom_env():
    from gymnasium.envs.registration import register
    register(
        id='MyCustomEnv-v0',
        entry_point='index:MyCustomEnv',
    )
