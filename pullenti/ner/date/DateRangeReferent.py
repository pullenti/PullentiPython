# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.Referent import Referent


class DateRangeReferent(Referent):
    """ Сущность, представляющая диапазон дат """
    
    def __init__(self) -> None:
        from pullenti.ner.date.internal.MetaDateRange import MetaDateRange
        super().__init__(DateRangeReferent.OBJ_TYPENAME)
        self.instance_of = MetaDateRange.GLOBAL_META
    
    OBJ_TYPENAME = "DATERANGE"
    
    ATTR_FROM = "FROM"
    
    ATTR_TO = "TO"
    
    @property
    def date_from(self) -> 'DateReferent':
        """ Начало диапазона """
        from pullenti.ner.date.DateReferent import DateReferent
        return (self.get_value(DateRangeReferent.ATTR_FROM) if isinstance(self.get_value(DateRangeReferent.ATTR_FROM), DateReferent) else None)
    
    @date_from.setter
    def date_from(self, value) -> 'DateReferent':
        self.add_slot(DateRangeReferent.ATTR_FROM, value, True, 0)
        return value
    
    @property
    def date_to(self) -> 'DateReferent':
        """ Конец диапазона """
        from pullenti.ner.date.DateReferent import DateReferent
        return (self.get_value(DateRangeReferent.ATTR_TO) if isinstance(self.get_value(DateRangeReferent.ATTR_TO), DateReferent) else None)
    
    @date_to.setter
    def date_to(self, value) -> 'DateReferent':
        self.add_slot(DateRangeReferent.ATTR_TO, value, True, 0)
        return value
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int) -> str:
        fr = (None if self.date_from is None else self.date_from._to_string(short_variant, lang, lev, 1))
        to = (None if self.date_to is None else self.date_to._to_string(short_variant, lang, lev, 2))
        if (fr is not None and to is not None): 
            return "{0} {1}".format(fr, (to if self.date_to.century > 0 and self.date_to.year == 0 else to.lower()))
        if (fr is not None): 
            return str(fr)
        if (to is not None): 
            return to
        return "{0} ? по ?".format(('з' if lang.is_ua else 'с'))
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        dr = (obj if isinstance(obj, DateRangeReferent) else None)
        if (dr is None): 
            return False
        if (self.date_from is not None): 
            if (not self.date_from.can_be_equals(dr.date_from, typ)): 
                return False
        elif (dr.date_from is not None): 
            return False
        if (self.date_to is not None): 
            if (not self.date_to.can_be_equals(dr.date_to, typ)): 
                return False
        elif (dr.date_to is not None): 
            return False
        return True
    
    @property
    def quarter_number(self) -> int:
        """ Проверка, что диапазон задаёт квартал, возвращает номер 1..4 """
        if (self.date_from is None or self.date_to is None or self.date_from.year != self.date_to.year): 
            return 0
        m1 = self.date_from.month
        m2 = self.date_to.month
        if (m1 == 1 and m2 == 3): 
            return 1
        if (m1 == 4 and m2 == 6): 
            return 2
        if (m1 == 7 and m2 == 9): 
            return 3
        if (m1 == 10 and m2 == 12): 
            return 4
        return 0
    
    @property
    def halfyear_number(self) -> int:
        """ Проверка, что диапазон задаёт полугодие, возвращает номер 1..2 """
        if (self.date_from is None or self.date_to is None or self.date_from.year != self.date_to.year): 
            return 0
        m1 = self.date_from.month
        m2 = self.date_to.month
        if (m1 == 1 and m2 == 6): 
            return 1
        if (m1 == 7 and m2 == 12): 
            return 2
        return 0

    
    @staticmethod
    def _new677(_arg1 : 'DateReferent', _arg2 : 'DateReferent') -> 'DateRangeReferent':
        res = DateRangeReferent()
        res.date_from = _arg1
        res.date_to = _arg2
        return res
    
    @staticmethod
    def _new682(_arg1 : 'DateReferent') -> 'DateRangeReferent':
        res = DateRangeReferent()
        res.date_to = _arg1
        return res