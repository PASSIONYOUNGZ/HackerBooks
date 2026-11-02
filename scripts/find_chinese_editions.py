"""Find Chinese edition titles by exact Open Library work ID; resumable metadata lookup."""
import concurrent.futures, json, pathlib, re, threading, time, urllib.parse, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
BOOKS=json.loads((ROOT/'data/catalogue.json').read_bytes())
CACHE=ROOT/'data/chinese-editions.json'
cache=json.loads(CACHE.read_bytes()) if CACHE.exists() else {}
todo=[b for b in BOOKS if b['status'] in ['machine','retained'] and b['id'].startswith('OL') and b['id'] not in cache]
groups=[todo[i:i+65] for i in range(0,len(todo),65)]
lock=threading.Lock();last=0
def fetch(group):
    global last
    query='language:chi AND ('+' OR '.join('key:/works/'+b['id'] for b in group)+')'
    params={'q':query,'fields':'key,title,editions,editions.title,editions.language,editions.key','lang':'zh','limit':100}
    url='https://openlibrary.org/search.json?'+urllib.parse.urlencode(params)
    for attempt in range(3):
        with lock:
            delay=1.25-(time.monotonic()-last)
            if delay>0:time.sleep(delay)
            last=time.monotonic()
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'HackerBooksChineseCatalogue/1.0 (public metadata research)'})
            with urllib.request.urlopen(req,timeout=30) as res:docs=json.load(res)['docs']
            out={b['id']:None for b in group}
            for doc in docs:
                ident=doc['key'].split('/')[-1]
                if ident not in out:continue
                for edition in doc.get('editions',{}).get('docs',[]):
                    title=edition.get('title','')
                    if 'chi' in edition.get('language',[]) and len(re.findall('[\u3400-\u9fff]',title))>=2:
                        out[ident]={'title':title,'url':'https://openlibrary.org'+edition['key'] if edition.get('key','').startswith('/') else 'https://openlibrary.org/works/'+ident};break
            return out
        except Exception as e:
            if attempt==2:return {}
            time.sleep(2+attempt*2)
print('Chinese edition lookup batches',len(groups),flush=True)
with concurrent.futures.ThreadPoolExecutor(2) as pool:
    for i,future in enumerate(concurrent.futures.as_completed([pool.submit(fetch,g) for g in groups]),1):
        cache.update(future.result());CACHE.write_text(json.dumps(cache,ensure_ascii=False,separators=(',',':')),encoding='utf8')
        if i%10==0 or i==len(groups):print(i,'/',len(groups),'checked',len(cache),'Chinese titles',sum(bool(x) for x in cache.values()),flush=True)
