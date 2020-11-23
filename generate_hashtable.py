import sqlite3
import hashlib

classname_file = open("tmp/unmatched_clean.txt", "r")
classnames = classname_file.readlines()

conn_clean = sqlite3.connect('tmp/clean_structs.db')
cursor_clean = conn_clean.cursor()

conn_hash = sqlite3.connect('tmp/hashtable.db')
cursor_hash = conn_hash.cursor()

cursor_hash.execute('''CREATE TABLE hashes (hash text, name text)''')
current_pos = 0
for classname in classnames:
    print(str(round((current_pos / len(classnames)) * 100, 4)) + "%", end="\r")

    classname = classname.strip()
    row = cursor_clean.execute("SELECT * FROM symbols WHERE name='%s'" % classname).fetchone()

    fields_length = 0
    static_fields_length = 0

    if row[1] is not None:
        struct_fields = row[1].split(',')
        struct_fields.pop(0)
        fields_length = len(struct_fields)
    else:
        struct_fields = None

    if row[2] is not None:
        struct_staticfields = row[2].split(',')
        struct_staticfields.pop(0)
        static_fields_length = len(struct_staticfields)
    else:
        struct_staticfields = None
    
    cursor_hash.execute("INSERT INTO hashes VALUES (\'" + str(hashlib.sha1(bytes(str(fields_length) + '_' + str(static_fields_length), encoding='utf8')).hexdigest()) + "\', \'" + classname + "\')")
    current_pos += 1
print("Generated hashtabel")
