from bs4 import BeautifulSoup
import requests
import re
import shutil
import json
import os
from collections import OrderedDict
from pprint import pprint
import pathlib
import time
from multiprocessing import Pool
from urllib.request import urlopen
from parse import compile

start = time.time()
text = ""
loc = "1" #input("위치 : ")
upHpAreaId = 2
hpAreaId = 1026 #input("AreaId : ")


file = 'C:/Users/k/Desktop/json/TempPlace.json'
basefile = 'C:/Users/k/Desktop/json/hhhppp/hotplace.json'
kofile = 'C:/Users/k/Desktop/json/ko.xlf'
kobasefile = 'C:/Users/k/Desktop/json/hhhppp/ko.xlf'
shutil.copy(basefile, file)



def get_links():
    print("link")

    r = requests.get("https://www.siksinhot.com/taste?upHpAreaId=" + str(upHpAreaId) + "&hpAreaId=" + str(hpAreaId) + "&isBestOrd=N")
    soup = BeautifulSoup(r.text, "html.parser")
    # 전화번호 parsing을 위한 pid
    mr = soup.find_all("script")
    pattern = "\"pid\":[^,]+"
    r = re.compile(pattern)
    results = r.findall(str(mr))
    # 추천 맛집 string 정리
    it = iter(results)
    list = []
    while True:
        try:
            pid = next(it)
            pid = pid[6:]
            list.append(pid)

        except StopIteration:
            break
    return list

def get_content(link):
    print("content")
    abs_link = "https://www.siksinhot.com/P/" + link
    r = requests.get(abs_link)
    soup = BeautifulSoup(r.text, "html.parser")

    # 상호명 parsing
    p = compile("\"pname\":\"{}\"")
    result = p.parse(soup)
    pname = result[0]


    # 주소 parsing
    p = compile("\"addr\":\"{}\"")
    result = p.parse(soup)
    addr = result[0]

    # 전화번호 parsing
    p = compile("phone_number\",\"content\":\"{}\"")
    result = p.parse(soup)
    phone_number = result[0]

    text += "\""+loc+"의 $hotplace-kind 맛집은 "+pname+" 입니다. "+pname+"의 주소는 "+addr+" 입니다. 전화번호는 "+phone_number+"입니다. \n 다른 음식 추천을 원하시면 다시 음식 종류를 말해주시고 종료를 원하시면 취소를 말씀해주세요.\",\n"

if __name__=='__main__':
    print("main")
    start_time = time.time()
    pool = Pool(processes=8) # 4개의 프로세스를 사용합니다.
    pool.map(get_content, get_links()) # get_contetn 함수를 넣어줍시다.
    print("--- %s seconds ---" % (time.time() - start_time))

print(text)
'''
            # r = requests.get("https://www.siksinhot.com/P/" + pid)
            # soup = BeautifulSoup(r.text, "html.parser")


            # 주소 parsing
            mr = soup.find_all("script")
            pattern = "\"addr\":\"[^\"]+"
            r = re.compile(pattern)
            results = r.findall(str(mr))
            '''
'''
if(len(results) == len(list)):
    str +="\""+loc+"의 $hotplace-kind 맛집은 "+pname+" 입니다. 다른 음식 추천을 원하시면 다시 음식 종류를 말해주시고 종료를 원하시면 취소를 말씀해주세요.\""
else:
    str +="\""+loc+"의 $hotplace-kind 맛집은 "+pname+" 입니다. 다른 음식 추천을 원하시면 다시 음식 종류를 말해주시고 종료를 원하시면 취소를 말씀해주세요.\",\n"
'''


"""
# 상호명 parsing
mr = soup.find_all("script")
pattern = "\"pname\":\"[^\"]+"
r = re.compile(pattern)
results = r.findall(str(mr))
"""

'''
# 기본 파일에 위치, 추천 맛집 텍스트 넣기
import codecs
fileObj = codecs.open(basefile, "r", "utf-8" )
u = fileObj.readlines()
text = ""
for i in u :
    i = i.replace("ㅁㅈㅇㅊ", loc)
    i = i.replace("ㄹㅋㅇㅅ", str)
    text += i+'\n'

fw = codecs.open(file, 'w', 'utf8')
fw.write(text)
fw.close()

# ko.xlf 파일 수정해서 압축파일 만들기
fileObj = codecs.open(kobasefile, "r", "utf-8" )
u = fileObj.readlines()
text = ""
for i in u :
    i = i.replace("목동", loc)
    text += i+'\n'

fw = codecs.open(kofile, 'w', 'utf8')
fw.write(text)
fw.close()

# 압축
os.chdir("C:/Users/k/Desktop/json")
import zipfile
with zipfile.ZipFile('namespace.zip', mode='w') as f:
    f.write('ko.xlf', compress_type=zipfile.ZIP_DEFLATED)
'''
