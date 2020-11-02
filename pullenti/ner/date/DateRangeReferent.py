# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import datetime
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.internal.MetaDateRange import MetaDateRange

class DateRangeReferent(Referent):
    """ Сущность, представляющая диапазон дат
    
    """
    
    def __init__(self) -> None:
        super().__init__(DateRangeReferent.OBJ_TYPENAME)
        self.instance_of = MetaDateRange.GLOBAL_META
    
    OBJ_TYPENAME = "DATERANGE"
    """ Имя типа сущности TypeName ("DATERANGE") """
    
    ATTR_FROM = "FROM"
    """ Имя атрибута - дата начала диапазона (DateReferent) """
    
    ATTR_TO = "TO"
    """ Имя атрибута - дата окончания диапазона (DateReferent) """
    
    @property
    def date_from(self) -> 'DateReferent':
        """ Начало диапазона """
        return Utils.asObjectOrNull(self.get_slot_value(DateRangeReferent.ATTR_FROM), DateReferent)
    @date_from.setter
    def date_from(self, value) -> 'DateReferent':
        self.add_slot(DateRangeReferent.ATTR_FROM, value, True, 0)
        return value
    
    @property
    def date_to(self) -> 'DateReferent':
        """ Конец диапазона """
        return Utils.asObjectOrNull(self.get_slot_value(DateRangeReferent.ATTR_TO), DateReferent)
    @date_to.setter
    def date_to(self, value) -> 'DateReferent':
        self.add_slot(DateRangeReferent.ATTR_TO, value, True, 0)
        return value
    
    @property
    def is_relative(self) -> bool:
        """ Признак относительности диапазона (с 10 по 20 февраля прошлого года) """
        if (self.date_from is not None and self.date_from.is_relative): 
            return True
        if (self.date_to is not None and self.date_to.is_relative): 
            return True
        return False
    
    def calculate_date_range(self, now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int=0) -> bool:
        """ Вычислить диапазон дат (если не диапазон, то from = to)
        
        Args:
            now(datetime.datetime): текущая дата-время
            from0_(datetime.datetime): результирующее начало диапазона
            to(datetime.datetime): результирующий конец диапазона
            tense(int): время (-1 - прошлое, 0 - любое, 1 - будущее) - используется
        при неоднозначных случаях.
        Например, 7 сентября, а сейчас лето, то какой это год? При +1 - этот, при -1 - предыдущий
        
        Returns:
            bool: признак корректности
        """
        from pullenti.ner.date.internal.DateRelHelper import DateRelHelper
        inoutres781 = DateRelHelper.calculate_date_range2(self, now, from0_, to, tense)
        return inoutres781
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        from pullenti.ner.date.internal.DateRelHelper import DateRelHelper
        if (self.is_relative and not short_variant): 
            res = io.StringIO()
            print(self.to_string(True, lang, lev), end="", file=res)
            DateRelHelper.append_to_string2(self, res)
            return Utils.toStringStringIO(res)
        fr = (None if self.date_from is None else self.date_from._to_string(short_variant, lang, lev, 1))
        to = (None if self.date_to is None else self.date_to._to_string(short_variant, lang, lev, 2))
        if (fr is not None and to is not None): 
            return "{0} {1}".format(fr, (to if self.date_to.century > 0 and self.date_to.year == 0 else to.lower()))
        if (fr is not None): 
            return str(fr)
        if (to is not None): 
            return to
        return "{0} ? по ?".format(('з' if lang.is_ua else 'с'))
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType') -> bool:
        dr = Utils.asObjectOrNull(obj, DateRangeReferent)
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
    def _new715(_arg1 : 'DateReferent', _arg2 : 'DateReferent') -> 'DateRangeReferent':
        res = DateRangeReferent()
        res.date_from = _arg1
        res.date_to = _arg2
        return res
    
    @staticmethod
    def _new721(_arg1 : 'DateReferent') -> 'DateRangeReferent':
        res = DateRangeReferent()
        res.date_to = _arg1
        return res