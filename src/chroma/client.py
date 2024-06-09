import chromadb
from src.models.train_data import TrainingData

client = chromadb.Client()


class Chroma:

    def __init__(self, db_path):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(self.db_path)
        self.collections = dict()

    def new_client(self):
        return self.client

    def create_collection(self, name):
        c = self.client.create_collection(name=name, metadata={"hnsw:space": "cosine"})
        self.collections[name] = c

    def add_to_collection(self, collection_name, docs, ids):
        tb = self.client.get_collection(collection_name)
        tb.add(documents=docs, ids=ids)

    def add_examples(self, collection_name, tdata):
        tb = self.client.get_collection(collection_name)
        docs = [dt.prompt for dt in tdata]
        mdata = [{"input": dt.prompt, "query": dt.query} for dt in tdata]
        ids = [f'id{dt.id}' for dt in tdata]
        tb.add(documents=docs, metadatas=mdata, ids=ids)

    def get_similar_examples(self, collection_name, doc, tot):
        tb = self.client.get_collection(collection_name)
        res = tb.query(query_texts=[doc], n_results=tot)
        return res

    def query(self, collection_name, doc, results):
        tb = self.client.get_collection(collection_name)
        res = tb.query(query_texts=[doc], n_results=results)
        return res


# if __name__ == '__main__':
#     ch = Chroma('./database')
#     cl = ch.new_client()
#     table = "test"
#     # ch.create_collection(table)
#     documents = [
#         "This is a document about pineapple",
#         "This is a document about oranges",
#         "This is a document about color",
#         "This is a document about red",
#         "This is a document about blue",
#         "My name is Arsalan"
#     ]
#     ids = ["id1", "id2", "id3", "id4", "id5", "id6"]
#     ch.add_to_collection(table, documents, ids)
#     res = ch.query(table, "This is a query about yellow and yellow is a color different than fruits", 6)
#     print(res)
