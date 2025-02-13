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
promptTemplate = PromptTemplate.from_template("{content}\n\n" +
  "위의 문서 내용을 요약해 주세요. 요약할 때 다음 사항을 포함해 주세요:\n" +
  "1. 주요 주제와 핵심 포인트\n" +
  "2. 중요한 세부 사항\n" +
  "3. 결론 또는 요약된 결과\n\n" +
  "요약된 내용을 한국어로 번역해 주세요. 번역할 때 정확성과 자연스러움을 유지해 주세요.\n\n" +
  "번역된 내용을 마크다운 형식으로 보여 주세요. 마크다운 형식의 예시는 다음과 같습니다:\n" +
  "# 요약\n\n" +
  "## 주요 주제\n- ...\n\n" +
  "## 핵심 포인트\n- ...\n\n" +
  "## 중요한 세부 사항\n- ...\n" +
  "## 결론\n- ...\n\n" +
  "마크다운의 표나 리스트 같은 서식, 하이라이트 등을 적극적으로 활용해 주세요."
)
input_pass = RunnableLambda(input_selector)

# connecting chains
doc_summary_agent = input_pass | promptTemplate
doc_summary_agent |= llmModel
doc_summary_agent |= outputParser

__all__ = ["doc_summary_agent"]