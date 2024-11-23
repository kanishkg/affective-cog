# evaluation script for morality
import time
import csv
import copy
import os
import argparse
import random
import yaml 
import json

from tqdm import tqdm
import anthropic



# from gpt4 import GPT4Agent
# from azure import AsyncAzureChatLLM, AzureChatLLM
from domain_var import *

def parse_response(raw_response, answer_options_list):
    if "a:" in raw_response.lower():
        if "a:" in raw_response:
            response = raw_response.split("a:")[1].lower().strip()
        elif "A:" in raw_response:
            response = raw_response.split("A:")[1].lower().strip()
    elif "answer:" in raw_response.lower():
        response = raw_response.split("Answer:")[1].lower().strip()
    else:
        response = raw_response.lower().strip()
    
    # answer is of the form <letter option>. <answer>, parse the letter option
    if "." in response:
        parsed_option = response.split(".")[0].strip()
        if parsed_option in ["a", "b", "c", "d", "e"]:
            return parsed_option
    else:
        # check if any of the answer options are in the response
        letters = ["a", "b", "c", "d", "e"]
        for i, answer in enumerate(answer_options_list):
            if answer.lower() in response:
                return letters[i]
    return "try again"

parser = argparse.ArgumentParser()

# model args
parser.add_argument('--model', type=str, default='gpt-4-0613', help='model name')
parser.add_argument('--temperature', type=float, default=0.0, help='temperature')
parser.add_argument('--max_tokens', type=int, default=10, help='max tokens')
parser.add_argument('--prompt', type=str, default="0shot", help='prompt')
parser.add_argument('--azure_config', type=str, default="azure_cogcas.yaml", help='azure config')
parser.add_argument('--completions', type=int, default=1, help='number of completions')

# eval args
parser.add_argument('--num', '-n', type=int, default=50, help='number of evaluations')
parser.add_argument('--offset', '-o', type=int, default=0, help='offset')
parser.add_argument('--verbose', action='store_true', help='verbose')

# data args
parser.add_argument('--data_dir', type=str, default='../../data/conditions_1/', help='data directory')
parser.add_argument('--output_dir', type=str, default='../../data/results/', help='output directory')

# all conditions
domains = ["goal_control", "safety_expected"]
inferences = ["belief_a", "belief_b", "emotion", "outcome"]
emotions = [
    goal_control_emotions, safety_expected_emotions
]
sets = ["0", "1"]


# join all variables
max_retry = 2
conditions = []
for i, domain in enumerate(domains):
    for inf in inferences:
        for emotion in emotions[i]:
            for s in sets:
                conditions.append(f"{domain}/{inf}_{emotion}_{s}")

# parse args
args = parser.parse_args()

# read the story, question, and answers from the csv file
data = {}
conditions = sorted(conditions)[22:24]
for condition in conditions:
    data[condition] = []
    with open(os.path.join(args.data_dir, condition, "stories.csv"), 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            story = row[0]
            question = row[1]
            answers = row[2:]
            data[condition].append({
                "story": story,
                "question": question,
                "answers": answers
            })

# get prompt
PROMPT_DIR = "../prompt_instructions/"
if args.prompt == "0shot":
    with open(os.path.join(PROMPT_DIR, "evaluation_0shot.txt"), 'r') as f:
        prompt = f.read().strip()
elif args.prompt == "0shot_cot":
    with open(os.path.join(PROMPT_DIR, "evaluation_0shot_cot.txt"), 'r') as f:
        prompt = f.read().strip()
else:
    raise ValueError(f"Prompt {args.prompt} not found.")

# initialize LLM
if args.model in ["gpt-4-0613", "gpt-3.5-turbo"]:
    # llm = ChatOpenAI(model_name=args.model,
    #                 temperature=args.temperature,
    #                 max_tokens = args.max_tokens)
    llm = crfmChatLLM(model_name=f"openai/{args.model}",
                    temperature=args.temperature,
                    max_tokens = args.max_tokens)
elif args.model in ["gpt-4-1106-preview"]:
    from openai import OpenAI
    client = OpenAI()
elif args.model in ["azure/gpt-4"]:
    assert args.azure_config is not None
    with open(args.azure_config, "r") as f:
        azure_config = yaml.load(f, Loader=yaml.FullLoader)
    azure_config["completion_config"]["max_tokens"] = args.max_tokens
    azure_config["completion_config"]["temperature"] = args.temperature
    import openai
    openai.api_type = "azure"
    openai.api_base = azure_config["azure_api"]["azure_endpoint"]
    openai.api_key = azure_config["azure_api"]["api_key"]
    openai.api_version = azure_config["azure_api"]["api_version"]
    # llm = AzureChatLLM(**azure_config["azure_api"])
    # llm = GPT4Agent(llm=model, azure_config=azure_config["completion_config"])
elif args.model in ["gemini-1.5-pro-002"]:
    import google.generativeai as genai
    # Create the model
    generation_config = {
        "temperature": args.temperature,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": args.max_tokens,
        "response_mime_type": "text/plain",
        }

    model = genai.GenerativeModel(
        model_name=args.model,
        generation_config=generation_config,
        system_instruction=prompt
    )    
    # llm = GenerativeModel("gemini-1.5-pro-preview-0409")
    # import google.generativeai as genai
    # genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # generation_config = {
    #     "temperature": args.temperature,
    #     "top_p": 0.95,
    #     "top_k": 1,
    #     "max_output_tokens": args.max_tokens,
    #     "response_mime_type": "text/plain",
    # }
    # generation_config = GenerationConfig(
    #     temperature=args.temperature,
    #     max_output_tokens=args.max_tokens,
    #     stop_sequences=["Q:"])
    # llm = ChatVertexAI(model_name="gemini-1.0-pro",
    #                temperature=args.temperature,
    #                max_output_tokens=args.max_tokens,
    #                convert_system_message_to_human=True)
elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022"]:
    client = anthropic.Anthropic()
elif args.model in ["claude-2.1"]:
    llm = ChatAnthropic(model_name=args.model,
                    temperature=args.temperature,
                    max_tokens = args.max_tokens)
elif args.model in ["llama-2-7b-chat"]:
    llm = HuggingFacePipeline.from_model_id(
        model_id="meta-llama/Llama-2-7b-chat-hf",
        task="text-generation",
        model_kwargs={"temperature": args.temperature, "max_length": args.max_tokens},
    )
else:
    raise ValueError(f"Model {args.model} not found.")

# evaluate

for condition in conditions:
    print(condition)
    predicted_answers = []
    graded_answers = []
    parsed_answers = []
    for i in tqdm(range(args.offset, args.num)):
        predicted_answers.append([])
        parsed_answers.append([])
        graded_answers.append([])
        for _ in range(args.completions):
            story = data[condition][i]['story']
            name = story.split(',')[0]
            question = data[condition][i]['question']
            answers = data[condition][i]['answers']
            correct_answer = answers[0]
            shuffled_answers = copy.deepcopy(answers)
            random.shuffle(shuffled_answers)
            
            # format the answers as options for the qa style answer
            # <letter option>. <answer>

            letters = ["a", "b", "c", "d", "e"]
            answer_options_list = []
            correct_answer_option = letters[shuffled_answers.index(correct_answer)]
            for a, answer in enumerate(shuffled_answers):
                answer_options_list.append(f"{letters[a]}. {answer}")
            answer_options = "\n".join(answer_options_list)
            # skip last newline
            # answer_options = answer_options[:]
            query = f"{story}\nQ: {question}\n{answer_options}"

            if args.model in ["gpt-4-0613", "gpt-3.5-turbo", "claude-2.1"]:
                messages = [SystemMessage(content=prompt), HumanMessage(content=query)]
                response = llm.generate([messages], stop=["Q:"]).generations[0][0].text
                time.sleep(1)
            
            elif args.model in ["gpt-4-1106-preview"]:
                message_list = [
                {"role": "user", "content": query},
            ]
                message = client.messages.create(
                    model=args.model,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    system=prompt,
                    messages=message_list
                )
                response = message.choices[0].message.content
            elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022"]:
                message_list = [
                {"role": "user", "content": query},
            ]
                message = client.messages.create(
                    model=args.model,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    system=prompt,
                    messages=message_list
                )
                response = message.content[0].text
            elif args.model in ["gemini-1.5-pro-002"]:
                chat_session = model.start_chat(history=[])
                query = f"{prompt}\n{query}"
                response = chat_session.send_message(query).text
                message_list =  [
                    {"role": "user", "parts": [{"text": query}]}
                ]
                # response = llm.generate_content(contents=message_list)

                # print(response.candidates[0].finish_reason)
                # if str(response.candidates[0].finish_reason) == "FinishReason.SAFETY":
                #     response = "A:e. none of the above"
                # else:
                #     response = response.candidates[0].content.parts[0].text
                # time.sleep(13)
            elif args.model in ["llama-2-7b-chat"]:
                template = f"Instructions: {prompt}\n{query}\nA:"
                response = llm(template)[0]
            elif args.model in ["azure/gpt-4"]:
                messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ]
                retries = 0
                success = False
                while retries < max_retry and not success:
                    try:
                        response = openai.ChatCompletion.create(
                        engine=azure_config["azure_api"]["azure_deployment"],
                        messages=messages, 
                            **azure_config["completion_config"]
                        )
                        retries += 1
                        response = response['choices'][0]['message']['content']
                        success = True
                        break
                    except Exception as e:
                        print("gpt-4 azure error", retries)
                        time.sleep(1)
                        retries += 1
                if not success:
                    # raise ValueError("Failed to get response from gpt-4 azure")
                    response = "A:e. none of the above"
                    print("gpt-4 azure error", retries)
            # if args.model in ["gpt-4-0613", "gpt-3.5-turbo", "claude-2.1"]:
            #     messages = [SystemMessage(content=prompt), HumanMessage(content=query)]
            #     response = llm.generate([messages], stop=["Q:"]).generations[0][0].text
            # elif args.model in ["llama-2-7b-chat"]:
            #     template = f"Instructions: {prompt}\n{query}\nA:"
            #     response = llm(template)[0]
            
            # parse response
            parsed_response = parse_response(response, answer_options_list)
            if args.model in ["gpt-4-0613", "gpt-3.5-turbo", "claude-2.1"]:
                message_list = [SystemMessage(content=prompt), HumanMessage(content=query), AIMessage(content=response)]
            elif args.model in ["gemini-1.5-pro-002"]:
                message_list.append({"role": "model", "parts": [response]})
            elif args.model in ["azure/gpt-4"]:
                message_list = [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]
            elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022"]:
                message_list = [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]
            tried = 0
            while parsed_response == "try again":
                tried += 1
                if args.model in ["gpt-4-0613", "gpt-3.5-turbo", "claude-2.1"]:
                    message_list.append(HumanMessage(content="Try again, choose one of the options."))
                    print("calling llm")
                    response = llm.generate([message_list], stop=["Q:"]).generations[0][0].text
                    time.sleep(1)
                    print("llm called")
                elif args.model in ["gemini-1.5-pro-002"]:
                    message_list.append({"role": "user", "parts": [f"Try again, choose one of the options {letters[:len(shuffled_answers)]}."]})
                    response = chat_session.send_message(query).text
                    # if str(response.candidates[0].finish_reason) == "FinishReason.SAFETY":
                    #     response = "A:e. none of the above"
                    # else:
                    #     response = response.candidates[0].content.parts[0].text
                    # time.sleep(13)

                elif args.model in ["azure/gpt-4"]:
                    message_list.append({"role": "user", "content": "Try again, choose one of the options."})
                    response = openai.ChatCompletion.create(
                        engine=azure_config["azure_api"]["azure_deployment"],
                        messages=messages, 
                        **azure_config["completion_config"]
                    )
                    time.sleep(1)
                    response = response['choices'][0]['message']['content']
                elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022"]:
                    message_list.append({"role": "user", "content": "Try again, choose one of the options."})
                    message = client.messages.create(
                        model=args.model,
                        max_tokens=args.max_tokens,
                        system=prompt,
                        temperature=args.temperature,
                        messages=message_list
                    )
                    response = message.content[0].text
                parsed_response = parse_response(response, answer_options_list)
                if args.model in ["gpt-4-0613", "gpt-3.5-turbo", "claude-2.1"]:
                    message_list.append(AIMessage(content=response))
                elif args.model in ["gemini-1.5-pro-002"]:
                    message_list.append({"role": "assistant", "parts": [response]})
                elif args.model in ["azure/gpt-4"]:
                    message_list.append({"role": "assistant", "content": response})
                elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022"]:
                    message_list.append({"role": "assistant", "content": response})
                print(f"tried: {tried}")
                if tried > max_retry:
                    response = "A:e. none of the above"
                    parsed_response = "e"
                    break
            if parsed_response == "e":
                parsed_answer = "none of the above"
            else:
                if letters.index(parsed_response) >= len(shuffled_answers):
                    parsed_answer = "none of the above"
                else:
                    parsed_answer = shuffled_answers[letters.index(parsed_response)]
            parsed_answers[-1].append(parsed_answer)
            # grade response
            if parsed_response == correct_answer_option:
                graded_response = 1
            else:
                graded_response = 0

            if args.verbose:
                print("--------------------------------------------------")
                print(f"Condition: {condition}")
                print(f"Prompt: {prompt}")
                print(f"Story: {story}")
                print(f"Q: {query}")
                print(f"A: {response}")
                print(f"Parsed A: {parsed_response}")
                print(f"Correct A: {correct_answer_option}")
                print(f"Graded A: {graded_response}")

            # append to list
            predicted_answers[-1].append(response)
            graded_answers[-1].append(graded_response)
    
    # write to file
    if not os.path.exists(os.path.join(args.output_dir, condition)):
        os.makedirs(os.path.join(args.output_dir, condition))
            
    prefix = f"{args.model.replace('/','_')}_{args.prompt}_{args.temperature}_{args.num}_{args.offset}_{args.completions}"
    with open(os.path.join(args.output_dir, condition, f"{prefix}_predicted_answers.json"), 'w') as f:
        json.dump(predicted_answers, f, indent=4)
    with open(os.path.join(args.output_dir, condition, f"{prefix}_parsed_answers.json"), 'w') as f:
        json.dump(parsed_answers, f, indent=4)
    with open(os.path.join(args.output_dir, condition, f"{prefix}_graded_answers.json"), 'w') as f:
        json.dump(graded_answers, f, indent=4)
    # with open(os.path.join(args.output_dir, condition, f"{prefix}_parsed_answers.txt"), 'w') as f:
    #     f.write('\n'.join(parsed_answers))
    # with open(os.path.join(args.output_dir, condition, f"{prefix}_graded_answers.txt"), 'w') as f:
    #     f.write('\n'.join([str(x) for x in graded_answers]))
