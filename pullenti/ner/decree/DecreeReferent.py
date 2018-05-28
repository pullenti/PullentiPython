# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
import datetime
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.decree.internal.DecreeHelper import DecreeHelper


from pullenti.ner.core.IntOntologyItem import IntOntologyItem


class DecreeReferent(Referent):
    """ Сущность, представляющая ссылку на НПА """
    
    def __init__(self) -> None:
        from pullenti.ner.decree.internal.MetaDecree import MetaDecree
        super().__init__(DecreeReferent.OBJ_TYPENAME)
        self.instance_of = MetaDecree.GLOBAL_META
    
    OBJ_TYPENAME = "DECREE"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_DATE = "DATE"
    
    ATTR_SOURCE = "SOURCE"
    
    ATTR_GEO = "GEO"
    
    ATTR_READING = "READING"
    
    ATTR_CASENUMBER = "CASENUMBER"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = Utils.newStringIO(None)
        ki = self.kind
        out_part = False
        nam = self.name
        if (self.typ is not None): 
            if ((nam is not None and not nam.startswith("О") and self.typ in nam) and ki != DecreeKind.STANDARD): 
                print(MiscHelper.convert_first_char_upper_and_other_lower(nam), end="", file=res)
                nam = None
            elif (ki == DecreeKind.STANDARD and (len(self.typ) < 6)): 
                print(self.typ, end="", file=res)
            else: 
                print(MiscHelper.convert_first_char_upper_and_other_lower(self.typ), end="", file=res)
        else: 
            print("?", end="", file=res)
        out_src = True
        if (ki == DecreeKind.CONTRACT and self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
            srcs = list()
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_SOURCE): 
                    srcs.append(str(s.value))
            if (len(srcs) > 1): 
                for ii in range(len(srcs)):
                    if (ii > 0 and ((ii + 1) < len(srcs))): 
                        print(", ", end="", file=res)
                    elif (ii > 0): 
                        print(" и ", end="", file=res)
                    else: 
                        print(" между ", end="", file=res)
                    print(srcs[ii], end="", file=res)
                    out_src = False
        num = self.number
        if (num is not None): 
            print(" № {0}".format(num), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                    nn = str(s.value)
                    if (nn != num): 
                        print("/{0}".format(nn), end="", file=res, flush=True)
        num = self.case_number
        if ((num) is not None): 
            print(" по делу № {0}".format(num), end="", file=res, flush=True)
        if (self.get_string_value(DecreeReferent.ATTR_DATE) is not None): 
            print(" {0}{1}".format(("" if ki == DecreeKind.PROGRAM else "от "), self.get_string_value(DecreeReferent.ATTR_DATE)), end="", file=res, flush=True)
        if (out_src and self.get_value(DecreeReferent.ATTR_SOURCE) is not None): 
            print("; {0}".format(self.get_string_value(DecreeReferent.ATTR_SOURCE)), end="", file=res, flush=True)
        if (not short_variant): 
            s = self.get_string_value(DecreeReferent.ATTR_GEO)
            if (s is not None): 
                print("; {0}".format(s), end="", file=res, flush=True)
            if (nam is not None): 
                s = self.__get_short_name()
                if (s is not None): 
                    print("; \"{0}\"".format(s), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def name(self) -> str:
        """ Наименование (если несколько, то самое короткое) """
        nam = None
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_NAME): 
                n = str(s.value)
                if (nam is None or len(nam) > len(n)): 
                    nam = n
        return nam
    
    def __get_short_name(self) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        nam = self.name
        if (nam is None): 
            return None
        if (len(nam) > 100): 
            i = 100
            while i < len(nam): 
                if (not nam[i].isalpha()): 
                    break
                i += 1
            if (i < len(nam)): 
                nam = (nam[0 : (i)] + "...")
        return MiscHelper.convert_first_char_upper_and_other_lower(nam)
    
    def get_compare_strings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_NAME or s.type_name == DecreeReferent.ATTR_NUMBER): 
                res.append(str(s.value))
        if (len(res) == 0 and self.typ is not None): 
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_GEO): 
                    res.append("{0} {1}".format(self.typ, str(s.value)))
        if (self.typ == "КОНСТИТУЦИЯ"): 
            res.append(self.typ)
        if (len(res) > 0): 
            return res
        else: 
            return super().get_compare_strings()
    
    @property
    def date(self) -> datetime.datetime:
        """ Дата подписания (для законов дат может быть много - по редакциям) """
        s = self.get_string_value(DecreeReferent.ATTR_DATE)
        if (s is None): 
            return None
        return DecreeHelper.parse_date_time(s)
    
    def _add_date(self, dt : 'DecreeToken') -> bool:
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        if (dt is None): 
            return False
        if (dt.ref is not None and isinstance(dt.ref.referent, DateReferent)): 
            dr = (dt.ref.referent if isinstance(dt.ref.referent, DateReferent) else None)
            year = dr.year
            mon = dr.month
            day = dr.day
            if (year == 0): 
                return False
            tmp = Utils.newStringIO(None)
            print(year, end="", file=tmp)
            if (mon > 0): 
                print(".{0}".format("{:02d}".format(mon)), end="", file=tmp, flush=True)
            if (day > 0): 
                print(".{0}".format("{:02d}".format(day)), end="", file=tmp, flush=True)
            self.add_slot(DecreeReferent.ATTR_DATE, Utils.toStringStringIO(tmp), False, 0)
            return True
        if (dt.ref is not None and isinstance(dt.ref.referent, DateRangeReferent)): 
            self.add_slot(DecreeReferent.ATTR_DATE, dt.ref.referent, False, 0)
            return True
        if (dt.value is not None): 
            self.add_slot(DecreeReferent.ATTR_DATE, dt.value, False, 0)
            return True
        return False
    
    def __all_years(self) -> typing.List[int]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_DATE): 
                str0 = str(s.value)
                i = str0.find('.')
                if (i == 4): 
                    str0 = str0[0 : 4]
                inoutarg1038 = RefOutArgWrapper(None)
                inoutres1039 = Utils.tryParseInt(str0, inoutarg1038)
                i = inoutarg1038.value
                if (inoutres1039): 
                    res.append(i)
        return res
    
    @property
    def typ(self) -> str:
        """ Тип """
        return self.get_string_value(DecreeReferent.ATTR_TYPE)
    
    @typ.setter
    def typ(self, value) -> str:
        self.add_slot(DecreeReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def kind(self) -> 'DecreeKind':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        return DecreeToken.get_kind(self.typ)
    
    @property
    def is_law(self) -> bool:
        """ Признак того, что это именно закон, а не подзаконный акт.
         Для законов возможны несколько номеров и дат (редакций) """
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        return DecreeToken.is_law(self.typ)
    
    @property
    def typ0(self) -> str:
        typ_ = self.typ
        if (typ_ is None): 
            return None
        i = typ_.rfind(' ')
        if (i < 0): 
            return typ_
        if (typ_.startswith("ПАСПОРТ")): 
            return "ПАСПОРТ"
        if (typ_.startswith("ОСНОВЫ") or typ_.startswith("ОСНОВИ")): 
            i = typ_.find(' ')
            return typ_[0 : (i)]
        return typ_[i + 1 : ]
    
    @property
    def number(self) -> str:
        """ Номер (для законов номеров может быть много) """
        return self.get_string_value(DecreeReferent.ATTR_NUMBER)
    
    @property
    def case_number(self) -> str:
        return self.get_string_value(DecreeReferent.ATTR_CASENUMBER)
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        from pullenti.ner.decree.internal.PartToken import PartToken
        
        if (isinstance(attr_value, PartToken.PartValue)): 
            attr_value = (attr_value if isinstance(attr_value, PartToken.PartValue) else None).value
        s = super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
        if (isinstance(attr_value, PartToken.PartValue)): 
            s.tag = (attr_value if isinstance(attr_value, PartToken.PartValue) else None).source_value
        return s
    
    def _add_number(self, dt : 'DecreeToken') -> None:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        if (dt.typ == DecreeToken.ItemType.NUMBER): 
            if (dt.num_year > 0): 
                self.add_slot(DecreeReferent.ATTR_DATE, str(dt.num_year), False, 0)
        if (Utils.isNullOrEmpty(dt.value)): 
            return
        value = dt.value
        if ((value[len(value) - 1]) in ".,"): 
            value = value[0 : (len(value) - 1)]
        self.add_slot(DecreeReferent.ATTR_NUMBER, value, False, 0)
    
    def _add_name(self, dr : 'DecreeReferent') -> None:
        s = dr.find_slot(DecreeReferent.ATTR_NAME, None, True)
        if (s is None): 
            return
        ss = self.add_slot(DecreeReferent.ATTR_NAME, s.value, False, 0)
        if (ss is not None and ss.tag is None): 
            ss.tag = s.tag
    
    def _add_name_str(self, name_ : str) -> None:
        if (name_ is None or len(name_) == 0): 
            return
        if (name_[len(name_) - 1] == '.'): 
            if (len(name_) > 5 and name_[len(name_) - 2].isalpha() and not name_[len(name_) - 3].isalpha()): 
                pass
            else: 
                name_ = name_[0 : (len(name_) - 1)]
        name_ = name_.strip()
        uname = name_.upper()
        s = self.add_slot(DecreeReferent.ATTR_NAME, uname, False, 0)
        if (uname != name_): 
            s.tag = name_
    
    def __get_number_digits(self, num : str) -> str:
        if (num is None): 
            return ""
        tmp = Utils.newStringIO(None)
        for i in range(len(num)):
            if (num[i].isdigit()): 
                if (num[i] == '0' and tmp.tell() == 0): 
                    pass
                elif (num[i] == '3' and tmp.tell() > 0 and num[i - 1] == 'Ф'): 
                    pass
                else: 
                    print(num[i], end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    def __all_number_digits(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                res.append(self.__get_number_digits(s.value if isinstance(s.value, str) else None))
        return res
    
    def __all_dates(self) -> typing.List[datetime.datetime]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_DATE): 
                dt = DecreeHelper.parse_date_time(s.value if isinstance(s.value, str) else None)
                if (dt is not None): 
                    res.append(dt)
        return res
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType') -> bool:
        b = self.__can_be_equals(obj, typ_, False)
        return b
    
    def __can_be_equals(self, obj : 'Referent', typ_ : 'EqualType', ignore_geo : bool) -> bool:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        dr = (obj if isinstance(obj, DecreeReferent) else None)
        if (dr is None): 
            return False
        if (dr.typ0 is not None and self.typ0 is not None): 
            if (dr.typ0 != self.typ0): 
                return False
        num_eq = 0
        if (self.number is not None or dr.number is not None): 
            if (self.number is not None and dr.number is not None): 
                di1 = self.__all_number_digits()
                di2 = dr.__all_number_digits()
                for d1 in di1: 
                    if (d1 in di2): 
                        num_eq = 1
                        break
                if (num_eq == 0 and not self.is_law): 
                    return False
                for s in self.slots: 
                    if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                        if (dr.find_slot(s.type_name, s.value, True) is not None): 
                            num_eq = 2
                            break
                if (num_eq == 0): 
                    return False
        if (self.case_number is not None and dr.case_number is not None): 
            if (self.case_number != dr.case_number): 
                return False
        if (self.find_slot(DecreeReferent.ATTR_GEO, None, True) is not None and dr.find_slot(DecreeReferent.ATTR_GEO, None, True) is not None): 
            if (self.get_string_value(DecreeReferent.ATTR_GEO) != dr.get_string_value(DecreeReferent.ATTR_GEO)): 
                return False
        src_eq = False
        src_not_eq = False
        src = self.find_slot(DecreeReferent.ATTR_SOURCE, None, True)
        if (src is not None and dr.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
            if (dr.find_slot(src.type_name, src.value, True) is None): 
                src_not_eq = True
            else: 
                src_eq = True
        date_not_eq = False
        date_is_equ = False
        years_is_equ = False
        date1 = self.get_string_value(DecreeReferent.ATTR_DATE)
        date2 = dr.get_string_value(DecreeReferent.ATTR_DATE)
        if (date1 is not None or date2 is not None): 
            if (self.is_law): 
                ys1 = self.__all_years()
                ys2 = dr.__all_years()
                for y1 in ys1: 
                    if (y1 in ys2): 
                        years_is_equ = True
                        break
                if (years_is_equ): 
                    dts1 = self.__all_dates()
                    dts2 = dr.__all_dates()
                    for d1 in dts1: 
                        if (d1 in dts2): 
                            date_is_equ = True
                            break
                if (not date_is_equ and self.date is not None and dr.date is not None): 
                    date_not_eq = True
            elif (date1 == date2 or ((self.date is not None and dr.date is not None and self.date == dr.date))): 
                if (num_eq > 1): 
                    return True
                date_is_equ = True
            elif (self.date is not None and dr.date is not None): 
                if (self.date.year != dr.date.year): 
                    return False
                if (num_eq >= 1): 
                    if (src_eq): 
                        return True
                    if (src_not_eq): 
                        return False
                else: 
                    return False
            elif (typ_ == Referent.EqualType.DIFFERENTTEXTS or self.kind == DecreeKind.PUBLISHER): 
                date_not_eq = True
        if (self.find_slot(DecreeReferent.ATTR_NAME, None, True) is not None and dr.find_slot(DecreeReferent.ATTR_NAME, None, True) is not None): 
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_NAME): 
                    if (dr.find_slot(s.type_name, s.value, True) is not None): 
                        return True
                    for ss in dr.slots: 
                        if (ss.type_name == s.type_name): 
                            n0 = str(s.value)
                            n1 = str(ss.value)
                            if (n0.startswith(n1) or n1.startswith(n0)): 
                                return True
            if (date_not_eq): 
                return False
            if (self.is_law and not date_is_equ): 
                return False
            if (num_eq > 0): 
                if (src_eq): 
                    return True
                if (src_not_eq and typ_ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
                elif ((not src_not_eq and num_eq > 1 and self.date is None) and dr.date is None): 
                    return True
                return False
        elif (self.is_law and date_not_eq): 
            return False
        if (date_not_eq): 
            return False
        ty = self.typ
        if (ty is None): 
            return num_eq > 0
        t = DecreeToken.get_kind(ty)
        if (t == DecreeKind.USTAV or ty == "КОНСТИТУЦИЯ"): 
            return True
        if (num_eq > 0): 
            return True
        if (self.__str__() == str(obj)): 
            return True
        return False
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (not self.__can_be_equals(obj, Referent.EqualType.WITHINONETEXT, True)): 
            return False
        g1 = (self.get_value(DecreeReferent.ATTR_GEO) if isinstance(self.get_value(DecreeReferent.ATTR_GEO), GeoReferent) else None)
        g2 = (obj.get_value(DecreeReferent.ATTR_GEO) if isinstance(obj.get_value(DecreeReferent.ATTR_GEO), GeoReferent) else None)
        if (g1 is None and g2 is not None): 
            return True
        return False
    
    def _check_correction(self, noun_is_doubtful : bool) -> bool:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        typ_ = self.typ0
        if (typ_ is None): 
            return False
        if (typ_ == "КОНСТИТУЦИЯ" or typ_ == "КОНСТИТУЦІЯ"): 
            return True
        if ((typ_ == "КОДЕКС" or typ_ == "ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА" or typ_ == "ПРОГРАММА") or typ_ == "ОСНОВИ ЗАКОНОДАВСТВА" or typ_ == "ПРОГРАМА"): 
            if (self.find_slot(DecreeReferent.ATTR_NAME, None, True) is None): 
                return False
            if (self.find_slot(DecreeReferent.ATTR_GEO, None, True) is not None): 
                return True
            return not noun_is_doubtful
        if (typ_.startswith("ОСНОВ")): 
            if (self.find_slot(DecreeReferent.ATTR_GEO, None, True) is not None): 
                return True
            return False
        if ("ЗАКОН" in typ_): 
            if (self.find_slot(DecreeReferent.ATTR_NAME, None, True) is None and self.number is None): 
                return False
            return True
        if (((("ОПРЕДЕЛЕНИЕ" in typ_ or "РЕШЕНИЕ" in typ_ or "ПОСТАНОВЛЕНИЕ" in typ_) or "ПРИГОВОР" in typ_ or "ВИЗНАЧЕННЯ" in typ_) or "РІШЕННЯ" in typ_ or "ПОСТАНОВА" in typ_) or "ВИРОК" in typ_): 
            if (self.number is not None): 
                if (self.find_slot(DecreeReferent.ATTR_DATE, None, True) is not None or self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                    return True
            elif (self.find_slot(DecreeReferent.ATTR_DATE, None, True) is not None and self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                return True
            return False
        ty = DecreeToken.get_kind(typ_)
        if (ty == DecreeKind.USTAV): 
            if (self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                return True
        if (ty == DecreeKind.KONVENTION): 
            if (self.find_slot(DecreeReferent.ATTR_NAME, None, True) is not None): 
                if (typ_ != "ДОГОВОР" and typ_ != "ДОГОВІР"): 
                    return True
        if (ty == DecreeKind.STANDARD): 
            if (self.number is not None): 
                return True
        if (self.number is None): 
            if (self.find_slot(DecreeReferent.ATTR_NAME, None, True) is None or self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is None or self.find_slot(DecreeReferent.ATTR_DATE, None, True) is None): 
                if (ty == DecreeKind.CONTRACT and self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is not None and self.find_slot(DecreeReferent.ATTR_DATE, None, True) is not None): 
                    pass
                elif (self.find_slot(DecreeReferent.ATTR_NAME, "ПРАВИЛА ДОРОЖНОГО ДВИЖЕНИЯ", True) is not None): 
                    pass
                elif (self.find_slot(DecreeReferent.ATTR_NAME, "ПРАВИЛА ДОРОЖНЬОГО РУХУ", True) is not None): 
                    pass
                else: 
                    return False
        else: 
            if ((typ_ == "ПАСПОРТ" or typ_ == "ГОСТ" or typ_ == "ПБУ") or typ_ == "ФОРМА"): 
                return True
            if (self.find_slot(DecreeReferent.ATTR_SOURCE, None, True) is None and self.find_slot(DecreeReferent.ATTR_DATE, None, True) is None and self.find_slot(DecreeReferent.ATTR_NAME, None, True) is None): 
                return False
        return True
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
        i = 0
        while i < (len(self.slots) - 1): 
            j = i + 1
            while j < len(self.slots): 
                if (self.slots[i].type_name == self.slots[j].type_name and self.slots[i].value == self.slots[j].value): 
                    del self.slots[j]
                    j -= 1
                j += 1
            i += 1
        nums = self.get_string_values(DecreeReferent.ATTR_NUMBER)
        if (len(nums) > 1): 
            nums.sort()
            i = 0
            while i < (len(nums) - 1): 
                if (nums[i + 1].startswith(nums[i]) and len(nums[i + 1]) > len(nums[i]) and not nums[i + 1][len(nums[i])].isdigit()): 
                    s = self.find_slot(DecreeReferent.ATTR_NUMBER, nums[i], True)
                    if (s is not None): 
                        self.slots.remove(s)
                    del nums[i]
                    i -= 1
                i += 1
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        from pullenti.ner.core.Termin import Termin
        oi = IntOntologyItem(self)
        vars0 = list()
        for a in self.slots: 
            if (a.type_name == DecreeReferent.ATTR_NAME): 
                s = str(a.value)
                if (not s in vars0): 
                    vars0.append(s)
        if (self.number is not None): 
            for digs in self.__all_number_digits(): 
                if (not digs in vars0): 
                    vars0.append(digs)
        for v in vars0: 
            oi.termins.append(Termin(v))
        return oi

    
    @staticmethod
    def _new1022(_arg1 : str) -> 'DecreeReferent':
        res = DecreeReferent()
        res.typ = _arg1
        return res