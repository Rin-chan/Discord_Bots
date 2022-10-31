class Enemy:
    def __init__(self, name, hp, damage, exp, gold):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.exp = exp
        self.gold = gold
        
    def get_name(self):
        return self.name
    
    def get_hp(self):
        return self.hp

    def get_damage(self):
        return self.damage

    def get_exp(self):
        return self.exp

    def get_gold(self):
        return self.gold
    
    def set_name(self, name):
        self.name = name
    
    def set_hp(self, hp):
        self.hp = hp

    def set_damage(self, damage):
        self.damage = damage

    def set_exp(self, exp):
        self.exp = exp

    def set_gold(self, gold):
        self.gold = gold