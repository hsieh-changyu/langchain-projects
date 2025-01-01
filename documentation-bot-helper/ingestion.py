from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs():
    loader = ReadTheDocsLoader("langchain-docs/api.python.langchain.com/en/latest")

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(
        documents, embeddings, index_name="langchain-doc-index"
    )
    print("****Loading to vectorstore done ***")


def ingest_firecrawl():
    from langchain_community.document_loaders.firecrawl import FireCrawlLoader

    base_url = ["https://docs.pinecone.io/guides/indexes/understanding-indexes",
                "https://docs.pinecone.io/guides/get-started/quickstart",
                "https://docs.pinecone.io/guides/organizations/manage-billing/changing-your-billing-plan"]
    base_url2 = ["https://docs.pinecone.io/guides/indexes/understanding-indexes","https://docs.pinecone.io/guides/get-started/quickstart"]
    for url in base_url2:
        loader = FireCrawlLoader(
            url=url,
            mode="crawl",
            params={
                "limit": 5, 
                "pageOptions": {"onlyMainContent": True}
            }
        )
        docs = loader.load()
        for doc in docs:
            new_url = doc.metadata["og:url"]
            doc.metadata.update({"source": new_url})

        print(f"Going to add {len(docs)} to Pinecone")
        PineconeVectorStore.from_documents(
            docs, embeddings, index_name="firecrawl-index"
        )
        print("****Loading to vectorstore done ***")
    


if __name__ == "__main__":
    #ingest_docs()
    ingest_firecrawl()
