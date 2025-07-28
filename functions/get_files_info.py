import os
from google import generativeai as genai
from google.genai import types





from functions.run_python import run_python_file



# define working_directory as the current working directory
working_directory = os.getcwd()

directory = None # Default to None, which will list the working directory itself


def get_files_info(working_directory, directory=None):
	# if directory is None, default to listing the working directory itself
	if directory is None:
		directory = working_directory

	# use os.path.join() to ensure the directory is relative to the working directory
	
	
	# Ensure the working directory and directory are absolute paths
	parent_dir = os.path.abspath(working_directory)
	child_dir = os.path.abspath(directory)

	try:
		common = os.path.commonpath([parent_dir, child_dir])
		if common != parent_dir:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	
	if not os.path.isdir(directory):
		return f'Error: "{directory}" is not a directory'

	try:
		# Build and return a string of the contents of the directory
		files = os.listdir(directory)
		files_info = []
		# Determine file size and whether it is a directory or file
		for file in files:
			file_path = os.path.join(directory, file)
			file_size = os.path.getsize(file_path)
			if os.path.isdir(file_path):
				files_info.append(f"- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}")
			else:
				files_info.append(f"- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}")
		
		# Combine the file information into a single string
		files_info_str = "\n".join(files_info)
		
			# Return the formatted string in this format: - <name>: file_size=<size> bytes, is_dir=<True/False>
		return files_info_str

	except Exception as e:
		return f'Error: {e}'
	
# Create function to get file content
def get_file_content(working_directory, file_path):

	abs_path = os.path.join(working_directory, file_path)

	# Ensure the working directory and directory are absolute paths
	working_dir = os.path.abspath(working_directory)
	file_path_dir = os.path.abspath(abs_path)

	# Check if file_path is within working_directory using os.path.commonpath
	try:
		common = os.path.commonpath([working_dir, file_path_dir])
		if common != working_dir:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	
	
	
	# if file_path is not a file, return an error message
	if not os.path.isfile(abs_path):
		return f'Error: File not found or is not a regular file: "{file_path}"'
	
	# read the file and return its content as string. Always return. if file is longer than 1000 characters, truncate it to 1000 characters and append message
	try:
		with open(abs_path, 'r') as file:
			content = file.read()
			if len(content) > 10000:
				return f"{content[:10000]}[...File \"{file_path}\" truncated at 10000 characters]"
			return content
	except Exception as e:
		return f'Error: {e}'

# Write and overwrite files
def write_file(working_directory, file_path, content):
	abs_path = os.path.join(working_directory, file_path)

	# Ensure the working directory and directory are absolute paths
	working_dir = os.path.abspath(working_directory)
	file_path_dir = os.path.abspath(abs_path)

	# Check if file_path is within working_directory using os.path.commonpath
	try:
		common = os.path.commonpath([working_dir, file_path_dir])
		if common != working_dir:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	
	# if file_path doesn't exist, create it. If there is an error, return an error message
	if not os.path.exists(os.path.dirname(abs_path)):
		try:
			os.makedirs(os.path.dirname(abs_path))
		except Exception as e:
			return f'Error: Could not create directory for "{file_path}": {e}'

	# write the content to the file, overwriting it if it exists
	try:
		with open(abs_path, 'w') as file:
			file.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f'Error: Could not write to file "{file_path}": {e}'
	

# Use types.FunctionDeclaration to build teh "declaration" or "schema" of the function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# build schema_get_file_content function
schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="Retrieves the content of a specified file, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path to the file to retrieve content from, relative to the working directory.",
			),
		},
	),
)

# build schema_run_python_file function
schema_run_python_file = types.FunctionDeclaration(
	name="run_python_file",
	description="runs a Python file and returns its output, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path to the Python file to run, relative to the working directory.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="Executable Python code to run. If provided, this will override the file_path parameter.",
			),
		},
	),
)

# build schema_write_file function
schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Writes content to a specified file, creating the file if it does not exist, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path to the file to write to, relative to the working directory.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The content to write to the file.",
			),
		},
	),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
		schema_get_file_content,
		schema_run_python_file,
		schema_write_file,
    ]
)



# write a function to handle function calls
def call_function(function_call_part, verbose=False):
	# if verbose, print function_call_part and args
	if verbose:
		print(f"Calling function: {function_call_part.name}({function_call_part.args})")
	else:
		# just print the name
		print(f" - Calling function: {function_call_part.name}")

	# Add working_directory to args
	args_with_working_dir = dict(function_call_part.args)  # Convert to regular dict
	args_with_working_dir["working_directory"] = "./calculator"

	# Call the function based on the function_call_part.name
	if function_call_part.name == "get_files_info":
		result = get_files_info(**args_with_working_dir)
	elif function_call_part.name == "get_file_content":
		result = get_file_content(**args_with_working_dir)
	elif function_call_part.name == "run_python_file":
		result = run_python_file(**args_with_working_dir)
	elif function_call_part.name == "write_file":
		result = write_file(**args_with_working_dir)
	else:
		# return genai.types.Content 
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_call_part.name,
					response={"error": f"Unknown function: {function_call_part.name}"},
				)
			],
		)

	# Return the result as genai.types.Content
	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=function_call_part.name,
				response={"result": result}
			)
		],

	)

# Handle function calls and return the result

def handle_function_calls(response, verbose):
	for candidate in response.candidates:
		for part in candidate.content.parts:
			if hasattr(part, "function_call") and part.function_call:
				result = call_function(part.function_call, verbose)

				# Check if result has the expected structure
				# Handle both object and dictionary formats
				if result:
					if hasattr(result, 'parts'):
						# Object format
						if result.parts and result.parts[0].function_response:
							if verbose:
								#print(f"-> {result.parts[0].function_response.response}")
								pass
					elif isinstance(result, dict) and 'parts' in result:
						# Dictionary format
						if result['parts'] and 'function_response' in result['parts'][0]:
							#if verbose:
								#print(f"-> {result['parts'][0]['function_response']['response']}")
							pass
					else:
						raise Exception("Function call failed to return proper response")
					return result
				else:
					raise Exception("Function call failed to return proper response")
	return None  # If no function calls were made, return None

