# components/dialog_manager.py - С ОГРАНИЧЕНИЕМ ДЛИНЫ
import random
from collections import defaultdict

class ResponseLengthController:
    def __init__(self):
        self.max_response_length = 120  # Максимальная длина ответа пользователя
        self.max_question_length = 80   # Максимальная длина вопроса AI
    
    def truncate_response(self, text):
        """Ограничивает длину ответа пользователя"""
        if len(text) <= self.max_response_length:
            return text
        # Обрезаем до максимальной длины и добавляем многоточие
        return text[:self.max_response_length-3] + "..."
    
    def truncate_question(self, text):
        """Ограничивает длину вопроса AI"""
        if len(text) <= self.max_question_length:
            return text
        # Обрезаем до максимальной длины и добавляем вопросительный знак
        return text[:self.max_question_length-3] + "?"

class KnowledgeGraph:
    def __init__(self):
        self.graph = {
            "technology": {
                "name": "Технологии",
                "questions": [
                    "Что думаете о будущем искусственного интеллекта?",
                    "Какими умными устройствами вы пользуетесь?",
                    "Как технологии изменили вашу работу?",
                    "Что вас беспокоит в развитии технологий?"
                ],
                "keywords": ["технолог", "гаджет", "ии", "смартфон", "компьютер"]
            },
            
            "science": {
                "name": "Наука", 
                "questions": [
                    "Какие научные открытия последних лет вас удивили?",
                    "Как вы относитесь к генной инженерии?",
                    "Что вас впечатляет в изучении космоса?",
                    "Какие направления в медицине кажутся перспективными?"
                ],
                "keywords": ["наук", "открыт", "космос", "медицин", "ген"]
            }
        }

class KnowledgeBasedDialogManager:
    def __init__(self):
        self.knowledge_graph = KnowledgeGraph()
        self.used_questions = set()
        self.current_topic = None
        self.last_question = ""
        self.length_controller = ResponseLengthController()

    def generate_user_response(self, question, topic):
        """Генерирует логичный ответ пользователя, связанный с конкретным вопросом"""
        self.last_question = question
        question_lower = question.lower()
        
        # Контекстные ответы на основе конкретных вопросов
        if "искусственного интеллекта" in question_lower:
            response = "Думаю, ИИ сильно изменит многие области, особенно медицину и образование. Но важно разработать этические нормы для его использования."
        
        elif "умными устройствами" in question_lower:
            response = "Пользуюсь смартфоном, умными часами и системой умного дома. Особенно ценю возможность удаленного контроля за домашними приборами."
        
        elif "технологии изменили вашу работу" in question_lower:
            response = "Технологии позволили работать удаленно, автоматизировали рутинные задачи и ускорили обмен информацией с коллегами."
        
        elif "беспокоит в развитии технологий" in question_lower:
            response = "Немного беспокоюсь о конфиденциальности данных и растущей зависимости людей от цифровых устройств."
        
        elif "научные открытия" in question_lower:
            response = "Недавно читал о новых методах редактирования генома и открытии экзопланет. Поражает, как быстро развивается наука."
        
        elif "генной инженерии" in question_lower:
            response = "Считаю, что генная инженерия имеет огромный потенциал для лечения заболеваний, но требует строгого регулирования."
        
        elif "изучении космоса" in question_lower or "космос" in question_lower:
            response = "Впечатляет масштаб исследований - от поиска экзопланет до изучения черных дыр. Особенно интересны миссии по исследованию Марса."
        
        elif "медицине" in question_lower:
            response = "Персонализированная медицина и иммунотерапия кажутся наиболее перспективными направлениями в современной медицине."
        
        else:
            # Фолбэк ответ
            response = "Это интересный вопрос. Мне нравится обсуждать такие темы."
        
        # Ограничиваем длину ответа
        response = self.length_controller.truncate_response(response)
        return response

    def get_next_question(self, user_response=""):
        """Генерирует следующий вопрос, избегая повторений и чередуя темы"""
        
        # Определяем следующую тему (чередуем или выбираем новую)
        available_topics = list(self.knowledge_graph.graph.keys())
        
        if self.current_topic and len(available_topics) > 1:
            # Убираем текущую тему из доступных
            available_topics.remove(self.current_topic)
            next_topic = random.choice(available_topics)
        else:
            next_topic = random.choice(available_topics)
        
        # Получаем доступные вопросы по выбранной теме
        topic_info = self.knowledge_graph.graph.get(next_topic)
        if not topic_info:
            next_topic = random.choice(available_topics)
            topic_info = self.knowledge_graph.graph.get(next_topic)
        
        available_questions = [q for q in topic_info["questions"] if q not in self.used_questions]
        
        # Если все вопросы использованы, очищаем историю для этой темы
        if not available_questions:
            self.used_questions = set(q for q in self.used_questions 
                                    if not any(q in topic_info["questions"] for topic_info in self.knowledge_graph.graph.values()))
            available_questions = topic_info["questions"]
        
        # Выбираем вопрос
        if available_questions:
            question = random.choice(available_questions)
            self.used_questions.add(question)
            self.current_topic = next_topic
            
            # Ограничиваем длину вопроса
            question = self.length_controller.truncate_question(question)
            
            return question, next_topic
        
        # Фолбэк
        fallback_question = "Что вас интересует в современных технологиях и науке?"
        fallback_question = self.length_controller.truncate_question(fallback_question)
        return fallback_question, "technology"

# Тест
if __name__ == "__main__":
    dialog_manager = KnowledgeBasedDialogManager()
    print("Тест диалога с ограничением длины:")
    for i in range(4):
        question, topic = dialog_manager.get_next_question()
        print(f"{i+1}. [{topic}] {question}")
        response = dialog_manager.generate_user_response(question, topic)
        print(f"   Ответ: {response}")
        print(f"   Длина вопроса: {len(question)}, Длина ответа: {len(response)}")