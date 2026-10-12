import json, os
_F = json.load(open(os.path.join(os.path.dirname(__file__) or ".", "refs_found_all.json")))
def R(sid):
    return [(x["source_name"], x["citation"], x["url"]) for x in _F.get(sid, [])]
