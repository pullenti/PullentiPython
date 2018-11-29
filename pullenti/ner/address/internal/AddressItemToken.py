# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.GetTextAttr import GetTextAttr


class AddressItemToken(MetaToken):
    
    class ItemType(IntEnum):
        PREFIX = 0
        STREET = 0 + 1
        HOUSE = (0 + 1) + 1
        BUILDING = ((0 + 1) + 1) + 1
        CORPUS = (((0 + 1) + 1) + 1) + 1
        POTCH = ((((0 + 1) + 1) + 1) + 1) + 1
        FLOOR = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        FLAT = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
        CORPUSORFLAT = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        OFFICE = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        PLOT = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        BLOCK = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        BOX = (((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        CITY = ((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        REGION = (((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        COUNTRY = ((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        NUMBER = (((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        NONUMBER = ((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        KILOMETER = (((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        ZIP = ((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        POSTOFFICEBOX = (((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        CSP = ((((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        DETAIL = (((((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        BUSINESSCENTER = ((((((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, typ_ : 'ItemType', begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = AddressItemToken.ItemType.PREFIX
        self.value = None;
        self.referent = None;
        self.ref_token = None;
        self.ref_token_is_gsk = False
        self.is_doubt = False
        self.detail_type = AddressDetailType.UNDEFINED
        self.building_type = AddressBuildingType.UNDEFINED
        self.house_type = AddressHouseType.UNDEFINED
        self.detail_meters = 0
        self.typ = typ_
    
    @property
    def is_street_road(self) -> bool:
        from pullenti.ner.address.StreetReferent import StreetReferent
        if (self.typ != AddressItemToken.ItemType.STREET): 
            return False
        if (not ((isinstance(self.referent, StreetReferent)))): 
            return False
        return (Utils.asObjectOrNull(self.referent, StreetReferent)).kind == StreetKind.ROAD
    
    @property
    def is_terr_or_rzd(self) -> bool:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (self.typ == AddressItemToken.ItemType.CITY and (isinstance(self.referent, GeoReferent))): 
            if ((Utils.asObjectOrNull(self.referent, GeoReferent)).is_territory): 
                return True
        return False
    
    @property
    def is_digit(self) -> bool:
        if (self.value == "Б/Н"): 
            return True
        if (Utils.isNullOrEmpty(self.value)): 
            return False
        if (str.isdigit(self.value[0])): 
            return True
        if (len(self.value) > 1): 
            if (str.isalpha(self.value[0]) and str.isdigit(self.value[1])): 
                return True
        if (len(self.value) != 1 or not str.isalpha(self.value[0])): 
            return False
        if (not self.begin_token.chars.is_all_lower): 
            return False
        return True
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, "")), end="", file=res, flush=True)
        if (self.referent is not None): 
            print(" <{0}>".format(str(self.referent)), end="", file=res, flush=True)
        if (self.detail_type != AddressDetailType.UNDEFINED): 
            print(" [{0}, {1}]".format(Utils.enumToString(self.detail_type), self.detail_meters), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def tryParseList(t : 'Token', loc_streets : 'IntOntologyCollection', max_count : int=20) -> typing.List['AddressItemToken']:
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.address.StreetReferent import StreetReferent
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (isinstance(t, NumberToken)): 
            v = (Utils.asObjectOrNull(t, NumberToken)).value
            if ((v < (100000)) or v >= (10000000)): 
                if ((Utils.asObjectOrNull(t, NumberToken)).typ == NumberSpellingType.DIGIT and not t.morph.class0_.is_adjective): 
                    if (t.next0_ is None or (isinstance(t.next0_, NumberToken))): 
                        if (t.previous is None or not t.previous.morph.class0_.is_preposition): 
                            return None
        it = AddressItemToken.tryParse(t, loc_streets, False, False, None)
        if (it is None): 
            return None
        if (it.typ == AddressItemToken.ItemType.NUMBER): 
            return None
        if (it.typ == AddressItemToken.ItemType.KILOMETER and not it.is_number and (isinstance(it.begin_token.previous, NumberToken))): 
            it.begin_token = it.begin_token.previous
            it.value = str((Utils.asObjectOrNull(it.begin_token, NumberToken)).value)
            if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                it.begin_token = it.begin_token.previous
        res = list()
        res.append(it)
        pref = it.typ == AddressItemToken.ItemType.PREFIX
        t = it.end_token.next0_
        first_pass2733 = True
        while True:
            if first_pass2733: first_pass2733 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            last = res[len(res) - 1]
            if (len(res) > 1): 
                if (last.is_newline_before and res[len(res) - 2].typ != AddressItemToken.ItemType.PREFIX): 
                    i = 0
                    first_pass2734 = True
                    while True:
                        if first_pass2734: first_pass2734 = False
                        else: i += 1
                        if (not (i < (len(res) - 1))): break
                        if (res[i].typ == last.typ): 
                            if (i == (len(res) - 2) and ((last.typ == AddressItemToken.ItemType.CITY or last.typ == AddressItemToken.ItemType.REGION))): 
                                jj = 0
                                while jj < i: 
                                    if ((res[jj].typ != AddressItemToken.ItemType.PREFIX and res[jj].typ != AddressItemToken.ItemType.ZIP and res[jj].typ != AddressItemToken.ItemType.REGION) and res[jj].typ != AddressItemToken.ItemType.COUNTRY): 
                                        break
                                    jj += 1
                                if (jj >= i): 
                                    continue
                            break
                    if ((i < (len(res) - 1)) or last.typ == AddressItemToken.ItemType.ZIP): 
                        res.remove(last)
                        break
            if (t.is_table_control_char): 
                break
            if (t.isChar(',')): 
                continue
            if (BracketHelper.canBeEndOfSequence(t, True, None, False) and last.typ == AddressItemToken.ItemType.STREET): 
                continue
            if (t.isChar('.')): 
                if (t.is_newline_after): 
                    break
                if (t.previous is not None and t.previous.isChar('.')): 
                    break
                continue
            if (t.is_hiphen or t.isChar('_')): 
                if (((it.typ == AddressItemToken.ItemType.NUMBER or it.typ == AddressItemToken.ItemType.STREET)) and (isinstance(t.next0_, NumberToken))): 
                    continue
            if (it.typ == AddressItemToken.ItemType.DETAIL and it.detail_type == AddressDetailType.CROSS): 
                str1 = AddressItemToken.tryParse(t, loc_streets, True, False, None)
                if (str1 is not None and str1.typ == AddressItemToken.ItemType.STREET): 
                    if (str1.end_token.next0_ is not None and ((str1.end_token.next0_.is_and or str1.end_token.next0_.is_hiphen))): 
                        str2 = AddressItemToken.tryParse(str1.end_token.next0_.next0_, loc_streets, True, False, None)
                        if (str2 is None or str2.typ != AddressItemToken.ItemType.STREET): 
                            str2 = StreetDefineHelper._tryParseSecondStreet(str1.begin_token, str1.end_token.next0_.next0_, loc_streets)
                            if (str2 is not None): 
                                str2.is_doubt = False
                        if (str2 is not None and str2.typ == AddressItemToken.ItemType.STREET): 
                            res.append(str1)
                            res.append(str2)
                            t = str2.end_token
                            it = str2
                            continue
            pre = pref
            if (it.typ == AddressItemToken.ItemType.KILOMETER or it.typ == AddressItemToken.ItemType.HOUSE): 
                if (not t.is_newline_before): 
                    pre = True
            it0 = AddressItemToken.tryParse(t, loc_streets, pre, False, it)
            if (it0 is None): 
                ok2 = True
                if (it.typ == AddressItemToken.ItemType.BUILDING and it.begin_token.isValue("СТ", None)): 
                    ok2 = False
                else: 
                    for rr in res: 
                        if (rr.typ == AddressItemToken.ItemType.BUILDING and rr.begin_token.isValue("СТ", None)): 
                            ok2 = False
                if (it.typ == AddressItemToken.ItemType.POSTOFFICEBOX): 
                    break
                if (ok2): 
                    it0 = AddressItemToken.tryAttachOrg(t)
                if (it0 is not None): 
                    res.append(it0)
                    it = it0
                    t = it.end_token
                    tt1 = t.next0_
                    while tt1 is not None: 
                        if (tt1.is_comma): 
                            pass
                        else: 
                            if (tt1.isValue("Л", None) and tt1.next0_ is not None and tt1.next0_.isChar('.')): 
                                ait = AddressItemToken.tryParse(tt1.next0_.next0_, None, False, True, None)
                                if (ait is not None and ait.typ == AddressItemToken.ItemType.NUMBER): 
                                    st2 = StreetReferent()
                                    st2.addSlot(StreetReferent.ATTR_TYP, "линия", False, 0)
                                    st2.number = ait.value
                                    it = AddressItemToken._new83(AddressItemToken.ItemType.STREET, tt1, ait.end_token, st2)
                                    res.append(it)
                                    t = it.end_token
                            break
                        tt1 = tt1.next0_
                    continue
                if (t.morph.class0_.is_preposition): 
                    it0 = AddressItemToken.tryParse(t.next0_, loc_streets, False, False, it)
                    if (it0 is not None and it0.typ == AddressItemToken.ItemType.BUILDING and it0.begin_token.isValue("СТ", None)): 
                        it0 = (None)
                        break
                    if (it0 is not None): 
                        if ((it0.typ == AddressItemToken.ItemType.HOUSE or it0.typ == AddressItemToken.ItemType.BUILDING or it0.typ == AddressItemToken.ItemType.CORPUS) or it0.typ == AddressItemToken.ItemType.STREET): 
                            it = it0
                            res.append(it)
                            t = it.end_token
                            continue
                if (it.typ == AddressItemToken.ItemType.HOUSE or it.typ == AddressItemToken.ItemType.BUILDING or it.typ == AddressItemToken.ItemType.NUMBER): 
                    if ((not t.is_whitespace_before and t.length_char == 1 and t.chars.is_letter) and not t.is_whitespace_after and (isinstance(t.next0_, NumberToken))): 
                        ch = AddressItemToken.__correctCharToken(t)
                        if (ch == "К" or ch == "С"): 
                            it0 = AddressItemToken._new84((AddressItemToken.ItemType.CORPUS if ch == "К" else AddressItemToken.ItemType.BUILDING), t, t.next0_, str((Utils.asObjectOrNull(t.next0_, NumberToken)).value))
                            it = it0
                            res.append(it)
                            t = it.end_token
                            tt = t.next0_
                            if (((tt is not None and not tt.is_whitespace_before and tt.length_char == 1) and tt.chars.is_letter and not tt.is_whitespace_after) and (isinstance(tt.next0_, NumberToken))): 
                                ch = AddressItemToken.__correctCharToken(tt)
                                if (ch == "К" or ch == "С"): 
                                    it = AddressItemToken._new84((AddressItemToken.ItemType.CORPUS if ch == "К" else AddressItemToken.ItemType.BUILDING), tt, tt.next0_, str((Utils.asObjectOrNull(tt.next0_, NumberToken)).value))
                                    res.append(it)
                                    t = it.end_token
                            continue
                if (t.morph.class0_.is_preposition): 
                    if ((((t.isValue("У", None) or t.isValue("ВОЗЛЕ", None) or t.isValue("НАПРОТИВ", None)) or t.isValue("НА", None) or t.isValue("В", None)) or t.isValue("ВО", None) or t.isValue("ПО", None)) or t.isValue("ОКОЛО", None)): 
                        continue
                if (t.morph.class0_.is_noun): 
                    if ((t.isValue("ДВОР", None) or t.isValue("ПОДЪЕЗД", None) or t.isValue("КРЫША", None)) or t.isValue("ПОДВАЛ", None)): 
                        continue
                if (t.isValue("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                    continue
                if (t.isChar('(') and t.next0_ is not None): 
                    it0 = AddressItemToken.tryParse(t.next0_, loc_streets, pre, False, None)
                    if (it0 is not None and it0.end_token.next0_ is not None and it0.end_token.next0_.isChar(')')): 
                        it0.begin_token = t
                        it0.end_token = it0.end_token.next0_
                        it = it0
                        res.append(it)
                        t = it.end_token
                        continue
                    br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 100)): 
                        if (t.next0_.isValue("БЫВШИЙ", None) or t.next0_.isValue("БЫВШ", None)): 
                            it = AddressItemToken(AddressItemToken.ItemType.DETAIL, t, br.end_token)
                            res.append(it)
                        t = br.end_token
                        continue
                check_kv = False
                if (t.isValue("КВ", None) or t.isValue("KB", None)): 
                    if (it.typ == AddressItemToken.ItemType.NUMBER and len(res) > 1 and res[len(res) - 2].typ == AddressItemToken.ItemType.STREET): 
                        check_kv = True
                    elif ((it.typ == AddressItemToken.ItemType.HOUSE or it.typ == AddressItemToken.ItemType.BUILDING or it.typ == AddressItemToken.ItemType.CORPUS) or it.typ == AddressItemToken.ItemType.CORPUSORFLAT): 
                        for jj in range(len(res) - 2, -1, -1):
                            if (res[jj].typ == AddressItemToken.ItemType.STREET or res[jj].typ == AddressItemToken.ItemType.CITY): 
                                check_kv = True
                    if (check_kv): 
                        tt2 = t.next0_
                        if (tt2 is not None and tt2.isChar('.')): 
                            tt2 = tt2.next0_
                        it22 = AddressItemToken.tryParse(tt2, loc_streets, False, True, None)
                        if (it22 is not None and it22.typ == AddressItemToken.ItemType.NUMBER): 
                            it22.begin_token = t
                            it22.typ = AddressItemToken.ItemType.FLAT
                            res.append(it22)
                            t = it22.end_token
                            continue
                if (res[len(res) - 1].typ == AddressItemToken.ItemType.CITY): 
                    if (((t.is_hiphen or t.isChar('_') or t.isValue("НЕТ", None))) and t.next0_ is not None and t.next0_.is_comma): 
                        att = AddressItemToken.__TryParse(t.next0_.next0_, None, False, True, None)
                        if (att is not None): 
                            if (att.typ == AddressItemToken.ItemType.HOUSE or att.typ == AddressItemToken.ItemType.BUILDING or att.typ == AddressItemToken.ItemType.CORPUS): 
                                it = AddressItemToken(AddressItemToken.ItemType.STREET, t, t)
                                res.append(it)
                                continue
                break
            if (t.whitespaces_before_count > 15): 
                if (it0.typ == AddressItemToken.ItemType.STREET and last.typ == AddressItemToken.ItemType.CITY): 
                    pass
                else: 
                    break
            if (it0.typ == AddressItemToken.ItemType.STREET and t.isValue("КВ", None)): 
                if (it is not None): 
                    if (it.typ == AddressItemToken.ItemType.HOUSE or it.typ == AddressItemToken.ItemType.BUILDING or it.typ == AddressItemToken.ItemType.CORPUS): 
                        it2 = AddressItemToken.tryParse(t, loc_streets, False, True, None)
                        if (it2 is not None and it2.typ == AddressItemToken.ItemType.FLAT): 
                            it0 = it2
            if (it0.typ == AddressItemToken.ItemType.PREFIX): 
                break
            if (it0.typ == AddressItemToken.ItemType.NUMBER): 
                if (Utils.isNullOrEmpty(it0.value)): 
                    break
                if (not str.isdigit(it0.value[0])): 
                    break
                cou = 0
                for i in range(len(res) - 1, -1, -1):
                    if (res[i].typ == AddressItemToken.ItemType.NUMBER): 
                        cou += 1
                    else: 
                        break
                if (cou > 5): 
                    break
                if (it.is_doubt and t.is_newline_before): 
                    break
            if (it0.typ == AddressItemToken.ItemType.CORPUSORFLAT and it is not None and it.typ == AddressItemToken.ItemType.FLAT): 
                it0.typ = AddressItemToken.ItemType.OFFICE
            if ((((it0.typ == AddressItemToken.ItemType.FLOOR or it0.typ == AddressItemToken.ItemType.POTCH or it0.typ == AddressItemToken.ItemType.BLOCK) or it0.typ == AddressItemToken.ItemType.KILOMETER)) and Utils.isNullOrEmpty(it0.value) and it.typ == AddressItemToken.ItemType.NUMBER): 
                it.typ = it0.typ
                it.end_token = it0.end_token
            elif (((it.typ == AddressItemToken.ItemType.FLOOR or it.typ == AddressItemToken.ItemType.POTCH)) and Utils.isNullOrEmpty(it.value) and it0.typ == AddressItemToken.ItemType.NUMBER): 
                it.value = it0.value
                it.end_token = it0.end_token
            else: 
                it = it0
                res.append(it)
            t = it.end_token
        if (len(res) > 0): 
            it = res[len(res) - 1]
            it0 = (res[len(res) - 2] if len(res) > 1 else None)
            if (it.typ == AddressItemToken.ItemType.NUMBER and it0 is not None and it0.ref_token is not None): 
                for s in it0.ref_token.referent.slots: 
                    if (s.type_name == "TYPE"): 
                        ss = (Utils.asObjectOrNull(s.value, str))
                        if ("гараж" in ss or ((ss[0] == 'Г' and ss[len(ss) - 1] == 'К'))): 
                            it.typ = AddressItemToken.ItemType.BOX
                            break
            if (it.typ == AddressItemToken.ItemType.NUMBER or it.typ == AddressItemToken.ItemType.ZIP): 
                del0_ = False
                if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                    del0_ = True
                elif (it.morph.class0_.is_noun): 
                    del0_ = True
                if ((not del0_ and it.end_token.whitespaces_after_count == 1 and it.whitespaces_before_count > 0) and it.typ == AddressItemToken.ItemType.NUMBER): 
                    npt = NounPhraseHelper.tryParse(it.end_token.next0_, NounPhraseParseAttr.NO, 0)
                    if (npt is not None): 
                        del0_ = True
                if (del0_): 
                    del res[len(res) - 1]
                elif ((it.typ == AddressItemToken.ItemType.NUMBER and it0 is not None and it0.typ == AddressItemToken.ItemType.STREET) and it0.ref_token is None): 
                    if (it.begin_token.previous.isChar(',') or it.is_newline_after): 
                        it.typ = AddressItemToken.ItemType.HOUSE
        if (len(res) == 0): 
            return None
        for r in res: 
            if (r.typ == AddressItemToken.ItemType.CITY or r.typ == AddressItemToken.ItemType.REGION): 
                ty = AddressItemToken.__findAddrTyp(r.begin_token, r.end_char, 0)
                if (ty is not None): 
                    r.detail_type = ty.detail_type
                    if (ty.detail_meters > 0): 
                        r.detail_meters = ty.detail_meters
        i = 0
        while i < (len(res) - 1): 
            if (res[i].is_terr_or_rzd and res[i + 1].typ == AddressItemToken.ItemType.KILOMETER and (((i + 1) >= len(res) or not res[i + 1].is_terr_or_rzd))): 
                str0_ = StreetReferent()
                str0_.addSlot(StreetReferent.ATTR_TYP, "километр", True, 0)
                str0_.addSlot(StreetReferent.ATTR_NAME, res[i].referent.getStringValue(GeoReferent.ATTR_NAME), False, 0)
                str0_.addSlot(StreetReferent.ATTR_GEO, res[i].referent, False, 0)
                str0_.number = res[i + 1].value
                t11 = res[i + 1].end_token
                remove2 = False
                if ((res[i].value is None and ((i + 2) < len(res)) and res[i + 2].typ == AddressItemToken.ItemType.NUMBER) and res[i + 2].value is not None): 
                    str0_.number = res[i + 2].value + "км"
                    t11 = res[i + 2].end_token
                    remove2 = True
                ai = AddressItemToken._new86(AddressItemToken.ItemType.STREET, res[i].begin_token, t11, str0_, False)
                res[i] = ai
                del res[i + 1]
                if (remove2): 
                    del res[i + 1]
            elif (res[i + 1].is_terr_or_rzd and res[i].typ == AddressItemToken.ItemType.KILOMETER): 
                str0_ = StreetReferent()
                str0_.addSlot(StreetReferent.ATTR_TYP, "километр", True, 0)
                str0_.addSlot(StreetReferent.ATTR_NAME, res[i + 1].referent.getStringValue(GeoReferent.ATTR_NAME), False, 0)
                str0_.addSlot(StreetReferent.ATTR_GEO, res[i + 1].referent, False, 0)
                str0_.number = res[i].value
                t11 = res[i + 1].end_token
                remove2 = False
                if ((res[i].value is None and ((i + 2) < len(res)) and res[i + 2].typ == AddressItemToken.ItemType.NUMBER) and res[i + 2].value is not None): 
                    str0_.number = res[i + 2].value + "км"
                    t11 = res[i + 2].end_token
                    remove2 = True
                ai = AddressItemToken._new86(AddressItemToken.ItemType.STREET, res[i].begin_token, t11, str0_, False)
                res[i] = ai
                del res[i + 1]
                if (remove2): 
                    del res[i + 1]
            i += 1
        i = 0
        while i < (len(res) - 2): 
            if (res[i].typ == AddressItemToken.ItemType.STREET and res[i + 1].typ == AddressItemToken.ItemType.NUMBER): 
                if ((res[i + 2].typ == AddressItemToken.ItemType.BUSINESSCENTER or res[i + 2].typ == AddressItemToken.ItemType.BUILDING or res[i + 2].typ == AddressItemToken.ItemType.CORPUS) or res[i + 2].typ == AddressItemToken.ItemType.OFFICE or res[i + 2].typ == AddressItemToken.ItemType.FLAT): 
                    res[i + 1].typ = AddressItemToken.ItemType.HOUSE
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i].typ == AddressItemToken.ItemType.STREET and res[i + 1].typ == AddressItemToken.ItemType.KILOMETER and (isinstance(res[i].referent, StreetReferent))) and (Utils.asObjectOrNull(res[i].referent, StreetReferent)).number is None): 
                (Utils.asObjectOrNull(res[i].referent, StreetReferent)).number = res[i + 1].value + "км"
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == AddressItemToken.ItemType.STREET and res[i].typ == AddressItemToken.ItemType.KILOMETER and (isinstance(res[i + 1].referent, StreetReferent))) and (Utils.asObjectOrNull(res[i + 1].referent, StreetReferent)).number is None): 
                (Utils.asObjectOrNull(res[i + 1].referent, StreetReferent)).number = res[i].value + "км"
                res[i + 1].begin_token = res[i].begin_token
                del res[i]
                break
            i += 1
        return res
    
    @staticmethod
    def __findAddrTyp(t : 'Token', max_char : int, lev : int=0) -> 'AddressItemToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (t is None or t.end_char > max_char): 
            return None
        if (lev > 5): 
            return None
        if (isinstance(t, ReferentToken)): 
            geo = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
            if (geo is not None): 
                for s in geo.slots: 
                    if (s.type_name == GeoReferent.ATTR_TYPE): 
                        ty = s.value
                        if ("район" in ty): 
                            return None
            tt = (Utils.asObjectOrNull(t, ReferentToken)).begin_token
            while tt is not None: 
                if (tt.end_char > max_char): 
                    break
                ty = AddressItemToken.__findAddrTyp(tt, max_char, lev + 1)
                if (ty is not None): 
                    return ty
                tt = tt.next0_
        else: 
            ai = AddressItemToken.tryAttachDetail(t)
            if (ai is not None): 
                if (ai.detail_type != AddressDetailType.UNDEFINED or ai.detail_meters > 0): 
                    return ai
        return None
    
    @staticmethod
    def tryParse(t : 'Token', loc_streets : 'IntOntologyCollection', prefix_before : bool, ignore_street : bool=False, prev : 'AddressItemToken'=None) -> 'AddressItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return None
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = AddressItemToken.__TryParse(t, loc_streets, prefix_before, ignore_street, prev)
        t.kit.recurse_level -= 1
        if (((res is not None and not res.is_whitespace_after and res.end_token.next0_ is not None) and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and res.value is not None): 
            if (res.typ == AddressItemToken.ItemType.HOUSE or res.typ == AddressItemToken.ItemType.BUILDING or res.typ == AddressItemToken.ItemType.CORPUS): 
                tt = res.end_token.next0_.next0_
                if (isinstance(tt, NumberToken)): 
                    res.value = "{0}-{1}".format(res.value, (Utils.asObjectOrNull(tt, NumberToken)).value)
                    res.end_token = tt
                    if ((not tt.is_whitespace_after and (isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1) and tt.next0_.chars.is_all_upper): 
                        tt = tt.next0_
                        res.end_token = tt
                        res.value += (Utils.asObjectOrNull(tt, TextToken)).term
                    if ((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.isCharOf("\\/")) and (isinstance(tt.next0_.next0_, NumberToken))): 
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        res.value = "{0}/{1}".format(res.value, (Utils.asObjectOrNull(tt, NumberToken)).value)
                    if ((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_hiphen) and (isinstance(tt.next0_.next0_, NumberToken))): 
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        res.value = "{0}-{1}".format(res.value, (Utils.asObjectOrNull(tt, NumberToken)).value)
                        if ((not tt.is_whitespace_after and (isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1) and tt.next0_.chars.is_all_upper): 
                            tt = tt.next0_
                            res.end_token = tt
                            res.value += (Utils.asObjectOrNull(tt, TextToken)).term
                elif ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_all_upper): 
                    res.value = "{0}-{1}".format(res.value, (Utils.asObjectOrNull(tt, TextToken)).term)
                    res.end_token = tt
        return res
    
    @staticmethod
    def __TryParse(t : 'Token', loc_streets : 'IntOntologyCollection', prefix_before : bool, ignore_street : bool, prev : 'AddressItemToken') -> 'AddressItemToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.date.DateReferent import DateReferent
        if (isinstance(t, ReferentToken)): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            geo = Utils.asObjectOrNull(rt.referent, GeoReferent)
            if (geo is not None): 
                if (geo.is_city or geo.is_territory): 
                    ty = AddressItemToken.ItemType.CITY
                elif (geo.is_state): 
                    ty = AddressItemToken.ItemType.COUNTRY
                else: 
                    ty = AddressItemToken.ItemType.REGION
                return AddressItemToken._new83(ty, t, t, rt.referent)
        if (not ignore_street and t is not None and prev is not None): 
            if (t.isValue("КВ", None) or t.isValue("КВАРТ", None)): 
                if (((prev.typ == AddressItemToken.ItemType.HOUSE or prev.typ == AddressItemToken.ItemType.NUMBER or prev.typ == AddressItemToken.ItemType.BUILDING) or prev.typ == AddressItemToken.ItemType.CORPUS or prev.typ == AddressItemToken.ItemType.CORPUSORFLAT) or prev.typ == AddressItemToken.ItemType.DETAIL): 
                    ignore_street = True
        if (not ignore_street): 
            sli = StreetItemToken.tryParseList(t, loc_streets, 10)
            if (sli is not None): 
                rt = StreetDefineHelper._tryParseStreet(sli, prefix_before, False)
                if (rt is not None): 
                    crlf = False
                    ttt = rt.begin_token
                    while ttt != rt.end_token: 
                        if (ttt.is_newline_after): 
                            crlf = True
                            break
                        ttt = ttt.next0_
                    if (crlf): 
                        ttt = rt.begin_token.previous
                        first_pass2735 = True
                        while True:
                            if first_pass2735: first_pass2735 = False
                            else: ttt = ttt.previous
                            if (not (ttt is not None)): break
                            if (ttt.morph.class0_.is_preposition or ttt.is_comma): 
                                continue
                            if (isinstance(ttt.getReferent(), GeoReferent)): 
                                crlf = False
                            break
                        if (sli[0].typ == StreetItemType.NOUN and "ДОРОГА" in sli[0].termin.canonic_text): 
                            crlf = False
                    if (crlf): 
                        aat = AddressItemToken.tryParse(rt.end_token.next0_, None, False, True, None)
                        if (aat is None): 
                            return None
                        if (aat.typ != AddressItemToken.ItemType.HOUSE): 
                            return None
                    return rt
                if (len(sli) == 1 and sli[0].typ == StreetItemType.NOUN): 
                    tt = sli[0].end_token.next0_
                    if (tt is not None and ((tt.is_hiphen or tt.isChar('_') or tt.isValue("НЕТ", None)))): 
                        ttt = tt.next0_
                        if (ttt is not None and ttt.is_comma): 
                            ttt = ttt.next0_
                        att = AddressItemToken.tryParse(ttt, None, False, True, None)
                        if (att is not None): 
                            if (att.typ == AddressItemToken.ItemType.HOUSE or att.typ == AddressItemToken.ItemType.CORPUS or att.typ == AddressItemToken.ItemType.BUILDING): 
                                return AddressItemToken(AddressItemToken.ItemType.STREET, t, tt)
        if (isinstance(t, ReferentToken)): 
            return None
        if (isinstance(t, NumberToken)): 
            n = Utils.asObjectOrNull(t, NumberToken)
            if (((n.length_char == 6 or n.length_char == 5)) and n.typ == NumberSpellingType.DIGIT and not n.morph.class0_.is_adjective): 
                return AddressItemToken._new84(AddressItemToken.ItemType.ZIP, t, t, str(n.value))
            ok = False
            if ((t.previous is not None and t.previous.morph.class0_.is_preposition and t.next0_ is not None) and t.next0_.chars.is_letter and t.next0_.chars.is_all_lower): 
                ok = True
            elif (t.morph.class0_.is_adjective and not t.morph.class0_.is_noun): 
                ok = True
            tok0 = AddressItemToken.M_ONTOLOGY.tryParse(t.next0_, TerminParseAttr.NO)
            if (tok0 is not None and (isinstance(tok0.termin.tag, AddressItemToken.ItemType))): 
                if (tok0.end_token.next0_ is None or tok0.end_token.next0_.is_comma or tok0.end_token.is_newline_after): 
                    ok = True
                typ0 = Utils.valToEnum(tok0.termin.tag, AddressItemToken.ItemType)
                if (typ0 == AddressItemToken.ItemType.FLAT): 
                    if ((isinstance(t.next0_, TextToken)) and t.next0_.isValue("КВ", None)): 
                        if (t.next0_.getSourceText() == "кВ"): 
                            return None
                    if ((isinstance(tok0.end_token.next0_, NumberToken)) and (tok0.end_token.whitespaces_after_count < 3)): 
                        if (prev is not None and ((prev.typ == AddressItemToken.ItemType.STREET or prev.typ == AddressItemToken.ItemType.CITY))): 
                            return AddressItemToken._new84(AddressItemToken.ItemType.NUMBER, t, t, str(n.value))
                if ((typ0 == AddressItemToken.ItemType.KILOMETER or typ0 == AddressItemToken.ItemType.FLOOR or typ0 == AddressItemToken.ItemType.BLOCK) or typ0 == AddressItemToken.ItemType.POTCH or typ0 == AddressItemToken.ItemType.FLAT): 
                    return AddressItemToken._new84(typ0, t, tok0.end_token, str(n.value))
        prepos = False
        tok = None
        if (t.morph.class0_.is_preposition): 
            tok = AddressItemToken.M_ONTOLOGY.tryParse(t, TerminParseAttr.NO)
            if ((tok) is None): 
                if (t.begin_char < t.end_char): 
                    return None
                if (not t.isCharOf("КСкс")): 
                    t = t.next0_
                prepos = True
        if (tok is None): 
            tok = AddressItemToken.M_ONTOLOGY.tryParse(t, TerminParseAttr.NO)
        t1 = t
        typ_ = AddressItemToken.ItemType.NUMBER
        house_typ = AddressHouseType.UNDEFINED
        build_typ = AddressBuildingType.UNDEFINED
        if (tok is not None): 
            if (t.isValue("УЖЕ", None)): 
                return None
            if (tok.termin.canonic_text == "ТАМ ЖЕ"): 
                cou = 0
                tt = t.previous
                first_pass2736 = True
                while True:
                    if first_pass2736: first_pass2736 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (cou > 1000): 
                        break
                    r = tt.getReferent()
                    if (r is None): 
                        continue
                    if (isinstance(r, AddressReferent)): 
                        g = Utils.asObjectOrNull(r.getSlotValue(AddressReferent.ATTR_GEO), GeoReferent)
                        if (g is not None): 
                            return AddressItemToken._new83(AddressItemToken.ItemType.CITY, t, tok.end_token, g)
                        break
                    elif (isinstance(r, GeoReferent)): 
                        g = Utils.asObjectOrNull(r, GeoReferent)
                        if (not g.is_state): 
                            return AddressItemToken._new83(AddressItemToken.ItemType.CITY, t, tok.end_token, g)
                return None
            if (isinstance(tok.termin.tag, AddressDetailType)): 
                return AddressItemToken.tryAttachDetail(t)
            t1 = tok.end_token.next0_
            if (isinstance(tok.termin.tag, AddressItemToken.ItemType)): 
                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                if (isinstance(tok.termin.tag2, AddressBuildingType)): 
                    build_typ = (Utils.valToEnum(tok.termin.tag2, AddressBuildingType))
                typ_ = (Utils.valToEnum(tok.termin.tag, AddressItemToken.ItemType))
                if (typ_ == AddressItemToken.ItemType.PREFIX): 
                    first_pass2737 = True
                    while True:
                        if first_pass2737: first_pass2737 = False
                        else: t1 = t1.next0_
                        if (not (t1 is not None)): break
                        if (((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and t1.whitespaces_after_count == 1): 
                            continue
                        if (t1.isChar(':')): 
                            t1 = t1.next0_
                            break
                        if (t1.isChar('(')): 
                            br = BracketHelper.tryParse(t1, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                t1 = br.end_token
                                continue
                        if ((isinstance(t1, TextToken)) and t1.chars.is_all_lower): 
                            npt = NounPhraseHelper.tryParse(t1, NounPhraseParseAttr.NO, 0)
                            if (npt is not None): 
                                t1 = npt.end_token
                                continue
                        if (t1.isValue("УКАЗАННЫЙ", None) or t1.isValue("ЕГРИП", None) or t1.isValue("ФАКТИЧЕСКИЙ", None)): 
                            continue
                        if (t1.is_comma): 
                            if (t1.next0_ is not None and t1.next0_.isValue("УКАЗАННЫЙ", None)): 
                                continue
                        break
                    if (t1 is not None): 
                        t0 = t
                        if (((t0.previous is not None and not t0.is_newline_before and t0.previous.isChar(')')) and (isinstance(t0.previous.previous, TextToken)) and t0.previous.previous.previous is not None) and t0.previous.previous.previous.isChar('(')): 
                            t = t0.previous.previous.previous.previous
                            if (t is not None and t.getMorphClassInDictionary().is_adjective and not t.is_newline_after): 
                                t0 = t
                        res = AddressItemToken(AddressItemToken.ItemType.PREFIX, t0, t1.previous)
                        tt = t0.previous
                        first_pass2738 = True
                        while True:
                            if first_pass2738: first_pass2738 = False
                            else: tt = tt.previous
                            if (not (tt is not None)): break
                            if (tt.newlines_after_count > 3): 
                                break
                            if (tt.is_comma_and or tt.isCharOf("().")): 
                                continue
                            if (not ((isinstance(tt, TextToken)))): 
                                break
                            if (((tt.isValue("ПОЧТОВЫЙ", None) or tt.isValue("ЮРИДИЧЕСКИЙ", None) or tt.isValue("ЮР", None)) or tt.isValue("ФАКТИЧЕСКИЙ", None) or tt.isValue("ФАКТ", None)) or tt.isValue("ПОЧТ", None) or tt.isValue("АДРЕС", None)): 
                                res.begin_token = tt
                            else: 
                                break
                        return res
                    else: 
                        return None
                elif (typ_ == AddressItemToken.ItemType.BUSINESSCENTER): 
                    rt = t.kit.processReferent("ORGANIZATION", t)
                    if (rt is not None): 
                        return AddressItemToken._new94(typ_, t, rt.end_token, rt)
                elif ((typ_ == AddressItemToken.ItemType.CORPUSORFLAT and not tok.is_whitespace_before and not tok.is_whitespace_after) and tok.begin_token == tok.end_token and tok.begin_token.isValue("К", None)): 
                    typ_ = AddressItemToken.ItemType.CORPUS
                if (typ_ == AddressItemToken.ItemType.DETAIL and t.isValue("У", None)): 
                    if (not MiscLocationHelper.checkGeoObjectBefore(t)): 
                        return None
                if (typ_ == AddressItemToken.ItemType.FLAT and t.isValue("КВ", None)): 
                    if (t.getSourceText() == "кВ"): 
                        return None
                if (typ_ == AddressItemToken.ItemType.KILOMETER or typ_ == AddressItemToken.ItemType.FLOOR or typ_ == AddressItemToken.ItemType.POTCH): 
                    return AddressItemToken(typ_, t, tok.end_token)
                if ((typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.BUILDING or typ_ == AddressItemToken.ItemType.CORPUS) or typ_ == AddressItemToken.ItemType.PLOT): 
                    if (t1 is not None and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and (t1.whitespaces_after_count < 2)): 
                        tok2 = AddressItemToken.M_ONTOLOGY.tryParse(t1.next0_, TerminParseAttr.NO)
                        if (tok2 is not None and (isinstance(tok2.termin.tag, AddressItemToken.ItemType))): 
                            typ2 = Utils.valToEnum(tok2.termin.tag, AddressItemToken.ItemType)
                            if (typ2 != typ_ and ((typ2 == AddressItemToken.ItemType.PLOT or ((typ2 == AddressItemToken.ItemType.HOUSE and typ_ == AddressItemToken.ItemType.PLOT))))): 
                                typ_ = typ2
                                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                                t1 = tok2.end_token.next0_
                                if (t1 is None): 
                                    return AddressItemToken._new95(typ_, t, tok2.end_token, "0", house_typ)
                if (typ_ != AddressItemToken.ItemType.NUMBER): 
                    if (t1 is None and t.length_char > 1): 
                        return AddressItemToken._new96(typ_, t, tok.end_token, house_typ, build_typ)
                    if ((isinstance(t1, NumberToken)) and (Utils.asObjectOrNull(t1, NumberToken)).value == (0)): 
                        return AddressItemToken._new97(typ_, t, t1, "0", house_typ, build_typ)
        if (t1 is not None and t1.isChar('.') and t1.next0_ is not None): 
            if (not t1.is_whitespace_after): 
                t1 = t1.next0_
            elif ((isinstance(t1.next0_, NumberToken)) and (Utils.asObjectOrNull(t1.next0_, NumberToken)).typ == NumberSpellingType.DIGIT and (t1.whitespaces_after_count < 2)): 
                t1 = t1.next0_
        if ((t1 is not None and not t1.is_whitespace_after and ((t1.is_hiphen or t1.isChar('_')))) and (isinstance(t1.next0_, NumberToken))): 
            t1 = t1.next0_
        tok = AddressItemToken.M_ONTOLOGY.tryParse(t1, TerminParseAttr.NO)
        if (tok is not None and (isinstance(tok.termin.tag, AddressItemToken.ItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemToken.ItemType)) == AddressItemToken.ItemType.NUMBER): 
            t1 = tok.end_token.next0_
        elif (tok is not None and (isinstance(tok.termin.tag, AddressItemToken.ItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemToken.ItemType)) == AddressItemToken.ItemType.NONUMBER): 
            re0 = AddressItemToken._new97(typ_, t, tok.end_token, "0", house_typ, build_typ)
            if (not re0.is_whitespace_after and (isinstance(re0.end_token.next0_, NumberToken))): 
                re0.end_token = re0.end_token.next0_
                re0.value = str((Utils.asObjectOrNull(re0.end_token, NumberToken)).value)
            return re0
        elif (t1 is not None): 
            if (typ_ == AddressItemToken.ItemType.FLAT): 
                tok2 = AddressItemToken.M_ONTOLOGY.tryParse(t1, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, AddressItemToken.ItemType)) == AddressItemToken.ItemType.FLAT): 
                    t1 = tok2.end_token.next0_
            if (t1.isValue("СТРОИТЕЛЬНЫЙ", None) and t1.next0_ is not None): 
                t1 = t1.next0_
            ttt = MiscHelper.checkNumberPrefix(t1)
            if (ttt is not None): 
                t1 = ttt
                if (t1.is_hiphen or t1.isChar('_')): 
                    t1 = t1.next0_
        if (t1 is None): 
            return None
        num = io.StringIO()
        nt = Utils.asObjectOrNull(t1, NumberToken)
        if (nt is not None): 
            if (nt.value == (0)): 
                return None
            print(nt.value, end="", file=num)
            if (nt.typ == NumberSpellingType.DIGIT or nt.typ == NumberSpellingType.WORDS): 
                if (((isinstance(nt.end_token, TextToken)) and (Utils.asObjectOrNull(nt.end_token, TextToken)).term == "Е" and nt.end_token.previous == nt.begin_token) and not nt.end_token.is_whitespace_before): 
                    print("Е", end="", file=num)
                drob = False
                hiph = False
                lit = False
                et = nt.next0_
                if (et is not None and ((et.isCharOf("\\/") or et.isValue("ДРОБЬ", None)))): 
                    drob = True
                    et = et.next0_
                    if (et is not None and et.isCharOf("\\/")): 
                        et = et.next0_
                    t1 = et
                elif (et is not None and ((et.is_hiphen or et.isChar('_')))): 
                    hiph = True
                    et = et.next0_
                elif ((et is not None and et.isChar('.') and (isinstance(et.next0_, NumberToken))) and not et.is_whitespace_after): 
                    return None
                if (isinstance(et, NumberToken)): 
                    if (drob): 
                        print("/{0}".format((Utils.asObjectOrNull(et, NumberToken)).value), end="", file=num, flush=True)
                        drob = False
                        t1 = et
                        et = et.next0_
                        if (et is not None and et.isCharOf("\\/") and (isinstance(et.next0_, NumberToken))): 
                            t1 = et.next0_
                            print("/{0}".format((Utils.asObjectOrNull(t1, NumberToken)).value), end="", file=num, flush=True)
                            et = t1.next0_
                    elif ((hiph and not t1.is_whitespace_after and (isinstance(et, NumberToken))) and not et.is_whitespace_before): 
                        numm = AddressItemToken.tryParse(et, None, False, True, None)
                        if (numm is not None and numm.typ == AddressItemToken.ItemType.NUMBER): 
                            merge = False
                            if (typ_ == AddressItemToken.ItemType.FLAT or typ_ == AddressItemToken.ItemType.PLOT): 
                                merge = True
                            elif (typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.BUILDING or typ_ == AddressItemToken.ItemType.CORPUS): 
                                ttt = numm.end_token.next0_
                                if (ttt is not None and ttt.is_comma): 
                                    ttt = ttt.next0_
                                numm2 = AddressItemToken.tryParse(ttt, None, False, True, None)
                                if (numm2 is not None): 
                                    if ((numm2.typ == AddressItemToken.ItemType.FLAT or numm2.typ == AddressItemToken.ItemType.BUILDING or ((numm2.typ == AddressItemToken.ItemType.CORPUSORFLAT and numm2.value is not None))) or numm2.typ == AddressItemToken.ItemType.CORPUS): 
                                        merge = True
                            if (merge): 
                                print("/{0}".format(numm.value), end="", file=num, flush=True)
                                t1 = numm.end_token
                                et = t1.next0_
                elif (et is not None and ((et.is_hiphen or et.isChar('_') or et.isValue("НЕТ", None))) and drob): 
                    t1 = et
                if (((BracketHelper.isBracket(et, False) and (isinstance(et.next0_, TextToken)) and et.next0_.length_char == 1) and et.next0_.is_letters and BracketHelper.isBracket(et.next0_.next0_, False)) and not et.is_whitespace_after and not et.next0_.is_whitespace_after): 
                    ch = AddressItemToken.__correctCharToken(et.next0_)
                    if (ch is None): 
                        return None
                    print(ch, end="", file=num)
                    t1 = et.next0_.next0_
                elif (BracketHelper.canBeStartOfSequence(et, True, False) and (et.whitespaces_before_count < 2)): 
                    br = BracketHelper.tryParse(et, BracketParseAttr.NO, 100)
                    if (br is not None and (isinstance(br.begin_token.next0_, TextToken)) and br.begin_token.next0_.next0_ == br.end_token): 
                        s = AddressItemToken.__correctCharToken(br.begin_token.next0_)
                        if (s is not None): 
                            print(s, end="", file=num)
                            t1 = br.end_token
                elif ((isinstance(et, TextToken)) and (Utils.asObjectOrNull(et, TextToken)).length_char == 1): 
                    s = AddressItemToken.__correctCharToken(et)
                    if (s is not None): 
                        if (((s == "К" or s == "С")) and (isinstance(et.next0_, NumberToken)) and not et.is_whitespace_after): 
                            pass
                        elif ((s == "Б" and et.next0_ is not None and et.next0_.isCharOf("/\\")) and (isinstance(et.next0_.next0_, TextToken)) and et.next0_.next0_.isValue("Н", None)): 
                            et = et.next0_.next0_
                            t1 = et
                        else: 
                            ok = False
                            if (drob or hiph or lit): 
                                ok = True
                            elif (not et.is_whitespace_before or ((et.whitespaces_before_count == 1 and et.chars.is_all_upper))): 
                                ok = True
                                if (isinstance(et.next0_, NumberToken)): 
                                    if (not et.is_whitespace_before and et.is_whitespace_after): 
                                        pass
                                    else: 
                                        ok = False
                            elif (((et.next0_ is None or et.next0_.is_comma)) and (et.whitespaces_before_count < 2)): 
                                ok = True
                            elif (et.is_whitespace_before and et.chars.is_all_lower and et.isValue("В", "У")): 
                                pass
                            else: 
                                ait_next = AddressItemToken.tryParse(et.next0_, None, False, True, None)
                                if (ait_next is not None): 
                                    if ((ait_next.typ == AddressItemToken.ItemType.CORPUS or ait_next.typ == AddressItemToken.ItemType.FLAT or ait_next.typ == AddressItemToken.ItemType.BUILDING) or ait_next.typ == AddressItemToken.ItemType.OFFICE): 
                                        ok = True
                            if (ok): 
                                print(s, end="", file=num)
                                t1 = et
                                if (et.next0_ is not None and et.next0_.isCharOf("\\/") and et.next0_.next0_ is not None): 
                                    if (isinstance(et.next0_.next0_, NumberToken)): 
                                        print("/{0}".format((Utils.asObjectOrNull(et.next0_.next0_, NumberToken)).value), end="", file=num, flush=True)
                                        et = et.next0_.next0_
                                        t1 = et
                                    elif (et.next0_.next0_.is_hiphen or et.next0_.next0_.isChar('_') or et.next0_.next0_.isValue("НЕТ", None)): 
                                        et = et.next0_.next0_
                                        t1 = et
                elif ((isinstance(et, TextToken)) and not et.is_whitespace_before): 
                    val = (Utils.asObjectOrNull(et, TextToken)).term
                    if (val == "КМ" and typ_ == AddressItemToken.ItemType.HOUSE): 
                        t1 = et
                        print("КМ", end="", file=num)
                    elif (val == "БН"): 
                        t1 = et
                    elif (((len(val) == 2 and val[1] == 'Б' and et.next0_ is not None) and et.next0_.isCharOf("\\/") and et.next0_.next0_ is not None) and et.next0_.next0_.isValue("Н", None)): 
                        print(val[0], end="", file=num)
                        et = et.next0_.next0_
                        t1 = et
        else: 
            re11 = AddressItemToken.__tryAttachVCH(t1, typ_)
            if ((re11) is not None): 
                re11.begin_token = t
                re11.house_type = house_typ
                re11.building_type = build_typ
                return re11
            elif ((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.is_letters): 
                ch = AddressItemToken.__correctCharToken(t1)
                if (ch is not None): 
                    if (typ_ == AddressItemToken.ItemType.NUMBER): 
                        return None
                    if (ch == "К" or ch == "С"): 
                        if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                            return None
                    if (ch == "Д" and typ_ == AddressItemToken.ItemType.PLOT): 
                        rrr = AddressItemToken.__TryParse(t1, None, False, True, None)
                        if (rrr is not None): 
                            rrr.typ = AddressItemToken.ItemType.PLOT
                            rrr.begin_token = t
                            return rrr
                    if (t1.chars.is_all_lower and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction))): 
                        if ((t1.whitespaces_after_count < 2) and t1.next0_.chars.is_letter): 
                            return None
                    if (t.chars.is_all_upper and t.length_char == 1 and t.next0_.isChar('.')): 
                        return None
                    print(ch, end="", file=num)
                    if ((t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.isChar('_'))) and not t1.is_whitespace_after) and (isinstance(t1.next0_.next0_, NumberToken)) and not t1.next0_.is_whitespace_after): 
                        print((Utils.asObjectOrNull(t1.next0_.next0_, NumberToken)).value, end="", file=num)
                        t1 = t1.next0_.next0_
                    elif ((isinstance(t1.next0_, NumberToken)) and not t1.is_whitespace_after and t1.chars.is_all_upper): 
                        print((Utils.asObjectOrNull(t1.next0_, NumberToken)).value, end="", file=num)
                        t1 = t1.next0_
                if (typ_ == AddressItemToken.ItemType.BOX and num.tell() == 0): 
                    rom = NumberHelper.tryParseRoman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new84(typ_, t, rom.end_token, str(rom.value))
            elif (((BracketHelper.isBracket(t1, False) and (isinstance(t1.next0_, TextToken)) and t1.next0_.length_char == 1) and t1.next0_.is_letters and BracketHelper.isBracket(t1.next0_.next0_, False)) and not t1.is_whitespace_after and not t1.next0_.is_whitespace_after): 
                ch = AddressItemToken.__correctCharToken(t1.next0_)
                if (ch is None): 
                    return None
                print(ch, end="", file=num)
                t1 = t1.next0_.next0_
            elif ((isinstance(t1, TextToken)) and ((((t1.length_char == 1 and ((t1.is_hiphen or t1.isChar('_'))))) or t1.isValue("НЕТ", None) or t1.isValue("БН", None))) and (((typ_ == AddressItemToken.ItemType.CORPUS or typ_ == AddressItemToken.ItemType.CORPUSORFLAT or typ_ == AddressItemToken.ItemType.BUILDING) or typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.FLAT))): 
                while t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.isChar('_'))) and not t1.is_whitespace_after:
                    t1 = t1.next0_
                val = None
                if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                    t1 = t1.next0_
                    val = str((Utils.asObjectOrNull(t1, NumberToken)).value)
                if (t1.isValue("БН", None)): 
                    val = "0"
                return AddressItemToken._new84(typ_, t, t1, val)
            else: 
                if (((typ_ == AddressItemToken.ItemType.FLOOR or typ_ == AddressItemToken.ItemType.KILOMETER or typ_ == AddressItemToken.ItemType.POTCH)) and (isinstance(t.previous, NumberToken))): 
                    return AddressItemToken(typ_, t, t1.previous)
                if ((isinstance(t1, ReferentToken)) and (isinstance(t1.getReferent(), DateReferent))): 
                    nn = AddressItemToken.__TryParse((Utils.asObjectOrNull(t1, ReferentToken)).begin_token, loc_streets, prefix_before, True, None)
                    if (nn is not None and nn.end_char == t1.end_char and nn.typ == AddressItemToken.ItemType.NUMBER): 
                        nn.begin_token = t
                        nn.end_token = t1
                        nn.typ = typ_
                        return nn
                if ((isinstance(t1, TextToken)) and ((typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.BUILDING or typ_ == AddressItemToken.ItemType.CORPUS))): 
                    ter = (Utils.asObjectOrNull(t1, TextToken)).term
                    if (ter == "АБ" or ter == "АБВ" or ter == "МГУ"): 
                        return AddressItemToken._new97(typ_, t, t1, ter, house_typ, build_typ)
                    if (prev is not None and ((prev.typ == AddressItemToken.ItemType.STREET or prev.typ == AddressItemToken.ItemType.CITY)) and t1.chars.is_all_upper): 
                        return AddressItemToken._new97(typ_, t, t1, ter, house_typ, build_typ)
                if (typ_ == AddressItemToken.ItemType.BOX): 
                    rom = NumberHelper.tryParseRoman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new84(typ_, t, rom.end_token, str(rom.value))
                if (typ_ == AddressItemToken.ItemType.PLOT and t1 is not None): 
                    if ((t1.isValue("ОКОЛО", None) or t1.isValue("РЯДОМ", None) or t1.isValue("НАПРОТИВ", None)) or t1.isValue("БЛИЗЬКО", None) or t1.isValue("НАВПАКИ", None)): 
                        return AddressItemToken._new84(typ_, t, t1, t1.getSourceText().lower())
                return None
        if (typ_ == AddressItemToken.ItemType.NUMBER and prepos): 
            return None
        if (t1 is None): 
            t1 = t
            while t1.next0_ is not None:
                t1 = t1.next0_
        return AddressItemToken._new105(typ_, t, t1, Utils.toStringStringIO(num), t.morph, house_typ, build_typ)
    
    @staticmethod
    def __tryAttachVCH(t : 'Token', ty : 'ItemType') -> 'AddressItemToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        tt = t
        while tt is not None: 
            if ((((tt.isValue("В", None) or tt.isValue("B", None))) and tt.next0_ is not None and tt.next0_.isCharOf("./\\")) and (isinstance(tt.next0_.next0_, TextToken)) and tt.next0_.next0_.isValue("Ч", None)): 
                tt = tt.next0_.next0_
                if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                    tt = tt.next0_
                tt2 = MiscHelper.checkNumberPrefix(tt.next0_)
                if (tt2 is not None): 
                    tt = tt2
                if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                    tt = tt.next0_
                return AddressItemToken._new84(ty, t, tt, "В/Ч")
            elif (((tt.isValue("ВОЙСКОВОЙ", None) or tt.isValue("ВОИНСКИЙ", None))) and tt.next0_ is not None and tt.next0_.isValue("ЧАСТЬ", None)): 
                tt = tt.next0_
                tt2 = MiscHelper.checkNumberPrefix(tt.next0_)
                if (tt2 is not None): 
                    tt = tt2
                if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                    tt = tt.next0_
                return AddressItemToken._new84(ty, t, tt, "В/Ч")
            elif (ty == AddressItemToken.ItemType.FLAT): 
                if (tt.whitespaces_before_count > 1): 
                    break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if ((Utils.asObjectOrNull(tt, TextToken)).term.startswith("ОБЩ")): 
                    if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                        tt = tt.next0_
                    re = AddressItemToken.__tryAttachVCH(tt.next0_, ty)
                    if (re is not None): 
                        return re
                    return AddressItemToken._new84(ty, t, tt, "ОБЩ")
                if (tt.chars.is_all_upper and tt.length_char > 1): 
                    re = AddressItemToken._new84(ty, t, tt, (Utils.asObjectOrNull(tt, TextToken)).term)
                    if ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_all_upper): 
                        tt = tt.next0_
                        re.end_token = tt
                        re.value += (Utils.asObjectOrNull(tt, TextToken)).term
                    return re
                break
            else: 
                break
            tt = tt.next0_
        return None
    
    @staticmethod
    def tryAttachDetail(t : 'Token') -> 'AddressItemToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        if (t is None or ((isinstance(t, ReferentToken)))): 
            return None
        tt = t
        if (t.chars.is_capital_upper and not t.morph.class0_.is_preposition): 
            return None
        tok = AddressItemToken.M_ONTOLOGY.tryParse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_preposition and t.next0_ is not None): 
            tt = t.next0_
            if (isinstance(tt, NumberToken)): 
                pass
            else: 
                if (tt.chars.is_capital_upper and not tt.morph.class0_.is_preposition): 
                    return None
                tok = AddressItemToken.M_ONTOLOGY.tryParse(tt, TerminParseAttr.NO)
        res = None
        first_num = False
        if (tok is None): 
            if (isinstance(tt, NumberToken)): 
                first_num = True
                nex = NumberExToken.tryParseNumberWithPostfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    res = AddressItemToken(AddressItemToken.ItemType.DETAIL, t, nex.end_token)
                    tyy = NumberExType.METER
                    wraptyy110 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalizeValue(wraptyy110)))
                    tyy = wraptyy110.value
            if (res is None): 
                return None
        else: 
            if (not ((isinstance(tok.termin.tag, AddressDetailType)))): 
                return None
            if (t.isValue("У", None)): 
                if (MiscLocationHelper.checkGeoObjectBefore(t)): 
                    pass
                elif (MiscLocationHelper.checkGeoObjectAfter(t)): 
                    pass
                else: 
                    return None
            res = AddressItemToken._new111(AddressItemToken.ItemType.DETAIL, t, tok.end_token, Utils.valToEnum(tok.termin.tag, AddressDetailType))
        tt = res.end_token.next0_
        first_pass2739 = True
        while True:
            if first_pass2739: first_pass2739 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (isinstance(tt, ReferentToken)): 
                break
            if (not tt.morph.class0_.is_preposition): 
                if (tt.chars.is_capital_upper or tt.chars.is_all_upper): 
                    break
            tok = AddressItemToken.M_ONTOLOGY.tryParse(tt, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, AddressDetailType))): 
                ty = Utils.valToEnum(tok.termin.tag, AddressDetailType)
                if (ty != AddressDetailType.UNDEFINED): 
                    if (ty == AddressDetailType.NEAR and res.detail_type != AddressDetailType.UNDEFINED and res.detail_type != ty): 
                        pass
                    else: 
                        res.detail_type = ty
                tt = tok.end_token
                res.end_token = tt
                continue
            if (tt.isValue("ОРИЕНТИР", None) or tt.isValue("НАПРАВЛЕНИЕ", None) or tt.isValue("ОТ", None)): 
                res.end_token = tt
                continue
            if (tt.is_comma or tt.morph.class0_.is_preposition): 
                continue
            if ((isinstance(tt, NumberToken)) and tt.next0_ is not None): 
                nex = NumberExToken.tryParseNumberWithPostfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    tt = nex.end_token
                    res.end_token = tt
                    tyy = NumberExType.METER
                    wraptyy112 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalizeValue(wraptyy112)))
                    tyy = wraptyy112.value
                    continue
            break
        if (first_num and res.detail_type == AddressDetailType.UNDEFINED): 
            return None
        if (res is not None and res.end_token.next0_ is not None and res.end_token.next0_.morph.class0_.is_preposition): 
            if (res.end_token.whitespaces_after_count == 1 and res.end_token.next0_.whitespaces_after_count == 1): 
                res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def tryAttachOrg(t : 'Token') -> 'AddressItemToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.Referent import Referent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (not ((isinstance(t, TextToken)))): 
            return None
        if ((t.length_char > 5 and not t.chars.is_all_upper and not t.chars.is_all_lower) and not t.chars.is_capital_upper): 
            namm = (Utils.asObjectOrNull(t, TextToken)).getSourceText()
            if (str.isupper(namm[0]) and str.isupper(namm[1])): 
                i = 0
                while i < len(namm): 
                    if (str.islower(namm[i]) and i > 2): 
                        abbr = namm[0:0+i - 1]
                        te = Termin._new113(abbr, abbr)
                        li = AddressItemToken.M_ORG_ONTOLOGY.tryAttach(te)
                        if (li is not None and len(li) > 0): 
                            org00 = t.kit.createReferent("ORGANIZATION")
                            org00.addSlot("TYPE", li[0].canonic_text.lower(), False, 0)
                            org00.addSlot("TYPE", abbr, False, 0)
                            namm = (Utils.asObjectOrNull(t, TextToken)).term[i - 1:]
                            rt00 = ReferentToken(org00, t, t)
                            rt00.data = t.kit.getAnalyzerDataByAnalyzerName("ORGANIZATION")
                            if (t.next0_ is not None and t.next0_.is_hiphen): 
                                if (isinstance(t.next0_.next0_, NumberToken)): 
                                    org00.addSlot("NUMBER", str((Utils.asObjectOrNull(t.next0_.next0_, NumberToken)).value), False, 0)
                                    rt00.end_token = t.next0_.next0_
                                elif ((isinstance(t.next0_.next0_, TextToken)) and not t.next0_.is_whitespace_after): 
                                    namm = "{0}-{1}".format(namm, (Utils.asObjectOrNull(t.next0_.next0_, TextToken)).term)
                                    rt00.end_token = t.next0_.next0_
                            org00.addSlot("NAME", namm, False, 0)
                            return AddressItemToken._new114(AddressItemToken.ItemType.STREET, t, rt00.end_token, rt00.referent, rt00, True)
                        break
                    i += 1
        if (t.isValue("СНТ", None) and (isinstance(t.next0_, ReferentToken))): 
            pass
        rt = None
        typ_ = None
        typ2 = None
        nam = None
        num = None
        t1 = None
        ok = False
        tok = AddressItemToken.M_ORG_ONTOLOGY.tryParse(t, TerminParseAttr.NO)
        rt1 = t.kit.processReferent("ORGANIZATION", t)
        if (rt1 is None): 
            rt1 = t.kit.processReferent("NAMEDENTITY", t)
            if (rt1 is not None): 
                tyy = rt1.referent.getStringValue("TYPE")
                if (((tyy == "аэропорт" or tyy == "аэродром" or tyy == "заказник") or tyy == "лес" or tyy == "заповедник") or tyy == "сад"): 
                    pass
                else: 
                    rt1 = (None)
        else: 
            tt = rt1.begin_token.next0_
            while tt is not None and (tt.end_char < rt1.end_char): 
                if (tt.is_comma): 
                    rt1.end_token = tt.previous
                    if (isinstance(tt.next0_, ReferentToken)): 
                        s = rt1.referent.findSlot(None, tt.next0_.getReferent(), True)
                        if (s is not None): 
                            rt1.referent.slots.remove(s)
                tt = tt.next0_
            tt = rt1.end_token.next0_
            while tt is not None: 
                if (tt.is_hiphen or tt.is_comma): 
                    pass
                elif ((isinstance(tt, TextToken)) and (Utils.asObjectOrNull(tt, TextToken)).term == "ПМК"): 
                    tt2 = tt.next0_
                    if (tt2 is not None and ((tt2.is_hiphen or tt2.isCharOf(":")))): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2, NumberToken)): 
                        rt1.referent.addSlot("NUMBER", str((Utils.asObjectOrNull(tt2, NumberToken)).value), False, 0)
                        rt1.end_token = tt2
                        break
                else: 
                    break
                tt = tt.next0_
        tt1 = t.next0_
        if (tt1 is not None and tt1.isValue("ПМК", None)): 
            tt1 = tt1.next0_
        if (tok is not None): 
            if (tok.begin_token == tok.end_token and tok.begin_token.isValue("СП", None)): 
                tok = AddressItemToken.M_ORG_ONTOLOGY.tryParse(tok.end_token.next0_, TerminParseAttr.NO)
                if (tok is not None): 
                    tok.begin_token = t
                    ok = True
                    tt1 = tok.end_token.next0_
                if (rt1 is None): 
                    rt1 = t.kit.processReferent("ORGANIZATION", t.next0_)
                    if ((rt1) is not None): 
                        rt1.begin_token = t
            elif (tok.begin_token == tok.end_token and tok.begin_token.isValue("ГПК", None)): 
                tt1 = tok.end_token.next0_
                if (tt1 is None or tok.is_newline_after or not ((isinstance(tt1, TextToken)))): 
                    return None
                if (tt1.kit.processReferent("GEO", tt1) is not None): 
                    return None
                if (tt1.chars.is_all_upper or BracketHelper.canBeStartOfSequence(tt1, True, False)): 
                    pass
                else: 
                    return None
            else: 
                ok = True
                tt1 = tok.end_token.next0_
            tok2 = AddressItemToken.M_ORG_ONTOLOGY.tryParse(tt1, TerminParseAttr.NO)
            if (tok2 is not None): 
                tt1 = tok2.end_token.next0_
                tok2 = AddressItemToken.M_ORG_ONTOLOGY.tryParse(tt1, TerminParseAttr.NO)
                if (tok2 is not None): 
                    tt1 = tok2.end_token.next0_
            while tt1 is not None:
                if (tt1.isValue("ОБЩЕСТВО", None) or tt1.isValue("ТЕРРИТОРИЯ", None) or tt1.isValue("ПМК", None)): 
                    tt1 = tt1.next0_
                else: 
                    break
            if ((isinstance(tt1, TextToken)) and tt1.chars.is_all_lower and ((tt1.length_char == 2 or tt1.length_char == 3))): 
                if (tt1.whitespaces_before_count < 2): 
                    if (AddressItemToken.checkHouseAfter(tt1, False, False)): 
                        return None
                    tt1 = tt1.next0_
        elif (t.length_char > 1 and t.chars.is_cyrillic_letter): 
            nt2 = t
            num2 = None
            if (t.chars.is_all_upper): 
                if (t.isValue("ФЗ", None) or t.isValue("ФКЗ", None)): 
                    return None
                ok = True
            elif (t.chars.is_all_lower and t.getMorphClassInDictionary().is_undefined and not t.isValue("ПСЕВДО", None)): 
                ok = True
            tt2 = t.next0_
            first_pass2740 = True
            while True:
                if first_pass2740: first_pass2740 = False
                else: tt2 = tt2.next0_
                if (not (tt2 is not None)): break
                if (tt2.whitespaces_before_count > 2): 
                    break
                ooo = AddressItemToken.M_ORG_ONTOLOGY.tryParse(tt2, TerminParseAttr.NO)
                if (ooo is not None): 
                    oooo = AddressItemToken.tryAttachOrg(tt2)
                    if (oooo is None): 
                        ok = True
                        tok = ooo
                        typ_ = tok.termin.canonic_text.lower()
                        typ2 = tok.termin.acronym
                        nam = MiscHelper.getTextValue(t, nt2, GetTextAttr.NO)
                        if (isinstance(num2, NumberToken)): 
                            num = str((Utils.asObjectOrNull(num2, NumberToken)).value)
                        t1 = nt2
                    break
                if (tt2.is_hiphen): 
                    continue
                if (tt2.isValue("ИМ", None)): 
                    if (tt2.next0_ is not None and tt2.next0_.isChar('.')): 
                        tt2 = tt2.next0_
                    continue
                if (isinstance(tt2, NumberToken)): 
                    num2 = tt2
                    continue
                nuuu = NumberHelper.tryParseAge(tt2)
                if (nuuu is not None): 
                    num = str((Utils.asObjectOrNull(nuuu, NumberToken)).value)
                    num2 = (nuuu)
                    tt2 = nuuu.end_token
                    continue
                if (not ((isinstance(tt2, TextToken))) or not tt2.chars.is_cyrillic_letter): 
                    break
                if (tt2.chars.is_all_lower): 
                    nnn = NounPhraseHelper.tryParse(tt2.previous, NounPhraseParseAttr.NO, 0)
                    if (nnn is not None and nnn.end_token == tt2): 
                        pass
                    elif (tt2.getMorphClassInDictionary().is_noun and tt2.morph.case_.is_genitive): 
                        pass
                    else: 
                        break
                nt2 = tt2
        elif (BracketHelper.isBracket(t, True)): 
            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                if (AddressItemToken.checkHouseAfter(br.end_token.next0_, False, False)): 
                    tt1 = t
                    ok = True
                else: 
                    txt = Utils.ifNotNull(MiscHelper.getTextValue(br.begin_token, br.end_token, GetTextAttr.NO), "")
                    if (("БИЗНЕС" in txt or "БІЗНЕС" in txt or "ПЛАЗА" in txt) or "PLAZA" in txt): 
                        tt1 = t
                        ok = True
        bracks = False
        is_very_doubt = False
        if (ok and BracketHelper.isBracket(tt1, False)): 
            br = BracketHelper.tryParse(tt1, BracketParseAttr.NO, 100)
            if (br is not None and (br.length_char < 100)): 
                res1 = AddressItemToken.tryAttachOrg(tt1.next0_)
                if (res1 is not None and res1.ref_token is not None): 
                    if (res1.end_token == br.end_token or res1.end_token == br.end_token.previous): 
                        res1.ref_token.begin_token = res1.begin_token = t
                        res1.ref_token.end_token = res1.end_token = br.end_token
                        res1.ref_token.referent.addSlot("TYPE", (t.getSourceText().upper() if tok is None else tok.termin.canonic_text.lower()), False, 0)
                        return res1
                typ_ = (((None if t == tt1 else MiscHelper.getTextValue(t, t, GetTextAttr.NO))) if tok is None else tok.termin.canonic_text.lower())
                if (tok is not None): 
                    typ2 = tok.termin.acronym
                tt = br.end_token.previous
                if (isinstance(tt, NumberToken)): 
                    num = str((Utils.asObjectOrNull(tt, NumberToken)).value)
                    tt = tt.previous
                    if (tt is not None and (((tt.is_hiphen or tt.isChar('_') or tt.isValue("N", None)) or tt.isValue("№", None)))): 
                        tt = tt.previous
                if (tt is not None): 
                    nam = MiscHelper.getTextValue(br.begin_token, tt, GetTextAttr.NO)
                t1 = br.end_token
                bracks = True
        if (ok and ((((typ_ is None and ((t.chars.is_all_upper and t.length_char == 3)))) or tok is not None))): 
            tt = tt1
            if (tt is not None and ((tt.is_hiphen or tt.isChar('_')))): 
                tt = tt.next0_
            adt = AddressItemToken.tryParse(tt, None, False, True, None)
            if (adt is not None and adt.typ == AddressItemToken.ItemType.NUMBER): 
                if (tt.previous.is_hiphen or tt.previous.isChar('_') or not ((isinstance(tt, NumberToken)))): 
                    pass
                else: 
                    is_very_doubt = True
                num = adt.value
                t1 = adt.end_token
                if (tok is not None): 
                    typ_ = tok.termin.canonic_text.lower()
                    typ2 = tok.termin.acronym
        if (((tok is not None and typ_ is None and (isinstance(tt1, TextToken))) and not tt1.chars.is_all_lower and tt1.chars.is_cyrillic_letter) and (tt1.whitespaces_before_count < 3)): 
            typ_ = tok.termin.canonic_text.lower()
            typ2 = tok.termin.acronym
            nam = MiscHelper.getTextValue(tt1, tt1, GetTextAttr.NO)
            t1 = tt1
        elif (((tok is not None and typ_ is None and tt1 is not None) and (isinstance(tt1.getReferent(), GeoReferent)) and (tt1.whitespaces_before_count < 3)) and (Utils.asObjectOrNull(tt1, ReferentToken)).begin_token == (Utils.asObjectOrNull(tt1, ReferentToken)).end_token): 
            typ_ = tok.termin.canonic_text.lower()
            typ2 = tok.termin.acronym
            nam = MiscHelper.getTextValue(tt1, tt1, GetTextAttr.NO)
            t1 = tt1
        if ((ok and typ_ is None and num is not None) and t.length_char > 2 and (t.length_char < 5)): 
            tt2 = t1.next0_
            if (tt2 is not None and tt2.isChar(',')): 
                tt2 = tt2.next0_
            if (tt2 is not None and (tt2.whitespaces_after_count < 2)): 
                adt = AddressItemToken.tryParse(tt2, None, False, True, None)
                if (adt is not None): 
                    if (((adt.typ == AddressItemToken.ItemType.BLOCK or adt.typ == AddressItemToken.ItemType.BOX or adt.typ == AddressItemToken.ItemType.BUILDING) or adt.typ == AddressItemToken.ItemType.CORPUS or adt.typ == AddressItemToken.ItemType.HOUSE) or adt.typ == AddressItemToken.ItemType.PLOT): 
                        typ_ = t.getSourceText()
        if (typ_ is None and nam is not None): 
            if ("БИЗНЕС" in nam or "ПЛАЗА" in nam or "PLAZA" in nam): 
                typ_ = "бизнес центр"
            elif ("БІЗНЕС" in nam): 
                typ_ = "бізнес центр"
        if (typ_ is not None): 
            org0_ = t.kit.createReferent("ORGANIZATION")
            if (org0_ is None): 
                org0_ = Referent("ORGANIZATION")
            org0_.addSlot("TYPE", typ_, False, 0)
            if (typ2 is not None): 
                org0_.addSlot("TYPE", typ2, False, 0)
            if (nam is not None): 
                if ((not bracks and t1.next0_ is not None and t1.next0_.chars.is_cyrillic_letter) and t1.whitespaces_after_count == 1): 
                    ok = False
                    if (tok is not None and t1.next0_ == tok.end_token): 
                        pass
                    elif (t1.next0_.next0_ is None or BracketHelper.canBeEndOfSequence(t1.next0_.next0_, False, None, False)): 
                        ok = True
                    elif (t1.next0_.next0_.isChar(',')): 
                        ok = True
                    elif ((isinstance(t1.next0_.next0_, NumberToken)) and ((t1.next0_.next0_.next0_ is None or BracketHelper.canBeEndOfSequence(t1.next0_.next0_.next0_, False, None, False)))): 
                        ok = True
                    elif (((t1.next0_.next0_.is_hiphen or t1.next0_.next0_.isValue("N", None) or t1.next0_.next0_.isValue("№", None))) and (isinstance(t1.next0_.next0_.next0_, NumberToken))): 
                        ok = True
                    if (ok): 
                        nam = "{0} {1}".format(nam, t1.next0_.getSourceText().upper())
                        t1 = t1.next0_
                elif ((((not bracks and t1.next0_ is not None and t1.next0_.next0_ is not None) and t1.next0_.is_hiphen and not t1.is_whitespace_after) and not t1.next0_.is_whitespace_after and (((isinstance(t1.next0_.next0_, TextToken)) or (isinstance(t1.next0_.next0_.getReferent(), GeoReferent))))) and t1.next0_.next0_.chars.is_cyrillic_letter): 
                    nam = "{0} {1}".format(nam, MiscHelper.getTextValue(t1.next0_.next0_, t1.next0_.next0_, GetTextAttr.NO))
                    t1 = t1.next0_.next0_
                if ((nam.startswith("ИМ.") or nam.startswith("ИМ ") or nam.startswith("ІМ.")) or nam.startswith("ІМ ")): 
                    org0_.addSlot("NAME", nam[3:].strip(), False, 0)
                    nam = "{0} {1}".format(("ІМЕНІ" if nam.startswith("ІМ") else "ИМЕНИ"), nam[3:].strip())
                if (nam.startswith("ИМЕНИ ") or nam.startswith("ІМЕНІ ")): 
                    org0_.addSlot("NAME", nam[6:].strip(), False, 0)
                org0_.addSlot("NAME", nam, False, 0)
            rt = ReferentToken._new115(org0_, t, t1, t.kit.getAnalyzerDataByAnalyzerName("ORGANIZATION"))
            empty_org = False
            if ((t1.next0_ is not None and t1.next0_.is_hiphen and t1.next0_.next0_ is not None) and t1.next0_.next0_.isValue("ГОРОДИЩЕ", None)): 
                rt.end_token = t1.next0_.next0_
            if (t1.next0_ is not None and t1.next0_.isValue("ПРИ", None)): 
                rtt = t1.kit.processReferent("ORGANIZATION", t1.next0_.next0_)
                if (rtt is not None): 
                    empty_org = True
                    t1 = rtt.end_token
                    rt.end_token = t1
            if (t1.next0_ is not None and t1.next0_.isValue("АПН", None)): 
                t1 = t1.next0_
                rt.end_token = t1
            if (t1.whitespaces_after_count < 2): 
                rtt1 = t1.kit.processReferent("ORGANIZATION", t1.next0_)
                if (rtt1 is not None): 
                    empty_org = True
                    t1 = rtt1.end_token
                    rt.end_token = t1
            if (empty_org and (t1.whitespaces_after_count < 2)): 
                terr = TerrItemToken.tryParse(t1.next0_, None, False, False)
                if (terr is not None and terr.onto_item is not None): 
                    t1 = terr.end_token
                    rt.end_token = t1
            if (num is not None): 
                org0_.addSlot("NUMBER", num, False, 0)
            elif (t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.isValue("№", None) or t1.next0_.isValue("N", None))) and (isinstance(t1.next0_.next0_, NumberToken))): 
                nai = AddressItemToken.tryParse(t1.next0_.next0_, None, False, True, None)
                if (nai is not None and nai.typ == AddressItemToken.ItemType.NUMBER): 
                    org0_.addSlot("NUMBER", nai.value, False, 0)
                    rt.end_token = nai.end_token
                    t1 = rt.end_token
                else: 
                    rt.end_token = t1.next0_.next0_
                    t1 = rt.end_token
                    org0_.addSlot("NUMBER", str((Utils.asObjectOrNull(t1, NumberToken)).value), False, 0)
            if (tok is not None and (t1.end_char < tok.end_char)): 
                rt.end_token = tok.end_token
                t1 = rt.end_token
                if (t1.next0_ is not None and (t1.whitespaces_after_count < 2) and t1.next0_.isValue("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                    rt.end_token = t1.next0_
                    t1 = rt.end_token
        if (rt is None): 
            rt = rt1
        elif (rt1 is not None and rt1.referent.type_name == "ORGANIZATION"): 
            if (is_very_doubt): 
                rt = rt1
            else: 
                rt.referent.mergeSlots(rt1.referent, True)
                if (rt1.end_char > rt.end_char): 
                    rt.end_token = rt1.end_token
        if (rt is None): 
            return None
        if (t.isValue("АО", None)): 
            return None
        if (rt.referent.findSlot("TYPE", "администрация", True) is not None or rt.referent.findSlot("TYPE", "адміністрація", True) is not None): 
            ge = Utils.asObjectOrNull(rt.referent.getSlotValue("GEO"), GeoReferent)
            if (ge is not None): 
                return AddressItemToken._new83((AddressItemToken.ItemType.REGION if ge.is_region else AddressItemToken.ItemType.CITY), t, rt.end_token, ge)
        res = AddressItemToken._new114(AddressItemToken.ItemType.STREET, t, rt.end_token, rt.referent, rt, typ_ is not None)
        return res
    
    def createGeoOrgTerr(self) -> 'ReferentToken':
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        geo = GeoReferent()
        t1 = self.end_token
        geo._addOrgReferent(self.referent)
        geo.addExtReferent(self.ref_token)
        if (geo.findSlot(GeoReferent.ATTR_TYPE, None, True) is None): 
            geo._addTypTer(self.kit.base_language)
        return ReferentToken(geo, self.begin_token, self.end_token)
    
    @staticmethod
    def checkHouseAfter(t : 'Token', leek : bool=False, pure_house : bool=False) -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return False
        cou = 0
        while t is not None and (cou < 4): 
            if (t.isCharOf(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        if (t.is_newline_before): 
            return False
        ait = AddressItemToken.tryParse(t, None, False, True, None)
        if (ait is not None): 
            if (pure_house): 
                return ait.typ == AddressItemToken.ItemType.HOUSE or ait.typ == AddressItemToken.ItemType.PLOT
            if ((ait.typ == AddressItemToken.ItemType.HOUSE or ait.typ == AddressItemToken.ItemType.FLOOR or ait.typ == AddressItemToken.ItemType.OFFICE) or ait.typ == AddressItemToken.ItemType.FLAT or ait.typ == AddressItemToken.ItemType.PLOT): 
                if (((isinstance(t, TextToken)) and t.chars.is_all_upper and t.next0_ is not None) and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))): 
                    return False
                if ((isinstance(t, TextToken)) and t.next0_ == ait.end_token and t.next0_.is_hiphen): 
                    return False
                return True
            if (leek): 
                if (ait.typ == AddressItemToken.ItemType.NUMBER): 
                    return True
            if (ait.typ == AddressItemToken.ItemType.NUMBER): 
                t1 = t.next0_
                while t1 is not None and t1.isCharOf(".,"):
                    t1 = t1.next0_
                ait = AddressItemToken.tryParse(t1, None, False, True, None)
                if (ait is not None and (((ait.typ == AddressItemToken.ItemType.BUILDING or ait.typ == AddressItemToken.ItemType.CORPUS or ait.typ == AddressItemToken.ItemType.FLAT) or ait.typ == AddressItemToken.ItemType.FLOOR or ait.typ == AddressItemToken.ItemType.OFFICE))): 
                    return True
        return False
    
    @staticmethod
    def checkKmAfter(t : 'Token') -> bool:
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        cou = 0
        while t is not None and (cou < 4): 
            if (t.isCharOf(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        km = AddressItemToken.tryParse(t, None, False, True, None)
        if (km is not None and km.typ == AddressItemToken.ItemType.KILOMETER): 
            return True
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0)
        if (npt is not None): 
            if (npt.end_token.isValue("КИЛОМЕТР", None) or npt.end_token.isValue("МЕТР", None)): 
                return True
        return False
    
    @staticmethod
    def checkKmBefore(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.isCharOf(",.")): 
                pass
            elif (t.isValue("КМ", None) or t.isValue("КИЛОМЕТР", None) or t.isValue("МЕТР", None)): 
                return True
            t = t.previous; cou += 1
        return False
    
    @staticmethod
    def correctChar(v : 'char') -> 'char':
        if (v == 'A' or v == 'А'): 
            return 'А'
        if (v == 'Б' or v == 'Г'): 
            return v
        if (v == 'B' or v == 'В'): 
            return 'В'
        if (v == 'C' or v == 'С'): 
            return 'С'
        if (v == 'D' or v == 'Д'): 
            return 'Д'
        if (v == 'E' or v == 'Е'): 
            return 'Е'
        if (v == 'H' or v == 'Н'): 
            return 'Н'
        if (v == 'K' or v == 'К'): 
            return 'К'
        return chr(0)
    
    @staticmethod
    def __correctCharToken(t : 'Token') -> str:
        from pullenti.ner.TextToken import TextToken
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        v = tt.term
        if (len(v) != 1): 
            return None
        corr = AddressItemToken.correctChar(v[0])
        if (corr != (chr(0))): 
            return "{0}".format(corr)
        if (t.chars.is_cyrillic_letter): 
            return v
        return None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (AddressItemToken.M_ONTOLOGY is not None): 
            return
        StreetItemToken.initialize()
        AddressItemToken.M_ONTOLOGY = TerminCollection()
        t = Termin._new118("ДОМ", AddressItemToken.ItemType.HOUSE)
        t.addAbridge("Д.")
        t.addVariant("КОТТЕДЖ", False)
        t.addAbridge("КОТ.")
        t.addVariant("ДАЧА", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new119("БУДИНОК", AddressItemToken.ItemType.HOUSE, MorphLang.UA)
        t.addAbridge("Б.")
        t.addVariant("КОТЕДЖ", False)
        t.addAbridge("БУД.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new120("ВЛАДЕНИЕ", AddressItemToken.ItemType.HOUSE, AddressHouseType.ESTATE)
        t.addAbridge("ВЛАД.")
        t.addAbridge("ВЛД.")
        t.addAbridge("ВЛ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new120("ДОМОВЛАДЕНИЕ", AddressItemToken.ItemType.HOUSE, AddressHouseType.HOUSEESTATE)
        t.addVariant("ДОМОВЛАДЕНИЕ", False)
        t.addAbridge("ДВЛД.")
        t.addAbridge("ДМВЛД.")
        t.addVariant("ДОМОВЛ", False)
        t.addVariant("ДОМОВА", False)
        t.addVariant("ДОМОВЛАД", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ПОДЪЕЗД ДОМА", AddressItemToken.ItemType.HOUSE)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ПОДВАЛ ДОМА", AddressItemToken.ItemType.HOUSE)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КРЫША ДОМА", AddressItemToken.ItemType.HOUSE)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ЭТАЖ", AddressItemToken.ItemType.FLOOR)
        t.addAbridge("ЭТ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ПОДЪЕЗД", AddressItemToken.ItemType.POTCH)
        t.addAbridge("ПОД.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КОРПУС", AddressItemToken.ItemType.CORPUS)
        t.addAbridge("КОРП.")
        t.addAbridge("КОР.")
        t.addAbridge("Д.КОРП.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("К", AddressItemToken.ItemType.CORPUSORFLAT)
        t.addAbridge("К.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("СТРОЕНИЕ", AddressItemToken.ItemType.BUILDING)
        t.addAbridge("СТРОЕН.")
        t.addAbridge("СТР.")
        t.addAbridge("СТ.")
        t.addAbridge("ПОМ.СТР.")
        t.addAbridge("Д.СТР.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new120("СООРУЖЕНИЕ", AddressItemToken.ItemType.BUILDING, AddressBuildingType.CONSTRUCTION)
        t.addAbridge("СООР.")
        t.addAbridge("СООРУЖ.")
        t.addAbridge("СООРУЖЕН.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new120("ЛИТЕРА", AddressItemToken.ItemType.BUILDING, AddressBuildingType.LITER)
        t.addAbridge("ЛИТ.")
        t.addVariant("ЛИТЕР", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("УЧАСТОК", AddressItemToken.ItemType.PLOT)
        t.addAbridge("УЧАСТ.")
        t.addAbridge("УЧ.")
        t.addAbridge("УЧ-К")
        t.addVariant("ЗЕМЕЛЬНЫЙ УЧАСТОК", False)
        t.addAbridge("ЗЕМ.УЧ.")
        t.addAbridge("ЗЕМ.УЧ-К")
        t.addAbridge("З/У")
        t.addAbridge("ПОЗ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КВАРТИРА", AddressItemToken.ItemType.FLAT)
        t.addAbridge("КВАРТ.")
        t.addAbridge("КВАР.")
        t.addAbridge("КВ.")
        t.addAbridge("КВ-РА")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ОФИС", AddressItemToken.ItemType.OFFICE)
        t.addAbridge("ОФ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new119("ОФІС", AddressItemToken.ItemType.OFFICE, MorphLang.UA)
        t.addAbridge("ОФ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("БИЗНЕС-ЦЕНТР", AddressItemToken.ItemType.BUSINESSCENTER)
        t.acronym = "БЦ"
        t.addVariant("БИЗНЕС ЦЕНТР", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("БЛОК", AddressItemToken.ItemType.BLOCK)
        t.addVariant("РЯД", False)
        t.addVariant("СЕКТОР", False)
        t.addAbridge("СЕК.")
        t.addVariant("МАССИВ", False)
        t.addVariant("ОЧЕРЕДЬ", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("БОКС", AddressItemToken.ItemType.BOX)
        t.addVariant("ГАРАЖ", False)
        t.addVariant("САРАЙ", False)
        t.addAbridge("ГАР.")
        t.addVariant("МАШИНОМЕСТО", False)
        t.addVariant("ПОМЕЩЕНИЕ", False)
        t.addAbridge("ПОМ.")
        t.addVariant("НЕЖИЛОЕ ПОМЕЩЕНИЕ", False)
        t.addAbridge("Н.П.")
        t.addAbridge("НП")
        t.addVariant("ПОДВАЛ", False)
        t.addVariant("ПОГРЕБ", False)
        t.addVariant("ПОДВАЛЬНОЕ ПОМЕЩЕНИЕ", False)
        t.addVariant("ПОДЪЕЗД", False)
        t.addAbridge("ГАРАЖ-БОКС")
        t.addVariant("ГАРАЖНЫЙ БОКС", False)
        t.addAbridge("ГБ.")
        t.addAbridge("Г.Б.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КОМНАТА", AddressItemToken.ItemType.OFFICE)
        t.addAbridge("КОМ.")
        t.addAbridge("КОМН.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КАБИНЕТ", AddressItemToken.ItemType.OFFICE)
        t.addAbridge("КАБ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("НОМЕР", AddressItemToken.ItemType.NUMBER)
        t.addAbridge("НОМ.")
        t.addAbridge("№")
        t.addAbridge("N")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new142("БЕЗ НОМЕРА", "Б/Н", AddressItemToken.ItemType.NONUMBER)
        t.addAbridge("Б.Н.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("АБОНЕНТСКИЙ ЯЩИК", AddressItemToken.ItemType.POSTOFFICEBOX)
        t.addAbridge("А.Я.")
        t.addVariant("ПОЧТОВЫЙ ЯЩИК", False)
        t.addAbridge("П.Я.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new144("ГОРОДСКАЯ СЛУЖЕБНАЯ ПОЧТА", AddressItemToken.ItemType.CSP, "ГСП")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("АДРЕС", AddressItemToken.ItemType.PREFIX)
        t.addVariant("ЮРИДИЧЕСКИЙ АДРЕС", False)
        t.addVariant("ФАКТИЧЕСКИЙ АДРЕС", False)
        t.addAbridge("ЮР.АДРЕС")
        t.addAbridge("ПОЧТ.АДРЕС")
        t.addAbridge("ФАКТ.АДРЕС")
        t.addAbridge("П.АДРЕС")
        t.addVariant("ЮРИДИЧЕСКИЙ/ФАКТИЧЕСКИЙ АДРЕС", False)
        t.addVariant("ПОЧТОВЫЙ АДРЕС", False)
        t.addVariant("АДРЕС ПРОЖИВАНИЯ", False)
        t.addVariant("МЕСТО НАХОЖДЕНИЯ", False)
        t.addVariant("МЕСТОНАХОЖДЕНИЕ", False)
        t.addVariant("МЕСТОПОЛОЖЕНИЕ", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("АДРЕСА", AddressItemToken.ItemType.PREFIX)
        t.addVariant("ЮРИДИЧНА АДРЕСА", False)
        t.addVariant("ФАКТИЧНА АДРЕСА", False)
        t.addVariant("ПОШТОВА АДРЕСА", False)
        t.addVariant("АДРЕСА ПРОЖИВАННЯ", False)
        t.addVariant("МІСЦЕ ПЕРЕБУВАННЯ", False)
        t.addVariant("ПРОПИСКА", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КИЛОМЕТР", AddressItemToken.ItemType.KILOMETER)
        t.addAbridge("КИЛОМ.")
        t.addAbridge("КМ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ПЕРЕСЕЧЕНИЕ", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("НА ПЕРЕСЕЧЕНИИ", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ПЕРЕКРЕСТОК", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("НА ПЕРЕКРЕСТКЕ", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("НА ТЕРРИТОРИИ", AddressDetailType.NEAR))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕРЕДИНА", AddressDetailType.NEAR))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ПРИМЫКАТЬ", AddressDetailType.NEAR))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ГРАНИЧИТЬ", AddressDetailType.NEAR))
        t = Termin._new118("ВБЛИЗИ", AddressDetailType.NEAR)
        t.addVariant("У", False)
        t.addAbridge("ВБЛ.")
        t.addVariant("ВОЗЛЕ", False)
        t.addVariant("ОКОЛО", False)
        t.addVariant("НЕДАЛЕКО ОТ", False)
        t.addVariant("РЯДОМ С", False)
        t.addVariant("ГРАНИЦА", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new118("РАЙОН", AddressDetailType.NEAR)
        t.addAbridge("Р-Н")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new142("В РАЙОНЕ", "РАЙОН", AddressDetailType.NEAR)
        t.addAbridge("В Р-НЕ")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ПРИМЕРНО", AddressDetailType.UNDEFINED))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ПОРЯДКА", AddressDetailType.UNDEFINED))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ПРИБЛИЗИТЕЛЬНО", AddressDetailType.UNDEFINED))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("НАПРАВЛЕНИЕ", AddressDetailType.UNDEFINED))
        t = Termin._new118("ОБЩЕЖИТИЕ", AddressDetailType.HOSTEL)
        t.addAbridge("ОБЩ.")
        t.addAbridge("ПОМ.ОБЩ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕВЕРНЕЕ", AddressDetailType.NORTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕВЕР", AddressDetailType.NORTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЮЖНЕЕ", AddressDetailType.SOUTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЮГ", AddressDetailType.SOUTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЗАПАДНЕЕ", AddressDetailType.WEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЗАПАД", AddressDetailType.WEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ВОСТОЧНЕЕ", AddressDetailType.EAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ВОСТОК", AddressDetailType.EAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕВЕРО-ЗАПАДНЕЕ", AddressDetailType.NORTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕВЕРО-ЗАПАД", AddressDetailType.NORTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕВЕРО-ВОСТОЧНЕЕ", AddressDetailType.NORTHEAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("СЕВЕРО-ВОСТОК", AddressDetailType.NORTHEAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЮГО-ЗАПАДНЕЕ", AddressDetailType.SOUTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЮГО-ЗАПАД", AddressDetailType.SOUTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЮГО-ВОСТОЧНЕЕ", AddressDetailType.SOUTHEAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new118("ЮГО-ВОСТОК", AddressDetailType.SOUTHEAST))
        t = Termin("ТАМ ЖЕ")
        t.addAbridge("ТАМЖЕ")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ORG_ONTOLOGY = TerminCollection()
        t = Termin._new113("САДОВОЕ ТОВАРИЩЕСТВО", "СТ")
        t.addVariant("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СТ"
        t.addAbridge("С/ТОВ")
        t.addAbridge("ПК СТ")
        t.addAbridge("САД.ТОВ.")
        t.addAbridge("САДОВ.ТОВ.")
        t.addAbridge("С/Т")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНОЕ ТОВАРИЩЕСТВО")
        t.addAbridge("Д/Т")
        t.addAbridge("ДАЧ/Т")
        t.acronym = "ДТ"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САДОВЫЙ КООПЕРАТИВ")
        t.addAbridge("С/К")
        t.acronym = "СК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ")
        t.addVariant("ПОТРЕБКООПЕРАТИВ", False)
        t.acronym = "ПК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САДОВОДЧЕСКОЕ ДАЧНОЕ ТОВАРИЩЕСТВО")
        t.addVariant("САДОВОЕ ДАЧНОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СДТ"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ")
        t.acronym = "ДНО"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО")
        t.acronym = "ДНП"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО")
        t.acronym = "ДНТ"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ")
        t.acronym = "ДПК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ")
        t.addVariant("ДАЧНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        t.acronym = "ДСК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ")
        t.acronym = "СПК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО")
        t.addVariant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СНТ"
        t.acronym_can_be_lower = True
        t.addAbridge("САДОВОЕ НЕКОМ-Е ТОВАРИЩЕСТВО")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "СНО", True)
        t.addVariant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "СНП", True)
        t.addVariant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "СНТ", True)
        t.addVariant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "НСТ", True)
        t.addVariant("НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНСТ", True)
        t.addVariant("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("САДОВОДЧЕСКАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", "СПК", True)
        t.addVariant("САДОВАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ДАЧНО СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ДСПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ЖИЛИЩНЫЙ СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ЖСПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ЖСК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ЖСКИЗ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "ОНО", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "ОНП", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНТ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ОГОРОДНИЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ОПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СТСН", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "ТСН", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ", "ТСЖ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("САДОВЫЕ ЗЕМЕЛЬНЫЕ УЧАСТКИ", "СЗУ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ТОВАРИЩЕСТВО ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ТИЗ", True))
        t = Termin._new181("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "КИЗ", True)
        t.addVariant("КИЗК", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new181("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СНТСН", True)
        t.addVariant("СНТ СН", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("СОВМЕСТНОЕ ПРЕДПРИЯТИЕ")
        t.acronym = "СП"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО")
        t.acronym = "НП"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("АВТОМОБИЛЬНЫЙ КООПЕРАТИВ")
        t.addAbridge("А/К")
        t.acronym = "АК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ГАРАЖНЫЙ КООПЕРАТИВ")
        t.addAbridge("Г/К")
        t.addAbridge("ГР.КОП.")
        t.addAbridge("ГАР.КОП.")
        t.acronym = "ГК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ГСК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", "ГЭК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ГАРАЖНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ПГСК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new181("ГАРАЖНЫЙ СТРОИТЕЛЬНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГСПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САНАТОРИЙ")
        t.addAbridge("САН.")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДОМ ОТДЫХА")
        t.addAbridge("Д/О")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("СОВХОЗ")
        t.addAbridge("С-ЗА")
        t.addAbridge("С/ЗА")
        t.addAbridge("С/З")
        t.addAbridge("СХ.")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ПИОНЕРСКИЙ ЛАГЕРЬ")
        t.addAbridge("П/Л")
        t.addAbridge("П.Л.")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("КУРОРТ")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ВЛАДЕЛЬЦЕВ")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("БИЗНЕС ЦЕНТР")
        t.acronym = "БЦ"
        t.addVariant("БІЗНЕС ЦЕНТР", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
    
    M_ONTOLOGY = None
    
    M_ORG_ONTOLOGY = None
    
    @staticmethod
    def _new83(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        return res
    
    @staticmethod
    def _new84(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        return res
    
    @staticmethod
    def _new86(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.is_doubt = _arg5
        return res
    
    @staticmethod
    def _new94(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'ReferentToken') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.ref_token = _arg4
        return res
    
    @staticmethod
    def _new95(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        return res
    
    @staticmethod
    def _new96(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressHouseType', _arg5 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.house_type = _arg4
        res.building_type = _arg5
        return res
    
    @staticmethod
    def _new97(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType', _arg6 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        res.building_type = _arg6
        return res
    
    @staticmethod
    def _new105(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'AddressHouseType', _arg7 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.morph = _arg5
        res.house_type = _arg6
        res.building_type = _arg7
        return res
    
    @staticmethod
    def _new111(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressDetailType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.detail_type = _arg4
        return res
    
    @staticmethod
    def _new114(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : 'ReferentToken', _arg6 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.ref_token = _arg5
        res.ref_token_is_gsk = _arg6
        return res