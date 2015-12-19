# -*- coding: UTF-8 -*-

import re
import urllib
import urllib2
import os
import urlparse
import requests

def name_of_url(url):
    adress = ''
    invalidSymbols = ['/', '\\', '|', '*', ':', '"', '?', '<', '>' ]
    for i in range(len(url)- 3):
        if not url[i] in invalidSymbols and url[i].isalnum():
            adress += url[i]
    return adress

def find_all_elements(url):
    content = urllib2.urlopen(url).read()
    img_urls = re.findall('img .*?src="(.*?)"', content)
    js_urls = re.findall('script .*?src="(http:*.*?)"', content)
    css_urls = re.findall('href .*?src="(.css)"', content)
    urls = img_urls + js_urls + css_urls
    return urls

def name_of_files(url):
    name = ''
    if url[len(url) - 1] == '/':
        url = url[:len(url) - 1]
    for i in range (url.rfind('/') + 1, len(url)):
        if  'A' <= url[i] <= 'Z' or 'a' <= url[i] <= 'z' or '0' <= url[i] <= '9' or url[i] == '.':
            name += url[i]
    return name

def rename(old_name, new_name, first, second, path):
    new_name = path + new_name
    file = open(first)
    file1 = open(second, 'w')
    line = file.readline()
    i = 0
    k = 0
    while line != '':
        if old_name in line:
            line1 = ''
            while k < len(line):
                if line[k: k + len(old_name)] == old_name:
                    line1 += new_name
                    k += len(old_name)
                else:
                    line1 += line[k]
                    k += 1
            file1.write(line1)
        else:
            file1.write(line)
        line = file.readline()
    file1.close()
    file.close()

def download_files(url, name, path):
    path_f = path + name
    if not ('https:' in url or 'http:' in url):
        url = 'http:' + url
    urllib.urlretrieve(url, path_f)

def all_urls(url, arr, string, host_name, path, page_name, already_check, folder):
    try:
        content = urllib.urlopen(url).read()
    except:
        content = ''
    if string in content:
        try:
            urllib.urlretrieve(url, url_name + '.txt')
            os.mkdir(folder)
            files = find_all_elements(url)
            k = 1
            for file in files:
                name = name_of_files(file)
                download_files(file, name, path)
                first = page_name + '.txt'
                second = 'output.txt'
                if k == 1:
                    rename(file, name, first, second, path)
                    k -= 1
                else:
                    rename(file, name, second, first, path)
                    k += 1

            if k == 1:
                os.rename(first, page_name + '.html')
                os.remove('output.txt')
            else:
                os.rename('output.txt', page_name + '.html')
                os.remove(first)
        except:
            print ('-')

    lst = re.findall('"((http|ftp)s?://*.*?)"', content)
    print (lst)
    print (len(lst))
    for i in range(len(lst)):
       new_url, b = lst[i]
       url_domain = urlparse.urlparse(new_url).hostname
       if url_domain == None:
           url_domain = ''
       if host_name in url_domain:
           if not 'http:' in new_url:
              if 'https' in new_url:
                  new_url = new_url[6::]
              new_url = 'http:' + new_url
           if not new_url in arr and not new_url in already_check:
              print (new_url)
              arr.append(str(new_url))
              print ('!!!', arr)
    return arr


os.chdir("C:/Python27/parsing")
url = 'https://hsp.kz/category/avtorskie-stati/'
word = 'android'
urls = []
urls.append(url)
host_name  = urlparse.urlparse(url).hostname
already_check = []

while len(urls) != 0:
    print (urls)
    url = urls.pop(0)
    print (urls, '+')
    print (already_check)
    already_check.append(url)
    url_name = name_of_url(url)
    print (url_name, url)
    folder = 'files_' + url_name
    path = './' + folder + '/'
    urls = all_urls(url, urls, word, host_name, path, url_name, already_check, folder)

