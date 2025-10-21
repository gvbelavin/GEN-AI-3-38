# main.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from components.greeting import get_greeting
from components.farewell import get_farewell
from components.dialog_manager import KnowledgeBasedDialogManager
from components.history import HistoryManager
from utils.json_generator import JSONGenerator
import time

def main():
    print("УМНАЯ ДИАЛОГ-СИСТЕМА С ГРАФОМ ЗНАНИЙ")
    print("=" * 50)
    
    # Инициализация
    greeting = get_greeting()
    farewell = get_farewell()
    dialog_manager = KnowledgeBasedDialogManager()
    history_manager = HistoryManager()
    json_generator = JSONGenerator()
    
    # Начало диалога
    print(f"{greeting}\n")
    history_manager.add_exchange("AI", greeting, "greeting")
    conversation_data = []
    
    # Генерация диалога (4 вопроса)
    for i in range(4):
        question, topic = dialog_manager.get_next_question()
        print(f"Вопрос {i+1} [{topic}]: {question}")
        
        history_manager.add_exchange("AI", question, "question")
        conversation_data.append({
            "speaker": "AI", 
            "type": "question", 
            "text": question,
            "topic": topic
        })
        
        # Логичный ответ пользователя
        time.sleep(1)
        user_response = dialog_manager.generate_user_response(question, topic)
        print(f"Ответ: {user_response}\n")
        
        history_manager.add_exchange("User", user_response, "response")
        conversation_data.append({
            "speaker": "User", 
            "type": "response", 
            "text": user_response,
            "topic": topic
        })
    
    # Завершение диалога
    time.sleep(1)
    print(f"{farewell}")
    history_manager.add_exchange("AI", farewell, "farewell")
    
    # Результаты
    history_summary = history_manager.get_history_summary()
    print(f"\n{history_summary}")
    
    # Анализ тематического разнообразия
    topics = list(set([msg.get("topic", "unknown") for msg in conversation_data if msg["speaker"] == "AI"]))
    print(f"Затронутые темы: {', '.join(topics)}")
    
    # Сохранение в JSON
    json_data = json_generator.generate_dialog_json(
        greeting=greeting,
        conversation=conversation_data,
        history_summary=history_summary,
        farewell=farewell
    )
    
    filename = json_generator.save_to_file(json_data)
    print(f"Файл: {filename}")
    
    # Проверка качества
    consistency = json_data["consistency_check"]
    print(f"Согласованность: {consistency['score']}%")

if __name__ == "__main__":
    main()