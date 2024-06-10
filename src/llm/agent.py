
from langchain_community.llms import VLLMOpenAI
from src.llm import template
from src.chroma import client
import os

os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "false"


chroma = client.Chroma("sqlite:///chroma.db")

class Agent:
    name: str
    pod_id: str
    base_uri: str
    llm: VLLMOpenAI

    def __init__(self, model_name, pod_id, port):
        print(f'initializing agent with model {model_name} \n pod_id {pod_id} : {port}')
        self.pod_id = pod_id
        self.name = model_name
        base_uri = f'https://{self.pod_id}-{port}.proxy.runpod.net/v1/'
        self.llm = VLLMOpenAI(
            openai_api_key="EMPTY",
            openai_api_base=base_uri,
            model_name=self.name,
            # model_kwargs={"stop": [";"]}
        )

  

  

    def get_prompt_template(self, question, ctx):
       
        prompt = template.ans[0].format(question=question, context=ctx)
        return prompt


  
    def get_context(self, question):
        exs = chroma.get_similar_examples("examples", question, 5)
        return exs["metadatas"][0]

    

    def response(self, question, ctx):
        p = self.get_prompt_template(question, ctx)
        print(p)
        res = self.llm(p, stop=["Business Details"])

        print(res)

        return res
