# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

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
        first_pass3567 = True
        while True:
            if first_pass3567: first_pass3567 = False
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
                it = DateExToken.DateExItemToken._new676(None, None, DateExToken.DateExItemTokenType.UNDEFINED)
                if (dr.get_string_value(DateReferent.ATTR_ISRELATIVE) == "true"): 
                    it.is_value_relate = True
                if (s.type_name == DateReferent.ATTR_YEAR): 
                    it.typ = DateExToken.DateExItemTokenType.YEAR
                    wrapn677 = RefOutArgWrapper(0)
                    inoutres678 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn677)
                    n = wrapn677.value
                    if (inoutres678): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_QUARTAL): 
                    it.typ = DateExToken.DateExItemTokenType.QUARTAL
                    wrapn679 = RefOutArgWrapper(0)
                    inoutres680 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn679)
                    n = wrapn679.value
                    if (inoutres680): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MONTH): 
                    it.typ = DateExToken.DateExItemTokenType.MONTH
                    wrapn681 = RefOutArgWrapper(0)
                    inoutres682 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn681)
                    n = wrapn681.value
                    if (inoutres682): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_WEEK): 
                    it.typ = DateExToken.DateExItemTokenType.WEEK
                    wrapn683 = RefOutArgWrapper(0)
                    inoutres684 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn683)
                    n = wrapn683.value
                    if (inoutres684): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAYOFWEEK): 
                    it.typ = DateExToken.DateExItemTokenType.DAYOFWEEK
                    wrapn685 = RefOutArgWrapper(0)
                    inoutres686 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn685)
                    n = wrapn685.value
                    if (inoutres686): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAY): 
                    it.typ = DateExToken.DateExItemTokenType.DAY
                    wrapn687 = RefOutArgWrapper(0)
                    inoutres688 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn687)
                    n = wrapn687.value
                    if (inoutres688): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HOUR): 
                    it.typ = DateExToken.DateExItemTokenType.HOUR
                    wrapn689 = RefOutArgWrapper(0)
                    inoutres690 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn689)
                    n = wrapn689.value
                    if (inoutres690): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MINUTE): 
                    it.typ = DateExToken.DateExItemTokenType.MINUTE
                    wrapn691 = RefOutArgWrapper(0)
                    inoutres692 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn691)
                    n = wrapn691.value
                    if (inoutres692): 
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
        inoutres693 = det.get_dates(now, from0_, to, tense)
        return inoutres693
    
    @staticmethod
    def calculate_date_range2(dr : 'DateRangeReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.max
        if (dr.date_from is None): 
            if (dr.date_to is None): 
                return False
            wrapdt0694 = RefOutArgWrapper(None)
            wrapdt1695 = RefOutArgWrapper(None)
            inoutres696 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt0694, wrapdt1695, tense)
            dt0 = wrapdt0694.value
            dt1 = wrapdt1695.value
            if (not inoutres696): 
                return False
            to.value = dt1
            return True
        elif (dr.date_to is None): 
            wrapdt0697 = RefOutArgWrapper(None)
            wrapdt1698 = RefOutArgWrapper(None)
            inoutres699 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0697, wrapdt1698, tense)
            dt0 = wrapdt0697.value
            dt1 = wrapdt1698.value
            if (not inoutres699): 
                return False
            from0_.value = dt0
            return True
        wrapdt0703 = RefOutArgWrapper(None)
        wrapdt1704 = RefOutArgWrapper(None)
        inoutres705 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0703, wrapdt1704, tense)
        dt0 = wrapdt0703.value
        dt1 = wrapdt1704.value
        if (not inoutres705): 
            return False
        from0_.value = dt0
        wrapdt2700 = RefOutArgWrapper(None)
        wrapdt3701 = RefOutArgWrapper(None)
        inoutres702 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt2700, wrapdt3701, tense)
        dt2 = wrapdt2700.value
        dt3 = wrapdt3701.value
        if (not inoutres702): 
            return False
        to.value = dt3
        return True
    
    @staticmethod
    def append_to_string(dr : 'DateReferent', res : io.StringIO) -> None:
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0706 = RefOutArgWrapper(None)
        wrapdt1707 = RefOutArgWrapper(None)
        inoutres708 = DateRelHelper.calculate_date_range(dr, cur, wrapdt0706, wrapdt1707, 0)
        dt0 = wrapdt0706.value
        dt1 = wrapdt1707.value
        if (not inoutres708): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def append_to_string2(dr : 'DateRangeReferent', res : io.StringIO) -> None:
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0709 = RefOutArgWrapper(None)
        wrapdt1710 = RefOutArgWrapper(None)
        inoutres711 = DateRelHelper.calculate_date_range2(dr, cur, wrapdt0709, wrapdt1710, 0)
        dt0 = wrapdt0709.value
        dt1 = wrapdt1710.value
        if (not inoutres711): 
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