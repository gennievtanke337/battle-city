import pygame
class Logger:
    def __init__(self, fn): self.fn = fn
    def log(self, msg):
        with open(self.fn, "a") as f:
            f.write(msg + "\n")
        print(msg)
