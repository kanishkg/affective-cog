import os
import csv
import argparse
import random

from domain_var import *

DATA_DIR = '../../data'



DOMAIN_LIST = ['goal_control', 'safety_expected']


EMOTION_QUESTION = "How does {name} feel?"
EMOTION_SENTENCE_OUTCOME = "{name} feels {emotion}."
EMOTION_SENTENCE_APP = "{name} feels {emotion}."
IMAGE_NAMES = {
    "joyful": "joyful.png",
    "frustrated": "frustrated.png",
    "grateful": "grateful.png",
    "disappointed": "disappointed.png",
    "relieved": "relieved.png",
    "resigned": "resigned.png",
    "surprised": "surprised.png",
    "devastated": "devastated.png"
}
AGENT_NAMES = ["Annie", "Glenda", "Chanda", "Hana", "Oskar"]

parser = argparse.ArgumentParser()
parser.add_argument('-e','--experiment', type=str, default='1', help='experiment number, 1: text 2: expression 3: ambiguous')

def get_completions(domain):
    CSV_NAME = os.path.join(DATA_DIR, f'{domain}.csv')
    with open(CSV_NAME, "r") as f:
        reader = csv.reader(f, delimiter=";")
        completions = list(reader)
    return completions

def write_to_csv(data, path, domain, experiment):
    CONDITION_DIR = os.path.join(DATA_DIR, f'conditions_{experiment}', domain)
    if not os.path.exists(os.path.join(CONDITION_DIR, path)):
        os.makedirs(os.path.join(CONDITION_DIR, path))
    csv_file = os.path.join(CONDITION_DIR, path, f'stories.csv')
    with open(csv_file, "a") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(data)
    
def generate_conditions(completions, domain, experiment):
    # TODO change based on domain
    if domain == 'goal_control':
        DOMAIN = 'goal_control'
        list_var = goal_control_list_var
        EMOTIONS = goal_control_emotions
        VARIABLE = ['emotion', 'outcome', 'belief_a', 'belief_b']

    elif domain == 'safety_expected':
        DOMAIN = 'safety_expected'
        list_var = safety_expected_list_var
        EMOTIONS = safety_expected_emotions
        VARIABLE = ['emotion', 'outcome', 'belief_a', 'belief_b']

    for completion_idx, completion in enumerate(completions):
        dict_var = {k:v for k,v in zip(list_var, completion)}
        context = dict_var['Context'] # context (constant)
        name = context.split(' ')[0]
        name = name.replace(',', '')
        emotion_question = EMOTION_QUESTION.format(name=name)

        if domain == 'goal_control':
            belief_a = [dict_var['Control Belief'], dict_var['Lack of Control Belief']]
            belief_b = [dict_var['Goal Belief 1'], dict_var['Goal Belief 2']]
            belief_question_a = dict_var['Belief question a']
            belief_a_answers = [dict_var['Belief answer 1a'], dict_var['Belief answer 2a']]
            belief_question_b = dict_var['Belief question b']
            belief_b_answers = [dict_var['Belief answer 1b'], dict_var['Belief answer 2b']]
            action = dict_var['Action']
            outcome_goal = [dict_var['Outcome Goal 1'], dict_var['Outcome Goal 2']]
            outcome_question = dict_var['Outcome question']
            outcome_answers = [dict_var['Outcome answer 1'], dict_var['Outcome answer 2']]
        elif domain == 'safety_expected':
            belief_a = [dict_var['Expectedness'], dict_var['Unexpectedness']]
            belief_b = [dict_var['Safety Belief 1'], dict_var['Safety Belief 2']]
            belief_question_a = dict_var['Belief question a']
            belief_a_answers = [dict_var['Belief answer 1a'], dict_var['Belief answer 2a']]
            belief_question_b = dict_var['Belief question b']
            # hack to correct wrong generation
            belief_b_answers = [dict_var['Belief answer 1b'], dict_var['Belief answer 2b']]
            action = dict_var['Action']
            outcome_goal = [dict_var['Outcome 1'], dict_var['Outcome 2']]
            outcome_question = dict_var['Outcome question']
            outcome_answers = [dict_var['Outcome answer 1'], dict_var['Outcome answer 2']]
        
        agent = AGENT_NAMES[completion_idx % len(AGENT_NAMES)]
        # 4 variables x 2 appraisals x 2 values x 2 outcomes
        for variable in VARIABLE:
            image = None
            # 4 x 2 conditions
            if variable == 'emotion':
                question = emotion_question
                for e, emotion in enumerate(EMOTIONS):
                    correct_answer = emotion
                    image = agent+'/'+IMAGE_NAMES[emotion]
                    wrong_answers = [e for e in EMOTIONS if e != emotion]
                    if e == 0:
                        story_1 = f"{context} {belief_a[0]} {belief_b[0]} {action} {outcome_goal[0]}"
                        story_2 = f"{context} {belief_a[0]} {belief_b[1]} {action} {outcome_goal[1]}"
                    elif e == 1:
                        story_1 = f"{context} {belief_a[0]} {belief_b[0]} {action} {outcome_goal[1]}"
                        story_2 = f"{context} {belief_a[0]} {belief_b[1]} {action} {outcome_goal[0]}"
                    elif e == 2:
                        story_1 = f"{context} {belief_a[1]} {belief_b[0]} {action} {outcome_goal[0]}"
                        story_2 = f"{context} {belief_a[1]} {belief_b[1]} {action} {outcome_goal[1]}"
                    elif e == 3:
                        story_1 = f"{context} {belief_a[1]} {belief_b[0]} {action} {outcome_goal[1]}"
                        story_2 = f"{context} {belief_a[1]} {belief_b[1]} {action} {outcome_goal[0]}"
                    if experiment == '1':
                        write_to_csv([story_1, question, correct_answer, *wrong_answers], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, question, correct_answer, *wrong_answers], f'{variable}_{emotion}_1', domain, experiment)
                    else:
                        write_to_csv([story_1, image, question, correct_answer, *wrong_answers], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, image, question, correct_answer, *wrong_answers], f'{variable}_{emotion}_1', domain, experiment)
            # 4x2 conditions
            elif variable == 'outcome':
                for e, emotion in enumerate(EMOTIONS):
                    if experiment == '1':
                        emotion_sentence = EMOTION_SENTENCE_OUTCOME.format(name=name, emotion=emotion)
                    else:
                        emotion_sentence = ""
                    image = agent+'/'+IMAGE_NAMES[emotion]
                    question = f"{emotion_sentence} {outcome_question}"
                    if e == 0:
                        story_1 = f"{context} {belief_a[0]} {belief_b[0]} {action}"
                        story_2 = f"{context} {belief_a[0]} {belief_b[1]} {action}"
                        correct_answer_1 = outcome_answers[0]
                        correct_answer_2 = outcome_answers[1]
                    elif e == 1:
                        story_1 = f"{context} {belief_a[0]} {belief_b[0]} {action}"
                        story_2 = f"{context} {belief_a[0]} {belief_b[1]} {action}"
                        correct_answer_1 = outcome_answers[1]
                        correct_answer_2 = outcome_answers[0]
                    elif e == 2:
                        story_1 = f"{context} {belief_a[1]} {belief_b[0]} {action}"
                        story_2 = f"{context} {belief_a[1]} {belief_b[1]} {action}"
                        correct_answer_1 = outcome_answers[0]
                        correct_answer_2 = outcome_answers[1]
                    elif e == 3:
                        story_1 = f"{context} {belief_a[1]} {belief_b[0]} {action}"
                        story_2 = f"{context} {belief_a[1]} {belief_b[1]} {action}"
                        correct_answer_1 = outcome_answers[1]
                        correct_answer_2 = outcome_answers[0]
                    wrong_answers_1 = [e for e in outcome_answers if e != correct_answer_1]
                    wrong_answers_2 = [e for e in outcome_answers if e != correct_answer_2]
                    if experiment == '1':
                        write_to_csv([story_1, question, correct_answer_1, *wrong_answers_1], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, question, correct_answer_2, *wrong_answers_2], f'{variable}_{emotion}_1', domain, experiment)
                    else:
                        write_to_csv([story_1, image, question, correct_answer_1, *wrong_answers_1], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, image, question, correct_answer_2, *wrong_answers_2], f'{variable}_{emotion}_1', domain, experiment)
 
            # 4x2 conditions
            elif variable == 'belief_a':
                for e, emotion in enumerate(EMOTIONS):
                    image = agent+'/'+IMAGE_NAMES[emotion]
                    if experiment == '1':
                        emotion_sentence = EMOTION_SENTENCE_APP.format(name=name, emotion=emotion)
                    else:
                        emotion_sentence = ""
                    question = f"{emotion_sentence} {belief_question_a}"
                    wrong_answers_1 = [e for e in belief_a_answers if e != belief_a_answers[0]]
                    wrong_answers_2 = [e for e in belief_a_answers if e != belief_a_answers[1]]
                    if e == 0:
                        story_1 = f"{context} {belief_b[0]} {action} {outcome_goal[0]}"
                        story_2 = f"{context} {belief_b[1]} {action} {outcome_goal[1]}"
                        correct_answer_1 = belief_a_answers[0]
                        correct_answer_2 = belief_a_answers[0]
                    elif e == 1:
                        story_1 = f"{context} {belief_b[0]} {action} {outcome_goal[1]}"
                        story_2 = f"{context} {belief_b[1]} {action} {outcome_goal[0]}"
                        correct_answer_1 = belief_a_answers[0]
                        correct_answer_2 = belief_a_answers[0]

                    elif e == 2:
                        story_1 = f"{context} {belief_b[0]} {action} {outcome_goal[0]}"
                        story_2 = f"{context} {belief_b[1]} {action} {outcome_goal[1]}"
                        correct_answer_1 = belief_a_answers[1]
                        correct_answer_2 = belief_a_answers[1]
                    elif e == 3:
                        story_1 = f"{context} {belief_b[0]} {action} {outcome_goal[1]}"
                        story_2 = f"{context} {belief_b[1]} {action} {outcome_goal[0]}"
                        correct_answer_1 = belief_a_answers[1]
                        correct_answer_2 = belief_a_answers[1]
                    wrong_answers_1 = [e for e in belief_a_answers if e != correct_answer_1]
                    wrong_answers_2 = [e for e in belief_a_answers if e != correct_answer_2]
                    if experiment == '1':
                        write_to_csv([story_1, question, correct_answer_1, *wrong_answers_1], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, question, correct_answer_2, *wrong_answers_2], f'{variable}_{emotion}_1', domain, experiment)
                    else:
                        write_to_csv([story_1, image, question, correct_answer_1, *wrong_answers_1], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, image, question, correct_answer_2, *wrong_answers_2], f'{variable}_{emotion}_1', domain, experiment)
            # 4x2 conditions
            elif variable == 'belief_b':
                for e, emotion in enumerate(EMOTIONS):
                    if experiment == '1':
                        emotion_sentence = EMOTION_SENTENCE_APP.format(name=name, emotion=emotion)
                    else:
                        emotion_sentence = ""
                    image = agent+'/'+IMAGE_NAMES[emotion]
                    question = f"{emotion_sentence} {belief_question_b}"
                    correct_answer_1 = belief_b_answers[0]
                    correct_answer_2 = belief_b_answers[1]
                    wrong_answers_1 = [e for e in belief_b_answers if e != belief_b_answers[0]]
                    wrong_answers_2 = [e for e in belief_b_answers if e != belief_b_answers[1]]
                    if e == 0:
                        story_1 = f"{context} {belief_a[0]} {action} {outcome_goal[0]}"
                        story_2 = f"{context} {belief_a[0]} {action} {outcome_goal[1]}"
                    elif e == 1:
                        story_1 = f"{context} {belief_a[0]} {action} {outcome_goal[1]}"
                        story_2 = f"{context} {belief_a[0]} {action} {outcome_goal[0]}"
                    elif e == 2:
                        story_1 = f"{context} {belief_a[1]} {action} {outcome_goal[0]}"
                        story_2 = f"{context} {belief_a[1]} {action} {outcome_goal[1]}"
                    elif e == 3:
                        story_1 = f"{context} {belief_a[1]} {action} {outcome_goal[1]}"
                        story_2 = f"{context} {belief_a[1]} {action} {outcome_goal[0]}"
                    if experiment == '1':
                        write_to_csv([story_1, question, correct_answer_1, *wrong_answers_1], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, question, correct_answer_2, *wrong_answers_2], f'{variable}_{emotion}_1', domain, experiment) 
                    else:
                        write_to_csv([story_1, image, question, correct_answer_1, *wrong_answers_1], f'{variable}_{emotion}_0', domain, experiment)
                        write_to_csv([story_2, image, question, correct_answer_2, *wrong_answers_2], f'{variable}_{emotion}_1', domain, experiment)

if __name__ == "__main__":  
    random.seed(42)
    args = parser.parse_args()
    if args.experiment not in ['1', '2', '3']:
        raise ValueError("Experiment number must be 1, 2, or 3")
    # delete condition files
    for domain in DOMAIN_LIST:
        completions = get_completions(domain)
        generate_conditions(completions, domain, args.experiment)
