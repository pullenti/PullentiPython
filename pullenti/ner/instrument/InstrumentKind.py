# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class InstrumentKind(IntEnum):
    """ Классы фрагментов документа """
    UNDEFINED = 0
    """ Неизвестно """
    DOCUMENT = 1
    """ Корневой документ """
    INTERNALDOCUMENT = 2
    """ Внутренний документ (например, который утверждается) """
    HEAD = 3
    """ Заголовочная часть """
    CONTENT = 4
    """ Элемент с основным содержимым """
    TAIL = 5
    """ Хвостовая часть """
    APPENDIX = 6
    """ Приложение """
    DOCPART = 7
    """ Часть документа (деление самого верхнего уровня) """
    SECTION = 8
    """ Раздел """
    SUBSECTION = 9
    """ Подраздел """
    CHAPTER = 10
    """ Глава """
    PARAGRAPH = 11
    """ Параграф """
    SUBPARAGRAPH = 12
    """ Подпараграф """
    CLAUSE = 13
    """ Статья """
    CLAUSEPART = 14
    """ Часть статьи """
    ITEM = 15
    """ Пункт """
    SUBITEM = 16
    """ Подпункт """
    INDENTION = 17
    """ Абзац """
    LISTITEM = 18
    """ Элемент списка """
    LISTHEAD = 19
    """ Заголовок списка (первый абзац перед перечислением) """
    PREAMBLE = 20
    """ Преамбула """
    INDEX = 21
    """ Оглавление """
    INDEXITEM = 22
    """ Элемент оглавления """
    NOTICE = 23
    """ Примечание """
    NUMBER = 24
    """ Номер """
    CASENUMBER = 25
    """ Номер дела (для судебных документов) """
    CASEINFO = 26
    """ Дополнительная информация (для судебных документов) """
    NAME = 27
    """ Наименование """
    TYP = 28
    """ Тип """
    SIGNER = 29
    """ Подписант """
    ORGANIZATION = 30
    """ Организация """
    PLACE = 31
    """ Место """
    DATE = 32
    """ Дата-время """
    CONTACT = 33
    """ Контактные данные """
    INITIATOR = 34
    """ Инициатор """
    DIRECTIVE = 35
    """ Директива """
    EDITIONS = 36
    """ Редакции """
    APPROVED = 37
    """ Одобрен, утвержден """
    DOCREFERENCE = 38
    """ Ссылка на документ """
    KEYWORD = 39
    """ Ключевое слово (типа Приложение и т.п.) """
    COMMENT = 40
    """ Комментарий """
    CITATION = 41
    """ Цитата """
    QUESTION = 42
    """ Вопрос """
    ANSWER = 43
    """ Ответ """
    TABLE = 44
    """ Таблица """
    TABLEROW = 45
    """ Строка таблицы """
    TABLECELL = 46
    """ Ячейка таблицы """
    IGNORED = 47
    """ Для внутреннего использования """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)