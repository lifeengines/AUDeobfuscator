import sqlite3

obf_classname_file = open("tmp/obfuscated_classnames.txt", "r")
obf_classnames = obf_classname_file.readlines()

common_classname_file = open("tmp/common_classnames.txt", "r")
common_classnames = common_classname_file.readlines()

conn_clean = sqlite3.connect('tmp/clean_structs.db')
cursor_clean = conn_clean.cursor()

conn_obf = sqlite3.connect('tmp/obf_structs.db')
cursor_obf = conn_obf.cursor()

clean_structs = cursor_clean.execute('SELECT * FROM symbols').fetchall()
current_pos = 0
matches = []
for classname in obf_classnames:
    print(str(round((current_pos / len(obf_classnames)) * 100, 4)) + "%", end="\r")
    classname = classname.strip()
    row = cursor_obf.execute("SELECT * FROM symbols WHERE name='%s'" % classname).fetchone()

    if row[1] is not None:
        struct_fields = row[1].split(',')
        struct_fields.pop(0)
    else:
        struct_fields = None

    if row[2] is not None:
        struct_staticfields = row[2].split(',')
        struct_staticfields.pop(0)
    else:
        struct_staticfields = None
    
    if row[3] is not None:
        struct_class = row[3].split(',')
        struct_class.pop(0)
    else:
        struct_class = None

    if row[4] is not None:
        struct_vtable = row[4].split(',')
        struct_vtable.pop(0)
    else:
        struct_vtable = None

    def_canidate = None
    canidates = []
    for struct in clean_structs:
        if struct_fields is not None and struct[1] is not None:
            fields = struct[1].split(',')
            fields.pop(0)
            if len(fields) == len(struct_fields):               
                if(struct[0] + "\n" not in common_classnames and "_" not in struct[0]):
                    canidates.append(struct)

    for canidate in canidates:
        if struct_staticfields is not None and canidate[2] is not None:
            staticfields = canidate[2].split(',')
            staticfields.pop(0)
            if len(staticfields) != len(struct_staticfields):            
                canidates.remove(canidate)

    for canidate in canidates:
        if struct_fields is not None and canidate[1] is not None:
            fields = canidate[1].split(',')
            fields.pop(0)
            
            for index, field in enumerate(fields):  
                if field.split(" ")[0].strip() != struct_fields[index].split(" ")[0].strip():
                    if canidate in canidates:
                        canidates.remove(canidate)
                        break
    
    for canidate in canidates:
        if struct_fields is not None and canidate[1] is not None:
            fields = canidate[1].split(',')
            fields.pop(0)
            
            for index, field in enumerate(fields):  
                varname = field.split(" ")[-1]
                struct_varname = struct_fields[index].split(" ")[-1]
                if varname == struct_varname and "_" not in varname:
                    def_canidate = canidate
                    break
    current_pos += 1
    if def_canidate is not None:
        if def_canidate in clean_structs:
            clean_structs.remove(def_canidate)
        matches.append((classname, def_canidate[0]))
        continue

    if len(canidates) > 0:
        if canidate[0] in clean_structs:
            clean_structs.remove(canidate[0])
        matches.append((classname, canidate[0]))
    


f = open('deobf/matches.txt', 'w')
for (obfname, cleanname) in matches:
    obf_classnames.remove(obfname + "\n")
    f.write(obfname + "/" + cleanname + "\n")
    
f = open('deobf/unmatched.txt', 'w')
for obfname in obf_classnames:
    f.write(obfname)

f = open('tmp/unmatched_clean.txt', 'w')
for struct in clean_structs:
    f.write(struct[0] + "\n")
conn_obf.close()
conn_clean.close()
print("Generated all classname matches (not very accurate)")