import requests

print(requests.get(url="https://norgau.com/search/?PAGEN_1=1&sort=null-null&size=72&q=%D1%88%D1%82%D0%B0%D0%BD%D0%B3%D0%B5%D0%BD%D1%86%D0%B8%D1%80%D0%BA%D1%83%D0%BB%D1%8C").text)