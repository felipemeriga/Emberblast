---
title: "feat: Comprehensive TUI Visual Overhaul"
type: feat
status: completed
date: 2026-03-28
---

# Comprehensive TUI Visual Overhaul

## Overview

Overhaul the Emberblast Textual TUI from a functional prototype into a polished, game-friendly RPG interface. The current layout is functional but visually sparse — the map is too small, the character info is incomplete, and the overall feel doesn't match a tactical RPG. This plan restructures the layout, makes the map the visual centerpiece, adds a persistent character badge, and polishes every widget for a cohesive game experience.

## Problem Frame

The current TUI works but doesn't feel like a game:
- Map is small and crammed into one corner with tiny cells
- Character stats panel only shows when it's your turn (should be persistent)
- No enemy detail panel — enemies are a compact list inside the HUD
- Combat log works but has no visual personality
- Action bar is plain text, not the colorful button layout from the design mockup
- No visual feedback during combat (damage numbers, status effects)
- Overall layout proportions waste screen space

## Requirements Trace

- R1. Map must be the visual centerpiece — take maximum available width, with larger cells and clear terrain distinction
- R2. A fixed "character badge" panel must always be visible showing the controlled player's full stats, equipment, and status effects
- R3. Enemy info must be a separate dedicated panel (not crammed into the player HUD)
- R4. Combat log must auto-scroll, be visually structured, and feel like an RPG battle log
- R5. Action bar must show colored keybinding buttons matching the design mockup
- R6. Layout must use Textual's grid system for proper proportional sizing
- R7. All widgets must have consistent visual style (borders, colors, spacing)
- R8. Movement selection must clearly highlight reachable cells and flash the currently selected cell

## Scope Boundaries

- No gameplay logic changes — only rendering and UI layout
- No new Textual dependencies beyond what's already installed
- No changes to the questioner/event/renderer architecture — only what widgets render
- No responsive breakpoints — optimize for standard terminal size (80x24 minimum, 120x40+ ideal)
- Title screen, setup screens, and game over screen are out of scope

## Context & Research

### Relevant Code and Patterns

- `emberblast/tui/screens/battle.py` — Current layout uses `Horizontal`/`Vertical` containers
- `emberblast/tui/widgets/map_grid.py` — Map renders via `_build_grid_text()` returning Rich `Text`
- `emberblast/tui/widgets/player_hud.py` — Combined player + enemy info widget
- `emberblast/tui/widgets/combat_log.py` — RichLog-based scrollable log
- `emberblast/tui/widgets/action_bar.py` — Docked bottom bar with keybinding display
- `emberblast/tui/app.py` — Bridge methods for widget updates
- `emberblast/tui/renderer.py` — Event dispatch with `_refresh_game_state()`
- `emberblast/tui/styles.py` — Shared color constants

### Textual Capabilities (v8.2.0)

- **Grid layout** (`layout: grid`) with `grid-size`, `grid-columns`, `grid-rows`, `column-span`, `row-span` for complex multi-panel layouts
- **ScrollView** with `render_line()` line API for high-performance per-row rendering (ideal for large maps)
- **Reactive properties** (`reactive()`) for automatic widget refresh on state changes
- **VerticalScroll** container for scrollable panels
- **Dock** for fixed header/footer
- **Grid gutter** — `grid-gutter: 1 2` for visually even spacing (terminal cells are ~2x taller than wide)
- **RichLog** for combat log (already in use)

## Key Technical Decisions

- **Switch from Horizontal/Vertical to Grid layout**: The current nested container approach makes proportional sizing brittle. Grid gives direct control over column/row sizing and spanning. Rationale: Grid is the standard Textual approach for multi-panel layouts.

- **Split PlayerHUDWidget into two widgets — CharacterBadge + EnemyPanel**: The current widget tries to do too much. Separate widgets have independent sizing, borders, and update cycles. The character badge stays compact and always visible; the enemy panel can scroll when there are many enemies.

- **Use reactive properties for widget state**: Currently all widgets use manual `self.refresh()` calls. Reactive properties batch updates automatically and make the code cleaner.

- **Map uses wider cells (5 chars) with double-height rows**: Each map cell becomes ` ░░░ ` (5 chars wide) and rows get a blank line between them for visual breathing room. This makes terrain patterns and player tokens much more readable at a glance.

- **Action bar uses a proper button layout**: Instead of "[M] Move  [A] Attack" as plain text, each action gets a bordered box with colored text, matching the design mockup.

## Open Questions

### Resolved During Planning

- **Should the map use ScrollView with line API?** No — the grid is typically 8x8 which fits in any terminal. The Rich Text approach is simpler and sufficient. ScrollView is only needed for maps larger than the visible area.
- **Should we add animations/timers?** Not in this plan. Focus on static visual quality first. Animation (damage numbers floating, turn transitions) can be a follow-up.

### Deferred to Implementation

- Exact CSS pixel values for grid proportions — will need tuning in a real terminal
- Whether `grid-gutter` looks better than explicit border spacing — try both

## Implementation Units

- [ ] **Unit 1: Grid Layout Restructure**

  **Goal:** Replace the Horizontal/Vertical container layout with a proper CSS Grid that gives each panel dedicated space.

  **Requirements:** R1, R6, R7

  **Dependencies:** None

  **Files:**
  - Modify: `emberblast/tui/screens/battle.py`
  - Test: `emberblast/test/test_battle_screen.py` (if exists, otherwise structural tests via existing test suite)

  **Approach:**
  The new BattleScreen layout uses a 2-column, 3-row grid:
  ```
  ┌──────────────────────────────────┬───────────────────┐
  │         Turn Header (span 2)     │                   │
  ├──────────────────────────────────┼───────────────────┤
  │                                  │  Character Badge  │
  │           MAP (large)            ├───────────────────┤
  │                                  │   Enemy Panel     │
  ├──────────────────────────────────┼───────────────────┤
  │        Action Bar (span 2)       │                   │
  └──────────────────────────────────┴───────────────────┘
  │            Combat Log (span 2)   │
  └──────────────────────────────────┘
  ```

  Actually, simpler — keep docked header/footer, use grid for the middle:
  - TurnHeader: docked top
  - ActionBar: docked bottom
  - Middle area: 2-column grid
    - Left (3fr): MapWidget (full height)
    - Right (2fr): Vertical with CharacterBadge (fixed height) + EnemyPanel (auto) + CombatLog (1fr)

  Use `Horizontal` with fr units (which already works) but fix the proportions and add proper IDs for CSS targeting. The key change is giving the map MORE space (use `width: 3fr` for map, `width: 1fr` for right panel) and removing wasted space.

  **Patterns to follow:**
  - Existing `BattleScreen.compose()` pattern
  - Textual's docking for header/footer

  **Test scenarios:**
  - Happy path: BattleScreen composes all expected widgets (turn-header, map-widget, character-badge, enemy-panel, combat-log, action-bar) — verify via `query_one` for each ID
  - Happy path: Widget hierarchy is correct — map is in left column, info panels in right column

  **Verification:**
  - Running the app shows a proportional layout with map taking ~60% width and info panels taking ~40%

- [ ] **Unit 2: Character Badge Widget**

  **Goal:** Create a dedicated, always-visible character info panel showing the controlled player's full stats with visual polish.

  **Requirements:** R2, R7

  **Dependencies:** Unit 1 (layout must have a slot for it)

  **Files:**
  - Create: `emberblast/tui/widgets/character_badge.py`
  - Modify: `emberblast/tui/screens/battle.py` (add to compose)
  - Modify: `emberblast/tui/app.py` (add bridge method)
  - Modify: `emberblast/tui/renderer.py` (update `_refresh_game_state`)
  - Test: `emberblast/test/test_character_badge.py`

  **Approach:**
  A new `CharacterBadgeWidget(Widget)` that renders:
  - Sword emoji + player name (bold, blue) + race
  - Job name + "Lv.X" (orange)
  - HP bar: colored block bar (20 chars) with numeric values
  - MP bar: colored block bar (20 chars) with numeric values
  - Full stats: STR, INT, ACC, ARM, RES, SPD, WILL in a compact grid
  - Position indicator: current grid position (e.g., "Pos: D5")
  - Active status effects (if any)

  Uses reactive properties: `_player = reactive(None)` triggers auto-refresh on update.

  Styled with green border (matching "friendly" color) and dark panel background.

  **Patterns to follow:**
  - Current `PlayerHUDWidget._build_hud_text()` for bar rendering
  - `_build_bar()` helper function (move to shared utils or keep in widget)

  **Test scenarios:**
  - Happy path: Widget renders player name, job, race, level when player data is set
  - Happy path: HP and MP bars render with correct fill ratio
  - Happy path: Stats line shows all 7 attributes
  - Edge case: Widget shows "No player data" when player is None
  - Edge case: HP at 0 renders full red bar with 0/max

  **Verification:**
  - Character badge always visible during battle, showing current player stats
  - Stats update after taking damage, leveling up, using mana

- [ ] **Unit 3: Enemy Panel Widget**

  **Goal:** Create a dedicated scrollable panel showing all enemy information with individual HP bars and status.

  **Requirements:** R3, R7

  **Dependencies:** Unit 1

  **Files:**
  - Create: `emberblast/tui/widgets/enemy_panel.py`
  - Modify: `emberblast/tui/screens/battle.py` (add to compose)
  - Modify: `emberblast/tui/app.py` (add bridge method)
  - Modify: `emberblast/tui/renderer.py` (update `_refresh_game_state`)
  - Test: `emberblast/test/test_enemy_panel.py`

  **Approach:**
  A new `EnemyPanelWidget(Widget)` that renders each alive enemy as a mini-card:
  - "ENEMIES" header with red styling
  - Per enemy: skull emoji + name (red) + job + "Lv.X"
  - Mini HP bar (12 chars) with numeric values
  - Position indicator
  - Dead enemies shown as struck-through or greyed out

  Styled with red border (matching "enemy" color).

  The enemy list is passed separately from the character badge — they have independent update cycles.

  **Patterns to follow:**
  - Current enemy list rendering in `PlayerHUDWidget._build_hud_text()`

  **Test scenarios:**
  - Happy path: Panel renders all alive enemies with name, job, HP bar
  - Happy path: Dead enemies are visually distinct (greyed out)
  - Edge case: Empty enemy list shows "No enemies" placeholder
  - Edge case: Single enemy renders correctly without list artifacts

  **Verification:**
  - Enemy panel updates each turn showing current enemy HP
  - Dead enemies visually change appearance

- [ ] **Unit 4: Enhanced Map Widget**

  **Goal:** Make the map the visual centerpiece with larger cells, better terrain distinction, and clear player identification.

  **Requirements:** R1, R8

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `emberblast/tui/widgets/map_grid.py`
  - Modify: `emberblast/tui/styles.py` (terrain style constants)
  - Test: `emberblast/test/test_map_widget.py`

  **Approach:**
  Increase cell width to 5 characters and add vertical spacing between rows:
  - Each cell: ` ░░░ ` (5 chars) — more visual weight for terrain
  - Row spacing: blank half-row between grid rows for readability
  - Player tokens: 3 chars centered (` GK `) instead of 2
  - Terrain backgrounds: deeper, more saturated colors
  - Grid border: thicker box-drawing characters (`║`, `═`, `╔`, `╗`, `╚`, `╝`)
  - Column headers: spaced to match new cell width
  - Movement highlights: bright pulsing cyan with `▸` markers on highlighted cells
  - Flash cell (selected): inverted bright white background
  - Legend at bottom: larger token previews with full name

  New terrain symbols with more visual texture:
  - Plains: `·.·` (sparse dots)
  - Wall: `███` (solid)
  - Water: `≈≈≈` (water waves)
  - Mountain: `⌂△⌂` (peaks)
  - Forest: `♠♣♠` (trees)

  **Patterns to follow:**
  - Current `_build_grid_text()` structure
  - `_TERRAIN_STYLE` dict pattern

  **Test scenarios:**
  - Happy path: Grid renders with column headers and row labels at new cell width
  - Happy path: Player tokens appear at correct positions
  - Happy path: Terrain types render with distinct symbols and colors
  - Happy path: Highlight cells render with cyan styling
  - Happy path: Flash cells render with inverted styling
  - Edge case: Void cells (value 0) render as blank space at correct width
  - Edge case: Dead players are excluded from rendering

  **Verification:**
  - Map visually dominates the left side of the screen
  - Different terrain types are immediately distinguishable
  - Player tokens are clearly visible with team coloring
  - Movement highlights clearly show reachable cells

- [ ] **Unit 5: Polished Action Bar**

  **Goal:** Transform the action bar from plain text into styled, bordered action buttons matching the design mockup.

  **Requirements:** R5, R7

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `emberblast/tui/widgets/action_bar.py`
  - Test: `emberblast/test/test_action_bar.py` (if exists)

  **Approach:**
  Each action renders as a "button" using box-drawing characters:
  ```
  ┌───────┐  ┌─────────┐  ┌───────┐  ┌─────────┐  ┌───────┐
  │[M]ove │  │[A]ttack │  │[S]kill│  │[D]efend │  │[I]tem │
  └───────┘  └─────────┘  └───────┘  └─────────┘  └───────┘
  ```
  Each button's border color matches its action color from `ACTION_COLORS`. The key letter is bold and highlighted.

  When in "choices" mode, the status line appears above the buttons (or replaces them if actions aren't relevant).

  Increase action bar height from 3 to 4 to accommodate the bordered buttons.

  **Patterns to follow:**
  - Current `_build_bar_text()` approach
  - `ACTION_COLORS` and `ACTION_KEYS` mappings

  **Test scenarios:**
  - Happy path: Actions render with bordered button format
  - Happy path: Each button uses its action color
  - Happy path: Status message displays when set
  - Edge case: Empty action list renders no buttons

  **Verification:**
  - Action bar shows colored bordered buttons during action selection
  - Visual style matches the design mockup

- [ ] **Unit 6: Combat Log Polish**

  **Goal:** Improve combat log visual structure with better formatting, icons, and category-specific styling.

  **Requirements:** R4, R7

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `emberblast/tui/widgets/combat_log.py`
  - Modify: `emberblast/tui/styles.py` (add log category icons)
  - Test: `emberblast/test/test_combat_log_widget.py`

  **Approach:**
  Add category-specific icons/prefixes to log entries:
  - Damage: `⚔` sword icon, red
  - Heal: `✚` cross icon, green
  - Move: `→` arrow, blue
  - Skill: `✦` star, purple
  - Death: `☠` skull, bold red
  - Victory: `🏆` trophy, bold green
  - Narration: `"` quote marks, orange italic
  - Item: `◆` diamond, green
  - Level up: `⬆` arrow up, bold green
  - XP: `★` star, yellow
  - Turn start: larger separator with turn number centered

  Turn headers get a distinct visual treatment:
  ```
  ═══════════ TURN 3 ═══════════
  ```

  The "COMBAT LOG" header gets a proper styled banner.

  **Patterns to follow:**
  - Current `add_entry()` and `on_mount()` pattern
  - `LOG_COLORS` mapping

  **Test scenarios:**
  - Happy path: Widget is instance of RichLog with auto_scroll enabled
  - Happy path: Turn number tracking works via set_turn()
  - Happy path: add_entry and clear_log methods exist and are callable

  **Verification:**
  - Log entries have distinctive icons per category
  - Turn transitions are visually clear separators
  - Log auto-scrolls to newest entries

- [ ] **Unit 7: Wire Everything Together**

  **Goal:** Update the app bridge methods, renderer, and entry point to work with the new widget structure.

  **Requirements:** R2, R3 (persistent updates)

  **Dependencies:** Units 1-6

  **Files:**
  - Modify: `emberblast/tui/app.py` (new bridge methods for character badge and enemy panel)
  - Modify: `emberblast/tui/renderer.py` (update `_refresh_game_state` to update new widgets)
  - Modify: `emberblast/__main__.py` (initial data population for new widgets)
  - Modify: `emberblast/tui/screens/battle.py` (remove old PlayerHUDWidget references)
  - Delete: `emberblast/tui/widgets/player_hud.py` (replaced by character_badge + enemy_panel)
  - Test: `emberblast/test/test_tui_app.py` (update structural tests)

  **Approach:**
  - Replace `update_hud(player)` + `update_enemies(enemies)` with `update_character_badge(player)` + `update_enemy_panel(enemies)`
  - `_refresh_game_state` always finds the controlled player and updates the badge; finds all enemies and updates the enemy panel
  - Initial data population in `__main__.py` uses new bridge methods
  - Remove `PlayerHUDWidget` references everywhere
  - Clean up old test files for removed widget

  **Patterns to follow:**
  - Current bridge method pattern in `app.py`
  - `_refresh_game_state` pattern in `renderer.py`

  **Test scenarios:**
  - Happy path: App has `update_character_badge` and `update_enemy_panel` methods
  - Happy path: BattleScreen composes character-badge and enemy-panel widgets
  - Integration: Renderer `_refresh_game_state` calls badge and panel updates

  **Verification:**
  - Game launches, transitions to battle screen, all panels populated
  - Character badge persists across all turns (doesn't blank out during bot turns)
  - Enemy panel updates after each action (damage, death, movement)
  - Combat log scrolls and shows all events
  - Map highlights work during movement selection

- [ ] **Unit 8: Visual Consistency Pass**

  **Goal:** Final polish pass ensuring consistent borders, colors, spacing, and visual hierarchy across all widgets.

  **Requirements:** R7

  **Dependencies:** Units 1-7

  **Files:**
  - Modify: `emberblast/tui/styles.py` (finalize color palette)
  - Modify: Various widget CSS as needed
  - Modify: `emberblast/tui/screens/battle.py` (final CSS tuning)

  **Approach:**
  - Ensure all panels use consistent border styles (solid borders with appropriate team/category colors)
  - Turn header: orange border
  - Character badge: green border (friendly)
  - Enemy panel: red border (enemy)
  - Combat log: grey border (neutral)
  - Action bar: grey top border
  - Map: orange border
  - Verify spacing between panels is even
  - Ensure dark theme consistency — all backgrounds use `#0d1117` or `#161b22`
  - Test at different terminal sizes to verify proportions

  **Test scenarios:**
  - Happy path: All widgets have non-empty DEFAULT_CSS with border and background
  - Happy path: Color constants in styles.py are consistent across widget usage

  **Verification:**
  - Screenshots of the running game show a cohesive, polished visual style
  - No visual artifacts, overlapping borders, or misaligned panels
  - Layout looks good at both 80-column and 120-column terminal widths

## System-Wide Impact

- **Widget query changes:** `app.py` bridge methods change from `#player-hud` to `#character-badge` and `#enemy-panel` — all query_one calls must be updated
- **Renderer coupling:** `_refresh_game_state()` must update two new widgets instead of one — the controlled player goes to badge, enemies go to panel
- **Test impact:** Tests referencing `PlayerHUDWidget` must be updated or removed
- **CSS specificity:** New grid layout CSS must not conflict with widget DEFAULT_CSS

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Grid layout doesn't render well at small terminal sizes | Set reasonable `min-width`/`min-height` on widgets; test at 80x24 |
| Widget query_one fails during screen transitions | Keep existing try/except pattern with logging |
| RichLog performance with many entries | Already using `max_lines` cap — monitor |
| Box-drawing characters don't render in all terminals | Use Unicode block elements that have broad support |

## Sources & References

- Textual Layout Guide: https://textual.textualize.io/how-to/design-a-layout/
- Textual Grid Styles: https://textual.textualize.io/styles/grid/
- Textual Reactivity: https://textual.textualize.io/guide/reactivity/
- Textual RichLog: https://textual.textualize.io/widgets/rich_log/
- Textual Containers: https://textual.textualize.io/api/containers/
