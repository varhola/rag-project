from dataset import create_dataset, DATASET
from evaluator import read_answers, debug_retrieval, debug_questions, combined_evaluation

create_dataset()

questions = read_answers("./query_set.csv")

# debug_retrieval(questions)
#debug_questions(questions)
combined_evaluation(questions)