# Helper

def write_text(filename, text):
    return open(filename, 'w', encoding='utf-8').write(text)


def read_text(filename):
    return open(filename, 'r', encoding='utf-8').read()


def get_file_lines(filename):
    return read_text(filename).split('\n')
#
#
def file_lines(filename):
    return get_file_lines(filename)


def write_bytes(filename, _bytes):
    return open(filename, 'wb').write(_bytes)


def read_bytes(filename):
    return open(filename, 'rb').read()


def get_str(msg='>>> '):
    return input(msg)


def get_int(msg='>>> '):
    return int(input(msg))


def get_float(msg='>>> '):
    return float(input(msg))


def get_bool(msg):
    return bool(input(msg))


def unique_items(items):
    result = []
    
    for item in items:
        if item not in result:
            result.append(item)
    
    return result


def split(spliters, text):
    default_spliter = spliters[0]
    
    for spliter in spliters[1:]:
        text = text.replace(spliter, default_spliter)
    
    return text.split(default_spliter)


import string
def wordized(word, fa=False):
    apostrophes = """'"ˮ‘’“”"""
    
    if fa: # Fa
        string.ascii_letters = "چحخدذربپتثجز‌ژس‌شصضطظعغفقکگلمنوهی" + "ءاآ" + "َُِّۀًٍةيؤءهٔ"
        acceptable = string.ascii_letters + apostrophes + ' _-'
    else:  # En
        acceptable = string.ascii_letters + apostrophes + ' _-'
    
    extra = ' _-' + apostrophes
    all = string.printable + extra + acceptable
    stripable = ''.join(
                        set(all) - set(string.ascii_letters)
                        )
    
    chars = []
    for c in word:
        if c in acceptable:
            chars.append(c)
    word = ''.join(chars)
    
    return word.strip(stripable)


import string
def text_words(text, lower=True):
    if lower:
        text = text.lower()
    
    words = split(string.whitespace, text)
    words = unique_items(words) # UNIQUE
    words = [wordized(word) for word in words]
    words = unique_items(words) # UNIQUE
    
    if '' in words:
        words.remove('')
    
    return words


def file_words(filename, lower=True):
    text = read_text(filename)
    
    words = text_words(text, lower)
    
    return words


import requests as r
def get_url_content_type_file_extension(url):
    try:
        content_type = r.head(url).headers['content-type']
        ext = content_type.split('/')[1][:4].strip(' ;-,:=')
        if len(ext) < 1:
            raise Exception
        ext = f'.{ext}'
    except:
        ext = ''
    
    return ext


def url_ext(url):
    return get_url_content_type_file_extension(url)


from random import randint
def url_filename(url):
    if url.endswith('/'):
        url = url[:-1]
    
    try:
        name = url.split('/')[-1]
        if '.' in name:
            name = name.split('.')[:-1]
            name = ''.join(name)
        name = wordized(name)
        if len(name) < 1:
            raise Exception
    except:
        name = str(randint(1_000_000, 9_999_999))


import requests as r
def get_url_content_bytes_with_chunk(url, chunk=64, headers={}, cookies={}):
    chunk = 1024 * chunk
    _bytes = bytes()
    _from = 0
    
    while True:
        to = _from + chunk
        headers['Range'] = 'bytes=-'
        get = r.get(url, headers=headers, cookies=cookies)
        _bytes = _bytes + get.content
        _from = to
        
        if len(get.content) < chunk:
            break
    
    return _bytes


def download(url, filename=None, location='', headers={}, cookies={}):
    if filename == None:
        filename = url_filename(url) + url_ext(url)
        filename = filename.replace('/', '')
    
    _bytes = get_url_content_bytes_with_chunk(url, headers=headers, cookies=cookies)
    
    if location.endswith('/') or location == '':
        path = location + filename
    else:
        path = f'{location}/{filename}'
    
    open(path, 'wb').write(_bytes)
    
    return True, path


from pytube import YouTube
def youtube_download(url, quality='HD', filename=None, location=None):
    qualities = {
        'SD': '480',
        'HD': '720',
        
        'Full HD': '1080',
        'Full-HD': '1080',
        'FullHD': '1080',
        'F HD': '1080',
        'F-HD': '1080',
        'FHD': '1080',
        
        'MIN': 'MIN',
        'MAX': 'MAX',
    }
    quality = qualities.get(quality)
    
    yt = YouTube(url)
    
    streams = yt.streams.filter(file_extension='mp4').order_by('resolution')
    
    if quality == 'MIN':
        stream = streams.first()
    elif quality == 'MAX':
        stream = streams.last()
    else:
        stream = streams.filter(res=f'{quality}p').order_by('resolution').first()
    
    if filename == None:
        result = stream.download(output_path=location)
    else:
        result = stream.download(output_path=location, filename=filename)
    
    return True, stream, result


# from flask import Flask, request
# def show_video_in_web():
#     def inner():
#         app = Flask(__name__)

#         @app.route('/', methods=['GET', 'POST'])
#         def show_video():
#             url = request.form.get('url')
            
#             html_get_url = """
#             <form action="/" method="POST">
#             <textarea name="url" rows="5" placeholder="URL" style="width: 90%; font-size: 2em;"></textarea>
#             <br><br>
#             <input type="submit">
#             </form>
#             """
            
#             html_show_video = f"""
#             <video width="100%" height="100%" controls>
#                 <source src="{url}">
#             </video>
#             """
            
#             if url == None:
#                 return html_get_url
#             return html_show_video
    
#     inner()


import re
def get_all_sources_from_text(text, file_only=True, specific_file_extension=[]):
    result = []
    
    if not file_only:
        pattern = r'(href|src|action|data)="(.*)"'
        result.extend(re.findall(pattern, text))
    else:
        pattern = r'(href|src)="(.*\.[a-zA-Z0-9]{,4})"'
        result.extend(re.findall(pattern, text))
    
    result = [m[1] for m in result]
    result = unique_items(result)
    
    if len(specific_file_extension) > 0:
        temp_result = []
        for item in result:
            for ext in specific_file_extension:
                if item.endswith(ext):
                    temp_result.append(item)
                    continue
        result = temp_result
    
    return result


import re, requests as r
def get_all_sources_from_url(url, file_only=True, specific_file_extension=[]):
    result = []
    text = r.get(url).text
    
    return get_all_sources_from_text(text, file_only, specific_file_extension)


class RotationalList:
    def __init__(self, items=[]):
        self.r_list = []
        self.current_index = 0
        self.r_list.extend(items)
    
    def __str__(self):
        result = []
        current = self.current()
        
        for item in self.r_list:
            if item == current:
                item = f'({item})'
            result.append(item)
        
        return str(result)
    #
    def __repr__(self):
        return self.__str__()
    
    def current(self):
        return self.r_list[self.current_index]
    #
    def current_item(self):
        return self.current
    
    def rotate(self, times=None):
        def forward():
            if self.current_index == len(self.r_list)-1:
                self.current_index = 0
            else:
                self.current_index += 1
        
        def backward():
            if (self.current_index == 0) or (self.current_index == -len(self.r_list)):
                self.current_index = -1
            else:
                self.current_index -= 1
        
        def do_rotate(times):
            if times > 0:
                for _ in range(times):
                    forward()
            elif times < 0:
                times = abs(times)
                
                for _ in range(times):
                    backward()
        
        if times == None:
            forward()
        else:
            do_rotate(times)
    
    def next(self):
        # current
        current_item = self.current()
        
        # rotate
        self.rotate()
        
        return current_item
    
    def len(self):
        return len(self.r_list)
    
    def is_first(self):
        return self.current() == self.r_list[0]
    
    def is_last(self):
        return self.current() == self.r_list[-1]
    
    def get_list(self):
        return self.r_list
    #
    def all(self):
        return self.r_list
    
    def first(self):
        return self.r_list[0]
    
    def last(self):
        return self.r_list[-1]
    
    def init(self, items):
        self.__init__(items)
    
    def clear(self):
        self.__init__()
    
    def reset(self):
        self.current_index = 0
    
    def add(self, item):
        self.r_list.append(item)
    #
    def append(self, item):
        self.r_list.append(item)
    
    def extend(self, items):
        self.r_list.extend(items)
    
    def remove(self, item):
        self.r_list.remove(item)
#
#
class RL(RotationalList):
    pass


import requests as r
def get_url_response_text(url):
    return r.get(url).text
#
#
def url_response_text(url):
    return get_url_response_text(url)


from bs4 import BeautifulSoup as bs
def bs_find_all(url, wants):
    """
    want = text|string|'attribute'
    
    wants = [
        want == { tag, attribute='', value='', attributes={}, want=None }
        ...
    ]
    """
    
    result = []
    _soup = bs(url_response_text(url))
    
    def inner(want):
        inner_result = []
        
        if want == 'text':
            for tag in soup:
                inner_result.append(tag.text)
        elif want == 'string':
            for tag in soup:
                inner_result.append(tag.string)
        else:
            for tag in soup:
                inner_result.append(tag.get(want))
        
        return inner_result
    
    for _want in range(len(wants)):
        tag = wants[_want].get('tag')
        attribute = wants[_want].get('attribute', '')
        value = wants[_want].get('value', '')
        attributes = wants[_want].get('attributes', {})
        want = wants[_want].get('want', None)
        
        attributes[attribute] = value
        
        soup = _soup.find_all(tag, attributes)
        
        if want == None:
            return soup
        
        result.append(
            {f'{tag}-{want}': inner(want)}
        )
        
    return result


def hierarchy_bs(root_url, attributes={}, insider_tag='', insider_attributes={}, want=None, insider_raw=False, source=''):
    links = bs_find_all(root_url, 'a', attributes=attributes, want='href')
    
    result = []
    for l in links:
        if insider_raw:
            if not l.startswith('http'):
                l = source + l
            result.append(
                url_response_text(l)
            )
            continue
        
        result.extend(
            bs_find_all(l, insider_tag, attributes=insider_attributes, want=want)
        )
    
    return result


def clean_text(text):
    if not isinstance(text, str):
        return text
    
    text = text.strip()
    
    if len(text) == 0:
        return None
    
    return text


import string
from random import shuffle, sample, choices
def random_str(length=62, lowercase=True, uppercase=True, digits=True, symbols=False):
    chars = ''
    if lowercase:
        chars += string.ascii_lowercase
    if uppercase:
        chars +=  string.ascii_uppercase
    if digits:
        chars += string.digits
    if symbols:
        chars += string.punctuation
    chars = list(chars)
    
    shuffle(chars)
    if length > len(chars):
        return ''.join(choices(chars, k=length))
    return ''.join(sample(chars, length))


#
