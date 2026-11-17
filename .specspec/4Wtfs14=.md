---
id: 4Wtfs14=
type: implementation
parents:
- 4-FOgn4=
- uuRV-lo=
sources:
- path: src/poketonieengagementhunt/parts_core.py
  symbol: stage
- path: src/poketonieengagementhunt/parts_core.py
  symbol: cradle
- path: src/poketonieengagementhunt/parts_core.py
  symbol: slider
- path: src/poketonieengagementhunt/checks.py
  symbol: check_ring_lock
---
# Stage with ring cradle and lock

The stage is the inner dome with the flat deck, the collar that centres the lid, the four screw wells and the guide for the lock pin. The cradle drops into a pocket in the deck and is kept captive by the pin in both slider positions. The slider holds the pin and clicks into two dimples.

The checks confirm that the locked pin collides with a ring lifted by 2 mm, that the ring lifts out freely when the pin is withdrawn, and report 0.3 mm of lift play and 0.6 mm of side play before felt.

Bounds: the ring dummy is a typical solitaire; the real ring decides the cradle's dimensions.
