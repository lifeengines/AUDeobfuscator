import os
import sqlite3

matches = open('deobf/matches.txt', 'r').readlines()

conn_clean = sqlite3.connect('tmp/clean_structs.db')
cursor_clean = conn_clean.cursor()

conn_obf = sqlite3.connect('tmp/obf_structs.db')
cursor_obf = conn_obf.cursor()

current_pos = 0
var_matches = []
for l in matches:
    print(str(round((current_pos / len(matches)) * 100, 4)) + "%", end="\r")

    obf_classname = l.split("/")[0].strip()
    clean_classname = l.split("/")[1].strip()

    row_obf = cursor_obf.execute("SELECT * FROM symbols WHERE name='%s'" % obf_classname).fetchone()
    row_clean = cursor_clean.execute("SELECT * FROM symbols WHERE name='%s'" % clean_classname).fetchone()

    try:
        if row_obf[1] is not None:
            struct_obf_fields = row_obf[1].split(',')
            struct_obf_fields.pop(0)
        else:
            struct_obf_fields = None

        if row_obf[2] is not None:
            struct_obf_staticfields = row_obf[2].split(',')
            struct_obf_staticfields.pop(0)
        else:
            struct_obf_staticfields = None

        if row_clean[1] is not None:
            struct_clean_fields = row_clean[1].split(',')
            struct_clean_fields.pop(0)
        else:
            struct_clean_fields = None

        if row_clean[2] is not None:
            struct_clean_staticfields = row_clean[2].split(',')
            struct_clean_staticfields.pop(0)
        else:
            struct_clean_staticfields = None
        
        if struct_clean_fields is None and struct_clean_staticfields is None:
            continue
        if struct_obf_fields is None and struct_obf_staticfields is None:
            continue
    except:
        continue

    try:
        for index, obf_field in enumerate(struct_obf_fields):
            try:
                obf_varname = obf_field.split(" ")[-1]
                clean_varname = struct_clean_fields[index].split(" ")[-1]
                
                obf_varname = obf_varname.replace(";", "").replace("*", "")
                clean_varname = clean_varname.replace(";", "").replace("*", "")

                if obf_varname != clean_varname and '_' not in obf_varname and '_' not in clean_varname:
                    var_matches.append((obf_varname, clean_varname))
            except:
                continue
    except:
        continue
    current_pos += 1

conn_obf.close()
conn_clean.close()

f = open('deobf/matches.txt', 'a')
f.write("//start variable matches")
for (obfname, cleanname) in var_matches:
    f.write(obfname + "/" + cleanname + "\n")
    
print("Generated all variable name matches")