# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class InstrumentKind(IntEnum):
    """ Классы частей НПА """
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
    NOTICE = 22
    """ Примечание """
    NUMBER = 23
    """ Номер """
    CASENUMBER = 24
    """ Номер дела (для судебных документов) """
    CASEINFO = 25
    """ Дополнительная информация (для судебных документов) """
    NAME = 26
    """ Наименование """
    TYP = 27
    """ Тип """
    SIGNER = 28
    """ Подписант """
    ORGANIZATION = 29
    """ Организация """
    PLACE = 30
    """ Место """
    DATE = 31
    """ Дата-время """
    CONTACT = 32
    """ Контактные данные """
    INITIATOR = 33
    """ Инициатор """
    DIRECTIVE = 34
    """ Директива """
    EDITIONS = 35
    """ Редакции """
    APPROVED = 36
    """ Одобрен, утвержден """
    DOCREFERENCE = 37
    """ Ссылка на документ """
    KEYWORD = 38
    """ Ключевое слово (типа Приложение и т.п.) """
    COMMENT = 39
    """ Комментарий """
    CITATION = 40
    """ Цитата """
    QUESTION = 41
    """ Вопрос """
    ANSWER = 42
    """ Ответ """
    TABLE = 43
    """ Таблица """
    TABLEROW = 44
    """ Строка таблицы """
    TABLECELL = 45
    """ Ячейка таблицы """
    IGNORED = 46
    """ Для внутреннего использования """