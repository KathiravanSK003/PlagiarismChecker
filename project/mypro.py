from flask import Flask, request, render_template
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
student_notes = [open(_file, encoding='utf-8').read()
                 for _file in student_files]


def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


vectors = vectorize(student_notes)
s_vectors = list(zip(student_files, vectors))
plagiarism_results = set()


app = Flask(__name__,template_folder='template')

@app.route('/')
def gfg():
    return render_template("ht.html")
@app.route('/file_info',methods =["GET","POST"])
def check_plagiarism():
    global s_vectors
    che = []
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            filee = request.form.get("filename")
            if student_b == filee:
                sim_score = similarity(text_vector_a,text_vector_b)[0][1]
                if sim_score != 0:
                    student_pair = sorted((student_a, student_b))
                    if student_pair[0] == filee:
                        score = [student_pair[1],int(sim_score*100)]
                        che.append(score)
                    elif student_pair[1] == filee:
                        score = [student_pair[0],int(sim_score*100)]
                        che.append(score)
    return render_template("fd.html",che=che,filee=filee)
if __name__=='__main__':
   app.run(debug=True)
