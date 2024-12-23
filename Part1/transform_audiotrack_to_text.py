import requests
import json

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
API_TOKEN = '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'
headers = {"Authorization": f"Bearer {API_TOKEN}"}

try:
    with open('/data/audio.aac', "rb") as f:
        data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)

        # Проверка статуса ответа
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
        else:
            result = response.json()
            # Проверка наличия ключа 'text'
            if 'text' in result:
                text_from_audio = result['text']
                with open("/data/text.txt", "w+") as text_file:
                    text_file.write(text_from_audio)
            else:
                print("Error: 'text' key not found in the response.")
                print(f"Response content: {json.dumps(result, indent=2)}")  # Логирование полного ответа
except Exception as e:
    print(f"An error occurred: {e}")
