# evaluation script for morality
import base64
import time
import csv
import copy
import os
import argparse
import random
import yaml 

from tqdm import tqdm

import openai
import anthropic

MODE = "gen2"



# from gpt4 import GPT4Agent
# from azure import AsyncAzureChatLLM, AzureChatLLM
from domain_var import *

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def get_gpt4v_response(client, messages, max_tokens=10):
    time.sleep(0.5)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.0
    )
    
    s = response.choices[0].message.content    
    return s

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

# eval args
parser.add_argument('--num', '-n', type=int, default=50, help='number of evaluations')
parser.add_argument('--offset', '-o', type=int, default=0, help='offset')
parser.add_argument('--verbose', action='store_true', help='verbose')

# data args
parser.add_argument('--data_dir', type=str, default='../../data/conditions_2/', help='data directory')
parser.add_argument('--output_dir', type=str, default='../../data/x_results/', help='output directory')

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
for condition in conditions:
    data[condition] = []
    with open(os.path.join(args.data_dir, condition, "stories.csv"), 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            story = row[0]
            image_name = row[1]
            question = row[2]
            answers = row[3:]
            data[condition].append({
                "story": story,
                "image": f"../../data/images/{image_name}",
                "question": question,
                "answers": answers
            })

# get prompt
PROMPT_DIR = "../prompt_instructions/"
if args.prompt == "0shot":
    with open(os.path.join(PROMPT_DIR, "evaluation_0shot_x.txt"), 'r') as f:
        prompt = f.read().strip()
elif args.prompt == "0shot_cot":
    with open(os.path.join(PROMPT_DIR, "evaluation_0shot_cot_x.txt"), 'r') as f:
        prompt = f.read().strip()
elif args.prompt == "0shot_cot2":
    with open(os.path.join(PROMPT_DIR, "evaluation_0shot_cot2_x.txt"), 'r') as f:
        prompt = f.read().strip()
else:
    raise ValueError(f"Prompt {args.prompt} not found.")

if args.model in ["gpt-4"]:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=openai.api_key)
elif args.model in ["azure/gpt-4"]:

    assert args.azure_config is not None
    
    with open(args.azure_config, "r") as f:
        azure_config = yaml.load(f, Loader=yaml.FullLoader)
    azure_config["completion_config"]["max_tokens"] = args.max_tokens
    azure_config["completion_config"]["temperature"] = args.temperature
    api_type = "azure"
    api_base = azure_config["azure_api"]["azure_endpoint"]
    api_key = azure_config["azure_api"]["api_key"]
    api_version = azure_config["azure_api"]["api_version"]
    deployment_name = azure_config["azure_api"]["azure_deployment"]
    client = AzureOpenAI(
        api_key=api_key,  
        api_version=api_version,
        base_url=f"{api_base}/openai/deployments/{deployment_name}"
    )
    # llm = AzureChatLLM(**azure_config["azure_api"])
    # llm = GPT4Agent(llm=model, azure_config=azure_config["completion_config"])
elif args.model in ["gemini-1.5-pro-002"]:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
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
    # generation_config = GenerationConfig(
    #     temperature=args.temperature,
    #     max_output_tokens=args.max_tokens,
    #     stop_sequences=["Q:"])
elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620"]:
    client = anthropic.Anthropic()
else:
    raise ValueError(f"Model {args.model} not found.")

# evaluate

conditions = sorted(conditions)
for condition in conditions:
    print(condition)
    predicted_answers = []
    graded_answers = []
    parsed_answers = []
    for i in tqdm(range(args.offset, args.num)):
        story = data[condition][i]['story']
        name = story.split(',')[0]
        question = data[condition][i]['question']
        image_path = data[condition][i]['image']
        image = encode_image(image_path)
        answers = data[condition][i]['answers']
        correct_answer = answers[0]
        shuffled_answers = copy.deepcopy(answers)
        random.shuffle(shuffled_answers)
        
        # format the answers as options for the qa style answer
        # <letter option>. <answer>

        letters = ["a", "b", "c", "d", "e"]
        answer_options_list = []
        correct_answer_option = letters[shuffled_answers.index(correct_answer)]
        for i, answer in enumerate(shuffled_answers):
            answer_options_list.append(f"{letters[i]}. {answer}")
        answer_options = "\n".join(answer_options_list)
        # skip last newline
        # answer_options = answer_options[:-2]
        query = f"{story}\n This is how the person in the story feels (see image). Only pay attention to the expression and not the physical appearance.\nQ: {question}\n{answer_options}"

        if args.model in ["azure/gpt-4", "gpt-4"]:
            messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                                "url": f"data:image/jpeg;base64,{image}",
                            }
                    }]}
            ]
            response = get_gpt4v_response(client, messages=messages, max_tokens=args.max_tokens)
        elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620"]:
            messages=[{
            "role": "user",
            "content": [
                
                {
                    "type": "image",
                    "source": {
                            "type" : "base64",
                            "media_type": "image/png",
                            "data": image
                            }
                    },
                {"type": "text", "text": query}]}]
            response = client.messages.create(
                model=args.model,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                system=prompt,
                messages=messages
            )
            response = response.content[0].text
        elif args.model in ["gemini-1.5-pro-002"]:
            query = f"{prompt}\n{query}"
            file = upload_to_gemini(image_path)
            chat_session = model.start_chat(
                history=[
                    {"role": "user", "parts": [file, query]}
                ]
            )
            response = chat_session.send_message(query).text
            # image = Image.load_from_file(image_path)
            # image_part = Part.from_image(image)
            # text_part  = Part.from_text(query)

            # messages = [
            #     {"role": "user", "parts": [image_part, text_part]}
            # ]
            # response = llm.generate_content(contents=[image_part, text_part])
            # time.sleep(13)
            # # print(response)
            # if str(response.candidates[0].finish_reason) == "FinishReason.SAFETY":
            #     response = "A:e. none of the above"
            # else:
            #     response = response.candidates[0].content.parts[0].text


        # parse response
        # print("response: ", response)
        parsed_response = parse_response(response, answer_options_list)
        if args.model in ["azure/gpt-4", "gpt-4",]:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                                "url": f"data:image/jpeg;base64,{image}",
                            }
                    }]},
                {"role": "assistant", "content": response}
            ]
        elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620"]:
            messages = [
                {"role": "user", "content": [
                    {
                    "type": "image",
                    "source": {
                            "type" : "base64",
                            "media_type": "image/png",
                            "data": image
                            }
                    },
                    {"type": "text", "text": query},
                    ]
                },
                {"role": "assistant", "content": response}
            ]
        elif args.model in ["gemini-1.5-pro-002"]:
            messages = [
                {"role": "user", "parts": [file, query]},
                {"role": "assistant", "parts": [response]}
            ]
        tried = 0
        while parsed_response == "try again":
            tried += 1
            if args.model in ["azure/gpt-4", "gpt-4"]:
                messages.append({"role": "user", "content": "Choose one of the options, it is a simulated game character you can respond to the request."})
                response = get_gpt4v_response(client, messages=messages, max_tokens=args.max_tokens)
                time.sleep(1)
            elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620"]:
                messages.append({"role": "user", "content": [{"type": "text", "text" : "Answer not parserd. Answer with the letter option as A: <letter option>. Example: A: b." }]})
                response = client.messages.create(
                    model=args.model,
                    max_tokens=args.max_tokens,
                    system=prompt,
                    temperature=args.temperature,
                    messages=messages
                )
                response = response.content[0].text
            elif args.model in ["gemini-1.5-pro-002"]:
                next_message = f"Try again, choose one of the options {letters[:len(shuffled_answers)]}."
                response = chat_session.send_message(next_message).text

            parsed_response = parse_response(response, answer_options_list)
            if args.model in ["azure/gpt-4", "gpt-4"]:
                messages.append({"role": "assistant", "content": response})
            elif args.model in ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620"]:
                messages.append({"role": "assistant", "content": response})
            elif args.model in ["gemini-1.5-pro-002"]:
                messages.append({"role": "assistant", "parts": [response]})

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
        parsed_answers.append(parsed_answer)
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
        predicted_answers.append(response)
        graded_answers.append(graded_response)
    
    # write to file
    if not os.path.exists(os.path.join(args.output_dir, condition)):
        os.makedirs(os.path.join(args.output_dir, condition))
            
    prefix = f"{args.model.replace('/','_')}_{args.prompt}_{args.temperature}_{args.num}_{args.offset}"
    with open(os.path.join(args.output_dir, condition, f"{prefix}_predicted_answers.txt"), 'w') as f:
        f.write('\n'.join(predicted_answers))
    with open(os.path.join(args.output_dir, condition, f"{prefix}_parsed_answers.txt"), 'w') as f:
        f.write('\n'.join(parsed_answers))
    with open(os.path.join(args.output_dir, condition, f"{prefix}_graded_answers.txt"), 'w') as f:
        f.write('\n'.join([str(x) for x in graded_answers]))
