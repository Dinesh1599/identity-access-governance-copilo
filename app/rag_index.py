import os, glob
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document


POLICY_DIR = os.getenv("POLICY_DIR", "data/policies")
VEC_DIR = os.getenv("VEC_DIR", "data/vecstore")




def _load_docs() -> list[Document]:
    docs = []
    for path in glob.glob(os.path.join(POLICY_DIR, "**/*"), recursive=True):
        if os.path.isdir(path):
            continue
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        docs.append(Document(page_content=text, metadata={"source": os.path.basename(path)}))
        print(docs)
    return docs




def build_or_load_index():
    os.makedirs(VEC_DIR, exist_ok=True)
    index_path = os.path.join(VEC_DIR, "faiss_index")
    embeddings = OpenAIEmbeddings()

    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    docs = _load_docs()
    splits = splitter.split_documents(docs)

    store = FAISS.from_documents(splits, embeddings)
    store.save_local(index_path)
    return store