"""
知识库
"""
import hashlib
import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.util import md5_hex
from datetime import datetime

import config_data as config
from langchain_chroma import Chroma
# 检查传入md5字符串是否已经被处理过
def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w',encoding="utf-8").close()
        return False#True:md5已处理过,false:md5未处理过
    else:
        lines=open(config.md5_path, 'r',encoding="utf-8").readlines();
        for line in lines:
            line = line.strip()#处理字符串前后的空格和回车
            if line == md5_str:
                return True
        return False
# 将传入的md5字符串，记录到文件内保存
def save_md5(md5_str: str):
    with open(config.md5_path, 'a',encoding="utf-8") as f:
        f.write(md5_str+'\n')
# 将传入的字符串转换为md5字符串
def get_string_md5(input_str: str ,encoding='utf-8' ):
    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    md5 = hashlib.md5()#得到md5对象
    md5.update(str_bytes)#更新内容（传入即将要转换的字符数组）
    return md5.hexdigest()#得到md5的十六进制字符串

class KnowledgeBaseService:
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma =None
        self.spliter=None
    def upload_by_str(self,data,filename):
        # 将传入的字符串，进行向量化，存入向量数据库中
        pass


if __name__ == '__main__':
    # r1=get_string_md5("黄谨来")
    # r2 = get_string_md5("黄谨来")
    # r3 = get_string_md5("黄谨来")
    #
    #
    # print(r1)
    # print(r2)
    # print(r3)
    print(check_md5("8bc9d300be4e7d15e6184b8a0b146723"))