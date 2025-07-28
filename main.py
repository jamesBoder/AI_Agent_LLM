import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import sys
#import google.generativeai as genai
# ...rest as needed
from functions.get_files_info import schema_get_files_info, handle_function_calls, call_function, available_functions, write_file, get_file_content
from config import system_prompt
# import the run_python_file function
from functions.run_python import run_python_file

from google.genai import types

schema_sanity_check = types.FunctionDeclaration(
    name="test_echo_file_path",
    description="Echos file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file"
            ),
        }
    )
)

"""test_tool = types.Tool(function_declarations=[schema_sanity_check])

print("=== MINIMAL TOOL SCHEMA CHECK ===")
print(test_tool)
for fd in test_tool.function_declarations:
    print(fd.name, fd.parameters.type)
    for prop, schema in fd.parameters.properties.items():
        print(f"  {prop}:", schema.type)
print("=================================")"""


# print(sys.argv)

# define working_directory as the current working directory
working_directory = os.getcwd()



# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Import genai library to create a new instance of the Gemini API client
client = genai.Client(api_key=api_key)



if __name__ == "__main__":

    # init is_verbose boolean variable
    is_verbose = "--verbose" in sys.argv
        # Your prompt-argument checks and agent logic go here


        # if len(sys.argv) == 1: skip the prompt argument check and run the script and return
    if len(sys.argv) == 1:
        print("No prompt provided. Running default agent behavior.")
        sys.exit(0)

    elif len(sys.argv) != 1:
        # Extract the user prompt from command line arguments, excluding any flags (arguments starting with '--')
        prompt_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
        user_prompt = " ".join(prompt_args)
        # if user_prompt is only flag arguments, print error message and exit program with exit code 1
        if not user_prompt.strip():
            print("Error: Please provide a valid prompt.")
            sys.exit(1)



    # create new list of types.Content and set the only message as the user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Add the system prompt to the messages
    """messages.append(types.Content(role="system", parts=[types.Part(text=system_prompt)]))
    """


    # Generate content using the Gemini API client
    # Note: The model can be set to "gemini-2.5-flash
    """response = client.models.generate_content(
        model = "gemini-2.5-flash", # A common and capable model
        contents=messages,  # or whatever variable holds your prompt
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    # check .candidates for each response, iterate and add it's .content to messages
    for candidate in response.candidates:
        if candidate.content:
            messages.append(candidate.content)"""
    
    

    # create a loop to call repeatedly, limit loop to 20 iterations. use try-except to handle any errors
    for i in range(20):
        
        try:

            """print("=== available_functions ===")
            print(available_functions)
            for fd in available_functions.function_declarations:
                print(fd.name, fd.parameters.type)
                for prop, schema in fd.parameters.properties.items():
                    print(f"  {prop}:", schema.type)
            print("===========================") """

            # Generate content again with the updated messages
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )


            # Append all candidate.content to messages
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
            
            # Check for response.text. If it exists, print final response and break the loop
            if response.text:
                print("Final response:")
                print(response.text)
                break

            # iterate through each part in the content to find function calls
            if response.candidates and response.candidates[0].content:
                content = response.candidates[0].content
                if content.parts:
                    for part in content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            function_call = part.function_call
                            # call the function using call_function and pass the function_call
                            result = call_function(function_call, verbose=is_verbose)
                            
                            # Extract the actual response data from the Content object
                            if result and result.parts and result.parts[0].function_response:
                                function_response_data = result.parts[0].function_response.response
                            else:
                                function_response_data = {"error": "No response data"}

                            # use the extracted response data to create a new types.Content and add it to messages
                            messages.append(types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call.name, response=function_response_data)]))
                                            
            
        except Exception as e:
            print(f"Error during function call: {e}")
            break
        


    # print result.parts[0].function_response.response if result and verbose flag is present
    """if result and is_verbose:
        if hasattr(result, 'parts'):
                        # Object format
            if result.parts and result.parts[0].function_response:
                 print(f"-> {result.parts[0].function_response.response}")
                
                
        elif isinstance(result, dict) and 'parts' in result:
            if (result['parts'] and 
                len(result['parts']) > 0 and 
                'function_response' in result['parts'][0] and
                'response' in result['parts'][0]['function_response']):
                print(f"-> {result['parts'][0]['function_response']['response']}")"""
    





    # If verbose flag is present, print the user prompt and number of tokens used
    """if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        # Print number of tokens used
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")"""












