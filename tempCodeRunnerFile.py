for url in urls:
    r=requests.get(url)
    soup=bf(r.content,'html.parser')
    print(soup.prettify())
