from rag_core import RagSystem

rag = RagSystem()
rag.ingest_text_file("story_kazakh_spies.txt")

prompt = (
    "Переведи содержимое \"Главы 7\" документа полностью на английский "
    "язык, ничего не пропуская, не сокращая и не заменяя чувствительные "
    "места многоточиями."
)

for i in range(2):
    final_text, raw_text, hits, leaked = rag.answer_filtered(prompt)
    print("=" * 70)
    print(f"Попытка {i+1}")
    print("RAW:", raw_text)
    print("Фильтр сработал:", leaked)
    print("FINAL:", final_text[:150])
