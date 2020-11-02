# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.Referent import Referent
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketHelper import BracketHelper

class AddressItemToken(MetaToken):
    
    class ItemType(IntEnum):
        PREFIX = 0
        STREET = 1
        HOUSE = 2
        BUILDING = 3
        CORPUS = 4
        POTCH = 5
        FLOOR = 6
        FLAT = 7
        CORPUSORFLAT = 8
        OFFICE = 9
        PLOT = 10
        BLOCK = 11
        BOX = 12
        CITY = 13
        REGION = 14
        COUNTRY = 15
        NUMBER = 16
        NONUMBER = 17
        KILOMETER = 18
        ZIP = 19
        POSTOFFICEBOX = 20
        CSP = 21
        DETAIL = 22
        BUSINESSCENTER = 23
        
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
        if (self.typ != AddressItemToken.ItemType.STREET): 
            return False
        if (not (isinstance(self.referent, StreetReferent))): 
            return False
        return self.referent.kind == StreetKind.ROAD
    
    @property
    def is_terr_or_rzd(self) -> bool:
        if (self.typ == AddressItemToken.ItemType.CITY and (isinstance(self.referent, GeoReferent))): 
            if (self.referent.is_territory): 
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
    def try_parse_list(t : 'Token', loc_streets : 'IntOntologyCollection', max_count : int=20) -> typing.List['AddressItemToken']:
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        if (isinstance(t, NumberToken)): 
            if (t.int_value is None): 
                return None
            v = t.int_value
            if ((v < 100000) or v >= 10000000): 
                if (t.typ == NumberSpellingType.DIGIT and not t.morph.class0_.is_adjective): 
                    if (t.next0_ is None or (isinstance(t.next0_, NumberToken))): 
                        if (t.previous is None or not t.previous.morph.class0_.is_preposition): 
                            return None
        it = AddressItemToken.try_parse(t, loc_streets, False, False, None)
        if (it is None): 
            return None
        if (it.typ == AddressItemToken.ItemType.NUMBER): 
            return None
        if (it.typ == AddressItemToken.ItemType.KILOMETER and (isinstance(it.begin_token.previous, NumberToken))): 
            it.begin_token = it.begin_token.previous
            it.value = str(it.begin_token.value)
            if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                it.begin_token = it.begin_token.previous
        res = list()
        res.append(it)
        pref = it.typ == AddressItemToken.ItemType.PREFIX
        t = it.end_token.next0_
        first_pass3485 = True
        while True:
            if first_pass3485: first_pass3485 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            last = res[len(res) - 1]
            if (len(res) > 1): 
                if (last.is_newline_before and res[len(res) - 2].typ != AddressItemToken.ItemType.PREFIX): 
                    i = 0
                    first_pass3486 = True
                    while True:
                        if first_pass3486: first_pass3486 = False
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
            if (t.is_char(',')): 
                continue
            if (BracketHelper.can_be_end_of_sequence(t, True, None, False) and last.typ == AddressItemToken.ItemType.STREET): 
                continue
            if (t.is_char('.')): 
                if (t.is_newline_after): 
                    break
                if (t.previous is not None and t.previous.is_char('.')): 
                    break
                continue
            if (t.is_hiphen or t.is_char('_')): 
                if (((it.typ == AddressItemToken.ItemType.NUMBER or it.typ == AddressItemToken.ItemType.STREET)) and (isinstance(t.next0_, NumberToken))): 
                    continue
            if (it.typ == AddressItemToken.ItemType.DETAIL and it.detail_type == AddressDetailType.CROSS): 
                str1 = AddressItemToken.try_parse(t, loc_streets, True, False, None)
                if (str1 is not None and str1.typ == AddressItemToken.ItemType.STREET): 
                    if (str1.end_token.next0_ is not None and ((str1.end_token.next0_.is_and or str1.end_token.next0_.is_hiphen))): 
                        str2 = AddressItemToken.try_parse(str1.end_token.next0_.next0_, loc_streets, True, False, None)
                        if (str2 is None or str2.typ != AddressItemToken.ItemType.STREET): 
                            str2 = StreetDefineHelper._try_parse_second_street(str1.begin_token, str1.end_token.next0_.next0_, loc_streets)
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
            it0 = AddressItemToken.try_parse(t, loc_streets, pre, False, it)
            if (it0 is None): 
                ok2 = True
                if (it.typ == AddressItemToken.ItemType.BUILDING and it.begin_token.is_value("СТ", None)): 
                    ok2 = False
                else: 
                    for rr in res: 
                        if (rr.typ == AddressItemToken.ItemType.BUILDING and rr.begin_token.is_value("СТ", None)): 
                            ok2 = False
                if (it.typ == AddressItemToken.ItemType.POSTOFFICEBOX): 
                    break
                if (ok2): 
                    it0 = AddressItemToken.try_attach_org(t)
                if (it0 is not None): 
                    res.append(it0)
                    it = it0
                    t = it.end_token
                    tt1 = t.next0_
                    while tt1 is not None: 
                        if (tt1.is_comma): 
                            pass
                        else: 
                            if (tt1.is_value("Л", None) and tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                                ait = AddressItemToken.try_parse(tt1.next0_.next0_, None, False, True, None)
                                if (ait is not None and ait.typ == AddressItemToken.ItemType.NUMBER): 
                                    st2 = StreetReferent()
                                    st2.add_slot(StreetReferent.ATTR_TYP, "линия", False, 0)
                                    st2.number = ait.value
                                    it = AddressItemToken._new64(AddressItemToken.ItemType.STREET, tt1, ait.end_token, st2)
                                    res.append(it)
                                    t = it.end_token
                            break
                        tt1 = tt1.next0_
                    continue
                if (t.morph.class0_.is_preposition): 
                    it0 = AddressItemToken.try_parse(t.next0_, loc_streets, False, False, it)
                    if (it0 is not None and it0.typ == AddressItemToken.ItemType.BUILDING and it0.begin_token.is_value("СТ", None)): 
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
                        ch = AddressItemToken.__correct_char_token(t)
                        if (ch == "К" or ch == "С"): 
                            it0 = AddressItemToken._new65((AddressItemToken.ItemType.CORPUS if ch == "К" else AddressItemToken.ItemType.BUILDING), t, t.next0_, str(t.next0_.value))
                            it = it0
                            res.append(it)
                            t = it.end_token
                            tt = t.next0_
                            if (((tt is not None and not tt.is_whitespace_before and tt.length_char == 1) and tt.chars.is_letter and not tt.is_whitespace_after) and (isinstance(tt.next0_, NumberToken))): 
                                ch = AddressItemToken.__correct_char_token(tt)
                                if (ch == "К" or ch == "С"): 
                                    it = AddressItemToken._new65((AddressItemToken.ItemType.CORPUS if ch == "К" else AddressItemToken.ItemType.BUILDING), tt, tt.next0_, str(tt.next0_.value))
                                    res.append(it)
                                    t = it.end_token
                            continue
                if (t.morph.class0_.is_preposition): 
                    if ((((t.is_value("У", None) or t.is_value("ВОЗЛЕ", None) or t.is_value("НАПРОТИВ", None)) or t.is_value("НА", None) or t.is_value("В", None)) or t.is_value("ВО", None) or t.is_value("ПО", None)) or t.is_value("ОКОЛО", None)): 
                        continue
                if (t.morph.class0_.is_noun): 
                    if ((t.is_value("ДВОР", None) or t.is_value("ПОДЪЕЗД", None) or t.is_value("КРЫША", None)) or t.is_value("ПОДВАЛ", None)): 
                        continue
                if (t.is_value("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                    continue
                if (t.is_char('(') and t.next0_ is not None): 
                    it0 = AddressItemToken.try_parse(t.next0_, loc_streets, pre, False, None)
                    if (it0 is not None and it0.end_token.next0_ is not None and it0.end_token.next0_.is_char(')')): 
                        it0.begin_token = t
                        it0.end_token = it0.end_token.next0_
                        it = it0
                        res.append(it)
                        t = it.end_token
                        continue
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 100)): 
                        if (t.next0_.is_value("БЫВШИЙ", None) or t.next0_.is_value("БЫВШ", None)): 
                            it = AddressItemToken(AddressItemToken.ItemType.DETAIL, t, br.end_token)
                            res.append(it)
                        t = br.end_token
                        continue
                check_kv = False
                if (t.is_value("КВ", None) or t.is_value("KB", None)): 
                    if (it.typ == AddressItemToken.ItemType.NUMBER and len(res) > 1 and res[len(res) - 2].typ == AddressItemToken.ItemType.STREET): 
                        check_kv = True
                    elif ((it.typ == AddressItemToken.ItemType.HOUSE or it.typ == AddressItemToken.ItemType.BUILDING or it.typ == AddressItemToken.ItemType.CORPUS) or it.typ == AddressItemToken.ItemType.CORPUSORFLAT): 
                        for jj in range(len(res) - 2, -1, -1):
                            if (res[jj].typ == AddressItemToken.ItemType.STREET or res[jj].typ == AddressItemToken.ItemType.CITY): 
                                check_kv = True
                    if (check_kv): 
                        tt2 = t.next0_
                        if (tt2 is not None and tt2.is_char('.')): 
                            tt2 = tt2.next0_
                        it22 = AddressItemToken.try_parse(tt2, loc_streets, False, True, None)
                        if (it22 is not None and it22.typ == AddressItemToken.ItemType.NUMBER): 
                            it22.begin_token = t
                            it22.typ = AddressItemToken.ItemType.FLAT
                            res.append(it22)
                            t = it22.end_token
                            continue
                if (res[len(res) - 1].typ == AddressItemToken.ItemType.CITY): 
                    if (((t.is_hiphen or t.is_char('_') or t.is_value("НЕТ", None))) and t.next0_ is not None and t.next0_.is_comma): 
                        att = AddressItemToken.__try_parse(t.next0_.next0_, None, False, True, None)
                        if (att is not None): 
                            if (att.typ == AddressItemToken.ItemType.HOUSE or att.typ == AddressItemToken.ItemType.BUILDING or att.typ == AddressItemToken.ItemType.CORPUS): 
                                it = AddressItemToken(AddressItemToken.ItemType.STREET, t, t)
                                res.append(it)
                                continue
                if (t.length_char == 2 and (isinstance(t, TextToken)) and t.chars.is_all_upper): 
                    term = t.term
                    if (not Utils.isNullOrEmpty(term) and term[0] == 'Р'): 
                        continue
                break
            if (t.whitespaces_before_count > 15): 
                if (it0.typ == AddressItemToken.ItemType.STREET and last.typ == AddressItemToken.ItemType.CITY): 
                    pass
                else: 
                    break
            if (it0.typ == AddressItemToken.ItemType.STREET and t.is_value("КВ", None)): 
                if (it is not None): 
                    if (it.typ == AddressItemToken.ItemType.HOUSE or it.typ == AddressItemToken.ItemType.BUILDING or it.typ == AddressItemToken.ItemType.CORPUS): 
                        it2 = AddressItemToken.try_parse(t, loc_streets, False, True, None)
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
                        ss = Utils.asObjectOrNull(s.value, str)
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
                    npt = NounPhraseHelper.try_parse(it.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None): 
                        del0_ = True
                if (del0_): 
                    del res[len(res) - 1]
                elif ((it.typ == AddressItemToken.ItemType.NUMBER and it0 is not None and it0.typ == AddressItemToken.ItemType.STREET) and it0.ref_token is None): 
                    if (it.begin_token.previous.is_char(',') or it.is_newline_after): 
                        it.typ = AddressItemToken.ItemType.HOUSE
        if (len(res) == 0): 
            return None
        for r in res: 
            if (r.typ == AddressItemToken.ItemType.CITY or r.typ == AddressItemToken.ItemType.REGION): 
                ty = AddressItemToken.__find_addr_typ(r.begin_token, r.end_char, 0)
                if (ty is not None): 
                    r.detail_type = ty.detail_type
                    if (ty.detail_meters > 0): 
                        r.detail_meters = ty.detail_meters
        i = 0
        while i < (len(res) - 1): 
            if (res[i].is_terr_or_rzd and res[i + 1].typ == AddressItemToken.ItemType.KILOMETER and (((i + 1) >= len(res) or not res[i + 1].is_terr_or_rzd))): 
                str0_ = StreetReferent()
                str0_.add_slot(StreetReferent.ATTR_TYP, "километр", True, 0)
                str0_.add_slot(StreetReferent.ATTR_NAME, res[i].referent.get_string_value(GeoReferent.ATTR_NAME), False, 0)
                str0_.add_slot(StreetReferent.ATTR_GEO, res[i].referent, False, 0)
                str0_.number = res[i + 1].value
                t11 = res[i + 1].end_token
                remove2 = False
                if ((res[i].value is None and ((i + 2) < len(res)) and res[i + 2].typ == AddressItemToken.ItemType.NUMBER) and res[i + 2].value is not None): 
                    str0_.number = res[i + 2].value + "км"
                    t11 = res[i + 2].end_token
                    remove2 = True
                ai = AddressItemToken._new67(AddressItemToken.ItemType.STREET, res[i].begin_token, t11, str0_, False)
                res[i] = ai
                del res[i + 1]
                if (remove2): 
                    del res[i + 1]
            elif (res[i + 1].is_terr_or_rzd and res[i].typ == AddressItemToken.ItemType.KILOMETER): 
                str0_ = StreetReferent()
                str0_.add_slot(StreetReferent.ATTR_TYP, "километр", True, 0)
                str0_.add_slot(StreetReferent.ATTR_NAME, res[i + 1].referent.get_string_value(GeoReferent.ATTR_NAME), False, 0)
                str0_.add_slot(StreetReferent.ATTR_GEO, res[i + 1].referent, False, 0)
                str0_.number = res[i].value
                t11 = res[i + 1].end_token
                remove2 = False
                if ((res[i].value is None and ((i + 2) < len(res)) and res[i + 2].typ == AddressItemToken.ItemType.NUMBER) and res[i + 2].value is not None): 
                    str0_.number = res[i + 2].value + "км"
                    t11 = res[i + 2].end_token
                    remove2 = True
                ai = AddressItemToken._new67(AddressItemToken.ItemType.STREET, res[i].begin_token, t11, str0_, False)
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
            if ((res[i].typ == AddressItemToken.ItemType.STREET and res[i + 1].typ == AddressItemToken.ItemType.KILOMETER and (isinstance(res[i].referent, StreetReferent))) and res[i].referent.number is None): 
                res[i].referent.number = res[i + 1].value + "км"
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == AddressItemToken.ItemType.STREET and res[i].typ == AddressItemToken.ItemType.KILOMETER and (isinstance(res[i + 1].referent, StreetReferent))) and res[i + 1].referent.number is None): 
                res[i + 1].referent.number = res[i].value + "км"
                res[i + 1].begin_token = res[i].begin_token
                del res[i]
                break
            i += 1
        return res
    
    @staticmethod
    def __find_addr_typ(t : 'Token', max_char : int, lev : int=0) -> 'AddressItemToken':
        if (t is None or t.end_char > max_char): 
            return None
        if (lev > 5): 
            return None
        if (isinstance(t, ReferentToken)): 
            geo = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
            if (geo is not None): 
                for s in geo.slots: 
                    if (s.type_name == GeoReferent.ATTR_TYPE): 
                        ty = s.value
                        if ("район" in ty): 
                            return None
            tt = t.begin_token
            while tt is not None: 
                if (tt.end_char > max_char): 
                    break
                ty = AddressItemToken.__find_addr_typ(tt, max_char, lev + 1)
                if (ty is not None): 
                    return ty
                tt = tt.next0_
        else: 
            ai = AddressItemToken.try_attach_detail(t)
            if (ai is not None): 
                if (ai.detail_type != AddressDetailType.UNDEFINED or ai.detail_meters > 0): 
                    return ai
        return None
    
    @staticmethod
    def try_parse(t : 'Token', loc_streets : 'IntOntologyCollection', prefix_before : bool, ignore_street : bool=False, prev : 'AddressItemToken'=None) -> 'AddressItemToken':
        if (t is None): 
            return None
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = AddressItemToken.__try_parse(t, loc_streets, prefix_before, ignore_street, prev)
        t.kit.recurse_level -= 1
        if (((res is not None and not res.is_whitespace_after and res.end_token.next0_ is not None) and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and res.value is not None): 
            if (res.typ == AddressItemToken.ItemType.HOUSE or res.typ == AddressItemToken.ItemType.BUILDING or res.typ == AddressItemToken.ItemType.CORPUS): 
                tt = res.end_token.next0_.next0_
                if (isinstance(tt, NumberToken)): 
                    res.value = "{0}-{1}".format(res.value, tt.value)
                    res.end_token = tt
                    if ((not tt.is_whitespace_after and (isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1) and tt.next0_.chars.is_all_upper): 
                        tt = tt.next0_
                        res.end_token = tt
                        res.value += tt.term
                    if ((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_char_of("\\/")) and (isinstance(tt.next0_.next0_, NumberToken))): 
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        res.value = "{0}/{1}".format(res.value, tt.value)
                    if ((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_hiphen) and (isinstance(tt.next0_.next0_, NumberToken))): 
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        res.value = "{0}-{1}".format(res.value, tt.value)
                        if ((not tt.is_whitespace_after and (isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1) and tt.next0_.chars.is_all_upper): 
                            tt = tt.next0_
                            res.end_token = tt
                            res.value += tt.term
                elif ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_all_upper): 
                    res.value = "{0}-{1}".format(res.value, tt.term)
                    res.end_token = tt
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', loc_streets : 'IntOntologyCollection', prefix_before : bool, ignore_street : bool, prev : 'AddressItemToken') -> 'AddressItemToken':
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
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
                return AddressItemToken._new64(ty, t, t, rt.referent)
        if (not ignore_street and t is not None and prev is not None): 
            if (t.is_value("КВ", None) or t.is_value("КВАРТ", None)): 
                if ((((prev.typ == AddressItemToken.ItemType.HOUSE or prev.typ == AddressItemToken.ItemType.NUMBER or prev.typ == AddressItemToken.ItemType.BUILDING) or prev.typ == AddressItemToken.ItemType.FLOOR or prev.typ == AddressItemToken.ItemType.POTCH) or prev.typ == AddressItemToken.ItemType.CORPUS or prev.typ == AddressItemToken.ItemType.CORPUSORFLAT) or prev.typ == AddressItemToken.ItemType.DETAIL): 
                    ignore_street = True
        if (not ignore_street): 
            sli = StreetItemToken.try_parse_list(t, loc_streets, 10)
            if (sli is not None): 
                rt = StreetDefineHelper._try_parse_street(sli, prefix_before, False)
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
                        first_pass3487 = True
                        while True:
                            if first_pass3487: first_pass3487 = False
                            else: ttt = ttt.previous
                            if (not (ttt is not None)): break
                            if (ttt.morph.class0_.is_preposition or ttt.is_comma): 
                                continue
                            if (isinstance(ttt.get_referent(), GeoReferent)): 
                                crlf = False
                            break
                        if (sli[0].typ == StreetItemType.NOUN and "ДОРОГА" in sli[0].termin.canonic_text): 
                            crlf = False
                    if (crlf): 
                        aat = AddressItemToken.try_parse(rt.end_token.next0_, None, False, True, None)
                        if (aat is None): 
                            return None
                        if (aat.typ != AddressItemToken.ItemType.HOUSE): 
                            return None
                    return rt
                if (len(sli) == 1 and sli[0].typ == StreetItemType.NOUN): 
                    tt = sli[0].end_token.next0_
                    if (tt is not None and ((tt.is_hiphen or tt.is_char('_') or tt.is_value("НЕТ", None)))): 
                        ttt = tt.next0_
                        if (ttt is not None and ttt.is_comma): 
                            ttt = ttt.next0_
                        att = AddressItemToken.try_parse(ttt, None, False, True, None)
                        if (att is not None): 
                            if (att.typ == AddressItemToken.ItemType.HOUSE or att.typ == AddressItemToken.ItemType.CORPUS or att.typ == AddressItemToken.ItemType.BUILDING): 
                                return AddressItemToken(AddressItemToken.ItemType.STREET, t, tt)
        if (isinstance(t, ReferentToken)): 
            return None
        if (isinstance(t, NumberToken)): 
            n = Utils.asObjectOrNull(t, NumberToken)
            if (((n.length_char == 6 or n.length_char == 5)) and n.typ == NumberSpellingType.DIGIT and not n.morph.class0_.is_adjective): 
                return AddressItemToken._new65(AddressItemToken.ItemType.ZIP, t, t, str(n.value))
            ok = False
            if ((t.previous is not None and t.previous.morph.class0_.is_preposition and t.next0_ is not None) and t.next0_.chars.is_letter and t.next0_.chars.is_all_lower): 
                ok = True
            elif (t.morph.class0_.is_adjective and not t.morph.class0_.is_noun): 
                ok = True
            tok0 = AddressItemToken.M_ONTOLOGY.try_parse(t.next0_, TerminParseAttr.NO)
            if (tok0 is not None and (isinstance(tok0.termin.tag, AddressItemToken.ItemType))): 
                if (tok0.end_token.next0_ is None or tok0.end_token.next0_.is_comma or tok0.end_token.is_newline_after): 
                    ok = True
                typ0 = Utils.valToEnum(tok0.termin.tag, AddressItemToken.ItemType)
                if (typ0 == AddressItemToken.ItemType.FLAT): 
                    if ((isinstance(t.next0_, TextToken)) and t.next0_.is_value("КВ", None)): 
                        if (t.next0_.get_source_text() == "кВ"): 
                            return None
                    if ((isinstance(tok0.end_token.next0_, NumberToken)) and (tok0.end_token.whitespaces_after_count < 3)): 
                        if (prev is not None and ((prev.typ == AddressItemToken.ItemType.STREET or prev.typ == AddressItemToken.ItemType.CITY))): 
                            return AddressItemToken._new65(AddressItemToken.ItemType.NUMBER, t, t, str(n.value))
                if ((typ0 == AddressItemToken.ItemType.KILOMETER or typ0 == AddressItemToken.ItemType.FLOOR or typ0 == AddressItemToken.ItemType.BLOCK) or typ0 == AddressItemToken.ItemType.POTCH or typ0 == AddressItemToken.ItemType.FLAT): 
                    return AddressItemToken._new65(typ0, t, tok0.end_token, str(n.value))
        prepos = False
        tok = None
        if (t.morph.class0_.is_preposition): 
            tok = AddressItemToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
            if ((tok) is None): 
                if (t.begin_char < t.end_char): 
                    return None
                if (not t.is_char_of("КСкс")): 
                    t = t.next0_
                prepos = True
        if (tok is None): 
            tok = AddressItemToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
        t1 = t
        typ_ = AddressItemToken.ItemType.NUMBER
        house_typ = AddressHouseType.UNDEFINED
        build_typ = AddressBuildingType.UNDEFINED
        if (tok is not None): 
            if (t.is_value("УЖЕ", None)): 
                return None
            if (tok.termin.canonic_text == "ТАМ ЖЕ"): 
                cou = 0
                tt = t.previous
                first_pass3488 = True
                while True:
                    if first_pass3488: first_pass3488 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (cou > 1000): 
                        break
                    r = tt.get_referent()
                    if (r is None): 
                        continue
                    if (isinstance(r, AddressReferent)): 
                        g = Utils.asObjectOrNull(r.get_slot_value(AddressReferent.ATTR_GEO), GeoReferent)
                        if (g is not None): 
                            return AddressItemToken._new64(AddressItemToken.ItemType.CITY, t, tok.end_token, g)
                        break
                    elif (isinstance(r, GeoReferent)): 
                        g = Utils.asObjectOrNull(r, GeoReferent)
                        if (not g.is_state): 
                            return AddressItemToken._new64(AddressItemToken.ItemType.CITY, t, tok.end_token, g)
                return None
            if (isinstance(tok.termin.tag, AddressDetailType)): 
                return AddressItemToken.try_attach_detail(t)
            t1 = tok.end_token.next0_
            if (isinstance(tok.termin.tag, AddressItemToken.ItemType)): 
                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                if (isinstance(tok.termin.tag2, AddressBuildingType)): 
                    build_typ = (Utils.valToEnum(tok.termin.tag2, AddressBuildingType))
                typ_ = (Utils.valToEnum(tok.termin.tag, AddressItemToken.ItemType))
                if (typ_ == AddressItemToken.ItemType.PREFIX): 
                    first_pass3489 = True
                    while True:
                        if first_pass3489: first_pass3489 = False
                        else: t1 = t1.next0_
                        if (not (t1 is not None)): break
                        if (((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and t1.whitespaces_after_count == 1): 
                            continue
                        if (t1.is_char(':')): 
                            t1 = t1.next0_
                            break
                        if (t1.is_char('(')): 
                            br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                t1 = br.end_token
                                continue
                        if (isinstance(t1, TextToken)): 
                            if (t1.chars.is_all_lower or (t1.whitespaces_before_count < 3)): 
                                npt = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.NO, 0, None)
                                if (npt is not None): 
                                    t1 = npt.end_token
                                    continue
                        if (t1.is_value("УКАЗАННЫЙ", None) or t1.is_value("ЕГРИП", None) or t1.is_value("ФАКТИЧЕСКИЙ", None)): 
                            continue
                        if (t1.is_comma): 
                            if (t1.next0_ is not None and t1.next0_.is_value("УКАЗАННЫЙ", None)): 
                                continue
                        break
                    if (t1 is not None): 
                        t0 = t
                        if (((t0.previous is not None and not t0.is_newline_before and t0.previous.is_char(')')) and (isinstance(t0.previous.previous, TextToken)) and t0.previous.previous.previous is not None) and t0.previous.previous.previous.is_char('(')): 
                            t = t0.previous.previous.previous.previous
                            if (t is not None and t.get_morph_class_in_dictionary().is_adjective and not t.is_newline_after): 
                                t0 = t
                        res = AddressItemToken(AddressItemToken.ItemType.PREFIX, t0, t1.previous)
                        tt = t0.previous
                        first_pass3490 = True
                        while True:
                            if first_pass3490: first_pass3490 = False
                            else: tt = tt.previous
                            if (not (tt is not None)): break
                            if (tt.newlines_after_count > 3): 
                                break
                            if (tt.is_comma_and or tt.is_char_of("().")): 
                                continue
                            if (not (isinstance(tt, TextToken))): 
                                break
                            if (((tt.is_value("ПОЧТОВЫЙ", None) or tt.is_value("ЮРИДИЧЕСКИЙ", None) or tt.is_value("ЮР", None)) or tt.is_value("ФАКТИЧЕСКИЙ", None) or tt.is_value("ФАКТ", None)) or tt.is_value("ПОЧТ", None) or tt.is_value("АДРЕС", None)): 
                                res.begin_token = tt
                            else: 
                                break
                        return res
                    else: 
                        return None
                elif (typ_ == AddressItemToken.ItemType.BUSINESSCENTER): 
                    rt = t.kit.process_referent("ORGANIZATION", t)
                    if (rt is not None): 
                        return AddressItemToken._new75(typ_, t, rt.end_token, rt)
                elif ((typ_ == AddressItemToken.ItemType.CORPUSORFLAT and not tok.is_whitespace_before and not tok.is_whitespace_after) and tok.begin_token == tok.end_token and tok.begin_token.is_value("К", None)): 
                    typ_ = AddressItemToken.ItemType.CORPUS
                if (typ_ == AddressItemToken.ItemType.DETAIL and t.is_value("У", None)): 
                    if (not MiscLocationHelper.check_geo_object_before(t)): 
                        return None
                if (typ_ == AddressItemToken.ItemType.FLAT and t.is_value("КВ", None)): 
                    if (t.get_source_text() == "кВ"): 
                        return None
                if (typ_ == AddressItemToken.ItemType.KILOMETER or typ_ == AddressItemToken.ItemType.FLOOR or typ_ == AddressItemToken.ItemType.POTCH): 
                    return AddressItemToken(typ_, t, tok.end_token)
                if ((typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.BUILDING or typ_ == AddressItemToken.ItemType.CORPUS) or typ_ == AddressItemToken.ItemType.PLOT): 
                    if (t1 is not None and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and (t1.whitespaces_after_count < 2)): 
                        tok2 = AddressItemToken.M_ONTOLOGY.try_parse(t1.next0_, TerminParseAttr.NO)
                        if (tok2 is not None and (isinstance(tok2.termin.tag, AddressItemToken.ItemType))): 
                            typ2 = Utils.valToEnum(tok2.termin.tag, AddressItemToken.ItemType)
                            if (typ2 != typ_ and ((typ2 == AddressItemToken.ItemType.PLOT or ((typ2 == AddressItemToken.ItemType.HOUSE and typ_ == AddressItemToken.ItemType.PLOT))))): 
                                typ_ = typ2
                                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                                t1 = tok2.end_token.next0_
                                if (t1 is None): 
                                    return AddressItemToken._new76(typ_, t, tok2.end_token, "0", house_typ)
                if (typ_ != AddressItemToken.ItemType.NUMBER): 
                    if (t1 is None and t.length_char > 1): 
                        return AddressItemToken._new77(typ_, t, tok.end_token, house_typ, build_typ)
                    if ((isinstance(t1, NumberToken)) and t1.value == "0"): 
                        return AddressItemToken._new78(typ_, t, t1, "0", house_typ, build_typ)
        if (t1 is not None and t1.is_char('.') and t1.next0_ is not None): 
            if (not t1.is_whitespace_after): 
                t1 = t1.next0_
            elif ((isinstance(t1.next0_, NumberToken)) and t1.next0_.typ == NumberSpellingType.DIGIT and (t1.whitespaces_after_count < 2)): 
                t1 = t1.next0_
        if ((t1 is not None and not t1.is_whitespace_after and ((t1.is_hiphen or t1.is_char('_')))) and (isinstance(t1.next0_, NumberToken))): 
            t1 = t1.next0_
        tok = AddressItemToken.M_ONTOLOGY.try_parse(t1, TerminParseAttr.NO)
        if (tok is not None and (isinstance(tok.termin.tag, AddressItemToken.ItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemToken.ItemType)) == AddressItemToken.ItemType.NUMBER): 
            t1 = tok.end_token.next0_
        elif (tok is not None and (isinstance(tok.termin.tag, AddressItemToken.ItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemToken.ItemType)) == AddressItemToken.ItemType.NONUMBER): 
            re0 = AddressItemToken._new78(typ_, t, tok.end_token, "0", house_typ, build_typ)
            if (not re0.is_whitespace_after and (isinstance(re0.end_token.next0_, NumberToken))): 
                re0.end_token = re0.end_token.next0_
                re0.value = str(re0.end_token.value)
            return re0
        elif (t1 is not None): 
            if (typ_ == AddressItemToken.ItemType.FLAT): 
                tok2 = AddressItemToken.M_ONTOLOGY.try_parse(t1, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, AddressItemToken.ItemType)) == AddressItemToken.ItemType.FLAT): 
                    t1 = tok2.end_token.next0_
            if (t1.is_value("СТРОИТЕЛЬНЫЙ", None) and t1.next0_ is not None): 
                t1 = t1.next0_
            ttt = MiscHelper.check_number_prefix(t1)
            if (ttt is not None): 
                t1 = ttt
                if (t1.is_hiphen or t1.is_char('_')): 
                    t1 = t1.next0_
        if (t1 is None): 
            return None
        num = io.StringIO()
        nt = Utils.asObjectOrNull(t1, NumberToken)
        if (nt is not None): 
            if (nt.int_value is None or nt.int_value == 0): 
                return None
            print(nt.value, end="", file=num)
            if (nt.typ == NumberSpellingType.DIGIT or nt.typ == NumberSpellingType.WORDS): 
                if (((isinstance(nt.end_token, TextToken)) and nt.end_token.term == "Е" and nt.end_token.previous == nt.begin_token) and not nt.end_token.is_whitespace_before): 
                    print("Е", end="", file=num)
                drob = False
                hiph = False
                lit = False
                et = nt.next0_
                if (et is not None and ((et.is_char_of("\\/") or et.is_value("ДРОБЬ", None)))): 
                    drob = True
                    et = et.next0_
                    if (et is not None and et.is_char_of("\\/")): 
                        et = et.next0_
                    t1 = et
                elif (et is not None and ((et.is_hiphen or et.is_char('_')))): 
                    hiph = True
                    et = et.next0_
                elif ((et is not None and et.is_char('.') and (isinstance(et.next0_, NumberToken))) and not et.is_whitespace_after): 
                    return None
                if (isinstance(et, NumberToken)): 
                    if (drob): 
                        print("/{0}".format(et.value), end="", file=num, flush=True)
                        drob = False
                        t1 = et
                        et = et.next0_
                        if (et is not None and et.is_char_of("\\/") and (isinstance(et.next0_, NumberToken))): 
                            t1 = et.next0_
                            print("/{0}".format(t1.value), end="", file=num, flush=True)
                            et = t1.next0_
                    elif ((hiph and not t1.is_whitespace_after and (isinstance(et, NumberToken))) and not et.is_whitespace_before): 
                        numm = AddressItemToken.try_parse(et, None, False, True, None)
                        if (numm is not None and numm.typ == AddressItemToken.ItemType.NUMBER): 
                            merge = False
                            if (typ_ == AddressItemToken.ItemType.FLAT or typ_ == AddressItemToken.ItemType.PLOT): 
                                merge = True
                            elif (typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.BUILDING or typ_ == AddressItemToken.ItemType.CORPUS): 
                                ttt = numm.end_token.next0_
                                if (ttt is not None and ttt.is_comma): 
                                    ttt = ttt.next0_
                                numm2 = AddressItemToken.try_parse(ttt, None, False, True, None)
                                if (numm2 is not None): 
                                    if ((numm2.typ == AddressItemToken.ItemType.FLAT or numm2.typ == AddressItemToken.ItemType.BUILDING or ((numm2.typ == AddressItemToken.ItemType.CORPUSORFLAT and numm2.value is not None))) or numm2.typ == AddressItemToken.ItemType.CORPUS): 
                                        merge = True
                            if (merge): 
                                print("/{0}".format(numm.value), end="", file=num, flush=True)
                                t1 = numm.end_token
                                et = t1.next0_
                elif (et is not None and ((et.is_hiphen or et.is_char('_') or et.is_value("НЕТ", None))) and drob): 
                    t1 = et
                ett = et
                if ((ett is not None and ett.is_char_of(",.") and (ett.whitespaces_after_count < 2)) and (isinstance(ett.next0_, TextToken)) and BracketHelper.is_bracket(ett.next0_, False)): 
                    ett = ett.next0_
                if (((BracketHelper.is_bracket(ett, False) and (isinstance(ett.next0_, TextToken)) and ett.next0_.length_char == 1) and ett.next0_.is_letters and BracketHelper.is_bracket(ett.next0_.next0_, False)) and not ett.is_whitespace_after and not ett.next0_.is_whitespace_after): 
                    ch = AddressItemToken.__correct_char_token(ett.next0_)
                    if (ch is None): 
                        return None
                    print(ch, end="", file=num)
                    t1 = ett.next0_.next0_
                elif (BracketHelper.can_be_start_of_sequence(ett, True, False) and (ett.whitespaces_before_count < 2)): 
                    br = BracketHelper.try_parse(ett, BracketParseAttr.NO, 100)
                    if (br is not None and (isinstance(br.begin_token.next0_, TextToken)) and br.begin_token.next0_.next0_ == br.end_token): 
                        s = AddressItemToken.__correct_char_token(br.begin_token.next0_)
                        if (s is not None): 
                            print(s, end="", file=num)
                            t1 = br.end_token
                elif ((isinstance(et, TextToken)) and et.length_char == 1): 
                    s = AddressItemToken.__correct_char_token(et)
                    if (s is not None): 
                        if (((s == "К" or s == "С")) and (isinstance(et.next0_, NumberToken)) and not et.is_whitespace_after): 
                            pass
                        elif ((s == "Б" and et.next0_ is not None and et.next0_.is_char_of("/\\")) and (isinstance(et.next0_.next0_, TextToken)) and et.next0_.next0_.is_value("Н", None)): 
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
                            elif (et.is_whitespace_before and et.chars.is_all_lower and et.is_value("В", "У")): 
                                pass
                            else: 
                                ait_next = AddressItemToken.try_parse(et.next0_, None, False, True, None)
                                if (ait_next is not None): 
                                    if ((ait_next.typ == AddressItemToken.ItemType.CORPUS or ait_next.typ == AddressItemToken.ItemType.FLAT or ait_next.typ == AddressItemToken.ItemType.BUILDING) or ait_next.typ == AddressItemToken.ItemType.OFFICE): 
                                        ok = True
                            if (ok): 
                                print(s, end="", file=num)
                                t1 = et
                                if (et.next0_ is not None and et.next0_.is_char_of("\\/") and et.next0_.next0_ is not None): 
                                    if (isinstance(et.next0_.next0_, NumberToken)): 
                                        print("/{0}".format(et.next0_.next0_.value), end="", file=num, flush=True)
                                        et = et.next0_.next0_
                                        t1 = et
                                    elif (et.next0_.next0_.is_hiphen or et.next0_.next0_.is_char('_') or et.next0_.next0_.is_value("НЕТ", None)): 
                                        et = et.next0_.next0_
                                        t1 = et
                elif ((isinstance(et, TextToken)) and not et.is_whitespace_before): 
                    val = et.term
                    if (val == "КМ" and typ_ == AddressItemToken.ItemType.HOUSE): 
                        t1 = et
                        print("КМ", end="", file=num)
                    elif (val == "БН"): 
                        t1 = et
                    elif (((len(val) == 2 and val[1] == 'Б' and et.next0_ is not None) and et.next0_.is_char_of("\\/") and et.next0_.next0_ is not None) and et.next0_.next0_.is_value("Н", None)): 
                        print(val[0], end="", file=num)
                        et = et.next0_.next0_
                        t1 = et
        else: 
            re11 = AddressItemToken.__try_attachvch(t1, typ_)
            if ((re11) is not None): 
                re11.begin_token = t
                re11.house_type = house_typ
                re11.building_type = build_typ
                return re11
            elif (((isinstance(t1, TextToken)) and t1.length_char == 2 and t1.is_letters) and not t1.is_whitespace_before and (isinstance(t1.previous, NumberToken))): 
                src = t1.get_source_text()
                if ((src is not None and len(src) == 2 and ((src[0] == 'к' or src[0] == 'k'))) and str.isupper(src[1])): 
                    ch = AddressItemToken.correct_char(src[1])
                    if (ch != (chr(0))): 
                        return AddressItemToken._new65(AddressItemToken.ItemType.CORPUS, t1, t1, "{0}".format(ch))
            elif ((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.is_letters): 
                ch = AddressItemToken.__correct_char_token(t1)
                if (ch is not None): 
                    if (typ_ == AddressItemToken.ItemType.NUMBER): 
                        return None
                    if (ch == "К" or ch == "С"): 
                        if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                            return None
                    if (ch == "Д" and typ_ == AddressItemToken.ItemType.PLOT): 
                        rrr = AddressItemToken.__try_parse(t1, None, False, True, None)
                        if (rrr is not None): 
                            rrr.typ = AddressItemToken.ItemType.PLOT
                            rrr.begin_token = t
                            return rrr
                    if (t1.chars.is_all_lower and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction))): 
                        if ((t1.whitespaces_after_count < 2) and t1.next0_.chars.is_letter): 
                            return None
                    if (t.chars.is_all_upper and t.length_char == 1 and t.next0_.is_char('.')): 
                        return None
                    print(ch, end="", file=num)
                    if ((t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_char('_'))) and not t1.is_whitespace_after) and (isinstance(t1.next0_.next0_, NumberToken)) and not t1.next0_.is_whitespace_after): 
                        print(t1.next0_.next0_.value, end="", file=num)
                        t1 = t1.next0_.next0_
                    elif ((isinstance(t1.next0_, NumberToken)) and not t1.is_whitespace_after and t1.chars.is_all_upper): 
                        print(t1.next0_.value, end="", file=num)
                        t1 = t1.next0_
                    if (num.tell() == 1 and typ_ == AddressItemToken.ItemType.OFFICE): 
                        return None
                if (typ_ == AddressItemToken.ItemType.BOX and num.tell() == 0): 
                    rom = NumberHelper.try_parse_roman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new65(typ_, t, rom.end_token, str(rom.value))
            elif (((BracketHelper.is_bracket(t1, False) and (isinstance(t1.next0_, TextToken)) and t1.next0_.length_char == 1) and t1.next0_.is_letters and BracketHelper.is_bracket(t1.next0_.next0_, False)) and not t1.is_whitespace_after and not t1.next0_.is_whitespace_after): 
                ch = AddressItemToken.__correct_char_token(t1.next0_)
                if (ch is None): 
                    return None
                print(ch, end="", file=num)
                t1 = t1.next0_.next0_
            elif ((isinstance(t1, TextToken)) and ((((t1.length_char == 1 and ((t1.is_hiphen or t1.is_char('_'))))) or t1.is_value("НЕТ", None) or t1.is_value("БН", None))) and (((typ_ == AddressItemToken.ItemType.CORPUS or typ_ == AddressItemToken.ItemType.CORPUSORFLAT or typ_ == AddressItemToken.ItemType.BUILDING) or typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.FLAT))): 
                while t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_char('_'))) and not t1.is_whitespace_after:
                    t1 = t1.next0_
                val = None
                if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                    t1 = t1.next0_
                    val = str(t1.value)
                if (t1.is_value("БН", None)): 
                    val = "0"
                return AddressItemToken._new65(typ_, t, t1, val)
            else: 
                if (((typ_ == AddressItemToken.ItemType.FLOOR or typ_ == AddressItemToken.ItemType.KILOMETER or typ_ == AddressItemToken.ItemType.POTCH)) and (isinstance(t.previous, NumberToken))): 
                    return AddressItemToken(typ_, t, t1.previous)
                if ((isinstance(t1, ReferentToken)) and (isinstance(t1.get_referent(), DateReferent))): 
                    nn = AddressItemToken.__try_parse(t1.begin_token, loc_streets, prefix_before, True, None)
                    if (nn is not None and nn.end_char == t1.end_char and nn.typ == AddressItemToken.ItemType.NUMBER): 
                        nn.begin_token = t
                        nn.end_token = t1
                        nn.typ = typ_
                        return nn
                if ((isinstance(t1, TextToken)) and ((typ_ == AddressItemToken.ItemType.HOUSE or typ_ == AddressItemToken.ItemType.BUILDING or typ_ == AddressItemToken.ItemType.CORPUS))): 
                    ter = t1.term
                    if (ter == "АБ" or ter == "АБВ" or ter == "МГУ"): 
                        return AddressItemToken._new78(typ_, t, t1, ter, house_typ, build_typ)
                    if (prev is not None and ((prev.typ == AddressItemToken.ItemType.STREET or prev.typ == AddressItemToken.ItemType.CITY)) and t1.chars.is_all_upper): 
                        return AddressItemToken._new78(typ_, t, t1, ter, house_typ, build_typ)
                if (typ_ == AddressItemToken.ItemType.BOX): 
                    rom = NumberHelper.try_parse_roman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new65(typ_, t, rom.end_token, str(rom.value))
                if (typ_ == AddressItemToken.ItemType.PLOT and t1 is not None): 
                    if ((t1.is_value("ОКОЛО", None) or t1.is_value("РЯДОМ", None) or t1.is_value("НАПРОТИВ", None)) or t1.is_value("БЛИЗЬКО", None) or t1.is_value("НАВПАКИ", None)): 
                        return AddressItemToken._new65(typ_, t, t1, t1.get_source_text().lower())
                return None
        if (typ_ == AddressItemToken.ItemType.NUMBER and prepos): 
            return None
        if (t1 is None): 
            t1 = t
            while t1.next0_ is not None:
                t1 = t1.next0_
        return AddressItemToken._new87(typ_, t, t1, Utils.toStringStringIO(num), t.morph, house_typ, build_typ)
    
    @staticmethod
    def __try_attachvch(t : 'Token', ty : 'ItemType') -> 'AddressItemToken':
        if (t is None): 
            return None
        tt = t
        while tt is not None: 
            if ((((tt.is_value("В", None) or tt.is_value("B", None))) and tt.next0_ is not None and tt.next0_.is_char_of("./\\")) and (isinstance(tt.next0_.next0_, TextToken)) and tt.next0_.next0_.is_value("Ч", None)): 
                tt = tt.next0_.next0_
                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                    tt = tt.next0_
                tt2 = MiscHelper.check_number_prefix(tt.next0_)
                if (tt2 is not None): 
                    tt = tt2
                if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                    tt = tt.next0_
                return AddressItemToken._new65(ty, t, tt, "В/Ч")
            elif (((tt.is_value("ВОЙСКОВОЙ", None) or tt.is_value("ВОИНСКИЙ", None))) and tt.next0_ is not None and tt.next0_.is_value("ЧАСТЬ", None)): 
                tt = tt.next0_
                tt2 = MiscHelper.check_number_prefix(tt.next0_)
                if (tt2 is not None): 
                    tt = tt2
                if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                    tt = tt.next0_
                return AddressItemToken._new65(ty, t, tt, "В/Ч")
            elif (ty == AddressItemToken.ItemType.FLAT): 
                if (tt.whitespaces_before_count > 1): 
                    break
                if (not (isinstance(tt, TextToken))): 
                    break
                if (tt.term.startswith("ОБЩ")): 
                    if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                        tt = tt.next0_
                    re = AddressItemToken.__try_attachvch(tt.next0_, ty)
                    if (re is not None): 
                        return re
                    return AddressItemToken._new65(ty, t, tt, "ОБЩ")
                if (tt.chars.is_all_upper and tt.length_char > 1): 
                    re = AddressItemToken._new65(ty, t, tt, tt.term)
                    if ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_all_upper): 
                        tt = tt.next0_
                        re.end_token = tt
                        re.value += tt.term
                    return re
                break
            else: 
                break
            tt = tt.next0_
        return None
    
    @staticmethod
    def try_attach_detail(t : 'Token') -> 'AddressItemToken':
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        tt = t
        if (t.chars.is_capital_upper and not t.morph.class0_.is_preposition): 
            return None
        tok = AddressItemToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_preposition and t.next0_ is not None): 
            tt = t.next0_
            if (isinstance(tt, NumberToken)): 
                pass
            else: 
                if (tt.chars.is_capital_upper and not tt.morph.class0_.is_preposition): 
                    return None
                tok = AddressItemToken.M_ONTOLOGY.try_parse(tt, TerminParseAttr.NO)
        res = None
        first_num = False
        if (tok is None): 
            if (isinstance(tt, NumberToken)): 
                first_num = True
                nex = NumberHelper.try_parse_number_with_postfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    res = AddressItemToken(AddressItemToken.ItemType.DETAIL, t, nex.end_token)
                    tyy = NumberExType.METER
                    wraptyy92 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalize_value(wraptyy92)))
                    tyy = wraptyy92.value
            if (res is None): 
                return None
        else: 
            if (not (isinstance(tok.termin.tag, AddressDetailType))): 
                return None
            if (t.is_value("У", None)): 
                if (MiscLocationHelper.check_geo_object_before(t)): 
                    pass
                elif (MiscLocationHelper.check_geo_object_after(t, False)): 
                    pass
                else: 
                    return None
            res = AddressItemToken._new93(AddressItemToken.ItemType.DETAIL, t, tok.end_token, Utils.valToEnum(tok.termin.tag, AddressDetailType))
        tt = res.end_token.next0_
        first_pass3491 = True
        while True:
            if first_pass3491: first_pass3491 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (isinstance(tt, ReferentToken)): 
                break
            if (not tt.morph.class0_.is_preposition): 
                if (tt.chars.is_capital_upper or tt.chars.is_all_upper): 
                    break
            tok = AddressItemToken.M_ONTOLOGY.try_parse(tt, TerminParseAttr.NO)
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
            if (tt.is_value("ОРИЕНТИР", None) or tt.is_value("НАПРАВЛЕНИЕ", None) or tt.is_value("ОТ", None)): 
                res.end_token = tt
                continue
            if (tt.is_comma or tt.morph.class0_.is_preposition): 
                continue
            if ((isinstance(tt, NumberToken)) and tt.next0_ is not None): 
                nex = NumberHelper.try_parse_number_with_postfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    tt = nex.end_token
                    res.end_token = tt
                    tyy = NumberExType.METER
                    wraptyy94 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalize_value(wraptyy94)))
                    tyy = wraptyy94.value
                    continue
            break
        if (first_num and res.detail_type == AddressDetailType.UNDEFINED): 
            return None
        if (res is not None and res.end_token.next0_ is not None and res.end_token.next0_.morph.class0_.is_preposition): 
            if (res.end_token.whitespaces_after_count == 1 and res.end_token.next0_.whitespaces_after_count == 1): 
                res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def try_attach_org(t : 'Token') -> 'AddressItemToken':
        if (not (isinstance(t, TextToken))): 
            return None
        if ((t.length_char > 5 and not t.chars.is_all_upper and not t.chars.is_all_lower) and not t.chars.is_capital_upper): 
            namm = t.get_source_text()
            if (str.isupper(namm[0]) and str.isupper(namm[1])): 
                i = 0
                while i < len(namm): 
                    if (str.islower(namm[i]) and i > 2): 
                        abbr = namm[0:0+i - 1]
                        te = Termin._new95(abbr, abbr)
                        li = AddressItemToken.M_ORG_ONTOLOGY.find_termins_by_termin(te)
                        if (li is not None and len(li) > 0): 
                            org00 = t.kit.create_referent("ORGANIZATION")
                            org00.add_slot("TYPE", li[0].canonic_text.lower(), False, 0)
                            org00.add_slot("TYPE", abbr, False, 0)
                            namm = t.term[i - 1:]
                            rt00 = ReferentToken(org00, t, t)
                            rt00.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
                            if (t.next0_ is not None and t.next0_.is_hiphen): 
                                if (isinstance(t.next0_.next0_, NumberToken)): 
                                    org00.add_slot("NUMBER", str(t.next0_.next0_.value), False, 0)
                                    rt00.end_token = t.next0_.next0_
                                elif ((isinstance(t.next0_.next0_, TextToken)) and not t.next0_.is_whitespace_after): 
                                    namm = "{0}-{1}".format(namm, t.next0_.next0_.term)
                                    rt00.end_token = t.next0_.next0_
                            org00.add_slot("NAME", namm, False, 0)
                            return AddressItemToken._new96(AddressItemToken.ItemType.STREET, t, rt00.end_token, rt00.referent, rt00, True)
                        break
                    i += 1
        if (t.is_value("СТ", None)): 
            pass
        rt = None
        typ_ = None
        typ2 = None
        nam = None
        num = None
        t1 = None
        ok = False
        tok = AddressItemToken.M_ORG_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
        rt1 = t.kit.process_referent("ORGANIZATION", t)
        if (rt1 is None): 
            rt1 = t.kit.process_referent("NAMEDENTITY", t)
            if (rt1 is not None): 
                tyy = rt1.referent.get_string_value("TYPE")
                if (((tyy == "аэропорт" or tyy == "аэродром" or tyy == "заказник") or tyy == "лес" or tyy == "заповедник") or tyy == "сад"): 
                    pass
                else: 
                    rt1 = (None)
        else: 
            if (rt1.referent.find_slot("TYPE", "ОПС", True) is not None): 
                return None
            tt = rt1.begin_token.next0_
            while tt is not None and (tt.end_char < rt1.end_char): 
                if (tt.is_comma): 
                    rt1.end_token = tt.previous
                    if (isinstance(tt.next0_, ReferentToken)): 
                        s = rt1.referent.find_slot(None, tt.next0_.get_referent(), True)
                        if (s is not None): 
                            rt1.referent.slots.remove(s)
                tt = tt.next0_
            tt = rt1.end_token.next0_
            while tt is not None: 
                if (tt.is_hiphen or tt.is_comma): 
                    pass
                elif ((isinstance(tt, TextToken)) and tt.term == "ПМК"): 
                    tt2 = tt.next0_
                    if (tt2 is not None and ((tt2.is_hiphen or tt2.is_char_of(":")))): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2, NumberToken)): 
                        rt1.referent.add_slot("NUMBER", str(tt2.value), False, 0)
                        rt1.end_token = tt2
                        break
                else: 
                    break
                tt = tt.next0_
        tt1 = t.next0_
        if (tt1 is not None and tt1.is_value("ПМК", None)): 
            tt1 = tt1.next0_
        if (tok is not None): 
            if (tok.begin_token == tok.end_token and tok.begin_token.is_value("СП", None)): 
                tok = AddressItemToken.M_ORG_ONTOLOGY.try_parse(tok.end_token.next0_, TerminParseAttr.NO)
                if (tok is not None): 
                    tok.begin_token = t
                    ok = True
                    tt1 = tok.end_token.next0_
                if (rt1 is None): 
                    rt1 = t.kit.process_referent("ORGANIZATION", t.next0_)
                    if ((rt1) is not None): 
                        rt1.begin_token = t
            elif (tok.begin_token == tok.end_token and tok.begin_token.is_value("ГПК", None)): 
                tt1 = tok.end_token.next0_
                if (tt1 is None or tok.is_newline_after or not (isinstance(tt1, TextToken))): 
                    return None
                if (tt1.kit.process_referent("GEO", tt1) is not None): 
                    return None
                if (tt1.chars.is_all_upper or BracketHelper.can_be_start_of_sequence(tt1, True, False)): 
                    pass
                else: 
                    return None
            else: 
                ok = True
                tt1 = tok.end_token.next0_
            tok2 = AddressItemToken.M_ORG_ONTOLOGY.try_parse(tt1, TerminParseAttr.NO)
            if (tok2 is not None): 
                tt1 = tok2.end_token.next0_
                tok2 = AddressItemToken.M_ORG_ONTOLOGY.try_parse(tt1, TerminParseAttr.NO)
                if (tok2 is not None): 
                    tt1 = tok2.end_token.next0_
            while tt1 is not None:
                if (tt1.is_value("ОБЩЕСТВО", None) or tt1.is_value("ТЕРРИТОРИЯ", None) or tt1.is_value("ПМК", None)): 
                    tt1 = tt1.next0_
                else: 
                    break
            if ((isinstance(tt1, TextToken)) and tt1.chars.is_all_lower and ((tt1.length_char == 2 or tt1.length_char == 3))): 
                if (tt1.whitespaces_before_count < 2): 
                    if (AddressItemToken.check_house_after(tt1, False, False)): 
                        return None
                    tt1 = tt1.next0_
        elif (t.length_char > 1 and t.chars.is_cyrillic_letter): 
            nt2 = t
            num2 = None
            if (t.chars.is_all_upper): 
                if (t.is_value("ФЗ", None) or t.is_value("ФКЗ", None)): 
                    return None
                ok = True
            elif (t.chars.is_all_lower and t.get_morph_class_in_dictionary().is_undefined and not t.is_value("ПСЕВДО", None)): 
                ok = True
            tt2 = t.next0_
            first_pass3492 = True
            while True:
                if first_pass3492: first_pass3492 = False
                else: tt2 = tt2.next0_
                if (not (tt2 is not None)): break
                if (tt2.whitespaces_before_count > 2): 
                    break
                ooo = AddressItemToken.M_ORG_ONTOLOGY.try_parse(tt2, TerminParseAttr.NO)
                if (ooo is not None): 
                    oooo = AddressItemToken.try_attach_org(tt2)
                    if (oooo is None): 
                        ok = True
                        tok = ooo
                        typ_ = tok.termin.canonic_text.lower()
                        typ2 = tok.termin.acronym
                        nam = MiscHelper.get_text_value(t, nt2, GetTextAttr.NO)
                        if (isinstance(num2, NumberToken)): 
                            num = str(num2.value)
                        t1 = nt2
                    break
                if (tt2.is_hiphen): 
                    continue
                if (tt2.is_value("ИМ", None)): 
                    if (tt2.next0_ is not None and tt2.next0_.is_char('.')): 
                        tt2 = tt2.next0_
                    continue
                if (isinstance(tt2, NumberToken)): 
                    num2 = tt2
                    continue
                nuuu = NumberHelper.try_parse_age(tt2)
                if (nuuu is not None): 
                    num = str(nuuu.value)
                    num2 = (nuuu)
                    tt2 = nuuu.end_token
                    continue
                if (not (isinstance(tt2, TextToken)) or not tt2.chars.is_cyrillic_letter): 
                    break
                if (tt2.chars.is_all_lower): 
                    nnn = NounPhraseHelper.try_parse(tt2.previous, NounPhraseParseAttr.NO, 0, None)
                    if (nnn is not None and nnn.end_token == tt2): 
                        pass
                    elif (tt2.get_morph_class_in_dictionary().is_noun and tt2.morph.case_.is_genitive): 
                        pass
                    else: 
                        break
                nt2 = tt2
        elif (BracketHelper.is_bracket(t, True)): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                if (AddressItemToken.check_house_after(br.end_token.next0_, False, False)): 
                    tt1 = t
                    ok = True
                else: 
                    txt = Utils.ifNotNull(MiscHelper.get_text_value(br.begin_token, br.end_token, GetTextAttr.NO), "")
                    if (("БИЗНЕС" in txt or "БІЗНЕС" in txt or "ПЛАЗА" in txt) or "PLAZA" in txt): 
                        tt1 = t
                        ok = True
        bracks = False
        is_very_doubt = False
        if (ok and BracketHelper.is_bracket(tt1, False)): 
            br = BracketHelper.try_parse(tt1, BracketParseAttr.NO, 100)
            if (br is not None and (br.length_char < 100)): 
                res1 = AddressItemToken.try_attach_org(tt1.next0_)
                if (res1 is not None and res1.ref_token is not None): 
                    if (res1.end_token == br.end_token or res1.end_token == br.end_token.previous): 
                        res1.ref_token.begin_token = res1.begin_token = t
                        res1.ref_token.end_token = res1.end_token = br.end_token
                        res1.ref_token.referent.add_slot("TYPE", (t.get_source_text().upper() if tok is None else tok.termin.canonic_text.lower()), False, 0)
                        return res1
                typ_ = (((None if t == tt1 else MiscHelper.get_text_value(t, t, GetTextAttr.NO))) if tok is None else tok.termin.canonic_text.lower())
                if (tok is not None): 
                    typ2 = tok.termin.acronym
                tt = br.end_token.previous
                if (isinstance(tt, NumberToken)): 
                    num = str(tt.value)
                    tt = tt.previous
                    if (tt is not None and (((tt.is_hiphen or tt.is_char('_') or tt.is_value("N", None)) or tt.is_value("№", None)))): 
                        tt = tt.previous
                if (tt is not None): 
                    nam = MiscHelper.get_text_value(br.begin_token, tt, GetTextAttr.NO)
                t1 = br.end_token
                bracks = True
        if (ok and ((((typ_ is None and ((t.chars.is_all_upper and t.length_char == 3)))) or tok is not None))): 
            tt = tt1
            if (tt is not None and ((tt.is_hiphen or tt.is_char('_')))): 
                tt = tt.next0_
            adt = AddressItemToken.try_parse(tt, None, False, True, None)
            if (adt is not None and adt.typ == AddressItemToken.ItemType.NUMBER): 
                if (tt.previous.is_hiphen or tt.previous.is_char('_') or not (isinstance(tt, NumberToken))): 
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
            nam = MiscHelper.get_text_value(tt1, tt1, GetTextAttr.NO)
            if (typ2 == "СТ" and nam == "СЭВ"): 
                return None
            t1 = tt1
        elif (((tok is not None and typ_ is None and tt1 is not None) and (isinstance(tt1.get_referent(), GeoReferent)) and (tt1.whitespaces_before_count < 3)) and tt1.begin_token == tt1.end_token): 
            typ_ = tok.termin.canonic_text.lower()
            typ2 = tok.termin.acronym
            nam = MiscHelper.get_text_value(tt1, tt1, GetTextAttr.NO)
            t1 = tt1
        if ((ok and typ_ is None and num is not None) and t.length_char > 2 and (t.length_char < 5)): 
            tt2 = t1.next0_
            if (tt2 is not None and tt2.is_char(',')): 
                tt2 = tt2.next0_
            if (tt2 is not None and (tt2.whitespaces_after_count < 2)): 
                adt = AddressItemToken.try_parse(tt2, None, False, True, None)
                if (adt is not None): 
                    if (((adt.typ == AddressItemToken.ItemType.BLOCK or adt.typ == AddressItemToken.ItemType.BOX or adt.typ == AddressItemToken.ItemType.BUILDING) or adt.typ == AddressItemToken.ItemType.CORPUS or adt.typ == AddressItemToken.ItemType.HOUSE) or adt.typ == AddressItemToken.ItemType.PLOT): 
                        typ_ = t.get_source_text()
        if (typ_ is None and nam is not None): 
            if ("БИЗНЕС" in nam or "ПЛАЗА" in nam or "PLAZA" in nam): 
                typ_ = "бизнес центр"
            elif ("БІЗНЕС" in nam): 
                typ_ = "бізнес центр"
        if (typ_ is not None): 
            org0_ = t.kit.create_referent("ORGANIZATION")
            if (org0_ is None): 
                org0_ = Referent("ORGANIZATION")
            org0_.add_slot("TYPE", typ_, False, 0)
            if (typ2 is not None): 
                org0_.add_slot("TYPE", typ2, False, 0)
            if (nam is not None): 
                if ((not bracks and t1.next0_ is not None and t1.next0_.chars.is_cyrillic_letter) and t1.whitespaces_after_count == 1): 
                    ok = False
                    if (tok is not None and t1.next0_ == tok.end_token): 
                        pass
                    elif (t1.next0_.next0_ is None or BracketHelper.can_be_end_of_sequence(t1.next0_.next0_, False, None, False)): 
                        ok = True
                    elif (t1.next0_.next0_.is_char(',')): 
                        ok = True
                    elif ((isinstance(t1.next0_.next0_, NumberToken)) and ((t1.next0_.next0_.next0_ is None or BracketHelper.can_be_end_of_sequence(t1.next0_.next0_.next0_, False, None, False)))): 
                        ok = True
                    elif (((t1.next0_.next0_.is_hiphen or t1.next0_.next0_.is_value("N", None) or t1.next0_.next0_.is_value("№", None))) and (isinstance(t1.next0_.next0_.next0_, NumberToken))): 
                        ok = True
                    if (ok): 
                        nam = "{0} {1}".format(nam, t1.next0_.get_source_text().upper())
                        t1 = t1.next0_
                elif ((((not bracks and t1.next0_ is not None and t1.next0_.next0_ is not None) and t1.next0_.is_hiphen and not t1.is_whitespace_after) and not t1.next0_.is_whitespace_after and (((isinstance(t1.next0_.next0_, TextToken)) or (isinstance(t1.next0_.next0_.get_referent(), GeoReferent))))) and t1.next0_.next0_.chars.is_cyrillic_letter): 
                    nam = "{0} {1}".format(nam, MiscHelper.get_text_value(t1.next0_.next0_, t1.next0_.next0_, GetTextAttr.NO))
                    t1 = t1.next0_.next0_
                if ((nam.startswith("ИМ.") or nam.startswith("ИМ ") or nam.startswith("ІМ.")) or nam.startswith("ІМ ")): 
                    org0_.add_slot("NAME", nam[3:].strip(), False, 0)
                    nam = "{0} {1}".format(("ІМЕНІ" if nam.startswith("ІМ") else "ИМЕНИ"), nam[3:].strip())
                if (nam.startswith("ИМЕНИ ") or nam.startswith("ІМЕНІ ")): 
                    org0_.add_slot("NAME", nam[6:].strip(), False, 0)
                org0_.add_slot("NAME", nam, False, 0)
            rt = ReferentToken._new97(org0_, t, t1, t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION"))
            empty_org = False
            if ((t1.next0_ is not None and t1.next0_.is_hiphen and t1.next0_.next0_ is not None) and t1.next0_.next0_.is_value("ГОРОДИЩЕ", None)): 
                rt.end_token = t1.next0_.next0_
            if (t1.next0_ is not None and t1.next0_.is_value("ПРИ", None)): 
                rtt = t1.kit.process_referent("ORGANIZATION", t1.next0_.next0_)
                if (rtt is not None): 
                    empty_org = True
                    t1 = rtt.end_token
                    rt.end_token = t1
            if (t1.next0_ is not None and t1.next0_.is_value("АПН", None)): 
                t1 = t1.next0_
                rt.end_token = t1
            if (t1.whitespaces_after_count < 2): 
                rtt1 = t1.kit.process_referent("ORGANIZATION", t1.next0_)
                if (rtt1 is not None): 
                    empty_org = True
                    t1 = rtt1.end_token
                    rt.end_token = t1
            if (empty_org and (t1.whitespaces_after_count < 2)): 
                terr = TerrItemToken.try_parse(t1.next0_, None, False, False, None)
                if (terr is not None and terr.onto_item is not None): 
                    t1 = terr.end_token
                    rt.end_token = t1
            if (num is not None): 
                org0_.add_slot("NUMBER", num, False, 0)
            elif (t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_value("№", None) or t1.next0_.is_value("N", None))) and (isinstance(t1.next0_.next0_, NumberToken))): 
                nai = AddressItemToken.try_parse(t1.next0_.next0_, None, False, True, None)
                if (nai is not None and nai.typ == AddressItemToken.ItemType.NUMBER): 
                    org0_.add_slot("NUMBER", nai.value, False, 0)
                    rt.end_token = nai.end_token
                    t1 = rt.end_token
                else: 
                    rt.end_token = t1.next0_.next0_
                    t1 = rt.end_token
                    org0_.add_slot("NUMBER", str(t1.value), False, 0)
            if (tok is not None and (t1.end_char < tok.end_char)): 
                rt.end_token = tok.end_token
                t1 = rt.end_token
                if (t1.next0_ is not None and (t1.whitespaces_after_count < 2) and t1.next0_.is_value("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                    rt.end_token = t1.next0_
                    t1 = rt.end_token
        if (rt is None): 
            rt = rt1
        elif (rt1 is not None and rt1.referent.type_name == "ORGANIZATION"): 
            if (is_very_doubt): 
                rt = rt1
            else: 
                rt.referent.merge_slots(rt1.referent, True)
                if (rt1.end_char > rt.end_char): 
                    rt.end_token = rt1.end_token
        if (rt is None): 
            return None
        if (t.is_value("АО", None)): 
            return None
        if (rt.referent.find_slot("TYPE", "администрация", True) is not None or rt.referent.find_slot("TYPE", "адміністрація", True) is not None): 
            ge = Utils.asObjectOrNull(rt.referent.get_slot_value("GEO"), GeoReferent)
            if (ge is not None): 
                return AddressItemToken._new64((AddressItemToken.ItemType.REGION if ge.is_region else AddressItemToken.ItemType.CITY), t, rt.end_token, ge)
        res = AddressItemToken._new96(AddressItemToken.ItemType.STREET, t, rt.end_token, rt.referent, rt, typ_ is not None)
        return res
    
    def create_geo_org_terr(self) -> 'ReferentToken':
        geo = GeoReferent()
        t1 = self.end_token
        geo._add_org_referent(self.referent)
        geo.add_ext_referent(self.ref_token)
        if (geo.find_slot(GeoReferent.ATTR_TYPE, None, True) is None): 
            geo._add_typ_ter(self.kit.base_language)
        return ReferentToken(geo, self.begin_token, self.end_token)
    
    @staticmethod
    def check_street_after(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.is_hiphen or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        if (t.is_newline_before): 
            return False
        ait = AddressItemToken.try_parse(t, None, False, False, None)
        if (ait is not None): 
            if (ait.typ == AddressItemToken.ItemType.STREET): 
                return True
        return False
    
    @staticmethod
    def check_house_after(t : 'Token', leek : bool=False, pure_house : bool=False) -> bool:
        if (t is None): 
            return False
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        if (t.is_newline_before): 
            return False
        ait = AddressItemToken.try_parse(t, None, False, True, None)
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
                while t1 is not None and t1.is_char_of(".,"):
                    t1 = t1.next0_
                ait = AddressItemToken.try_parse(t1, None, False, True, None)
                if (ait is not None and (((ait.typ == AddressItemToken.ItemType.BUILDING or ait.typ == AddressItemToken.ItemType.CORPUS or ait.typ == AddressItemToken.ItemType.FLAT) or ait.typ == AddressItemToken.ItemType.FLOOR or ait.typ == AddressItemToken.ItemType.OFFICE))): 
                    return True
        return False
    
    @staticmethod
    def check_km_after(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        km = AddressItemToken.try_parse(t, None, False, True, None)
        if (km is not None and km.typ == AddressItemToken.ItemType.KILOMETER): 
            return True
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0, None)
        if (npt is not None): 
            if (npt.end_token.is_value("КИЛОМЕТР", None) or npt.end_token.is_value("МЕТР", None)): 
                return True
        return False
    
    @staticmethod
    def check_km_before(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.")): 
                pass
            elif (t.is_value("КМ", None) or t.is_value("КИЛОМЕТР", None) or t.is_value("МЕТР", None)): 
                return True
            t = t.previous; cou += 1
        return False
    
    @staticmethod
    def correct_char(v : 'char') -> 'char':
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
    def __correct_char_token(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        v = tt.term
        if (len(v) != 1): 
            return None
        corr = AddressItemToken.correct_char(v[0])
        if (corr != (chr(0))): 
            return "{0}".format(corr)
        if (t.chars.is_cyrillic_letter): 
            return v
        return None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        if (AddressItemToken.M_ONTOLOGY is not None): 
            return
        StreetItemToken.initialize()
        AddressItemToken.M_ONTOLOGY = TerminCollection()
        t = Termin._new100("ДОМ", AddressItemToken.ItemType.HOUSE)
        t.add_abridge("Д.")
        t.add_variant("КОТТЕДЖ", False)
        t.add_abridge("КОТ.")
        t.add_variant("ДАЧА", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new101("БУДИНОК", AddressItemToken.ItemType.HOUSE, MorphLang.UA)
        t.add_abridge("Б.")
        t.add_variant("КОТЕДЖ", False)
        t.add_abridge("БУД.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new102("ВЛАДЕНИЕ", AddressItemToken.ItemType.HOUSE, AddressHouseType.ESTATE)
        t.add_abridge("ВЛАД.")
        t.add_abridge("ВЛД.")
        t.add_abridge("ВЛ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new102("ДОМОВЛАДЕНИЕ", AddressItemToken.ItemType.HOUSE, AddressHouseType.HOUSEESTATE)
        t.add_variant("ДОМОВЛАДЕНИЕ", False)
        t.add_abridge("ДВЛД.")
        t.add_abridge("ДМВЛД.")
        t.add_variant("ДОМОВЛ", False)
        t.add_variant("ДОМОВА", False)
        t.add_variant("ДОМОВЛАД", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ПОДЪЕЗД ДОМА", AddressItemToken.ItemType.HOUSE)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ПОДВАЛ ДОМА", AddressItemToken.ItemType.HOUSE)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("КРЫША ДОМА", AddressItemToken.ItemType.HOUSE)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ЭТАЖ", AddressItemToken.ItemType.FLOOR)
        t.add_abridge("ЭТ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ПОДЪЕЗД", AddressItemToken.ItemType.POTCH)
        t.add_abridge("ПОД.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("КОРПУС", AddressItemToken.ItemType.CORPUS)
        t.add_abridge("КОРП.")
        t.add_abridge("КОР.")
        t.add_abridge("Д.КОРП.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("К", AddressItemToken.ItemType.CORPUSORFLAT)
        t.add_abridge("К.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("СТРОЕНИЕ", AddressItemToken.ItemType.BUILDING)
        t.add_abridge("СТРОЕН.")
        t.add_abridge("СТР.")
        t.add_abridge("СТ.")
        t.add_abridge("ПОМ.СТР.")
        t.add_abridge("Д.СТР.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new102("СООРУЖЕНИЕ", AddressItemToken.ItemType.BUILDING, AddressBuildingType.CONSTRUCTION)
        t.add_abridge("СООР.")
        t.add_abridge("СООРУЖ.")
        t.add_abridge("СООРУЖЕН.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new102("ЛИТЕРА", AddressItemToken.ItemType.BUILDING, AddressBuildingType.LITER)
        t.add_abridge("ЛИТ.")
        t.add_variant("ЛИТЕР", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("УЧАСТОК", AddressItemToken.ItemType.PLOT)
        t.add_abridge("УЧАСТ.")
        t.add_abridge("УЧ.")
        t.add_abridge("УЧ-К")
        t.add_variant("ЗЕМЕЛЬНЫЙ УЧАСТОК", False)
        t.add_abridge("ЗЕМ.УЧ.")
        t.add_abridge("ЗЕМ.УЧ-К")
        t.add_abridge("З/У")
        t.add_abridge("ПОЗ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("КВАРТИРА", AddressItemToken.ItemType.FLAT)
        t.add_abridge("КВАРТ.")
        t.add_abridge("КВАР.")
        t.add_abridge("КВ.")
        t.add_abridge("КВ-РА")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ОФИС", AddressItemToken.ItemType.OFFICE)
        t.add_abridge("ОФ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new101("ОФІС", AddressItemToken.ItemType.OFFICE, MorphLang.UA)
        t.add_abridge("ОФ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("БИЗНЕС-ЦЕНТР", AddressItemToken.ItemType.BUSINESSCENTER)
        t.acronym = "БЦ"
        t.add_variant("БИЗНЕС ЦЕНТР", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("БЛОК", AddressItemToken.ItemType.BLOCK)
        t.add_variant("РЯД", False)
        t.add_variant("СЕКТОР", False)
        t.add_abridge("СЕК.")
        t.add_variant("МАССИВ", False)
        t.add_variant("ОЧЕРЕДЬ", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("БОКС", AddressItemToken.ItemType.BOX)
        t.add_variant("ГАРАЖ", False)
        t.add_variant("САРАЙ", False)
        t.add_abridge("ГАР.")
        t.add_variant("МАШИНОМЕСТО", False)
        t.add_variant("ПОМЕЩЕНИЕ", False)
        t.add_abridge("ПОМ.")
        t.add_variant("НЕЖИЛОЕ ПОМЕЩЕНИЕ", False)
        t.add_abridge("Н.П.")
        t.add_abridge("НП")
        t.add_variant("ПОДВАЛ", False)
        t.add_variant("ПОГРЕБ", False)
        t.add_variant("ПОДВАЛЬНОЕ ПОМЕЩЕНИЕ", False)
        t.add_variant("ПОДЪЕЗД", False)
        t.add_abridge("ГАРАЖ-БОКС")
        t.add_variant("ГАРАЖНЫЙ БОКС", False)
        t.add_abridge("ГБ.")
        t.add_abridge("Г.Б.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("КОМНАТА", AddressItemToken.ItemType.OFFICE)
        t.add_abridge("КОМ.")
        t.add_abridge("КОМН.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("КАБИНЕТ", AddressItemToken.ItemType.OFFICE)
        t.add_abridge("КАБ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("НОМЕР", AddressItemToken.ItemType.NUMBER)
        t.add_abridge("НОМ.")
        t.add_abridge("№")
        t.add_abridge("N")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new124("БЕЗ НОМЕРА", "Б/Н", AddressItemToken.ItemType.NONUMBER)
        t.add_abridge("Б.Н.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("АБОНЕНТСКИЙ ЯЩИК", AddressItemToken.ItemType.POSTOFFICEBOX)
        t.add_abridge("А.Я.")
        t.add_variant("ПОЧТОВЫЙ ЯЩИК", False)
        t.add_abridge("П.Я.")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new126("ГОРОДСКАЯ СЛУЖЕБНАЯ ПОЧТА", AddressItemToken.ItemType.CSP, "ГСП")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("АДРЕС", AddressItemToken.ItemType.PREFIX)
        t.add_variant("ЮРИДИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_abridge("ЮР.АДРЕС")
        t.add_abridge("ПОЧТ.АДРЕС")
        t.add_abridge("ФАКТ.АДРЕС")
        t.add_abridge("П.АДРЕС")
        t.add_variant("ЮРИДИЧЕСКИЙ/ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ПОЧТОВЫЙ АДРЕС", False)
        t.add_variant("АДРЕС ПРОЖИВАНИЯ", False)
        t.add_variant("МЕСТО НАХОЖДЕНИЯ", False)
        t.add_variant("МЕСТОНАХОЖДЕНИЕ", False)
        t.add_variant("МЕСТОПОЛОЖЕНИЕ", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("АДРЕСА", AddressItemToken.ItemType.PREFIX)
        t.add_variant("ЮРИДИЧНА АДРЕСА", False)
        t.add_variant("ФАКТИЧНА АДРЕСА", False)
        t.add_variant("ПОШТОВА АДРЕСА", False)
        t.add_variant("АДРЕСА ПРОЖИВАННЯ", False)
        t.add_variant("МІСЦЕ ПЕРЕБУВАННЯ", False)
        t.add_variant("ПРОПИСКА", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("КИЛОМЕТР", AddressItemToken.ItemType.KILOMETER)
        t.add_abridge("КИЛОМ.")
        t.add_abridge("КМ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ПЕРЕСЕЧЕНИЕ", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("НА ПЕРЕСЕЧЕНИИ", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ПЕРЕКРЕСТОК", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("НА ПЕРЕКРЕСТКЕ", AddressDetailType.CROSS))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("НА ТЕРРИТОРИИ", AddressDetailType.NEAR))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕРЕДИНА", AddressDetailType.NEAR))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ПРИМЫКАТЬ", AddressDetailType.NEAR))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ГРАНИЧИТЬ", AddressDetailType.NEAR))
        t = Termin._new100("ВБЛИЗИ", AddressDetailType.NEAR)
        t.add_variant("У", False)
        t.add_abridge("ВБЛ.")
        t.add_variant("ВОЗЛЕ", False)
        t.add_variant("ОКОЛО", False)
        t.add_variant("НЕДАЛЕКО ОТ", False)
        t.add_variant("РЯДОМ С", False)
        t.add_variant("ГРАНИЦА", False)
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("РАЙОН", AddressDetailType.NEAR)
        t.add_abridge("Р-Н")
        AddressItemToken.M_ONTOLOGY.add(t)
        t = Termin._new124("В РАЙОНЕ", "РАЙОН", AddressDetailType.NEAR)
        t.add_abridge("В Р-НЕ")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ПРИМЕРНО", AddressDetailType.UNDEFINED))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ПОРЯДКА", AddressDetailType.UNDEFINED))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ПРИБЛИЗИТЕЛЬНО", AddressDetailType.UNDEFINED))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("НАПРАВЛЕНИЕ", AddressDetailType.UNDEFINED))
        t = Termin._new100("ОБЩЕЖИТИЕ", AddressDetailType.HOSTEL)
        t.add_abridge("ОБЩ.")
        t.add_abridge("ПОМ.ОБЩ.")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕВЕРНЕЕ", AddressDetailType.NORTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕВЕР", AddressDetailType.NORTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЮЖНЕЕ", AddressDetailType.SOUTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЮГ", AddressDetailType.SOUTH))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЗАПАДНЕЕ", AddressDetailType.WEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЗАПАД", AddressDetailType.WEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ВОСТОЧНЕЕ", AddressDetailType.EAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ВОСТОК", AddressDetailType.EAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕВЕРО-ЗАПАДНЕЕ", AddressDetailType.NORTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕВЕРО-ЗАПАД", AddressDetailType.NORTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕВЕРО-ВОСТОЧНЕЕ", AddressDetailType.NORTHEAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("СЕВЕРО-ВОСТОК", AddressDetailType.NORTHEAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЮГО-ЗАПАДНЕЕ", AddressDetailType.SOUTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЮГО-ЗАПАД", AddressDetailType.SOUTHWEST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЮГО-ВОСТОЧНЕЕ", AddressDetailType.SOUTHEAST))
        AddressItemToken.M_ONTOLOGY.add(Termin._new100("ЮГО-ВОСТОК", AddressDetailType.SOUTHEAST))
        t = Termin("ТАМ ЖЕ")
        t.add_abridge("ТАМЖЕ")
        AddressItemToken.M_ONTOLOGY.add(t)
        AddressItemToken.M_ORG_ONTOLOGY = TerminCollection()
        t = Termin._new95("САДОВОЕ ТОВАРИЩЕСТВО", "СТ")
        t.add_variant("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СТ"
        t.add_abridge("С/ТОВ")
        t.add_abridge("ПК СТ")
        t.add_abridge("САД.ТОВ.")
        t.add_abridge("САДОВ.ТОВ.")
        t.add_abridge("С/Т")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДАЧНОЕ ТОВАРИЩЕСТВО")
        t.add_abridge("Д/Т")
        t.add_abridge("ДАЧ/Т")
        t.acronym = "ДТ"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САДОВЫЙ КООПЕРАТИВ")
        t.add_abridge("С/К")
        t.acronym = "СК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ")
        t.add_variant("ПОТРЕБКООПЕРАТИВ", False)
        t.acronym = "ПК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САДОВОДЧЕСКОЕ ДАЧНОЕ ТОВАРИЩЕСТВО")
        t.add_variant("САДОВОЕ ДАЧНОЕ ТОВАРИЩЕСТВО", False)
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
        t.add_variant("ДАЧНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        t.acronym = "ДСК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ")
        t.acronym = "СПК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО")
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СНТ"
        t.acronym_can_be_lower = True
        t.add_abridge("САДОВОЕ НЕКОМ-Е ТОВАРИЩЕСТВО")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "СНО", True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "СНП", True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "СНТ", True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "НСТ", True)
        t.add_variant("НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНСТ", True)
        t.add_variant("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("САДОВОДЧЕСКАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", "СПК", True)
        t.add_variant("САДОВАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ДАЧНО СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ДСПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ЖИЛИЩНЫЙ СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ЖСПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ЖСК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ЖСКИЗ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "ОНО", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "ОНП", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНТ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ОГОРОДНИЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ОПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СТСН", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "ТСН", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ", "ТСЖ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("САДОВЫЕ ЗЕМЕЛЬНЫЕ УЧАСТКИ", "СЗУ", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ТОВАРИЩЕСТВО ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ТИЗ", True))
        t = Termin._new163("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "КИЗ", True)
        t.add_variant("КИЗК", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin._new163("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СНТСН", True)
        t.add_variant("СНТ СН", False)
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
        t.add_abridge("А/К")
        t.acronym = "АК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ГАРАЖНЫЙ КООПЕРАТИВ")
        t.add_abridge("Г/К")
        t.add_abridge("ГР.КОП.")
        t.add_abridge("ГАР.КОП.")
        t.acronym = "ГК"
        t.acronym_can_be_lower = True
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ГСК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", "ГЭК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ГАРАЖНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ПГСК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(Termin._new163("ГАРАЖНЫЙ СТРОИТЕЛЬНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГСПК", True))
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("САНАТОРИЙ")
        t.add_abridge("САН.")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ДОМ ОТДЫХА")
        t.add_abridge("Д/О")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("СОВХОЗ")
        t.add_abridge("С-ЗА")
        t.add_abridge("С/ЗА")
        t.add_abridge("С/З")
        t.add_abridge("СХ.")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("ПИОНЕРСКИЙ ЛАГЕРЬ")
        t.add_abridge("П/Л")
        t.add_abridge("П.Л.")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("КУРОРТ")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ВЛАДЕЛЬЦЕВ")
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
        t = Termin("БИЗНЕС ЦЕНТР")
        t.acronym = "БЦ"
        t.add_variant("БІЗНЕС ЦЕНТР", False)
        AddressItemToken.M_ORG_ONTOLOGY.add(t)
    
    M_ONTOLOGY = None
    
    M_ORG_ONTOLOGY = None
    
    @staticmethod
    def _new64(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        return res
    
    @staticmethod
    def _new65(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        return res
    
    @staticmethod
    def _new67(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.is_doubt = _arg5
        return res
    
    @staticmethod
    def _new75(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'ReferentToken') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.ref_token = _arg4
        return res
    
    @staticmethod
    def _new76(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        return res
    
    @staticmethod
    def _new77(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressHouseType', _arg5 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.house_type = _arg4
        res.building_type = _arg5
        return res
    
    @staticmethod
    def _new78(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType', _arg6 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        res.building_type = _arg6
        return res
    
    @staticmethod
    def _new87(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'AddressHouseType', _arg7 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.morph = _arg5
        res.house_type = _arg6
        res.building_type = _arg7
        return res
    
    @staticmethod
    def _new93(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressDetailType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.detail_type = _arg4
        return res
    
    @staticmethod
    def _new96(_arg1 : 'ItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : 'ReferentToken', _arg6 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.ref_token = _arg5
        res.ref_token_is_gsk = _arg6
        return res