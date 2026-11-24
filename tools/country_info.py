"""Basic facts shown in the "country at a glance" box on each country page.

Capital, official language(s), currency and main study cities are stable facts.
Population is a rounded estimate (millions, about 2024); each country links to its
World Bank country page (Taiwan: its national statistics office) so readers can
check the current figure. When the weekly task adds a country, add an entry here.

Each entry: slug -> dict(
    capital=(bn, en), pop=millions, lang=(bn, en), cur=(bn, en),
    cities=(bn, en), src=(label, url), note=(bn, en) optional)
"""

WB = "https://data.worldbank.org/country/"


def _wb(iso2):
    return ("World Bank", WB + iso2)


INFO = {
    "asia/bangladesh": dict(capital=("ঢাকা", "Dhaka"), pop=173.6, lang=("বাংলা", "Bangla"), cur=("টাকা (BDT)", "Taka (BDT)"),
                            cities=("ঢাকা, চট্টগ্রাম, রাজশাহী, খুলনা, সিলেট", "Dhaka, Chattogram, Rajshahi, Khulna, Sylhet"), src=_wb("bd")),
    "asia/india": dict(capital=("নয়াদিল্লি", "New Delhi"), pop=1450.9, lang=("হিন্দি, ইংরেজি (আরও ২২টি তফসিলি ভাষা)", "Hindi, English (plus 22 scheduled languages)"),
                       cur=("ভারতীয় রুপি (INR)", "Indian rupee (INR)"), cities=("দিল্লি, মুম্বাই, বেঙ্গালুরু, চেন্নাই, কলকাতা", "Delhi, Mumbai, Bengaluru, Chennai, Kolkata"), src=_wb("in")),
    "asia/china": dict(capital=("বেইজিং", "Beijing"), pop=1409.0, lang=("মান্দারিন চীনা", "Standard Chinese (Mandarin)"), cur=("ইউয়ান / রেনমিনবি (CNY)", "Yuan renminbi (CNY)"),
                       cities=("বেইজিং, সাংহাই, গুয়াংজু, উহান, নানজিং", "Beijing, Shanghai, Guangzhou, Wuhan, Nanjing"), src=_wb("cn")),
    "asia/japan": dict(capital=("টোকিও", "Tokyo"), pop=124.0, lang=("জাপানি", "Japanese"), cur=("ইয়েন (JPY)", "Yen (JPY)"),
                       cities=("টোকিও, ওসাকা, কিয়োটো, নাগোয়া, ফুকুওকা", "Tokyo, Osaka, Kyoto, Nagoya, Fukuoka"), src=_wb("jp")),
    "asia/south-korea": dict(capital=("সিউল", "Seoul"), pop=51.7, lang=("কোরিয়ান", "Korean"), cur=("ওন (KRW)", "Won (KRW)"),
                             cities=("সিউল, বুসান, দেজন, ইনচন, দেগু", "Seoul, Busan, Daejeon, Incheon, Daegu"), src=_wb("kr")),
    "asia/singapore": dict(capital=("সিঙ্গাপুর (নগর-রাষ্ট্র)", "Singapore (city-state)"), pop=6.0, lang=("ইংরেজি, মালয়, মান্দারিন, তামিল", "English, Malay, Mandarin, Tamil"),
                           cur=("সিঙ্গাপুর ডলার (SGD)", "Singapore dollar (SGD)"), cities=("পুরো দেশই একটি শহর", "The whole country is one city"), src=_wb("sg")),
    "asia/hong-kong": dict(capital=("— (চীনের বিশেষ প্রশাসনিক অঞ্চল)", "— (Special Administrative Region of China)"), pop=7.5, lang=("চীনা (ক্যান্টোনিজ), ইংরেজি", "Chinese (Cantonese), English"),
                           cur=("হংকং ডলার (HKD)", "Hong Kong dollar (HKD)"), cities=("হংকং দ্বীপ, কাউলুন, নিউ টেরিটরিজ", "Hong Kong Island, Kowloon, New Territories"), src=_wb("hk")),
    "asia/taiwan": dict(capital=("তাইপেই", "Taipei"), pop=23.4, lang=("মান্দারিন চীনা", "Mandarin Chinese"), cur=("নিউ তাইওয়ান ডলার (TWD)", "New Taiwan dollar (TWD)"),
                        cities=("তাইপেই, সিনচু, তাইচুং, তাইনান, কাওশিউং", "Taipei, Hsinchu, Taichung, Tainan, Kaohsiung"), src=("Ministry of the Interior (Taiwan)", "https://www.ris.gov.tw/app/en/3910")),
    "asia/thailand": dict(capital=("ব্যাংকক", "Bangkok"), pop=71.7, lang=("থাই", "Thai"), cur=("বাত (THB)", "Baht (THB)"),
                          cities=("ব্যাংকক, চিয়াং মাই, খোন কেন, হাট ইয়াই", "Bangkok, Chiang Mai, Khon Kaen, Hat Yai"), src=_wb("th")),
    "asia/pakistan": dict(capital=("ইসলামাবাদ", "Islamabad"), pop=251.3, lang=("উর্দু, ইংরেজি", "Urdu, English"), cur=("পাকিস্তানি রুপি (PKR)", "Pakistani rupee (PKR)"),
                          cities=("করাচি, লাহোর, ইসলামাবাদ, পেশোয়ার", "Karachi, Lahore, Islamabad, Peshawar"), src=_wb("pk")),
    "asia/israel": dict(capital=("জেরুজালেম (ঘোষিত; আন্তর্জাতিকভাবে বিতর্কিত — বেশির ভাগ দূতাবাস তেল আবিবে)", "Jerusalem (proclaimed; internationally disputed — most embassies are in Tel Aviv)"),
                        pop=9.9, lang=("হিব্রু (আরবির বিশেষ মর্যাদা)", "Hebrew (Arabic has special status)"), cur=("নতুন শেকেল (ILS)", "New shekel (ILS)"),
                        cities=("তেল আবিব, জেরুজালেম, হাইফা, বের শেভা", "Tel Aviv, Jerusalem, Haifa, Be'er Sheva"), src=_wb("il")),
    "asia/nepal": dict(capital=("কাঠমান্ডু", "Kathmandu"), pop=29.7, lang=("নেপালি", "Nepali"), cur=("নেপালি রুপি (NPR)", "Nepalese rupee (NPR)"),
                       cities=("কাঠমান্ডু, ললিতপুর, পোখরা, বিরাটনগর", "Kathmandu, Lalitpur, Pokhara, Biratnagar"), src=_wb("np")),
    "asia/malaysia": dict(capital=("কুয়ালালামপুর (প্রশাসনিক কেন্দ্র পুত্রাজায়া)", "Kuala Lumpur (administrative centre: Putrajaya)"), pop=35.6, lang=("মালয়", "Malay"),
                          cur=("রিঙ্গিত (MYR)", "Ringgit (MYR)"), cities=("কুয়ালালামপুর, পেনাং, জোহর বাহরু, কোটা কিনাবালু", "Kuala Lumpur, Penang, Johor Bahru, Kota Kinabalu"), src=_wb("my")),
    "asia/indonesia": dict(capital=("জাকার্তা (নুসান্তারায় স্থানান্তর চলছে)", "Jakarta (move to Nusantara under way)"), pop=283.5, lang=("ইন্দোনেশীয়", "Indonesian"),
                           cur=("রুপিয়া (IDR)", "Rupiah (IDR)"), cities=("জাকার্তা, বান্দুং, যোগ্যাকার্তা, সুরাবায়া", "Jakarta, Bandung, Yogyakarta, Surabaya"), src=_wb("id")),
    "asia/brunei": dict(capital=("বন্দর সেরি বেগাওয়ান", "Bandar Seri Begawan"), pop=0.46, lang=("মালয়", "Malay"), cur=("ব্রুনেই ডলার (BND)", "Brunei dollar (BND)"),
                        cities=("বন্দর সেরি বেগাওয়ান, কুয়ালা বেলাইত", "Bandar Seri Begawan, Kuala Belait"), src=_wb("bn")),
    "gcc/saudi-arabia": dict(capital=("রিয়াদ", "Riyadh"), pop=33.9, lang=("আরবি", "Arabic"), cur=("সৌদি রিয়াল (SAR)", "Saudi riyal (SAR)"),
                             cities=("রিয়াদ, জেদ্দা, দাম্মাম, মদিনা", "Riyadh, Jeddah, Dammam, Medina"), src=_wb("sa")),
    "gcc/uae": dict(capital=("আবুধাবি", "Abu Dhabi"), pop=10.9, lang=("আরবি", "Arabic"), cur=("দিরহাম (AED)", "Dirham (AED)"),
                    cities=("আবুধাবি, দুবাই, শারজাহ, আল আইন", "Abu Dhabi, Dubai, Sharjah, Al Ain"), src=_wb("ae")),
    "gcc/qatar": dict(capital=("দোহা", "Doha"), pop=3.0, lang=("আরবি", "Arabic"), cur=("কাতারি রিয়াল (QAR)", "Qatari riyal (QAR)"),
                      cities=("দোহা, আল রাইয়ান", "Doha, Al Rayyan"), src=_wb("qa")),
    "gcc/kuwait": dict(capital=("কুয়েত সিটি", "Kuwait City"), pop=4.9, lang=("আরবি", "Arabic"), cur=("কুয়েতি দিনার (KWD)", "Kuwaiti dinar (KWD)"),
                       cities=("কুয়েত সিটি", "Kuwait City"), src=_wb("kw")),
    "gcc/oman": dict(capital=("মাসকাট", "Muscat"), pop=5.3, lang=("আরবি", "Arabic"), cur=("ওমানি রিয়াল (OMR)", "Omani rial (OMR)"),
                     cities=("মাসকাট, সালালাহ, সোহার", "Muscat, Salalah, Sohar"), src=_wb("om")),
    "gcc/bahrain": dict(capital=("মানামা", "Manama"), pop=1.6, lang=("আরবি", "Arabic"), cur=("বাহরাইনি দিনার (BHD)", "Bahraini dinar (BHD)"),
                        cities=("মানামা, মুহাররাক", "Manama, Muharraq"), src=_wb("bh")),
    "europe/italy": dict(capital=("রোম", "Rome"), pop=59.0, lang=("ইতালীয়", "Italian"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                         cities=("রোম, মিলান, বোলোনিয়া, তুরিন, পাদোভা", "Rome, Milan, Bologna, Turin, Padua"), src=_wb("it")),
    "europe/germany": dict(capital=("বার্লিন", "Berlin"), pop=83.5, lang=("জার্মান", "German"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                           cities=("বার্লিন, মিউনিখ, হামবুর্গ, ফ্রাঙ্কফুর্ট, আখেন", "Berlin, Munich, Hamburg, Frankfurt, Aachen"), src=_wb("de")),
    "europe/united-kingdom": dict(capital=("লন্ডন", "London"), pop=69.2, lang=("ইংরেজি (ওয়েলসে ওয়েলশও)", "English (Welsh also official in Wales)"), cur=("পাউন্ড স্টার্লিং (GBP)", "Pound sterling (GBP)"),
                                  cities=("লন্ডন, ম্যানচেস্টার, বার্মিংহাম, এডিনবরা, গ্লাসগো", "London, Manchester, Birmingham, Edinburgh, Glasgow"), src=_wb("gb")),
    "europe/france": dict(capital=("প্যারিস", "Paris"), pop=68.5, lang=("ফরাসি", "French"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                          cities=("প্যারিস, লিয়ঁ, তুলুজ, মার্সেই, গ্রেনোবল", "Paris, Lyon, Toulouse, Marseille, Grenoble"), src=_wb("fr")),
    "europe/sweden": dict(capital=("স্টকহোম", "Stockholm"), pop=10.6, lang=("সুইডিশ", "Swedish"), cur=("সুইডিশ ক্রোনা (SEK)", "Swedish krona (SEK)"),
                          cities=("স্টকহোম, গোথেনবার্গ, উপসালা, লুন্ড", "Stockholm, Gothenburg, Uppsala, Lund"), src=_wb("se")),
    "europe/switzerland": dict(capital=("বার্ন (ফেডারেল শহর)", "Bern (federal city)"), pop=9.0, lang=("জার্মান, ফরাসি, ইতালীয়, রোমানশ", "German, French, Italian, Romansh"),
                               cur=("সুইস ফ্রাঁ (CHF)", "Swiss franc (CHF)"), cities=("জুরিখ, জেনেভা, বাসেল, লোজান", "Zurich, Geneva, Basel, Lausanne"), src=_wb("ch")),
    "europe/netherlands": dict(capital=("আমস্টারডাম (সরকারের আসন দ্য হেগ)", "Amsterdam (seat of government: The Hague)"), pop=17.9, lang=("ডাচ", "Dutch"),
                               cur=("ইউরো (EUR)", "Euro (EUR)"), cities=("আমস্টারডাম, রটারডাম, ডেলফট, ইউট্রেখট, গ্রোনিঙেন", "Amsterdam, Rotterdam, Delft, Utrecht, Groningen"), src=_wb("nl")),
    "europe/belgium": dict(capital=("ব্রাসেলস", "Brussels"), pop=11.8, lang=("ডাচ, ফরাসি, জার্মান", "Dutch, French, German"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                           cities=("ব্রাসেলস, অ্যান্টওয়ার্প, গেন্ট, লুভেন", "Brussels, Antwerp, Ghent, Leuven"), src=_wb("be")),
    "europe/finland": dict(capital=("হেলসিঙ্কি", "Helsinki"), pop=5.6, lang=("ফিনিশ, সুইডিশ", "Finnish, Swedish"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                           cities=("হেলসিঙ্কি, এসপো, টাম্পেরে, তুর্কু", "Helsinki, Espoo, Tampere, Turku"), src=_wb("fi")),
    "europe/austria": dict(capital=("ভিয়েনা", "Vienna"), pop=9.2, lang=("জার্মান", "German"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                           cities=("ভিয়েনা, গ্রাৎস, ইন্সব্রুক, সালজবুর্গ", "Vienna, Graz, Innsbruck, Salzburg"), src=_wb("at")),
    "europe/denmark": dict(capital=("কোপেনহেগেন", "Copenhagen"), pop=6.0, lang=("ড্যানিশ", "Danish"), cur=("ড্যানিশ ক্রোন (DKK)", "Danish krone (DKK)"),
                           cities=("কোপেনহেগেন, আরহুস, ওডেন্স, অলবর্গ", "Copenhagen, Aarhus, Odense, Aalborg"), src=_wb("dk")),
    "europe/norway": dict(capital=("অসলো", "Oslo"), pop=5.6, lang=("নরওয়েজীয়", "Norwegian"), cur=("নরওয়েজীয় ক্রোন (NOK)", "Norwegian krone (NOK)"),
                          cities=("অসলো, বার্গেন, ট্রনহেইম, ট্রমসো", "Oslo, Bergen, Trondheim, Tromsø"), src=_wb("no")),
    "europe/latvia": dict(capital=("রিগা", "Riga"), pop=1.9, lang=("লাটভীয়", "Latvian"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                          cities=("রিগা, দাউগাভপিলস, ইয়েলগাভা", "Riga, Daugavpils, Jelgava"), src=_wb("lv")),
    "europe/slovakia": dict(capital=("ব্রাতিস্লাভা", "Bratislava"), pop=5.4, lang=("স্লোভাক", "Slovak"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                            cities=("ব্রাতিস্লাভা, কোশিৎসে, ঝিলিনা", "Bratislava, Košice, Žilina"), src=_wb("sk")),
    "europe/turkiye": dict(capital=("আঙ্কারা", "Ankara"), pop=85.5, lang=("তুর্কি", "Turkish"), cur=("তুর্কি লিরা (TRY)", "Turkish lira (TRY)"),
                           cities=("ইস্তাম্বুল, আঙ্কারা, ইজমির, বুরসা", "Istanbul, Ankara, Izmir, Bursa"), src=_wb("tr")),
    "europe/hungary": dict(capital=("বুদাপেস্ট", "Budapest"), pop=9.6, lang=("হাঙ্গেরীয়", "Hungarian"), cur=("ফোরিন্ট (HUF)", "Forint (HUF)"),
                           cities=("বুদাপেস্ট, ডেব্রেৎসেন, সেগেড, পেচ", "Budapest, Debrecen, Szeged, Pécs"), src=_wb("hu")),
    "europe/ireland": dict(capital=("ডাবলিন", "Dublin"), pop=5.4, lang=("আইরিশ, ইংরেজি", "Irish, English"), cur=("ইউরো (EUR)", "Euro (EUR)"),
                           cities=("ডাবলিন, কর্ক, গলওয়ে, লিমেরিক", "Dublin, Cork, Galway, Limerick"), src=_wb("ie")),
    "north-america/usa": dict(capital=("ওয়াশিংটন, ডি.সি.", "Washington, D.C."), pop=340.1, lang=("ইংরেজি", "English"), cur=("মার্কিন ডলার (USD)", "US dollar (USD)"),
                              cities=("নিউ ইয়র্ক, বোস্টন, লস অ্যাঞ্জেলেস, শিকাগো, হিউস্টন", "New York, Boston, Los Angeles, Chicago, Houston"), src=_wb("us")),
    "north-america/canada": dict(capital=("অটোয়া", "Ottawa"), pop=41.3, lang=("ইংরেজি, ফরাসি", "English, French"), cur=("কানাডিয়ান ডলার (CAD)", "Canadian dollar (CAD)"),
                                 cities=("টরন্টো, মন্ট্রিয়ল, ভ্যাঙ্কুভার, অটোয়া, ক্যালগারি", "Toronto, Montreal, Vancouver, Ottawa, Calgary"), src=_wb("ca")),
    "latin-america/brazil": dict(capital=("ব্রাসিলিয়া", "Brasília"), pop=211.9, lang=("পর্তুগিজ", "Portuguese"), cur=("রিয়াল (BRL)", "Real (BRL)"),
                                 cities=("সাও পাওলো, রিও ডি জেনেইরো, ব্রাসিলিয়া, বেলো অরিজন্তি", "São Paulo, Rio de Janeiro, Brasília, Belo Horizonte"), src=_wb("br")),
    "latin-america/colombia": dict(capital=("বোগোতা", "Bogotá"), pop=52.9, lang=("স্প্যানিশ", "Spanish"), cur=("কলম্বিয়ান পেসো (COP)", "Colombian peso (COP)"),
                                   cities=("বোগোতা, মেডেলিন, কালি, বারানকিয়া", "Bogotá, Medellín, Cali, Barranquilla"), src=_wb("co")),
    "oceania/australia": dict(capital=("ক্যানবেরা", "Canberra"), pop=27.2, lang=("ইংরেজি", "English"), cur=("অস্ট্রেলিয়ান ডলার (AUD)", "Australian dollar (AUD)"),
                              cities=("সিডনি, মেলবোর্ন, ব্রিসবেন, পার্থ, অ্যাডিলেড", "Sydney, Melbourne, Brisbane, Perth, Adelaide"), src=_wb("au")),
    "oceania/new-zealand": dict(capital=("ওয়েলিংটন", "Wellington"), pop=5.3, lang=("ইংরেজি, মাওরি, নিউজিল্যান্ড সাংকেতিক ভাষা", "English, Māori, NZ Sign Language"),
                                cur=("নিউজিল্যান্ড ডলার (NZD)", "New Zealand dollar (NZD)"), cities=("অকল্যান্ড, ওয়েলিংটন, ক্রাইস্টচার্চ, ডানেডিন", "Auckland, Wellington, Christchurch, Dunedin"), src=_wb("nz")),
    "africa/mauritius": dict(capital=("পোর্ট লুই", "Port Louis"), pop=1.3, lang=("ইংরেজি ও ফরাসি বহুল ব্যবহৃত; কথ্য মরিশিয়ান ক্রেওল", "English and French widely used; Mauritian Creole spoken"),
                             cur=("মরিশিয়ান রুপি (MUR)", "Mauritian rupee (MUR)"), cities=("পোর্ট লুই, কিউরপিপ, কাত্র বর্ন", "Port Louis, Curepipe, Quatre Bornes"), src=_wb("mu")),
    "africa/nigeria": dict(capital=("আবুজা", "Abuja"), pop=232.7, lang=("ইংরেজি", "English"), cur=("নাইরা (NGN)", "Naira (NGN)"),
                           cities=("লাগোস, আবুজা, কানো, ইবাদান", "Lagos, Abuja, Kano, Ibadan"), src=_wb("ng")),
}

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def pop_bn(m):
    """Millions -> rounded Bangla text (কোটি / লাখ)."""
    if m >= 10:
        crore = m / 10
        t = f"{crore:.0f}" if crore >= 100 else f"{crore:.1f}".rstrip("0").rstrip(".")
        return f"প্রায় {t.translate(BN_DIGITS)} কোটি"
    lakh = round(m * 10)
    return f"প্রায় {str(lakh).translate(BN_DIGITS)} লাখ"


def pop_en(m):
    if m >= 1000:
        return f"about {m / 1000:.2f} billion".replace(".00", "")
    if m >= 1:
        return f"about {m:.1f} million".replace(".0 ", " ")
    return f"about {round(m * 1000)},000"


CSS = """<style>
.facts{border:1px solid var(--line);border-radius:10px;background:var(--surface);padding:14px 16px;display:flex;flex-direction:column;gap:10px;max-width:820px}
.facts h2{font-size:18px;margin:0}
.facts dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px 18px;margin:0}
.facts dt{font-size:13px;color:var(--muted)}.facts dd{margin:2px 0 0;font-weight:600}
.facts .wide{grid-column:1/-1}
.facts .src{font-size:12px;color:var(--muted);font-family:var(--body);margin:0}.facts .src a{color:var(--accent)}
</style>"""


def box_bn(slug):
    d = INFO.get(slug)
    if not d:
        return ""
    items = [("🏛️ রাজধানী", d["capital"][0]), ("👥 জনসংখ্যা", pop_bn(d["pop"])), ("🗣️ দাপ্তরিক ভাষা", d["lang"][0]),
             ("💱 মুদ্রা", d["cur"][0]), ("🎓 পড়াশোনার বড় শহর", d["cities"][0])]
    dl = "".join(f"<div{' class=\"wide\"' if i == len(items) - 1 else ''}><dt>{a}</dt><dd>{b}</dd></div>" for i, (a, b) in enumerate(items))
    return (f'<section class="facts" aria-label="দেশ পরিচিতি"><h2>এক নজরে দেশটি</h2><dl>{dl}</dl>'
            f'<p class="src">জনসংখ্যা আনুমানিক (২০২৪-এর কাছাকাছি)। সর্বশেষ সংখ্যা: <a href="{d["src"][1]}" target="_blank" rel="noopener">{d["src"][0]} ↗</a></p></section>')


def box_en(slug):
    d = INFO.get(slug)
    if not d:
        return ""
    items = [("🏛️ Capital", d["capital"][1]), ("👥 Population", pop_en(d["pop"])), ("🗣️ Official language(s)", d["lang"][1]),
             ("💱 Currency", d["cur"][1]), ("🎓 Main study cities", d["cities"][1])]
    dl = "".join(f"<div{' class=\"wide\"' if i == len(items) - 1 else ''}><dt>{a}</dt><dd>{b}</dd></div>" for i, (a, b) in enumerate(items))
    return (f'<section class="facts" aria-label="Country facts"><h2>At a glance</h2><dl>{dl}</dl>'
            f'<p class="src">Population is a rounded estimate (around 2024). Latest figure: <a href="{d["src"][1]}" target="_blank" rel="noopener">{d["src"][0]} ↗</a></p></section>')
