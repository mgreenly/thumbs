# thumbs

A toolkit and a conversation protocol for building YouTube thumbnails in the
michaelgreenly.dev visual system. The layout is modeled on the Matt Maher
(`@MetalSole`) thumbnails: subject on one side of the frame, headline on the
other, a full-width bar along the bottom, exactly one accent per image.

This tree is *only* that. Nothing else belongs here. A session is a
conversation with the operator that ends in a rendered thumbnail.

## How work is done

Every session works in a dated folder under Dropbox, never in this tree:

    ~/Dropbox/Thumbs/<YYYY-MM-DD>/

Create it if it does not exist. The operator drops one or more portrait frames
there, sometimes several to experiment with, and gives instructions in prose.
Every generated file (cutouts, backdrops, headline and banner layers, and the
finished composites) is written back to that same folder. Nothing is scattered
into `/tmp`, the scratchpad, or `~/Pictures`. The folder is the whole record of
the session.

Portraits arrive with their studio background intact. Cutting them is the first
step and is not something the operator does. `bin/thumbnail` does it for you,
once, to `<stem>-cut.png` beside the portrait, and reuses that file on later
runs.

Finished composites are always named `thumb-<n>.jpg`, numbered from 1. `<n>` is
the next integer not already used in the folder, so successive attempts
accumulate rather than overwrite and can be compared side by side. Never
re-use a number and never overwrite an earlier `thumb-<n>.jpg`; a rejected
attempt is still part of the record.

`thumb` appears in the name of the finished composite and nowhere else, so a
glob for `thumb-*.jpg` returns exactly the deliverables and nothing else in the
folder. Intermediate layers carry the same number, which keeps each attempt's
inputs beside its output: `<n>-backdrop.png`, `<n>-stage.png`,
`<n>-headline.png`, `<n>-banner.png`, and the layouts `<n>-stage.json`,
`<n>-headline.json` and `<n>-banner.json`. A list writes `<n>-headline.png` and
`<n>-headline.json` too, because it is the headline layer; the layer is named
for its slot, not for whichever generator filled it.

A background photograph the operator drops in the folder is an *input*, not an
attempt, so it carries no number: `background.jpg` or `background.png`, named
by the operator, beside the portrait.

Every attempt also writes `thumb-<n>.svg`, the same composition as an editable
layered file. It carries the composite's number because it is the same attempt,
and it leaves the `thumb-*.jpg` glob returning exactly the deliverables.

Because every attempt writes fresh filenames, nothing in the sequence needs
`--force`. All the tools refuse to overwrite by default, so a repeated `<n>`
fails loudly instead of destroying an earlier attempt. Do not add `--force` to
work around that; take the next number.

## Running it

One command builds the whole thing. `$D` is the dated folder:

    bin/thumbnail "$D/portrait.png" --side left \
      -t 'I walk through how my *SPEC* harness works'

That cuts the portrait if it has not been cut, builds the plate, solves the
headline into the largest empty space beside the placed subject, draws the
banner, and writes both `thumb-<n>.jpg` and `thumb-<n>.svg` into the portrait's
own folder at the next free number. It prints the JPEG's path. Everything the
operator did not name takes its default.

The type layer is a headline or a numbered list, never both:

    bin/thumbnail "$D/portrait.png" --side left \
      --item 'gather' --item '*build*' --item 'verify'

The flags it exposes are the ones the operator actually varies:

    --side left|right      which side of the final image the subject stands on
    --mirror               flip the subject horizontally
    -t COPY                headline copy; *word* is an accent
    --lines N              rebreak the headline into N lines (default 3)
    --item COPY            one list row; repeat in order. Excludes -t
    --start N              number the first list row N (default 1)
    --shape wide|tall      the shape of box to look for; defaults to the one
                           that suits the layer asked for
    --banner COPY          bar copy
    --tint HEX             plate tint; omit for a neutral gray wall
    --strength F           how far to push the tint (default 0.20)
    --background PATH      a photograph as the plate instead of the gradient
    --framing F            the share of the frame the portrait takes: full,
                           1/3 or 3/5 (default full)
    --stage circle         a shape behind the subject; off unless asked for
    --stage-fill COLOR     the stage's flat field (default a near-plate neutral)
    --stage-ring COLOR     the stage's border (default #18181B)
    --subject-inset FRAC   subject center as a fraction of width from its own
                           side; smaller pushes it further into its corner and
                           leaves the headline more room (default 0.26)
    --font / --accent-font re-face the type
    --recut                re-run the cut even though `<stem>-cut.png` exists

Anything past that, drop down to the individual tools. `thumbnail` wraps them,
it does not replace them, and it is a short script: read it to see the exact
sequence it runs.

To see where the type is going to land before rendering:

    bin/freebox --subject "$D/portrait-cut.png" --side left --format table
    bin/freebox --subject "$D/portrait-cut.png" --side left --shape tall

And to see the circle a stage would draw:

    bin/freebox --subject "$D/portrait-cut.png" --side left --framing 1/3 \
      --find stage

Pass `freebox` the same `--side`, `--mirror`, `--subject-inset`, `--shape` and
`--stage` as the render, or its box describes a composition nobody is building.

## The dialog

The operator speaks in these terms, each mapping to exactly one argument. Do
not invent synonyms and do not guess at a term that was not used.

| Operator says | Becomes |
|---|---|
| `portrait left` / `portrait right` | `--side` (the side of the **final image** the portrait sits on), at `--framing full` |
| `portrait 1/3 <side>` / `portrait 3/5 <side>` | the same `--side`, at `--framing 1/3` or `--framing 3/5` |
| `mirrored` | `--mirror` (flip the subject horizontally; off unless said) |
| `headline in N lines: <copy>` | `--lines N -t '<copy>'` |
| `list with:` then one item per line | `--item '<copy>'` per row, in order |
| `wide list` / `tall headline` | `--shape` (otherwise inferred from the layer) |
| `banner: <copy>` | `--banner '<copy>'` |
| `backdrop: <color in words>` | `--tint '<hex>'` |
| `use the background` | `--background "$D/background.<ext>"`, the image in the folder instead of a generated plate |
| `stage` | `--stage circle` |
| `stage in <color in words>` | `--stage-fill '<hex>'` |
| "stronger" / "more subtle" | `--strength` (default 0.20) |
| "give the headline more room" | `--subject-inset` below 0.26 |

Those three terms stack in one order, which is the order of the layers. The
plate is a generated backdrop unless the operator says `use the background`, in
which case it is the image in the folder. A `stage` goes in front of whichever
of the two is there and behind the portrait. And the fraction in
`portrait 3/5 left` says how big the portrait is and where it sits.

The fraction and the stage are independent, and deliberately so. The fraction
sizes the portrait and says nothing about the shape; the stage is drawn where
its own constants put it, in any framing or none. Do not infer one from the
other in either direction.

A word wrapped in `*asterisks*` is an accent, in the headline, the list and the
banner alike. The operator calls these earmuffs. Accents survive `--lines`
rebreaking.

A list is dictated one item per line, and the operator writes their own `01 - `
prefixes to say which item is which. **Those numbers are decoration.** Strip
them and pass only the copy: `list` numbers the rows itself, so the markers can
never fall out of step with the items and a typo cannot reach the render. When
the numbering should genuinely start somewhere other than 1, that is `--start`,
not a number typed into the copy.

    list with:
    01 - gather
    02 - *build*
    03 - verify

becomes `--item 'gather' --item '*build*' --item 'verify'`.

Line breaks are never dictated, only the line *count*. `--lines` measures with
the real faces and picks the breaks that minimize the widest line, which is
also what maximizes the type size.

The subject is never mirrored unless the operator says `mirrored`. Mirroring
flips the subject horizontally, so a gesturing hand can be made to point into
the type rather than off the frame, but it is not derived from the side and is
not applied on your own initiative. Default to no `--mirror`; add it only when
the operator uses the word.

**Every setting has a default; never ask for one.** When the operator does not
specify something, use its default and proceed. A session names only what
differs from the defaults, and an unspecified setting is an answered question,
not an open one. The defaults are:

- **Headline:** none. No headline layer is drawn unless the operator gives
  headline copy. Skipping it is the normal case, not an omission to flag.
  When there is copy, it is set in 3 lines, with the drop shadow on.
- **List:** none, and never both a list and a headline. When there are items,
  they are numbered from 1, zero-padded to two digits, set in IBM Plex Mono at
  `#18181B` and 0.8 of the label size, with the drop shadow on. The block is
  centered in its box and the rows are flush left inside it.
- **Banner:** the copy defaults to `https://michaelgreenly.dev`.
- **Backdrop:** a neutral gray wall (no `--tint`) at `--strength 0.20`, unless a
  color or "stronger"/"more subtle" is named. A photograph is used only when the
  operator asks for one; a `background.jpg` sitting in the folder is not itself
  the instruction to use it.
- **Stage:** none. Nothing sits between the plate and the subject unless the
  operator asks for a shape. When they do, it is the disc that just holds the
  whole visible portrait, filled `#DEDCDE` (the middle of the wall `backdrop`
  builds its gradient between) with a `#18181B` ring. Its size is measured, not
  named, and it does not change the portrait's size; the framing does that.
- **Subject:** `--framing full`, `--side right`, no `--mirror`, cut with
  `birefnet-portrait` and no alpha matting. The framing carries the height and
  the inset; `full` is 0.90 of frame height at inset 0.26.
- **Type placement:** computed by `freebox` from this frame's negative space,
  centered in the box it finds. The box is `--shape wide` for a headline and
  `--shape tall` for a list.

## The tools

- `bin/thumbnail` — the whole pipeline in one command. This is what a session
  runs.
- `bin/thumblayout.py` — every fixed coordinate in the system, as fractions of
  the canvas. **No other file may know a geometry number.**
- `bin/layout` — prints those boxes as `json`, `sh`, or `table`.
- `bin/freebox` — per-frame geometry measured from the placed subject's
  silhouette. `--find box` is the type layer's box, computed from the negative
  space rather than taken from the fixed column, with `--shape` picking which
  proportions it may have; `--find stage` is the circle that holds the whole
  visible subject, which is what the stage draws.
- `bin/unback` — rembg segmentation; portrait to transparency.
- `bin/backdrop` — the tinted gradient plate, or a photograph cover-cropped to
  the canvas with `--image`. Opaque; everything else is not.
- `bin/stage` — the shape the subject stands in front of, drawn on the full
  canvas between the plate and the subject. `--form` picks the shape.
- `bin/headline` — the only text engine in the tree. `banner` shells out to it;
  `list` imports it.
- `bin/list` — a numbered list in the headline's slot, for the frames whose copy
  is a set of things rather than a sentence. Same box, same kind of PNG, same
  kind of layout dump, so nothing downstream can tell the difference.
- `bin/banner` — the bottom bar plus its copy.
- `bin/compose` — trims, scales, places, flattens, downsamples to 1280x720.
- `bin/layered` — the same composition as an Inkscape SVG, one named layer
  each. Takes `compose`'s arguments, plus the type layouts.
- `.venv/` — rembg and ONNX Runtime, used only by `unback`.

Each tool's docstring is the reference for its own flags. Read it there rather
than restating it here.

## Where the headline goes

`thumblayout` gives the headline a fixed column on the side opposite the
subject. That is the Maher grid and it is right when the subject is a clean
half-frame silhouette. It wastes space the moment the subject is small, off in
a corner, or reaching a hand into what would otherwise be the type column: the
column cannot move, so the type shrinks to dodge the hand instead of sitting
beside it.

`bin/freebox` computes the alternative. It places the subject exactly as
`compose` will (trimmed, scaled, centered at the inset, optionally mirrored),
marks the banner and a margin as occupied too, and finds the largest empty
axis-aligned rectangle that is still headline-shaped. The mask is the real
silhouette, not its bounding box, which is the whole point: a raised finger
blocks its own few hundred px and the rectangle tucks in beside it. `compose`
and `layered` take that rectangle as `--headline-box WxH+X+Y`; without it they
fall back to the fixed column.

Two constants in `freebox` are the composition, and are settled:

- `MARGIN = 0.04`, the air the box keeps from the silhouette, the bar, and the
  frame edges alike. The occupancy is dilated by it and the edges are inset by
  it, so the clearance is even on all sides. Larger shrinks the box and the
  type with it; 0.08 was tried and read as too much air and too small a
  headline.
- `SHAPES`, the band a winning rectangle's `w/h` must fall in, so a thin
  full-width strip never beats a chunky block. There are two, because there are
  two kinds of type block. `wide` is the headline's and is the default. `tall`
  is the list's: a column of rows cannot fill a short wide box and would only
  shrink to fit one, so the band that suits three lines of a sentence is the
  wrong band for five items. Out-of-band rectangles are discarded outright
  rather than penalized; a preference would let a big enough strip win anyway,
  which is the failure the band exists to prevent.

Treat both as locked, the same as the proportions in `thumblayout.py`. The
`tall` band in particular has been through one composite, not the dozen the
`wide` one has, so it is the first number to revisit if a list lands badly.

## The stage

The subject is an actor, the backdrop is behind everything, and the stage is the
shape between them. It is one metaphor and the layer names follow it.

It exists for the halo. A cut-out's edge is a few pixels of semi-transparent
hair, and how much of it you see depends entirely on what is behind it: against
a photograph or a gradient the fringe reads as a rim of the wrong color, and
against a flat field near its own value it disappears. So the fill is not
decoration, and "a color near the plate" is the whole trick. The ring is what
keeps a near-plate fill from reading as a smudge instead of a shape.

**The disc has no size of its own, and there is no way to give it one.** The
rule is about the person rather than the canvas: the whole of the visible
subject sits inside the ring, head included. That is the smallest circle
enclosing the placed silhouette, so `freebox --find stage` measures it off this
frame's matte and `thumbnail` hands the result to `stage`. Change the framing
and the disc follows, because the person it has to hold changed size. Mirror
the subject and it follows again: a silhouette is not symmetric, so the circle
is refit rather than flipped.

Only what the viewer sees counts. Below the bar the body is covered anyway, and
fitting those pixels would drag the circle down and out for nothing.

Two constants dress that measurement, and they are the only stage numbers:
`STAGE_GAP` (0.02 of width), the air between the silhouette and the inner edge
of the ring, and `STAGE_RING` (0.012), the border's weight. `freebox` fits the
same circle for its own occupancy when `--stage` is passed, so a headline is
kept off the real disc rather than off a guess at it.

The framing is separate, and is not a flag one tool can hold on its own.
`FRAMINGS` says how tall the portrait is and where its center goes, one entry
per fraction the operator can say. `compose`, `layered` and `freebox` all place
the subject, so all three take `--framing`, and `thumbnail` resolves it once and
passes it to each: they share a default, but a default agreed on in three places
is a disagreement waiting to happen.

Unlike the rest of the composition, `FRAMINGS` is **not settled**. `1/3` and
`3/5` were approved against composites of one portrait, so they are the first
numbers to revisit when a frame lands badly.

## The layered file

`thumb-<n>.svg` is the attempt as named Inkscape layers (backdrop, stage,
subject, headline, banner, whichever of them the attempt has) for the case where
the composition is right and one word wants nudging by hand. Open it, move the thing, export at 1280x720. It is
a hand-off, not a second renderer, and nothing downstream reads it.

The plate and the subject are linked PNGs, because a grain-flecked gradient and
a photograph gain nothing from being described in XML. Links rather than
embedded data, so the SVG stays small and the dated folder stays the one copy
of everything. Moving the SVG out of its folder breaks its links.

The stage is a live shape for the same reason the type is live text: a disc is
three numbers and two colors, so it loses nothing in XML and gains being
draggable. `stage --dump-layout` writes those numbers and `layered` redraws them
as an SVG circle rather than linking the PNG.

The type is live text, and that is the point. `--dump-layout` makes `headline`,
`list` and `banner` write out the pointsize the solver landed on and the x and
baseline of every segment, so `layered` can pin each word exactly where
ImageMagick drew it. A segment may carry its own pointsize and letter spacing,
overriding the document's, which is how a list's markers come out smaller than
its labels while sharing their baselines. Inkscape never re-breaks a line or re-spaces a word; the
copy is editable without being re-laid-out. Drop the two `--dump-layout` flags
and the layers are linked PNGs instead: still layered, no longer editable.

The rendered SVG is not pixel-identical to the JPEG and is not meant to be.
Different rasterizers hint glyphs and resample images differently, which is a
few percent of edge noise and no positional drift.

## Standing rules

**The composition is locked.** The proportions in `thumblayout.py` and the
constants in `freebox` were settled by eye against rendered composites and
approved. Change one only when the operator asks for that change. Tuning them
to make a particular headline fit is wrong; change the line count or the copy
instead.

**The palette is the site's, and it has no yellow and no red.** `#2563EB`
accent, `#18181B` text and bar, `#FFFFFF` bar copy. Maher's yellow bar becomes
a dark bar, and his rotated red badge is deliberately not implemented. Blue
means exactly one thing everywhere: the accent.

**Faces.** IBM Plex Sans SemiBold sets the headline, Space Grotesk Bold its
accents, IBM Plex Mono the banner. All three are installed in
`~/.local/share/fonts`. Ask ImageMagick for the exact name
(`IBM-Plex-Mono-Medium`, not `IBM Plex Mono`); some weights register as their
own family rather than as a style. Bebas Neue
(`--font Bebas-Neue-Regular --accent-font Bebas-Neue-Regular`) has been tried
and is not the house default.

**The cut is the model's, not a threshold's.** `unback` defaults to
`birefnet-portrait`, which holds a raised pointing finger that
`isnet-general-use` lops off. Alpha matting is opt-in (`--matting`) because on
a gesturing subject over bright cloth it re-solves solid limbs as
semi-transparent. Do not turn either default around to fix an edge; recut with
a different model and look at it.

**Render high, export once.** Work at 2560x1440 and let `compose` downsample.
Type edges and gradient banding both survive that better than being drawn at
final size.

## The tree stays minimal

This file and `bin/` are the whole project. There is no README, no notes file,
and no scratch work here. Earlier ones were deleted because they documented a
pipeline that no longer exists, and a stale document is worse than none. If
something needs saying, it is said here. Session work lives in the dated
Dropbox folder, never in this tree.
