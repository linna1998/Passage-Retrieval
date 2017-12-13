import jieba
import math
import re
import numpy as np
from numpy import linalg
from itertools import chain
from gensim import corpora, models, similarities
from collections import defaultdict

stopwords = None

def Initialization():
    analyse.set_stop_words("question_stopword.txt")
    jieba.initialize()
    with open("stopword.txt") as f:
        global stopwords 
        stopwords = {}.fromkeys([l.strip() for l in f])

def SplitSentence(docs): 
    r = re.compile(r'[.?!¡££¿£¡]')
    return list(chain(*[r.split(doc) for doc in docs]))

def sentence_similarity(question, sentences, key_sentences): 
    frequency = defaultdict(int)
    text = sentences + [question]
    text_cutted = [[word for word in jieba.cut_for_search(s) if word not in stopwords] for s in text]
    for s in text_cutted:
        for word in s:
            frequency[word] += 1 
    text_cutted = [[word for word in sentence if frequency[word] > 1] for sentence in text_cutted]
    dictionary = corpora.Dictionary(text_cutted)
    corpus_simple = [dictionary.doc2bow(s) for s in text_cutted]
    tfidf_model = models.TfidfModel(corpus_simple)
    corpus = tfidf_model[corpus_simple]
    matrix_similarity = similarities.MatrixSimilarity(corpus)
    def sentence2vec(sentence):
        sentence = [word for word in jieba.cut_for_search(sentence) if word not in stopwords]
        return tfidf_model[dictionary.doc2bow(sentence)]
    A = np.array([matrix_similarity[sentence2vec(s)] for s in key_sentences])
    B = np.array([matrix_similarity[sentence2vec(question)]]).T
    num = np.dot(A, B)
    denom = (linalg.norm(A, axis=1) * linalg.norm(B)).reshape((-1,1))
    cos = num / denom 
    sim = 0.5 + 0.5 * cos 
    return sim.reshape(-1,)

def SelectSentence(question, sentences, keywords, lim=15):
    key_sentences_index = []
    key_sentences = [] 
    for i, s in enumerate(sentences):
        for key in keywords:
            if key in s:            
                key_sentences_index.append(i) 
                key_sentences.append(s)
                break
    score = sentence_similarity(question, sentences, key_sentences).tolist()    
    score_sentences = sorted(zip(score, key_sentences_index), key=lambda x : float('-inf') if math.isnan(x[0]) else x[0], reverse=True)
    selected_score = [i for sc, i in score_sentences[:lim]]
    selected = [False] * len(sentences)
    for i in selected_score:
        if i > 0:
            selected[i - 1] = True
        selected[i] = True
        if i + 1 < len(selected):
            selected[i + 1] = True
    ranges = []
    i = 0
    while i < len(selected):
        if selected[i]:
            start = i
            while i < len(selected) and selected[i]:
                i += 1
                end = i
            ranges.append((start, end))
        i += 1
    paragraphs = ["¡£".join(sentences[start:end]) for start, end in ranges]    
    return paragraphs