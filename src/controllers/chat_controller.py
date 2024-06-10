import time


from src.routes import api, chat
from flask import request, make_response, jsonify
from langchain_community.utilities import SQLDatabase
import os

os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
api.register_blueprint(chat, url_prefix='/chat')
pod_id = os.environ.get("POD_ID")
pod_port = os.environ.get("POD_PORT")
model_name = os.environ.get("MODEL")

testdb = SQLDatabase.from_uri("sqlite:///test.db")

from src.llm import agent

agent = agent.Agent(model_name=model_name, pod_id=pod_id, port=pod_port)


@chat.route('/', methods=['POST'])
def complete():
    req = request.get_json()

    if 'prompt' in req:
        prompt = req['prompt']
        ctx = req['context']
      
        try:
           

            start = time.time()
            res = agent.response(prompt, ctx=ctx)
            end = time.time()
            duration = end - start
            print(res)
            return make_response(
                jsonify({"result": res, "time_took": f'{duration}s'}),
                200
            )
        except openai.APIError as e:
            return make_response(
                jsonify({"error": str(e)}),
                400
            )

    return make_response(
        jsonify({"result": "error", "msg": "no prompt given"}),
        400
    )
