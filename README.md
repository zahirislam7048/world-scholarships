# world-scholarships

Country-by-country list of current and upcoming scholarships, each with a link to the official source. Expired items are removed.

| country / programme | data | preview |
|---|---|---|
| Bangladesh | [`data/bangladesh/scholarships.csv`](data/bangladesh/scholarships.csv) | https://claude.ai/artifact/GHhrqtV9tbHzor4g3BAsZ5 |
| Italy | [`data/italy/scholarships.csv`](data/italy/scholarships.csv) | https://claude.ai/artifact/2ZddPNekLNEboGyxecSmcW |
| Erasmus Mundus (EU) | [`data/erasmus-mundus/scholarships.csv`](data/erasmus-mundus/scholarships.csv) | https://claude.ai/artifact/XqHK8BnRFMiq2p1b2qf89A |

A scheduled task updates every dataset once a week (Sunday 09:41 Asia/Dhaka).

Every dataset uses the same columns and keep/remove rule; see [`data/bangladesh/README.md`](data/bangladesh/README.md). `provider_type` is one of `government`, `eu`, `consortium`, `public`, `private`, `international`.

Rebuild a preview page: `python3 tools/build_preview.py <slug> <out.html> [YYYY-MM-DD]` (slug = folder name under `data/`).
