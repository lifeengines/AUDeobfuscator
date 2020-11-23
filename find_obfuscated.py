import sqlite3

obf_type_file = open("data/obf/il2cpp-types.h", "r")

conn_clean = sqlite3.connect('tmp/clean_structs.db')
cursor_clean = conn_clean.cursor()

conn_obf = sqlite3.connect('tmp/obf_structs.db')
cursor_obf = conn_obf.cursor()

diff = []

obfuscated_structs = cursor_obf.execute('SELECT * FROM symbols').fetchall()
current_pos = 0
for row in obfuscated_structs:
    print(str(round((current_pos / len(obfuscated_structs)) * 100, 4)) + "%", end="\r")
    struct_name = row[0]

    cursor_clean.execute("SELECT * FROM symbols WHERE name='%s'" % struct_name)

    rsymbol = cursor_clean.fetchone()
    if(rsymbol is None and "_" not in struct_name):
        diff.append(struct_name)

    current_pos += 1

conn_clean.close()
conn_obf.close()

f = open('tmp/obfuscated_classnames.txt', 'w')
for i in diff:
    f.write(i + "\n")

print('Classnames written to tmp/obfuscated_classnames.txt')