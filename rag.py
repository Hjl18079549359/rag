from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

import config_data as config
from vector_stores import VectorStoreService
from langchain_community.chat_models.tongyi import ChatTongyi


def print_prompt(prompt):
    print("*" * 30)
    print(prompt.to_string())
    print("*" * 30)
    return prompt
class RagService(object):
    def __init__(self):
        self.vector_service=VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题，参考资料：{context}"),
                ("user","请回答用户提问：{input}")
            ]
        )
        self.chat_model=ChatTongyi(model=config.chat_model_name)
        self.chain=self.__get_chain()
    def __get_chain(self):
        # 获取最终的执行链
        retriever=self.vector_service.get_retriever()
        def format_document(docs:list[Document]):
            if not docs:
                return "无相关资料"
            format_str=""
            for doc in docs:
                format_str+=f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return format_str
        chain=(
            {"input":RunnablePassthrough(),"context":retriever|format_document}
            |self.prompt_template|print_prompt|self.chat_model|StrOutputParser()
        )
        return chain
if __name__ == '__main__':
    service=RagService()
    chain=service.chain
    res=chain.invoke("体重150，尺码推荐")
    print(res)
