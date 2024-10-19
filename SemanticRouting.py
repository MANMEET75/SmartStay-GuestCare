from semantic_router import Route
from semantic_router import RouteLayer
from semantic_router.encoders import OpenAIEncoder
from semantic_router.encoders import HuggingFaceEncoder
from datetime import datetime, timedelta

# useful when user asks time
time_route = Route(
    name="get_time",
    utterances=[
        "what time is it?",
        "what is the time",
        "can u tell me the time",
    ],
)


encoder =HuggingFaceEncoder(model_name="nomic-ai/nomic-embed-text-v1.5")


routes = [time_route]
rl = RouteLayer(encoder=encoder, routes=routes, llm=llm)


def get_time():
    now = datetime.now()
    return f"The current time is {now.strftime('%H:%M')}. Use this information in your response."


def semantic_layer(query: str):
    route = rl(query)
    if route.name == "get_time":
        query += f" (SYSTEM NOTE: {get_time()})" 

    else:
        pass
    return query


