
import sys
import json
# from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200
)

def main():
    myfile = open("D:\Workspace\sample_data_for_elst\data_shakespeare_cut.json",'r').read()
    rawdata = myfile.splitlines(True)
    i = 0
    json_str = ""
    docs = {}

    for line in rawdata:
        line = ''.join(line.split())

        header_str = '{"index":{"_index":"shakespeare","_type":"line","_id":"' + str(i) + '"}}'
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
        res = es.index(index='shakespeare', doc_type='line', id=i, body=test)

        print(res['result'])

        i = i + 1
        if i > 0: break
    # print(json_str)


if __name__ == '__main__':
    main()