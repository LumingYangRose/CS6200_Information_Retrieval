from flask import *
import searchModelWebPartII,re

app = Flask(__name__)

@app.route('/')
def upload():
    return render_template("search.html")

@app.route('/success',methods=['POST'])
def top_k():
    global query
    if request.method == 'POST':
        query = request.form['text'].lower()
        # query_main = searchModelWebPartII.abbreviations(query)
        top_k_results = searchModelWebPartII.retieve_top_convos(query)

        for key,val in top_k_results.items():
            temp = []
            for i in top_k_results[key]:
                i = i.replace("<mark>","")
                i = i.replace("</mark>","")
                temp.append(i)
            top_k_results[key] = temp

    return render_template("output.html", name = top_k_results, q = query)




if __name__ == '__main__':
    app.run(debug = True)