import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import glob

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	# there may be more elements you don't want, such as "style", etc.
]

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

def epub_to_txt(input_path, output_path):
    file_name = input_path.split('/')[-1]
    file_name = file_name.split('.')[0]
    out = epub2text(input_path)
    with open(output_path + file_name + '.txt', 'w', encoding='utf-8') as txt_copy:
        for string in out:
            txt_copy.write(string)


file_list = glob.glob('D:/Downloads/EpubProcess/*')
for path in file_list:
    path = path.replace('\\', '/')
    try:
        epub_to_txt(path, 'D:/Downloads/LibGen_txts/')
    except Exception:
        print(path)
        pass