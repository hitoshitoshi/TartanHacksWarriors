from flask import Flask, request, render_template
from openai import OpenAI
import os

client = OpenAI()

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

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