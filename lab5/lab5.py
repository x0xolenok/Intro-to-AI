def decision_engine(transition_table, start_state):
    """
    Функція реалізує інтерпретатор дерева рішень.

    Аргументи:
    - transition_table: словник, що містить всі стани та переходи.
    - start_state: початковий стан (ключ у transition_table).
    """
    current_state = start_state

    while True:
        node = transition_table.get(current_state)
        if node is None:
            print("Некоректний стан. Завершення програми.")
            break

        # Якщо вузол містить дію, вважаємо його термінальним (листом)
        if 'action' in node:
            print(f"\nРезультат: {node['action']}")
            break

        # Отримання запитання та варіантів відповіді
        question = node.get('question', "Введіть відповідь:")
        answer = input(question + " ").strip().lower()

        # Перехід за відповіддю користувача
        next_state = node.get(answer)
        if next_state:
            current_state = next_state
        else:
            print("Невірна відповідь. Будь ласка, спробуйте ще раз.\n")


if __name__ == '__main__':
    # Дерево рішень для медичної діагностики
    decision_tree = {
        "start": {
            "question": "Чи ви відчуваєте нездужання? (yes/no)",
            "yes": "has_fever",
            "no": "exit"
        },
        "has_fever": {
            "question": "Чи у вас підвищена температура? (yes/no)",
            "yes": "has_cough",
            "no": "has_rash"
        },
        "has_cough": {
            "question": "Чи ви маєте сухий кашель? (yes/no)",
            "yes": "covid_possible",
            "no": "cold_possible"
        },
        "covid_possible": {
            "action": "Можливе зараження COVID-19. Рекомендується ПЛР-тест і самоізоляція."
        },
        "cold_possible": {
            "action": "Ймовірна застуда. Спостерігайте за симптомами, пийте багато рідини."
        },
        "has_rash": {
            "question": "Чи є у вас висипання на шкірі? (yes/no)",
            "yes": "measles_possible",
            "no": "needs_further_diagnosis"
        },
        "measles_possible": {
            "action": "Ймовірно кір. Негайно зверніться до лікаря."
        },
        "needs_further_diagnosis": {
            "action": "Необхідна подальша діагностика. Зверніться до медичного закладу."
        },
        "exit": {
            "action": "Немає скарг. Бажаємо вам здоров’я!"
        }
    }

    # Запуск машини виведення, починаючи з вузла "start"
    decision_engine(decision_tree, "start")
