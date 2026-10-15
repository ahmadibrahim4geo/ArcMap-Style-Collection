النسخ العربية للاستايلات - دليل شامل
========================================
التاريخ: 29-09-2026 | المشروع: Styles ArcMap
النطاق: 40 ملف ستايل | 45,589 رمز | 49,869 حقلاً مترجماً (أسماء + فئات + وسوم)

1) الفكرة
---------
كل ستايل أصلي بقي كما هو بدون أي تعديل، وأُنشئت بجانبه نسخة عربية داخل مجلد فرعي
باسم Arabic. النسخة العربية ثنائية اللغة بالتنسيق:
    عربي | English
مثال:  «بئر نفط | Oil Well»  -  «فالق عكسي مؤكدة | Reverse fault - Certain»
الأصل الإنجليزي محفوظ كاملاً بعد الفاصل | لذلك البحث يعمل بالعربية والإنجليزية معاً،
والأكواد (FGDC مثل 01.04.01) وأكواد الألوان (AXX0) وأكواد التربة (Zt) بقيت كما هي.

2) أماكن النسخ العربية (كل نسخة داخل مجلد Arabic بجانب الأصل)
--------------------------------------------------------------
- Alaska DGGS AK-GeMS Style\Arabic\ ........... نسختا ArcMap + Pro (ver_1 + ver_2)
- BGS Geology 50k Styles\Arabic\ .............. نسخة Pro (الأسماء أكواد: أُضيفت تسمية «صخر الأساس»)
- Forestry Styles\Arabic\ ..................... نسختا ArcMap + Pro
- Geology 24K Styles\Arabic\ .................. نسختا ArcMap + Pro
- Hydrology and Water Resources Styles\Arabic\  نسختا ArcMap (Utilities + Water Wastewater) + نسختا Pro
- Mining Styles\Arabic\ ....................... نسختا ArcMap + Pro
- Petroleum Styles\Arabic\ .................... نسختا ArcMap + Pro + نسختا Shell (Red/Green)
- Soils SSURGO Styles\Arabic\ ................. نسختا ArcMap + نسخة Pro (أسماء FAO مترجمة + الأكواد الحرفية كما هي)
- USGS FGDC-GeMS ...\GSC_..._ArcMap\Arabic\ ... نسخة ArcMap (الفئات الوصفية مترجمة + الأكواد الرقمية كما هي)
- USGS FGDC-GeMS ...\GSC_..._ArcGISPro\Arabic\  نسخة Pro
- USGS OF2005-1314 ...\Arabic\ ................ النسخ السبع (DNAG/ISC/ISC_USGS/SGMC/lith4_3/lith6_1/lith6_2:
                                                المراحل الزمنية + الصخور مترجمة + قيم RGB كما هي)
- Geomorphological Style\Style geomorpho\Arabic\  نسخة Vorarlberg فقط
- Administrative Boundaries Styles\Arabic\ ... نسختا ArcMap + Pro (حدود إدارية NaturalEarth/GADM)
- Land Cover Styles\Arabic\ ................... نسختا ArcMap + Pro (غطاء أرضي FAO-LCCS)
- Population and Demographics Styles\Arabic\ .. نسختا ArcMap + Pro (سكان وتعداد)
- Transportation Styles\Arabic\ ............... نسختا ArcMap + Pro (نقل OSM/MUTCD)
- Urban Land Use Styles\Arabic\ ............... نسختا ArcMap + Pro (استخدام حضري UrbanAtlas/CORINE)
  (ملاحظة: Geomorphological.style نفسه ثنائي اللغة أصلاً لذلك لم تُعمل له نسخة)

3) الاستخدام
------------
- ArcMap: Customize > Style Manager > Styles... > Add Style to List > اختر ملف *-AR.style
- ArcGIS Pro: Insert > Add Style > اختر ملف *-AR.stylx
- ابحث في Symbol Selector بالعربية (بئر، فالق، غابة، خزان...) أو بالإنجليزية.

4) المراجعة والتصحيح (مهم)
---------------------------
الترجمة آلية بقاموس (00 - Arabic Translation Kit\ar_dict.py - حوالي 2860 مصطلحاً)
ومرتبة ككلمات مفتاحية بغرض البحث والفهم، وليست صياغة نهائية منقحة لغوياً
(ترتيب الكلمات إنجليزي، والتذكير/التأنيث والجمع غير منقحة).
- لكل نسخة يوجد ملف Translations_*.csv داخل نفس مجلد Arabic:
  الأعمدة: field | id | key | original | arabic | new_value | status
  (status = translated مترجمة / kept بقيت إنجليزية: كود أو اسم علم أو غير موجودة بالقاموس)
- راجع CSV في Excel وعدّل عمود arabic، ثم أعد تشغيل:
  00 - Arabic Translation Kit\translate_styles.py all
  (يعيد توليد النسخ من الأصول + القاموس المحدّث، والأصول لا تُمس أبداً - يُتحقق بـ SHA256)

5) ملاحظات تقنية
-----------------
- ملفات .stylx قواعد SQLite (جدول ITEMS: الاسم + الفئة + الوسوم).
- ملفات .style قواعد Jet (جداول Fill/Line/Marker Symbols + Colors...: الاسم + الفئة + الوسوم).
- BGS: الأسماء أكواد لونية (gb_50k_bedrock_N) فأُضيفت التسمية العربية للطبقة + وسم.
- FGDC/Alaska/GSC: الأسماء أكواد رقمية بقيت، والفئات الوصفية (Faults, Bedding...) تُرجمت.
- Soils: أسماء FAO (YERMOSOLS...) تُرجمت + الأكواد الحرفية (Zt) بقيت.
- Shell: الأسماء الوصفية تُرجمت + الاختصارات (GOC, OWC, FWL) والأرقام بقيت.
- OF2005: المراحل الزمنية (Albian...) والصخور (Granitoid...) تُرجمت + قيم RGB بقيت أرقاماً.
- ملفات .ldb المذكورة سابقاً (64 بايت) كانت ملفات قفل مؤقتة لقاعدة البيانات وليست بيانات.
