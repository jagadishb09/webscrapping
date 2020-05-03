import difflib
with open('file1.rtf') as f1:
    f1_text = f1.read()
with open ('file2.rtf') as f2:
    f2_text = f2.read()
for line in difflib.unified_diff(f1_text, f2_text, fromfile='file1.rtf', tofile='file2.rtf', lineterm=''):
    print(line)