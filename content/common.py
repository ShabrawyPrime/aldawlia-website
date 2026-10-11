# -*- coding: utf-8 -*-
"""Shared, bilingual content for the Aldawlia for Cooling Corporation website (the group's home on aldawlia.org).

Every user-facing string is T(en, ar). Facts come from: Group Presentation R4.0,
the six company profiles (Aldawlia 2026, ETS brochure, JET Solar profile and brochure,
Nova Freeze profile v6 and brochure, NEO Energy flyer/profile, GGG flyer), the live
aldawlia.org site and the Test_project site, plus notes the user gave.
"""

def T(en, ar):
    return {"en": en, "ar": ar}


SITE = {
    "url": "https://www.aldawlia.org",          # production origin used for canonical/hreflang/sitemap
    # where the site is served today; link previews fetch their image from here (GitHub Pages forwards to the
    # custom domain once it is set, so this keeps working after the move)
    "deploy": "https://shabrawyprime.github.io/aldawlia-website",
    "name": T("Aldawlia for Cooling Corporation", "المؤسسة الدولية للتبريد"),
    "short": T("Aldawlia", "الدولية"),
    "legal": T("Aldawlia for Cooling Corporation", "المؤسسة الدولية للتبريد"),
    "tagline": T("We build the infrastructure of the future.", "نبني البنية التحتية للمستقبل."),
    "since": "1983",
    "revision": "1.0",
    "rev_date": "2026-10",
}

# Arabic-speaking countries for the language gateway (ISO 3166-1 alpha-2).
# Arab League members (22) + Western Sahara + Chad (Arabic is an official language).
ARABIC_COUNTRIES = ["DZ", "BH", "KM", "DJ", "EG", "IQ", "JO", "KW", "LB", "LY", "MR", "MA",
                    "OM", "PS", "QA", "SA", "SO", "SD", "SY", "TN", "AE", "YE", "EH", "TD"]

NAV = [
    {"key": "index", "href": "index.html", "label": T("Home", "الرئيسية")},
    {"key": "story", "href": "story.html", "label": T("Our Story", "قصتنا")},
    {"key": "group", "href": "group.html", "label": T("The Group", "المجموعة"), "mega": True},
    {"key": "solutions", "href": "solutions.html", "label": T("Solutions", "الحلول")},
    {"key": "projects", "href": "projects.html", "label": T("Projects", "المشروعات")},
    {"key": "sustainability", "href": "sustainability.html", "label": T("Sustainability", "الاستدامة")},
    {"key": "contact", "href": "contact.html", "label": T("Contact", "تواصل معنا")},
]

UI = {
    "skip": T("Skip to content", "انتقل إلى المحتوى"),
    "menu": T("Menu", "القائمة"),
    "close": T("Close", "إغلاق"),
    "start_project": T("Start a project", "ابدأ مشروعك"),
    "lang_other": T("العربية", "English"),
    "lang_other_code": T("ar", "en"),
    "lang_switch_label": T("Switch to Arabic", "التبديل إلى الإنجليزية"),
    "home": T("Home", "الرئيسية"),
    "learn_more": T("Learn more", "اعرف المزيد"),
    "visit_site": T("Visit website", "زيارة الموقع"),
    "company_profile": T("Company page", "صفحة الشركة"),
    "est": T("Est.", "تأسست"),
    "since": T("Since", "منذ"),
    "led_by": T("Led by", "بقيادة"),
    "website": T("Website", "الموقع الإلكتروني"),
    "email": T("Email", "البريد الإلكتروني"),
    "phone": T("Phone", "الهاتف"),
    "address": T("Address", "العنوان"),
    "copy": T("Copy", "نسخ"),
    "copied": T("Copied", "تم النسخ"),
    "open_map": T("Open in Maps", "افتح في الخرائط"),
    "all": T("All", "الكل"),
    "group_company": T("Aldawlia family of companies", "من عائلة شركات الدولية"),
    "back_to_group": T("All group companies", "جميع شركات المجموعة"),
    "other_companies": T("More from the group", "المزيد من شركات المجموعة"),
    "rights": T("All rights reserved.", "جميع الحقوق محفوظة."),
    "sheet": T("Sheet", "اللوحة"),
    "rev": T("Rev.", "مراجعة"),
    "drawing": T("Drawing", "رقم اللوحة"),
    "brand_link": T("Brand guidelines", "دليل الهوية"),
    "follow": T("Follow Aldawlia", "تابعوا الدولية"),
    "sector_cooling": T("Cooling & refrigeration", "التبريد والتجميد"),
    "sector_energy": T("Energy & renewables", "الطاقة والطاقة المتجددة"),
    "mother": T("Mother company", "الشركة الأم"),
    "where_they_meet": T("Hybrid cold chains", "سلاسل تبريد هجينة"),
    "read_story": T("Read our story", "اقرأ قصتنا"),
    "see_all_projects": T("See all projects", "كل المشروعات"),
    "explore_solutions": T("Explore our solutions", "استكشف حلولنا"),
    "talk_engineer": T("Talk to an engineer", "تحدث إلى مهندس"),
    "explore_group": T("Explore the group", "تعرّف على المجموعة"),
    "breadcrumb": T("Breadcrumb", "مسار التنقل"),
    "main_nav": T("Main navigation", "التنقل الرئيسي"),
    "footer_nav": T("Footer navigation", "روابط التذييل"),
    "companies": T("Companies", "الشركات"),
    "explore": T("Explore", "استكشف"),
    "get_in_touch": T("Get in touch", "تواصل معنا"),
    "head_office": T("Head office", "المقر الرئيسي"),
    "slide_label": T("Slide", "الشريحة"),
    "pause": T("Pause slideshow", "إيقاف العرض"),
    "play": T("Play slideshow", "تشغيل العرض"),
    "legend": T("Key to the drawing", "دليل الرسم"),
    "landline": T("Landline", "هاتف أرضي"),
    "quick_contact": T("Reach the head office", "تواصل مع المقر الرئيسي"),
}

# Accent colours per company: brand (logo colour), on_dark (accent on night backgrounds),
# on_light (accent text on light backgrounds, AA contrast).
COMPANIES = [
    {
        "key": "aldawlia", "page": "aldawlia.html", "logo": "aldawlia", "sector": "cooling", "mother": True,
        "name": T("Aldawlia for Cooling Corporation", "المؤسسة الدولية للتبريد"),
        "short": T("Aldawlia", "الدولية"),
        "est": "1986", "est_short": T("1986", "1986"), "est_label": T("1986 · since 1983", "1986 · منذ 1983"),
        "role": T("Mother company · industrial refrigeration", "الشركة الأم · التبريد الصناعي"),
        "verb": T("Engineers and builds", "تصمّم وتنفّذ"),
        "line": T("Consultancy, design, local contracting, automation and maintenance of large-scale industrial refrigeration since 1986.",
                  "استشارات أنظمة التبريد الصناعي الكبرى وتصميمها ومقاولاتها المحلية وأتمتتها وصيانتها منذ 1986."),
        "led": T("Eng. Nabil El Shabrawy, Founder, Chairman &amp; CEO", "م. نبيل الشبراوي، المؤسس ورئيس مجلس الإدارة والرئيس التنفيذي"),
        "web": "aldawlia.org", "url": "https://www.aldawlia.org",
        "email": "info@aldawlia.org",
        "phones": ["+20 2 3836 7822", "+20 50 233 0872"],
        "mobile": "+20 121 301 3861", "mobile_role": T("Office Manager", "مدير المكتب"), "mobile_name": T("Mr. Mohamed Reda", "أ. محمد رضا"),
        "address": T("5 Solimar Buildings, Central Axis, Office 101, 6th of October City, Giza, Egypt",
                     "مباني سوليمار 5، المحور المركزي، مكتب 101، مدينة السادس من أكتوبر، الجيزة، مصر"),
        "map": "https://www.google.com/maps/search/?api=1&query=Solimar+Buildings+Central+Axis+6th+of+October+City+Giza",
        "color": "#1F5AA6", "on_dark": "#6FB6FF", "on_light": "#1F5AA6",
    },
    {
        "key": "ert", "page": None, "logo": "ert", "sector": "cooling",
        "name": T("Egypt for Refrigeration Technology", "مصر لتكنولوجيا التبريد"),
        "short": T("ERT", "ERT"),
        "est": "2022", "est_short": T("2022", "2022"), "est_label": T("2022", "2022"),
        "role": T("Local refrigeration contracting", "مقاولات التبريد المحلية"),
        "verb": T("Installs", "تركّب"),
        "line": T("A local contractor for refrigeration installation works, based in 10th of Ramadan City.",
                  "مقاول محلي لأعمال تركيب أنظمة التبريد، مقره مدينة العاشر من رمضان."),
        "web": "ert-eg.com", "url": "https://www.ert-eg.com",
        "email": "info@ert-eg.com",
        "phones": ["+20 109 300 0773", "+20 55 446 7403"],
        "address": T("Villa ERT, Neighbourhood No. 4, 10th of Ramadan City, Al Sharqia, Egypt",
                     "فيلا ERT، المجاورة الرابعة، مدينة العاشر من رمضان، الشرقية، مصر"),
        "map": "https://www.google.com/maps/search/?api=1&query=10th+of+Ramadan+City+Sharqia+Egypt",
        "color": "#204392", "on_dark": "#7FA2F0", "on_light": "#204392",
    },
    {
        "key": "ets", "page": "ets.html", "logo": "ets", "sector": "cooling",
        "name": T("Engineering Trading Solutions FZ-LLC", "Engineering Trading Solutions FZ-LLC"),
        "short": T("ETS", "ETS"),
        "est": "2023", "est_short": T("Mid-2023", "منتصف 2023"), "est_label": T("Mid-2023", "منتصف 2023"),
        "role": T("Refrigeration EPC &amp; global supply", "مقاولات EPC للتبريد والتوريد العالمي"),
        "verb": T("Supplies", "تورّد"),
        "line": T("Premium refrigeration equipment from Europe, China and Japan, delivered as EPC.",
                  "معدات تبريد متميزة من أوروبا والصين واليابان، تُسلَّم بنظام EPC متكامل."),
        "led": T("Eng. Mohamed Nabil El Shabrawy, CEO", "م. محمد نبيل الشبراوي، الرئيس التنفيذي"),
        "web": "ets-ae.com", "url": "https://www.ets-ae.com",
        "email": "info@ets-ae.com",
        "phones": ["+971 54 454 9809"],
        "address": T("S241001T, New Shed No. 24, Al Hulaila Industrial Free Zone, Ras Al Khaimah, UAE",
                     "S241001T، المستودع الجديد رقم 24، منطقة الحليلة الصناعية الحرة، رأس الخيمة، الإمارات العربية المتحدة"),
        "map": "https://www.google.com/maps/search/?api=1&query=Al+Hulaila+Industrial+Free+Zone+Ras+Al+Khaimah",
        "color": "#004A82", "on_dark": "#5AAAF0", "on_light": "#004A82",
    },
    {
        "key": "nova-freeze", "page": "nova-freeze.html", "logo": "nova-freeze", "sector": "cooling",
        "name": T("Nova Freeze", "نوفا فريز"),
        "short": T("Nova Freeze", "نوفا فريز"),
        "est": "2025", "est_short": T("2025", "2025"), "est_label": T("2025 · with ELARABY Group", "2025 · مع مجموعة العربي"),
        "role": T("Joint venture with ELARABY Group", "مشروع مشترك مع مجموعة العربي"),
        "verb": T("Scales up", "تتوسّع"),
        "line": T("Integrated cooling EPC for strategic, mega and state-led projects, powered by ELARABY and Aldawlia.",
                  "حلول EPC متكاملة للتبريد للمشروعات الاستراتيجية والكبرى والمشروعات التي تقودها الدولة، بقوة العربي والدولية."),
        "web": "novafreeze.com", "url": "https://www.novafreeze.com",
        "email": "info@novafreeze.com",
        "phones": ["+20 11 4221 0033"],
        "address": T("Office 312, Plaza 34, Third District, Sheikh Zayed City, Giza, Egypt",
                     "مكتب 312، بلازا 34، الحي الثالث، مدينة الشيخ زايد، الجيزة، مصر"),
        "map": "https://www.google.com/maps/search/?api=1&query=Plaza+34+Sheikh+Zayed+City+Giza",
        "color": "#00BAF2", "on_dark": "#00BAF2", "on_light": "#0059AA",
    },
    {
        "key": "jet-solar", "page": "jet-solar.html", "logo": "jet-solar", "sector": "energy",
        "name": T("JET Solar", "جيت سولار"),
        "short": T("JET Solar", "جيت سولار"),
        "est": "2020", "est_short": T("2020", "2020"), "est_label": T("2020", "2020"),
        "role": T("Solar module manufacturing", "تصنيع الألواح الشمسية"),
        "verb": T("Manufactures", "تُصنّع"),
        "line": T("High-performance photovoltaic modules made in Egypt, plus BIPV and turnkey solar projects.",
                  "ألواح كهروضوئية عالية الأداء صُنعت في مصر، إلى جانب حلول BIPV ومشروعات طاقة شمسية متكاملة."),
        "led": T("Eng. Hazem Nabil El Shabrawy, CEO &amp; General Manager", "م. حازم نبيل الشبراوي، الرئيس التنفيذي والمدير العام"),
        "web": "jet-solar.com", "url": "https://www.jet-solar.com",
        "email": "info@jet-solar.com",
        "phones": ["+20 128 230 0081", "+20 123 453 4333"],
        "address": T("5 Solimar Buildings, Central Axis, 6th of October City, Giza, Egypt · Factory: Abu Rawash Industrial Zone, Giza",
                     "مباني سوليمار 5، المحور المركزي، مدينة السادس من أكتوبر، الجيزة، مصر · المصنع: المنطقة الصناعية بأبو رواش، الجيزة"),
        "map": "https://www.google.com/maps/search/?api=1&query=Abu+Rawash+Industrial+Zone+Giza",
        "color": "#F2B21A", "on_dark": "#F6B61D", "on_light": "#0A0A6C",
    },
    {
        "key": "neo-energy", "page": "neo-energy.html", "logo": "neo-energy", "sector": "energy",
        "name": T("NEO Energy Solutions", "نيو إنرجي سوليوشنز"),
        "short": T("NEO Energy", "نيو إنرجي"),
        "est": None, "est_short": None, "est_label": T("Joint venture", "مشروع مشترك"),
        "role": T("Solar distribution · joint venture", "توزيع منتجات الطاقة الشمسية · مشروع مشترك"),
        "verb": T("Distributes", "توزّع"),
        "line": T("Premium solar products across seven markets, from modules and inverters to storage.",
                  "منتجات طاقة شمسية متميزة في سبعة أسواق، من الألواح والعواكس إلى أنظمة التخزين."),
        "web": "neo-es.com", "url": "https://www.neo-es.com",
        "email": "info@neo-es.com",
        "phones": ["+20 120 843 4441", "+20 120 843 4449"],
        "address": T("Villa 8, Ninth District Service Center, Sheikh Zayed City, Giza, Egypt",
                     "فيلا 8، مركز خدمات الحي التاسع، مدينة الشيخ زايد، الجيزة، مصر"),
        "map": "https://www.google.com/maps/search/?api=1&query=Ninth+District+Service+Center+Sheikh+Zayed+City",
        "color": "#41B93A", "on_dark": "#4CC944", "on_light": "#237A1F",
    },
    {
        "key": "ggg", "page": "ggg.html", "logo": "ggg", "sector": "energy",
        "name": T("Green Global Group", "جرين جلوبال جروب"),
        "short": T("GGG", "GGG"),
        "est": None, "est_short": None, "est_label": T("Joint venture", "مشروع مشترك"),
        "role": T("Turnkey solar EPC · joint venture", "مقاولات EPC للطاقة الشمسية · مشروع مشترك"),
        "verb": T("Builds", "تبني"),
        "line": T("Turnkey solar plants that turn energy into a controllable, income-generating asset.",
                  "محطات طاقة شمسية متكاملة تحوّل الطاقة إلى أصل يمكن التحكم فيه ويدرّ دخلًا."),
        "web": "ggg-energy.com", "url": "https://ggg-energy.com",
        "email": "info@ggg-energy.com",
        "phones": ["+20 121 318 5100"],
        "address": T("Egypt", "مصر"),
        "map": None,
        "color": "#004A3A", "on_dark": "#3CC48A", "on_light": "#00573F",
    },
]
COMPANY = {c["key"]: c for c in COMPANIES}

OFFICES = [
    {"key": "october", "name": T("Aldawlia · 6th of October office", "الدولية · مكتب السادس من أكتوبر"),
     "address": COMPANY["aldawlia"]["address"], "phone": "+20 2 3836 7822", "email": "info@aldawlia.org",
     "mobile": COMPANY["aldawlia"]["mobile"], "mobile_role": COMPANY["aldawlia"]["mobile_role"], "mobile_name": COMPANY["aldawlia"]["mobile_name"],
     "map": COMPANY["aldawlia"]["map"]},
    {"key": "mansoura", "name": T("Aldawlia · Mansoura office", "الدولية · مكتب المنصورة"),
     "address": T("Abo Samra Towers, 7th floor, Happy Land Square, Mansoura, Dakahlia, Egypt",
                  "أبراج أبو سمرة، الطابق السابع، ميدان هابي لاند، المنصورة، الدقهلية، مصر"),
     "phone": "+20 50 233 0872", "email": "info@aldawlia.org",
     "map": "https://www.google.com/maps/search/?api=1&query=Abo+Samra+Towers+Happy+Land+Mansoura"},
]

SOCIAL = [
    {"name": "LinkedIn", "url": "https://www.linkedin.com/company/aldawliacooling/", "icon": "linkedin"},
    {"name": "Facebook", "url": "https://www.facebook.com/aldawliaforcooling", "icon": "facebook"},
    {"name": "Instagram", "url": "https://www.instagram.com/aldawliaforcooling/", "icon": "instagram"},
]

# Headline figures: the group at a glance (deck R4.0). A figure with a unit is T(en, ar);
# the Arabic keeps the deck's order ("+750,000 طن") and is rendered right to left.
KPIS = [
    {"n": "40+", "l": T("years of excellence, since 1983", "عامًا من التميز منذ 1983")},
    {"n": "500+", "l": T("projects delivered", "مشروع منفّذ")},
    {"n": T("750,000+ t", "+750,000 طن"), "l": T("of cold storage supplied and serviced", "سعة ثلاجات ورّدناها وخدمناها")},
    {"n": T("800+ t/h", "+800 طن/ساعة"), "l": T("of production lines supplied and serviced", "خطوط إنتاج ورّدناها وخدمناها")},
    {"n": "165+ MW", "l": T("of solar by the energy division", "من الطاقة الشمسية لقطاع الطاقة")},
    {"n": "17", "l": T("countries across the Middle East and Africa", "دولة في الشرق الأوسط وإفريقيا")},
]

PAGES = ["index", "story", "group", "aldawlia", "jet-solar", "ets", "nova-freeze", "neo-energy", "ggg",
         "solutions", "projects", "sustainability", "contact", "brand"]
