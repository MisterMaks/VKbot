from true_project import *
import warnings

warnings.filterwarnings('ignore')
'''
while True:
    print("Введите вопрос: ")
    question = input()
    if question == "exit":
        break'''
answer = good_answer('президент', df_stack_questions, df_stack_answers, df_quest_ans_mail_ans)
print(answer)
answer = good_answer('бинарное дерево', df_stack_questions, df_stack_answers, df_quest_ans_mail_ans)
print(answer)
answer = good_answer("вывав", df_stack_questions, df_stack_answers, df_quest_ans_mail_ans)
print(answer)

