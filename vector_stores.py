from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config


class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding=embedding
        self.vector_store=Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )
    def get_retriever(self):
        # 返回向量检索器，方便加入链
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})


if __name__ == '__main__':
    retriever=VectorStoreService(embedding=DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()

    res=retriever.invoke("我体重150，尺码推荐")
    print(res)