# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import datetime
import typing
import math
import operator
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.date.internal.DateItemToken import DateItemToken
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class DateExToken(MetaToken):
    """ Используется для нахождения в тексте абсолютных и относительных дат и диапазонов,
     например, "в прошлом году", "за первый квартал этого года", "два дня назад и т.п." """
    
    class DateExItemTokenType(IntEnum):
        YEAR = 0
        QUARTAL = 1
        MONTH = 2
        WEEK = 3
        DAY = 4
        DAYOFWEEK = 5
        """ День недели """
        HOUR = 6
        MINUTE = 7
        WEEKEND = 8
        """ Выходные """
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class DateValues:
        
        def __init__(self) -> None:
            self.day1 = 0
            self.day2 = 0
            self.month1 = 0
            self.month2 = 0
            self.year = 0
        
        def __str__(self) -> str:
            tmp = io.StringIO()
            if (self.year > 0): 
                print("Year:{0}".format(self.year), end="", file=tmp, flush=True)
            if (self.month1 > 0): 
                print(" Month:{0}".format(self.month1), end="", file=tmp, flush=True)
                if (self.month2 > self.month1): 
                    print("..{0}".format(self.month2), end="", file=tmp, flush=True)
            if (self.day1 > 0): 
                print(" Day:{0}".format(self.day1), end="", file=tmp, flush=True)
                if (self.day2 > self.day1): 
                    print("..{0}".format(self.day2), end="", file=tmp, flush=True)
            return Utils.toStringStringIO(tmp).strip()
        
        def generate_date(self, today : datetime.datetime, end_of_diap : bool) -> datetime.datetime:
            year_ = self.year
            if (year_ == 0): 
                year_ = today.year
            mon = self.month1
            if (mon == 0): 
                mon = (12 if end_of_diap else 1)
            elif (end_of_diap and self.month2 > 0): 
                mon = self.month2
            day = self.day1
            if (day == 0): 
                day = (31 if end_of_diap else 1)
            elif (self.day2 > 0 and end_of_diap): 
                day = self.day2
            if (day > Utils.lastDayOfMonth(year_, mon)): 
                day = Utils.lastDayOfMonth(year_, mon)
            return datetime.datetime(year_, mon, day, 0, 0, 0)
        
        @staticmethod
        def try_create(list0_ : typing.List['DateExItemToken'], today : datetime.datetime, tense : int) -> 'DateValues':
            oo = False
            if (list0_ is not None): 
                for v in list0_: 
                    if (v.typ != DateExToken.DateExItemTokenType.HOUR and v.typ != DateExToken.DateExItemTokenType.MINUTE): 
                        oo = True
            if (not oo): 
                return DateExToken.DateValues._new685(today.year, today.month, today.day)
            res = DateExToken.DateValues()
            i = 0
            has_rel = False
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.YEAR): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    res.year = it.value
                else: 
                    res.year = (today.year + it.value)
                    has_rel = True
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.QUARTAL): 
                it = list0_[i]
                v = 0
                if (not it.is_value_relate): 
                    if (res.year == 0): 
                        v0 = 1 + ((math.floor(((today.month - 1)) / 3)))
                        if (it.value > v0 and (tense < 0)): 
                            res.year = (today.year - 1)
                        elif ((it.value < v0) and tense > 0): 
                            res.year = (today.year + 1)
                        else: 
                            res.year = today.year
                    v = it.value
                else: 
                    if (res.year == 0): 
                        res.year = today.year
                    v = (1 + ((math.floor(((today.month - 1)) / 3))) + it.value)
                while v > 3:
                    v -= 3
                    res.year += 1
                while v <= 0:
                    v += 3
                    res.year -= 1
                res.month1 = ((((v - 1)) * 3) + 1)
                res.month2 = (res.month1 + 2)
                return res
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.MONTH): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    if (res.year == 0): 
                        if (it.value > today.month and (tense < 0)): 
                            res.year = (today.year - 1)
                        elif ((it.value < today.month) and tense > 0): 
                            res.year = (today.year + 1)
                        else: 
                            res.year = today.year
                    res.month1 = it.value
                else: 
                    has_rel = True
                    if (res.year == 0): 
                        res.year = today.year
                    v = today.month + it.value
                    while v > 12:
                        v -= 12
                        res.year += 1
                    while v <= 0:
                        v += 12
                        res.year -= 1
                    res.month1 = v
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.WEEKEND and i == 0): 
                it = list0_[i]
                has_rel = True
                if (res.year == 0): 
                    res.year = today.year
                if (res.month1 == 0): 
                    res.month1 = today.month
                if (res.day1 == 0): 
                    res.day1 = today.day
                dt0 = datetime.datetime(res.year, res.month1, res.day1, 0, 0, 0)
                dow = dt0.weekday()
                if (dow == 0): 
                    dt0 = (dt0 + datetime.timedelta(days=5))
                elif (dow == 1): 
                    dt0 = (dt0 + datetime.timedelta(days=4))
                elif (dow == 2): 
                    dt0 = (dt0 + datetime.timedelta(days=3))
                elif (dow == 3): 
                    dt0 = (dt0 + datetime.timedelta(days=2))
                elif (dow == 4): 
                    dt0 = (dt0 + datetime.timedelta(days=1))
                elif (dow == 5): 
                    dt0 = (dt0 + datetime.timedelta(days=-1))
                elif (dow == 6): 
                    pass
                if (it.value != 0): 
                    dt0 = (dt0 + datetime.timedelta(days=it.value * 7))
                res.year = dt0.year
                res.month1 = dt0.month
                res.day1 = dt0.day
                dt0 = (dt0 + datetime.timedelta(days=1))
                res.year = dt0.year
                res.month2 = dt0.month
                res.day2 = dt0.day
                i += 1
            if (((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.WEEK and i == 0) and list0_[i].is_value_relate): 
                it = list0_[i]
                has_rel = True
                if (res.year == 0): 
                    res.year = today.year
                if (res.month1 == 0): 
                    res.month1 = today.month
                if (res.day1 == 0): 
                    res.day1 = today.day
                dt0 = datetime.datetime(res.year, res.month1, res.day1, 0, 0, 0)
                dow = dt0.weekday()
                if (dow == 1): 
                    dt0 = (dt0 + datetime.timedelta(days=-1))
                elif (dow == 2): 
                    dt0 = (dt0 + datetime.timedelta(days=-2))
                elif (dow == 3): 
                    dt0 = (dt0 + datetime.timedelta(days=-3))
                elif (dow == 4): 
                    dt0 = (dt0 + datetime.timedelta(days=-4))
                elif (dow == 5): 
                    dt0 = (dt0 + datetime.timedelta(days=-5))
                elif (dow == 6): 
                    dt0 = (dt0 + datetime.timedelta(days=-6))
                if (it.value != 0): 
                    dt0 = (dt0 + datetime.timedelta(days=it.value * 7))
                res.year = dt0.year
                res.month1 = dt0.month
                res.day1 = dt0.day
                dt0 = (dt0 + datetime.timedelta(days=6))
                res.year = dt0.year
                res.month2 = dt0.month
                res.day2 = dt0.day
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.DAY): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    res.day1 = it.value
                    if (res.month1 == 0): 
                        if (res.year == 0): 
                            res.year = today.year
                        if (it.value > today.day and (tense < 0)): 
                            res.month1 = (today.month - 1)
                            if (res.month1 <= 0): 
                                res.month1 = 12
                                res.year -= 1
                        elif ((it.value < today.day) and tense > 0): 
                            res.month1 = (today.month + 1)
                            if (res.month1 > 12): 
                                res.month1 = 1
                                res.year += 1
                        else: 
                            res.month1 = today.month
                else: 
                    has_rel = True
                    if (res.year == 0): 
                        res.year = today.year
                    if (res.month1 == 0): 
                        res.month1 = today.month
                    v = today.day + it.value
                    while v > Utils.lastDayOfMonth(res.year, res.month1):
                        v -= Utils.lastDayOfMonth(res.year, res.month1)
                        res.month1 += 1
                        if (res.month1 > 12): 
                            res.month1 = 1
                            res.year += 1
                    while v <= 0:
                        res.month1 -= 1
                        if (res.month1 <= 0): 
                            res.month1 = 12
                            res.year -= 1
                        v += Utils.lastDayOfMonth(res.year, res.month1)
                    res.day1 = v
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                it = list0_[i]
            return res
        
        @staticmethod
        def _new685(_arg1 : int, _arg2 : int, _arg3 : int) -> 'DateValues':
            res = DateExToken.DateValues()
            res.year = _arg1
            res.month1 = _arg2
            res.day1 = _arg3
            return res
    
    class DateExItemToken(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            super().__init__(begin, end, None)
            self.typ = DateExToken.DateExItemTokenType.YEAR
            self.value = 0
            self.is_value_relate = False
            self.is_value_notstrict = False
        
        def __str__(self) -> str:
            tmp = io.StringIO()
            print("{0} ".format(Utils.enumToString(self.typ)), end="", file=tmp, flush=True)
            if (self.is_value_notstrict): 
                print("~", end="", file=tmp)
            if (self.is_value_relate): 
                print("{0}{1}".format(("" if self.value < 0 else "+"), self.value), end="", file=tmp, flush=True)
            else: 
                print(self.value, end="", file=tmp)
            return Utils.toStringStringIO(tmp)
        
        @staticmethod
        def try_parse(t : 'Token', prev : typing.List['DateExItemToken']) -> 'DateExItemToken':
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
            from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
            from pullenti.ner.date.internal.DateItemToken import DateItemToken
            if (t is None): 
                return None
            if (t.is_value("СЕГОДНЯ", None)): 
                return DateExToken.DateExItemToken._new688(t, t, DateExToken.DateExItemTokenType.DAY, 0, True)
            if (t.is_value("ЗАВТРА", None)): 
                return DateExToken.DateExItemToken._new688(t, t, DateExToken.DateExItemTokenType.DAY, 1, True)
            if (t.is_value("ПОСЛЕЗАВТРА", None)): 
                return DateExToken.DateExItemToken._new688(t, t, DateExToken.DateExItemTokenType.DAY, 2, True)
            if (t.is_value("ВЧЕРА", None)): 
                return DateExToken.DateExItemToken._new688(t, t, DateExToken.DateExItemTokenType.DAY, -1, True)
            if (t.is_value("ПОЗАВЧЕРА", None)): 
                return DateExToken.DateExItemToken._new688(t, t, DateExToken.DateExItemTokenType.DAY, -2, True)
            if (t.is_value("ПОЛЧАСА", None)): 
                return DateExToken.DateExItemToken._new688(t, t, DateExToken.DateExItemTokenType.MINUTE, 30, True)
            npt = NounPhraseHelper.try_parse(t, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0)
            if (npt is None): 
                if ((isinstance(t, NumberToken)) and (t).int_value is not None): 
                    res0 = DateExToken.DateExItemToken.try_parse(t.next0_, prev)
                    if (res0 is not None and res0.value == 1): 
                        res0.begin_token = t
                        res0.value = (t).int_value
                        if (t.previous is not None and t.previous.is_value("ЧЕРЕЗ", None)): 
                            res0.is_value_relate = True
                        return res0
                    dtt = DateItemToken.try_attach(t, None, False)
                    if (dtt is not None and dtt.typ == DateItemToken.DateItemType.YEAR): 
                        return DateExToken.DateExItemToken._new687(t, dtt.end_token, DateExToken.DateExItemTokenType.YEAR, dtt.int_value)
                return None
            ty = DateExToken.DateExItemTokenType.HOUR
            val = 0
            if (npt.noun.is_value("ГОД", None) or npt.noun.is_value("ГОДИК", None)): 
                ty = DateExToken.DateExItemTokenType.YEAR
            elif (npt.noun.is_value("КВАРТАЛ", None)): 
                ty = DateExToken.DateExItemTokenType.QUARTAL
            elif (npt.noun.is_value("МЕСЯЦ", None)): 
                ty = DateExToken.DateExItemTokenType.MONTH
            elif (npt.noun.is_value("ДЕНЬ", None) or npt.noun.is_value("ДЕНЕК", None)): 
                if (npt.end_token.next0_ is not None and npt.end_token.next0_.is_value("НЕДЕЛЯ", None)): 
                    return None
                ty = DateExToken.DateExItemTokenType.DAY
            elif (npt.noun.is_value("НЕДЕЛЯ", None) or npt.noun.is_value("НЕДЕЛЬКА", None)): 
                if (t.previous is not None and t.previous.is_value("ДЕНЬ", None)): 
                    return None
                if (t.previous is not None and t.previous.is_value("ЗА", None)): 
                    ty = DateExToken.DateExItemTokenType.WEEK
                elif (t.is_value("ЗА", None)): 
                    ty = DateExToken.DateExItemTokenType.WEEK
                else: 
                    ty = DateExToken.DateExItemTokenType.DAY
                    val = 7
            elif (npt.noun.is_value("ВЫХОДНОЙ", None)): 
                ty = DateExToken.DateExItemTokenType.WEEKEND
            elif (npt.noun.is_value("ЧАС", None) or npt.noun.is_value("ЧАСИК", None) or npt.noun.is_value("ЧАСОК", None)): 
                ty = DateExToken.DateExItemTokenType.HOUR
            elif (npt.noun.is_value("МИНУТА", None) or npt.noun.is_value("МИНУТКА", None)): 
                ty = DateExToken.DateExItemTokenType.MINUTE
            elif (npt.noun.is_value("ПОНЕДЕЛЬНИК", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 1
            elif (npt.noun.is_value("ВТОРНИК", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 2
            elif (npt.noun.is_value("СРЕДА", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 3
            elif (npt.noun.is_value("ЧЕТВЕРГ", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 4
            elif (npt.noun.is_value("ПЯТНИЦА", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 5
            elif (npt.noun.is_value("СУББОТА", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 6
            elif (npt.noun.is_value("ВОСКРЕСЕНЬЕ", None) or npt.noun.is_value("ВОСКРЕСЕНИЕ", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 7
            else: 
                dti = DateItemToken.try_attach(npt.end_token, None, False)
                if (dti is not None and dti.typ == DateItemToken.DateItemType.MONTH): 
                    ty = DateExToken.DateExItemTokenType.MONTH
                    val = dti.int_value
                else: 
                    return None
            res = DateExToken.DateExItemToken._new687(t, npt.end_token, ty, val)
            heg = False
            for a in npt.adjectives: 
                if (a.is_value("СЛЕДУЮЩИЙ", None) or a.is_value("БУДУЩИЙ", None) or a.is_value("БЛИЖАЙШИЙ", None)): 
                    if (res.value == 0 and ty != DateExToken.DateExItemTokenType.WEEKEND): 
                        res.value = 1
                    res.is_value_relate = True
                elif (a.is_value("ПРЕДЫДУЩИЙ", None) or a.is_value("ПРОШЛЫЙ", None) or a.is_value("ПРОШЕДШИЙ", None)): 
                    if (res.value == 0): 
                        res.value = 1
                    res.is_value_relate = True
                    heg = True
                elif (a.begin_token == a.end_token and (isinstance(a.begin_token, NumberToken)) and (a.begin_token).int_value is not None): 
                    if (res.typ != DateExToken.DateExItemTokenType.DAYOFWEEK): 
                        res.value = (a.begin_token).int_value
                elif (a.is_value("ЭТОТ", None) or a.is_value("ТЕКУЩИЙ", None)): 
                    res.is_value_relate = True
                elif (a.is_value("БЛИЖАЙШИЙ", None) and res.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                    pass
                else: 
                    return None
            if (npt.anafor is not None and npt.anafor.is_value("ЭТОТ", None)): 
                if (res.value == 0): 
                    res.is_value_relate = True
            if (heg): 
                res.value = (- res.value)
            if (t.previous is not None): 
                if (t.previous.is_value("ЧЕРЕЗ", None)): 
                    res.is_value_relate = True
                    if (res.value == 0): 
                        res.value = 1
                    res.begin_token = t.previous
                elif (t.previous.is_value("ЗА", None) and res.value == 0): 
                    res.is_value_relate = True
            return res
        
        def compareTo(self, other : 'DateExItemToken') -> int:
            if ((self.typ) < (other.typ)): 
                return -1
            if ((self.typ) > (other.typ)): 
                return 1
            return 0
        
        @staticmethod
        def _new687(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            return res
        
        @staticmethod
        def _new688(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int, _arg5 : bool) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            res.is_value_relate = _arg5
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.is_diap = False
        self.items_from = list()
        self.items_to = list()
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        for it in self.items_from: 
            print("{0}{1}; ".format(("(fr)" if self.is_diap else ""), str(it)), end="", file=tmp, flush=True)
        for it in self.items_to: 
            print("(to){0}; ".format(str(it)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def get_date(self, now : datetime.datetime, tense : int=0) -> datetime.datetime:
        """ Получить дату-время (одну)
        
        Args:
            now(datetime.datetime): текущая дата (для относительных вычислений)
            tense(int): время (-1 - прошлое, 0 - любое, 1 - будущее) - испрользуется
         при неоднозначных случаях
        
        Returns:
            datetime.datetime: дата-время или null
        """
        dvl = DateExToken.DateValues.try_create((self.items_from if len(self.items_from) > 0 else self.items_to), now, tense)
        try: 
            dt = dvl.generate_date(now, False)
            dt = self.__correct_hours(dt, (self.items_from if len(self.items_from) > 0 else self.items_to), now)
            return dt
        except Exception as ex: 
            return None
    
    def get_dates(self, now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int=0) -> bool:
        """ Получить диапазон (если не диапазон, то from = to)
        
        Args:
            now(datetime.datetime): текущая дата-время
            from0_(datetime.datetime): начало диапазона
            to(datetime.datetime): конец диапазона
            tense(int): время (-1 - прошлое, 0 - любое, 1 - будущее) - испрользуется
         при неоднозначных случаях
         Например, 7 сентября, а сейчас лето, то какой это год? При true - этот, при false - предыдущий
        
        Returns:
            bool: признак корректности
        """
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.min
        has_hours = False
        for it in self.items_from: 
            if (it.typ == DateExToken.DateExItemTokenType.HOUR or it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                has_hours = True
        for it in self.items_to: 
            if (it.typ == DateExToken.DateExItemTokenType.HOUR or it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                has_hours = True
        li = list()
        if (has_hours): 
            for it in self.items_from: 
                if (it.typ != DateExToken.DateExItemTokenType.HOUR and it.typ != DateExToken.DateExItemTokenType.MINUTE): 
                    li.append(it)
            for it in self.items_to: 
                if (it.typ != DateExToken.DateExItemTokenType.HOUR and it.typ != DateExToken.DateExItemTokenType.MINUTE): 
                    exi = False
                    for itt in li: 
                        if (itt.typ == it.typ): 
                            exi = True
                            break
                    if (not exi): 
                        li.append(it)
            li.sort(key=operator.attrgetter('typ'))
            dvl = DateExToken.DateValues.try_create(li, now, tense)
            if (dvl is None): 
                return False
            try: 
                from0_.value = dvl.generate_date(now, False)
            except Exception as ex: 
                return False
            to.value = from0_.value
            from0_.value = self.__correct_hours(from0_.value, self.items_from, now)
            to.value = self.__correct_hours(to.value, self.items_to, now)
            return True
        if (len(self.items_to) == 0): 
            dvl = DateExToken.DateValues.try_create(self.items_from, now, tense)
            try: 
                from0_.value = dvl.generate_date(now, False)
            except Exception as ex: 
                return False
            try: 
                to.value = dvl.generate_date(now, True)
            except Exception as ex: 
                to.value = from0_.value
            return True
        li.clear()
        for it in self.items_from: 
            li.append(it)
        for it in self.items_to: 
            exi = False
            for itt in li: 
                if (itt.typ == it.typ): 
                    exi = True
                    break
            if (not exi): 
                li.append(it)
        li.sort(key=operator.attrgetter('typ'))
        dvl1 = DateExToken.DateValues.try_create(li, now, tense)
        li.clear()
        for it in self.items_to: 
            li.append(it)
        for it in self.items_from: 
            exi = False
            for itt in li: 
                if (itt.typ == it.typ): 
                    exi = True
                    break
            if (not exi): 
                li.append(it)
        li.sort(key=operator.attrgetter('typ'))
        dvl2 = DateExToken.DateValues.try_create(li, now, tense)
        try: 
            from0_.value = dvl1.generate_date(now, False)
        except Exception as ex: 
            return False
        try: 
            to.value = dvl2.generate_date(now, True)
        except Exception as ex: 
            return False
        return True
    
    def __correct_hours(self, dt : datetime.datetime, li : typing.List['DateExItemToken'], now : datetime.datetime) -> datetime.datetime:
        has_hour = False
        for it in li: 
            if (it.typ == DateExToken.DateExItemTokenType.HOUR): 
                has_hour = True
                if (it.is_value_relate): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, now.hour, now.minute, 0)
                    dt = (dt + datetime.timedelta(hours=it.value))
                elif (it.value > 0 and (it.value < 24)): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, it.value, 0, 0)
            elif (it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                if (not has_hour): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, now.hour, 0, 0)
                if (it.is_value_relate): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
                    dt = (dt + datetime.timedelta(minutes=it.value))
                    if (not has_hour): 
                        dt = (dt + datetime.timedelta(minutes=now.minute))
                elif (it.value > 0 and (it.value < 60)): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, it.value, 0)
        return dt
    
    @staticmethod
    def try_parse(t : 'Token') -> 'DateExToken':
        """ Выделить в тексте дату с указанной позиции
        
        Args:
            t(Token): 
        
        """
        if (t is None): 
            return None
        if (t.is_value("ЗА", None) and t.next0_ is not None and t.next0_.is_value("ПЕРИОД", None)): 
            ne = DateExToken.try_parse(t.next0_.next0_)
            if (ne is not None and ne.is_diap): 
                ne.begin_token = t
                return ne
        res = None
        to_regime = False
        from_regime = False
        t0 = None
        tt = t
        first_pass2997 = True
        while True:
            if first_pass2997: first_pass2997 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            drr = Utils.asObjectOrNull(tt.get_referent(), DateRangeReferent)
            if (drr is not None): 
                res = DateExToken._new686(t, tt, True)
                fr = drr.date_from
                if (fr is not None): 
                    DateExToken.__add_items(fr, res.items_from, tt)
                to = drr.date_to
                if (to is not None): 
                    DateExToken.__add_items(to, res.items_to, tt)
                has_year = False
                if (len(res.items_from) > 0 and res.items_from[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                elif (len(res.items_to) > 0 and res.items_to[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                if (not has_year and (tt.whitespaces_after_count < 3)): 
                    dit = DateExToken.DateExItemToken.try_parse(tt.next0_, None)
                    if (dit is not None and dit.typ == DateExToken.DateExItemTokenType.YEAR): 
                        if (len(res.items_from) > 0): 
                            res.items_from.insert(0, dit)
                        if (len(res.items_to) > 0): 
                            res.items_to.insert(0, dit)
                        res.end_token = dit.end_token
                return res
            dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
            if (dr is not None): 
                if (res is None): 
                    res = DateExToken(t, tt)
                if (to_regime): 
                    if (len(res.items_to) > 0): 
                        break
                    DateExToken.__add_items(dr, res.items_to, tt)
                else: 
                    if (len(res.items_from) > 0): 
                        break
                    DateExToken.__add_items(dr, res.items_from, tt)
                has_year = False
                if (len(res.items_from) > 0 and res.items_from[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                elif (len(res.items_to) > 0 and res.items_to[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                if (not has_year and (tt.whitespaces_after_count < 3)): 
                    dit = DateExToken.DateExItemToken.try_parse(tt.next0_, None)
                    if (dit is not None and dit.typ == DateExToken.DateExItemTokenType.YEAR): 
                        if (len(res.items_from) > 0): 
                            res.items_from.insert(0, dit)
                        if (len(res.items_to) > 0): 
                            res.items_to.insert(0, dit)
                        res.end_token = dit.end_token
                continue
            if (tt.morph.class0_.is_preposition): 
                if (tt.is_value("ПО", None) or tt.is_value("ДО", None)): 
                    to_regime = True
                    if (t0 is None): 
                        t0 = tt
                elif (tt.is_value("С", None) or tt.is_value("ОТ", None)): 
                    from_regime = True
                    if (t0 is None): 
                        t0 = tt
                continue
            it = DateExToken.DateExItemToken.try_parse(tt, None)
            if (it is None): 
                break
            if (tt.is_value("ДЕНЬ", None) and tt.next0_ is not None and tt.next0_.is_value("НЕДЕЛЯ", None)): 
                break
            if (it.end_token == tt and ((it.typ == DateExToken.DateExItemTokenType.HOUR or it.typ == DateExToken.DateExItemTokenType.MINUTE))): 
                if (tt.previous is None or not tt.previous.morph.class0_.is_preposition): 
                    break
            if (res is None): 
                res = DateExToken(t, tt)
            if (to_regime): 
                res.items_to.append(it)
            else: 
                res.items_from.append(it)
            tt = it.end_token
            res.end_token = tt
        if (res is not None): 
            if (t0 is not None and res.begin_token.previous == t0): 
                res.begin_token = t0
            res.is_diap = (from_regime or to_regime)
            res.items_from.sort(key=operator.attrgetter('typ'))
            res.items_to.sort(key=operator.attrgetter('typ'))
        return res
    
    @staticmethod
    def __add_items(fr : 'DateReferent', res : typing.List['DateExItemToken'], tt : 'Token') -> None:
        if (fr.year > 0): 
            res.append(DateExToken.DateExItemToken._new687(tt, tt, DateExToken.DateExItemTokenType.YEAR, fr.year))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new688(tt, tt, DateExToken.DateExItemTokenType.YEAR, 0, True))
        if (fr.month > 0): 
            res.append(DateExToken.DateExItemToken._new687(tt, tt, DateExToken.DateExItemTokenType.MONTH, fr.month))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new688(tt, tt, DateExToken.DateExItemTokenType.MONTH, 0, True))
        if (fr.day > 0): 
            res.append(DateExToken.DateExItemToken._new687(tt, tt, DateExToken.DateExItemTokenType.DAY, fr.day))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new688(tt, tt, DateExToken.DateExItemTokenType.DAY, 0, True))
    
    @staticmethod
    def _new686(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'DateExToken':
        res = DateExToken(_arg1, _arg2)
        res.is_diap = _arg3
        return res