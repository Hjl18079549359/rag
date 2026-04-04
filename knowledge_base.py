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
        # 如果文件夹不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma=Chroma(
            collection_name=config.collection_name,#数据库名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,#数据库本地存储文件夹
        )#向量存储实例Chroma向量数据库对象
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )#文本分割器的对象

    def upload_by_str(self,data,filename):
        # 将传入的字符串，进行向量化，存入向量数据库中
#         先得到传入字符串的md5值
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        if len(data)>config.max_split_char_number:
            knowledeg_chunks=self.spliter.split_text(data)
        else:
            knowledeg_chunks=[data]
        metadata={
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"huang"

        }
        self.chroma.add_texts(
            knowledeg_chunks,
            metadatas=[metadata for _ in knowledeg_chunks],
        )
        save_md5(md5_hex)
        return "[成功]，内容已经成功载入向量库"


if __name__ == '__main__':
    # r1=get_string_md5("黄谨来")
    # r2 = get_string_md5("黄谨来")
    # r3 = get_string_md5("黄谨来")
    #
    #
    # print(r1)
    # print(r2)
    # print(r3)
    # print(check_md5("8bc9d300be4e7d15e6184b8a0b146723"))
    service=KnowledgeBaseService()
    res=service.upload_by_str("黄金来","testfile.txt")
    print(res)