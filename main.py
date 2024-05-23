from fastapi import FastAPI
from chunks import Chunk
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# для выполнения ДЗ pro необходимо поменять только файл main.py
# база данных должна быть в текстовом формате

# инициализация индексной базы
chunk = Chunk(path_to_base="ПРАВИЛА СТРАХОВАНИЯ ОТВЕТСТВЕННОСТИ АЭРОПОРТОВ И АВИАЦИОННЫХ ТОВАРОПРОИЗВОДИТЕЛЕЙ.txt")

# загружаем промт
with open("Промпт.txt", 'r', encoding='utf-8') as file:
    default_system = file.read()

# класс с типами данных параметров 
class Item(BaseModel): 
    text: str

# создаем объект приложения
app = FastAPI()

# добавляем переменную для подсчета запросов
app.counter = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# функция обработки get запроса + декоратор 
@app.get("/")
def read_root():
    return {"message": "answer"}

# функция обработки get запроса для подсчета количества обращений
@app.get("/api/num_requests")
def read_root():
    return {"num_requests": app.counter}

# функция обработки post запроса + декоратор 
@app.post("/api/get_answer")
def get_answer(question: Item):
    answer = chunk.get_answer(query=question.text, system=default_system)
    app.counter+=1
    return {"message": answer}

