---
id: cz4F_cg=
type: requirement
parents:
- 4OBUPS8=
---
# The blue reader board lies under the standing spot, its antenna 3 mm below the Tonie's foot

The reader is the common blue PN5180 board (69.6 x 38.6 mm). It lies in the tongue with its components down and its plain side against the 1.6 mm turf, the centre of its antenna exactly under the standing spot. The antenna copper is 1.7 to 3.3 mm below the foot of a figure; in revision one it was 10.6 mm. The tag itself is an upright ferrite rod further up inside the figure, in classic Tonies 20 to 50 mm above the underside. It couples to the vertical field on the axis of the antenna, which is why the spot is centred on it.

Why components down: the standing surface stays one plane, and the wires leave on the lower side. Turned over, the copper would be 1.6 mm closer, but the parts on the board would need a step in the surface.

The board sets the length of the tongue at both ends. Its header end has to stay in front of the belly of the ball, which bulges over a tongue of 15 mm; the place of the figure therefore lies 87 mm in front of the ball's axis, and each of the four figures on it stays 11 mm clear of the ball. Its antenna end reaches 20.8 mm beyond the centre of the figure, and the tongue stops 3.2 mm in front of its pocket.

The figure is recognised by the UID of its ISO 15693 tag after the SLIX-L privacy unlock (GET RANDOM NUMBER, then SET PASSWORD with the bytes 5B 6E FD 7F).

Twelve wires join the tongue to the controller: ten for the reader, one for the hall switch and a spare. They are soldered to the board, because a pin header does not fit under the turf, and end in two 6-pin plugs inside the ball.

The antenna copper lies 11.7 mm above whatever the tongue stands on, a little more than the 10 mm that TI's antenna guide asks for between an antenna and a metal surface. In revision two it was 3.2 mm.

Open risks, to be closed on the bench before printing: how high the tag sits in the Pokémon figures and whether this antenna reaches it with reserve; and a metal table under the tongue, for which a ferrite sheet on the floor of the pocket is the untested remedy. One forum screenshot is so far the only evidence that the Pokémon figures carry the same SLIX-L tag as every Tonie.

Origin: agent conclusion from research/01_tonie_rfid_tag.md, research/02_rfid_reader_modules.md, research/08_blue_board_mechanics.md and research/09_tonie_figure_dimensions.md.
