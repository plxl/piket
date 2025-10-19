# Piket Usage Guide
You can manipulate Pikmin e+ cards using Piket in numerous ways with ease! Let's start by simply outputting conversions:
```py
import piket
from pathlib import Path

card = piket.decode("card.raw")
Path("card.bin").write_bytes(card) # <- editable level data
newcard = piket.encode(card, "card.raw")
Path("newcard.raw").write_bytes(newcard) # <- re-encoded level data, ready for playing
```

Now let's manipulate the level data, filling a Plucking Pikmin level with grass tiles and red Pikmin:
```py
import piket
from pathlib import Path

LEVEL_START = 0x115
TILE_SIZE = 0x58
TILE_END = LEVEL_START + TILE_SIZE
PIKI_END = TILE_END + TILE_SIZE

TILE_GRASS = 0x1
PIKI_RED = 0x1

card = piket.decode("card.raw")

# optional: guarantee this card contains Plucking Pikmin levels
card_id = piket.get_id("card.raw").decode("ascii").replace("\x00", "")
if card_id != "PIKMINCARD1S":
    raise Exception(f"This card is not from the Plucking Pikmin set.")

# set all ground tiles to grass
card[LEVEL_START:TILE_END] = bytes([TILE_GRASS]) * TILE_SIZE

# set all piki tiles to red pikmin
card[TILE_END:PIKI_END] = bytes([PIKI_RED]) * TILE_SIZE

Path("newcard.raw").write_bytes(piket.encode(card, "card.raw"))
```

When loading the `newcard.raw` output in-game, this is what we get:

![demo_allgrass_allred](https://raw.githubusercontent.com/plxl/piket/refs/heads/main/docs/demo_allgrass_allred.png)

---
<br>

There's plenty more features coming soon, and when they're added, this Usage Guide will update to reflect new possibilities within the library.
