import re
from gensim.models import Word2Vec
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


final_df = pd.read_csv('./cleaned_job_role.csv', sep=';')


class W2VSimilarity():
    def __init__(self, df, id, text):
        self.init_df = df
        self.df = df
        self.id = id
        self.text = text
        self.corpus = None
        self.model = None
        self.document_embedding_list = []
        self.sim = None
        self.f = open('./stop_words.txt', 'r')

    # input text 전처리
    def remove_sp_char(self,text):
        p = re.compile("\W+")
        return p.sub(' ', text)
        

    def make_lower_case(self,text):
        return text.lower()

    def remove_stop_words(self,text):
        text = text.replace('\n', ' ')
        text = text.replace(' 분석', '분석')
        text = text.split()
        stopwords = []
        stopwords_list = self.f.read().split('\n')
        stopwords = set(stopwords_list)
        text = [w for w in text if not w in stopwords]
        text = " ".join(text)
        return text

    def cleaning(self):
        self.text = self.remove_stop_words(self.text)
        self.text = self.make_lower_case(self.text)
        self.text = self.remove_sp_char(self.text)

        self.df.loc[100, 'recruit_id'] = self.id
        self.df.loc[100, 'cleaned'] = self.text


    # 코퍼스 만들기
    def make_corpus(self):
        corpus = []
        for words in self.df['cleaned']:
            corpus.append(words.split())
        self.corpus = corpus
    
    # 모델만들기
    def create_model(self):
        word2vec_model = Word2Vec(vector_size=500, window=5, min_count=2, workers=-1)
        word2vec_model.build_vocab(self.corpus)
        word2vec_model.train(self.corpus, total_examples=word2vec_model.corpus_count, epochs=20)
        self.model = word2vec_model

    # vector값 만들기
    def vectors(self):
        doc_embedding_list = []
        for line in self.df['cleaned']:
            doc2vec = None
            count = 0
            for word in line.split():
                if word in self.model.wv.index_to_key:
                    count += 1
                    if doc2vec is None:
                        doc2vec = self.model.wv[word]
                    else:
                        doc2vec = doc2vec + self.model.wv[word]

            if doc2vec is not None:
                doc2vec = doc2vec / count
                doc_embedding_list.append(doc2vec)

        self.document_embedding_list = doc_embedding_list

    # 유사도 구하기
    def cosine_sim(self):
        
        cosine_similarities = cosine_similarity(self.document_embedding_list, self.document_embedding_list)
        
        self.sim = cosine_similarities

    # 추천하기
    def recommendations(self):
        rec = self.init_df[['recruit_id', 'job_role']]
        indices = pd.Series(self.df.index, index = self.df['recruit_id']).drop_duplicates()    
        idx = indices[self.id]

        sim_scores = list(enumerate(self.sim[idx]))
        sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
        sim_scores = sim_scores[1:14]

        book_indices = [i[0] for i in sim_scores]

        recommend = rec.iloc[book_indices].reset_index(drop=True)

        return recommend

    def get_item(self):
        self.cleaning()
        self.make_corpus()
        self.create_model()
        self.vectors()
        self.cosine_sim()
        return self.recommendations()

          