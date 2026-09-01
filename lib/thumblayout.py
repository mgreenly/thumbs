"""The single source of truth for thumbnail geometry.

Every box in a thumbnail is derived here, from a canvas size and the side the
subject stands on. `bin/layout` prints what this computes; `bin/compose` places
layers using the same numbers. Nothing else is allowed to know a coordinate.

The reason for the split is that the generators and the compositor have to
agree. `headline` is handed a `--box WxH` and returns a PNG exactly that size,
which `compose` then drops at an offset. If the box came from one place and the
offset from another, they would drift the first time anything was tuned.

All proportions live in the constants below, expressed as fractions of the
canvas, so a composition change is an edit to one number here and nothing else.
"""

# The reference canvas. Everything is a fraction, so any 16:9 size works, but
# these are the numbers the proportions were eyeballed against.
CANVAS = (2560, 1440)

# YouTube's stated thumbnail size. Rendering above it and downsampling keeps
# the type edges and the gradient banding cleaner than drawing at final size.
EXPORT = (1280, 720)

# --- bottom bar -------------------------------------------------------------

# The bar this layout is descended from runs about 15% of frame height. 14%
# carries the same weight without eating into the headline's descenders.
BANNER_HEIGHT = 0.14

# --- headline ---------------------------------------------------------------

# Distance from the canvas edge to the outer edge of the type column.
HEADLINE_MARGIN_X = 0.0375
# Distance from the canvas top to the top of the type box.
HEADLINE_MARGIN_TOP = 0.10
# Gap between the bottom of the type box and the top of the bar.
HEADLINE_GAP_BOTTOM = 0.045
# The block is anchored to the top of its box rather than centred in it. The
# box runs most of the frame height so that a four-line headline has somewhere
# to go, but a two-line one should not drift down to the middle as a result:
# the first baseline lands in the same place regardless of how many lines the
# copy breaks into.
HEADLINE_VALIGN = "top"
# Where the type column stops on the subject's side. The subject gets the rest.
# Slightly past half, because the subject's silhouette is narrower than its
# bounding box and the gutter reads wider than it measures.
HEADLINE_INNER_EDGE = 0.52

# --- subject ----------------------------------------------------------------

# Trimmed subject height as a fraction of canvas height. Just under 1 so the
# top of the head clears the canvas edge; the body runs off the bottom behind
# the bar.
SUBJECT_HEIGHT = 0.90
# Where the horizontal center of the trimmed subject lands, as a fraction of
# canvas width, measured from the subject's own side. `compose --subject-inset`
# overrides it per attempt; this is the default when nothing is passed.
SUBJECT_CENTER_INSET = 0.26

# The framings, named for the share of the frame the portrait takes: the
# operator says "portrait 1/3 left" or "portrait 3/5 left", and `full` is the
# house half-frame those are alternatives to. Each names a subject height as a
# fraction of canvas height and a center inset as a fraction of canvas width
# from the subject's own side, so the whole of a framing is where the person is
# and how big.
#
# This is about the portrait and nothing else. A stage is drawn wherever the
# stage constants put it, in any framing or none, and the two are tuned
# separately.
FRAMINGS = {
    "full": {"height": SUBJECT_HEIGHT, "inset": SUBJECT_CENTER_INSET},
    "1/3": {"height": 0.6465, "inset": 0.19},
    "3/5": {"height": 0.7800, "inset": 0.28},
}

# --- stage ------------------------------------------------------------------

# The shape the subject stands in front of. There is no fixed circle here,
# because the rule the shape has to satisfy is about the person and not about
# the canvas: the whole of the visible silhouette sits inside the ring, head
# included. That is the smallest circle enclosing the placed cut-out, which
# only `freebox` can measure, since only it looks at the matte. What is fixed
# is the air around the person and the weight of the border.
#
# Air between the silhouette and the inner edge of the ring, as a fraction of
# canvas width. Small: the head is meant to sit *just* inside the border.
STAGE_GAP = 0.02
# Border thickness. Thin enough to read as a drawn edge rather than a second
# shape; the reference measures a shade under this.
STAGE_RING = 0.012

# --- backdrop ---------------------------------------------------------------

# The hotspot follows the type, because the type is black and black is most
# legible over the brightest part of the plate.
HOTSPOT_INSET_X = 0.28
HOTSPOT_Y = 0.30


def _round(v):
    return int(round(v))


def compute(canvas=CANVAS, side="right", subject_inset=None, framing="full"):
    """Return every layer's geometry for one composition.

    `side` names the side the *subject* stands on. The type column takes the
    other side, and the backdrop hotspot follows the type.

    `subject_inset` overrides the default inset for this composition, the
    fraction of canvas width from the subject's own side to its center; smaller
    pushes the subject further into its corner. `None` uses the default.

    `framing` is how big the subject is and where it sits, named for the share
    of the frame the portrait takes: `full` is the house half-frame, `1/3` and
    `3/5` are the smaller ones. It says nothing about the stage. It is not a
    cosmetic flag either: every tool that places the subject has to pass the
    same value or they will disagree about where the person is.
    """
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")
    if framing not in FRAMINGS:
        raise ValueError(
            f"framing must be one of {', '.join(FRAMINGS)}, got {framing!r}")

    frame = FRAMINGS[framing]

    if subject_inset is None:
        subject_inset = frame["inset"]
    elif not 0 <= subject_inset <= 1:
        raise ValueError(
            f"subject_inset must be between 0 and 1, got {subject_inset!r}")

    w, h = canvas
    text_side = "left" if side == "right" else "right"

    banner_h = _round(h * BANNER_HEIGHT)
    banner_y = h - banner_h

    margin_x = _round(w * HEADLINE_MARGIN_X)
    inner = _round(w * HEADLINE_INNER_EDGE)

    # The type column runs from the outer margin to the inner edge, on whichever
    # side the type lives.
    if text_side == "left":
        head_x = margin_x
        head_w = inner - margin_x
    else:
        head_x = w - inner
        head_w = inner - margin_x

    head_y = _round(h * HEADLINE_MARGIN_TOP)
    head_h = banner_y - _round(h * HEADLINE_GAP_BOTTOM) - head_y

    # Type is flush left in its box on both layouts, never flush right. A
    # balanced stack of lines is close enough to rectangular that the ragged
    # edge costs nothing, and a fixed left edge means the copy starts in the
    # same place whichever side the subject is on.
    head_align = "left"

    inset = _round(w * subject_inset)
    subject_cx = w - inset if side == "right" else inset

    subject_h = _round(h * frame["height"])

    hot_x = w * HOTSPOT_INSET_X
    if text_side == "right":
        hot_x = w - hot_x

    return {
        "canvas": {"width": w, "height": h},
        "export": {"width": EXPORT[0], "height": EXPORT[1]},
        "side": side,
        "text_side": text_side,
        "framing": framing,
        "backdrop": {
            "width": w,
            "height": h,
            # Fractional, because that is what `backdrop --hotspot` takes.
            "hotspot": [round(hot_x / w, 4), round(HOTSPOT_Y, 4)],
        },
        "headline": {
            "width": head_w,
            "height": head_h,
            "x": head_x,
            "y": head_y,
            "align": head_align,
            "valign": HEADLINE_VALIGN,
        },
        "banner": {
            "width": w,
            "height": banner_h,
            "x": 0,
            "y": banner_y,
        },
        # Not a circle: the circle is measured off the matte by `freebox`.
        # These are the two numbers that measurement is dressed with.
        "stage": {
            "gap": _round(w * STAGE_GAP),
            "ring": _round(w * STAGE_RING),
        },
        "subject": {
            # compose trims the cutout to its content before applying these.
            "height": subject_h,
            "center_x": subject_cx,
            # The subject is bottom-aligned to the canvas and runs off it.
            "bottom": h,
        },
    }


def geometry_string(box):
    """ImageMagick geometry for a layer dict carrying x/y."""
    return f"{box['width']}x{box['height']}+{box['x']}+{box['y']}"
