from .enemy import Enemy

class Enemy_Chicken(Enemy):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp, damage, 1, 1)

Chicken = Enemy_Chicken("Chicken", 4, 0)