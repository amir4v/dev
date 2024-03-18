import os
import requests as r
# from chunk import where, write_where


def download(link):
    filename = link.split('&name=')[1]
    path = 'videos/'+filename
    
    def inner(link, path, filename):   
        if os.path.exists(path):
            print(f'os.path.exists("{os.path.exists(path)}")', end=' - ')
            return True, filename
        
        chunk = (5000) *1024#KB
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }
        # From = where()
        From = 0
        _bytes = bytes()
        while True:
            to = From + chunk
            
            print(f'{int(to/1024/1024)}.MB/', end='')
            
            headers['Range'] = f'bytes={From}-{to}'
            response = r.get(link, headers=headers)
            
            From = to + 1
            
            _bytes = _bytes + response.content
            
            if len(response.content) < chunk:
                break
        
        if _bytes == bytes():
            return False, filename
        
        open(path, 'wb').write(_bytes)
        
        print()
        
        # write_where(0)
    
        return True, filename
    
    try:
        return inner(link, path, filename)
    except:
        try:
            os.system(f'rm {path}')
        except:
            pass
        # write_where(0)
        print('>>>ERROR')
