from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.document_loaders import PyMuPDFLoader

def text_extracter(file_path, start_page, end_page = None):
    loader = PyMuPDFLoader(file_path)
    start_page = start_page - 1 if start_page > 0 else 0
    if end_page:
        end_page = end_page - 1 if end_page - 1 > start_page else start_page
    else:
        end_page = start_page
    i = 0
    contents = ""
    for page in loader.lazy_load():
        if i >= start_page and i <= end_page:
            contents += "\n\n" + (page.page_content)
        i += 1
    return contents

def input_selector(inputs: dict) -> dict:
    file_path = inputs.get("file_path")
    start_page = inputs.get("start_page")
    end_page = inputs.get("end_page")
    return {"content" : text_extracter(file_path, start_page, end_page)}

llmModel = ChatOpenAI()
outputParser = StrOutputParser()
promptTemplate = PromptTemplate.from_template("{content}\n\n 주어진 문서의 내용을 요약해줘. 요약된 내용은 한국어로 번역해서 마크다운 형식으로 보여줘.")
input_pass = RunnableLambda(input_selector)

# connecting chains
doc_summary_agent = input_pass | promptTemplate
doc_summary_agent |= llmModel
doc_summary_agent |= outputParser

__all__ = ["doc_summary_agent"]