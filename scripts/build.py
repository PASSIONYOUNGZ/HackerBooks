"""Build a self-contained reading room. Standard library only; no network."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://passionyoungz.github.io/HackerBooks/'

def build():
    data = {key: json.loads((ROOT / 'data' / f'{filename}.json').read_text(encoding='utf-8'))
            for key, filename in [('books', 'catalogue'), ('topics', 'topics'), ('groups', 'groups'), ('meta', 'meta')]}
    books = data['books']
    assert len(books) == data['meta']['n_books'], 'Book count does not match snapshot metadata'
    assert len({b['id'] for b in books}) == len(books), 'Duplicate work IDs'
    topic_ids = {t['slug'] for t in data['topics']}
    assert all(b.get('cn') and b.get('t') and all(t in topic_ids for t in b['tp']) for b in books)
    assert set().union(*(set(g['topics']) for g in data['groups'])) == topic_ids
    footer = (ROOT / 'src/footer.html').read_text(encoding='utf-8').replace('<details open>', '<details>')
    footer = footer.replace('页面内数据及样式均已嵌入，无需联网即可浏览和搜索。', '页面内书目数据及样式均已嵌入，可离线搜索；真实封面需要联网加载。')
    footer = footer.replace('</ul>', '<li><b>封面</b>：沿用原站封面编号，并从 Open Library 为同作品补充版本封面，可能为外文版本，不表示中文译本封面。图片按需联网加载；缺失或加载失败时显示明确标注的排版占位图。<a href="https://openlibrary.org/dev/docs/api/covers" target="_blank" rel="noopener noreferrer">Open Library 封面服务说明</a>。</li></ul>')
    footer = footer.replace('</footer>', '<div class="footer-signature"><span>HACKERBOOKS · 中文主题书单</span><a href="https://github.com/PASSIONYOUNGZ/HackerBooks" target="_blank" rel="noopener noreferrer">项目源码 ↗</a><span>STAY CURIOUS. KEEP READING.</span></div></footer>')
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = (ROOT / 'src/index.template.html').read_text(encoding='utf-8')
    replacements = {'__DATA__': payload, '__CSS__': (ROOT / 'src/library.css').read_text(encoding='utf-8'),
                    '__JS__': (ROOT / 'src/library.js').read_text(encoding='utf-8'), '__FOOTER__': footer}
    for key, value in replacements.items():
        html = html.replace(key, value)
    assert not any(key in html for key in replacements), 'Unresolved template token'
    return html

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify the committed HTML matches source and data')
    args = parser.parse_args()
    html = build()
    dest = ROOT / 'docs/index.html'
    if args.check:
        assert dest.exists() and dest.read_text(encoding='utf-8') == html, 'Run python scripts/build.py and commit docs/index.html'
        print('PASS: embedded catalogue, topics, and published HTML are consistent.')
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding='utf-8')
        print(f'Built {dest} ({len(html.encode("utf-8")):,} bytes)')
