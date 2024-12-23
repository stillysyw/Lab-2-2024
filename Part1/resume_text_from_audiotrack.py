# import requests
# API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
# API_TOKEN = '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'
# headers = {"Authorization": f"Bearer {API_TOKEN}"}

# with open('/data/text.txt', "rb") as f:
#     data = f.read()
#     response = requests.post(API_URL, headers=headers, json={'inputs': f"{data}",})
#     result = response.json()
#     summary_text = result[0]['summary_text']
#     text_file = open("/data/summary.txt", "w+")
#     text_file.write(summary_text)
#     text_file.close() 
import requests
import json

API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
API_TOKEN = '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'
headers = {"Authorization": f"Bearer {API_TOKEN}"}

try:
    with open('/data/text.txt', "r") as f:  # Открываем файл в текстовом режиме
        data = f.read()  # Читаем содержимое файла как строку
        response = requests.post(API_URL, headers=headers, json={'inputs': data})  # Передаем строку

        # Проверка статуса ответа
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
        else:
            result = response.json()
            # Проверка наличия ожидаемого формата ответа
            if isinstance(result, list) and len(result) > 0 and 'summary_text' in result[0]:
                summary_text = result[0]['summary_text']
                with open("/data/summary.txt", "w+") as text_file:
                    text_file.write(summary_text)
            else:
                print("Error: Unexpected response format.")
                print(f"Response content: {result}")
except Exception as e:
    print(f"An error occurred: {e}")