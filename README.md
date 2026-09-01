# thumbs

Build a YouTube thumbnail by describing it. You drop a portrait in a folder,
say what you want in a handful of set phrases, and get back a finished 1280x720
JPEG plus a layered SVG you can nudge by hand.

The layout is fixed and deliberately so: subject on one side of the frame, type
on the other, a full-width bar along the bottom, exactly one accent per image.
You are choosing the content and a few knobs, not inventing a composition.

## The layers

Five layers, always in this order, bottom to top. Only the subject and the
banner are always there.

**Backdrop** is the plate everything sits on. By default it is a soft gray
wall. You can tint it any color, push the tint harder or softer, or replace it
outright with a photograph you drop in the folder.

**Stage** is a shape sitting between the backdrop and the subject, and it is
off unless you ask for it. It is a disc, sized to hold the whole visible
person, filled a shade near the wall with a dark ring around it. Its job is the
cut-out's edge: a few pixels of semi-transparent hair read as a colored fringe
against a photo or a gradient, and disappear against a flat field near their
own value.

**Subject** is you, cut out of your studio background. That cut happens
automatically the first time and is reused afterward. You pick which side of
the frame you stand on, how much of the frame you fill, and whether you are
flipped left-to-right, which is how a gesturing hand can be made to point into
the type rather than off the edge.

**Headline or list** is the type, and it is one or the other, never both. A
headline is a sentence broken over a few lines. A list is numbered rows for
when the copy is a set of things rather than a sentence. Either way it lands in
the largest empty space left beside you, measured off your actual silhouette,
so a raised finger gets tucked in beside rather than crowding the words.

**Banner** is the bar along the bottom, carrying a URL or a short line of copy.

## The vocabulary

You say these; everything else takes its default. Naming a setting is how you
change it, so a short request is a normal request, not an underspecified one.

| You say | What it does |
|---|---|
| `portrait left` / `portrait right` | which side of the finished image you stand on |
| `portrait 1/3 left` / `portrait 3/5 right` | the same, but you fill a third or three-fifths of the frame instead of all of it |
| `mirrored` | flip yourself left-to-right |
| `headline in 3 lines: <copy>` | the headline, and how many lines to break it into |
| `list with:` then one item per line | a numbered list instead of a headline |
| `wide list` / `tall headline` | ask for a differently shaped block of type than the default for that layer |
| `banner: <copy>` | the copy in the bottom bar |
| `backdrop: deep navy` | tint the wall |
| `stronger` / `more subtle` | push that tint harder or softer |
| `use the background` | use the photograph in the folder as the plate instead of the wall |
| `stage` | add the disc behind you |
| `stage in warm gray` | and give it a fill color |
| `give the headline more room` | shift yourself further into your corner |

Two conventions run through all the copy:

**Earmuffs** mark the accent. A word wrapped in `*asterisks*` is set in the
accent face and the accent color, in a headline, a list row, or the banner
alike. One accent per image is the house style, not a limit.

**You never dictate line breaks**, only the line count. The breaks are solved
with the real fonts to keep the widest line as narrow as possible, which is
also what makes the type as large as possible. Same for list numbering: you
write the items, the numbers are added for you, so they cannot fall out of step
with the rows.

## Output

Every attempt writes into the same dated folder, numbered so nothing is ever
overwritten and successive tries can be compared side by side:
`thumb-1.jpg`, `thumb-2.jpg`, and so on. Each one comes with a `thumb-<n>.svg`,
the same composition as named, editable layers, for when the composition is
right and a single word wants moving by hand.

## Under the hood

`bin/` holds the tools, one per layer plus `bin/thumbnail` which runs the whole
pipeline in a single command. `lib/` holds the geometry, which is the one place
any coordinate is allowed to live. `AGENTS.md` is the full reference: every
flag, the constants the composition is locked to, and why each one is what it
is.
