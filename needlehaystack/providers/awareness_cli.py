import os
import shutil
import subprocess
from typing import Optional
import tiktoken
import json
from datetime import datetime

#from anthropic import Anthropic as AnthropicModel

from .model import ModelProvider

BASE_RUN_RESULT_DIRECTORY_URI = f"awarity_results/"

class AwarenessCLI(ModelProvider):
    """
    A wrapper class for interacting with Awareness' CLI client, providing methods to encode text, generate prompts,
    evaluate models.

    Attributes:
        model_name (str): The name of the AwarenessCLI model to use for evaluations and interactions.
        model (AsyncOpenAI): An instance of the AwarenessCLI client for Awareness calls.
        tokenizer: A tokenizer instance for encoding and decoding text to and from token representations.
    """
    
    DEFAULT_MODEL_KWARGS: dict = dict(max_tokens  = 300,
                                      temperature = 0)

    def __init__(self,
                 args: dict,
                 model_name: str = "gpt-4o",
                 model_kwargs: dict = DEFAULT_MODEL_KWARGS):
        """
        Initializes the AwarenessCLI model provider with a specific model.

        Args:
            model_name (str): The name of the AwarenessCLI model to use. Defaults to 'gpt-4o'.
            model_kwargs (dict): Model configuration. Defaults to {max_tokens: 300, temperature: 0}.
        
        Raises:
            ValueError: If NIAH_MODEL_API_KEY is not found in the environment.
        """
        api_key = os.getenv('NIAH_MODEL_API_KEY')
        if (not api_key):
            raise ValueError("NIAH_MODEL_API_KEY must be in env.")

        self._create_result_directories(args, model_name)

        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.api_key = api_key

        self.model = None
        #self.model = AsyncOpenAI(api_key=self.api_key)

        self.tokenizer = tiktoken.encoding_for_model("gpt-4")  # NOTE: will return cl100k_base for model == gpt-4, which is the encoding Steve recommends for Awareness
        #self.tokenizer = AnthropicModel().get_tokenizer()   # BPE

        #self.tokenizer = tiktoken.encoding_for_model(self.model_name)
    
    async def evaluate_model(self, prompt: str, context_file_location) -> str:
        """
        Evaluates a given prompt using Awareness' model and retrieves the model's response.

        Args:
            prompt (str): The prompt to send to the model.

        Returns:
            str: The content of the model's response to the prompt.
        """

        # Store the context file
        CONTEXT_URI = f"{self.contexts_directory_uri}{context_file_location}_context.txt"
        with open(CONTEXT_URI, "w") as file:
            file.write(prompt[1]['content'])

        # Call Awareness CLI
        exit_code = self._call_awarenesscli(prompt[2]['content'], CONTEXT_URI, self.model_name)
        print(f"Command exited with code {exit_code}")

        # Store the training.jsonl file
        TRAINING_SRC_URI = "training.jsonl"
        TRAINING_DEST_URI = f"{self.trainings_directory_uri}{context_file_location}_training.jsonl"
        try:
            shutil.move(TRAINING_SRC_URI, TRAINING_DEST_URI)
            print(f"Training file moved from {TRAINING_SRC_URI} to {TRAINING_DEST_URI} successfully.")
        except Exception as e:
            print(f"Error: {e}")

        # Store the output.json file
        OUTPUT_SRC_URI = "output.json"
        OUTPUT_DEST_URI = f"{self.outputs_directory_uri}{context_file_location}_output.json"
        try:
            shutil.move(OUTPUT_SRC_URI, OUTPUT_DEST_URI)
            print(f"Output file moved from {OUTPUT_SRC_URI} to {OUTPUT_DEST_URI} successfully.")
        except Exception as e:
            print(f"Error: {e}")

        # Read the output.json file
        with open(OUTPUT_DEST_URI, "r") as json_file:
            output = json.load(json_file)
        
        return output['message']
    
    # NOTE: this is the thing that generates a prompt based on context and the question. OpenAI call example:
    # prompt: [{'role': 'system', 'content': 'You are a helpful AI bot that answers questions for a user. Keep your response short and direct'}, {'role': 'user', 'content': 'July 2010What hard liquor, cigarettes, heroin, and crack have in common is\nthat they\'re all more concentrated forms of less addictive predecessors.\nMost if not all the things we describe as addictive are.  And the\nscary thing is, the process that created them is accelerating.We wouldn\'t want to stop it.  It\'s the same process that cures\ndiseases: technological progress.  Technological progress means\nmaking things do more of what we want.  When the thing we want is\nsomething we want to want, we consider technological progress good.\nIf some new technique makes solar cells x% more efficient, that\nseems strictly better.  When progress concentrates something we\ndon\'t want to wantâ€”when it transforms opium into heroinâ€”it seems\nbad.  But it\'s the same process at work.\n[1]No one doubts this process is accelerating, which means increasing\nnumbers of things we like will be transformed into things we like\ntoo much.\n[2]As far as I know there\'s no word for something we like too much.\nThe closest is the colloquial sense of "addictive." That usage has\nbecome increasingly common during my lifetime.  And it\'s clear why:\nthere are an increasing number of things we need it for.  At the\nextreme end of the spectrum are crack and meth.\nThe best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny day.\n  Food has been\ntransformed by a combination of factory farming and innovations in\nfood processing into something with way more immediate bang for the\nbuck, and you can see the results in any town in America.  Checkers\nand solitaire have been replaced by World of Warcraft and FarmVille.\nTV has become much more engaging, and even so it can\'t compete with Facebook.The world is more addictive than it was 40 years ago.   And unless\nthe forms of technological progress that produced these things are\nsubject to different laws than technological progress in general,\nthe world will get more addictive in the next 40 years than it did\nin the last 40.The next 40 years will bring us some wonderful things.  I don\'t\nmean to imply they\'re all to be avoided.  Alcohol is a dangerous\ndrug, but I\'d rather live in a world with wine than one without.\nMost people can coexist with alcohol; but you have to be careful.\nMore things we like will mean more things we have to be careful\nabout.Most people won\'t, unfortunately.  Which means that as the world\nbecomes more addictive, the two senses in which one can live a\nnormal life will be driven ever further apart.  One sense of "normal"\nis statistically normal: what everyone else does.  The other is the\nsense we mean when we talk about the normal operating range of a\npiece of machinery: what works best.These two senses are already quite far apart.  Already someone\ntrying to live well would seem eccentrically abstemious in most of\nthe US.  That phenomenon is only going to become more pronounced.\nYou can probably take it as a rule of thumb from now on that if\npeople don\'t think you\'re weird, you\'re living badly.Societies eventually develop antibodies to addictive new things.\nI\'ve seen that happen with cigarettes.  When cigarettes first\nappeared, they spread the way an infectious disease spreads through\na previously isolated population.  Smoking rapidly became a\n(statistically) normal thing.  There were ashtrays everywhere.  We\nhad ashtrays in our house when I was a kid, even though neither of\nmy parents smoked.  You had to for guests.As knowledge spread about the dangers of smoking, customs changed.\nIn the last 20 years, smoking has been transformed from something\nthat seemed totally normal into a rather seedy habit: from something\nmovie stars did in publicity shots to something small h'}, {'role': 'user', 'content': "What is the best thing to do in San Francisco? Don't give information outside the document or repeat your findings"}]
    def generate_prompt(self, context: str, retrieval_question: str) -> str | list[dict[str, str]]:
        """
        Generates a structured prompt for querying the model, based on a given context and retrieval question.

        Args:
            context (str): The context or background information relevant to the question.
            retrieval_question (str): The specific question to be answered by the model.

        Returns:
            list[dict[str, str]]: A list of dictionaries representing the structured prompt, including roles and content for system and user messages.
        """
        return [{
                "role": "system",
                "content": "You are a helpful AI bot that answers questions for a user. Keep your response short and direct"
            },
            {
                "role": "user",
                "content": context
            },
            {
                "role": "user",
                "content": f"{retrieval_question} Do not give information outside the document or repeat your findings"
            }]
    
    def encode_text_to_tokens(self, text: str) -> list[int]:
        """
        Encodes a given text string to a sequence of tokens using the model's tokenizer.

        Args:
            text (str): The text to encode.

        Returns:
            list[int]: A list of token IDs representing the encoded text.
        """
        return self.tokenizer.encode(text)
    
    def decode_tokens(self, tokens: list[int], context_length: Optional[int] = None) -> str:
        """
        Decodes a sequence of tokens back into a text string using the model's tokenizer.

        Args:
            tokens (list[int]): The sequence of token IDs to decode.
            context_length (Optional[int], optional): An optional length specifying the number of tokens to decode. If not provided, decodes all tokens.

        Returns:
            str: The decoded text string.
        """
        return self.tokenizer.decode(tokens[:context_length])
    
    def _call_awarenesscli(self, question, context_uri, model_name):
        COMMAND = f'awareness --create-training --output json query "{question}" --uri {context_uri} --model {model_name}'
        try:
            # Run the command
            print(f"Running: {COMMAND}")
            result = subprocess.run(COMMAND, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Print the output and error (if any)
            print("Output:")
            print(result.stdout)
            if result.stderr:
                print("Error:")
                print(result.stderr)

            # Return the exit code
            return result.returncode
        except subprocess.CalledProcessError as e:
            # Handle errors in the called command
            print(f"Command '{COMMAND}' returned non-zero exit status {e.returncode}.")
            print("Error output:")
            print(e.stderr)
            return e.returncode
        
    def _create_result_directories(self, args, model_name):
        # Set the results folder name
        results_folder_name_for_test_run = f"awareness_{model_name}"
        if args.context_lengths is not None and len(args.context_lengths) > 0:
            results_folder_name_for_test_run += f"_len{args.context_lengths[0]}"
        else:
            results_folder_name_for_test_run += f"_len{args.context_lengths_min}-{args.context_lengths_max}"
        results_folder_name_for_test_run += f"_depth{args.document_depth_percent_min}-{args.document_depth_percent_max}"
        results_folder_name_for_test_run += "_multi" if args.multi_needle else "_single"
        results_folder_name_for_test_run += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create the results folder
        run_result_directory_uri = f"{BASE_RUN_RESULT_DIRECTORY_URI}{results_folder_name_for_test_run}/"
        if not os.path.exists(run_result_directory_uri):
            print(f"Creating run result directory: {run_result_directory_uri}")
            os.makedirs(run_result_directory_uri)

        # Create the contexts subfolder
        contexts_directory_uri = f"{run_result_directory_uri}contexts/"
        if not os.path.exists(contexts_directory_uri):
            print(f"Creating contexts directory: {contexts_directory_uri}")
            os.makedirs(contexts_directory_uri)

        # Create the trainings subfolder
        trainings_directory_uri = f"{run_result_directory_uri}trainings/"
        if not os.path.exists(trainings_directory_uri):
            print(f"Creating trainings directory: {trainings_directory_uri}")
            os.makedirs(trainings_directory_uri)

        # Create the outputs subfolder
        outputs_directory_uri = f"{run_result_directory_uri}outputs/"
        if not os.path.exists(outputs_directory_uri):
            print(f"Creating outputs directory: {outputs_directory_uri}")
            os.makedirs(outputs_directory_uri)

        # Store these values for later use
        self.contexts_directory_uri = contexts_directory_uri
        self.trainings_directory_uri = trainings_directory_uri
        self.outputs_directory_uri = outputs_directory_uri
    
    # NOTE: not impl
    # def get_langchain_runnable(self, context: str) -> str:
    #     """
    #     Creates a LangChain runnable that constructs a prompt based on a given context and a question, 
    #     queries the OpenAI model, and returns the model's response. This method leverages the LangChain 
    #     library to build a sequence of operations: extracting input variables, generating a prompt, 
    #     querying the model, and processing the response.

    #     Args:
    #         context (str): The context or background information relevant to the user's question. 
    #         This context is provided to the model to aid in generating relevant and accurate responses.

    #     Returns:
    #         str: A LangChain runnable object that can be executed to obtain the model's response to a 
    #         dynamically provided question. The runnable encapsulates the entire process from prompt 
    #         generation to response retrieval.

    #     Example:
    #         To use the runnable:
    #             - Define the context and question.
    #             - Execute the runnable with these parameters to get the model's response.
    #     """

    #     template = """You are a helpful AI bot that answers questions for a user. Keep your response short and direct" \n
    #     \n ------- \n 
    #     {context} 
    #     \n ------- \n
    #     Here is the user question: \n --- --- --- \n {question} \n Don't give information outside the document or repeat your findings."""
        
    #     prompt = PromptTemplate(
    #         template=template,
    #         input_variables=["context", "question"],
    #     )
    #     # Create a LangChain runnable
    #     model = ChatOpenAI(temperature=0, model=self.model_name)
    #     chain = ( {"context": lambda x: context,
    #               "question": itemgetter("question")} 
    #             | prompt 
    #             | model 
    #             )
    #     return chain
