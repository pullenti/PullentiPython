# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import datetime
import math
import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DatePointerType import DatePointerType

from pullenti.ner.core.NumberHelper import NumberHelper


class DateReferent(Referent):
    """ Сущность, представляющая дату """
    
    def __init__(self) -> None:
        from pullenti.ner.date.internal.MetaDate import MetaDate
        super().__init__(DateReferent.OBJ_TYPENAME)
        self.instance_of = MetaDate.GLOBAL_META
    
    OBJ_TYPENAME = "DATE"
    
    ATTR_CENTURY = "CENTURY"
    
    ATTR_YEAR = "YEAR"
    
    ATTR_MONTH = "MONTH"
    
    ATTR_DAY = "DAY"
    
    ATTR_DAYOFWEEK = "DAYOFWEEK"
    
    ATTR_HOUR = "HOUR"
    
    ATTR_MINUTE = "MINUTE"
    
    ATTR_SECOND = "SECOND"
    
    ATTR_HIGHER = "HIGHER"
    
    ATTR_POINTER = "POINTER"
    
    @property
    def dt(self) -> datetime.datetime:
        """ Дата в стандартной структуре .NET (null, если что-либо неопределено или дата некорректна) """
        if (self.year > 0 and self.month > 0 and self.day > 0): 
            if (self.month > 12): 
                return None
            if (self.day > Utils.lastDayOfMonth(self.year, self.month)): 
                return None
            h = self.hour
            m = self.minute
            s = self.second
            if (h < 0): 
                h = 0
            if (m < 0): 
                m = 0
            if (s < 0): 
                s = 0
            try: 
                return datetime.datetime(self.year, self.month, self.day, h, m, (s if s >= 0 and (s < 60) else 0))
            except Exception as ex: 
                pass
        return None
    
    @dt.setter
    def dt(self, value) -> datetime.datetime:
        return value
    
    @property
    def century(self) -> int:
        """ Век (0 - неопределён) """
        if (self.higher is not None): 
            return self.higher.century
        cent = self.get_int_value(DateReferent.ATTR_CENTURY, 0)
        if (cent != 0): 
            return cent
        year_ = self.year
        if (year_ > 0): 
            cent = (math.floor(year_ / 100))
            cent += 1
            return cent
        elif (year_ < 0): 
            cent = (math.floor(year_ / 100))
            cent -= 1
            return cent
        return 0
    
    @century.setter
    def century(self, value) -> int:
        self.add_slot(DateReferent.ATTR_CENTURY, value, True, 0)
        return value
    
    @property
    def year(self) -> int:
        """ Год (0 - неопределён) """
        if (self.higher is not None): 
            return self.higher.year
        else: 
            return self.get_int_value(DateReferent.ATTR_YEAR, 0)
    
    @year.setter
    def year(self, value) -> int:
        self.add_slot(DateReferent.ATTR_YEAR, value, True, 0)
        return value
    
    @property
    def month(self) -> int:
        """ Месяц (0 - неопределён) """
        if (self.find_slot(DateReferent.ATTR_MONTH, None, True) is None and self.higher is not None): 
            return self.higher.month
        else: 
            return self.get_int_value(DateReferent.ATTR_MONTH, 0)
    
    @month.setter
    def month(self, value) -> int:
        self.add_slot(DateReferent.ATTR_MONTH, value, True, 0)
        return value
    
    @property
    def day(self) -> int:
        """ День месяца (0 - неопределён) """
        if (self.find_slot(DateReferent.ATTR_DAY, None, True) is None and self.higher is not None): 
            return self.higher.day
        else: 
            return self.get_int_value(DateReferent.ATTR_DAY, 0)
    
    @day.setter
    def day(self, value) -> int:
        self.add_slot(DateReferent.ATTR_DAY, value, True, 0)
        return value
    
    @property
    def day_of_week(self) -> int:
        """ День недели (0 - неопределён, 1 - понедельник ...) """
        if (self.find_slot(DateReferent.ATTR_DAYOFWEEK, None, True) is None and self.higher is not None): 
            return self.higher.day_of_week
        else: 
            return self.get_int_value(DateReferent.ATTR_DAYOFWEEK, 0)
    
    @day_of_week.setter
    def day_of_week(self, value) -> int:
        self.add_slot(DateReferent.ATTR_DAYOFWEEK, value, True, 0)
        return value
    
    @property
    def hour(self) -> int:
        """ Час (-1 - неопределён) """
        return self.get_int_value(DateReferent.ATTR_HOUR, -1)
    
    @hour.setter
    def hour(self, value) -> int:
        self.add_slot(DateReferent.ATTR_HOUR, value, True, 0)
        return value
    
    @property
    def minute(self) -> int:
        """ Минуты (-1 - неопределён) """
        return self.get_int_value(DateReferent.ATTR_MINUTE, -1)
    
    @minute.setter
    def minute(self, value) -> int:
        self.add_slot(DateReferent.ATTR_MINUTE, value, True, 0)
        return value
    
    @property
    def second(self) -> int:
        """ Секунд (-1 - неопределён) """
        return self.get_int_value(DateReferent.ATTR_SECOND, -1)
    
    @second.setter
    def second(self, value) -> int:
        self.add_slot(DateReferent.ATTR_SECOND, value, True, 0)
        return value
    
    @property
    def higher(self) -> 'DateReferent':
        """ Вышестоящая дата """
        return (self.get_value(DateReferent.ATTR_HIGHER) if isinstance(self.get_value(DateReferent.ATTR_HIGHER), DateReferent) else None)
    
    @higher.setter
    def higher(self, value) -> 'DateReferent':
        self.add_slot(DateReferent.ATTR_HIGHER, value, True, 0)
        return value
    
    @property
    def pointer(self) -> 'DatePointerType':
        """ Дополнительный указатель примерной даты """
        s = self.get_string_value(DateReferent.ATTR_POINTER)
        if (s is None): 
            return DatePointerType.NO
        try: 
            res = Utils.valToEnum(s, DatePointerType)
            if (isinstance(res, DatePointerType)): 
                return Utils.valToEnum(res, DatePointerType)
        except Exception as ex741: 
            pass
        return DatePointerType.NO
    
    @pointer.setter
    def pointer(self, value) -> 'DatePointerType':
        if (value != DatePointerType.NO): 
            self.add_slot(DateReferent.ATTR_POINTER, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.higher
    
    @staticmethod
    def _can_be_higher(hi : 'DateReferent', lo : 'DateReferent') -> bool:
        if (lo is None or hi is None): 
            return False
        if (lo.higher == hi): 
            return True
        if (lo.higher is not None and lo.higher.can_be_equals(hi, Referent.EqualType.WITHINONETEXT)): 
            return True
        if (lo.higher is not None): 
            return False
        if (lo.hour >= 0): 
            if (hi.hour >= 0): 
                return False
            if (lo.day > 0): 
                return False
            return True
        if (hi.year > 0 and lo.year <= 0): 
            if (hi.month > 0): 
                return False
            return True
        return False
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        return self._to_string(short_variant, lang, lev, 0)
    
    def _to_string(self, short_variant : bool, lang : 'MorphLang', lev : int, from_range : int) -> str:
        from pullenti.ner.date.internal.MetaDate import MetaDate
        res = Utils.newStringIO(None)
        p = self.pointer
        if (from_range == 1): 
            print("{0} ".format(("з" if lang.is_ua else ("from" if lang.is_en else "с"))), end="", file=res, flush=True)
        elif (from_range == 2): 
            print(("to " if lang.is_en else "по ").format(), end="", file=res, flush=True)
        if (p != DatePointerType.NO): 
            val = MetaDate.POINTER.convert_inner_value_to_outer_value(Utils.enumToString(p), lang)
            if (from_range == 0 or lang.is_en): 
                pass
            elif (from_range == 1): 
                if (p == DatePointerType.BEGIN): 
                    val = ("початку" if lang.is_ua else "начала")
                elif (p == DatePointerType.CENTER): 
                    val = ("середини" if lang.is_ua else "середины")
                elif (p == DatePointerType.END): 
                    val = ("кінця" if lang.is_ua else "конца")
                elif (p == DatePointerType.TODAY): 
                    val = ("цього часу" if lang.is_ua else "настоящего времени")
            elif (from_range == 2): 
                if (p == DatePointerType.BEGIN): 
                    val = ("початок" if lang.is_ua else "начало")
                elif (p == DatePointerType.CENTER): 
                    val = ("середину" if lang.is_ua else "середину")
                elif (p == DatePointerType.END): 
                    val = ("кінець" if lang.is_ua else "конец")
                elif (p == DatePointerType.TODAY): 
                    val = ("теперішній час" if lang.is_ua else "настоящее время")
            print("{0} ".format(val), end="", file=res, flush=True)
        if (self.day_of_week > 0): 
            if (lang.is_en): 
                print("{0}, ".format(DateReferent.__m_week_day_en[self.day_of_week - 1]), end="", file=res, flush=True)
            else: 
                print("{0}, ".format(DateReferent.__m_week_day[self.day_of_week - 1]), end="", file=res, flush=True)
        y = self.year
        m = self.month
        d = self.day
        cent = self.century
        if (y == 0 and cent != 0): 
            is_bc = cent < 0
            if (cent < 0): 
                cent = (- cent)
            print(NumberHelper.get_number_roman(cent), end="", file=res)
            if (lang.is_ua): 
                print(" century", end="", file=res)
            elif (m > 0 or p != DatePointerType.NO or from_range == 1): 
                print((" віка" if lang.is_ua else " века"), end="", file=res)
            else: 
                print((" вік" if lang.is_ua else " век"), end="", file=res)
            if (is_bc): 
                print((" до н.е." if lang.is_ua else " до н.э."), end="", file=res)
            return Utils.toStringStringIO(res)
        if (d > 0): 
            print(d, end="", file=res)
        if (m > 0 and m <= 12): 
            if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) != ' '): 
                print(' ', end="", file=res)
            if (lang.is_ua): 
                print((DateReferent.__m_monthua[m - 1] if d > 0 or p != DatePointerType.NO or from_range != 0 else DateReferent.__m_month0ua[m - 1]), end="", file=res)
            elif (lang.is_en): 
                print(DateReferent.__m_monthen[m - 1], end="", file=res)
            else: 
                print((DateReferent.__m_month[m - 1] if d > 0 or p != DatePointerType.NO or from_range != 0 else DateReferent.__m_month0[m - 1]), end="", file=res)
        if (y != 0): 
            is_bc = y < 0
            if (y < 0): 
                y = (- y)
            if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) != ' '): 
                print(' ', end="", file=res)
            if (lang.is_en): 
                print("{0}".format(y), end="", file=res, flush=True)
            elif (short_variant): 
                print("{0}{1}".format(y, ("р" if lang.is_ua else "г")), end="", file=res, flush=True)
            elif (m > 0 or p != DatePointerType.NO or from_range == 1): 
                print("{0} {1}".format(y, ("року" if lang.is_ua else "года")), end="", file=res, flush=True)
            else: 
                print("{0} {1}".format(y, ("рік" if lang.is_ua else "год")), end="", file=res, flush=True)
            if (is_bc): 
                print((" до н.е." if lang.is_ua else ("BC" if lang.is_en else " до н.э.")), end="", file=res)
        h = self.hour
        mi = self.minute
        se = self.second
        if (h >= 0 and mi >= 0): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print("{0}:{1}".format("{:02d}".format(h), "{:02d}".format(mi)), end="", file=res, flush=True)
            if (se >= 0): 
                print(":{0}".format("{:02d}".format(se)), end="", file=res, flush=True)
        if (res.tell() == 0): 
            return "?"
        while Utils.getCharAtStringIO(res, res.tell() - 1) == ' ' or Utils.getCharAtStringIO(res, res.tell() - 1) == ',':
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res).strip()
    
    __m_month = None
    
    __m_month0 = None
    
    __m_monthen = None
    
    __m_monthua = None
    
    __m_month0ua = None
    
    __m_week_day = None
    
    __m_week_day_en = None
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        sd = (obj if isinstance(obj, DateReferent) else None)
        if (sd is None): 
            return False
        if (sd.century != self.century): 
            return False
        if (sd.year != self.year): 
            return False
        if (sd.month != self.month): 
            return False
        if (sd.day != self.day): 
            return False
        if (sd.hour != self.hour): 
            return False
        if (sd.minute != self.minute): 
            return False
        if (sd.second != self.second): 
            return False
        if (sd.pointer != self.pointer): 
            return False
        if (sd.day_of_week > 0 and self.day_of_week > 0): 
            if (sd.day_of_week != self.day_of_week): 
                return False
        return True
    
    @staticmethod
    def compare(d1 : 'DateReferent', d2 : 'DateReferent') -> int:
        if (d1.year < d2.year): 
            return -1
        if (d1.year > d2.year): 
            return 1
        if (d1.month < d2.month): 
            return -1
        if (d1.month > d2.month): 
            return 1
        if (d1.day < d2.day): 
            return -1
        if (d1.day > d2.day): 
            return 1
        if (d1.hour < d2.hour): 
            return -1
        if (d1.hour > d2.hour): 
            return 1
        if (d1.minute < d2.minute): 
            return -1
        if (d1.minute > d2.minute): 
            return 1
        if (d1.second > d2.second): 
            return -1
        if (d1.second < d2.second): 
            return 1
        return 0
    
    @staticmethod
    def is_month_defined(obj : 'Referent') -> bool:
        """ Проверка, что дата или диапазон определены с точностью до одного месяца
        
        Args:
            obj(Referent): 
        
        """
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        sd = (obj if isinstance(obj, DateReferent) else None)
        if (sd is not None): 
            return (sd.year > 0 and sd.month > 0)
        sdr = (obj if isinstance(obj, DateRangeReferent) else None)
        if (sdr is not None): 
            if (sdr.date_from is None or sdr.date_to is None): 
                return False
            if (sdr.date_from.year == 0 or sdr.date_to.year != sdr.date_from.year): 
                return False
            if (sdr.date_from.month == 0 or sdr.date_to.month != sdr.date_from.month): 
                return False
            return True
        return False

    
    @staticmethod
    def _new678(_arg1 : 'DateReferent', _arg2 : int) -> 'DateReferent':
        res = DateReferent()
        res.higher = _arg1
        res.day = _arg2
        return res
    
    @staticmethod
    def _new679(_arg1 : int, _arg2 : int) -> 'DateReferent':
        res = DateReferent()
        res.month = _arg1
        res.day = _arg2
        return res
    
    @staticmethod
    def _new680(_arg1 : int) -> 'DateReferent':
        res = DateReferent()
        res.year = _arg1
        return res
    
    @staticmethod
    def _new683(_arg1 : int, _arg2 : int) -> 'DateReferent':
        res = DateReferent()
        res.hour = _arg1
        res.minute = _arg2
        return res
    
    @staticmethod
    def _new684(_arg1 : 'DatePointerType') -> 'DateReferent':
        res = DateReferent()
        res.pointer = _arg1
        return res
    
    @staticmethod
    def _new696(_arg1 : int, _arg2 : 'DateReferent') -> 'DateReferent':
        res = DateReferent()
        res.month = _arg1
        res.higher = _arg2
        return res
    
    @staticmethod
    def _new701(_arg1 : int, _arg2 : 'DateReferent') -> 'DateReferent':
        res = DateReferent()
        res.day = _arg1
        res.higher = _arg2
        return res
    
    @staticmethod
    def _new717(_arg1 : int) -> 'DateReferent':
        res = DateReferent()
        res.month = _arg1
        return res
    
    @staticmethod
    def _new718(_arg1 : int) -> 'DateReferent':
        res = DateReferent()
        res.century = _arg1
        return res
    
    @staticmethod
    def _new724(_arg1 : int) -> 'DateReferent':
        res = DateReferent()
        res.day = _arg1
        return res
    
    @staticmethod
    def _new726(_arg1 : 'DateReferent') -> 'DateReferent':
        res = DateReferent()
        res.higher = _arg1
        return res
    
    @staticmethod
    def _new727(_arg1 : 'DateReferent', _arg2 : int) -> 'DateReferent':
        res = DateReferent()
        res.higher = _arg1
        res.month = _arg2
        return res
    
    @staticmethod
    def _new736(_arg1 : int) -> 'DateReferent':
        res = DateReferent()
        res.day_of_week = _arg1
        return res
    
    # static constructor for class DateReferent
    @staticmethod
    def _static_ctor():
        DateReferent.__m_month = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
        DateReferent.__m_month0 = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
        DateReferent.__m_monthen = ["jan", "fab", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        DateReferent.__m_monthua = ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"]
        DateReferent.__m_month0ua = ["січень", "лютий", "березень", "квітень", "травень", "червень", "липень", "серпень", "вересень", "жовтень", "листопад", "грудень"]
        DateReferent.__m_week_day = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        DateReferent.__m_week_day_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DateReferent._static_ctor()