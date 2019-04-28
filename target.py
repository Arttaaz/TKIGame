from enum import Enum
class Target(Enum):
    NEAREST_ENEMY = "PLUS PROCHE"

    def __str__(self):
        return self.value
