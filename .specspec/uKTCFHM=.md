---
id: uKTCFHM=
type: implementation
parents:
- APTJ9XE=
sources:
- path: src/poketonieengagementhunt/params.py
---
# Dimensions in params.py

params.py holds the diameter, the measured ratios of band, ring, flat rim and button, and every other dimension of the device as named values, grouped by function and annotated with the research note they come from.

The width of the tongue beside a figure and the ground that is kept free of grass are derived from the diameter of a Tonie's foot, so one value moves both; the length of the tongue follows the reader board. The pilot diameters of the M2 screws, M2_PILOT_FLAT and M2_PILOT_SIDE, are the two values to adjust once the test piece has been printed; HINGE_SLIDE and HINGE_PRESS, the bores for the hinge pins in the towers and in the sleeve, are adjusted in the same way after their own test piece. PRINT_TOL, the play of the hinge that follows from its bores, and the gaps round the lid are the values the checks of play work with. Bounds: the outline of the reader board and the position of its antenna, the height of the controller board, the connector overhang of the charger, the servo horn, the Tonie's foot and the ring are assumptions marked MEASURE. They have to be replaced by measurements of the delivered parts before printing.
