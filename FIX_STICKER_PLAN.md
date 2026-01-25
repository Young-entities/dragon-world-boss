# "De-Sticker" Restoration Plan

## The Problem
- The unit has a "White Border" around the weapon, making it look like a cheap sticker.
- Previous attempts failed to remove this border because they preserved the "faint white" pixels.

## The Solution: Geometric Solidification + Aggressive Trimming

### Step 1: The Solid Core (Geometric Fill)
- We define the "Skeleton" of the unit using Blue/Warm colors.
- We **Fill Holes** inside this skeleton. This ensures the Face and Inner Weapon are 100% Opaque Solid. No transparency inside the body.

### Step 2: The "Trimmer" (Edge Shaving)
- To kill the "Sticker Border", we must physically cut it off.
- **Action**: We will Erode (Shrink) the mask boundaries.
    - **General Body**: Shrink by 1 pixel (removes faint halos).
    - **Spear Tip**: Shrink by **3 pixels** (removes the thick white glow/border).

### Step 3: Result
- **Face**: Solid and Clear.
- **Weapon**: Sharp "Ice" edge only. No white fluff/border.
- **Background**: Perfectly deleted.

## Execution script
`surgical_v90_desticker.py`
