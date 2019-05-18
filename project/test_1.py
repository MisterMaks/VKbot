import re
from functools import lru_cache
import pymorphy2
import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from gensim.models.word2vec import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from gensim.models.word2vec import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import itertools

MORPH = pymorphy2.MorphAnalyzer()

df_stack_questions = pd.read_csv('stack_questions.csv')
df_stack_answers = pd.read_csv('stack_answers.csv')
df_quest_ans_mail_ans = pd.read_csv('quest_ans_from_mail.csv')


@lru_cache(maxsize=100000)
def get_normal_form(i):
    return MORPH.normal_forms(i)[0]


def normalize_text(text):
    text = text[:500]
    normalized = [get_normal_form(word) for word in re.findall('[a-zA-Zа-яА-Я]{3,}', text)]  # [a-zA-Zа-яА-Я]{3,}|\d+
    return ' '.join([word for word in normalized if word not in []])


stop_words = [get_normal_form(i) for i in []]  # стоп-слова


def normalization_vectorization_2(phrases, size, filename_vec, filename_d):
    norm_phrases = phrases.apply(normalize_text)
    sentences = norm_phrases.str.split()

    model = Word2Vec(sentences, size=size, workers=2, iter=3)  # последние два
    #    filename2 = name_vect
    joblib.dump(model, filename_vec)

    w2v = dict(zip(model.wv.index2word, model.wv.syn0))  # словарь из слов

    #    embed_matrix = []
    #    for i in w2v:
    #        embed_matrix.append(w2v[i])
    #    embed_matrix = np.vstack(embed_matrix)

    data_storage = list(norm_phrases.values)

    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(data_storage)
    idf = tfidf.idf_
    d = dict(zip(tfidf.get_feature_names(), idf))

    with open(filename_d, 'wb') as f:
        pickle.dump(d, f)

    data_storage_norm = {}  # хранит вектора для фраз
    for i in range(len(data_storage)):
        vec = np.zeros(size)
        for word in data_storage[i].split(' '):
            if word in model and word in d:
                vec += model[word] * d[word]
        vec /= len(data_storage[i].split(' '))
        data_storage_norm[i] = vec

    lst = []
    for v in data_storage_norm.values():
        lst.append(v)
    q = np.array(lst)

    return [data_storage, data_storage_norm, q]


def fit_2(phrases, target_values, size, filename_class, filename_vec, filename_d):  # принимает  столбец фраз и таргетов

    q = normalization_vectorization_2(phrases, size, filename_vec, filename_d)[2]

    clf = LogisticRegression()
    clf.fit(q, target_values)

    #    filename1 = name_classif
    joblib.dump(clf, filename_class)
    return None


def vectorize_one_2(zapros, size, w2v, d):
    zapros = normalize_text(zapros)
    seq = np.zeros(size)
    for word in zapros.split():
        if word in w2v and word in d:
            seq += w2v[word] * d[word]
    seq /= len(zapros.split())
    return seq.reshape(1, -1)


def pred_zapros_2(classif_model, zapros, size, w2v, d):
    vect_zapros = vectorize_one_2(zapros, size, w2v, d)
    if np.array_equal(vect_zapros, np.zeros(size).reshape(1, -1)):
        return -1
    y_hat = classif_model.predict(vectorize_one_2(zapros, size, w2v, d))
    return y_hat[0]


def vectorize_for_annoy_2(id_data, phrases_data, size, filename_vec, d):
    data_storage_vec = normalization_vectorization_2(phrases_data, size, filename_vec, d)[2]
    data_storage_norm = {}
    for i in range(len(data_storage_vec)):
        key = id_data[i]
        data_storage_norm[key] = data_storage_vec[i]
    # data_storage_norm[key] = [df_stack_questions["titles"][i], data_storage_vec[i]]
    return data_storage_norm


def build_annoy(data_storage_norm, NUM_TREES, VEC_SIZE_EMB):
    # NUM_TREES = 7
    # VEC_SIZE_EMB = 100
    # VEC_SIZE_EMB = 300

    counter = 0
    map_id_2_prod_hash = {}
    index_title_emb = AnnoyIndex(VEC_SIZE_EMB)

    print("Build annoy base")
    for prod_hash in data_storage_norm:
        title_vec = data_storage_norm[prod_hash]  # Вытаскиваем вектор

        index_title_emb.add_item(counter, title_vec)  # Кладем в анной

        map_id_2_prod_hash[counter] = prod_hash  # сохраняем мапу - (id в анное -> продукт_id)

        counter += 1
        if counter % 10000 == 1:
            print("computed for %d" % counter)

    index_title_emb.build(NUM_TREES)

    index_title_emb.save("annoy_for_mail.ann")
    with open("map_id_for_mail.pkl", 'wb') as f:
        pickle.dump(map_id_2_prod_hash, f)

    print("builded")
    return {'index_title_emb': index_title_emb, 'map_id_2_prod_hash': map_id_2_prod_hash}


# title_id = list(data_storage_norm.keys())[np.random.randint(10000)]

# zapros = df_stack_questions[df_stack_questions["ids_questions"]==title_id]["titles"].values[0]
# annoy_res = list(index_title_emb.get_nns_by_vector(zapros_vec.T, 10, include_distances=True))

def answer_for_stack(annoy_res, map_id_2_prod_hash, df_questions, df_answers, count_quest=1, count_ans=1):
    res = []
    #    print('Запрос:', zapros)
    #    print('Векторок:', data_storage_norm[title_id][:20], '\n')
    #    print("===" * 20)
    #    print("===" * 20 + '\n')
    # annoy_res = list(index_title_emb.get_nns_by_vector(data_storage_norm[title_id], 13, include_distances=True))
    #    annoy_res = list(index_title_emb.get_nns_by_vector(zapros_vec.T, 10, include_distances=True))

    # print('\n\nСоседи:')

    for annoy_id, annoy_sim in itertools.islice(zip(*annoy_res), count_quest):
        image_id = map_id_2_prod_hash[annoy_id]
        quest = df_stack_questions[df_stack_questions["ids_questions"] == image_id]["titles"].values[0]
        #    print(ans, 1 - annoy_sim ** 2 / 2)
        # print("===" * 20)
        # print("Похожий вопрос:")
        # print(quest)
        # print("___" * 20)
        accepted_id = df_stack_questions[df_stack_questions["ids_questions"] == image_id] \
            ["ids_accepted_answer"].values[0]
        if accepted_id == -1:
            ans = df_stack_answers[df_stack_answers["ids_parent"] == image_id]["answers"]
            id_ans = df_stack_answers[df_stack_answers["ids_parent"] == image_id]["ids_answers"]
            if len(ans) > 0:
                # print("Попробуй это:\n")
                # z = 0
                # for i in id_ans.values:
                #    res = i
                #    z += 1
                #    if z == count_ans:
                #        break
                # z = 0
                for i in ans.values:
                    return i
                    # print(i)
                    # z += 1
                    # if z == count_ans:
                    #    break
                    # print("___" * 20)
            else:
                ans = "Нет ответа"
                # print("Нет ответа!!!\n")
                # res = -1
        else:
            # print("Найден правильный ответ: \n")
            ans = df_stack_answers[df_stack_answers["ids_answers"] == accepted_id]["answers"].values[0]
        # id_ans = df_stack_answers[df_stack_answers["ids_answers"] == accepted_id]["ids_answers"]
        #    res = id_ans.values[0]
        # print(ans.values[0])
        #        print("===" * 20)
        return ans


def answer_for_mail(annoy_res, map_id_2_prod_hash, df_quest_ans_mail_ans, count_quest=1, count_ans=3):
    res = []
    for annoy_id, annoy_sim in itertools.islice(zip(*annoy_res), count_quest):
        image_id = map_id_2_prod_hash[annoy_id]
        quest = df_quest_ans_mail_ans[df_quest_ans_mail_ans["id"] == image_id]["questions"].values[0]
        ans = df_quest_ans_mail_ans[df_quest_ans_mail_ans["id"] == image_id]["answers"].values[0]
        res = df_quest_ans_mail_ans[df_quest_ans_mail_ans["id"] == image_id]["id"].values[0]
        # print("===" * 20)
        # print("Похожий вопрос:")
        # print(quest, '\n')
        # print("___" * 20)
        # print("Ответ: \n")
        # print(ans)
        # print("===" * 20)
        cleanr = re.compile('<.*?>')
        ans = re.sub(cleanr, '', ans)
        return ans
