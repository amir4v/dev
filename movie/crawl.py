from helper import *
from proxy import Link as MovieLink


root_links = { # the value is class value
    # """
    "https://sorenfilm.ir  https://sorenfilm.ir/series/page/": "read-more-link btn btn-serial",
    "https://sorenfilm.ir  https://sorenfilm.ir/category/moviez/page/": "read-more-link btn btn-serial",
    "https://sorenfilm.ir  https://sorenfilm.ir/page/": "read-more-link btn btn-serial",
    #
    "https://vipofilm.com  https://vipofilm.com/page/": "more",
    "https://hexdownload.co  https://hexdownload.co/page/": "more-link",
    "https://karanmovie.org  https://karanmovie.org/page/": ".ادامه و دانلود.",
    #
    "https://movielandz.com  https://movielandz.com/page/": "AB-more-link",
    "https://film2serial.ir  https://film2serial.ir/page/": "btn btn-success d-lg-inline-block py-lg-10 py-10 d-block mb-lg-0 mb-10 mr-lg-auto mr-md-0 mr-10",
    "https://uptvs.com  https://uptvs.com/page/": "btn btn-outline-blue",
    #
    "https://zfilm.info  https://zfilm.info/all-movie/page/": "hover_bg_link",
    "https://zfilm.info  https://zfilm.info/series/page/": "hover_bg_link",
    "https://zfilm.info  https://zfilm.info/genre/anime/page/": "hover_bg_link",
    "https://zfilm.info  https://zfilm.info/genre/documentary/page/": "hover_bg_link",
    "https://zfilm.info  https://zfilm.info/genre/animation/page/": "hover_bg_link",
    #
    "https://bia2hd.store  https://bia2hd.store/page/": "read-more-link btn btn-film",
    "http://myhastidl1.cam  http://myhastidl1.cam/page/": "edame",
    # """
    "https://myezx.top  https://myezx.top/page/": "post_more",
    "https://golchindlz.xyz  https://golchindlz.xyz/page/": "more",
    #
    "https://atamovie.click  https://atamovie.click/page/": "more",
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # "https://mobomovies.fun  https://mobomovies.fun/movies/": ".مشاهده و دانلود.",
    # "https://mobomovies.fun  https://mobomovies.fun/series/": ".مشاهده و دانلود.",
    # "https://mobomovies.fun  https://mobomovies.fun/mini-series/": ".مشاهده و دانلود.",
    # "https://mobomovies.fun  https://mobomovies.fun/anime/": ".مشاهده و دانلود.",
    #
    # "http://starkmovie.af  http://starkmovie.af/letter/0-9/": "",
    # "http://starkmovie.af  http://starkmovie.af/letter/a/ (a-z)": "",
    #
    # "https://azintv2.website  https://azintv2.website/movie/page/": "",
    # "https://azintv2.website  https://azintv2.website/tvshow/page/": "",
    # "https://berlin.iamnotindangeriamthedanger.website/Movies/": "",
    # "https://rio.iamnotindangeriamthedanger.website/Series/": "",
    # "https://dlx.nikimoviez.ir/": "",
    # temp
    # "https://digimovie.vip  https://digimovie.vip/page/": "",
}


PAGE = int(read_text('PAGE'))
for page in range(PAGE, 10_000):
    for Link, todo in root_links.items():
        pre, Link = Link.split('  ')
        link = Link + str(page)
        
        print(link)
        
        raw_list = []
        
        if '.' in todo:
            for a in bs_find_all(link, 'a'):
                if todo.strip('.') in a.text:
                    href = a.get('href')
                    if not href.startswith('http'):
                        href = pre + href
                    raw_list.append(url_response_text(href))
        else:
            raw_list.extend(
                hierarchy_bs(link, attributes={'class': todo}, insider_raw=True, source=pre)
            )
        
        files = []
        
        for text in raw_list:
            files.extend(
                get_all_sources_from_text(text, specific_file_extension=['mp4', 'mkv'])
            )
        
        from django.db import IntegrityError
        for file_url in files:
            try:
                MovieLink(url=file_url).save()
                print('GOOD DB')
            except IntegrityError as e: 
                # if 'unique constraint' in e: # or e.args[0] from Django 1.10
                print('UNIQUE ERROR')
                print(e)
            except Exception as e:
                print(e)
    
    write_text('PAGE', str(page))
