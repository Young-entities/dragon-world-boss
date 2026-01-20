# Layout Measurements & CSS Reference (Monster Warlord Style)
> **Approved State:** The boss scene layout is now finalized to match the dense, immersive "Monster Warlord" aesthetic.

## 1. Boss Stage (Primary Visual)
Maximized to fill vertical space and push content down.
- **Selector:** `.dragon-stage`
- **Height:** `52vh` (Dominates screen)
- **Width:** `100%` (Full width, no side margins)
- **Margin:** `0` (Touches Header Line)
- **Border:** Top/Bottom only (`2px solid #521`)

## 2. Monster Sprite Positioning
Grounded and massive.
- **Selector:** `#dragon`
- **Height:** `98%`
- **Scale:** `1.1` to `1.15` (via Keyframes)
- **Position:** `relative`
- **Top:** `10px` (Prevents foot cutoff, looks grounded)

## 3. Boss Name & Health Bar (Embedded)
Name is embedded inside the Health Bar for zero-gap layout.
- **Location:** Inside `.boss-bar-frame`
- **Position:** `absolute` overlay
- **Style:** White text, Centered, `z-index: 5`
- **Old Location:** Removed from `.boss-info` (top of HP) to save space.

## 4. Bottom UI Container
 Tightly packed below the stage.
- **Selector:** `.bottom-ui`
- **Padding:** `0 10px 5px 10px` (Bottom 5px minimizes gap to Battle Status)
- **Margin Top:** `0` (Touches Stage)

## 5. Health Bar Spacing
- **Selector:** `.boss-hp-wrapper`
- **Margin Top:** `0`
- **Margin Bottom:** `8px` (Small gap to Attack Buttons)

## 6. Attack Buttons (Warlord Style)
- **Selector:** `.btn`
- **Height:** `60px`
- **Border:** `5px solid` + Color (Blue/Green/Red)
- **Style:** Roundness (`15px`), Bevel (`inset shadow`), No 'X' icon.

## 7. Battle Status / Participants
- **Visibility:** Pushed below the fold (requires scrolling).
- **Position:** Flows naturally after `.bottom-ui`.
- **Note:** Hidden by the fixed Bottom Nav until scrolled.

## 8. Bottom Navigation (Fixed)
- **Selector:** `.bottom-nav`
- **Position:** `fixed`, `bottom: 0`
- **Z-Index:** `9999`
- **Width:** Fixed `480px` (centered) on desktop.
