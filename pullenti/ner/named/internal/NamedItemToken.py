# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.named.NamedEntityKind import NamedEntityKind
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr

class NamedItemToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.kind = NamedEntityKind.UNDEFINED
        self.name_value = None;
        self.type_value = None;
        self.ref = None;
        self.is_wellknown = False
        self.is_in_bracket = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.kind != NamedEntityKind.UNDEFINED): 
            print(" [{0}]".format(Utils.enumToString(self.kind)), end="", file=res, flush=True)
        if (self.is_wellknown): 
            print(" (!)".format(), end="", file=res, flush=True)
        if (self.is_in_bracket): 
            print(" [br]".format(), end="", file=res, flush=True)
        if (self.type_value is not None): 
            print(" {0}".format(self.type_value), end="", file=res, flush=True)
        if (self.name_value is not None): 
            print(" \"{0}\"".format(self.name_value), end="", file=res, flush=True)
        if (self.ref is not None): 
            print(" -> {0}".format(str(self.ref)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse_list(t : 'Token', loc_onto : 'IntOntologyCollection') -> typing.List['NamedItemToken']:
        ne = NamedItemToken.try_parse(t, loc_onto)
        if (ne is None): 
            return None
        res = list()
        res.append(ne)
        t = ne.end_token.next0_
        while t is not None: 
            if (t.whitespaces_before_count > 2): 
                break
            ne = NamedItemToken.try_parse(t, loc_onto)
            if (ne is None): 
                break
            if (t.is_value("НЕТ", None)): 
                break
            res.append(ne)
            t = ne.end_token
            t = t.next0_
        return res
    
    @staticmethod
    def try_parse(t : 'Token', loc_onto : 'IntOntologyCollection') -> 'NamedItemToken':
        if (t is None): 
            return None
        if (isinstance(t, ReferentToken)): 
            r = t.get_referent()
            if ((r.type_name == "PERSON" or r.type_name == "PERSONPROPERTY" or (isinstance(r, GeoReferent))) or r.type_name == "ORGANIZATION"): 
                return NamedItemToken._new1754(t, t, r, t.morph)
            return None
        typ = NamedItemToken.__m_types.try_parse(t, TerminParseAttr.NO)
        nam = NamedItemToken.__m_names.try_parse(t, TerminParseAttr.NO)
        if (typ is not None): 
            if (not (isinstance(t, TextToken))): 
                return None
            res = NamedItemToken._new1755(typ.begin_token, typ.end_token, typ.morph, typ.chars)
            res.kind = (Utils.valToEnum(typ.termin.tag, NamedEntityKind))
            res.type_value = typ.termin.canonic_text
            if ((nam is not None and nam.end_token == typ.end_token and not t.chars.is_all_lower) and (Utils.valToEnum(nam.termin.tag, NamedEntityKind)) == res.kind): 
                res.name_value = nam.termin.canonic_text
                res.is_wellknown = True
            return res
        if (nam is not None): 
            if (nam.begin_token.chars.is_all_lower): 
                return None
            res = NamedItemToken._new1755(nam.begin_token, nam.end_token, nam.morph, nam.chars)
            res.kind = (Utils.valToEnum(nam.termin.tag, NamedEntityKind))
            res.name_value = nam.termin.canonic_text
            ok = True
            if (not t.is_whitespace_before and t.previous is not None): 
                ok = False
            elif (not t.is_whitespace_after and t.next0_ is not None): 
                if (t.next0_.is_char_of(",.;!?") and t.next0_.is_whitespace_after): 
                    pass
                else: 
                    ok = False
            if (ok): 
                res.is_wellknown = True
                res.type_value = (Utils.asObjectOrNull(nam.termin.tag2, str))
            return res
        adj = MiscLocationHelper.try_attach_nord_west(t)
        if (adj is not None): 
            if (adj.morph.class0_.is_noun): 
                if (adj.end_token.is_value("ВОСТОК", None)): 
                    if (adj.begin_token == adj.end_token): 
                        return None
                    re = NamedItemToken._new1757(t, adj.end_token, adj.morph)
                    re.kind = NamedEntityKind.LOCATION
                    re.name_value = MiscHelper.get_text_value(t, adj.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                    re.is_wellknown = True
                    return re
                return None
            if (adj.whitespaces_after_count > 2): 
                return None
            if ((isinstance(adj.end_token.next0_, ReferentToken)) and (isinstance(adj.end_token.next0_.get_referent(), GeoReferent))): 
                re = NamedItemToken._new1757(t, adj.end_token.next0_, adj.end_token.next0_.morph)
                re.kind = NamedEntityKind.LOCATION
                re.name_value = MiscHelper.get_text_value(t, adj.end_token.next0_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                re.is_wellknown = True
                re.ref = adj.end_token.next0_.get_referent()
                return re
            res = NamedItemToken.try_parse(adj.end_token.next0_, loc_onto)
            if (res is not None and res.kind == NamedEntityKind.LOCATION): 
                s = adj.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, res.morph.gender, False)
                if (s is not None): 
                    if (res.name_value is None): 
                        res.name_value = s.upper()
                    else: 
                        res.name_value = "{0} {1}".format(s.upper(), res.name_value)
                        res.type_value = (None)
                    res.begin_token = t
                    res.chars = t.chars
                    res.is_wellknown = True
                    return res
        if (t.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(t)): 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and len(npt.adjectives) > 0): 
                test = NamedItemToken.try_parse(npt.noun.begin_token, loc_onto)
                if (test is not None and test.end_token == npt.end_token and test.type_value is not None): 
                    test.begin_token = t
                    tmp = io.StringIO()
                    for a in npt.adjectives: 
                        s = a.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, test.morph.gender, False)
                        if (tmp.tell() > 0): 
                            print(' ', end="", file=tmp)
                        print(s, end="", file=tmp)
                    test.name_value = Utils.toStringStringIO(tmp)
                    test.chars = t.chars
                    if (test.kind == NamedEntityKind.LOCATION): 
                        test.is_wellknown = True
                    return test
        if ((BracketHelper.is_bracket(t, True) and t.next0_ is not None and t.next0_.chars.is_letter) and not t.next0_.chars.is_all_lower): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                res = NamedItemToken(t, br.end_token)
                res.is_in_bracket = True
                res.name_value = MiscHelper.get_text_value(t, br.end_token, GetTextAttr.NO)
                nam = NamedItemToken.__m_names.try_parse(t.next0_, TerminParseAttr.NO)
                if (nam is not None and nam.end_token == br.end_token.previous): 
                    res.kind = (Utils.valToEnum(nam.termin.tag, NamedEntityKind))
                    res.is_wellknown = True
                    res.name_value = nam.termin.canonic_text
                return res
        if (((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower) and t.length_char > 2): 
            res = NamedItemToken._new1757(t, t, t.morph)
            str0_ = t.term
            if (str0_.endswith("О") or str0_.endswith("И") or str0_.endswith("Ы")): 
                res.name_value = str0_
            else: 
                res.name_value = t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
            res.chars = t.chars
            if (((not t.is_whitespace_after and t.next0_ is not None and t.next0_.is_hiphen) and (isinstance(t.next0_.next0_, TextToken)) and not t.next0_.next0_.is_whitespace_after) and t.chars.is_cyrillic_letter == t.next0_.next0_.chars.is_cyrillic_letter): 
                res.end_token = t.next0_.next0_
                t = res.end_token
                res.name_value = "{0}-{1}".format(res.name_value, t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
            return res
        return None
    
    @staticmethod
    def _initialize() -> None:
        if (NamedItemToken.__m_types is not None): 
            return
        NamedItemToken.__m_types = TerminCollection()
        NamedItemToken.__m_names = TerminCollection()
        for s in ["ПЛАНЕТА", "ЗВЕЗДА", "КОМЕТА", "МЕТЕОРИТ", "СОЗВЕЗДИЕ", "ГАЛАКТИКА"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.PLANET
            NamedItemToken.__m_types.add(t)
        for s in ["СОЛНЦЕ", "МЕРКУРИЙ", "ВЕНЕРА", "ЗЕМЛЯ", "МАРС", "ЮПИТЕР", "САТУРН", "УРАН", "НЕПТУН", "ПЛУТОН", "ЛУНА", "ДЕЙМОС", "ФОБОС", "Ио", "Ганимед", "Каллисто"]: 
            t = Termin()
            t.init_by_normal_text(s.upper(), None)
            t.tag = NamedEntityKind.PLANET
            NamedItemToken.__m_names.add(t)
        for s in ["РЕКА", "ОЗЕРО", "МОРЕ", "ОКЕАН", "ЗАЛИВ", "ПРОЛИВ", "ПОБЕРЕЖЬЕ", "КОНТИНЕНТ", "ОСТРОВ", "ПОЛУОСТРОВ", "МЫС", "ГОРА", "ГОРНЫЙ ХРЕБЕТ", "ПЕРЕВАЛ", "ЛЕС", "САД", "ЗАПОВЕДНИК", "ЗАКАЗНИК", "ДОЛИНА", "УЩЕЛЬЕ", "РАВНИНА", "БЕРЕГ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            NamedItemToken.__m_types.add(t)
        for s in ["ТИХИЙ", "АТЛАНТИЧЕСКИЙ", "ИНДИЙСКИЙ", "СЕВЕРО-ЛЕДОВИТЫЙ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            t.tag2 = ("океан")
            NamedItemToken.__m_names.add(t)
        for s in ["ЕВРАЗИЯ", "АФРИКА", "АМЕРИКА", "АВСТРАЛИЯ", "АНТАРКТИДА"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            t.tag2 = ("континент")
            NamedItemToken.__m_names.add(t)
        for s in ["ВОЛГА", "НЕВА", "АМУР", "ОБЪ", "АНГАРА", "ЛЕНА", "ИРТЫШ", "ДНЕПР", "ДОН", "ДНЕСТР", "РЕЙН", "АМУДАРЬЯ", "СЫРДАРЬЯ", "ТИГР", "ЕВФРАТ", "ИОРДАН", "МИССИСИПИ", "АМАЗОНКА", "ТЕМЗА", "СЕНА", "НИЛ", "ЯНЦЗЫ", "ХУАНХЭ", "ПАРАНА", "МЕКОНГ", "МАККЕНЗИ", "НИГЕР", "ЕНИСЕЙ", "МУРРЕЙ", "САЛУИН", "ИНД", "РИО-ГРАНДЕ", "БРАХМАПУТРА", "ДАРЛИНГ", "ДУНАЙ", "ЮКОН", "ГАНГ", "МАРРАМБИДЖИ", "ЗАМБЕЗИ", "ТОКАНТИС", "ОРИНОКО", "СИЦЗЯН", "КОЛЫМА", "КАМА", "ОКА", "ЭЛЬЮА", "ВИСЛА", "ДАУГАВА", "ЗАПАДНАЯ ДВИНА", "НЕМАН", "МЕЗЕНЬ", "КУБАНЬ", "ЮЖНЫЙ БУГ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            t.tag2 = ("река")
            NamedItemToken.__m_names.add(t)
        for s in ["ЕВРОПА", "АЗИЯ", "АРКТИКА", "КАВКАЗ", "ПРИБАЛТИКА", "СИБИРЬ", "ЗАПОЛЯРЬЕ", "ЧУКОТКА", "ПРИБАЛТИКА", "БАЛКАНЫ", "СКАНДИНАВИЯ", "ОКЕАНИЯ", "АЛЯСКА", "УРАЛ", "ПОВОЛЖЬЕ", "ПРИМОРЬЕ", "КУРИЛЫ", "ТИБЕТ", "ГИМАЛАИ", "АЛЬПЫ", "САХАРА", "ГОБИ", "СИНАЙ", "БАЙКОНУР", "ЧЕРНОБЫЛЬ", "САДОВОЕ КОЛЬЦО", "СТАРЫЙ ГОРОД"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            NamedItemToken.__m_names.add(t)
        for s in ["ПАМЯТНИК", "МОНУМЕНТ", "МЕМОРИАЛ", "БЮСТ", "ОБЕЛИСК"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.MONUMENT
            NamedItemToken.__m_types.add(t)
        for s in ["ДВОРЕЦ", "КРЕМЛЬ", "ЗАМОК", "УСАДЬБА", "ДОМ", "ЗДАНИЕ", "ШТАБ-КВАРТИРА", "ЖЕЛЕЗНОДОРОЖНЫЙ ВОКЗАЛ", "ВОКЗАЛ", "АВТОВОКЗАЛ", "АЭРОПОРТ", "АЭРОДРОМ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.BUILDING
            NamedItemToken.__m_types.add(t)
        for s in ["КРЕМЛЬ", "КАПИТОЛИЙ", "БЕЛЫЙ ДОМ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.BUILDING
            NamedItemToken.__m_names.add(t)
        t = Termin._new100("МЕЖДУНАРОДНАЯ КОСМИЧЕСКАЯ СТАНЦИЯ", NamedEntityKind.BUILDING)
        t.acronym = "МКС"
        NamedItemToken.__m_names.add(t)
    
    __m_types = None
    
    __m_names = None
    
    @staticmethod
    def _new1754(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Referent', _arg4 : 'MorphCollection') -> 'NamedItemToken':
        res = NamedItemToken(_arg1, _arg2)
        res.ref = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1755(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : 'CharsInfo') -> 'NamedItemToken':
        res = NamedItemToken(_arg1, _arg2)
        res.morph = _arg3
        res.chars = _arg4
        return res
    
    @staticmethod
    def _new1757(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'NamedItemToken':
        res = NamedItemToken(_arg1, _arg2)
        res.morph = _arg3
        return res