from dataset import create_dataset
from evaluator import read_answers, debug_retrieval, debug_questions, combined_evaluation, gemini_comparison

create_dataset()

questions = read_answers("./query_set.csv")

# debug_retrieval(questions)
# debug_questions(questions)
# combined_evaluation(questions)

gemini_comparison("./Gemini_1.5_Flash_model_responses.json")