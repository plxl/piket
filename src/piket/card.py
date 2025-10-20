from pathlib import Path
from piket.util import _to_bytes, decode, encode, get_id
from piket.constants import *
from pathlib import Path
from . import connecting_pikmin as ConnectingPikmin
from piket.base.level_base import LevelBase

class Card:
    def __init__(self, card: bytes | bytearray | str | Path | None):
        self.levels: list[LevelBase] = []
        if card is not None:
            self.raw = _to_bytes(card)
            self.decoded = decode(self.raw)
            self.id = get_id(self.raw).decode("ascii").replace('\x00', '')

            if self.id == CARD_SET_A_PLUCKING or self.id == CARD_SET_D_OLIMAR:
                # Plucking Pikmin x3
                raise NotImplementedError(f"Card with ID {self.id} has not been implemented yet.")

            elif self.id == CARD_SET_B_MARCHING or self.id == CARD_SET_D_PRESIDENT:
                # Marching Pikmin x3
                raise NotImplementedError(f"Card with ID {self.id} has not been implemented yet.")

            elif self.id == CARD_SET_C_CONNECTING or self.id == CARD_SET_D_LOUIE:
                # Connecting Pikmin x3
                for i in range(3):
                    start = i*0x100
                    end = min((i+1)*0x100, len(self.decoded) - LEVEL_FOOTER_LENGTH)
                    level_data = self.decoded[start:end]
                    level = ConnectingPikmin.Level.from_bytes(level_data)
                    self.levels.append(level)
            
            elif self.id == CARD_SETS_H_P_ALL:
                # Promo card; 1x Plucking 1x Marching 1x Connecting
                raise NotImplementedError(f"Card with ID {self.id} has not been implemented yet.")

            else:
                raise ValueError(f"Card data contains an unrecognised ID: '{self.id}'.")

    def encode(self, partial_encode = False, raw_level = False) -> bytes:
        new_decoded = bytearray()
        for i, level in enumerate(self.levels):
            if isinstance(level, ConnectingPikmin.Level) and i < 2:
                new_decoded.extend(level.to_bytes().ljust(0x100, b'\x00'))

            else:
                new_decoded.extend(level.to_bytes())
        new_decoded.extend(self.decoded[-LEVEL_FOOTER_LENGTH:])
        if raw_level: return new_decoded

        out = encode(new_decoded, self.raw, partial_encode)
        if not partial_encode: self.raw = out
        return bytes(out)
