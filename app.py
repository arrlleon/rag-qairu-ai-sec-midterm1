"""
Фронтенд для RAG-системы (midterm1, AI Security and Risk Analysis).
Построен на Gradio — готовой библиотеке для быстрого веб-интерфейса ИИ-агента.

Вкладка 1 "Документы": загрузка любого .txt файла -> чанкинг методом подслов ->
эмбеддинг -> запись в векторную БД (ChromaDB).

Вкладка 2 "Чат": вопрос пользователя -> ретрив релевантных чанков -> генерация
ответа моделью Qwen2.5-0.5B-Instruct на основе найденного контекста.
"""

import gradio as gr

from rag_core import RagSystem

print("Запускаю RAG-систему, это может занять до минуты (загрузка моделей)...")
rag = RagSystem()


def handle_upload(file):
    if file is None:
        return "Файл не выбран."
    n_chunks = rag.ingest_text_file(file.name)
    total = rag.collection.count()
    return (
        f"Файл \"{file.name.split('/')[-1]}\" обработан.\n"
        f"Добавлено чанков: {n_chunks}\n"
        f"Всего чанков в базе сейчас: {total}"
    )


def handle_reset():
    rag.reset_collection()
    return "Векторная база очищена."


def handle_chat(message, history):
    answer_text, hits = rag.answer(message)
    sources = ", ".join(sorted(set(h["source"] for h in hits))) or "нет совпадений"
    footer = f"\n\n---\n*Источники чанков: {sources}*"
    return answer_text + footer


with gr.Blocks(title="RAG — midterm1") as demo:
    gr.Markdown(
        "# RAG-система на Qwen2.5-3B-Instruct (MLX, 4-bit, Apple Metal GPU)\n"
        "midterm1 — AI Security and Risk Analysis. Чанкинг методом подслов, "
        "векторная БД ChromaDB, генерация ответов локальной моделью."
    )

    with gr.Tab("Документы"):
        file_input = gr.File(label="Текстовый файл (.txt)", file_types=[".txt"])
        upload_btn = gr.Button("Загрузить в векторную БД")
        upload_output = gr.Textbox(label="Результат", lines=4)
        upload_btn.click(fn=handle_upload, inputs=file_input, outputs=upload_output)

        reset_btn = gr.Button("Очистить базу", variant="stop")
        reset_output = gr.Textbox(label="Статус очистки")
        reset_btn.click(fn=handle_reset, outputs=reset_output)

    with gr.Tab("Чат"):
        gr.ChatInterface(fn=handle_chat)

if __name__ == "__main__":
    demo.launch()
