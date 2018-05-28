﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper

from pullenti.morph.LanguageHelper import LanguageHelper

from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.TerminParseAttr import TerminParseAttr


class TerrAttachHelper:
    
    @staticmethod
    def __try_attach_moscowao(li : typing.List['TerrItemToken'], ad : 'AnalyzerData') -> 'ReferentToken':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (li[0].termin_item is None or not li[0].termin_item.is_moscow_region): 
            return None
        if (li[0].is_doubt): 
            ok = False
            if (CityAttachHelper.check_city_after(li[0].end_token.next0)): 
                ok = True
            else: 
                ali = AddressItemToken.try_parse_list(li[0].end_token.next0, None, 2)
                if (ali is not None and len(ali) > 0 and ali[0].typ == AddressItemToken.ItemType.STREET): 
                    ok = True
            if (not ok): 
                return None
        reg = GeoReferent()
        typ = "АДМИНИСТРАТИВНЫЙ ОКРУГ"
        reg._add_typ(typ)
        name = li[0].termin_item.canonic_text
        if (LanguageHelper.ends_with(name, typ)): 
            name = name[0 : (len(name) - len(typ) - 1)].strip()
        reg._add_name(name)
        return ReferentToken(reg, li[0].begin_token, li[0].end_token)
    
    @staticmethod
    def __try_attach_pure_terr(li : typing.List['TerrItemToken'], ad : 'AnalyzerData') -> 'ReferentToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        aid = None
        t = li[0].end_token.next0
        if (t is None): 
            return None
        tt = t
        if (BracketHelper.can_be_start_of_sequence(tt, True, False)): 
            tt = tt.next0
        if (len(li) > 1): 
            tmp = list(li)
            del tmp[0]
            rt0 = TerrAttachHelper.try_attach_territory(tmp, ad, False, None, None)
            if (rt0 is None and len(tmp) == 2): 
                if (((tmp[0].termin_item is None and tmp[1].termin_item is not None)) or ((tmp[0].termin_item is not None and tmp[1].termin_item is None))): 
                    if (aid is None): 
                        rt0 = TerrAttachHelper.try_attach_territory(tmp, ad, True, None, None)
            if (rt0 is not None): 
                if ((rt0.referent if isinstance(rt0.referent, GeoReferent) else None).is_state): 
                    return None
                rt0.begin_token = li[0].begin_token
                return rt0
        if (aid is None): 
            aid = AddressItemToken.try_attach_org(tt)
        if (aid is not None): 
            rt = aid.create_geo_org_terr()
            if (rt is None): 
                return None
            rt.begin_token = li[0].begin_token
            t1 = rt.end_token
            if (tt != t and BracketHelper.can_be_end_of_sequence(t1.next0, False, None, False)): 
                t1 = t1.next0
                rt.end_token = t1
            return rt
        return None
    
    @staticmethod
    def try_attach_territory(li : typing.List['TerrItemToken'], ad : 'AnalyzerData', attach_always : bool=False, cits : typing.List['CityItemToken']=None, exists : typing.List['GeoReferent']=None) -> 'ReferentToken':
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.ProperNameHelper import ProperNameHelper
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.ner.TextToken import TextToken
        if (li is None or len(li) == 0): 
            return None
        ex_obj = None
        new_name = None
        adj_list = list()
        noun = None
        add_noun = None
        rt = TerrAttachHelper.__try_attach_moscowao(li, ad)
        if (rt is not None): 
            return rt
        if (li[0].termin_item is not None and li[0].termin_item.canonic_text == "ТЕРРИТОРИЯ"): 
            res2 = TerrAttachHelper.__try_attach_pure_terr(li, ad)
            return res2
        if (len(li) == 2): 
            if (li[0].rzd is not None and li[1].rzd_dir is not None): 
                rzd = GeoReferent()
                rzd._add_name(li[1].rzd_dir)
                rzd._add_typ_ter(li[0].kit.base_language)
                rzd.add_slot(GeoReferent.ATTR_REF, li[0].rzd.referent, False, 0)
                rzd.add_ext_referent(li[0].rzd)
                return ReferentToken(rzd, li[0].begin_token, li[1].end_token)
            if (li[1].rzd is not None and li[0].rzd_dir is not None): 
                rzd = GeoReferent()
                rzd._add_name(li[0].rzd_dir)
                rzd._add_typ_ter(li[0].kit.base_language)
                rzd.add_slot(GeoReferent.ATTR_REF, li[1].rzd.referent, False, 0)
                rzd.add_ext_referent(li[1].rzd)
                return ReferentToken(rzd, li[0].begin_token, li[1].end_token)
        can_be_city_before = False
        adj_terr_before = False
        if (cits is not None): 
            if (cits[0].typ == CityItemToken.ItemType.CITY): 
                can_be_city_before = True
            elif (cits[0].typ == CityItemToken.ItemType.NOUN and len(cits) > 1): 
                can_be_city_before = True
        for k in range(len(li)):
            if (li[k].onto_item is not None): 
                if (ex_obj is not None or new_name is not None): 
                    break
                if (noun is not None): 
                    if (k == 1): 
                        if (noun.termin_item.canonic_text == "РАЙОН" or noun.termin_item.canonic_text == "ОБЛАСТЬ" or noun.termin_item.canonic_text == "СОЮЗ"): 
                            if (isinstance(li[k].onto_item.referent, GeoReferent)): 
                                if ((li[k].onto_item.referent if isinstance(li[k].onto_item.referent, GeoReferent) else None).is_state): 
                                    break
                            ok = False
                            tt = li[k].end_token.next0
                            if (tt is None): 
                                ok = True
                            elif (tt.is_char_of(",.")): 
                                ok = True
                            if (not ok): 
                                ok = MiscLocationHelper.check_geo_object_before(li[0].begin_token)
                            if (not ok): 
                                adr = AddressItemToken.try_parse(tt, None, False, False, None)
                                if (adr is not None): 
                                    if (adr.typ == AddressItemToken.ItemType.STREET): 
                                        ok = True
                            if (not ok): 
                                break
                        if (li[k].onto_item is not None): 
                            if (noun.begin_token.is_value("МО", None) or noun.begin_token.is_value("ЛО", None)): 
                                return None
                ex_obj = li[k]
            elif (li[k].termin_item is not None): 
                if (noun is not None): 
                    break
                if (li[k].termin_item.is_always_prefix and k > 0): 
                    break
                if (k > 0 and li[k].is_doubt): 
                    if (li[k].begin_token == li[k].end_token and li[k].begin_token.is_value("ЗАО", None)): 
                        break
                if (li[k].termin_item.is_adjective or li[k].is_geo_in_dictionary): 
                    adj_list.append(li[k])
                else: 
                    if (ex_obj is not None): 
                        geo_ = (ex_obj.onto_item.referent if isinstance(ex_obj.onto_item.referent, GeoReferent) else None)
                        if (geo_ is None): 
                            break
                        if (ex_obj.is_adjective and ((li[k].termin_item.canonic_text == "СОЮЗ" or li[k].termin_item.canonic_text == "ФЕДЕРАЦИЯ"))): 
                            str0 = str(ex_obj.onto_item)
                            if (not li[k].termin_item.canonic_text in str0): 
                                return None
                        if (li[k].termin_item.canonic_text == "РАЙОН" or li[k].termin_item.canonic_text == "ОКРУГ" or li[k].termin_item.canonic_text == "КРАЙ"): 
                            tmp = Utils.newStringIO(None)
                            for s in geo_.slots: 
                                if (s.type_name == GeoReferent.ATTR_TYPE): 
                                    print("{0};".format(s.value), end="", file=tmp, flush=True)
                            if (not li[k].termin_item.canonic_text in Utils.toStringStringIO(tmp).upper()): 
                                if (k != 1 or new_name is not None): 
                                    break
                                new_name = li[0]
                                new_name.is_adjective = True
                                new_name.onto_item = None
                                ex_obj = None
                    noun = li[k]
                    if (k == 0): 
                        tt = TerrItemToken.try_parse(li[k].begin_token.previous, None, True, False)
                        if (tt is not None and tt.morph.class0.is_adjective): 
                            adj_terr_before = True
            else: 
                if (ex_obj is not None): 
                    break
                if (new_name is not None): 
                    break
                new_name = li[k]
        else: k = len(li)
        name = None
        alt_name = None
        full_name = None
        morph_ = None
        if (ex_obj is not None): 
            if (ex_obj.is_adjective and not ex_obj.morph.language.is_en and noun is None): 
                if (attach_always and ex_obj.end_token.next0 is not None): 
                    npt = NounPhraseHelper.try_parse(ex_obj.begin_token, NounPhraseParseAttr.NO, 0)
                    if (ex_obj.end_token.next0.is_comma_and): 
                        pass
                    elif (npt is None): 
                        pass
                    else: 
                        str0 = StreetItemToken.try_parse(ex_obj.end_token.next0, None, False, None, False)
                        if (str0 is not None): 
                            if (str0.typ == StreetItemType.NOUN and str0.end_token == npt.end_token): 
                                return None
                else: 
                    cit = CityItemToken.try_parse(ex_obj.end_token.next0, None, False, None)
                    if (cit is not None and ((cit.typ == CityItemToken.ItemType.NOUN or cit.typ == CityItemToken.ItemType.CITY))): 
                        npt = NounPhraseHelper.try_parse(ex_obj.begin_token, NounPhraseParseAttr.NO, 0)
                        if (npt is not None and npt.end_token == cit.end_token): 
                            pass
                        else: 
                            return None
                    elif (ex_obj.begin_token.is_value("ПОДНЕБЕСНЫЙ", None)): 
                        pass
                    else: 
                        return None
            if (noun is None and ex_obj.can_be_city): 
                cit0 = CityItemToken.try_parse_back(ex_obj.begin_token.previous)
                if (cit0 is not None and cit0.typ != CityItemToken.ItemType.PROPERNAME): 
                    return None
            if (ex_obj.is_doubt and noun is None): 
                ok2 = False
                if (TerrAttachHelper.__can_be_geo_after(ex_obj.end_token.next0)): 
                    ok2 = True
                elif (not ex_obj.can_be_surname and not ex_obj.can_be_city): 
                    if ((ex_obj.end_token.next0 is not None and ex_obj.end_token.next0.is_char(')') and ex_obj.begin_token.previous is not None) and ex_obj.begin_token.previous.is_char('(')): 
                        ok2 = True
                    elif (ex_obj.chars.is_latin_letter and ex_obj.begin_token.previous is not None): 
                        if (ex_obj.begin_token.previous.is_value("IN", None)): 
                            ok2 = True
                        elif (ex_obj.begin_token.previous.is_value("THE", None) and ex_obj.begin_token.previous.previous is not None and ex_obj.begin_token.previous.previous.is_value("IN", None)): 
                            ok2 = True
                if (not ok2): 
                    cit0 = CityItemToken.try_parse_back(ex_obj.begin_token.previous)
                    if (cit0 is not None and cit0.typ != CityItemToken.ItemType.PROPERNAME): 
                        pass
                    elif (MiscLocationHelper.check_geo_object_before(ex_obj.begin_token.previous)): 
                        pass
                    else: 
                        return None
            name = ex_obj.onto_item.canonic_text
            morph_ = ex_obj.morph
        elif (new_name is not None): 
            if (noun is None): 
                return None
            j = 1
            while j < k: 
                if (li[j].is_newline_before): 
                    return None
                j += 1
            morph_ = noun.morph
            if (new_name.is_adjective): 
                if (noun.termin_item.acronym == "АО"): 
                    if (noun.begin_token != noun.end_token): 
                        return None
                    if (new_name.morph.gender != MorphGender.FEMINIE): 
                        return None
                geo_before = None
                tt0 = li[0].begin_token.previous
                if (tt0 is not None and tt0.is_comma_and): 
                    tt0 = tt0.previous
                if (not li[0].is_newline_before and tt0 is not None): 
                    geo_before = (tt0.get_referent() if isinstance(tt0.get_referent(), GeoReferent) else None)
                if (Utils.indexOfList(li, noun, 0) < Utils.indexOfList(li, new_name, 0)): 
                    if (noun.termin_item.is_state): 
                        return None
                    if (new_name.can_be_surname and geo_before is None): 
                        if ((noun.morph.case & new_name.morph.case).is_undefined): 
                            return None
                    if (MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE | MorphClass.PRONOUN | MorphClass.VERB)): 
                        if (noun.begin_token != new_name.begin_token): 
                            if (geo_before is None): 
                                if (len(li) == 2 and TerrAttachHelper.__can_be_geo_after(li[1].end_token.next0)): 
                                    pass
                                elif (new_name.is_geo_in_dictionary): 
                                    pass
                                elif (new_name.end_token.is_newline_after): 
                                    pass
                                else: 
                                    return None
                    npt = NounPhraseHelper.try_parse(new_name.end_token, NounPhraseParseAttr.PARSEPRONOUNS, 0)
                    if (npt is not None and npt.end_token != new_name.end_token): 
                        return None
                    rtp = new_name.kit.process_referent("PERSON", new_name.begin_token)
                    if (rtp is not None): 
                        return None
                    name = ProperNameHelper.get_name(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                else: 
                    ok = False
                    if (((k + 1) < len(li)) and li[k].termin_item is None and li[k + 1].termin_item is not None): 
                        ok = True
                    elif ((k < len(li)) and li[k].onto_item is not None): 
                        ok = True
                    elif (k == len(li) and not new_name.is_adj_in_dictionary): 
                        ok = True
                    elif (MiscLocationHelper.check_geo_object_before(li[0].begin_token) or can_be_city_before): 
                        ok = True
                    elif (MiscLocationHelper.check_geo_object_after(li[k - 1].end_token)): 
                        ok = True
                    elif (len(li) == 3 and k == 2): 
                        cit = CityItemToken.try_parse(li[2].begin_token, None, False, None)
                        if (cit is not None): 
                            if (cit.typ == CityItemToken.ItemType.CITY or cit.typ == CityItemToken.ItemType.NOUN): 
                                ok = True
                    elif (len(li) == 2): 
                        ok = TerrAttachHelper.__can_be_geo_after(li[len(li) - 1].end_token.next0)
                    if (not ok and not li[0].is_newline_before and not li[0].chars.is_all_lower): 
                        rt00 = li[0].kit.process_referent("PERSONPROPERTY", li[0].begin_token.previous)
                        if (rt00 is not None): 
                            ok = True
                    if (noun.termin_item is not None and noun.termin_item.is_strong and new_name.is_adjective): 
                        ok = True
                    if (noun.is_doubt and len(adj_list) == 0 and geo_before is None): 
                        return None
                    name = ProperNameHelper.get_name(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    if (not ok and not attach_always): 
                        if (MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE | MorphClass.PRONOUN | MorphClass.VERB)): 
                            if (exists is not None): 
                                for e0 in exists: 
                                    if (e0.find_slot(GeoReferent.ATTR_NAME, name, True) is not None): 
                                        ok = True
                                        break
                            if (not ok): 
                                return None
                    full_name = "{0} {1}".format(ProperNameHelper.get_name(li[0].begin_token, noun.begin_token.previous, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False), noun.termin_item.canonic_text)
            else: 
                if (not attach_always or ((noun.termin_item is not None and noun.termin_item.canonic_text == "ФЕДЕРАЦИЯ"))): 
                    is_latin = noun.chars.is_latin_letter and new_name.chars.is_latin_letter
                    if (Utils.indexOfList(li, noun, 0) > Utils.indexOfList(li, new_name, 0)): 
                        if (not is_latin): 
                            return None
                    if (not new_name.is_district_name): 
                        if (len(adj_list) == 0 and MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, MorphClass.NOUN | MorphClass.PRONOUN)): 
                            if (len(li) == 2 and noun.is_city_region and (noun.whitespaces_after_count < 2)): 
                                pass
                            else: 
                                return None
                        if (not is_latin): 
                            if ((noun.termin_item.is_region and not attach_always and ((not adj_terr_before or new_name.is_doubt))) and not noun.is_city_region and not noun.termin_item.is_specific_prefix): 
                                if (not MiscLocationHelper.check_geo_object_before(noun.begin_token)): 
                                    if (not noun.is_doubt and noun.begin_token != noun.end_token): 
                                        pass
                                    else: 
                                        return None
                            if (noun.is_doubt and len(adj_list) == 0): 
                                if (((noun.termin_item.acronym == "МО" or noun.termin_item.acronym == "ЛО")) and k == (len(li) - 1) and li[k].termin_item is not None): 
                                    add_noun = li[k]
                                    k += 1
                                else: 
                                    return None
                            pers = new_name.kit.process_referent("PERSON", new_name.begin_token)
                            if (pers is not None): 
                                return None
                name = ProperNameHelper.get_name(new_name.begin_token, new_name.end_token, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, False, False)
                if (len(adj_list) > 0): 
                    npt = NounPhraseHelper.try_parse(adj_list[0].begin_token, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and npt.end_token == noun.end_token): 
                        alt_name = "{0} {1}".format(npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), name)
        else: 
            if ((len(li) == 1 and noun is not None and noun.end_token.next0 is not None) and isinstance(noun.end_token.next0.get_referent(), GeoReferent)): 
                g = (noun.end_token.next0.get_referent() if isinstance(noun.end_token.next0.get_referent(), GeoReferent) else None)
                if (noun.termin_item is not None): 
                    if (g.find_slot(GeoReferent.ATTR_TYPE, noun.termin_item.canonic_text.lower(), True) is not None): 
                        return ReferentToken._new695(g, noun.begin_token, noun.end_token.next0, noun.begin_token.morph)
            if ((len(li) == 1 and noun == li[0] and li[0].termin_item is not None) and TerrItemToken.try_parse(li[0].end_token.next0, None, True, False) is None and TerrItemToken.try_parse(li[0].begin_token.previous, None, True, False) is None): 
                if (li[0].morph.number == MorphNumber.PLURAL): 
                    return None
                cou = 0
                str0 = li[0].termin_item.canonic_text.lower()
                tt = li[0].begin_token.previous
                first_pass2689 = True
                while True:
                    if first_pass2689: first_pass2689 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_newline_after): 
                        cou += 10
                    else: 
                        cou += 1
                    if (cou > 500): 
                        break
                    g = (tt.get_referent() if isinstance(tt.get_referent(), GeoReferent) else None)
                    if (g is None): 
                        continue
                    ok = True
                    cou = 0
                    tt = li[0].end_token.next0
                    first_pass2690 = True
                    while True:
                        if first_pass2690: first_pass2690 = False
                        else: tt = tt.next0
                        if (not (tt is not None)): break
                        if (tt.is_newline_before): 
                            cou += 10
                        else: 
                            cou += 1
                        if (cou > 500): 
                            break
                        tee = TerrItemToken.try_parse(tt, None, True, False)
                        if (tee is None): 
                            continue
                        ok = False
                        break
                    if (ok): 
                        ii = 0
                        while g is not None and (ii < 3): 
                            if (g.find_slot(GeoReferent.ATTR_TYPE, str0, True) is not None): 
                                return ReferentToken._new695(g, li[0].begin_token, li[0].end_token, noun.begin_token.morph)
                            g = g.higher; ii += 1
                    break
            return None
        ter = None
        if (ex_obj is not None and isinstance(ex_obj.tag, GeoReferent)): 
            ter = (ex_obj.tag if isinstance(ex_obj.tag, GeoReferent) else None)
        else: 
            ter = GeoReferent()
            if (ex_obj is not None): 
                geo_ = (ex_obj.onto_item.referent if isinstance(ex_obj.onto_item.referent, GeoReferent) else None)
                if (geo_ is not None and not geo_.is_city): 
                    ter._merge_slots2(geo_, li[0].kit.base_language)
                else: 
                    ter._add_name(name)
                if (noun is None and ex_obj.can_be_city): 
                    ter._add_typ_city(li[0].kit.base_language)
                else: 
                    pass
            elif (new_name is not None): 
                ter._add_name(name)
                if (alt_name is not None): 
                    ter._add_name(alt_name)
            if (noun is not None): 
                if (noun.termin_item.canonic_text == "АО"): 
                    ter._add_typ(("АВТОНОМНИЙ ОКРУГ" if li[0].kit.base_language.is_ua else "АВТОНОМНЫЙ ОКРУГ"))
                elif (noun.termin_item.canonic_text == "МУНИЦИПАЛЬНОЕ СОБРАНИЕ" or noun.termin_item.canonic_text == "МУНІЦИПАЛЬНЕ ЗБОРИ"): 
                    ter._add_typ(("МУНІЦИПАЛЬНЕ УТВОРЕННЯ" if li[0].kit.base_language.is_ua else "МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ"))
                elif (noun.termin_item.acronym == "МО" and add_noun is not None): 
                    ter._add_typ(add_noun.termin_item.canonic_text)
                else: 
                    ter._add_typ(noun.termin_item.canonic_text)
                    if (noun.termin_item.is_region and ter.is_state): 
                        ter._add_typ_reg(li[0].kit.base_language)
            if (ter.is_state and ter.is_region): 
                for a in adj_list: 
                    if (a.termin_item.is_region): 
                        ter._add_typ_reg(li[0].kit.base_language)
                        break
            if (ter.is_state): 
                if (full_name is not None): 
                    ter._add_name(full_name)
        res = ReferentToken(ter, li[0].begin_token, li[k - 1].end_token)
        if (noun is not None and noun.morph.class0.is_noun): 
            res.morph = noun.morph
        else: 
            res.morph = MorphCollection()
            ii = 0
            while ii < k: 
                for v in li[ii].morph.items: 
                    bi = MorphBaseInfo(v)
                    if (noun is not None): 
                        if (bi.class0.is_adjective): 
                            bi.class0 = MorphClass.NOUN
                    res.morph.add_item(bi)
                ii += 1
        if (li[0].termin_item is not None and li[0].termin_item.is_specific_prefix): 
            res.begin_token = li[0].end_token.next0
        if (isinstance(res.begin_token.previous, TextToken) and (res.whitespaces_before_count < 2)): 
            tt = (res.begin_token.previous if isinstance(res.begin_token.previous, TextToken) else None)
            if (tt.term == "АР"): 
                for ty in ter.typs: 
                    if ("республика" in ty or "республіка" in ty): 
                        res.begin_token = tt
                        break
        return res
    
    @staticmethod
    def __can_be_geo_after(tt : 'Token') -> bool:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (tt is not None and tt.is_comma): 
            tt = tt.next0
        if (tt is None): 
            return False
        if (isinstance(tt.get_referent(), GeoReferent)): 
            return True
        tli = TerrItemToken.try_parse_list(tt, None, 2)
        if (tli is not None and len(tli) > 1): 
            if (tli[0].termin_item is None and tli[1].termin_item is not None): 
                return True
            elif (tli[0].termin_item is not None and tli[1].termin_item is None): 
                return True
        if (CityAttachHelper.check_city_after(tt)): 
            return True
        if (TerrAttachHelper.try_attach_stateusaterritory(tt) is not None): 
            return True
        return False
    
    @staticmethod
    def try_attach_stateusaterritory(t : 'Token') -> 'ReferentToken':
        """ Это привязка сокращений штатов
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None or not t.chars.is_latin_letter): 
            return None
        tok = TerrItemToken._m_geo_abbrs.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        g = (tok.termin.tag if isinstance(tok.termin.tag, GeoReferent) else None)
        if (g is None): 
            return None
        if (tok.end_token.next0 is not None and tok.end_token.next0.is_char('.')): 
            tok.end_token = tok.end_token.next0
        gg = g.clone()
        gg.occurrence.clear()
        return ReferentToken(gg, tok.begin_token, tok.end_token)