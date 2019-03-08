# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.geo.GeoReferent import GeoReferent

class GeoOwnerHelper:
    
    @staticmethod
    def __get_types_string(g : 'GeoReferent') -> str:
        tmp = io.StringIO()
        for s in g.slots: 
            if (s.type_name == GeoReferent.ATTR_TYPE): 
                print("{0};".format(s.value), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def _can_be_higher_token(rhi : 'Token', rlo : 'Token') -> bool:
        if (rhi is None or rlo is None): 
            return False
        if (rhi.morph.case_.is_instrumental0 and not rhi.morph.case_.is_genitive0): 
            return False
        hi = Utils.asObjectOrNull(rhi.get_referent(), GeoReferent)
        lo = Utils.asObjectOrNull(rlo.get_referent(), GeoReferent)
        if (hi is None or lo is None): 
            return False
        citi_in_reg = False
        if (hi.is_city0 and lo.is_region0): 
            if (hi.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None or hi.find_slot(GeoReferent.ATTR_TYPE, "місто", True) is not None or hi.find_slot(GeoReferent.ATTR_TYPE, "city", True) is not None): 
                s = GeoOwnerHelper.__get_types_string(lo)
                if ((("район" in s or "административный округ" in s or "муниципальный округ" in s) or "адміністративний округ" in s or "муніципальний округ" in s) or lo.find_slot(GeoReferent.ATTR_TYPE, "округ", True) is not None): 
                    if (rhi.next0_ == rlo and rlo.morph.case_.is_genitive0): 
                        citi_in_reg = True
        if (hi.is_region0 and lo.is_city0): 
            if (lo.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None or lo.find_slot(GeoReferent.ATTR_TYPE, "місто", True) is not None or lo.find_slot(GeoReferent.ATTR_TYPE, "city", True) is not None): 
                s = GeoOwnerHelper.__get_types_string(hi)
                if (s == "район;"): 
                    if (hi.higher is not None and hi.higher.is_region0): 
                        citi_in_reg = True
                    elif (rhi.end_char <= rlo.begin_char and rhi.next0_.is_comma0 and not rlo.morph.case_.is_genitive0): 
                        citi_in_reg = True
                    elif (rhi.end_char <= rlo.begin_char and rhi.next0_.is_comma0): 
                        citi_in_reg = True
            else: 
                citi_in_reg = True
        if (rhi.end_char <= rlo.begin_char): 
            if (not rhi.morph.class0_.is_adjective0): 
                if (hi.is_state0 and not rhi.chars.is_latin_letter0): 
                    return False
            if (rhi.is_newline_after0 or rlo.is_newline_before0): 
                if (not citi_in_reg): 
                    return False
        else: 
            pass
        if (rlo.previous is not None and rlo.previous.morph.class0_.is_preposition0): 
            if (rlo.previous.morph.language.is_ua0): 
                if ((rlo.previous.is_value("У", None) and not rlo.morph.case_.is_dative0 and not rlo.morph.case_.is_prepositional0) and not rlo.morph.case_.is_undefined0): 
                    return False
                if (rlo.previous.is_value("З", None) and not rlo.morph.case_.is_genitive0 and not rlo.morph.case_.is_undefined0): 
                    return False
            else: 
                if ((rlo.previous.is_value("В", None) and not rlo.morph.case_.is_dative0 and not rlo.morph.case_.is_prepositional0) and not rlo.morph.case_.is_undefined0): 
                    return False
                if (rlo.previous.is_value("ИЗ", None) and not rlo.morph.case_.is_genitive0 and not rlo.morph.case_.is_undefined0): 
                    return False
        if (not GeoOwnerHelper.can_be_higher(hi, lo)): 
            return citi_in_reg
        return True
    
    @staticmethod
    def can_be_higher(hi : 'GeoReferent', lo : 'GeoReferent') -> bool:
        if (hi is None or lo is None or hi == lo): 
            return False
        if (lo.higher is not None): 
            return lo.higher == hi
        if (lo.is_state0): 
            if (lo.is_region0 and hi.is_state0 and not hi.is_region0): 
                return True
            return False
        if (hi.is_territory0): 
            return False
        if (lo.is_territory0): 
            return True
        hit = GeoOwnerHelper.__get_types_string(hi)
        lot = GeoOwnerHelper.__get_types_string(lo)
        if (hi.is_city0): 
            if (lo.is_region0): 
                if ("город;" in hit or "місто" in hit or "city" in hit): 
                    if (("район" in lot or "административный округ" in lot or "адміністративний округ" in lot) or "муниципальн" in lot or "муніципаль" in lot): 
                        return True
                    if (lo.find_slot(GeoReferent.ATTR_TYPE, "округ", True) is not None and not "автономн" in lot): 
                        return True
            if (lo.is_city0): 
                if (not "станция" in hit and "станция" in lot): 
                    return True
                if (not "станція" in hit and "станція" in lot): 
                    return True
                if ("город;" in hit or "місто" in hit or "city" in hit): 
                    if (("поселок" in lot or "селище" in lot or "село" in lot) or "деревня" in lot or "городок" in lot): 
                        return True
                if ("поселение" in hit or "поселок" in hit): 
                    if ("село;" in lot or "деревня" in lot or "хутор" in lot): 
                        return True
                if ("поселение" in hit and "поселок" in lot): 
                    return True
                if ("село;" in hit): 
                    if ("поселение" in lot or "поселок" in lot): 
                        return True
                if (hi.find_slot(GeoReferent.ATTR_NAME, "МОСКВА", True) is not None): 
                    if ("город;" in lot or "місто" in lot or "city" in lot): 
                        if (lo.find_slot(GeoReferent.ATTR_NAME, "ЗЕЛЕНОГРАД", True) is not None or lo.find_slot(GeoReferent.ATTR_NAME, "ТРОИЦК", True) is not None): 
                            return True
        elif (lo.is_city0): 
            if (not "город" in lot and not "місто" in lot and not "city" in lot): 
                if (hi.is_region0): 
                    return True
            else: 
                if (hi.is_state0): 
                    return True
                if (("административный округ" in hit or "адміністративний округ" in hit or "муниципальн" in hit) or "муніципаль" in hit): 
                    return False
                if (not "район" in hit): 
                    return True
                if (hi.higher is not None and hi.higher.is_region0): 
                    return True
        elif (lo.is_region0): 
            for s in hi.slots: 
                if (s.type_name == GeoReferent.ATTR_TYPE): 
                    if ((s.value) != "регион" and (s.value) != "регіон"): 
                        if (lo.find_slot(s.type_name, s.value, True) is not None): 
                            return False
            if (hi.is_state0): 
                return True
            if ("волость" in lot): 
                return True
            if ("county" in lot or "borough" in lot or "parish" in lot): 
                if ("state" in hit): 
                    return True
            if ("район" in lot): 
                if (("область" in hit or "регион" in hit or "край" in hit) or "регіон" in hit): 
                    return True
                if ("округ" in hit and not "сельский" in hit and not "поселковый" in hit): 
                    return True
            if ("область" in lot): 
                if ("край" in hit): 
                    return True
                if ("округ" in hit and not "сельский" in hit and not "поселковый" in hit): 
                    return True
            if ("округ" in lot): 
                if ("сельский" in lot or "поселковый" in lot): 
                    return True
                if ("край" in hit): 
                    return True
                if ("округ" in lot): 
                    if ("область" in hit or "республика" in hit): 
                        return True
            if ("муницип" in lot): 
                if ("область" in hit or "район" in hit or "округ" in hit): 
                    return True
        return False