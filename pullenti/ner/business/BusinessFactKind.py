# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class BusinessFactKind(IntEnum):
    """ Типы бизнес-фактов """
    UNDEFINED = 0
    CREATE = 1
    """ Создан """
    DELETE = 2
    """ Упразднён """
    GET = 3
    """ Приобретать, покупать """
    SELL = 4
    """ Продавать """
    HAVE = 5
    """ Владеть, иметь """
    PROFIT = 6
    """ Прибыль, доход """
    DAMAGES = 7
    """ Убытки """
    AGREEMENT = 8
    """ Соглашение """
    SUBSIDIARY = 9
    """ Дочернее предприятие """
    FINANCE = 10
    """ Финансировать, спонсировать """
    LAWSUIT = 11
    """ Судебный иск """