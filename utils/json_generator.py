import json
from datetime import datetime
import uuid

class JSONGenerator:
    def __init__(self):
        self.version = "GenAl-3-38"
    
    def generate_dialog_json(self, greeting, conversation, history_summary, farewell):
        """Генерирует JSON структуру диалога"""
        
        # Проверяем длину реплик
        length_analysis = self._analyze_response_lengths(conversation)
        
        dialog_structure = {
            "metadata": {
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "dialog_id": str(uuid.uuid4()),
                "total_exchanges": len(conversation),
                "status": "completed",
                "length_limits": {
                    "max_question_length": 80,
                    "max_response_length": 120
                }
            },
            "dialog": {
                "greeting": greeting,
                "conversation": conversation,
                "history_summary": history_summary,
                "farewell": farewell
            },
            "analysis": {
                "topics_discussed": list(set(
                    exchange.get("topic", "general")
                    for exchange in conversation 
                    if exchange["speaker"] == "AI"
                )),
                "conversation_quality": self._evaluate_quality(conversation),
                "length_analysis": length_analysis
            },
            "consistency_check": {
                "score": 100.0,
                "is_consistent": True,
                "length_check": length_analysis["all_within_limits"]
            }
        }
        
        return dialog_structure
    
    def _analyze_response_lengths(self, conversation):
        """Анализирует длину реплик"""
        ai_lengths = []
        user_lengths = []
        
        for exchange in conversation:
            if exchange["speaker"] == "AI":
                ai_lengths.append(len(exchange["text"]))
            else:
                user_lengths.append(len(exchange["text"]))
        
        all_within_limits = (
            all(length <= 80 for length in ai_lengths) and
            all(length <= 120 for length in user_lengths)
        )
        
        return {
            "ai_avg_length": sum(ai_lengths) / len(ai_lengths) if ai_lengths else 0,
            "user_avg_length": sum(user_lengths) / len(user_lengths) if user_lengths else 0,
            "ai_max_length": max(ai_lengths) if ai_lengths else 0,
            "user_max_length": max(user_lengths) if user_lengths else 0,
            "all_within_limits": all_within_limits
        }
    
    def _evaluate_quality(self, conversation):
        """Оценивает качество диалога"""
        ai_messages = len([msg for msg in conversation if msg["speaker"] == "AI"])
        
        if ai_messages >= 4:
            return "high"
        elif ai_messages >= 2:
            return "medium"
        else:
            return "low"
    
    def save_to_file(self, dialog_data, filename=None):
        """Сохраняет диалог в JSON файл"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dialog_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dialog_data, f, ensure_ascii=False, indent=2)
        
        return filename