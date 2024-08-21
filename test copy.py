import ollama


chat_messages = []
system_message='You are a helpful assistant.'


# Defining a function to create new messages with specified roles ('user' or 'assistant')
def create_message(message, role):
    return {
        'role': role,
        'content': message
    }

# Starting the main conversation loop
def chat():
    # Calling the ollama API to get the assistant response
    # ollama_response = ollama.chat(model='llama3', stream=True, messages=chat_messages)
    ollama_response = ollama.chat(model='llama3', stream=False, messages=chat_messages)

    # Preparing the assistant message by concatenating all received chunks from the API
    assistant_message = ollama_response['message']['content']
    # for chunk in ollama_response:
    #     assistant_message += chunk['message']['content']
    #     print(chunk['message']['content'], end='', flush=True)

    # Adding the finalized assistant message to the chat log
    print(assistant_message)
    chat_messages.append(create_message(assistant_message, 'assistant'))

# Function for asking questions - appending user messages to the chat logs before starting the `chat()` function
def ask(message):
    chat_messages.append(
        create_message(message, 'user')
    )
    print(f'\n\n--{message}--\n\n')
    chat()

# Sending two example requests using the defined `ask()` function
ask('Desde ahora en adelante, tu nombre es "Robotin".')
print(chat_messages)
ask('Cual es tu nombre?')
print(chat_messages)
