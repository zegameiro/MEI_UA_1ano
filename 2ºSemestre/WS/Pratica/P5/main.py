import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

endpoint = "http://localhost:7200"
repo_name = "movies"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

query = """
    PREFIX mov:<http://movies.org/pred/>
    SELECT ?actor_n
    WHERE{
    ?film mov:name "Blade Runner" .
    ?film mov:starring ?actor .
    ?actor mov:name ?actor_n .
    }
"""

payload_query = {"query": query}
res = accessor.sparql_select(body=payload_query,
repo_name=repo_name)
res = json.loads(res)
for e in res['results']['bindings']:
    print(e['actor_n']['value'])