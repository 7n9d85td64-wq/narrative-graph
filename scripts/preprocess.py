import zipfile, re, os, shutil

SRC = 'G:/写作系统/素材/未处理'
DST = 'G:/写作系统/素材/预分析'
# msys path fix
if not os.path.exists(SRC): SRC = '/g/写作系统/素材/未处理'
if not os.path.exists(DST): DST = '/g/写作系统/素材/预分析'

world_kw = {
    '修仙界': ['修仙','宗门','元婴','金丹','渡劫','飞升','灵根','修士','仙尊','仙帝','魔修','阐教'],
    '星际科幻': ['星际','星舰','机甲','虫族','宇宙','太空'],
    '游戏世界': ['游戏','副本','BOSS','公会','系统面板','登录','退出','帮战'],
    '废土末世': ['末世','丧尸','辐射','变异','废墟','末日','废土','避难所'],
    '古代架空': ['皇帝','王爷','太子','科举','江湖','将军','公主','侯府'],
    '现代都市': ['公司','总裁','手机','学校','高铁'],
    '年代背景': ['七十年代','八十年代','九十年代','种田','养崽','打渔']
}
f_kw = {
    '昆墟社会': ['考核','任务系统','正神','内卷'],
    '宗门联盟': ['宗门','长老','联盟','世家','帮会'],
    '帝国科层制': ['皇帝','朝廷','科举','官僚','律法'],
    '公司城': ['公司','股权','董事会','KPI'],
    '无政府竞争': ['弱肉强食','丛林法则','末世','求生','掠夺'],
    '血缘宗法制': ['家族','族长','宗祠','嫡系','血缘'],
    '民主议会制': ['议会','选举','投票','民主'],
    '神权统治': ['神','祭司','神殿','教皇']
}
b_kw = {
    '重生': ['重生','前世','上一世'],
    '穿书': ['穿书','穿成','穿越到','穿越'],
    '系统': ['系统','叮','绑定','天赋','金手指'],
    '马甲': ['马甲','假身份','伪装'],
    '扮猪吃虎': ['扮猪吃虎','隐藏实力'],
    '复仇': ['复仇','报仇','血债'],
    '种田': ['种田','打渔','养崽','经商']
}
c_kw = {'欲望驱动': ['登顶','第一','最强','碾压','我要','翻身'], '规则驱动': ['规矩','必须','任务','规则','考核'], '正向驱动': ['治愈','保护','守护','拯救','善意']}
d_kw = {'无CP': ['无CP','无感情线','单身','独行'], '甜宠': ['甜宠','宠溺','恋爱','CP','甜'], '虐恋': ['虐恋','虐心'], '修罗场': ['修罗场','多角']}
e_types = ['复仇虐渣','生死对决','情感拉扯','成长逆袭','日常治愈','权谋博弈','经营升级']

def best(kw_dict, text, tags):
    best_k, best_s = '待定', 0
    for k, kws in kw_dict.items():
        s = sum(text.count(kw)*2 + tags.count(kw) for kw in kws)
        if s > best_s: best_k, best_s = k, s
    return best_k if best_s > 0 else '待定'

epubs = [f for f in os.listdir(SRC) if f.endswith('.epub') and f != '已处理']
print(f'共 {len(epubs)} 本\n')

for epub_name in epubs:
    epub_path = os.path.join(SRC, epub_name)
    try:
        with zipfile.ZipFile(epub_path) as z:
            texts = []
            for name in sorted(z.namelist()):
                if name.endswith('.html') or name.endswith('.xhtml'):
                    try:
                        content = z.read(name).decode('utf-8','ignore')
                        text = re.sub(r'<[^>]+>', '\n', content)
                        text = re.sub(r'\n{3,}', '\n\n', text).strip()
                        if text: texts.append(text)
                    except: pass
        full = '\n\n'.join(texts)
        head = full[:2000].replace('\n', ' ')
        
        # title: just the book name (first line or from metadata)
        tm = re.search(r'书名[：:]\s*[《]?([^》\n]+)', head)
        if tm:
            book_title = tm.group(1).strip()[:25]
        else:
            book_title = epub_name.replace('.epub','').replace('：','_')[:25]
        book_title = re.sub(r'[\\/:*?"<>|]', '_', book_title)
        
        tags = ''
        tagm = re.search(r'标签[：:]\s*([^\n]+)', head)
        if tagm: tags = tagm.group(1)
        
        desc = head[500:1500]
        dm = re.search(r'(?:简介|文案)[：:]\s*(.+?)(?=第[一二三])', head, re.DOTALL)
        if dm: desc = dm.group(1).strip()[:500]
        
        cn = sum(1 for c in full if '\u4e00' <= c <= '\u9fff')
        platform = '番茄短篇' if cn < 300000 else '晋江长篇'
        
        a_pool = best(world_kw, head, tags)
        if a_pool == '待定': a_pool = '现代都市'
        f_pool = best(f_kw, head, tags)
        if f_pool == '待定': f_pool = '待定'
        b_pool = best(b_kw, head, tags)
        c_pool = best(c_kw, desc, tags)
        if c_pool == '待定': c_pool = '欲望驱动'
        d_pool = best(d_kw, head, tags)
        if d_pool == '待定': d_pool = '无CP'
        
        e_intensity = '强冲突' if any(k in tags+desc for k in ['生死','毁灭','杀','深渊','宣战']) else '中冲突'
        e_type = '成长逆袭'
        for t in e_types:
            if any(kw in tags+desc for kw in t.split('-')): e_type = t; break
        e_pool = e_intensity + '-' + e_type
        
        fname = f'{book_title}-{a_pool}-{f_pool}-{b_pool}-{c_pool}-{d_pool}-{e_pool}-预处理.md'
        dest_dir = os.path.join(DST, f'{a_pool}_{c_pool}_{e_pool}')
        os.makedirs(dest_dir, exist_ok=True)
        
        with open(os.path.join(dest_dir, fname), 'w', encoding='utf-8') as f:
            f.write(f'# {book_title}\n平台: {platform}\nA: {a_pool} F: {f_pool} B: {b_pool}\nC: {c_pool} D: {d_pool} E: {e_pool}\n标签: {tags}\n\n{full}')
        
        pool = f'{a_pool}_{c_pool}_{e_pool}'
        cnt = len(os.listdir(dest_dir))
        print(f'OK {book_title[:20]:20s} {platform:6s} {cn//10000}w字 | {a_pool}-{c_pool}-{e_pool:18s} | {pool} (+{cnt})')
        
        # move epub to done
        done_dir = os.path.join(SRC, '已处理')
        os.makedirs(done_dir, exist_ok=True)
        shutil.move(epub_path, os.path.join(done_dir, epub_name))
    except Exception as e:
        print(f'ERR {epub_name[:30]}: {e}')

print(f'\n===== DONE =====')
for d in sorted(os.listdir(DST)):
    path = os.path.join(DST, d)
    if os.path.isdir(path):
        print(f'  {d}: {len(os.listdir(path))}本')
