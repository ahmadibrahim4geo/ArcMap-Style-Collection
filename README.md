# ArcMap Style Collection | مكتبة ستايلات الأرك ماب

> تجميعة نادرة ومنظمة لستايلات **ArcMap (.style)** و **ArcGIS Pro (.stylx)** — جيولوجيا، هيدرولوجيا، بترول، تعدين، تربة، غطاء أرضي، نقل، ألوان — مع **40 نسخة عربية** ثنائية اللغة.

🌐 **الواجهة التفاعلية:** افتح ملف [`index.html`](index.html) في المتصفح (أو عبر GitHub Pages) لتصفح الـ 27 تصنيفًا بالبحث الفوري.

## 📊 الأرقام

| المؤشر | القيمة |
|---|---|
| ستايلات ArcMap (`.style`) | **486** |
| ستايلات Pro (`.stylx`) | **230** |
| ServerStyle | 114 |
| Layer files (`.lyrx`) | 37 |
| خرائط (`.mxd`) | 11 |
| خطوط (TTF/OTF) | 50+ |
| النسخ العربية (`*-AR`) | **40 ملف / 45,589 رمز / 49,869 حقلًا** |
| إجمالي الملفات | **4125** |
| التصنيفات | **27 مجلدًا** |

## ⚠️ قاعدة التوافق الذهبية

**الأرك برو يقدر يفتح ستايلات الأرك ماب ويستخدمها عادي — لكن العكس لا يحدث.**

| الصيغة | الامتداد | يعمل في |
|---|---|---|
| ArcMap Style | `.style` | ArcMap 10.x + ArcGIS Pro ✓ |
| ArcGIS Pro Style | `.stylx` | ArcGIS Pro فقط (✕ ArcMap) |
| Server Style | `.ServerStyle` | Pro / Server |
| Fonts | `.ttf/.otf` | تُثبت على النظام |

## 📁 التصنيفات (27)

| # | المجلد | .style | .stylx | ملفات | ملاحظة |
|---|---|---|---|---|---|
| 1 | Administrative Boundaries Styles | 2 | 2 | 11 | حدود NaturalEarth/GADM + عربي |
| 2 | Alaska DGGS AK-GeMS Style | 2 | 2 | 17 | الإصداران 1 و 2 + عربي |
| 3 | Ar North Arrow | 1 | 0 | 4 | أسهم شمال |
| 4 | BGS Geology 50k Styles | 0 | 2 | 14 | جيولوجيا بريطانيا + عربي Pro |
| 5 | Climate Regions Styles | 2 | 2 | 10 | أقاليم مناخية |
| 6 | Color For ArcGIS | 207 | 41 | 1152 | أضخم مجلد ألوان |
| 7 | ColorBrewer | 1 | 0 | 2 | سكيمات ColorBrewer |
| 8 | ESRI's Styles from arcMap | 57 | 0 | 554 | ستايلات Esri الأصلية |
| 9 | Forestry Styles | 2 | 2 | 11 | غابات + عربي |
| 10 | Geology 24K Styles | 2 | 2 | 11 | جيولوجيا 1:24K + عربي |
| 11 | Geomorphological Style | 3 | 0 | 19 | Vorarlberg + عربي |
| 12 | GitHub-Collected-Styles | 6 | 0 | 7 | من مستودعات GitHub |
| 13 | Hydrology and Water Resources Styles | 4 | 4 | 17 | مياه وصرف + عربي |
| 14 | Land Cover Styles | 2 | 2 | 11 | FAO-LCCS + عربي |
| 15 | Mining Styles | 2 | 2 | 10 | تعدين + عربي |
| 16 | Petroleum Styles | 2 | 6 | 16 | نفط + Shell + عربي |
| 17 | Population and Demographics Styles | 2 | 2 | 11 | سكان + عربي |
| 18 | Soils SSURGO Styles | 4 | 2 | 14 | تربة FAO + عربي |
| 19 | Styles and Fonts Symbol | 157 | 149 | 2128 | القلب: 8 مجلدات منظمة |
| 20 | Topographic Styles - Egypt | 2 | 2 | 10 | طبوغرافيا مصر |
| 21 | Transportation Styles | 2 | 2 | 11 | طرق OSM/MUTCD + عربي |
| 22 | Urban Land Use Styles | 2 | 2 | 12 | UrbanAtlas/CORINE + عربي |
| 23 | USGS FGDC Symbol Standard 2006 - Standard Documents | 0 | 0 | 5 | وثائق المعيار |
| 24 | USGS FGDC-GeMS - Standard Geologic Symbology | 2 | 2 | 21 | المعيار الاتحادي + عربي |
| 25 | USGS OF2005-1314 - Lithology and Geologic Time Styles | 14 | 0 | 30 | صخور وأزمنة + عربي |
| 26 | Vegetation and Biomes Styles | 2 | 2 | 10 | نباتات + عربي |
| 27 | Water NetWork Styles | 2 | 0 | 3 | شبكات مياه |

### 🧰 داخل `Styles and Fonts Symbol/`

`01_ArcMap_Styles / 02_ArcPro_Stylx / 03_from QGIS to ArcMap_Style / 04_Fonts / 05_USGS_AI_Inkscape / 06_Docs_PDF_Books / 07_MXD_GDB_Templates / 08_Tools_Scripts`

## 🌍 النسخ العربية

- كل أصل إنجليزي بقي كما هو، والنسخة العربية بجانبه في مجلد `Arabic` بالتنسيق: `عربي | English` (مثال: «بئر نفط | Oil Well»).
- البحث يعمل بالعربية والإنجليزية، والأكواد (FGDC / AXX0 / Zt) والاختصارات (GOC, OWC) بقيت كما هي.
- لكل نسخة ملف `Translations_*.csv` بأعمدة `field | id | key | original | arabic | new_value | status`.
- لإعادة التوليد بعد مراجعة CSV: `00 - Arabic Translation Kit\translate_styles.py all` (الأصول لا تُمس — تحقق SHA256).
- القاموس: حوالي 2860 مصطلحًا — الترجمة آلية للبحث والفهم وليست منقحة لغويًا نهائيًا.

## 🚀 الاستخدام (3 خطوات)

1. **انسخ المستودع:** `git clone https://github.com/ahmadibrahim4geo/ArcMap-Style-Collection.git`
2. **أضف الستايل:** ArcMap ← `Customize > Style Manager > Add Style` واختر `*-AR.style` للعربية · Pro ← `Insert > Add Style` واختر `*-AR.stylx` · ثبّت الخطوط من مجلد Fonts أولًا.
3. **ابحث وطبّق:** في Symbol Selector ابحث (بئر، فالق، غابة، خزان...) أو بالإنجليزية.

## 📜 الترخيص والشكر

- المحتوى الأصلي (Esri/USGS/BGS/DGGS) يبقى بحقوق أصحابه وتراخيصهم المرفقة داخل المجلدات.
- التنظيم والنسخ العربية والواجهة: **أحمد إبراهيم — MIT License**.
- التواصل: GitHub [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo) · البريد ahmadibrahim.geo@gmail.com · واتساب https://wa.me/201111915925
