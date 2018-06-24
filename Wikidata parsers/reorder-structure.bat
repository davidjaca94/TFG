echo off
cls

set INPUT=all_wikidata_relevant_es-en.json
set OUTPUT=all_wikidata_reordered.json

py -3 reorder-structure.py --input_file %INPUT% --output_file %OUTPUT%

pause