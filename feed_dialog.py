import argparse
import json
from elasticsearch import Elasticsearch

JSN_KEY_MSGS = "messages"

JSN_KEY_MSSG = "message"
JSN_KEY_CDID = "content_digest_id"
JSN_KEY_ITID = "intention_id"

JSN_KEY_UUID = "uuid"
JSN_KEY_CHNL = "channel"
JSN_KEY_SKLL = "skill"
JSN_KEY_DLID = "dialog_id"
JSN_KEY_SPID = "speaker_id"
JSN_KEY_ISID = "inst_id"
JSN_KEY_NTRN = "nth_turn"
JSN_KEY_SDTP = "sender_type"
JSN_KEY_MGTP = "message_type"
JSN_KEY_MGTM = "message_time"
JSN_KEY_CTNT = "content"
JSN_KEY_CTNP = "prep_content"
JSN_KEY_CTNS = "seg_content"
JSN_KEY_ENTS = "entities"
JSN_KEY_ETFM = "entity_from_idx"
JSN_KEY_ETTO = "entity_to_idx"
JSN_KEY_ETTP = "entity_type"

MAP_KEY_MSGS = JSN_KEY_MSGS
MAP_KEY_CHNL = JSN_KEY_CHNL
MAP_KEY_SKLL = JSN_KEY_SKLL
MAP_KEY_DLID = JSN_KEY_DLID
MAP_KEY_UUID = JSN_KEY_UUID
MAP_KEY_SPID = JSN_KEY_SPID
MAP_KEY_ISID = JSN_KEY_ISID
MAP_KEY_CDID = JSN_KEY_CDID
MAP_KEY_ITID = JSN_KEY_ITID
MAP_KEY_NTRN = JSN_KEY_NTRN
MAP_KEY_SDTP = JSN_KEY_SDTP
MAP_KEY_MGTP = JSN_KEY_MGTP
MAP_KEY_MGTM = JSN_KEY_MGTM
MAP_KEY_CTNT = JSN_KEY_CTNT
MAP_KEY_CTNS = JSN_KEY_CTNS
MAP_KEY_ENTS = JSN_KEY_ENTS
MAP_KEY_ETFM = JSN_KEY_ETFM
MAP_KEY_ETTO = JSN_KEY_ETTO
MAP_KEY_ETTP = JSN_KEY_ETTP

SKILL_TYPE_MOBILE = "MOBILE"
SKILL_TYPE_PC = "PC"

INDEX_DIALOG_MOBILE = "dialog_mobile"
INDEX_DIALOG_PC = "dialog_pc"
DOC_TYPE = "dialog"


def readlines():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The filename to be processed")
    args = parser.parse_args()
    if args.filename:
        with open(args.filename) as f:
            for line in f:
                yield line.strip('\n')


def string2dct(string):
    return json.loads(string)


es = Elasticsearch(
    ['localhost'],
    port=9200
)


def main():

    lines = readlines()
    obj_mobile_i = 0
    obj_pc_i = 0
    cnt = 0
    print("Parsing ...")
    while True:
        try:
            line = next(lines)
            json_dct = string2dct(line)
            data_bdy = reorg_dialog(json_dct)
            if len(data_bdy) == 0:
                continue

            if data_bdy[JSN_KEY_SKLL].upper() == SKILL_TYPE_MOBILE:
                res = es.index(
                    index=INDEX_DIALOG_MOBILE, doc_type=DOC_TYPE, id=obj_mobile_i, body=data_bdy)
                print("skill: {}, doc {}: {}".format(SKILL_TYPE_MOBILE, obj_mobile_i, res['result']))
                obj_mobile_i += 1
            elif data_bdy[JSN_KEY_SKLL].upper() == SKILL_TYPE_PC:
                res = es.index(
                    index=INDEX_DIALOG_PC, doc_type=DOC_TYPE, id=obj_pc_i, body=data_bdy)
                print("skill: {}, doc {}: {}".format(SKILL_TYPE_PC, obj_pc_i, res['result']))
                obj_pc_i += 1
            cnt += 1
        except StopIteration:
            break
    print("Done!")
    print("{} dialog, {} mobile dialog, {} pc dialog".format(cnt, obj_mobile_i, obj_pc_i))


# reorg dialog
def reorg_dialog(json_dct):

    data = {}
    if JSN_KEY_MSGS not in json_dct.keys():
        return data

    json_dlg = json_dct[JSN_KEY_MSGS]
    if len(json_dlg) == 0:
        return data

    data[MAP_KEY_CHNL] = json_dlg[0][JSN_KEY_MSSG][JSN_KEY_CHNL]
    data[MAP_KEY_SKLL] = json_dlg[0][JSN_KEY_MSSG][JSN_KEY_SKLL]
    data[MAP_KEY_DLID] = json_dlg[0][JSN_KEY_MSSG][JSN_KEY_DLID]

    msgs = []
    for item in json_dlg:
        msg = dict()
        msg[MAP_KEY_UUID] = item[JSN_KEY_MSSG][JSN_KEY_UUID]
        msg[MAP_KEY_ISID] = item[JSN_KEY_MSSG][JSN_KEY_ISID]
        msg[MAP_KEY_CDID] = item[JSN_KEY_CDID]
        msg[MAP_KEY_ITID] = item[JSN_KEY_ITID]
        msg[MAP_KEY_NTRN] = item[JSN_KEY_MSSG][JSN_KEY_NTRN]
        msg[MAP_KEY_SDTP] = item[JSN_KEY_MSSG][JSN_KEY_SDTP]
        msg[MAP_KEY_SPID] = item[JSN_KEY_MSSG][JSN_KEY_SPID]
        msg[MAP_KEY_MGTP] = item[JSN_KEY_MSSG][JSN_KEY_NTRN]
        msg[MAP_KEY_MGTM] = item[JSN_KEY_MSSG][JSN_KEY_NTRN]
        msg[MAP_KEY_CTNT] = item[JSN_KEY_MSSG][JSN_KEY_CTNT]
        msg[MAP_KEY_CTNS] = item[JSN_KEY_MSSG][JSN_KEY_CTNP][JSN_KEY_CTNS]

        entities = []
        for e in item[JSN_KEY_MSSG][JSN_KEY_CTNP][JSN_KEY_ENTS]:
            entity = dict()
            entity[MAP_KEY_ETFM] = e[JSN_KEY_ETFM]
            entity[MAP_KEY_ETTO] = e[JSN_KEY_ETTO]
            entity[MAP_KEY_ETTP] = e[JSN_KEY_ETTP]
            entities.append(entity)

        msg[MAP_KEY_ENTS] = entities

        msgs.append(msg)

    data[MAP_KEY_MSGS] = msgs
    return data


if __name__ == '__main__':
    main()