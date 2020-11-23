import sqlite3
import os

clean_type_file = open("data/clean/il2cpp-types.h", "r")
clean_ptr_file = open("data/clean/il2cpp-types-ptr.h", "r")
conn = sqlite3.connect('tmp/clean_structs.db')

c = conn.cursor()
c.execute('''CREATE TABLE symbols (name text, fields text, staticfields text, class text, vtable text)''')
for i in clean_ptr_file.readlines():
    if "DO_TYPEDEF" in i:
        name = i.split(",")[1].split(")")[0].strip()
        c.execute("INSERT INTO symbols VALUES (\'" + name + "\', NULL, NULL, NULL, NULL)")
conn.commit()

reading = False
data = []
lines = clean_type_file.readlines()
currentcount = 0
for i in lines:
    print(str(round((currentcount / len(lines)) * 100, 4)) + "%", end="\r")

    if not reading:
        if "struct " in i and " {" in i and "typedef" not in i:
            symbolname = i.split(" ")[1]
            if(symbolname == "__declspec(align(4))"):
                symbolname = i.split(" ")[2]
            
            if "Fields" in symbolname or "Class" in symbolname or "VTable" in symbolname or "StaticFields" in symbolname and "Array" not in symbolname:
                c.execute("SELECT * FROM symbols WHERE name='%s'" % symbolname.split("__")[0])
            else:
                c.execute("SELECT * FROM symbols WHERE name='%s'" % symbolname)

            rsymbol = c.fetchone()
            if(rsymbol is not None):
                reading = True
                data.append(symbolname)
    else:
        if "};" in i:
            reading = False
            try:
                if "Fields" in data[0] or "Class" in data[0] or "VTable" in data[0] or "StaticFields" in data[0]:
                    if("StaticFields" in data[0]):
                        c.execute("UPDATE symbols SET staticfields=\'" + ','.join(data) + "\' WHERE name='%s'" % data[0].split("__")[0])
                    elif("Class" in data[0]):
                        c.execute("UPDATE symbols SET class = \'" + ','.join(data) + "\' WHERE name='%s'" % data[0].split("__")[0])
                    elif("VTable" in data[0]):
                        c.execute("UPDATE symbols SET vtable = \'" + ','.join(data) + "\' WHERE name='%s'" % data[0].split("__")[0])
                    elif("Fields" in data[0]):
                        c.execute("UPDATE symbols SET fields = \'" + ','.join(data) + "\' WHERE name='%s'" % data[0].split("__")[0])
                conn.commit();
            except:
                continue
            
            data = []
        else:
            data.append(i.strip())
    currentcount += 1

conn.close()

print("Generated clean struct database")