# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json
import pandas as pd
import os
import threading
from tqdm import tqdm

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import time
SecretId = "1"
SecretKey = "1"

class Translator:
    def __init__(self, from_lang, to_lang):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, text):
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

        req = models.TextTranslateRequest()
        req.SourceText = text
        req.Source = self.from_lang
        req.Target = self.to_lang
        req.ProjectId = 0

        resp = client.TextTranslate(req)
        return resp.TargetText
translator = Translator(from_lang="en", to_lang="zh")
def trans_text(q):
    result = translator.translate(q)
    return result

def txt_trans(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        result  = trans_text(" ".join(lines))
    with open('zh-'+file_name, 'w', encoding='utf-8') as f:
        f.write(result)
    return result
    

def ana_trans(file_name, zn_text):
    with open(file_name, encoding='utf-8') as f:
        lines = f.readlines()
    trans_lines = []
    for line in lines:
        line = line.strip('\n').strip().replace('\t\t','\t')
        text = line.split('\t')[-1]
        
        if text!='' and len(line.split('\t'))==3 and not line.split('\t')[0].startswith('#'):
            t,start,end = line.split('\t')[1].split(' ')
            result  = trans_text(text)
            try:
                start = zn_text.index(result)
                end = start + len(result)
            except:
                start = -1
                end = -1
            mid = f"{t} {start} {end}"
            sanjin = '\t'
            temp = f"{line.split(sanjin)[0]}\t{mid}\t{result}"
            trans_lines.append(temp)
        else:
            trans_lines.append(line)
    with open('zh-'+file_name, 'w', encoding='utf-8') as f:
        for line in trans_lines:
            f.write(line+'\n')



def process_files(file_name):
    file_name = file_name.replace('.ann', '')


    text_path = os.path.join('txt', file_name + '.txt')
    zn_text = ""
    with open(text_path, 'r', encoding='utf-8') as f:
        zn_text = f.read()
    
    file = file_name + '.ann'
    file_path = os.path.join('ann', file)
    ana_trans(file_path, zn_text)
                
    print('done')


def main():
    for file_name in tqdm(os.listdir('ann'), desc="Processing files"):
        process_files(file_name)


if __name__ == "__main__":
    if not os.path.exists('zh-ann'):
        os.mkdir('zh-ann')
    main()



            
