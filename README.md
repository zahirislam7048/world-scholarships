# world-scholarships

Country-by-country list of current and upcoming scholarships, each with a link to the official source. Expired items are removed.

Data lives in `data/<section>/<country>/scholarships.csv` (sections: `asia`, `gcc`, `europe`, `north-america`, `latin-america`, `oceania`, `africa`). The website groups them the same way: https://higherstudyinfo.com/asia/bangladesh/ etc.

| dataset | claude.ai preview |
|---|---|
| `asia/bangladesh` | https://claude.ai/artifact/GHhrqtV9tbHzor4g3BAsZ5 |
| `europe/italy` | https://claude.ai/artifact/2ZddPNekLNEboGyxecSmcW |
| `europe/erasmus-mundus` | https://claude.ai/artifact/XqHK8BnRFMiq2p1b2qf89A |

Other datasets (website only) — Asia: india, china, japan, south-korea, singapore, hong-kong, taiwan, thailand, pakistan, israel; GCC: saudi-arabia, uae, qatar, kuwait, oman, bahrain; Europe: germany, united-kingdom, france, sweden, switzerland, netherlands, belgium, finland, austria, denmark, norway, latvia, slovakia; North America: usa, canada; Latin America: brazil, colombia; Oceania: australia, new-zealand; Africa: mauritius. Countries still to add / watched: [`data/asia/README.md`](data/asia/README.md), [`data/gcc/README.md`](data/gcc/README.md), [`data/europe/README.md`](data/europe/README.md), [`data/north-america/README.md`](data/north-america/README.md), [`data/latin-america/README.md`](data/latin-america/README.md), [`data/oceania/README.md`](data/oceania/README.md), [`data/africa/README.md`](data/africa/README.md).

A scheduled task updates every dataset once a week (Sunday 09:41 Asia/Dhaka).

Every dataset uses the same columns and keep/remove rule; see [`data/asia/bangladesh/README.md`](data/asia/bangladesh/README.md). `provider_type` is one of `government`, `eu`, `consortium`, `public`, `private`, `international`.

Website: https://higherstudyinfo.com, deployed to cPanel on every push to `main` (see [`DEPLOY.md`](DEPLOY.md)).

Rebuild a preview page: `python3 tools/build_preview.py <continent>/<country> <out.html> [YYYY-MM-DD]`. A new country also needs an entry in `COUNTRIES` in `tools/build_preview.py`.
