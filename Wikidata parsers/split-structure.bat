echo off
cls

set INPUT=all_wikidata_relevant_es-en.json

python split-structure.py --input_file %INPUT%

pause