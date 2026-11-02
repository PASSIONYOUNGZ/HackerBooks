"""Apply sourced Chinese editions and context-aware title edits without network calls."""
import collections,json,pathlib,re
from opencc import OpenCC
ROOT=pathlib.Path(__file__).resolve().parents[1]
books=json.loads((ROOT/'data/catalogue.json').read_bytes())
editions=json.loads((ROOT/'data/chinese-editions.json').read_bytes())
cc=OpenCC('t2s');changes=[]
edits={}
for line in (ROOT/'data/title-edits.txt').read_text(encoding='utf8').splitlines():
    rank,name=line.split('|',1);edits[int(rank)]=name
evidence={
 46:('reference','https://craftinginterpreters.com/'),
 73:('published','https://search.worldcat.org/title/1020336574'),
 75:('reference','https://www.penguinrandomhouse.com/books/294259/accelerando-by-charles-stross/'),
 172:('published','https://www.sanmin.com.tw/product/index/001475539'),
 399:('published','https://phei.com.cn/module/goods/wssd_content.jsp?bookid=33817'),
 1485:('published','https://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-67722-2'),
}
def change(book,name,kind,source=None):
    old=book['cn']
    book['status']='edition' if kind=='edition' else 'common' if kind=='published' else 'edited'
    book['cn_method']=kind
    if source:book['cn_source']=source
    if old==name:return
    book.setdefault('cn_previous',old)
    book['cn']=name
    changes.append({'id':book['id'],'original':book['t'],'before':old,'after':name,'method':kind,**({'source':source} if source else {})})

for b in books:
    candidate=editions.get(b['id'])
    if candidate and b['status'] in ['machine','retained']:
        name=cc.convert(candidate['title']).strip()
        name=re.sub(r'\s+\([A-Za-z][A-Za-z\s]*\)\s*$','',name)
        name=name.replace('哈利. 波特','哈利·波特').replace('哈利.波特','哈利·波特').replace('哈利 ・波特','哈利·波特').replace('哈利。波特与"混血王子','哈利·波特与混血王子')
        name=name.replace('大卫. 科波菲尔','大卫·科波菲尔').replace('果売中的宇宙','果壳中的宇宙')
        if name=='Water Margin水浒传':name='水浒传'
        # Prefer reliable plain metadata; leave OCR damage and English-edition labels for review.
        if not any(bad in name for bad in ['教唆熊','英文版', '",']):change(b,name,'edition',candidate['url'])
    rank=b['rank']
    if rank in edits and (b['status'] not in ['edition','common','wiki'] or rank in evidence):
        kind,source=evidence.get(rank,('reference',None));change(b,edits[rank],kind,source)
    if b['status']=='machine':
        name=b['cn'];original=b['t']
        tech=bool(set(b['tp'])&{'programming','computer-science','software-engineering','lisp-functional','systems','web'})
        if tech:
            if re.search(r'\bRuby\b',original,re.I):name=name.replace('红宝石','Ruby')
            if re.search(r'\bRails\b',original,re.I):name=name.replace('铁路','Rails')
            if re.search(r'\bRacket\b',original,re.I):name=name.replace('球拍','Racket')
            if re.search(r'\bElixir\b',original,re.I):name=name.replace('灵丹妙药','Elixir').replace('灵药','Elixir')
            if re.search(r'\bLisp\b',original,re.I):name=name.replace('口齿不清','Lisp')
            if re.search(r'\bWindows\b',original,re.I):name=name.replace('窗口','Windows')
            if re.search(r'\bForth\b',original,re.I):name=name.replace('前进','Forth').replace('第四','Forth')
            if re.search(r'\bRust\b',original,re.I):name=name.replace('生锈','Rust').replace('铁锈','Rust')
            if re.search(r'\b(Python|Ruby|Rust|Haskell|Elixir|Clojure|Erlang|Go|JavaScript)\b',original,re.I):name=name.replace('食谱','编程实例')
            if re.search(r'\bFunctional\b',original,re.I):name=name.replace('功能性','函数式')
            if re.search(r'\bInterpreter',original,re.I):name=name.replace('口译员','解释器')
        if name!=b['cn']:change(b,name,'terminology')
    if b['cn'].endswith('（原名保留）'):b['cn']=b['cn'][:-6]

# The source's year for Accelerando is erroneous; the publisher dates the first ebook to 2005.
accelerando=next(b for b in books if b['rank']==75)
if accelerando['y']==1900:
    accelerando['source_y']=1900;accelerando['y']=2005
    accelerando['year_source']='https://www.penguinrandomhouse.com/books/294259/accelerando-by-charles-stross/'
(ROOT/'data/catalogue.json').write_text(json.dumps(books,ensure_ascii=False,separators=(',',':')),encoding='utf8')
report_path=ROOT/'data/title-review-report.json'
previous=json.loads(report_path.read_bytes()).get('changes',[]) if report_path.exists() else []
by_id={x['id']:x for x in previous}
for x in changes:
    if x['id'] in by_id:x['before']=by_id[x['id']]['before']
    by_id[x['id']]=x
report={'date':'2026-11-02','revised_entries':len(by_id),'edition_lookup_checked':len(editions),'edition_candidates':sum(bool(v) for v in editions.values()),'methods':dict(collections.Counter(b.get('cn_method','original') for b in books)),'changes':list(by_id.values())}
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Revised entries',len(by_id),'methods',report['methods'])
