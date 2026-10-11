# -*- coding: utf-8 -*-
from .common import T

COUNTRIES = {
    "EG": T("Egypt", "مصر"), "LY": T("Libya", "ليبيا"), "YE": T("Yemen", "اليمن"), "SA": T("Saudi Arabia", "السعودية"),
    "AE": T("United Arab Emirates", "الإمارات"), "JO": T("Jordan", "الأردن"), "LB": T("Lebanon", "لبنان"),
    "SD": T("Sudan", "السودان"), "ET": T("Ethiopia", "إثيوبيا"), "KE": T("Kenya", "كينيا"), "DZ": T("Algeria", "الجزائر"),
    "MA": T("Morocco", "المغرب"), "SL": T("Sierra Leone", "سيراليون"), "MU": T("Mauritius", "موريشيوس"),
    "PS": T("Palestine", "فلسطين"), "IQ": T("Iraq", "العراق"), "SY": T("Syria", "سوريا"),
}

# Where each company has worked (company profiles; deck map slide 13).
MARKETS = {
    "aldawlia": ["EG", "LY", "YE", "SA", "AE", "JO", "LB", "SD", "ET", "KE", "DZ", "MA", "SL", "MU"],
    "jet-solar": ["EG", "LY", "PS", "SD", "SA"],
    "ets": ["EG", "LY", "LB", "IQ"],
    "nova-freeze": ["EG", "SA", "YE", "LB", "SL", "ET"],
    "neo-energy": ["EG", "SY", "LB", "IQ", "JO", "AE", "SD"],
    "ggg": ["EG"],
    "ert": ["EG"],
}

HUBS = [
    {"key": "cairo6oct", "name": T("6th of October City", "مدينة السادس من أكتوبر"), "note": T("Group head office", "المقر الرئيسي للمجموعة")},
    {"key": "mansoura", "name": T("Mansoura", "المنصورة"), "note": T("Aldawlia office", "مكتب الدولية")},
    {"key": "rak", "name": T("Ras Al Khaimah", "رأس الخيمة"), "note": T("ETS registered office", "المقر المسجل لـ ETS")},
    {"key": "dubai", "name": T("Dubai · Jebel Ali", "دبي · جبل علي"), "note": T("Nova Freeze office", "مكتب نوفا فريز")},
]

GROUP = {
    "meta": {
        "title": T("The Group | Aldawlia for Cooling Corporation", "المجموعة | المؤسسة الدولية للتبريد"),
        "desc": T("Aldawlia, ERT, ETS and Nova Freeze in cooling; JET Solar, NEO Energy and GGG in energy. How the Aldawlia family of companies is structured and works together.",
                  "الدولية وERT وETS ونوفا فريز في التبريد، وجيت سولار ونيو إنرجي وGGG في الطاقة. كيف تتكون عائلة شركات الدولية وكيف تعمل معًا."),
    },
    "hero": {
        "eyebrow": T("The Group", "المجموعة"),
        "title": T("One family of companies. Two sectors. One standard.", "عائلة واحدة من الشركات، وقطاعان، ومعيار واحد."),
        "lead": T("Aldawlia is the mother company. Around it the group works in two sectors, cooling and refrigeration, and energy and renewables, and the two meet in hybrid-powered cold chains.",
                  "الدولية هي الشركة الأم، ومن حولها تعمل المجموعة في قطاعين: التبريد والتجميد، والطاقة والطاقة المتجددة، ويلتقي القطاعان في سلاسل تبريد تعمل بالطاقة الهجينة."),
    },
    "companies_title": T("The companies at a glance.", "الشركات في لمحة."),
    "structure": {
        "eyebrow": T("Group structure", "هيكل المجموعة"),
        "title": T("One mother company, two sectors.", "شركة أم واحدة، وقطاعان."),
        "jv": T("Joint venture", "مشروع مشترك"),
        "jv_under": T("Joint ventures in the energy sector, alongside JET Solar", "مشروعات مشتركة في قطاع الطاقة إلى جانب جيت سولار"),
    },
    "details": {
        "aldawlia": [T("Consultancy, design and local contracting: 7 services across 14 sectors", "الاستشارات والتصميم والمقاولات المحلية: 7 خدمات في 14 قطاعًا"),
                     T("Civil Department since 2009, turnkey EPC since 2023", "قسم مدني منذ 2009، ومشروعات تسليم مفتاح منذ 2023"),
                     T("Offices in 6th of October City and Mansoura", "مكاتب في مدينة السادس من أكتوبر والمنصورة")],
        "ert": [T("Local contractor for refrigeration installation works", "مقاول محلي لأعمال تركيب أنظمة التبريد"),
                T("Established 2022", "تأسست عام 2022"),
                T("Based in 10th of Ramadan City, Al Sharqia", "مقرها مدينة العاشر من رمضان، الشرقية")],
        "ets": [T("80+ projects delivered since mid-2023", "أكثر من 80 مشروعًا منذ منتصف 2023"),
                T("Equipment from Europe, China and Japan", "معدات من أوروبا والصين واليابان"),
                T("Registered in Ras Al Khaimah, UAE", "مسجلة في رأس الخيمة، الإمارات")],
        "nova-freeze": [T("Strategic, mega, sovereign-backed and state-led projects", "المشروعات الاستراتيجية والكبرى والمدعومة سياديًا والتي تقودها الدولة"),
                        T("Natural refrigerants: ammonia and CO₂", "غازات تبريد طبيعية: الأمونيا وثاني أكسيد الكربون"),
                        T("100+ years of combined expertise with ELARABY Group", "أكثر من 100 عام من الخبرة المشتركة مع مجموعة العربي"),
                        T("Seven service centres in Egypt, plus a Dubai office in Jebel Ali", "سبعة مراكز خدمة في مصر، إضافة إلى مكتب في دبي بجبل علي")],
        "jet-solar": [T("Modules up to 725 W with a 30-year warranty", "ألواح بقدرة تصل إلى 725 واط وضمان 30 عامًا"),
                      T("TÜV certified; ISO 9001, 14001 and 45001", "معتمدة من TÜV؛ وISO 9001 و14001 و45001"),
                      T("Factory in Abu Rawash, Giza", "المصنع في أبو رواش، الجيزة")],
        "neo-energy": [T("150 MW supplied to Syria, Iraq and Lebanon", "150 ميجاواط وُرّدت إلى سوريا والعراق ولبنان"),
                       T("Seven markets, six international brands", "سبعة أسواق وست علامات عالمية")],
        "ggg": [T("5,027 kW installed across 18 projects", "5,027 كيلوواط مركّبة في 18 مشروعًا"),
                T("On site within 4–6 days", "في الموقع خلال 4–6 أيام")],
    },
    "synergy": {
        "eyebrow": T("One group", "مجموعة واحدة"),
        "title": T("How the companies work together.", "كيف تعمل الشركات معًا."),
        "cooling": [
            ("aldawlia", T("Engineers and builds", "تصمّم وتنفّذ"), T("Consultancy, design, local contracting, automation and maintenance since 1986", "الاستشارات والتصميم والمقاولات المحلية والأتمتة والصيانة منذ 1986")),
            ("ert", T("Installs", "تركّب"), T("Local contracting for refrigeration installation works", "مقاولات محلية لأعمال تركيب أنظمة التبريد")),
            ("ets", T("Supplies", "تورّد"), T("Equipment from Europe, China and Japan, delivered as EPC", "معدات من أوروبا والصين واليابان تُسلَّم بنظام EPC")),
            ("nova-freeze", T("Scales up", "تتوسّع"), T("Strategic, mega and state-led projects with ELARABY Group", "مشروعات استراتيجية وكبرى ومشروعات تقودها الدولة مع مجموعة العربي")),
        ],
        "energy": [
            ("jet-solar", T("Manufactures", "تُصنّع"), T("Photovoltaic modules made in Egypt", "ألواح كهروضوئية صُنعت في مصر")),
            ("neo-energy", T("Distributes", "توزّع"), T("Premium solar products across seven markets", "منتجات طاقة شمسية متميزة في سبعة أسواق")),
            ("ggg", T("Builds", "تبني"), T("Turnkey solar EPC for Egypt's productive sectors", "محطات طاقة شمسية متكاملة للقطاعات الإنتاجية في مصر")),
        ],
        "meet_title": T("Where they meet", "حيث يلتقيان"),
        "meet": T("Hybrid power for cooling: renewables, battery storage or generators, combined with existing infrastructure, that keep production and cold storage running without interruption.",
                  "طاقة هجينة للتبريد: طاقة متجددة أو بطاريات تخزين أو مولدات، مع البنية القائمة، تُبقي الإنتاج والتخزين المبرّد في عمل متواصل دون انقطاع."),
        "case_title": T("Case in point · Frosty Foods, Noubaria", "مثال عملي · فروستي فودز، النوبارية"),
        "case": T("ETS supplied and built the refrigeration plant, Aldawlia was the consultant for refrigeration, civil and MEP works, and JET Solar installed the rooftop solar beside the evaporative condensers and the ammonia piping. Cooling and energy, designed together.",
                  "ورّدت ETS محطة التبريد ونفّذتها، وكانت الدولية الاستشاري لأعمال التبريد والأعمال المدنية والكهروميكانيكية، وركّبت جيت سولار المحطة الشمسية على السطح بجوار المكثفات التبخيرية وخطوط الأمونيا. التبريد والطاقة مصممان معًا."),
    },
    "visions": {
        "eyebrow": T("Where we are going", "إلى أين نتجه"),
        "title": T("One direction, in each company's words.", "اتجاه واحد، بكلمات كل شركة."),
        "items": [
            ("aldawlia", T("To remain the regional leader in industrial refrigeration by driving innovation, maintaining integrity in every step, and delivering engineering excellence.", "أن نظل الرواد إقليميًا في التبريد الصناعي، بدفع الابتكار والالتزام بالنزاهة في كل خطوة وتقديم التميز الهندسي.")),
            ("ets", T("To become the region's leading one-stop shop, exporting Egyptian engineering excellence with global standards to the Middle East.", "أن نصبح الوجهة المتكاملة الرائدة في المنطقة، نصدّر التميز الهندسي المصري بمعايير عالمية إلى الشرق الأوسط.")),
            ("nova-freeze", T("To be the leading provider of sustainable industrial refrigeration and HVAC-R solutions, driving innovation in cold chain efficiency and environmental responsibility.", "أن نكون المزوّد الرائد لحلول التبريد الصناعي والتكييف والتبريد المستدامة، ونقود الابتكار في كفاءة سلاسل التبريد والمسؤولية البيئية.")),
            ("jet-solar", T("To become a leading regional manufacturer of solar panels, recognized for innovation, manufacturing excellence and commitment to accelerating the global transition toward clean energy.", "أن نصبح مصنّعًا إقليميًا رائدًا للألواح الشمسية، معروفًا بالابتكار والتميز في التصنيع والالتزام بتسريع التحول العالمي نحو الطاقة النظيفة.")),
            ("ggg", T("Shaping the future of energy infrastructure across Egypt, the GCC and Africa through engineering excellence, superior performance, and value for generations to come.", "نصوغ مستقبل البنية التحتية للطاقة في مصر ودول الخليج وإفريقيا، عبر التميز الهندسي والأداء المتفوق وقيمة تمتد للأجيال القادمة.")),
        ],
        "closing": T("We build the infrastructure of the future.", "نبني البنية التحتية للمستقبل."),
    },
}
