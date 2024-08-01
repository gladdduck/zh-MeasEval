# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json
import pandas as pd
import os
import threading


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

def tsv_trans(file_name, zn_text):

    def map_function(df):
        result = trans_text(df['text'])
        df['text'] = result
        try:
            start = zn_text.index(result)
            end = start + len(result)
        except:
            start = -1
            end = -1
        df['startOffset'] = start
        df['endOffset'] = end
        return df
    data = pd.read_csv(file_name, sep='\t')
    data = data.apply(map_function,axis=1)
    def eval_other(x):
        try:
            return eval(x)
        except:
            return x
    data['other'] = data['other'].map(eval_other)
    data.to_csv('zh-'+file_name, sep='\t', index=False)

def process_files(file_name):
    file_name = file_name.replace('.txt', '')

    tsv_path = os.path.join('zh-tsv', file_name + '.tsv')
    if os.path.exists(tsv_path):
        print(file_name + ' already done')
        return True
    else:
        print(file_name + ' translating')

    text_path = os.path.join('text', file_name + '.txt')
    zn_text = txt_trans(text_path)

    for file in os.listdir('brat'):
        if file.startswith(file_name):
            if file.endswith('.txt'):
                txt_path = os.path.join('zh-brat', file)
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(zn_text+'\n')
            else:
                file_path = os.path.join('brat', file)
                ana_trans(file_path, zn_text)

    tsv_path = os.path.join('tsv', file_name + '.tsv')
    if os.path.exists(tsv_path):
        tsv_trans(tsv_path, zn_text)
    print('done')

from concurrent.futures import ThreadPoolExecutor
def main():
    # 设置线程池的最大线程数为2
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     # 遍历目录中的文件
    #     for file_name in os.listdir('txt'):
    #         # 将任务提交给线程池执行
    #         executor.submit(process_files, file_name)
    #         break
    for file_name in os.listdir('text'):
        process_files(file_name)


if __name__ == "__main__":
    if not os.path.exists('zh-brat'):
        os.mkdir('zh-brat')
    if not os.path.exists('zh-tsv'):
        os.mkdir('zh-tsv')
    if not os.path.exists('zh-text'):
        os.mkdir('zh-text')
    main()



            
