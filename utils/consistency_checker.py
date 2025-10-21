# utils/consistency_checker.py - УПРОЩЕННАЯ ВЕРСИЯ
class ConsistencyChecker:
    def __init__(self):
        self.consistency_rules = [
            self.check_topic_consistency,
            self.check_temporal_consistency
        ]
    
    def check_dialog_consistency(self, dialog_data):
        """Проверяет весь диалог на согласованность"""
        results = {
            "is_consistent": True,
            "checks": {},
            "issues": [],
            "score": 0
        }
        
        total_checks = 0
        passed_checks = 0
        
        for rule in self.consistency_rules:
            check_name = rule.__name__
            is_consistent, message = rule(dialog_data)
            
            results["checks"][check_name] = {
                "passed": is_consistent,
                "message": message
            }
            
            total_checks += 1
            if is_consistent:
                passed_checks += 1
            else:
                results["issues"].append(f"{check_name}: {message}")
                results["is_consistent"] = False
        
        # Расчет общего score
        if total_checks > 0:
            results["score"] = round((passed_checks / total_checks) * 100, 2)
        
        return results
    
    def check_topic_consistency(self, dialog_data):
        """Проверяет согласованность тем в диалоге"""
        conversation = dialog_data["dialog"]["conversation"]
        ai_messages = [msg for msg in conversation if msg["speaker"] == "AI"]
        
        if len(ai_messages) < 2:
            return True, "Недостаточно сообщений для анализа тем"
        
        # Анализ смены тем
        topic_changes = 0
        previous_topic = ai_messages[0].get("topic", "unknown")
        
        for i in range(1, len(ai_messages)):
            current_topic = ai_messages[i].get("topic", "unknown")
            if current_topic != previous_topic:
                topic_changes += 1
            previous_topic = current_topic
        
        # Если слишком много смен тем - возможна несогласованность
        if topic_changes > len(ai_messages) * 0.6:  # Более 60% смен
            return False, f"Слишком частые смены тем: {topic_changes} раз"
        
        return True, f"Темы меняются плавно ({topic_changes} смен)"
    
    def check_temporal_consistency(self, dialog_data):
        """Проверяет временную согласованность"""
        conversation = dialog_data["dialog"]["conversation"]
        
        # Проверка порядка реплик (AI -> User -> AI -> User ...)
        expected_speaker = "AI"
        violations = 0
        
        for exchange in conversation:
            if exchange["speaker"] != expected_speaker:
                violations += 1
            expected_speaker = "User" if expected_speaker == "AI" else "AI"
        
        if violations > len(conversation) * 0.3:  # Более 30% нарушений
            return False, f"Нарушен порядок реплик: {violations} нарушений"
        
        return True, f"Порядок реплик соблюден"