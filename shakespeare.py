
import sys
import json
# from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200
)

def main():
    myfile = open("D:\Workspace\sample_data_for_elst\qa_cut.json",'r').read()
    rawdata = myfile.splitlines(True)
    i = 0
    json_str = ""
    docs = {}

    for line in rawdata:
        line = ''.join(line.split())
        # x = json.loads(line)
        # y = trim_qa_pair(x)

        header_str = '{"index":{"_index":"qa","_type":"qa_pair","_id":"' + str(i) + '"}}'
        header = json.loads(header_str)
        # print(header)
        # if line != "},":
        #     json_str = json_str+line
        # else:
        #     docs[i] = json_str+"}"
        #     json_str = ""
        #     print(docs[i])

        test = '{\
            "line_id": 111398,\
            "play_name": "A Winters Tale",\
            "speech_number": 38,\
            "line_number": "",\
            "speaker": "LEONTES",\
            "text_entry": "Exeunt"\
        }'
        res = es.index(index='qa', doc_type='qa_pair', id=i, body=test)

        print(res['result'])

        i = i + 1
        if i > 0: break
    # print(json_str)

def trim_qa_pair(x):
    del x["question"]["content_digest_id"]
    del x["question"]["intention_id"]
    del x["question"]["message"]["uuid"]
    del x["question"]["message"]["inst_id"]
    del x["question"]["message"]["prep_content"]
    del x["answer"]["content_digest_id"]
    del x["answer"]["intention_id"]
    del x["answer"]["message"]["uuid"]
    del x["answer"]["message"]["inst_id"]
    del x["answer"]["message"]["prep_content"]
    return x

if __name__ == '__main__':
    main()