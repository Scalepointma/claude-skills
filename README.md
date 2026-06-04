# ScalePoint M&A — Claude Skills

Internal Claude Code plugins for the ScalePoint team.

## Skills

| Plugin | Purpose |
|---|---|
| `scalepoint-report-format` | On-brand PDFs — CIMs, teasers, valuation reports, brochures, proposals |
| `scalepoint-teaser` | Confidential buyer teaser — collects data, verifies EBITDA, outputs markdown + branded HTML |
| `scalepoint-intake` | Buyer or seller intake — guided conversation → HubSpot Company + Contact + Deal |
| `scalepoint-meeting-crm` | Transcribe a meeting recording → populate HubSpot seller deal or buyer profile |
| `scalepoint-seller-subicp` | Identify seller Sub-ICP (A–G) during intake and route through Match Matrix |

## Install (one-time per machine)

```bash
claude plugins add https://github.com/Scalepointma/claude-skills
```

Updates are automatic — when skills are pushed to this repo, Claude Code picks them up on next sync.

## For Alina — first-time setup

1. Open Claude Code (CoWork)
2. In any chat, type:
   ```
   ! claude plugins add https://github.com/Scalepointma/claude-skills
   ```
3. Start a new chat — all 5 skills are now active

## Trigger phrases

| Skill | Say something like... |
|---|---|
| `scalepoint-teaser` | "write a teaser for [business]", "/teaser", "format a blind profile" |
| `scalepoint-intake` | "buyer intake", "seller intake", "add a new buyer", "fill out the form for [seller]" |
| `scalepoint-report-format` | "create a PDF", "make a CIM", "build a valuation report", "ScalePoint brand" |
| `scalepoint-meeting-crm` | "transcribe this meeting", "log this intake call", drops audio file |
| `scalepoint-seller-subicp` | "classify this seller", "what sub-ICP is this seller", "run the match matrix" |
