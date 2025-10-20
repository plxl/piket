from .tile import Tile
from .object import Object
from .piki import Piki
from piket.constants import CONNECTING_PIKMIN_HEADER_LENGTH, CONNECTING_PIKMIN_LAYER_LENGTH
from piket.base.level_base import LevelBase
from typing import Self

class Level(LevelBase):
    def __init__(
            self,
            index,
            tiles:   bytearray = bytearray(9 * 6),
            objects: bytearray = bytearray(9 * 6),
            pikis:   bytearray = bytearray(9 * 6),
            raw: bytes | bytearray = bytearray(0),
            grid: tuple[int, int] = (0, 0),
    ):
        super().__init__(index, 9, 6, 3, [tiles, objects, pikis], raw)
        self.grid = grid

    @classmethod
    def from_bytes(cls, level: bytearray) -> Self:
        index = level[0]
        grid = level[1], level[2]
        layers = level[CONNECTING_PIKMIN_HEADER_LENGTH:]
        tiles = layers[:CONNECTING_PIKMIN_LAYER_LENGTH]
        objects = layers[CONNECTING_PIKMIN_LAYER_LENGTH:CONNECTING_PIKMIN_LAYER_LENGTH*2]
        pikis = layers[CONNECTING_PIKMIN_LAYER_LENGTH*2:CONNECTING_PIKMIN_LAYER_LENGTH*3]
        return cls(index, tiles, objects, pikis, level, grid)

    def to_bytes(self) -> bytes:
        raw = bytearray()
        # the 12-C0XX levels do not have any main leveltype header like PIKMINPUZZLE01/02
        # though, in other cards, it is sometimes prefaced with PIKMINOTAKARA
        # TODO: figure that out
        raw.append(self.index)
        raw.extend(self.grid)
        return super().to_bytes(raw)

    def get_tile(self, x: int, y: int) -> Tile:
        """Gets the Tile at (x, y, layer 0)."""
        value = super().get_tile(x, y, 0)
        if value not in Tile._value2member_map_:
            raise ValueError(f"Unknown Tile with value {value}")
        return Tile(value)
    
    def get_object(self, x: int, y: int) -> Object:
        """Gets the Object at (x, y, layer 1)."""
        value = super().get_tile(x, y, 1)
        if value not in Object._value2member_map_:
            raise ValueError(f"Unknown Object with value {value}")
        return Object(value)

    def get_piki(self, x: int, y: int) -> Piki:
        """Gets the Piki at (x, y, layer 2)."""
        value = super().get_tile(x, y, 2)
        if value not in Piki._value2member_map_:
            raise ValueError(f"Unknown Piki with value {value}")
        return Piki(value)

    def set_tile(self, x: int, y: int, tile: Tile | Object | Piki):
        """Sets the (Tile | Piki | Object) at (x, y) on the correct layer."""
        value = tile.value
        if isinstance(tile, Tile):
            layer = 0
        elif isinstance(tile, Object):
            layer = 1
        elif isinstance(tile, Piki):
            layer = 2

        super().set_tile(x, y, value, layer)

    def set_tiles(self, x: int, y: int, w: int, h: int, tile: Tile | Object | Piki):
        """Sets the (Tiles | Objects | Pikis) from (x, y) to (w, h) on the correct layer."""
        value = tile.value
        if isinstance(tile, Tile):
            layer = 0
        elif isinstance(tile, Object):
            layer = 1
        elif isinstance(tile, Piki):
            layer = 2

        super().set_tiles(x, y, w, h, value, layer)

    def clear_all(self):
        """Sets all Tiles, Objects and Pikis to value 0."""
        for i in range(self.layers):
            super().set_tiles(0, 0, self.width, self.height, 0, i)
    
    def set_grid(self, tile: Tile | Object | Piki):
        """Sets the (Tiles | Objects | Pikis) from (0, 0) to (grid_w, grid_h) on the correct layer."""
        value = tile.value
        if isinstance(tile, Tile):
            layer = 0
        elif isinstance(tile, Object):
            layer = 1
        elif isinstance(tile, Piki):
            layer = 2

        super().set_tiles(0, 0, self.grid[0], self.grid[1], value, layer)
