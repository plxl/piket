from enum import Enum

class Tile(Enum):
    GROUND = 0
    FIRE = 0x10
    WATER = 0x11
    ELECTRICITY = 0x12
    BULBORB = 0x13
    POISON = 0x14
    ROCK = 0x20
    RED_CANDYPOP = 0x40
    BLUE_CANDYPOP = 0x41
    YELLOW_CANDYPOP = 0x42
    PURPLE_CANDYPOP = 0x43
    WHITE_CANDYPOP = 0x44
    TREASURE = 0x50
    NONE = 0x60
