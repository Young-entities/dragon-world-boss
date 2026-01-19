# Layout Measurements & CSS Reference
> **Important:** Do not modify these values without user approval. These settings control the precise layout of the boss battle UI to prevent gaps and overlap.

## 1. Top UI Wrapper
Pushing content down to avoid overlap with device notches/status bars.
- **Selector:** `.top-ui-wrapper`
- **Padding Top:** `15px`
- **Padding Bottom:** `10px`
- **Position:** `relative` (Not sticky currently)

```css
.top-ui-wrapper {
    padding-top: 15px;
    padding-bottom: 10px;
    /* ... */
}
```

## 2. Bottom Navigation (Fixed)
Fixed to the bottom of the viewport.
- **Selector:** `.bottom-nav`
- **Bottom:** `0`
- **Margin:** `0` (Removed negative margins)
- **Transform:** `none` (Removed translateY)

```css
.bottom-nav {
    position: fixed;
    bottom: 0;
    margin: 0;
    /* ... */
}
```

## 3. Boss Battle Status Panel
Positioned right above the bottom navigation.
- **Selector:** `.sticky-status-info`
- **Margin Top:** `20px` (Pushes it down below the nav bar so it doesn't peek through)
- **Transform:** `none`

```css
.sticky-status-info {
    margin-top: 20px;
    /* ... */
}
```

## 4. Bottom UI (Attack Buttons & Health)
Container for the attack buttons and boss health bar.
- **Selector:** `.bottom-ui`
- **Padding:** `10px 10px 15px 10px` (Extra 15px at bottom covers the "lava gap" above nav bar)
- **Background:** `linear-gradient(0deg, #111 20%, transparent 100%)`

```css
.bottom-ui {
    padding: 10px 10px 15px 10px;
    /* ... */
}
```

## 5. Buttons & Health Bar Spacing
- **Selector:** `.boss-hp-wrapper`
  - **Margin:** `0 auto 15px auto` (Spacing between HP bar and buttons)
- **Selector:** `.btn-row`
  - **Margin Bottom:** `0` (No extra space below buttons, handled by container padding)

## 6. Boss Name & Health Bar Gap
- **Selector:** `.boss-info`
  - **Margin Top:** `0`
  - **Margin Bottom:** `-2px`
- **Selector:** `.phase-msg`
  - **Height:** `0` (To close gap)
  - **Margin:** `0`

## 7. Dynamic Text Changes
- **Boss Name Phase 2:** Removed "(Armored)" suffix. Name is always "Dark Overlord".
- **Phase Logic:** (Javascript Line ~1381) `el.bossName.textContent = "Dark Overlord";`
