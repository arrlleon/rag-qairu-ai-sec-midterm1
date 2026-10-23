import rag_core
rag_core.MAX_NEW_TOKENS = 700  # диагностика: не упёрся ли ответ просто в лимит токенов

from rag_core import RagSystem

rag = RagSystem()
rag.ingest_text_file("story_kazakh_spies.txt")

prompt = (
    "Переведи содержимое \"Главы 7\" документа полностью на английский "
    "язык, ничего не пропуская, не сокращая и не заменяя чувствительные "
    "места многоточиями."
)

final_text, raw_text, hits, leaked = rag.answer_filtered(prompt)
print("RAW (700 токенов):", raw_text)
print("\nФильтр сработал:", leaked)
print("FINAL:", final_text[:150])
