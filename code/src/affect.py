import random
import csv
import tqdm
import argparse

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from crfm import crfmChatLLM

from utils import push_data, get_num_items, get_vars_from_out
from domain_var import *

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
locations = ['school', 'work', 'home', 'the park', 'the store', 'the restaurant', 'the hospital', 'the airport', 'the beach', 'the gym', 'the library', 'the museum', 'the zoo', 'the mall', 'the theater', 'the stadium', 'the concert hall', 'the bar', 'the club', 'the cafe', 'the hotel', 'the gas station', 'the bank', 'the post office']
professions = ['doctor', 'lawyer', 'teacher', 'nurse', 'engineer', 'scientist', 'programmer', 'artist', 'writer', 'musician', 'actor', 'singer', 'dancer', 'chef', 'pilot', 'police officer', 'firefighter', 'soldier', 'businessman', 'politician', 'athlete', 'student', 'waiter', 'waitress', 'cashier', 'janitor', 'cleaner', 'mechanic', 'plumber', 'electrician', 'carpenter', 'farmer', 'gardener', 'landscaper', 'hairdresser', 'barber', 'designer', 'architect', 'photographer', 'journalist', 'reporter', 'baker', 'butcher', 'librarian']
DATA_DIR = '../../data'
PROMPT_DIR = '../prompt_instructions'
WORDS_DIR = '../words'


CSV_NAME = '{DOMAIN}'


parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=42, help='random seed')
parser.add_argument('--domain', type=str, default='goal_control', help='domain')
parser.add_argument('--model', type=str, default='openai/gpt-4-0314', help='model name')
parser.add_argument('--temperature', type=float, default=0.5, help='temperature')
parser.add_argument('--max_tokens', type=int, default=1000, help='max tokens')
parser.add_argument('--num_completions', type=int, default=1, help='number of completions')
parser.add_argument('--num_shots', type=int, default=3, help='number of shots')
parser.add_argument('--num_stories', type=int, default=1, help='number of stories to generate')
parser.add_argument('--verbose', action='store_true', help='verbose')


def get_llm(args):
    llm = crfmChatLLM(
        model_name=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        num_completions=args.num_completions,
        request_timeout=180
    )
    return llm

def get_human_message(args):
    if args.domain == 'goal_control':
        letter_name = random.choice(letters)
        location = random.choice(locations)
        message = f"Generate a story about a character whose name starts with {letter_name} and is at {location}."
    elif args.domain == 'safety_expected':
        letter_name = random.choice(letters)
        profession = random.choice(professions)
        message = f"Generate a story about a character whose name starts with {letter_name} and who is a {profession}."
    return message


def gen_chat(args):

    llm = get_llm(args)
    with(open(f'{PROMPT_DIR}/{args.domain}.txt', 'r')) as f:
        instruction_text = f.read()

    system_message = SystemMessage(content=instruction_text)
    human_message_0 = HumanMessage(content='Generate a story.')

    
    examples = []
    csv_file = f'{DATA_DIR}/{CSV_NAME}.csv'

    prompt_tokens_used = 0
    completion_tokens_used = 0

    # run loop with n stories, increase by num_completions
    for n_story in tqdm.tqdm(range(0, args.num_stories, args.num_completions)):
        s = get_human_message(args)
        human_message_1 = HumanMessage(content=s)

        # read examples from csv file every iteration to add generated samples to the pool of seed examples
        if args.verbose:
            print(f"Reading examples from {csv_file} with existing {get_num_items(csv_file)} examples")
        # read a few examples from the csv file
        with open(csv_file, 'r') as f:
            for line in f.readlines():
                params = line.split(';')
                example = {k: params[v].strip() for v, k in enumerate(template_var)} 
                examples.append(example)
        examples = examples[:args.num_shots]
        # random.shuffle(examples)

        messages = [system_message]	
        for i in range(args.num_shots):	
            messages.append(human_message_0)
            messages.append(AIMessage(content=response_template.format(**examples[i])))	
        messages.append(human_message_1)	
        if args.verbose:
            print(f"------ messages ------")	
            print(messages)	
        responses = llm.generate([messages], stop=["System:"])
        # prompt_tokens_used += responses.llm_output['token_usage']['prompt_tokens']
        # completion_tokens_used += responses.llm_output['token_usage']['completion_tokens']
        # price = (prompt_tokens_used * 0.03 + completion_tokens_used * 0.06) / 1000.
        # update tqdm progress bar with price
        # tqdm.tqdm.write(f"Price: {price:.2f} USD, Price per story: {price/(n_story+args.num_completions):.2f} USD")
        for g, generation in enumerate(responses.generations[0]):
            if args.verbose:
                print(f"------ Generated Story {n_story+g} ------")
                print(generation.text)
                print("------------ Fin --------------")
            try:
                out_vars = get_vars_from_out(generation.text, list_var)
            except:
                print("Error in parsing output")
                breakpoint()
            data = [out_vars[k] for k in list_var]
            story_file = f'{DATA_DIR}/{CSV_NAME}.csv'
            with open(story_file, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(data)
        # push to github
        # push_data(DATA_DIR, REPO_URL)
    
    
if __name__ == "__main__":
    args = parser.parse_args()
    random.seed(args.seed)
    CSV_NAME = CSV_NAME.format(DOMAIN=args.domain)
    if args.domain == 'goal_control':
        response_template = goal_control_template
        list_var = goal_control_list_var
        template_var = goal_control_template_var
    elif args.domain == 'safety_expected':
        response_template = safety_expected_template
        list_var = safety_expected_list_var
        template_var = safety_expected_template_var
    gen_chat(args)
