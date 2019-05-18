from test_1 import *
import pandas as pd

#df_stack_questions = pd.read_csv('stack_questions.csv')
#df_stack_answers = pd.read_csv('stack_answers.csv')
#df_quest_ans_mail_ans = pd.read_csv('quest_ans_from_mail.csv')


def good_answer(zapros,
                df_stack_questions,
                df_stack_answers,
                df_quest_ans_mail_ans):
    ans = []
    size = 100
    classif_model_2 = joblib.load('logreg_for_prog_2.sav')
    with open("w2v_2_for_prog.pkl", 'rb') as f:
        classif_w2v_2 = pickle.load(f)
    with open("dict_tfidf_for_prog.pkl", 'rb') as f:
        d_prog = pickle.load(f)

    good_class = pred_zapros_2(classif_model_2, zapros, size, classif_w2v_2, d_prog)
    if good_class == -1:
        return "Шо то я такой не понял"
    ans.append(good_class)

    if good_class == 1:

        stack_VEC_SIZE_EMB = 300
        stack_index_title_emb_2 = AnnoyIndex(stack_VEC_SIZE_EMB)
        stack_index_title_emb_2.load('annoy_for_stack.ann')
        with open("map_id_for_stack.pkl", 'rb') as f:
            stack_map_id_2_prod_hash = pickle.load(f)
        with open("w2v_2_for_stack.pkl", 'rb') as f:
            stack_w2v_2 = pickle.load(f)
        with open("tfidf_for_annoy_for_stack.pkl", 'rb') as f:
            d_stack = pickle.load(f)

        stack_zapros_vec_2 = vectorize_one_2(zapros, 300, stack_w2v_2, d_stack)
        stack_annoy_res_2 = list(stack_index_title_emb_2
                                 .get_nns_by_vector(stack_zapros_vec_2.T, 1, include_distances=True))
        ans = answer_for_stack(stack_annoy_res_2,
                                    stack_map_id_2_prod_hash,
                                    df_stack_questions,
                                    df_stack_answers)

    elif good_class == 0:

        mail_VEC_SIZE_EMB = 100
        mail_index_title_emb_2 = AnnoyIndex(mail_VEC_SIZE_EMB)
        mail_index_title_emb_2.load('annoy_for_mail.ann')
        with open("map_id_for_mail.pkl", 'rb') as f:
            mail_map_id_2_prod_hash = pickle.load(f)
        with open("w2v_2_mail.pkl", 'rb') as f:
            mail_w2v_2 = pickle.load(f)
        with open("mail_tfidf.pkl", 'rb') as f:
            d_mail = pickle.load(f)

        mail_zapros_vec_2 = vectorize_one_2(zapros, 100, mail_w2v_2, d_mail)
        mail_annoy_res_2 = list(mail_index_title_emb_2
                                .get_nns_by_vector(mail_zapros_vec_2.T, 10, include_distances=True))

        ans = answer_for_mail(mail_annoy_res_2,
                                   mail_map_id_2_prod_hash,
                                   df_quest_ans_mail_ans)

    return ans


# print(good_answer("Сортировка пузырьком", df_stack_questions, df_stack_answers, df_quest_ans_mail_ans))
