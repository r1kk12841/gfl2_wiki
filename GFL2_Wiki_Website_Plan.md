# GFL2: Exilium Wiki — Website Build Plan

**For: Gemini (build agent)**
**Source file:** `GFL2_Official_Release_Info_Compilation.xlsx`
**Goal:** Turn this spreadsheet into a browsable wiki website, built with Python. Data entry is manual (via a purpose-built form), not scraped from the spreadsheet programmatically.

## 0. How to use this document

Work through the phases in order. Phase 1 (build the data-entry tool) unblocks Phase 2 (actually entering all the data), which unblocks everything else — the site generator has nothing to render until real JSON files exist. Where this document says "flag to the user" or "decide," stop and ask rather than guessing.

---

## 1. Project Summary

The source file is a community-maintained "info sheet" for the gacha game *Girls' Frontline 2: Exilium* — one tab per playable character plus a few reference tabs (weapons, FAQ, navigation). It's built for humans reading it in Excel/Sheets: hand-placed images, merged cells, free-form layout, no two character tabs shaped quite alike. Rather than reverse-engineering that layout in code, the plan is to read each tab by eye and re-enter the data through a small structured form, which then saves clean, consistent JSON. That JSON is what the actual wiki site is generated from.

**Final product:** a statically generated HTML site (character pages, weapons page, FAQ, search/filter), built once and hosted as flat files — see Section 4 for why static over a live server.

**Reference site:** [dandegate.net/dolls](https://dandegate.net/dolls) is an existing GFL2 database site covering the same ground (dolls, weapons, keys, effects). Use it to calibrate terminology and information architecture, not as something to copy — its content/design belong to that site. Two structural choices worth borrowing:
- A character page is a header block (portrait, name, **rarity** (Elite/Standard — confirmed, see Section 2), **class**, **phase** i.e. the character's primary elemental damage type, **ammo type**, and a link to their **signature weapon**) followed by content split into Introduction / Skills / **Fortification** / Keys.
- The doll index page filters on Class, Phase, Ammo Type, Rarity, and **Weapon Type** (Assault Rifle, SMG, Shotgun, MG, Sniper Rifle, Handgun, Blade) — a separate axis from Ammo Type (Light/Medium/Heavy/Shotgun/Melee).

These are folded into the schema and form below. "Phase" isn't a labeled field in the source spreadsheet — it shows up inside skill description text (e.g. "dealing Physical damage") — so it'll need to be read off the skill text during entry rather than copied from a single cell.

---

## 2. Source Data Reference

Useful context for whoever does data entry — what to expect on a typical character tab, and a few naming irregularities worth knowing about up front so they don't cause confusion mid-entry.

**Tab categories in the source file:**
- `Home` — credits + a changelog note. Not a wiki page; fold the credits text into the site's footer/about page.
- `Quick Links` — a navigation grid linking to every character/weapon tab. Treat this as the **authoritative list and display order** of what currently counts as a character vs. a weapon, rather than trusting the raw tab-name list (see the `OTs-14` note below).
- `FAQ ` — a handful of plain Q&A pairs.
- `Weapons ` — a list of weapons, each with an image, name, and rarity.
- **~63–65 character tabs**, each typically containing:
  - Unit Information: Class, HP / ATK / DEF, Skill Attribute, Weakness, Stability Gauge, Movement Speed, and a glossary of the status-effect terms used on that page
  - Rarity — confirmed Elite/Standard. The sheet's own text sometimes phrases this as a star count instead (e.g. Groza's tab says "Being a 4\* unit...") — map star-count phrasing to Elite/Standard during entry; flag any that don't map cleanly.
  - Skills: for each skill — name + tags (Basic Attack / Active / Buff / Debuff etc.), Stability Damage, Cooldown, Confectance Cost, Range, Effect Area, and a description (often with scaling values written as slash-separated levels, e.g. `10%/15%/20%/20%`)
  - Fortification (labeled **"Vertebrae Upgrade"** on the sheet) — a fixed set of 6 upgrade tiers (Fortification Lv 1–6), each one modifying a specific skill. Each tab has a clean summary table near the bottom (columns: Icon / Vertebrae / Skill / Level / Effect, six rows) — enter from that table rather than the scattered inline mentions that also appear next to each individual skill higher up the tab.
  - Neural Helix — a table immediately below Fortification, combining two things the schema treats separately (see Section 6): flat stat-boost nodes (Enhancement 1–6, e.g. "ATK +25 | DEF +23") unlocked at set character levels, and each Key's true unlock info (name, required character level, effect text, material cost) for Fixed Keys 1–6, the Affinity Key, Common Key, and Expansion Key.

**Out of scope, present on the sheet but deliberately not captured:** Suggested Path, Recommended Weapon(s), Recommended Attachment, Substat priority, and the "main"/"F2P" Recommended Key loadout. These are subjective build advice rather than fixed game data — v1 captures the objective Neural Helix/Key unlock info instead (see Section 6). Revisit if the site later wants a "builds" section.

**Irregularities to know about before entering data (don't silently paper over these — flag to the user):**
- `Jiangyu` and `Jiangyu(old)` both exist — almost certainly a pre-rework/post-rework pair. Decide whether "(old)" becomes a "previous version" note on Jiangyu's page, a separate archived entry, or is skipped.
- `Nemesis Gnosis` exists alongside `Nemesis` — reads like an alternate mode/awakened state rather than a distinct character. Recommend entering it as a section within Nemesis's record rather than a standalone one, but confirm.
- `OTs-14` looks like a character tab name but is actually **a weapon** (it appears as a "Recommended Weapon" value on other characters' tabs). Don't assume every tab that isn't in an exclude-list is a character — check what's actually on it.
- Tab names often carry stray whitespace (e.g. `'Groza '`). Trim before using a name anywhere (slugs, titles, filenames).

This context matters mainly so the person doing data entry (Section 7) knows what fields to expect and doesn't get tripped up by the duplicate/mislabeled tabs.

---

## 3. Scope

**In scope (v1):**
- Character index page (grid, filterable by class, phase, ammo type, weapon type, rarity) + one detail page per character
- Weapons index + detail
- FAQ page
- Home/about page carrying over the original credits
- Client-side search across character/weapon names
- Responsive (mobile-usable) layout

**Explicitly out of scope for v1** — note these back to the user as future options, don't build them speculatively:
- User accounts, comments, page-edit history (i.e., a *real* wiki engine like MediaWiki)
- Automated re-parsing of the spreadsheet if it updates (data entry stays manual — see Section 7's "editing" mode for how updates get handled)
- Structuring the slash-separated skill scaling values (`10%/15%/20%`) into per-level data — store as-is, as text
- Damage calculators, team builders, or any interactive game-logic tooling

---

## 4. Architecture & Tech Stack

**Recommendation: a Python-built static site**, fed by manually-entered JSON. Reasoning: the content only changes when a new character releases (infrequent, batch-style), the site is read-only for visitors, and static hosting is free with effectively zero maintenance.

| Layer | Choice | Notes |
|---|---|---|
| Data entry | A single-page HTML/JS form (Section 7) | Runs entirely in the browser, no backend needed |
| Data store | JSON files, one per character, checked into the repo | Human-readable, diffable in git — this is the site's "database" |
| Data validation | `pydantic` | Run against every JSON file before build; fail loudly on missing required fields |
| Templating | `Jinja2` | Standard, no framework lock-in |
| Site builder | A small custom Python script | Reads `/data`, renders templates, writes `/dist` |
| Styling | Plain CSS (or Tailwind via CDN, no build step) | Keep it framework-light |
| Search/filter | Fuse.js or Lunr.js via CDN, vanilla JS | No JS build tooling needed |
| Hosting | GitHub Pages (or Cloudflare Pages / Netlify) | Free, serves a static `dist/` or `docs/` folder |

No spreadsheet-parsing libraries (`openpyxl`, image extraction, etc.) are needed for this pipeline — the spreadsheet is a reference document a human reads, not an input the code touches.

---

## 5. Repository Layout

```
gfl2-wiki/
  data/
    characters/*.json          # one file per character, keyed by slug — filled in via the entry tool
    weapons.json
    faq.json
  assets/
    images/characters/<slug>/  # portrait.png, icons — saved manually, see Section 7
    images/weapons/<slug>.png
  tools/
    data-entry/
      index.html               # the manual entry form (Section 7)
      app.js
      style.css
    validate.py                 # pydantic schema check across all of /data
  site/
    templates/
      base.html
      home.html
      character_index.html
      character.html
      weapons_index.html
      weapon.html
      faq.html
    static/
      css/style.css
      js/search.js
    build.py                    # reads /data + /assets, renders templates, writes /dist
  dist/                          # generated output (git-ignored, or the deploy branch)
  tests/
    test_data_schema.py
    test_build.py
  requirements.txt
  README.md
```

---

## 6. Data Schema

This is the target format the entry tool (Section 7) produces and `build.py` consumes. Refine field names during Phase 1 if the form surfaces something awkward, but keep it stable once data entry starts — changing the schema partway through means re-touching every already-entered character.

**`data/characters/groza.json`** (illustrative):

```json
{
  "slug": "groza",
  "name": "Groza",
  "class": "Bulwark",
  "rarity": "Standard",
  "phase": "Physical",
  "weapon_type": "Assault Rifle",
  "signature_weapon": "ots-14",
  "stats": { "hp": 1981, "atk": 539, "def": 553 },
  "skill_attribute": null,
  "weakness": null,
  "stability_gauge": "12 points",
  "movement_speed": "6 tiles",
  "effects_glossary": [
    "Movement Down II: Mobility decreased by 2 tiles. Considered a Movement debuff.",
    "Shelter: Gains Stability Protection, reducing Stability Damage taken by 2 points..."
  ],
  "skills": [
    {
      "name": "Fire Command",
      "tags": ["Basic Attack", "Targeted"],
      "ammo_type": "Medium Ammo",
      "stability_damage": 4,
      "cooldown": "0 turns",
      "confectance_cost": 0,
      "range": 7,
      "effect_area": "Target",
      "description": "Selects 1 target within 7 tiles, dealing Physical damage equal to 80% of attack."
    }
  ],
  "fortification": [
    { "tier": 1, "skill": "Heavy Suppression", "level": 2, "effect": "If this skill causes the enemy to enter into Stability Break, the user gains 1 point of Confectance Index and recovers 4 points of stability index." },
    { "tier": 2, "skill": "Perfect Cover", "level": 2, "effect": "Restores 5 points of stability index." },
    { "tier": 3, "skill": "Explosive Bombardment", "level": 2, "effect": "Damage multiplier increased by 10%." },
    { "tier": 4, "skill": "Timely Maintenance", "level": 2, "effect": "When Groza's action ends, applies Attack Down I on the enemy with the highest ATK within a 7 tile radius of self for 1 turn." },
    { "tier": 5, "skill": "Explosive Bombardment", "level": 3, "effect": "Extends the duration of Movement Down II increases by 1 turn." },
    { "tier": 6, "skill": "Timely Maintenance", "level": 3, "effect": "When having Shelter, reduces stability damage taken by 1 point." }
  ],
  "neural_helix": [
    { "node": "Enhancement 1", "level": 1, "effect": "ATK +25 | DEF +23", "materials": "20 | 1000" },
    { "node": "Enhancement 2", "level": 20, "effect": "HP +84 | HP +5.0%", "materials": "20 | 2000" },
    { "node": "Enhancement 3", "level": 25, "effect": "ATK +30 | DEF +32", "materials": "40 | 4000" },
    { "node": "Enhancement 4", "level": 30, "effect": "HP +115 | HP +5.0%", "materials": "80 | 8000" },
    { "node": "Enhancement 5", "level": 35, "effect": "ATK +35 | DEF +42", "materials": "120 | 10000" },
    { "node": "Enhancement 6", "level": 40, "effect": "ATK +41 | HP +150", "materials": "160 | 12000" }
  ],
  "keys": [
    { "name": "Fixed Key 1 - Multidimensional Assessment", "level": 20, "effect": "When the user causes the enemy to enter into Stability Break, applies Defence Down I and Attack Down I on the enemy for 1 turn.", "materials": "1 | 3000" },
    { "name": "Fixed Key 2 - Controlled Advance", "level": 20, "effect": "When using Perfect Cover, additionally applies Attack Up I for 1 turn.", "materials": "1 | 3000" },
    { "name": "Fixed Key 3 - Adaptive Strategy", "level": 30, "effect": "When self HP is below 30%, increase healing received by 50%.", "materials": "1 | 8000" },
    { "name": "Fixed Key 4 - Firepower Superiority", "level": 30, "effect": "If Heavy Suppression causes the enemy target to enter Stability Break, applies Taunt to them for 1 turn.", "materials": "1 | 8000" },
    { "name": "Fixed Key 5 - Sustainable Operations", "level": 40, "effect": "When the user is under the effects of Shelter, reduces AoE damage taken by 20%.", "materials": "2 | 12000" },
    { "name": "Fixed Key 6 - Principles of Evasion", "level": 40, "effect": "When Groza enters into Stability Break, restore 20% of self max HP, 5 points of stability index, and cleanse 4 debuffs from self. Triggers only once per battle.", "materials": "2 | 12000" },
    { "name": "Affinity Key - Midnight Reflection", "level": "Affinity Lvl 5", "effect": "ATK +3%, DEF +3%, HP +3%", "materials": "Unlocked at Affinity Lvl 5" },
    { "name": "Common Key - Sustained Endurance", "level": 40, "effect": "HP +3.0% | When Shelter is active, immune to displacement for 1 time. Has a cooldown of 1 turn.", "materials": "None" },
    { "name": "Expansion Key - Absolute Defense's Essence", "level": 60, "effect": "When using the active skill Perfect Cover, gains Absolute Defense.", "materials": "3 | 15000" }
  ],
  "images": {
    "portrait": "assets/images/characters/groza/portrait.png",
    "class_icon": "assets/images/characters/groza/class_icon.png"
  },
  "source_notes": ""
}
```

Keep a similarly light schema for `weapons.json` (name, unit type, rarity, image path) and `faq.json` (question, answer). Note on `materials`: the sheet shows these as a row of material icons with quantities (some slots blank), not plain text — `"20 | 1000"` above only captures the numbers. During entry, either add a short name alongside each quantity (e.g. `"20 Combat Data | 1000 Credits"`) by reading the icon, or store the icon images as a `materials_icon` path per entry — decide which before Phase 2 so it's consistent across all ~65 characters.

The entry tool should save **compact JSON**: strip empty/null optional fields before writing, use 2-space indentation for readability in git diffs (not minified — a human will be editing these by hand sometimes too), and always emit keys in a fixed order matching this schema so diffs stay small and readable.

---

## 7. The Data Entry Tool

This is the core piece that replaces spreadsheet parsing. Build it in Phase 1, before entering any real data.

**What it is:** a single static HTML page (`tools/data-entry/index.html`) with vanilla JS — no server, no build step. Open it directly in a browser (or serve it with `python -m http.server` for convenience). It's a form that mirrors the Section 6 schema and exports a ready-to-use JSON file.

**Form sections:**
- **Basic Info** — name, slug (auto-generated from name, editable), class / rarity / phase / weapon type / ammo type (all dropdowns from fixed lists, so wording can't drift between characters entered on different days), signature weapon (text, matched against a `weapons.json` slug), HP/ATK/DEF (number inputs), skill attribute, weakness, stability gauge, movement speed.
- **Effects Glossary** — a repeatable list of text entries (add/remove row buttons), one per status effect referenced on that character's tab.
- **Skills** — repeatable "skill card" blocks (add/remove skill). Each card: name, tags (a small multi-select, not free text), ammo type (dropdown), stability damage / cooldown / confectance cost / range / effect area (typed inputs), description (textarea).
- **Fortification** — a repeatable list, normally exactly 6 rows (tier 1–6). Each row: tier number, skill (a dropdown sourced from the skill names already entered above — catches typos/mismatches immediately), level (number, as shown on the sheet), effect (textarea). Transcribe straight from the "Vertebrae Upgrade" summary table near the bottom of the tab (see Section 2), not the inline mentions next to individual skills.
- **Neural Helix** — a repeatable list, normally 6 rows (Enhancement 1–6): node name, unlock level, effect (text), materials.
- **Keys** — a repeatable list covering Fixed Keys 1–6, Affinity Key, Common Key, and Expansion Key: name, unlock level (a number, or free text for the Affinity Key's "Affinity Lvl 5"-style condition), effect (textarea), materials.
- **Images** — read-only fields showing the expected file paths (auto-derived from the slug, e.g. `assets/images/characters/groza/portrait.png`), as a checklist reminder of which image files still need to be saved manually into `/assets` (see below).
- **Source Notes** — free text for anything worth flagging later (e.g. "see Jiangyu(old) for pre-rework kit").

**Behavior:**
- A live JSON preview panel updates as fields are filled in, so what you're about to save is always visible.
- **Save/Download** writes the compact JSON described in Section 6 as a browser download (`<slug>.json`), which then gets moved into `data/characters/`.
- **Load JSON** lets you pick an existing file back into the form for edits — this makes the tool double as the ongoing maintenance workflow for future character reworks or corrections, not just first-pass entry.
- Client-side validation: required fields are visually flagged, numeric fields reject non-numbers, dropdowns constrain enum-like values. This is the main payoff of a form over hand-editing raw JSON — it keeps ~65 independently-entered records consistent with each other. Seed the dropdown lists from what's actually observed while entering the first several characters rather than guessing up front, but Class (Bulwark, Vanguard, Support, Sentinel) and Phase (Physical, Burn, Hydro, Electric, Freeze, Corrosion, Omni) can likely be fixed from the start.
- Build a second, simpler mode (or a second small page) for weapons and FAQ entries, matching their lighter schemas.

**Images:** the entry tool only records expected *paths* — it doesn't touch image files. Saving a character's portrait/icons out of the spreadsheet (copy the image, save as PNG, place it at the path shown in the form) stays a manual step per character, done alongside filling in that character's form. Keep it simple: no cropping/processing pipeline for v1, just get a usable PNG at the right path.

---

## 8. Phased Build Plan

### Phase 0 — Setup
- Repo, virtualenv, `requirements.txt` (`Jinja2`, `pydantic`, `pytest`).
- Keep the source `.xlsx` on hand as a reference document (not touched by code).

### Phase 1 — Build the Data Entry Tool
- Build the form described in Section 7 against the Section 6 schema.
- Test it by entering 2–3 characters end-to-end (including saving real image files), checking that the output JSON is valid, and confirming a saved file can be re-loaded into the form without data loss (round-trip check).
- **Checkpoint:** get sign-off on the schema/form fields here — changing them after 20 characters are already entered is expensive.

### Phase 2 — Data Entry Pass
- Go through `Quick Links` to build the authoritative character/weapon list (see Section 2's `OTs-14` note), then work tab by tab: open a character's tab in the spreadsheet, fill in the form, save its image files, export the JSON.
- Resolve the flagged irregularities (Jiangyu/Jiangyu(old), Nemesis/Nemesis Gnosis) as they come up, per whatever the user decided in Section 2.
- Do the Weapons and FAQ tabs the same way, using the lighter form mode.
- Run `tools/validate.py` periodically (not just at the end) so schema mistakes get caught a few characters in, not after all 65.

### Phase 3 — Static Site Generator
- Jinja2 templates: shared base layout (nav, search bar, footer with credits from `Home`), character index (grid of portraits, filterable by class), character detail page, weapons index/detail, FAQ.
- `build.py`: load every JSON file in `/data`, render each through its template, copy `/assets` into `/dist`, and emit a flat `search-index.json` (name, class, slug) for client-side search.
- Templates should be entirely data-driven — no character names hard-coded in Python or HTML, so adding a new character later means adding a JSON file and images, not touching code.

### Phase 4 — Styling & UX
- Consult the `frontend-design` skill for palette/typography before hand-rolling CSS.
- Reuse class-based color coding (Bulwark/Vanguard/etc.) if a consistent scheme is identifiable.
- Design mobile-first; the character index grid and skill-detail layout are the two views most likely to break on a narrow screen.

### Phase 5 — Search & Navigation
- Client-side fuzzy search over `search-index.json` (Fuse.js or Lunr.js via CDN).
- Class/weapon-type filter chips on the index page, plain data-attribute filtering in vanilla JS.

### Phase 6 — QA & Testing
- `pytest`: every character JSON validates against the schema; every character has a corresponding generated HTML file; every image path referenced in a JSON file exists on disk; no broken internal links in `/dist`.
- Spot-check a handful of pages against the original spreadsheet tabs for transcription accuracy.
- Accessibility pass: alt text on every image (e.g. `"{character} portrait"`), basic color-contrast check on the chosen palette.

### Phase 7 — Deployment
- Push `/dist` to GitHub Pages (a `gh-pages` branch or a `docs/` folder on `main`), or use Cloudflare Pages/Netlify.
- Add a GitHub Action that runs `build.py` on every push to `main`, so adding/editing a JSON file and pushing is enough to update the live site.
- README section: "adding or updating a character" (open the entry tool, fill in/load the form, save the JSON + images, run `build.py`, commit).

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Manual entry across ~65 characters is time-consuming | Spread across sessions; the entry tool's dropdowns/validation catch mistakes early rather than at the end |
| Transcription errors (typos, missed fields) | Schema-constrained form fields (dropdowns/number inputs) instead of free-typed JSON; periodic `validate.py` runs during entry, not just at the end |
| Inconsistent terminology across characters entered at different times | Fixed dropdown lists for class/ammo type/tags, kept in one place in the form's JS |
| Ambiguous duplicate/variant tabs (Jiangyu, Nemesis Gnosis) | Explicit decision checkpoint with the user before Phase 2 — don't silently merge or drop data |
| A tab name looks like a character but isn't (e.g. `OTs-14`) | Use `Quick Links` as the authoritative list, not tab names |
| Scope creep into calculators/build tools | Hold the line at the v1 scope in Section 3; log extras as future work |

---

## 10. Definition of Done (v1)

- [ ] Every character in `Quick Links` has a JSON record and a generated page: name, class, HP/ATK/DEF, full skill list, Fortification tiers, Neural Helix nodes, and Key unlock info
- [ ] Every character has at least a portrait image saved at its expected path
- [ ] Weapons index + detail pages live
- [ ] FAQ page live
- [ ] Search and class filter both functional
- [ ] `pytest` suite passes; zero pydantic validation errors on build
- [ ] Site deployed and reachable at a public URL
- [ ] README documents how to add/update a character using the entry tool and how to redeploy

---

## 11. Open Questions to Confirm with the User

1. `Jiangyu(old)` — keep as a visible "previous version" section, an archived page, or drop it?
2. `Nemesis Gnosis` — fold into Nemesis's page as an alternate-mode section, or give it a standalone page?
3. Hosting preference — GitHub Pages (free, simplest) vs. Netlify/Cloudflare Pages vs. something else?
4. Who's doing the data entry, and roughly how much time per week — worth knowing up front since Phase 2 is now the long pole in the schedule, not the code.
5. The "Neural Helix" table (Section 2) — flat stat-boost nodes plus each Key's true unlock level/materials. Fold this into v1's schema now, or leave it out and revisit after the first pass of characters is entered?
