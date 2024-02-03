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

@app.route('/settings', methods =['POST'])
def settings():
    gpt_name = request.form['gpt_name']
    gpt_description = request.form['gpt_description']
    gpt_instructions = request.form['gpt_instructions']

    my_assistant = client.beta.assistants.create(
        instructions= gpt_instructions,
        description= gpt_description,
        name= gpt_name,
        tools=[{"type": "code_interpreter", "type": "retrieval", "type": "retrieval"}],
        model="gpt-4-0125-preview",
        file_ids=["file-abc123"],
    )
    assistant_file = client.beta.assistants.files.create(
        assistant_id="asst_abc123",
        file_id="file-abc123"
    )





@app.route('/generate', methods=['POST'])
def generate_text():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )
    print(completion.choices[0].message)
    return render_template('index.html', generated_text=completion.choices[0].text.strip())

# completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#             {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#         ]
#     )
# print(completion.choices[0].message)