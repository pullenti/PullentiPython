# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

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
        if (rhi.morph.case_.is_instrumental and not rhi.morph.case_.is_genitive): 
            return False
        hi = Utils.asObjectOrNull(rhi.get_referent(), GeoReferent)
        lo = Utils.asObjectOrNull(rlo.get_referent(), GeoReferent)
        if (hi is None or lo is None): 
            return False
        citi_in_reg = False
        if (hi.is_city and lo.is_region): 
            if (hi.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None or hi.find_slot(GeoReferent.ATTR_TYPE, "місто", True) is not None or hi.find_slot(GeoReferent.ATTR_TYPE, "city", True) is not None): 
                s = GeoOwnerHelper.__get_types_string(lo)
                if ((("район" in s or "административный округ" in s or "муниципальный округ" in s) or "адміністративний округ" in s or "муніципальний округ" in s) or lo.find_slot(GeoReferent.ATTR_TYPE, "округ", True) is not None): 
                    if (rhi.next0_ == rlo and rlo.morph.case_.is_genitive): 
                        citi_in_reg = True
        if (hi.is_region and lo.is_city): 
            if (lo.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None or lo.find_slot(GeoReferent.ATTR_TYPE, "місто", True) is not None or lo.find_slot(GeoReferent.ATTR_TYPE, "city", True) is not None): 
                s = GeoOwnerHelper.__get_types_string(hi)
                if (s == "район;"): 
                    if (hi.higher is not None and hi.higher.is_region): 
                        citi_in_reg = True
                    elif (rhi.end_char <= rlo.begin_char and rhi.next0_.is_comma and not rlo.morph.case_.is_genitive): 
                        citi_in_reg = True
                    elif (rhi.end_char <= rlo.begin_char and rhi.next0_.is_comma): 
                        citi_in_reg = True
            else: 
                citi_in_reg = True
        if (rhi.end_char <= rlo.begin_char): 
            if (not rhi.morph.class0_.is_adjective): 
                if (hi.is_state and not rhi.chars.is_latin_letter): 
                    return False
            if (rhi.is_newline_after or rlo.is_newline_before): 
                if (not citi_in_reg): 
                    return False
        else: 
            pass
        if (rlo.previous is not None and rlo.previous.morph.class0_.is_preposition): 
            if (rlo.previous.morph.language.is_ua): 
                if ((rlo.previous.is_value("У", None) and not rlo.morph.case_.is_dative and not rlo.morph.case_.is_prepositional) and not rlo.morph.case_.is_undefined): 
                    return False
                if (rlo.previous.is_value("З", None) and not rlo.morph.case_.is_genitive and not rlo.morph.case_.is_undefined): 
                    return False
            else: 
                if ((rlo.previous.is_value("В", None) and not rlo.morph.case_.is_dative and not rlo.morph.case_.is_prepositional) and not rlo.morph.case_.is_undefined): 
                    return False
                if (rlo.previous.is_value("ИЗ", None) and not rlo.morph.case_.is_genitive and not rlo.morph.case_.is_undefined): 
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
        if (lo.is_state): 
            if (lo.is_region and hi.is_state and not hi.is_region): 
                return True
            return False
        if (hi.is_territory): 
            return False
        if (lo.is_territory): 
            return True
        hit = GeoOwnerHelper.__get_types_string(hi)
        lot = GeoOwnerHelper.__get_types_string(lo)
        if (hi.is_city): 
            if (lo.is_region): 
                if ("город;" in hit or "місто" in hit or "city" in hit): 
                    if (("район" in lot or "административный округ" in lot or "адміністративний округ" in lot) or "муниципальн" in lot or "муніципаль" in lot): 
                        return True
                    if (lo.find_slot(GeoReferent.ATTR_TYPE, "округ", True) is not None and not "автономн" in lot): 
                        return True
            if (lo.is_city): 
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
        elif (lo.is_city): 
            if (not "город" in lot and not "місто" in lot and not "city" in lot): 
                if (hi.is_region): 
                    return True
            else: 
                if (hi.is_state): 
                    return True
                if (("административный округ" in hit or "адміністративний округ" in hit or "муниципальн" in hit) or "муніципаль" in hit): 
                    return False
                if (not "район" in hit): 
                    return True
                if (hi.higher is not None and hi.higher.is_region): 
                    return True
        elif (lo.is_region): 
            for s in hi.slots: 
                if (s.type_name == GeoReferent.ATTR_TYPE): 
                    if ((s.value) != "регион" and (s.value) != "регіон"): 
                        if (lo.find_slot(s.type_name, s.value, True) is not None): 
                            return False
            if ("почтовое отделение" in hit): 
                return False
            if ("почтовое отделение" in lot): 
                return True
            if (hi.is_state): 
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