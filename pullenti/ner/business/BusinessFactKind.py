# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class BusinessFactKind(IntEnum):
    """ Типы бизнес-фактов """
    UNDEFINED = 0
    CREATE = 0 + 1
    """ Создан """
    DELETE = (0 + 1) + 1
    """ Упразднён """
    GET = ((0 + 1) + 1) + 1
    """ Приобретать, покупать """
    SELL = (((0 + 1) + 1) + 1) + 1
    """ Продавать """
    HAVE = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Владеть, иметь """
    PROFIT = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ Прибыль, доход """
    DAMAGES = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Убытки """
    AGREEMENT = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Соглашение """
    SUBSIDIARY = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Дочернее предприятие """
    FINANCE = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Финансировать, спонсировать """
    LAWSUIT = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Судебный иск """