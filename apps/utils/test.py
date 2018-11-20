__author__ = 'Administrator'

from random import choice
seeds = "1234567890"
random_str = []
for i in range(4):
    # 使用randoms中的choice()来随机获得1个数
    random_str.append(choice(seeds))
print(random_str)