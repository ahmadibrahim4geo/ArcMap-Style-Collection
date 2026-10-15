Geomorphological Style for ArcMap - README (v2)
=================================================
Folder: Geomorphological Style  |  Project: Style ArcMap
Date: 2026-09-28  |  ArcMap: 10.x  |  File: Geomorphological.style (175 symbols)

CONTENTS
--------
- Geomorphological.style ................ 70 Fill + 39 Line + 34 Marker + 32 Color = 175 symbols
- Raw_Data\Fill_Symbols.csv ............. 70 polygon units (AR/EN + RGB + outline)
- Raw_Data\Line_Symbols.csv ............. 39 lines (RGB + width + dash style)
- Raw_Data\Marker_Symbols.csv ........... 22 built point symbols (simple shapes)
- Raw_Data\Harvested_Markers.csv ........ 12 original ESRI/CADD symbols (triangles, wind/slope
                                          arrows, spring, waterfall, rapids, quarry, borrow pit,
                                          sediment sample, spot elevation) with source IDs
- Raw_Data\Colors.csv ................... 32 colors (RGB palette)
- Raw_Data\build_geomorph_style.py ...... builds the 163 custom symbols (ArcObjects/Python 2.7)
- Raw_Data\harvest_symbols.ps1 .......... injects the 12 original symbols byte-for-byte
- Sources\المصادر-والروابط.txt ......... sources with website + download links
- Preview\legend_preview.png ............ fills + colors swatches
- Preview\legend_preview_lines_markers.png  lines + markers index
- دليل-التركيب-والاستخدام.txt ........... Arabic install + usage guide (v2)

FIX IN v2
---------
Peak triangles that rendered as wheelchair icons (wrong glyph 116) were removed and
replaced with the original ESRI Triangle 1/4/5 + CADD wind/slope arrows + standard
hydro/quarry symbols (IDs 23-34 in Marker Symbols table).

QUICK START
-----------
1. ArcMap > Customize > Style Manager > Styles... > Add Style to List > select Geomorphological.style
2. Check it, then search Symbol Selector: dune, sabkha, wadi, fault, terrace, peak, moraine,
   till, karst, lava, quarry, waterfall, spring, cuesta, sandur...
3. Or copy the .style to C:\Program Files (x86)\ArcGIS\Desktop10.8\Styles\ for permanent listing.

SOURCES (verified links, see Sources folder for full list)
----------------------------------------------------------
- FGDC Geologic Map Symbolization: https://ngmdb.usgs.gov/fgdc_gds/geolsymstd.php
- Download page: https://ngmdb.usgs.gov/fgdc_gds/geolsymstd/download.php
- Full PDF: https://ngmdb.usgs.gov/fgdc_gds/geolsymstd/fgdc-geolsym-all.pdf
- GeMS + ArcGIS styles: https://ngmdb.usgs.gov/Info/standards/GeMS/
- ITC Verstappen & van Zuidam (library): https://library.wur.nl/WebQuery/titel/553295
- UvA geomorph legend: https://dare.uva.nl/document/25021
- ESRI symbol library PDFs: https://support.esri.com/en-us/patches-updates/2016/arcmap-symbol-library-854
- ColorBrewer: https://colorbrewer2.org
- Harvested from local ArcMap install: ESRI.style (Triangle 1/4/5) + CADD GIS Center SDS 220.Style
  (wind_direction_arrow, slope_direction_arrow, spring/waterfall/rapids/quarry/borrow-pit/sample/spot symbols)
