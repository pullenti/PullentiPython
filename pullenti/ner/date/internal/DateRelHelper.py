# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import operator
import datetime
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.date.internal.DateExToken import DateExToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent

class DateRelHelper:
    
    @staticmethod
    def create_referents(et : 'DateExToken') -> typing.List['ReferentToken']:
        if (not et.is_diap or len(et.items_to) == 0): 
            li = DateRelHelper.__create_refs(et.items_from)
            if (li is None or len(li) == 0): 
                return None
            return li
        li_fr = DateRelHelper.__create_refs(et.items_from)
        li_to = DateRelHelper.__create_refs(et.items_to)
        ra = DateRangeReferent()
        if (len(li_fr) > 0): 
            ra.date_from = Utils.asObjectOrNull(li_fr[0].tag, DateReferent)
        if (len(li_to) > 0): 
            ra.date_to = Utils.asObjectOrNull(li_to[0].tag, DateReferent)
        res = list()
        res.extend(li_fr)
        res.extend(li_to)
        res.append(ReferentToken(ra, et.begin_token, et.end_token))
        if (len(res) == 0): 
            return None
        res[0].tag = (ra)
        return res
    
    @staticmethod
    def __create_refs(its : typing.List['DateExItemToken']) -> typing.List['ReferentToken']:
        res = list()
        own = None
        i = 0
        first_pass3687 = True
        while True:
            if first_pass3687: first_pass3687 = False
            else: i += 1
            if (not (i < len(its))): break
            it = its[i]
            d = DateReferent()
            if (it.is_value_relate): 
                d.is_relative = True
            if (own is not None): 
                d.higher = own
            if (it.typ == DateExToken.DateExItemTokenType.DAY): 
                d.day = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                d.day_of_week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.HOUR): 
                d.hour = it.value
                if (((i + 1) < len(its)) and its[i + 1].typ == DateExToken.DateExItemTokenType.MINUTE and not its[i + 1].is_value_relate): 
                    d.minute = its[i + 1].value
                    i += 1
            elif (it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                d.minute = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.MONTH): 
                d.month = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.QUARTAL): 
                d.quartal = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.WEEK): 
                d.week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.YEAR): 
                d.year = it.value
            else: 
                continue
            res.append(ReferentToken(d, it.begin_token, it.end_token))
            own = d
            it.src = d
        if (len(res) > 0): 
            res[0].tag = (own)
        return res
    
    @staticmethod
    def __create_date_ex(dr : 'DateReferent') -> typing.List['DateExItemToken']:
        res = list()
        while dr is not None: 
            for s in dr.slots: 
                it = DateExToken.DateExItemToken._new742(None, None, DateExToken.DateExItemTokenType.UNDEFINED)
                if (dr.get_string_value(DateReferent.ATTR_ISRELATIVE) == "true"): 
                    it.is_value_relate = True
                if (s.type_name == DateReferent.ATTR_YEAR): 
                    it.typ = DateExToken.DateExItemTokenType.YEAR
                    wrapn743 = RefOutArgWrapper(0)
                    inoutres744 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn743)
                    n = wrapn743.value
                    if (inoutres744): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_QUARTAL): 
                    it.typ = DateExToken.DateExItemTokenType.QUARTAL
                    wrapn745 = RefOutArgWrapper(0)
                    inoutres746 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn745)
                    n = wrapn745.value
                    if (inoutres746): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MONTH): 
                    it.typ = DateExToken.DateExItemTokenType.MONTH
                    wrapn747 = RefOutArgWrapper(0)
                    inoutres748 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn747)
                    n = wrapn747.value
                    if (inoutres748): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_WEEK): 
                    it.typ = DateExToken.DateExItemTokenType.WEEK
                    wrapn749 = RefOutArgWrapper(0)
                    inoutres750 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn749)
                    n = wrapn749.value
                    if (inoutres750): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAYOFWEEK): 
                    it.typ = DateExToken.DateExItemTokenType.DAYOFWEEK
                    wrapn751 = RefOutArgWrapper(0)
                    inoutres752 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn751)
                    n = wrapn751.value
                    if (inoutres752): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAY): 
                    it.typ = DateExToken.DateExItemTokenType.DAY
                    wrapn753 = RefOutArgWrapper(0)
                    inoutres754 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn753)
                    n = wrapn753.value
                    if (inoutres754): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HOUR): 
                    it.typ = DateExToken.DateExItemTokenType.HOUR
                    wrapn755 = RefOutArgWrapper(0)
                    inoutres756 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn755)
                    n = wrapn755.value
                    if (inoutres756): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MINUTE): 
                    it.typ = DateExToken.DateExItemTokenType.MINUTE
                    wrapn757 = RefOutArgWrapper(0)
                    inoutres758 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn757)
                    n = wrapn757.value
                    if (inoutres758): 
                        it.value = n
                if (it.typ != DateExToken.DateExItemTokenType.UNDEFINED): 
                    res.insert(0, it)
            dr = dr.higher
        res.sort(key=operator.attrgetter('typ'))
        return res
    
    @staticmethod
    def calculate_date(dr : 'DateReferent', now : datetime.datetime, tense : int) -> datetime.datetime:
        if (dr.pointer == DatePointerType.TODAY): 
            return now
        if (not dr.is_relative and dr.dt is not None): 
            return dr.dt
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        return det.get_date(now, tense)
    
    @staticmethod
    def calculate_date_range(dr : 'DateReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        if (dr.pointer == DatePointerType.TODAY): 
            from0_.value = now
            to.value = now
            return True
        if (not dr.is_relative and dr.dt is not None): 
            to.value = dr.dt
            from0_.value = to.value
            return True
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        inoutres759 = det.get_dates(now, from0_, to, tense)
        return inoutres759
    
    @staticmethod
    def calculate_date_range2(dr : 'DateRangeReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.max
        if (dr.date_from is None): 
            if (dr.date_to is None): 
                return False
            wrapdt0760 = RefOutArgWrapper(None)
            wrapdt1761 = RefOutArgWrapper(None)
            inoutres762 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt0760, wrapdt1761, tense)
            dt0 = wrapdt0760.value
            dt1 = wrapdt1761.value
            if (not inoutres762): 
                return False
            to.value = dt1
            return True
        elif (dr.date_to is None): 
            wrapdt0763 = RefOutArgWrapper(None)
            wrapdt1764 = RefOutArgWrapper(None)
            inoutres765 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0763, wrapdt1764, tense)
            dt0 = wrapdt0763.value
            dt1 = wrapdt1764.value
            if (not inoutres765): 
                return False
            from0_.value = dt0
            return True
        wrapdt0769 = RefOutArgWrapper(None)
        wrapdt1770 = RefOutArgWrapper(None)
        inoutres771 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0769, wrapdt1770, tense)
        dt0 = wrapdt0769.value
        dt1 = wrapdt1770.value
        if (not inoutres771): 
            return False
        from0_.value = dt0
        wrapdt2766 = RefOutArgWrapper(None)
        wrapdt3767 = RefOutArgWrapper(None)
        inoutres768 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt2766, wrapdt3767, tense)
        dt2 = wrapdt2766.value
        dt3 = wrapdt3767.value
        if (not inoutres768): 
            return False
        to.value = dt3
        return True
    
    @staticmethod
    def append_to_string(dr : 'DateReferent', res : io.StringIO) -> None:
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0772 = RefOutArgWrapper(None)
        wrapdt1773 = RefOutArgWrapper(None)
        inoutres774 = DateRelHelper.calculate_date_range(dr, cur, wrapdt0772, wrapdt1773, 0)
        dt0 = wrapdt0772.value
        dt1 = wrapdt1773.value
        if (not inoutres774): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def append_to_string2(dr : 'DateRangeReferent', res : io.StringIO) -> None:
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0775 = RefOutArgWrapper(None)
        wrapdt1776 = RefOutArgWrapper(None)
        inoutres777 = DateRelHelper.calculate_date_range2(dr, cur, wrapdt0775, wrapdt1776, 0)
        dt0 = wrapdt0775.value
        dt1 = wrapdt1776.value
        if (not inoutres777): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def __append_dates(cur : datetime.datetime, dt0 : datetime.datetime, dt1 : datetime.datetime, res : io.StringIO) -> None:
        mon0 = dt0.month
        print(" ({0}.{1}.{2}".format(dt0.year, "{:02d}".format(mon0), "{:02d}".format(dt0.day)), end="", file=res, flush=True)
        if (dt0.hour > 0 or dt0.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(dt0.hour), "{:02d}".format(dt0.minute)), end="", file=res, flush=True)
        if (dt0 != dt1): 
            mon1 = dt1.month
            print("-{0}.{1}.{2}".format(dt1.year, "{:02d}".format(mon1), "{:02d}".format(dt1.day)), end="", file=res, flush=True)
            if (dt1.hour > 0 or dt1.minute > 0): 
                print(" {0}:{1}".format("{:02d}".format(dt1.hour), "{:02d}".format(dt1.minute)), end="", file=res, flush=True)
        monc = cur.month
        print(" отн. {0}.{1}.{2}".format(cur.year, "{:02d}".format(monc), "{:02d}".format(cur.day)), end="", file=res, flush=True)
        if (cur.hour > 0 or cur.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(cur.hour), "{:02d}".format(cur.minute)), end="", file=res, flush=True)
        print(")", end="", file=res)