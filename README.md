# world-scholarships

Country-by-country list of current and upcoming scholarships, each with a link to the official source. Expired items are removed.

Data lives in `data/<continent>/<country>/scholarships.csv` (continents: `asia`, `europe`). The website groups them the same way: https://higherstudyinfo.com/asia/bangladesh/ etc.

| dataset | claude.ai preview |
|---|---|
| `asia/bangladesh` | https://claude.ai/artifact/GHhrqtV9tbHzor4g3BAsZ5 |
| `europe/italy` | https://claude.ai/artifact/2ZddPNekLNEboGyxecSmcW |
| `europe/erasmus-mundus` | https://claude.ai/artifact/XqHK8BnRFMiq2p1b2qf89A |

Other Asian datasets: india, china, japan, south-korea, singapore, hong-kong, taiwan, thailand, saudi-arabia, uae, qatar (website only). See [`data/asia/README.md`](data/asia/README.md) for countries still to add.

A scheduled task updates every dataset once a week (Sunday 09:41 Asia/Dhaka).

Every dataset uses the same columns and keep/remove rule; see [`data/asia/bangladesh/README.md`](data/asia/bangladesh/README.md). `provider_type` is one of `government`, `eu`, `consortium`, `public`, `private`, `international`.

Website: https://higherstudyinfo.com, deployed to cPanel on every push to `main` (see [`DEPLOY.md`](DEPLOY.md)).

Rebuild a preview page: `python3 tools/build_preview.py <continent>/<country> <out.html> [YYYY-MM-DD]`. A new country also needs an entry in `COUNTRIES` in `tools/build_preview.py`.
