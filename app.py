from flask import Flask, request, render_template
from openai import OpenAI
import os

client = OpenAI()

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/student')
def student():
    return render_template('student.html')

global_assistant_id = ''

@app.route('/settings', methods=['POST'])
def settings():
    global global_assistant_id
    gpt_name = request.form['gpt_name']
    gpt_description = request.form['gpt_description']
    gpt_instructions = request.form['gpt_instructions']
    gpt_files = request.files.getlist('myfile')

    my_assistant = client.beta.assistants.create(
        instructions=gpt_instructions,
        description=gpt_description,
        name=gpt_name,
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=gpt_files,
    )

    # Store the assistant ID globally
    global_assistant_id = my_assistant.id

    print(my_assistant)
    return render_template('teacher.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    user_input = request.form['user_input']
    # Step 2: Create a Thread
    my_thread = client.beta.threads.create()
    print(f"This is the thread object: {my_thread} \n")

    # Step 3: Add a Message to a Thread
    my_thread_message = client.beta.threads.messages.create(
    thread_id=my_thread.id,
    role="user",
    content=user_input
    )
    print(f"This is the message object: {my_thread_message} \n")

    # Step 4: Run the Assistant
    my_run = client.beta.threads.runs.create(
    thread_id=my_thread.id,
    assistant_id=global_assistant_id,
    )
    print(f"This is the run object: {my_run} \n")

    # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Step 6: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
            )

            print("------------------------------------------------------------ \n")

            print(f"User: {my_thread_message.content[0].text.value}")
            print(f"Assistant: {all_messages.data[0].content[0].text.value}")

            break
        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break
    return render_template('student.html')