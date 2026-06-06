import json, urllib.request, os, glob

key = 'dataset-7eRPatytAMnbYwwdwMWsQqHh'
base = 'http://localhost:80/v1/datasets/7298a996-b0ad-4595-b441-7b737e87f4fc/document/create_by_text'
root = 'C:/Users/Administrator/WorkBuddy/2026-06-05-17-53-25/narrative-graph/data'

count = 0
for f in glob.glob(root + '/**/*.json', recursive=True):
    name = f[len(root)+1:].replace('\\', '/')
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        data = json.dumps({
            'name': name,
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
            count += 1
    except Exception as e:
        print('ERR', name, str(e)[:80])

print('Done:', count, 'files')
