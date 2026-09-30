# preflop_rfi.json

Open-raise (RFI) ranges, 6-max, by position (UTG, MP, CO, BTN, SB). BB has no RFI.

- Source: https://github.com/AHTOOOXA/poker-charts, `src/data/ranges/pekarstas.ts` (keys `*-RFI`), fetched 2026-09-21.
- The repo is MIT for its code; the range data is scraped from third-party chart providers, so its
  redistribution terms are unclear. Fine for a school project, check before publishing.
- Format: sparse map hand -> `"raise"` | `["raise","fold"]` (mixed/marginal). Unlisted hand = fold.

# poker_glossary_source.txt / poker_glossary.json

French poker glossary (313 entries) plus 14 online-chat abbreviations, built by `build_glossary.py`.

- Source: text pasted by the user, apparently from a French poker affiliate site (it mentions PokerListings).
  Copyright status unknown: fine for a school project, do not republish.
- Cleaned by hand: site ads, the A-Z index, the chat article prose and links to other articles were removed;
  paragraphs are joined by ` ¶ `; two entries written "X voir Y" became "X – voir Y".
- Left as in the source, typos included. "Bad beat jackpot" is truncated in the source itself.
- Known gap: "Surblinde – voir Grosse Blinde" points to a spelling that has no entry (BB says "Grosse Blind").
