import json
from modules.telegram_utils import send_telegram_message

PLAN_PATH = "plan.json"

def load_plan():
    with open(PLAN_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_unfinished_tasks(plan_data):
    message = "🛠 *Список незавершённых задач:*
"
    count = 0
    for section, tasks in plan_data.items():
        section_tasks = [t["task"] for t in tasks if not t["done"]]
        if section_tasks:
            message += f"\n📌 *{section.capitalize()}*\n"
            for task in section_tasks:
                count += 1
                message += f"• {task}\n"
    if count == 0:
        message = "✅ Все задачи выполнены!"
    return message

def handle_todo_command():
    plan_data = load_plan()
    msg = get_unfinished_tasks(plan_data)
    send_telegram_message(msg, parse_mode="Markdown")

# для ручного запуска:
if __name__ == "__main__":
    handle_todo_command()