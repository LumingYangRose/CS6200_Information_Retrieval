import pickle
# pickle_in = open("links_dataset.pickle","rb")
pickle_in = open("lyric_dataset.pickle","rb")
lyrics = pickle.load(pickle_in)
count = 3
print("number of lyrics: " + str(len(lyrics)))
# for lyric in lyrics:
#     print("number of lyrics: " + str(len(lyrics)))
#     print(lyric)
    # count -= 1

    # if (count < 0):
    #     break

# import pickle
# pickle_in = open("movie_list_paras_full.pickle","rb")
# lyrics = pickle.load(pickle_in)s
# count = 3
# for lyric in lyrics:
#     print(lyric)
#     count -= 1

#     if (count < 0):
#         break
