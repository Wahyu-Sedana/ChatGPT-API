from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import openai  

load_dotenv()

app = Flask(__name__)
app.use_json = True

openai.api_key = os.getenv('OPEN_AI_KEY')

@app.route('/tanya', methods=['POST'])
def tanya():
    try:
        data = request.get_json(force=True)
        if 'prompt' not in data:
            return jsonify({"success": False, "error": "Field 'prompt' is required"}), 400

        prompt = data['prompt']
        response_data = {"success": False}

        if prompt:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"{prompt}\nA:",
                    temperature=0.2,
                    max_tokens=1500,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=['\n']
                )
                print(response.choices)
                if response:
                    response_data["success"] = True
                    response_data["data"] = response.choices[0].text if response.choices[0].text else 'Jawaban Tidak Ditemukan'
            except Exception as e:
                response_data["error"] = str(e)
                return jsonify(response_data), 500
        else:
            response_data["error"] = "Invalid Parameter"
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
