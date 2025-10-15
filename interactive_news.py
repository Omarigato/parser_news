#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерактивный парсер новостей
Позволяет задавать вопросы и получать новости по конкретным темам
"""

import g4f
from news_parser import NewsParser
import re


class InteractiveNewsParser(NewsParser):
    """Интерактивная версия парсера новостей"""
    
    def __init__(self):
        super().__init__()
        self.conversation_history = []
    
    def get_interactive_response(self, user_input: str) -> str:
        """Получение ответа на пользовательский вопрос"""
        # Добавляем контекст для интерактивного режима
        interactive_prompt = (
            f"Пользователь спрашивает: '{user_input}'\n\n"
            "Ты — эксперт по новостям в области маркетинга, технологий, рекламы, "
            "искусственного интеллекта и социальных сетей. "
            "Отвечай кратко, по делу, основываясь на актуальных событиях. "
            "Если вопрос касается новостей, предоставь свежую информацию. "
            "Не придумывай факты и не давай вымышленные ссылки."
        )
        
        messages = [
            {"role": "system", "content": self.bot_style},
            {"role": "user", "content": interactive_prompt}
        ]
        
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=messages,
                stream=False,
                timeout=30
            )
            return self.filter_advertisements(response)
        
        except Exception as e:
            return f"Ошибка при получении ответа: {str(e)}"
    
    def is_news_request(self, user_input: str) -> bool:
        """Проверка, является ли запрос запросом новостей"""
        news_keywords = [
            'новости', 'новость', 'события', 'событие', 
            'обновления', 'обновление', 'что нового',
            'последние', 'актуальные', 'свежие'
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in news_keywords)
    
    def run_interactive(self):
        """Запуск интерактивного режима"""
        print("ИНТЕРАКТИВНЫЙ ПАРСЕР НОВОСТЕЙ")
        print("=" * 50)
        print("Доступные команды:")
        print("* 'новости' - получить свежие новости")
        print("* 'выход' или 'quit' - завершить работу")
        print("* Любой другой вопрос - получить ответ на тему")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\nВаш вопрос: ").strip()
                
                if not user_input:
                    continue
                
                # Команды выхода
                if user_input.lower() in ['выход', 'quit', 'exit', 'q']:
                    print("До свидания!")
                    break
                
                # Запрос новостей
                if user_input.lower() in ['новости', 'news'] or self.is_news_request(user_input):
                    print("\n[ОЖИДАНИЕ] Получение актуальных новостей...")
                    news_response = self.get_news_response()
                    
                    if "Ошибка" in news_response:
                        print(f"[ОШИБКА] {news_response}")
                        continue
                    
                    news_items = self.parse_news_structure(news_response)
                    if news_items:
                        self.display_news(news_items)
                    else:
                        print("\nНОВОСТИ:")
                        print("-" * 50)
                        print(news_response)
                        print("-" * 50)
                
                else:
                    # Обычный вопрос
                    print("\n[ОЖИДАНИЕ] Обработка запроса...")
                    response = self.get_interactive_response(user_input)
                    
                    print("\nОТВЕТ:")
                    print("-" * 50)
                    print(response)
                    print("-" * 50)
            
            except KeyboardInterrupt:
                print("\n\n[ОСТАНОВЛЕНО] Работа прервана пользователем")
                break
            except Exception as e:
                print(f"\n[ОШИБКА] Ошибка: {str(e)}")


def main():
    """Главная функция интерактивного режима"""
    try:
        parser = InteractiveNewsParser()
        parser.run_interactive()
    except Exception as e:
        print(f"\n[ОШИБКА] Критическая ошибка: {str(e)}")


if __name__ == "__main__":
    main()
