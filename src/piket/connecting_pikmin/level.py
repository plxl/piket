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

    def get_tile(self, x: int, y: int, layer: int) -> Tile | Object | Piki:
        value = super().get_tile(x, y, layer)
        try:
            if layer == 0:
                return Tile(value)
            elif layer == 1:
                return Object(value)
            elif layer == 2:
                return Piki(value)
            else:
                raise ValueError(f"Type {self.__class__.__name__} does not have Layer {layer}.")

        except ValueError:
            raise ValueError(
                f"Unknown Tile with ID {value} on {self.__class__.__name__}.Layer {layer}."
            )

    def set_tile(self, x: int, y: int, tile: Tile | Object | Piki):
        value = tile.value
        if isinstance(tile, Tile):
            layer = 0
        elif isinstance(tile, Object):
            layer = 1
        elif isinstance(tile, Piki):
            layer = 2
        else:
            raise ValueError(f"Type {self.__class__.__name__} does not have Layer {layer}.")

        super().set_tile(x, y, value, layer)

    def set_tiles(self, x: int, y: int, w: int, h: int, tile: Tile | Object | Piki):
        value = tile.value
        if isinstance(tile, Tile):
            layer = 0
        elif isinstance(tile, Object):
            layer = 1
        elif isinstance(tile, Piki):
            layer = 2
        else:
            raise ValueError(f"Type {self.__class__.__name__} does not have Layer {layer}.")

        super().set_tiles(x, y, w, h, value, layer)

    def clear_all(self):
        for i in range(self.layers):
            super().set_tiles(0, 0, self.width, self.height, 0, i)
    
    def set_grid(self, tile: Tile | Object | Piki):
        value = tile.value
        if isinstance(tile, Tile):
            layer = 0
        elif isinstance(tile, Object):
            layer = 1
        elif isinstance(tile, Piki):
            layer = 2
        else:
            raise ValueError(f"Type {self.__class__.__name__} does not have Layer {layer}.")

        super().set_tiles(0, 0, self.grid[0], self.grid[1], value, layer)
