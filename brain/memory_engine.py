import os
import config
import chromadb
from chromadb.utils import embedding_functions
import uuid
from datetime import datetime, timezone
import json
import math

os.environ["HF_HOME"] = "D:/Python/hf_cache"
os.environ["HF_TOKEN"] = config.HF_TOKEN

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-miniLM-L6-v2"
)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="AIs_memory",
    embedding_function=embedding_fn
    )

def createDB():
    if not os.path.exists(config.LONG_TERM_MEMORY):
        file = open(config.LONG_TERM_MEMORY,"x")
        file.close()
    if not os.path.exists(config.SHORT_TERM_MEMORY):
        file = open(config.SHORT_TERM_MEMORY,"x")
        file.close()
    if not os.path.exists(config.USER_PROFILE):
        file = open(config.USER_PROFILE,"x")
        file.close

def updateHistory(sessionHistory: list, prompt, reply):
    sessionHistory.append("user:"+prompt)
    sessionHistory.append("AI:"+reply)
    return sessionHistory

def updateLongTermMemory(memory):
    
    
    ids=[]
    document=[]
    metadata=[]
    memory = memory.replace("```json","").replace("```","").strip()
    memory = json.loads(memory)
    for m in memory["memories"]:
        ids.append(str(uuid.uuid4()))
        document.append(m["document"])
        metadata.append({
            **m["metadata"],
            "user_id":config.USER,
            "created_at":datetime.now(timezone.utc).isoformat(),
            "last_accessed":datetime.now(timezone.utc).isoformat(),
            "access_count":0,
            "frequency":0,
            "recency":0
            })
    collection.add(
        ids = ids,
        documents= document,
        metadatas= metadata
    )
def retrieveMemory(query):
    result = collection.query(
        query_texts=[query],
        n_results = min(10, collection.count())
    )
    relevant_memory=[]
    ids = []
    metadatas = []

    for i in range(len(result["ids"][0])):

        metadata = result["metadatas"][0][i]
        distance = result["distances"][0][i]
        similarity = max(0, 1 - distance)

        score = (
            0.5 * similarity +
            0.1 * metadata.get("frequency", 0) +
            0.2 * metadata.get("recency", 0) +
            0.2 * metadata.get("importance", 0)
        )

        relevant_memory.append({
            "id": result["ids"][0][i],
            "document": result["documents"][0][i],
            "score": score,
            "metadata": metadata
        })
    top5 = sorted(relevant_memory,key=lambda x:x["score"],reverse=True)[:min(5, collection.count())]
    
    for memory in top5:
        metadata = memory["metadata"]

        last_accessed_dt = datetime.fromisoformat(
            metadata["last_accessed"]
        )

        now = datetime.now(timezone.utc)
        time_diff = (now - last_accessed_dt).total_seconds() / 86400

        new_access_count = metadata.get("access_count", 0) + 1

        updated_metadata = {
            **metadata,
            "last_accessed": now.isoformat(),
            "access_count": new_access_count,
            "frequency": math.log(1 + new_access_count),
            "recency": math.exp(-0.1 * time_diff)
        }

        ids.append(memory["id"])
        metadatas.append(updated_metadata)

    collection.update(ids=ids, metadatas=metadatas)

    print(top5)
    if not top5:
        memory_context = "no relevent memories"
    else:
        memory_context = "\n".join([
            f"- {m['document']}" for m in top5
        ])

    return memory_context