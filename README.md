Readme
===

# List Indices

```
GET /_cat/indices?v
```

# Create Index

## Create Dialog Index


```
PUT dialog_<skill>_<dataset>
{
    "mappings": {
        "dialog": {
            "properties": {
                "channel": {"type": "keyword"},
                "skill": {"type": "keyword"},
                "dialog_id": {"type": "keyword"},
                "messages": {
                    "properties": {
                        "uuid": {"type": "keyword", "index": false},
                        "inst_id": {"type": "keyword", "index": false},
                        "content_digest_id":{"type": "keyword", "index": false},
                        "intention_id":{"type": "keyword", "index": false},
                        "speaker_id": {"type": "keyword"},
                        "nth_turn": {"type": "long"},
                        "sender_type": {"type": "keyword"},
                        "message_type": {"type": "keyword"},
                        "message_time": {"type": "keyword"},
                        "content": {"type": "text"},
                        "seg_content": {"type": "text", "index": false},
                        "entities": {
                            "properties": {
                                "entity_from_idx": {"type": "long", "index": false},
                                "entity_to_idx": {"type": "long", "index": false},
                                "entity_type": {"type": "keyword", "index": false}
                            }
                        }
                    }
                }
            }
        }
    }
}
```
## Create QA-pair Index

```
PUT qa_<skill>_<dataset>
{
    "mappings": {
        "qapair": {
            "properties": {
                "channel": {"type": "keyword"},
                "skill": {"type": "keyword"},
                "dialog_id": {"type": "keyword"},
                "question": {
                    "properties": {
                        "uuid": {"type": "keyword", "index": false},
                        "inst_id": {"type": "keyword", "index": false},
                        "content_digest_id":{"type": "keyword", "index": false},
                        "intention_id":{"type": "keyword", "index": false},
                        "speaker_id": {"type": "keyword"},
                        "nth_turn": {"type": "long"},
                        "sender_type": {"type": "keyword"},
                        "message_type": {"type": "keyword"},
                        "message_time": {"type": "keyword"},
                        "content": {"type": "text"},
                        "seg_content": {"type": "text", "index": false},
                        "entities": {
                            "properties": {
                                "entity_from_idx": {"type": "long", "index": false},
                                "entity_to_idx": {"type": "long", "index": false},
                                "entity_type": {"type": "keyword", "index": false}
                            }
                        }
                    }
                },
                "answer": {
                    "properties": {
                        "uuid": {"type": "keyword", "index": false},
                        "inst_id": {"type": "keyword", "index": false},
                        "content_digest_id":{"type": "keyword", "index": false},
                        "intention_id":{"type": "keyword", "index": false},
                        "speaker_id": {"type": "keyword", "index": false},
                        "nth_turn": {"type": "long"},
                        "sender_type": {"type": "keyword"},
                        "message_type": {"type": "keyword"},
                        "message_time": {"type": "keyword"},
                        "content": {"type": "text"},
                        "seg_content": {"type": "text", "index": false},
                        "entities": {
                        	"index": false,
                            "properties": {
                                "entity_from_idx": {"type": "long", "index": false},
                                "entity_to_idx": {"type": "long", "index": false},
                                "entity_type": {"type": "keyword", "index": false}
                            }
                        }
                    }
                }
            }
        }
    }
}
```



## Query

All

```
GET /<index_name>/_search
{
    "query": {
            "match_all": {}
    }
}
```

Specific Field (Dialog)

```
GET /<index_name>/_search
{
    "query": {
      "match": {
        "messages.content":"您好"
      }
    }
}
```

