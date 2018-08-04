# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import datetime
import typing
import math
import operator
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken


from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.date.DatePointerType import DatePointerType


class DateExToken(MetaToken):
    """ Используется для нахождения в тексте абсолютных и относительных дат и диапазонов,
     например, "в прошлом году", "за первый квартал этого года", "два дня назад и т.п." """
    
    class DateExItemTokenType(IntEnum):
        YEAR = 0
        QUARTAL = 1
        MONTH = 2
        DAY = 4
        DAYOFWEEK = 5
        """ День недели """
        HOUR = 6
        MINUTE = 7
    
    class DateValues:
        
        def __init__(self) -> None:
            self.day1 = 0
            self.day2 = 0
            self.month1 = 0
            self.month2 = 0
            self.year = 0
        
        def __str__(self) -> str:
            tmp = Utils.newStringIO(None)
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
            elif (self.day2 > 0): 
                day = self.day2
            if (day > Utils.lastDayOfMonth(year_, mon)): 
                day = Utils.lastDayOfMonth(year_, mon)
            return datetime.datetime(year_, mon, day)
        
        @staticmethod
        def try_create(list0_ : typing.List['DateExItemToken'], today : datetime.datetime, tense : int) -> 'DateValues':
            oo = False
            if (list0_ is not None): 
                for v in list0_: 
                    if (v.typ != DateExToken.DateExItemTokenType.HOUR and v.typ != DateExToken.DateExItemTokenType.MINUTE): 
                        oo = True
            if (not oo): 
                return DateExToken.DateValues._new655(today.year, today.month, today.day)
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
                        v0 = 1 + ((math.floor(((today.month - 1)) / 4)))
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
                    v = (1 + ((math.floor(((today.month - 1)) / 4))) + it.value)
                while v > 4:
                    v -= 4
                    res.year += 1
                while v <= 0:
                    v += 4
                    res.year -= 1
                res.month1 = ((((v - 1)) * 4) + 1)
                res.month2 = (res.month1 + 3)
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
        def _new655(_arg1 : int, _arg2 : int, _arg3 : int) -> 'DateValues':
            res = DateExToken.DateValues()
            res.year = _arg1
            res.month1 = _arg2
            res.day1 = _arg3
            return res
    
    class DateExItemToken(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            self.typ = DateExToken.DateExItemTokenType.YEAR
            self.value = 0
            self.is_value_relate = False
            self.is_value_notstrict = False
            super().__init__(begin, end, None)
        
        def __str__(self) -> str:
            tmp = Utils.newStringIO(None)
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
            from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
            from pullenti.ner.NumberToken import NumberToken
            if (t is None): 
                return None
            if (t.is_value("ЗАВТРА", None)): 
                return DateExToken.DateExItemToken._new658(t, t, DateExToken.DateExItemTokenType.DAY, 1, True)
            if (t.is_value("ПОСЛЕЗАВТРА", None)): 
                return DateExToken.DateExItemToken._new658(t, t, DateExToken.DateExItemTokenType.DAY, 2, True)
            if (t.is_value("ВЧЕРА", None)): 
                return DateExToken.DateExItemToken._new658(t, t, DateExToken.DateExItemTokenType.DAY, -1, True)
            if (t.is_value("ПОЗАВЧЕРА", None)): 
                return DateExToken.DateExItemToken._new658(t, t, DateExToken.DateExItemTokenType.DAY, -2, True)
            if (t.is_value("ПОЛЧАСА", None)): 
                return DateExToken.DateExItemToken._new658(t, t, DateExToken.DateExItemTokenType.MINUTE, 30, True)
            npt = NounPhraseHelper.try_parse(t, Utils.valToEnum(NounPhraseParseAttr.PARSENUMERICASADJECTIVE | NounPhraseParseAttr.PARSEPREPOSITION, NounPhraseParseAttr), 0)
            if (npt is None): 
                if (isinstance(t, NumberToken)): 
                    res0 = DateExToken.DateExItemToken.try_parse(t.next0_, prev)
                    if (res0 is not None and res0.value == 1): 
                        res0.begin_token = t
                        res0.value = (t if isinstance(t, NumberToken) else None).value
                        if (t.previous is not None and t.previous.is_value("ЧЕРЕЗ", None)): 
                            res0.is_value_relate = True
                        return res0
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
                ty = DateExToken.DateExItemTokenType.DAY
            elif (npt.noun.is_value("НЕДЕЛЯ", None) or npt.noun.is_value("НЕДЕЛЬКА", None)): 
                ty = DateExToken.DateExItemTokenType.DAY
                val = 7
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
                return None
            res = DateExToken.DateExItemToken._new657(t, npt.end_token, ty, val)
            heg = False
            for a in npt.adjectives: 
                if (a.is_value("СЛЕДУЮЩИЙ", None) or a.is_value("БУДУЩИЙ", None)): 
                    res.is_value_relate = True
                elif (a.is_value("ПРЕДЫДУЩИЙ", None) or a.is_value("ПРОШЛЫЙ", None)): 
                    res.is_value_relate = True
                    heg = True
                elif (a.begin_token == a.end_token and isinstance(a.begin_token, NumberToken)): 
                    if (res.typ != DateExToken.DateExItemTokenType.DAYOFWEEK): 
                        res.value = (a.begin_token if isinstance(a.begin_token, NumberToken) else None).value
                elif (a.is_value("ЭТОТ", None) or a.is_value("ТЕКУЩИЙ", None)): 
                    pass
                elif (a.is_value("БЛИЖАЙШИЙ", None) and res.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                    pass
                else: 
                    return None
            if (res.value == 0): 
                res.value = 1
            if (heg): 
                res.value = (- res.value)
            if (t.previous is not None): 
                if (t.previous.is_value("ЧЕРЕЗ", None)): 
                    res.is_value_relate = True
                    res.begin_token = t.previous
            return res
        
        def compareTo(self, other : 'DateExItemToken') -> int:
            if (self.typ < other.typ): 
                return -1
            if (self.typ > other.typ): 
                return 1
            return 0
    
        
        @staticmethod
        def _new657(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            return res
        
        @staticmethod
        def _new658(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int, _arg5 : bool) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            res.is_value_relate = _arg5
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        
        self.is_diap = False
        self.items_from = list()
        self.items_to = list()
        super().__init__(begin, end, None)
    
    def __str__(self) -> str:
        tmp = Utils.newStringIO(None)
        for it in self.items_from: 
            print("{0}{1}; ".format(("(fr)" if self.is_diap else ""), str(it)), end="", file=tmp, flush=True)
        for it in self.items_to: 
            print("(to){0}; ".format(str(it)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def get_dates_old(self, now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, can_be_future : bool=False) -> bool:
        yfrom = None
        yto = None
        yfrom_def = False
        yto_def = False
        qfrom = None
        qto = None
        mfrom = None
        mto = None
        dfrom = None
        dto = None
        hfrom = None
        hto = None
        min_from = None
        min_to = None
        for k in range(2):
            its = (self.items_from if k == 0 else self.items_to)
            i = 0
            v = 0
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.YEAR): 
                if (not its[i].is_value_relate): 
                    v = its[i].value
                else: 
                    v = (now.year + its[i].value)
                i += 1
                if (k == 0): 
                    yfrom = v
                else: 
                    yto = v
                if (k == 0): 
                    yfrom_def = True
                else: 
                    yto_def = True
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.QUARTAL): 
                if (not its[i].is_value_relate): 
                    v = its[i].value
                else: 
                    v = (1 + ((math.floor(((now.month - 1)) / 4))) + its[i].value)
                i = len(its)
                if (k == 0): 
                    qfrom = v
                else: 
                    qto = v
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.MONTH): 
                if (not its[i].is_value_relate): 
                    v = its[i].value
                else: 
                    v = (now.month + its[i].value)
                i += 1
                if (k == 0): 
                    mfrom = v
                else: 
                    mto = v
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.DAY): 
                if (not its[i].is_value_relate): 
                    v = its[i].value
                else: 
                    v = (now.day + its[i].value)
                i += 1
                if (k == 0): 
                    dfrom = v
                else: 
                    dto = v
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                v = its[i].value
                if (its[i].value < 0): 
                    v = (- v)
                    ddd = now
                    while True: 
                        if (ddd.weekday() == java.time.DayOfWeek.MONDAY): 
                            ddd = (ddd + datetime.timedelta(days=-7))
                            if (v > 1): 
                                ddd = (ddd + datetime.timedelta(days=v - 1))
                            if (k == 0): 
                                yfrom = ddd.year
                                mfrom = ddd.month
                                dfrom = ddd.day
                            else: 
                                yto = ddd.year
                                mto = ddd.month
                                dto = ddd.day
                            break
                        ddd = (ddd + datetime.timedelta(days=-1))
                else: 
                    dow = now.weekday()
                    if (dow == 0): 
                        dow = 7
                    ddd = now
                    if (v > dow): 
                        ddd = (ddd + datetime.timedelta(days=v - dow))
                    else: 
                        if (can_be_future): 
                            ddd = (ddd + datetime.timedelta(days=7))
                        if (dow > v): 
                            ddd = (ddd + datetime.timedelta(days=v - dow))
                    if (k == 0): 
                        yfrom = ddd.year
                        mfrom = ddd.month
                        dfrom = ddd.day
                    else: 
                        yto = ddd.year
                        mto = ddd.month
                        dto = ddd.day
                i += 1
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.HOUR): 
                if (not its[i].is_value_relate): 
                    v = its[i].value
                else: 
                    v = (now.hour + its[i].value)
                i += 1
                if (k == 0): 
                    hfrom = v
                else: 
                    hto = v
            if ((i < len(its)) and its[i].typ == DateExToken.DateExItemTokenType.MINUTE): 
                if (not its[i].is_value_relate and len(its) > 1): 
                    v = its[i].value
                else: 
                    v = (now.minute + its[i].value)
                i += 1
                if (k == 0): 
                    min_from = v
                else: 
                    min_to = v
        if (yfrom is None): 
            if (yto is None): 
                yto = now.year
                yfrom = yto
            else: 
                yfrom = yto
        elif (yto is None): 
            yto = yfrom
        if (qfrom is None and dfrom is None): 
            qfrom = qto
        elif (qto is None and dto is None): 
            qto = qfrom
        if (qfrom is not None): 
            mfrom = (1 + (((qfrom - 1)) * 4))
        if (qto is not None): 
            mto = ((qto * 4) - 1)
        if (mfrom is None and (((dfrom is not None or mfrom is not None or hfrom is not None) or min_from != 0 or len(self.items_from) == 0))): 
            if (mto is not None): 
                mfrom = mto
            else: 
                mto = now.month
                mfrom = mto
        if (mto is None and (((dto is not None or mto is not None or hto is not None) or min_to is not None or len(self.items_to) == 0))): 
            if (mfrom is not None): 
                mto = mfrom
            else: 
                mto = now.month
                mfrom = mto
        if (mfrom is not None): 
            while mfrom > 12:
                yfrom += 1
                mfrom -= 12
            while mfrom <= 0:
                yfrom -= 1
                mfrom += 12
        else: 
            mfrom = 1
        if (mto is not None): 
            while mto > 12:
                yto += 1
                mto -= 12
            while mto <= 0:
                yto -= 1
                mto += 12
        else: 
            mto = 12
        if (dfrom is None and ((hfrom is not None or min_from is not None or len(self.items_from) == 0))): 
            if (dto is not None): 
                dfrom = dto
            else: 
                dto = now.day
                dfrom = dto
        if (dto is None and ((hto is not None or min_to is not None or len(self.items_to) == 0))): 
            if (dfrom is not None): 
                dto = dfrom
            else: 
                dto = now.day
                dfrom = dto
        if (dfrom is not None): 
            while dfrom > Utils.lastDayOfMonth(yfrom, mfrom):
                dfrom -= Utils.lastDayOfMonth(yfrom, mfrom)
                mfrom += 1
                if (mfrom > 12): 
                    mfrom = 1
                    yfrom += 1
            while dfrom <= 0:
                mfrom -= 1
                if (mfrom <= 0): 
                    mfrom = 12
                    yfrom -= 1
                dfrom += Utils.lastDayOfMonth(yfrom, mfrom)
        if (dto is not None): 
            while dto > Utils.lastDayOfMonth(yto, mto):
                dto -= Utils.lastDayOfMonth(yto, mto)
                mto += 1
                if (mto > 12): 
                    mto = 1
                    yto += 1
            while dto <= 0:
                mto -= 1
                if (mto <= 0): 
                    mto = 12
                    yto -= 1
                dto += Utils.lastDayOfMonth(yto, mto)
        elif (dfrom is not None and mfrom == mto and yfrom == yto): 
            dto = dfrom
        else: 
            dto = Utils.lastDayOfMonth(yto, mto)
        if (dfrom is None): 
            dfrom = 1
        try: 
            from0_.value = datetime.datetime(yfrom, mfrom, dfrom)
            to.value = datetime.datetime(yto, mto, dto)
        except Exception as ex: 
            from0_.value = datetime.datetime()
            to.value = datetime.datetime()
            return False
        if ((not yfrom_def and len(self.items_from) > 0 and Utils.getDate(from0_.value) > datetime.datetime.today()) and not can_be_future): 
            if (not yto_def and to.value.year == from0_.value.year): 
                to.value = (to.value + datetime.timedelta(days=-1*365))
            from0_.value = (from0_.value + datetime.timedelta(days=-1*365))
        if (hfrom is None and hto is not None): 
            hfrom = hto
        elif (hto is None and hfrom is not None): 
            hto = hfrom
        if (min_from is None and min_to is not None): 
            min_from = min_to
        elif (min_to is None and min_from is not None): 
            min_to = min_from
        if (hfrom is not None or min_from is not None): 
            if (hfrom is None): 
                hfrom = now.hour
            if (min_from is None): 
                min_from = 0
            while min_from >= 60:
                hfrom += 1
                min_from -= 60
            while min_from < 0:
                hfrom -= 1
                min_from += 60
            while hfrom >= 24:
                from0_.value = (from0_.value + datetime.timedelta(days=1))
                hfrom -= 24
            while hfrom < 0:
                from0_.value = (from0_.value + datetime.timedelta(days=-1))
                hfrom += 24
            from0_.value = ((from0_.value + datetime.timedelta(hours=hfrom)) + datetime.timedelta(minutes=min_from))
        if (hto is not None or min_to is not None): 
            if (hto is None): 
                hto = now.hour
            if (min_to is None): 
                min_to = 0
            while min_to >= 60:
                hto += 1
                min_to -= 60
            while min_to < 0:
                hto -= 1
                min_to += 60
            while hto >= 24:
                to.value = (to.value + datetime.timedelta(days=1))
                hto -= 24
            while hto < 0:
                to.value = (to.value + datetime.timedelta(days=-1))
                hto += 24
            to.value = ((to.value + datetime.timedelta(hours=hto)) + datetime.timedelta(minutes=min_to))
        return True
    
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
            from0_.value = self.__correct_hours(from0_, self.items_from, now)
            to.value = self.__correct_hours(to, self.items_to, now)
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
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        from pullenti.ner.date.DateReferent import DateReferent
        
        if (t is None): 
            return None
        res = None
        to_regime = False
        from_regime = False
        t0 = None
        tt = t
        first_pass2769 = True
        while True:
            if first_pass2769: first_pass2769 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            drr = (tt.get_referent() if isinstance(tt.get_referent(), DateRangeReferent) else None)
            if (drr is not None): 
                res = DateExToken._new656(t, tt, True)
                fr = drr.date_from
                if (fr is not None): 
                    DateExToken.__add_items(fr, res.items_from, tt)
                to = drr.date_to
                DateExToken.__add_items(to, res.items_to, tt)
                return res
            dr = (tt.get_referent() if isinstance(tt.get_referent(), DateReferent) else None)
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
            res.append(DateExToken.DateExItemToken._new657(tt, tt, DateExToken.DateExItemTokenType.YEAR, fr.year))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new658(tt, tt, DateExToken.DateExItemTokenType.YEAR, 0, True))
        if (fr.month > 0): 
            res.append(DateExToken.DateExItemToken._new657(tt, tt, DateExToken.DateExItemTokenType.MONTH, fr.month))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new658(tt, tt, DateExToken.DateExItemTokenType.MONTH, 0, True))
        if (fr.day > 0): 
            res.append(DateExToken.DateExItemToken._new657(tt, tt, DateExToken.DateExItemTokenType.DAY, fr.day))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new658(tt, tt, DateExToken.DateExItemTokenType.DAY, 0, True))

    
    @staticmethod
    def _new656(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'DateExToken':
        res = DateExToken(_arg1, _arg2)
        res.is_diap = _arg3
        return res