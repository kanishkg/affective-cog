import json
import os
import numpy as np
import copy
import random

# Constants
DATA_DIR = '../../data/conditions_2'
NUM_CONDITIONS = 32
NUM_SCENARIOS = 20
PER_BATCH =  40
NUM_BATCHES = NUM_CONDITIONS * NUM_SCENARIOS // PER_BATCH
# how many times does a scenario get sampled (number of times a participant sees a scenario)
SAMPLE_FREQ = 4
# PER_BATCH = NUM_CONDITIONS * NUM_SCENARIOS // NUM_BATCHES
SEED = 103
random.seed(SEED)
np.random.seed(SEED)


# Function to read CSV
def read_csv(csv_file):
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        lines[i] = line.strip().split(';')
    return lines

# Define all conditions
appraisal_factors = ['goal_control', 'safety_expected']
inferences = ['belief_a', 'belief_b', 'outcome', 'emotion']
emotion = [['joyful', 'frustrated', 'grateful', 'disappointed'], ['relieved', 'resigned', 'surprised', 'devastated']]
scenario = ['0', '1']

# Read all the data
data = [[[]for _ in inferences] for _ in range(NUM_SCENARIOS)]
for a, af in enumerate(appraisal_factors):
    for i, inf in enumerate(inferences):
        for em in emotion[a]:
            for sc in scenario:
                condition_name = f"{af}/{inf}_{em}_{sc}"
                csv_path = os.path.join(DATA_DIR, condition_name, "stories.csv")
                try:
                    csv_data = read_csv(csv_path)
                except FileNotFoundError:
                    print(f"File {csv_path} not found.")
                    continue
                
                for s, story in enumerate(csv_data[:NUM_SCENARIOS//len(appraisal_factors)]):
                    data[len(csv_data)*a + s][i].append([story, condition_name])

print(f"Total number of scenarios: {len(data)}")
# check that all scenarios have the same number of conditions
for s in range(NUM_SCENARIOS):
    for i in range(len(inferences)):
        assert len(data[s][i]) == NUM_CONDITIONS // len(inferences), f"Scenario {s} has {len(data[s][i])} conditions for inference {i}."

for s in range(NUM_SCENARIOS):
    print(f"Scenario {s}: {len(data[s])} inferences with {len(data[s][1])} stories each.")

# we want to sample each scenario at most twice
# we want to sample inferences such that they are equal

# Initialize batches
batches = [[] for _ in range(NUM_BATCHES)]

# each scenario can be sampled at most twice
num_sampled_scenario = [0 for _ in range(NUM_SCENARIOS)]


rand_ids = [[] for _ in range(NUM_BATCHES)]

unsampled_ids = [[0 for _ in range(NUM_CONDITIONS)] for _ in range(NUM_SCENARIOS)]

for b in range(NUM_BATCHES):
    # sample stories such that each batch has at most 2 conditions per scenario
    num_sampled = [0 for _ in range(NUM_SCENARIOS)]
    num_sampled_inferences = [0 for _ in range(len(inferences))]
    while len(batches[b]) < PER_BATCH:
        # print logs
        print(f"Batch {b}: {len(batches[b])}/{PER_BATCH}, {num_sampled.count(2)}/{NUM_SCENARIOS} scenarios sampled twice")
        print(f"Number of scenarios sampled: {num_sampled_scenario}")
        print(rand_ids[b])

        # get list of scenarios that have not been sampled twice
        if len(batches[b]) < NUM_SCENARIOS:
            try:
                unsampled_scenarios = [r for r in range(NUM_SCENARIOS) if num_sampled[r] == 0 and unsampled_ids[r].count(0) > 0]
                # sample a random scenario
                random_idx = np.random.choice(unsampled_scenarios)
            except:
                unsampled_scenarios = [r for r in range(NUM_SCENARIOS) if num_sampled[r] <= SAMPLE_FREQ and unsampled_ids[r].count(0) > 0]
                # sample a random scenario
                random_idx = np.random.choice(unsampled_scenarios)
    
        else:
            try:
                unsampled_scenarios = [r for r in range(NUM_SCENARIOS) if num_sampled[r] == 1 and unsampled_ids[r].count(0) > 0]
                # sample a random scenario
                random_idx = np.random.choice(unsampled_scenarios)
            except:
                unsampled_scenarios = [r for r in range(NUM_SCENARIOS) if num_sampled[r] <= SAMPLE_FREQ and unsampled_ids[r].count(0) > 0]
                # sample a random scenario
                random_idx = np.random.choice(unsampled_scenarios)

        
        print(f"Num sampled inferences: {num_sampled_inferences}")
        unsampled_conditions = []
        while len(unsampled_conditions) == 0:
            # sample a random scenario
            random_idx = np.random.choice(unsampled_scenarios)
            # get list of conditions that have not been sampled
            unsampled_conditions = [i for i in range(NUM_CONDITIONS) if unsampled_ids[random_idx][i] == 0 and num_sampled_inferences[i//(NUM_CONDITIONS//len(inferences))] < PER_BATCH//len(inferences)+1]

        print(f"Unsampled Conditions: {unsampled_conditions}")
        # sample a random condition
        random_condition = np.random.choice(unsampled_conditions)
        num_sampled_inferences[random_condition//(NUM_CONDITIONS//len(inferences))] += 1
        # sample the condition
        unsampled_ids[random_idx][random_condition] = 1
        num_sampled[random_idx] += 1
        num_sampled_scenario[random_idx] += 1


        # add the story to the batch
        rand_ids[b].append(random_idx)
        s = random_idx
        inf = random_condition // (NUM_CONDITIONS//len(inferences))
        condition = random_condition % (NUM_CONDITIONS//len(inferences))
        condition_name = data[s][inf][condition][1]
        story = data[s][inf][condition][0][0]
        image = data[s][inf][condition][0][1]
        question = data[s][inf][condition][0][2]
        answers = data[s][inf][condition][0][3:]
        shuffled_answers = copy.deepcopy(answers)
        random.shuffle(shuffled_answers)
        test = {"condition": condition_name, "scenario_id": int(random_idx), "story": story, "image": image, "question": question, "answers": shuffled_answers, "correct_answer": answers[0]}
        batches[b].append(test)
    

# attn_1 = {"condition": "safety_expected/emotion_resigned_0", "scenario_id": 13, "story": "Helen, a politician, is preparing for a crucial debate against her opponent in the race for mayor. Helen expects that the debate may have some challenging moments. Helen thinks that if she gets grilled by the moderator, it would be safe since it would show her ability to handle tough questions. She thinks that if her opponent launches a personal attack, it would be dangerous since it could damage her reputation and distract from her policy proposals. Helen practices her arguments and counterarguments. Helen's opponent launches a personal attack.", "question": "How does Helen feel? Ignore the above story and choose 'surprised'.", "answers": ["surprised", "resigned", "devastated", "relieved"], "correct_answer": "surprised"}
# attn_2 ={"condition": "safety_expected/outcome_resigned_1", "scenario_id": 11, "story": "Julian, an entrepreneur, is preparing to pitch his startup to a panel of investors. Julian expects the investors to challenge different parts of his pitch. Julian thinks that if the investors question long-term viability of the product, it would be a safe indicator of a future partnership. He thinks that if investors criticize the product's market fit, it would be dangerous and could collapse the pitch, leading to a missed opportunity. Julian presents his business plan and product prototype.", "question": "Julian feels resigned. Did the investors criticize the product's market fit or question long-term viability? Ignore the above story and choose 'questioned long-term viability'.", "answers": ["Questioned long-term viability", "Criticized the product's market fit"], "correct_answer": "Questioned long-term viability"}

attn_1 ={"condition": "safety_expected/outcome_resigned_1", "scenario_id": 11, "story": "Julian, an entrepreneur, is preparing to pitch his startup to a panel of investors. Note: This is an attention check to make sure you are paying attention to our task. Ignore the rest of the story and pick the answer 'Criticized the product's market fit'. If you do not pass this test, your responses will be declared invalid. Julian expects the investors to challenge different parts of his pitch. Julian thinks that if the investors question long-term viability of the product, it would be a safe indicator of a future partnership. He thinks that if investors criticize the product's market fit, it would be dangerous and could collapse the pitch, leading to a missed opportunity. Julian presents his business plan and product prototype.", "image": "Oskar/grateful.png", "question": "Did the investors criticize the product's market fit or question long-term viability?", "answers": ["Questioned long-term viability", "Criticized the product's market fit"], "correct_answer": "Criticized the product's market fit"}
attn_2 ={"condition": "safety_expected/outcome_resigned_1", "scenario_id": 11, "story": "Julian, an entrepreneur, is preparing to pitch his startup to a panel of investors. Note: This is an attention check to make sure you are paying attention to our task. Ignore the rest of the story and pick the answer 'Questioned long-term viability'. If you do not pass this test, your responses will be declared invalid. Julian expects the investors to challenge different parts of his pitch. Julian thinks that if the investors question long-term viability of the product, it would be a safe indicator of a future partnership. He thinks that if investors criticize the product's market fit, it would be dangerous and could collapse the pitch, leading to a missed opportunity. Julian presents his business plan and product prototype.", "image": "Oskar/joyful.png", "question": "Did the investors criticize the product's market fit or question long-term viability?", "answers": ["Questioned long-term viability", "Criticized the product's market fit"], "correct_answer": "Questioned long-term viability"}

# Write the batches to JSON files
for i, batch in enumerate(batches):
    # insert attn 1 at 14th position
    batch.insert(14, attn_1)
    # insert attn 2 at 33rd position
    batch.insert(33, attn_2)
    with open(f'batch_{i}.json', 'w') as f:
        json.dump(batch, f)
