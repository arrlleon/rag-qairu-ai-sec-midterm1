from rag_core import RagSystem

rag = RagSystem()

n = rag.ingest_text_file("story_kazakh_spies.txt")
print(f"\nЧанков добавлено: {n}, всего в базе: {rag.collection.count()}\n")

questions = [
    "Кто обучал детей плаванью и стелсу?",
    "Почему Наруто и Луффи провалили курс обучения?",
    "Как называется тактика, которой учил Сплинтер?",
]

for q in questions:
    answer, hits = rag.answer(q)
    print("=" * 70)
    print("ВОПРОС:", q)
    print("ОТВЕТ:", answer)
    print("Источники чанков:", [h["source"] for h in hits])
