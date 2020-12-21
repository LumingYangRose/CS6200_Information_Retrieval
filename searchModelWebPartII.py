from elasticsearch import Elasticsearch
import pickle,heapq

"""
Methods mentioned below are used for the Flask application.
"""
es = Elasticsearch()
global res

"""
Uses the pickle object containing the dictionary of movie titles and their scripts, to insert into
a new Elasticsearch index, one record at a time. The resulting index is returned.
"""
def create_index():
    res = None
    pickle_in = open("lyric_dataset.pickle","rb")
    lyrics = pickle.load(pickle_in)

    count = 1

    if es.indices.exists(index="song_lyrics"):
        return res

    print(len(lyrics))
    for lyric in lyrics:
        res = es.index(index="song_lyrics", id=count, body=lyric)
        count += 1

    print("Finished indexing")
    es.indices.refresh(index="song_lyrics")

    return res



"""
The user's search query is processed and a match phrase process is conducted using the ES search API.
Highlighting, also a part of the ES API, is performed as well on the words directly matching the
search query. A dictionary with the song titles and their scores as well as a dictionary with the
resulting movie titles and their highlighted scripts are returned.
"""
def search_query(user_query):
    create_index()
    res = es.search(index="song_lyrics",
                    size = 50, body={"query":{
            "match_phrase":{
                "lyrics":user_query
            }
        },
            "highlight":{
                "type":"unified",
                "fragment_size":100,
                "fields":{
                    "lyrics":{ "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] }
                }
            }
        })
    #print(res)
    scores = {}
    convo = {}
    for hit in res['hits']['hits']:
        convo[hit["_source"]["title"]] = hit["highlight"]["lyrics"]
        #scores[hit["_source"]["title"]] = hit["_score"]
        scores[hit["_score"]] = hit["_source"]["title"]
        # print(hit["_source"]["title"])
        # print(hit["highlight"]["script"])
        # print(hit["_score"])

    return scores,convo


def retieve_top_convos(user_query):
    #lucene practical score based heap-top 10 results
    scores,convo = search_query(user_query)
    heap = [(-key, value) for key,value in scores.items()]
    largest = heapq.nsmallest(10, heap)
    largest = [key for value, key in largest]
    result = {}
    for i in largest:
        convo[i] = [" ".join(convo[i])]
        result[i] = convo[i]

    return result



"""
Deletes the index.
"""
def delete_index():
    es.indices.delete(index='song_lyrics')
    print("Existing index, 'song_lyrics' has been deleted. Index again.")
    # search_query()

# delete_index()
create_index()
# # search_query()
# retieve_top_convos("awful")