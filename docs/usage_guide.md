# Piket Usage Guide
You can manipulate Pikmin e+ cards using Piket in numerous ways with ease!

## Format Conversion
```py
import piket
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG) # output detailed logs

card = piket.decode("card.raw") # decode the raw card
Path("card.bin").write_bytes(card) # write the output

card = piket.encode(card, "card.raw") # re-encode the card
Path("newcard.raw").write_bytes(card) # write the output
```

## Level Editing
Level editing is slightly different for different minigame modes.

### Plucking Pikmin
```py
from piket import Card, PluckingPikmin as P
from pathlib import Path

card = Card("12-A001.raw") # import Plucking Pikmin card

# ensure that the level we want to edit is a Plucking Pikmin level
if isinstance(card.levels[0], P.Level):
    lvl: P.Level = card.levels[0]
    lvl.clear_all() # sets all tiles and pikis to 0x0
    lvl.grid = (4, 3) # sets the level to a 4x3 grid, maximum 11x8
    lvl.start = (1, 0) # sets the starting position
    lvl.player = P.Player.LOUIE # sets the player character

    lvl.set_grid(P.Tile.GRASS) # sets all tiles in the grid (4x3) to grass
    lvl.set_tile(0, 0, P.Piki.YELLOW) # places yellow Pikmin at top-left
    lvl.set_tiles(2, 0, 1, 3, P.Tile.NONE) # removes tiles
    lvl.set_tiles(3, 1, 1, 2, P.Tile.NONE) # removes tiles
    lvl.set_tile(0, 1, P.Tile.FIRE) # places fire geyser at (0, 1)
    lvl.set_tile(1, 1, P.Tile.WATER) # places water pool at (1, 1)
    lvl.set_tile(0, 2, P.Tile.ELECTRICITY_NODE) # places electricity node at (0, 2)
    lvl.set_tile(1, 2, P.Tile.ELECTRICTY) # places electricity at (1, 2)

Path("12-A001-New.raw").write_bytes(card.encode())
```
This is the result of our custom Plucking Pikmin level:

![demo_pluckingpikmin_customlevel](https://raw.githubusercontent.com/plxl/piket/refs/heads/main/docs/demo_pluckingpikmin_customlevel.png)

### Connecting Pikmin
```py
from piket import Card, ConnectingPikmin as C
from pathlib import Path

card = Card("12-C001.raw") # import Connecting Pikmin card

# ensure that the level we want to edit is a Connecting Pikmin level
if isinstance(card.levels[0], C.Level):
    level: C.Level = card.levels[0]
    level.clear_all() # sets all tiles, objects and pikis to 0x0
    level.grid = (4, 2) # sets the level to a 4x2 grid, maximum 9x6

    level.set_grid(C.Tile.NONE) # clears all tiles in the grid (4x2) (recommended)
    # build layout with set_tile() and set_tiles()
    level.set_tiles(0, 0, 2, 1, C.Tile.HORIZONTAL)
    level.set_tile(2, 0, C.Tile.BOTTOM_RIGHT)
    level.set_tile(3, 0, C.Tile.VERTICAL)
    level.set_tile(0, 1, C.Tile.TOP_RIGHT)
    level.set_tile(1, 1, C.Tile.HORIZONTAL)
    level.set_tile(2, 1, C.Tile.BOTTOM_LEFT)
    level.set_tile(3, 1, C.Tile.HORIZONTAL)

    level.set_tile(0, 0, C.Piki.BLUE_RIGHT) # places blue pikmin facing right at (0, 0)
    level.set_tile(3, 0, C.Object.GOAL) # places the ship pod goal object at (3, 0)

Path("12-C001-New.raw").write_bytes(card.encode())
```
This is the result of our custom Connecting Pikmin level:

![demo_connectingpikmin_customlevel](https://raw.githubusercontent.com/plxl/piket/refs/heads/main/docs/demo_connectingpikmin_customlevel.png)

---

There's plenty more features coming soon, and when they're added, this Usage Guide will update to reflect new possibilities within the library.
