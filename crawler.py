import requests
from bs4 import BeautifulSoup as bs
import re,pickle


'''
This class crawls required movie script information from a website and stores it into a pickle file 
to be used later.
'''
class Crawler(object):

    """
    Crawls a website that holds movie scripts. It curls through every link alphabetically
    in the website and it crawls each and every movie under every alphabet. A list of all these links
    is returned here.
    """
    def crawl_lyric_links(self):
        links = []
        artists = []
        # alphabet = ['0']
        alphabet = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        print("Fetching all lyric links...")
        count = 0
        for letter in alphabet:
            
            main_url = "https://www.lyrics.com/artists/" + letter + "/99999"
            try:
                requestSource = requests.get(main_url) # or "html.parser"
            except:
                print ("Failed to establish connection. Check your internet.")
            beautifiedSource = bs(requestSource.content, "html.parser")

            td_tag = beautifiedSource.findAll("td", {"class": "tal qx"})
            
            for i in list(td_tag):
                # print(i)
                if i.a:
                    try:
                        requestSource = requests.get("https://www.lyrics.com/" + i.a["href"])
                    except:
                        print ("Failed to establish connection. Check your internet.")
                    beautifiedSource = bs(requestSource.content, "html.parser")

                    td_tag = beautifiedSource.findAll("td", {"class": "tal qx"})

                    for i in list(td_tag):
                        if i.a:
                            print("add link no.", count)
                            count += 1
                            links.append("https://www.lyrics.com" + i.a["href"])
                        # if len(links) > 20000:
                        #     break
                    
                if len(links) > 20000:
                    break

            print("Got " + letter)

        pickle_out = open("links_dataset.pickle","wb")
        pickle.dump(links, pickle_out)
        pickle_out.close()

        return links

    """
    Each link that was returned as a total list will be parsed here. A dictionary containing the 
    movie title and the script of the first scene of each movie is stored. The script is further
    processed to remove unnecessary punctuation and it converted to lower case to better search 
    results.
    """
    def crawl_lyrics(self): #multiple dictionaries with one sentence and movie title EACH
        lyric_list = []
        pickle_in = open("links_dataset.pickle","rb")
        links = pickle.load(pickle_in)
        print(len(links))
        # text_file = open("OutputMovies1.txt", "a")
        print("Crawling all links...stay tuned.")
        count = 0
        for link in links:
            print("crawling link no.", count)
            count += 1
            if count > 20000:
                break
            # count -= 1
            # if count < 0:
            #     break           
            # print(link)
            requestSource = requests.get(link)

            if requestSource.status_code == 200:

                beautifiedSource = bs(requestSource.content, "html.parser")

                try:
                    h1_tag = beautifiedSource.find("h1", {"id": "lyric-title-text"})
                    title = h1_tag.text
                    # print(title)
                except:
                    title = "Unknown"
                
                try:
                    pre_tag = beautifiedSource.find("pre", {"id": "lyric-body-text"})
                    lyrics = pre_tag.text
                    # print("lyrics" + lyrics)
                except:
                    lyrics = "Unknown"

                # lyrics = lyrics.replace('\r', ' ')
                lyrics = lyrics.replace('\n', ' ')
                lyrics = re.sub("[^\w\d'\s]+",'',lyrics).lower()
                song = {"title":title, "lyrics":''}
   
                if lyrics != '':
                    song["lyrics"] = lyrics.strip(' ')
                else:
                    continue
                lyric_list.append(song)
                # print(song)
                # text_file.write(json.dumps(movie,indent=3, sort_keys=True))

            else:
                continue

        pickle_out = open("lyric_dataset_new.pickle","wb")
        pickle.dump(lyric_list, pickle_out)
        pickle_out.close()

        return None



x = Crawler()
# x.crawl_lyric_links()
x.crawl_lyrics()
# print(x.crawl_dialogues())
# print(x.find_synonyms())