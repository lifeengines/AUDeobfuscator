import os

matches = open('deobf/matches.txt', 'r').readlines()

current_pos = 0
for l in matches:
    print(str(round((current_pos / len(matches)) * 100, 4)) + "%", end="\r")
    os.system("sed -i '' 's/" + l.strip() + "/g' deobf/*.h")

    current_pos += 1

print('''Deobfuscated all classname and variable name matches 
Exported deobfuscated files to deobf/il2cpp-types.h and deobf/il2cpp-types-ptr.h
''')