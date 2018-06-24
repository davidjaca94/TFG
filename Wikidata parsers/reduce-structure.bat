echo off
cls

set INPUT=all_wikidata.json
set OUTPUT=all_wikidata_reduced_es-en.json
set LANG=es en

py -3 reduce-structure.py --input_file %INPUT% --output_file %OUTPUT% --languages %LANG%

pause