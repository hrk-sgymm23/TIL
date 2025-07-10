from abc import ABC, abstractmethod
from datetime import datetime
import re


# --- Strategyのインターフェース ---
class ProcessingStrategy(ABC):
    @abstractmethod
    def process(self, data: dict) -> dict:
        pass


# --- 具体的な処理戦略たち ---
class DateFormatStrategy(ProcessingStrategy):
    """ 'date' キーを ISO形式 → yyyy-mm-dd に変換 """
    def process(self, data):
        if 'date' in data:
            try:
                dt = datetime.fromisoformat(data['date'])
                data['date'] = dt.strftime('%Y-%m-%d')
            except Exception:
                pass
        return data


class RemoveKeysStrategy(ProcessingStrategy):
    """ 指定されたキーを削除する """
    def __init__(self, keys_to_remove):
        self.keys_to_remove = keys_to_remove

    def process(self, data):
        for key in self.keys_to_remove:
            data.pop(key, None)
        return data


class SnakeToCamelCaseStrategy(ProcessingStrategy):
    """ キーを snake_case → camelCase に変換する """
    def process(self, data):
        def snake_to_camel(s):
            parts = s.split('_')
            return parts[0] + ''.join(p.title() for p in parts[1:])

        return {snake_to_camel(k): v for k, v in data.items()}
    
class SeparateNameStrategy(ProcessingStrategy):
    """ 名前を分割して、first_nameとlast_nameに格納する """
    def process(self, data):
        if 'name' in data:
            name = data['name']
            parts = name.split(' ')
            data['first_name'] = parts[0]
            data['last_name'] = parts[1]
        return data

# --- パイプラインの本体 ---
class JsonProcessor:
    def __init__(self):
        self.strategies = []

    def add_strategy(self, strategy: ProcessingStrategy):
        self.strategies.append(strategy)

    def process(self, data: dict) -> dict:
        for strategy in self.strategies:
            data = strategy.process(data)
        return data

if __name__ == "__main__":
    data = {
        'date': '2025-01-01',
        'name': 'John Smith',
        'age': 30,
        'address': '123 Main St, Anytown, USA',
        'debug_info': 'This is a debug message'
    }

    processor = JsonProcessor()
    processor.add_strategy(RemoveKeysStrategy(["debug_info"]))
    processor.add_strategy(SnakeToCamelCaseStrategy())
    processor.add_strategy(DateFormatStrategy())
    processor.add_strategy(SeparateNameStrategy())

    result = processor.process(data)

    print(result)

