from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Replace "your_api_key_here" with your actual OpenAI API key
openai.api_key = 'your_api_key_here'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    prompt = request.form['prompt']
    response = openai.Completion.create(
      engine="text-davinci-003", # Adjust based on available models and your specific needs
      prompt=prompt,
      temperature=0.7,
      max_tokens=150,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    return render_template('index.html', generated_text=response.choices[0].text.strip())

if __name__ == '__main__':
    app.run(debug=True)
