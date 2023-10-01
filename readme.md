# Лабораторная работа №2

## Инференс и обучение НС

В рамках данной лабораторной работы предлагается построить два пайплайна:

1. Пайплайн, который позволяет получить предсказания для исходных данных с помощью некоторой модели.
2. Пайплайн, который позволяет обучить или дообучить целевую модель.

Для построения такого пайплайна воспользуемся следующими инструментами:

- Apache Airflow

## Подготовка к выполнению задания

Для выполнения лабораторной работы рекомендуется использовать докер контейнеры из подготовительного репозитория: https://github.com/ssau-data-engineering/Prerequisites/tree/main

## Задание на лабораторную работу

### Пайплайн для инференса данных

В рамках данного задания предлагается построить пайплайн, который реализует систему "Автоматического распознавания речи" для видеофайлов.

Построенный пайплайн будет выполнять следующие действия поочередно:

1. Производить мониторинг целевой папки на предмет появления новых видеофайлов.
2. Извлекать аудиодорожку из исходного видеофайла.
3. Преобразовывать аудиодорожку в текст с помощью нейросетевой модели.
4. Формировать конспект на основе полученного текста.
5. Формировать выходной .pdf файл с конспектом.

### Пайплайн для обучения модели

В рамках данного задания предлагается построить пайплайн, который реализует систему автоматического обучения/дообучения нейросетевой модели.

Предлагается самостоятельно выбрать набор данных и модель для обучения. Например, можно реализовать пайплайн для обучения модели, которую вы планируете использовать в вашей НИР или ВКРМ. Это также позволит вам добавить отдельный пункт в ваш отчет.

Итак, пайплайн будет выполнять следующие действия:

1. Читать набор файлов из определенного источника (файловой системы, сетевого интерфейса и т.д.).
2. Формировать пакет данных для обучения модели.
3. Обучать модель.
4. Сохранять данные результатов обученя (логи, значения функции ошибки) в текстовый файл

Для успешного выполнения задания необходимо продемонстрировать успешность обучения модели и приложить файл .ipynb, в котором продемонстрирован процесс инференса данной модели.

## Сдача лабораторной работы

Для успешной сдачи лабораторной работы ваш репозиторий должен содержать следующее:

1. Отчет, описывающий этапы выполнения работы (скриншоты, описание встреченных проблем и их решения приветствуются) в формате .pdf или .md.
2. Программный код, реализующий пайплайны.
3. Открыт Pull Request в данный репозиторий.

## Пример

Примеры далее отображают возможную конфигурацию пайплайнов с использованием `DockerOperator`

### Пайплайн для инференса


```python
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'audio_to_text_to_summary_to_pdf',
    default_args=default_args,
    description='DAG for extracting audio, transforming to text, summarizing, and saving as PDF',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,  # Interval to check for new files (in seconds)
    filepath='/path/to/input_video',  # Target folder to monitor
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='ffmpeg_image',
    command='ffmpeg -i input_video.mp4 -vn audio.wav',
    volumes=['/path/to/input_video:/input_video', '/path/to/output_folder:/output'],
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='ml_model_image',
    command='python audio_to_text.py --input audio.wav --output text.txt',
    volumes=['/path/to/audio:/audio', '/path/to/text:/text'],
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='ml_model_image',
    command='python summarize_text.py --input text.txt --output summary.txt',
    volumes=['/path/to/text:/text', '/path/to/summary:/summary'],
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='ml_model_image',
    command='python save_to_pdf.py --input summary.txt --output result.pdf',
    volumes=['/path/to/summary:/summary', '/path/to/output_folder:/output'],
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf
```

### Пайплайн для обучения НС

```python
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'data_engineering_lab_2',
    default_args=default_args,
    description='DAG for data engineering lab 2: training a neural network',
    schedule_interval=None,
)

read_data = DockerOperator(
    task_id='read_data',
    image='read_data_image',
    command='python read_data.py --input /data --output /prepared_data',
    volumes=['/path/to/input_folder:/data', '/path/to/output_folder:/prepared_data'],
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='train_model_image',
    command='python train_model.py --input /prepared_data --output /trained_model',
    volumes=['/path/to/prepared_data:/prepared_data', '/path/to/output_folder:/trained_model'],
    dag=dag,
)

read_data >> train_model

```

## FAQ

- В рамках работы рекомендуется использовать именно `DockerOperator` по следующему ряду причин:
    1. **Портативность и независимость от окружения**: Docker позволяет упаковать все зависимости, включая версии программного обеспечения, библиотеки и конфигурацию, в контейнер. Это гарантирует, что ваша задача будет выполняться в одинаковом окружении, независимо от того, где она запускается.
    2. **Изоляция**: Каждая задача выполняется в собственном контейнере, что обеспечивает изоляцию ресурсов и предотвращает взаимное влияние между задачами. Это особенно полезно, когда задачи требуют разных версий программного обеспечения или библиотек.
    3. **Масштабируемость**: Docker позволяет запускать и масштабировать задачи параллельно, а также легко управлять пакетами данных и моделями. Это особенно полезно при обработке больших объемов данных или при обучении моделей на кластере.
    4. **Управление зависимостями**: Docker позволяет легко управлять зависимостями и версиями программного обеспечения. Вы можете создать образ контейнера, содержащий все необходимые зависимости, и использовать его для запуска задачи без необходимости установки и настройки всех зависимостей на целевой системе.

- Для работы с видеозаписями, в нашем случае для эксопрта аудиодорожки в отдельный файл рекомендуется использовать
утилиту `ffmpeg`

- Для преобразования аудиозаписи в текст вы можете использовать следующую модель: <https://huggingface.co/openai/whisper-small>
  Данная модель способна преобразовывать в речь с различных языков, в том числе и русского.
  *Однако вы не ограничены в применении лишь этой модели.*

- Для составления конспекта по тексту вы можете использовать следующую модель: <https://huggingface.co/slauw87/bart_summarisation>
  К сожалению **небольших** моделей способных к анализу русского крайне мало и работают они крайне не эффективно. 
  Поэтому в рамках лабораторной работы предлагается анализировать **англоязычную** речь.
  *Однако если ваше вычислительное устройство или кластер позволяют запустить большую мультимодальную языковую модель (LLM), вы можете попробовать составлять конспекты и для русскоязычных текстов.*

- Для реализации `DockerOperator` для работы с моделями трансформеров вы можете использовать множество разных подходов:
  1. Использовать API HuggingFace
        ```python
        import requests
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        def query(filename):
            with open(filename, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            return response.json()

        output = query("sample1.flac")
        ```
    2. Использовать библиотеку [`transformers`](https://github.com/huggingface/transformers) и собрать собственный образ
    3. Найти готовый образ например <https://hub.docker.com/r/onerahmet/openai-whisper-asr-webservice>

