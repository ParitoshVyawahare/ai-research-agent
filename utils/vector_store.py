import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="research_data",
    embedding_function=embedding_fn
)


def store_results(results: list[dict]):
    documents = []
    metadatas = []
    ids = []

    for i, r in enumerate(results):
        documents.append(r["content"])
        metadatas.append({
            "title": r["title"],
            "url": r["url"]
        })
        ids.append(f"doc_{i}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Stored {len(documents)} documents in vector store")


def retrieve_relevant(query: str, n_results: int = 3) -> list[dict]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    relevant = []
    for i in range(len(results["documents"][0])):
        relevant.append({
            "content": results["documents"][0][i],
            "title": results["metadatas"][0][i]["title"],
            "url": results["metadatas"][0][i]["url"]
        })

    return relevant