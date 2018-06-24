echo off
cls

set INPUT=all_wikidata_relevant_extended_es-en.json
set OUTPUT=all_wikidata_reordered_extended.json

py -3 reorder-structure-extended.py --input_file %INPUT% --output_file %OUTPUT%

pause