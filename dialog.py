

import json
# from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200
)

def main():
    myfile = open("D:\Workspace\sample_data_for_elst\dummyIrKnowledge_dialog.jsonl",'r').read()
    rawdata = myfile.splitlines(True)
    i = 0
    for line in rawdata:
        line = ''.join(line.split())
        x = json.loads(line)
        y = modify_dialog(x)
        if len(y) == 0:
            continue
        res = es.index(index='dialog_exp', doc_type='dialog', id=i, body=y)
        print(res['result'])
        i = i + 1
        # if i > 0: break
    # print(json_str)

def modify_dialog(x):

    print(x.keys())

    data = {}
    if "messages" not in x.keys():
        return data
    z = x["messages"]
    if len(z) == 0:
        return data

    data["channel"] = z[0]["message"]["channel"]
    data["skill"] = z[0]["message"]["skill"]
    data["dialog_id"] = z[0]["message"]["dialog_id"]

    msgs = []
    for item in z:
        msg = {}
        # print(item["message"].keys())
        msg["nth_turn"] = item["message"]["nth_turn"]
        msg["sender_type"] = item["message"]["sender_type"]
        msg["message_type"] = item["message"]["message_type"]
        msg["message_time"] = item["message"]["message_time"]
        msg["message"] = item["message"]["content"]
        msgs.append(msg)

    data["messages"] = msgs
    return data

if __name__ == '__main__':
    main()