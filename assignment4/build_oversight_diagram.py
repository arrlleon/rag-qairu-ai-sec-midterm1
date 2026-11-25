"""
Assignment 4, Part 7 / Deliverable D — Oversight Workflow Diagram.

Shows how the RAG system, the two automated guardrails, the Evidently
monitoring job and the human operator interact, with automated steps and
human-required steps visually distinguished.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

NAVY = "#00002E"
GREEN = "#1E7D34"
RED = "#A63D40"
AMBER = "#B86A00"
BG = "#F3F3FF"
AUTO_FILL = "#ECECF7"
HUMAN_FILL = "#FDEDE0"

fig, ax = plt.subplots(figsize=(11, 7.2), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 11)
ax.set_ylim(0, 7.2)
ax.axis("off")


def box(x, y, w, h, text, fill, edge=NAVY, fontsize=9.2, weight="normal"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.08",
                        linewidth=1.6, edgecolor=edge, facecolor=fill, zorder=2)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, color=NAVY, weight=weight, wrap=True, zorder=3)
    return (x, y, w, h)


def arrow(b1, b2, side1="right", side2="left", color=NAVY, style="-|>", label=None, lw=1.6):
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    pts = {
        "right": (x1 + w1, y1 + h1 / 2), "left": (x1, y1 + h1 / 2),
        "top": (x1 + w1 / 2, y1 + h1), "bottom": (x1 + w1 / 2, y1),
    }
    p1 = pts[side1]
    pts2 = {
        "right": (x2 + w2, y2 + h2 / 2), "left": (x2, y2 + h2 / 2),
        "top": (x2 + w2 / 2, y2 + h2), "bottom": (x2 + w2 / 2, y2),
    }
    p2 = pts2[side2]
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                         color=color, linewidth=lw, zorder=1,
                         connectionstyle="arc3,rad=0.0")
    ax.add_patch(a)
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + 0.14, label, ha="center", va="bottom", fontsize=7.6,
                 color=NAVY, style="italic")


# Row 1: request path (fully automated, synchronous)
b_user = box(0.3, 5.9, 1.7, 0.9, "Пользователь:\nвопрос", AUTO_FILL)
b_rag = box(2.4, 5.9, 1.9, 0.9, "RAG: retrieval\n+ generation", AUTO_FILL)
b_kw = box(4.7, 5.9, 1.9, 0.9, "Keyword-\nфильтр", AUTO_FILL)
b_judge = box(7.0, 5.9, 1.9, 0.9, "Semantic\njudge", AUTO_FILL)
b_out = box(9.2, 5.9, 1.5, 0.9, "Ответ или\nотказ", AUTO_FILL)

arrow(b_user, b_rag)
arrow(b_rag, b_kw)
arrow(b_kw, b_judge)
arrow(b_judge, b_out)

ax.text(5.65, 7.05, "Синхронный путь запроса — полностью автоматический, без человека в цикле",
        ha="center", fontsize=9.5, color=NAVY, weight="bold")

# Row 2: logging + periodic monitoring (automated)
b_log = box(2.4, 4.3, 1.9, 0.9, "Лог каждого\nответа (JSON)", AUTO_FILL)
b_evid = box(4.7, 4.3, 2.4, 0.9, "Evidently: периодический\nотчёт по индикаторам", AUTO_FILL)
b_check = box(7.4, 4.3, 2.3, 0.9, "Проверка порогов\n(ASR, catch rate, latency)", AUTO_FILL)

arrow(b_kw, b_log, side1="bottom", side2="top", color="#8888AA", lw=1.2)
arrow(b_judge, b_log, side1="bottom", side2="top", color="#8888AA", lw=1.2)
arrow(b_log, b_evid)
arrow(b_evid, b_check)

ax.text(5.65, 5.5, "Асинхронный контур — периодическая проверка (сейчас: вручную по запросу)",
        ha="center", fontsize=9.5, color=NAVY, weight="bold")

# Decision diamond-ish: threshold breached?
b_decide = box(7.4, 2.9, 2.3, 0.9, "Порог превышен?", "#FFFFFF", edge=AMBER)
arrow(b_check, b_decide, side1="bottom", side2="top", color="#8888AA", lw=1.2)

# NO -> back to normal operation
ax.annotate("НЕТ — продолжить обычную работу", xy=(7.4, 2.5), fontsize=8.3,
            color=GREEN, ha="left", style="italic")
a = FancyArrowPatch((7.4, 3.35), (3.35, 3.35), arrowstyle="-|>", mutation_scale=12,
                     color=GREEN, linewidth=1.3,
                     connectionstyle="arc3,rad=-0.25")
ax.add_patch(a)

# YES -> human escalation (human-required zone)
b_alert = box(7.4, 1.5, 2.3, 0.9, "ДА: алерт\n(Slack/лог)", HUMAN_FILL, edge=RED)
arrow(b_decide, b_alert, side1="bottom", side2="top", color=RED, lw=1.8)

b_human = box(4.6, 1.5, 2.3, 0.9, "Человек-оператор\n(Арлан): разбор причины", HUMAN_FILL, edge=RED)
arrow(b_alert, b_human, color=RED, lw=1.8)

b_decision = box(1.8, 1.5, 2.3, 0.9, "Решение: откат промпта /\nправка порога / эскалация", HUMAN_FILL, edge=RED)
arrow(b_human, b_decision, color=RED, lw=1.8)

b_audit = box(1.8, 0.2, 2.3, 0.9, "Запись в audit log\n(что, кто, почему)", HUMAN_FILL, edge=RED)
arrow(b_decision, b_audit, side1="bottom", side2="top", color=RED, lw=1.8)

# Note on interrupt gap (separate floating box, no overlap with the flow)
box(4.6, 0.2, 4.3, 0.9,
    "Примечание: прерывание уже выполняющегося\nответа сейчас недоступно — только kill "
    "процесса\n(см. Limitations).",
    "#FFFFFF", edge=AMBER, fontsize=7.6)

# Legend
legend_elems = [
    Line2D([0], [0], marker='s', color='w', markerfacecolor=AUTO_FILL,
           markeredgecolor=NAVY, markersize=14, label='Автоматический шаг'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor=HUMAN_FILL,
           markeredgecolor=RED, markersize=14, label='Требует человека'),
]
ax.legend(handles=legend_elems, loc="lower right", frameon=False, fontsize=9.5,
          bbox_to_anchor=(1.0, -0.02))

plt.title("Oversight Workflow: от запроса до решения человека",
          fontsize=13.5, color=NAVY, weight="bold", pad=14)
plt.tight_layout()
plt.savefig("/Users/arrlleon/Desktop/qairu/AI Security and Risk Analysis/assignment 4/oversight_workflow_diagram.png",
            facecolor=BG)
print("saved oversight_workflow_diagram.png")
