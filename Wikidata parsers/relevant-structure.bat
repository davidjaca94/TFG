echo off
cls

set INPUT=all_wikidata_reduced_es-en.json
set OUTPUT=all_wikidata_relevant_es-en.json

py -3 relevant-structure.py --input_file %INPUT% --output_file %OUTPUT%

pause