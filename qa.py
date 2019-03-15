
import sys
import json
# from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200
)

def main():
    myfile = open("D:\Workspace\sample_data_for_elst\dummyIrKnowledge_qa.jsonl",'r').read()
    rawdata = myfile.splitlines(True)
    i = 0
    json_str = ""
    docs = {}

    for line in rawdata:
        line = ''.join(line.split())
        x = json.loads(line)
        y = trim_qa_pair(x)
        header_str = '{"index":{"_index":"qa","_type":"qa_pair","_id":"' + str(i) + '"}}'
        header = json.loads(header_str)
        res = es.index(index='qa', doc_type='qa_pair', id=i, body=y)
        print(res['result'])
        i = i + 1
        # if i > 0: break
    # print(json_str)

def trim_qa_pair(x):

    x.update({"channel": x["question"]["message"]["channel"]})
    x.update({"skill": x["question"]["message"]["skill"]})
    x.update({"dialog_id": x["question"]["message"]["dialog_id"]})

    del x["question"]["content_digest_id"]
    del x["question"]["intention_id"]

    x["question"].update({"nth_turn": x["question"]["message"]["nth_turn"]})
    x["question"].update({"speaker_id": x["question"]["message"]["speaker_id"]})
    x["question"].update({"sender_type": x["question"]["message"]["sender_type"]})
    x["question"].update({"message_type": x["question"]["message"]["message_type"]})
    x["question"].update({"message_time": x["question"]["message"]["message_time"]})
    x["question"].update({"message": x["question"]["message"]["content"]})

    # del x["question"]["message"]["uuid"]
    # del x["question"]["message"]["inst_id"]
    # del x["question"]["message"]["prep_content"]
    del x["answer"]["content_digest_id"]
    del x["answer"]["intention_id"]

    x["answer"].update({"nth_turn": x["answer"]["message"]["nth_turn"]})
    x["answer"].update({"speaker_id": x["answer"]["message"]["speaker_id"]})
    x["answer"].update({"sender_type": x["answer"]["message"]["sender_type"]})
    x["answer"].update({"message_type": x["answer"]["message"]["message_type"]})
    x["answer"].update({"message_time": x["answer"]["message"]["message_time"]})
    x["answer"].update({"message": x["answer"]["message"]["content"]})

    # del x["answer"]["message"]["uuid"]
    # del x["answer"]["message"]["inst_id"]
    # del x["answer"]["message"]["prep_content"]
    return x

if __name__ == '__main__':
    main()