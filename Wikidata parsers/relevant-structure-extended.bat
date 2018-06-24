echo off
cls

set INPUT=all_wikidata_reduced_es-en.json
set OUTPUT=all_wikidata_relevant_extended_es-en.json

py -3 relevant-structure-extended.py --input_file %INPUT% --output_file %OUTPUT%

pause