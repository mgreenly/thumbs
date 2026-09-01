# thumbs

A toolkit for building YouTube thumbnails to one fixed layout: subject on one
side of the frame, headline on the other, a full-width bar along the bottom,
exactly one accent per image.

One command builds a whole thumbnail:

    bin/thumbnail portrait.png --side left \
      -t 'I walk through how my *SPEC* harness works'

It cuts the portrait out of its background, builds the plate, solves the
headline into the largest empty space beside the placed subject, draws the
banner, and writes `thumb-<n>.jpg` plus an editable `thumb-<n>.svg` beside the
portrait.

`bin/` holds the individual tools the pipeline wraps. See `AGENTS.md` for the
full reference: the layout system, the dialog it is driven by, and the rules
the composition is locked to.
