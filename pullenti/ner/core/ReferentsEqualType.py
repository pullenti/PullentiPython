# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ReferentsEqualType(IntEnum):
    """ Атрибут сравнения сущностей (методом Referent.CanBeEquals)
    Атрибут сравнения сущностей
    """
    WITHINONETEXT = 0
    """ Сущности в рамках одного текста """
    DIFFERENTTEXTS = 1
    """ Сущности из разных текстов """
    FORMERGING = 2
    """ Проверка для потенциального объединения сущностей """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)