'''
Ok it's made with help of Sentdex
This is just starting point.
From this place I can make this Spider to acutaly do something on website.
My first idea is to collect email addresses :) 
Let's try it 
'''

from multiprocessing import Pool
import bs4 as bs
import random
import requests
import string
import re

def rand_str_url():
    middle = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _x in range(4))
    url = ''.join(['http://',middle,'.com'])
    return url
def handle_inside_links(url,link):
    if link.startswith('/'):
        return ''.join([url,link])
    else:
        return link
def get_emails(url):
   try:
       request = requests.get(url)
       soup = bs.BeautifulSoup(request.text, "lxml")
       bodys = soup.body
       sbody = str(bodys)
       redux = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
       emails = set(re.findall(redux, sbody))
       return emails

   except TypeError as e:
       print(e, "\n")
       print("TypeError, Iterating over None")
       return []
   except IndexError as e:
       print(e, "\n")
       print("IndexError, Iterating over empty list")
       return []
   except AttributeError as e:
       print(e, "\n")
       print("AttributeError, Iterating over None")
       return []
   except Exception as e:
       print(e)
       print("Exception occured why collecting emails ")
       return []
def get_links(url):
    try:
        request = requests.get(url)
        soup = bs.BeautifulSoup(request.text, 'lxml')
        body = soup.body
        links = [link.get('href') for link in body.find_all('a')]
        links = [handle_inside_links(url, link) for link in links]
        links = [str(link.encode("ascii")) for link in links]
        return links
    except TypeError as e:
        print(e,"\n")
        print("TypeError, Iterating over None")
        return []
    except IndexError as e:
        print(e,"\n")
        print("IndexError, Iterating over empty list")
        return []
    except AttributeError as e:
        print(e,"\n")
        print("AttributeError, Iterating over None")
        return []
    except Exception as e:
        print(str(e),"\n")
        return []

def main():
    numbr = 50
    while True:
        p = Pool(processes=numbr)
        parse_us = [rand_str_url() for _x in range(numbr)]

        data = p.map(get_links, [link for link in parse_us])
        data = [url for url_list in data for url in url_list]
        emails = p.map(get_emails, [link for link in parse_us])
        p.close()


        with open('urls.txt', 'a') as f:
            for d in data:
                f.write(str(d) + "\n")

        with open('emails.txt', 'a') as ew:
            for ems in emails:
                for em in ems:
                    em = str(em)
                    if (em != "set()") and (em != "[]"):
                        ew.write(em + "\n")

        emails = []
        data = []

if __name__ == '__main__':
    main()



