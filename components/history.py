class HistoryManager:
    def __init__(self):
        self.conversation_history = []
        self.discussed_topics = set()
    
    def add_exchange(self, speaker, text, exchange_type):
        """Добавляет реплику в историю диалога"""
        exchange = {
            "speaker": speaker,
            "text": text,
            "type": exchange_type
        }
        self.conversation_history.append(exchange)
        
        # Обновляем обсуждаемые темы для вопросов AI
        if speaker == "AI" and exchange_type == "question":
            if "технолог" in text.lower() or "ии" in text.lower() or "гаджет" in text.lower():
                self.discussed_topics.add("technology")
            elif "наук" in text.lower() or "космос" in text.lower() or "медицин" in text.lower():
                self.discussed_topics.add("science")
    
    def get_history_summary(self):
        """Создает краткую сводку истории диалога"""
        if not self.conversation_history:
            return "Диалог еще не начался"
        
        ai_messages = len([msg for msg in self.conversation_history if msg["speaker"] == "AI"])
        user_messages = len([msg for msg in self.conversation_history if msg["speaker"] == "User"])
        
        topics_text = ", ".join(self.discussed_topics) if self.discussed_topics else "разные темы"
        
        summary = (
            f"За время диалога мы обменялись {len(self.conversation_history)} репликами "
            f"(AI: {ai_messages}, Пользователь: {user_messages}). "
            f"Обсуждали темы: {topics_text}."
        )
        
        return summary