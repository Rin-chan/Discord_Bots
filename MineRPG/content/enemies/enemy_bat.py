from .enemy import Enemy

class Enemy_Bat(Enemy):
    def __init__(self, name, hp, damage, exp, gold, type):
        super().__init__(name, hp, damage, exp, gold)
        self.type = type

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

Water_Bat = Enemy_Bat("Water Bat", 5, 1, 1, 1, "Water")