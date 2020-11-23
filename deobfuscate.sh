mkdir tmp
mkdir deobf
python3 generate_db_clean.py
python3 generate_db_obf.py
python3 find_obfuscated.py
python3 find_common_structs.py
echo "Check obfuscated functions then press enter to continue"
open tmp/obfuscated_classnames.txt
read
python3 struct_match.py
python3 variable_match.py
cp data/obf/il2cpp-types.h deobf/il2cpp-types.h
cp data/obf/il2cpp-types-ptr.h deobf/il2cpp-types-ptr.h
cp data/obf/il2cpp-functions.h deobf/il2cpp-functions.h
python3 deobfuscate.py
echo "Finished struct deobfuscation starting function deobfuscation"
python3 generate_hashtable.py
