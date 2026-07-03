from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma

from langchain_ollama import OllamaEmbeddings
from functools import partial


BASE_DIR = Path(__file__).parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"

VECTOR_DB = BASE_DIR / "vector_db"


embedding = OllamaEmbeddings(
    model="embeddinggemma"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)


for collection_dir in KNOWLEDGE_DIR.iterdir():

    if not collection_dir.is_dir():
        continue

    loader = DirectoryLoader(
        collection_dir,
        glob="**/*.md",
        # loader_cls=TextLoader,
        loader_cls=partial(TextLoader, encoding="utf-8"),
    )

    docs = loader.load()

    for doc in docs:

        doc.metadata["collection"] = collection_dir.name

    splits = splitter.split_documents(docs)

    db = Chroma(
        persist_directory=str(VECTOR_DB),
        collection_name=collection_dir.name,
        embedding_function=embedding,
    )

    db.add_documents(splits)

    print(f"{collection_dir.name} indexed")