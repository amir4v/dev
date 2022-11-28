from helper import *
from proxy import Link as MovieLink


root_links = { # the value is class value
    f"https://sorenfilm.ir/series/page/": "read-more-link btn btn-serial",
    f"https://sorenfilm.ir/category/moviez/page/": "read-more-link btn btn-serial",
    f"https://sorenfilm.ir/page/": "read-more-link btn btn-serial",
    
    f"https://vipofilm.com/page/": "more",
    f"https://hexdownload.co/page/": "more-link",
    f"https://karanmovie.org/page/": ".ادامه و دانلود.",
    #
    # f"https://azintv2.website/movie/page/": "",
    # f"https://azintv2.website/tvshow/page/": "",
    # https://berlin.iamnotindangeriamthedanger.website/Movies/
    # https://rio.iamnotindangeriamthedanger.website/Series/
    # https://dlx.nikimoviez.ir/
    #
    f"https://movielandz.com/page/": "AB-more-link",
    f"https://www.film2serial.ir/page/": "btn btn-success d-lg-inline-block py-lg-10 py-10 d-block mb-lg-0 mb-10 mr-lg-auto mr-md-0 mr-10",
    f"https://www.uptvs.com/page/": "btn btn-outline-blue",
    #
    f"https://zfilm.info/all-movie/page/": "hover_bg_link",
    f"https://zfilm.info/series/page/": "hover_bg_link",
    f"https://zfilm.info/genre/anime/page/": "hover_bg_link",
    f"https://zfilm.info/genre/documentary/page/": "hover_bg_link",
    f"https://zfilm.info/genre/animation/page/": "hover_bg_link",
    #
    f"https://bia2hd.store/page/": "read-more-link btn btn-film",
    f"http://myhastidl1.cam/page/": "edame",
    f"https://myezx.top/page/": "post_more",
    f"https://golchindlz.xyz/page/": "more",
    #
    f"https://atamovie.click/page/": "more",
    #
    f"https://mobomovies.fun/movies/": ".مشاهده و دانلود.",
    f"https://mobomovies.fun/series/": ".مشاهده و دانلود.",
    f"https://mobomovies.fun/mini-series/": ".مشاهده و دانلود.",
    f"https://mobomovies.fun/anime/": ".مشاهده و دانلود.",
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # f"http://starkmovie.af/letter/0-9/": "",
    # f"http://starkmovie.af/letter/a/ (a-z)": "",
    #
    # temp
    # f"https://digimovie.vip/page/": "",
}


for page in range(1, 10_000):
    for Link, todo in root_links.items():
        link = Link + str(page)
        raw_list = []
        
        if '.' in todo:
            raw_list.extend(
                [url_response_text(a.get('href'))
                for a in bs_find_all(link, 'a')
                if todo.strip('.') in a.text]
            )
        else:
            raw_list.extend(
                hierarchy_bs(link, attributes={'class': todo}, insider_raw=True)
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
        
        print(link)
