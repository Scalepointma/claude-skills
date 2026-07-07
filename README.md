# ScalePoint M&A — Claude Skills

Internal Claude skills for the ScalePoint team. **This repo is the single
source of truth** — all skill changes are made here and released from here.
Never edit a skill in a chat session copy.

## Skills

| Skill | Purpose |
|---|---|
| `scalepoint-teaser` | One-page blind buyer teaser as a branded PDF (content firewall, math + blind gates) |
| `scalepoint-report-format` | Boardroom PDFs — CIMs, valuation reports, brochures, proposals |
| `scalepoint-intake` | Buyer or seller intake — guided conversation → HubSpot Company + Contact + Deal |
| `scalepoint-meeting-crm` | Transcribe a meeting recording → populate HubSpot seller deal or buyer profile |
| `scalepoint-seller-subicp` | Identify seller Sub-ICP (A–G) and route through the Match Matrix |

## How the team gets skills (claude.ai / Cowork — everyone)

Skills are distributed as **organization skills on claude.ai**. No installs.

1. Delta builds a zip per skill from this repo (`dist/` via `make-dist.sh`)
2. An org admin (Jodi) uploads each zip once: **claude.ai → Settings →
   Capabilities → Skills → Upload skill**, toggle on for the organization
3. Everyone in the org has them immediately, in Cowork and claude.ai chat
4. Updates: rebuild zip → re-upload (replaces the old version)

## How Delta's Mac gets skills (Claude Code)

The working clone at `~/delta/repos/claude-skills` plus the plugin
marketplace (`/plugin marketplace add Scalepointma/claude-skills`).

## Releasing a change

1. Branch → edit skill in `plugins/<name>/skills/<name>/` → PR → Jodi sign-off → merge
2. Run `./make-dist.sh` → fresh zips in `dist/`
3. Give the zips to Jodi for re-upload (step 2 above)
