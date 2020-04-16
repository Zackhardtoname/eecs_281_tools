# Created by @arya-k
# Usage: python3 test-generator.py
from random import randint

for n in range(1, 10):
    mode = ["MST", "FASTTSP", "OPTTSP"][n % 3]
    with open("test-{}-{}.txt".format(n, mode), "w") as f:
        f.write("10\n")
        for _ in range(10):
            f.write("{} {}\n".format(randint(-5, 5), randint(-5, 5)))
