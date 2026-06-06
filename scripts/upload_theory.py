import json, urllib.request

key = 'dataset-7eRPatytAMnbYwwdwMWsQqHh'
base = 'http://localhost:80/v1/datasets/7298a996-b0ad-4595-b441-7b737e87f4fc/document/create_by_text'
G = 'G:/obsidian文件夹/小说系统/'

files = [
    ('叙事动力学·理论库', G + '叙事动力学·理论库.txt'),
    ('叙事动力学·参数库', G + '叙事动力学·参数库.txt'),
    ('叙事动力学·交互库', G + '叙事动力学·交互库.txt'),
    ('叙事动力学·V3.1完整理论', G + '叙事动力学·完整理论体系 V3.1 最终完整版.txt'),
    ('叙事动力学·案例库归档规范', G + '叙事动力学·案例库归档规范.txt'),
]

for name, path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        data = json.dumps({
            'name': name + '.txt',
            'text': content,
            'indexing_technique': 'high_quality',
            'process_rule': {'mode': 'automatic'}
        }).encode('utf-8')
        req = urllib.request.Request(base, data=data, headers={
            'Authorization': 'Bearer ' + key,
            'Content-Type': 'application/json'
        }, method='POST')
        with urllib.request.urlopen(req) as resp:
            r = json.loads(resp.read())
            print('OK:', name, '({} chars)'.format(len(content)))
    except Exception as e:
        print('ERR:', name, str(e)[:120])

print('\nDone')
