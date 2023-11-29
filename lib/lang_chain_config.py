import json
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdf_text_extractor import extract_text_from_pdf
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQA

class LLMChainConfig:
  def __init__(self, config = {}):
    self._config = config
    self._load_embeddings()
    self._load_llm()
  
  def _load_embeddings(self):
    self._embedding = OpenAIEmbeddings()
  
  def _load_llm(self):
    self._llm = ChatOpenAI(temperature=0.6, verbose=True)
  

  def run(self, pdf_path, label = "PdfDataChunk", n_questions=1):
    text = extract_text_from_pdf(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000, chunk_overlap=50, length_function=len
    )

    chunks = text_splitter.split_text(text)
    v_store = Neo4jVector.from_texts(
      chunks,
      embedding=self._embedding,
      url = self._config["url"],
      username = self._config["username"],
      password = self._config["password"],
      index_name="quizme",
      node_label=label,
      pre_delete_collection=True,
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)

    qa = RetrievalQA.from_chain_type(llm=self._llm, retriever=v_store.as_retriever(), memory=memory)

    print("[Running] QA")
    result = qa({
        "query": f"""
               You are a assistant to a teacher. Using the context
              create questions, and provide the teacher with questions and the answers in JSON format.
              Make unique questions and answers using the context and also make sure that the answers are either one word or one line.
              Also make sure that you are using the whole context and not partially using the context.
              Make {n_questions} number of unique questions.
          """
      })
    
    return json.loads(result["result"])["questions"]