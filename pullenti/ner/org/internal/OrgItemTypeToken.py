# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.org.internal.EpNerOrgInternalResourceHelper import EpNerOrgInternalResourceHelper
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper


class OrgItemTypeToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        from pullenti.morph.CharsInfo import CharsInfo
        super().__init__(begin, end, None)
        self.typ = None;
        self.name = None;
        self.alt_name = None;
        self.name_is_name = False
        self.alt_typ = None;
        self.number = None;
        self.__m_profile = None;
        self.root = None;
        self.__m_is_dep = -1
        self.is_not_typ = False
        self.__m_coef = -1
        self.geo = None;
        self.geo2 = None;
        self.chars_root = CharsInfo()
        self.can_be_dep_before_organization = False
        self.is_douter_org = False
        self.__m_is_doubt_root_word = -1
        self.can_be_organization = False
    
    @property
    def profiles(self) -> typing.List['OrgProfile']:
        """ Список профилей """
        if (self.__m_profile is None): 
            self.__m_profile = list()
            if (self.root is not None): 
                self.__m_profile.extend(self.root.profiles)
        return self.__m_profile
    @profiles.setter
    def profiles(self, value) -> typing.List['OrgProfile']:
        self.__m_profile = value
        return value
    
    @property
    def is_dep(self) -> bool:
        if (self.__m_is_dep >= 0): 
            return self.__m_is_dep > 0
        if (self.root is None): 
            return False
        if (OrgProfile.UNIT in self.root.profiles): 
            return True
        return False
    @is_dep.setter
    def is_dep(self, value) -> bool:
        self.__m_is_dep = (1 if value else 0)
        return value
    
    @property
    def coef(self) -> float:
        if (self.__m_coef >= 0): 
            return self.__m_coef
        if (self.root is not None): 
            return self.root.coeff
        return 0
    @coef.setter
    def coef(self, value) -> float:
        self.__m_coef = value
        return value
    
    @property
    def name_words_count(self) -> int:
        """ Количество слов в имени """
        cou = 1
        if (self.name is None): 
            return 1
        i = 0
        while i < len(self.name): 
            if (self.name[i] == ' '): 
                cou += 1
            i += 1
        return cou
    
    @property
    def is_doubt_root_word(self) -> bool:
        """ Корень - сомнительное слово (типа: организация или движение) """
        if (self.__m_is_doubt_root_word >= 0): 
            return self.__m_is_doubt_root_word == 1
        if (self.root is None): 
            return False
        return self.root.is_doubt_word
    @is_doubt_root_word.setter
    def is_doubt_root_word(self, value) -> bool:
        self.__m_is_doubt_root_word = (1 if value else 0)
        return value
    
    def __str__(self) -> str:
        if (self.name is not None): 
            return self.name
        else: 
            return self.typ
    
    @staticmethod
    def tryAttach(t : 'Token', can_be_first_letter_lower : bool=False, ad : 'AnalyzerDataWithOntology'=None) -> 'OrgItemTypeToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.org.internal.OrgItemTermin import OrgItemTermin
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.org.internal.OrgItemNumberToken import OrgItemNumberToken
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.morph.Morphology import Morphology
        if (t is None or (((isinstance(t, ReferentToken)) and not t.chars.is_latin_letter))): 
            return None
        res = OrgItemTypeToken.__TryAttach(t, can_be_first_letter_lower)
        if (res is not None and res.geo is not None): 
            pass
        if (res is None and t.chars.is_latin_letter): 
            if (t.isValue("THE", None)): 
                res1 = OrgItemTypeToken.tryAttach(t.next0_, can_be_first_letter_lower, None)
                if (res1 is not None): 
                    res1.begin_token = t
                    return res1
                return None
            if ((isinstance(t.getReferent(), GeoReferent)) and (isinstance(t.next0_, TextToken)) and t.next0_.chars.is_latin_letter): 
                res1 = OrgItemTypeToken.tryAttach(t.next0_, can_be_first_letter_lower, None)
                if (res1 is not None): 
                    res1.begin_token = t
                    res1.geo = (Utils.asObjectOrNull(t, ReferentToken))
                    res1.name = MiscHelper.getTextValueOfMetaToken(res1, GetTextAttr.NO)
                    return res1
            if (t.chars.is_capital_upper): 
                mc = t.getMorphClassInDictionary()
                if ((mc.is_conjunction or mc.is_preposition or mc.is_misc) or mc.is_pronoun or mc.is_personal_pronoun): 
                    pass
                else: 
                    ttt = t.next0_
                    while ttt is not None: 
                        if (not ttt.chars.is_latin_letter): 
                            break
                        if (ttt.whitespaces_before_count > 3): 
                            break
                        if (MiscHelper.isEngAdjSuffix(ttt.next0_)): 
                            ttt = ttt.next0_.next0_.next0_
                            if (ttt is None): 
                                break
                        res1 = OrgItemTypeToken.__TryAttach(ttt, True)
                        if (res1 is not None): 
                            res1.name = MiscHelper.getTextValue(t, res1.end_token, GetTextAttr.IGNOREARTICLES)
                            if (res1.coef < 5): 
                                res1.coef = 5
                            res1.begin_token = t
                            return res1
                        if (ttt.chars.is_all_lower and not ttt.is_and): 
                            break
                        if (ttt.whitespaces_before_count > 1): 
                            break
                        ttt = ttt.next0_
        if ((res is not None and res.name is not None and res.name.startswith("СОВМЕСТ")) and LanguageHelper.endsWithEx(res.name, "ПРЕДПРИЯТИЕ", "КОМПАНИЯ", None, None)): 
            res.root = OrgItemTypeToken.__m_sovm_pred
            res.typ = "совместное предприятие"
            tt1 = t.next0_
            while tt1 is not None and tt1.end_char <= res.end_token.begin_char: 
                rt = tt1.kit.processReferent("GEO", tt1)
                if (rt is not None): 
                    res.coef = res.coef + .5
                    if (res.geo is None): 
                        res.geo = rt
                    elif (res.geo.referent.canBeEquals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                        pass
                    elif (res.geo2 is None): 
                        res.geo2 = rt
                    tt1 = rt.end_token
                tt1 = tt1.next0_
        if (((((res is not None and res.begin_token.length_char <= 2 and not res.begin_token.chars.is_all_lower) and res.begin_token.next0_ is not None and res.begin_token.next0_.isChar('.')) and res.begin_token.next0_.next0_ is not None and res.begin_token.next0_.next0_.length_char <= 2) and not res.begin_token.next0_.next0_.chars.is_all_lower and res.begin_token.next0_.next0_.next0_ is not None) and res.begin_token.next0_.next0_.next0_.isChar('.') and res.end_token == res.begin_token.next0_.next0_.next0_): 
            return None
        if (res is not None and res.typ == "управление"): 
            if (res.name is not None and "ГОСУДАРСТВЕННОЕ" in res.name): 
                return None
            if (res.begin_token.previous is not None and res.begin_token.previous.isValue("ГОСУДАРСТВЕННЫЙ", None)): 
                return None
        if (res is not None and res.geo is None and (isinstance(res.begin_token.previous, TextToken))): 
            rt = res.kit.processReferent("GEO", res.begin_token.previous)
            if (rt is not None and rt.morph.class0_.is_adjective): 
                if (res.begin_token.previous.previous is not None and res.begin_token.previous.previous.isValue("ОРДЕН", None)): 
                    pass
                else: 
                    res.geo = rt
                    res.begin_token = rt.begin_token
        if ((res is not None and res.typ == "комитет" and res.geo is None) and res.end_token.next0_ is not None and (isinstance(res.end_token.next0_.getReferent(), GeoReferent))): 
            res.geo = (Utils.asObjectOrNull(res.end_token.next0_, ReferentToken))
            res.end_token = res.end_token.next0_
            res.coef = 2
            if (res.end_token.next0_ is not None and res.end_token.next0_.isValue("ПО", None)): 
                res.coef = res.coef + (1)
        if ((res is not None and res.typ == "агентство" and res.chars.is_capital_upper) and res.end_token.next0_ is not None and res.end_token.next0_.isValue("ПО", None)): 
            res.coef = res.coef + (3)
        if (res is not None and res.geo is not None): 
            has_adj = False
            tt1 = res.begin_token
            first_pass3059 = True
            while True:
                if first_pass3059: first_pass3059 = False
                else: tt1 = tt1.next0_
                if (not (tt1 is not None and tt1.end_char <= res.end_token.begin_char)): break
                rt = tt1.kit.processReferent("GEO", tt1)
                if (rt is not None): 
                    if (res.geo is not None and res.geo.referent.canBeEquals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                        continue
                    if (res.geo2 is not None and res.geo2.referent.canBeEquals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                        continue
                    res.coef = res.coef + .5
                    if (res.geo is None): 
                        res.geo = rt
                    elif (res.geo2 is None): 
                        res.geo2 = rt
                    tt1 = rt.end_token
                elif (tt1.getMorphClassInDictionary().is_adjective): 
                    has_adj = True
            if ((res.typ == "институт" or res.typ == "академия" or res.typ == "інститут") or res.typ == "академія"): 
                if (has_adj): 
                    res.coef = res.coef + (2)
                    res.can_be_organization = True
        if (res is not None and res.geo is None): 
            tt2 = res.end_token.next0_
            if (tt2 is not None and not tt2.is_newline_before and tt2.morph.class0_.is_preposition): 
                if (((isinstance(tt2.next0_, TextToken)) and (Utils.asObjectOrNull(tt2.next0_, TextToken)).term == "ВАШ" and res.root is not None) and OrgProfile.JUSTICE in res.root.profiles): 
                    res.coef = 5
                    res.end_token = tt2.next0_
                    tt2 = tt2.next0_.next0_
                    res.name = (((Utils.ifNotNull(res.name, (res.root.canonic_text if res is not None and res.root is not None else None)))) + " ПО ВЗЫСКАНИЮ АДМИНИСТРАТИВНЫХ ШТРАФОВ")
                    res.typ = "отдел"
            if (tt2 is not None and not tt2.is_newline_before and tt2.morph.class0_.is_preposition): 
                tt2 = tt2.next0_
                if (tt2 is not None and not tt2.is_newline_before and (isinstance(tt2.getReferent(), GeoReferent))): 
                    res.end_token = tt2
                    res.geo = (Utils.asObjectOrNull(tt2, ReferentToken))
                    if ((tt2.next0_ is not None and tt2.next0_.is_and and (isinstance(tt2.next0_.next0_, ReferentToken))) and (isinstance(tt2.next0_.next0_.getReferent(), GeoReferent))): 
                        tt2 = tt2.next0_.next0_
                        res.end_token = tt2
                        res.geo2 = (Utils.asObjectOrNull(tt2, ReferentToken))
            elif (((tt2 is not None and not tt2.is_newline_before and tt2.is_hiphen) and (isinstance(tt2.next0_, TextToken)) and tt2.next0_.getMorphClassInDictionary().is_noun) and not tt2.next0_.isValue("БАНК", None)): 
                npt1 = NounPhraseHelper.tryParse(res.end_token, NounPhraseParseAttr.NO, 0)
                if (npt1 is not None and npt1.end_token == tt2.next0_): 
                    res.alt_typ = npt1.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
                    res.end_token = npt1.end_token
            elif (tt2 is not None and (tt2.whitespaces_before_count < 3)): 
                npt = NounPhraseHelper.tryParse(tt2, NounPhraseParseAttr.NO, 0)
                if (npt is not None and npt.morph.case_.is_genitive): 
                    rr = tt2.kit.processReferent("NAMEDENTITY", tt2)
                    if (rr is not None and ((rr.morph.case_.is_genitive or rr.morph.case_.is_undefined)) and rr.referent.findSlot("KIND", "location", True) is not None): 
                        res.end_token = rr.end_token
                    elif (res.root is not None and res.root.typ == OrgItemTermin.Types.PREFIX and npt.end_token.isValue("ОБРАЗОВАНИЕ", None)): 
                        res.end_token = npt.end_token
                        res.profiles.append(OrgProfile.EDUCATION)
        if (res is not None and res.typ is not None and str.isdigit(res.typ[0])): 
            ii = res.typ.find(' ')
            if (ii < (len(res.typ) - 1)): 
                res.number = res.typ[0:0+ii]
                res.typ = res.typ[ii + 1:].strip()
        if (res is not None and res.name is not None and str.isdigit(res.name[0])): 
            ii = res.name.find(' ')
            if (ii < (len(res.name) - 1)): 
                res.number = res.name[0:0+ii]
                res.name = res.name[ii + 1:].strip()
        if (res is not None and res.typ == "фонд"): 
            if (t.previous is not None and ((t.previous.isValue("ПРИЗОВОЙ", None) or t.previous.isValue("ЖИЛИЩНЫЙ", None)))): 
                return None
            if (res.begin_token.isValue("ПРИЗОВОЙ", None) or res.begin_token.isValue("ЖИЛИЩНЫЙ", None)): 
                return None
        if (res is not None and res.length_char == 2 and res.typ == "АО"): 
            res.is_doubt_root_word = True
        if (res is not None and res.typ == "администрация" and t.next0_ is not None): 
            if ((t.next0_.isChar('(') and t.next0_.next0_ is not None and ((t.next0_.next0_.isValue("ПРАВИТЕЛЬСТВО", None) or t.next0_.next0_.isValue("ГУБЕРНАТОР", None)))) and t.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.isChar(')')): 
                res.end_token = t.next0_.next0_.next0_
                res.alt_typ = "правительство"
                return res
            if (isinstance(t.next0_.getReferent(), GeoReferent)): 
                res.alt_typ = "правительство"
        if ((res is not None and res.typ == "ассоциация" and res.end_token.next0_ is not None) and (res.whitespaces_after_count < 2)): 
            npt = NounPhraseHelper.tryParse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                str0_ = MiscHelper.getTextValueOfMetaToken(npt, GetTextAttr.NO)
                res.name = "{0} {1}".format(Utils.ifNotNull(res.name, (res.typ.upper() if res is not None and res.typ is not None else None)), str0_)
                res.end_token = npt.end_token
                res.coef = res.coef + (1)
        if ((res is not None and res.typ == "представительство" and res.end_token.next0_ is not None) and (res.whitespaces_after_count < 2)): 
            npt = NounPhraseHelper.tryParse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if (npt.end_token.isValue("ИНТЕРЕС", None)): 
                    return None
        if (res is not None and ((res.typ == "производитель" or res.typ == "завод"))): 
            tt1 = res.end_token.next0_
            if (res.typ == "завод"): 
                if ((tt1 is not None and tt1.isValue("ПО", None) and tt1.next0_ is not None) and tt1.next0_.isValue("ПРОИЗВОДСТВО", None)): 
                    tt1 = tt1.next0_.next0_
            npt = NounPhraseHelper.tryParse(tt1, NounPhraseParseAttr.NO, 0)
            if ((npt is not None and (res.whitespaces_after_count < 2) and tt1.chars.is_all_lower) and npt.morph.case_.is_genitive): 
                str0_ = MiscHelper.getTextValueOfMetaToken(npt, GetTextAttr.NO)
                res.name = "{0} {1}".format(Utils.ifNotNull(res.name, (res.typ.upper() if res is not None and res.typ is not None else None)), str0_)
                if (res.geo is not None): 
                    res.coef = res.coef + (1)
                res.end_token = npt.end_token
            elif (res.typ != "завод"): 
                return None
        if (res is not None and (isinstance(res.begin_token.previous, TextToken)) and ((res.typ == "милиция" or res.typ == "полиция"))): 
            tok = OrgItemTypeToken.__m_global.tryAttach(res.begin_token.previous, None, False)
            if (tok is not None): 
                return None
        if (res is not None and res.typ == "предприятие"): 
            if (res.alt_typ == "головное предприятие" or res.alt_typ == "дочернее предприятие"): 
                res.is_not_typ = True
            elif (t.previous is not None and ((t.previous.isValue("ГОЛОВНОЙ", None) or t.previous.isValue("ДОЧЕРНИЙ", None)))): 
                return None
        if (res is not None and res.is_douter_org): 
            res.is_not_typ = True
            if (res.begin_token != res.end_token): 
                res1 = OrgItemTypeToken.__TryAttach(res.begin_token.next0_, True)
                if (res1 is not None and not res1.is_doubt_root_word): 
                    res.is_not_typ = False
        if (res is not None and res.typ == "суд"): 
            tt1 = Utils.asObjectOrNull(res.end_token, TextToken)
            if (tt1 is not None and ((tt1.term == "СУДА" or tt1.term == "СУДОВ"))): 
                if ((((res.morph.number) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                    return None
        if (res is not None and res.typ == "кафедра" and (isinstance(t, TextToken))): 
            if (t.isValue("КАФЕ", None) and ((t.next0_ is None or not t.next0_.isChar('.')))): 
                return None
        if (res is not None and res.typ == "компания"): 
            if ((t.previous is not None and t.previous.is_hiphen and t.previous.previous is not None) and t.previous.previous.isValue("КАЮТ", None)): 
                return None
        if (res is not None and t.previous is not None): 
            if (res.morph.case_.is_genitive): 
                if (t.previous.isValue("СТАНДАРТ", None)): 
                    return None
        if (res is not None and res.typ == "радиостанция" and res.name_words_count > 1): 
            return None
        if ((res is not None and res.typ == "предприятие" and res.alt_typ is not None) and res.begin_token.morph.class0_.is_adjective and not res.root.is_pure_prefix): 
            res.typ = res.alt_typ
            res.alt_typ = (None)
            res.coef = 3
        if (res is not None): 
            npt = NounPhraseHelper.tryParse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None and ((npt.noun.isValue("ТИП", None) or npt.noun.isValue("РЕЖИМ", None))) and npt.morph.case_.is_genitive): 
                res.end_token = npt.end_token
                s = "{0} {1}".format(res.typ, MiscHelper.getTextValueOfMetaToken(npt, GetTextAttr.NO)).lower()
                if ("колония" in res.typ or "тюрьма" in res.typ): 
                    res.coef = 3
                    res.alt_typ = s
                elif (res.name is None or len(res.name) == len(res.typ)): 
                    res.name = s
                else: 
                    res.alt_typ = s
        if (res is not None and OrgProfile.EDUCATION in res.profiles and (isinstance(res.end_token.next0_, TextToken))): 
            tt1 = res.end_token.next0_
            if ((Utils.asObjectOrNull(tt1, TextToken)).term == "ВПО" or (Utils.asObjectOrNull(tt1, TextToken)).term == "СПО"): 
                res.end_token = res.end_token.next0_
            else: 
                nnt = NounPhraseHelper.tryParse(tt1, NounPhraseParseAttr.NO, 0)
                if (nnt is not None and nnt.end_token.isValue("ОБРАЗОВАНИЕ", "ОСВІТА")): 
                    res.end_token = nnt.end_token
        if (res is not None and res.root is not None and res.root.is_pure_prefix): 
            tt1 = res.end_token.next0_
            if (tt1 is not None and ((tt1.isValue("С", None) or tt1.isValue("C", None)))): 
                npt = NounPhraseHelper.tryParse(tt1.next0_, NounPhraseParseAttr.NO, 0)
                if (npt is not None and ((npt.noun.isValue("ИНВЕСТИЦИЯ", None) or npt.noun.isValue("ОТВЕТСТВЕННОСТЬ", None)))): 
                    res.end_token = npt.end_token
        if (res is not None and res.root == OrgItemTypeToken.__m_military_unit and res.end_token.next0_ is not None): 
            if (res.end_token.next0_.isValue("ПП", None)): 
                res.end_token = res.end_token.next0_
            elif (res.end_token.next0_.isValue("ПОЛЕВОЙ", None) and res.end_token.next0_.next0_ is not None and res.end_token.next0_.next0_.isValue("ПОЧТА", None)): 
                res.end_token = res.end_token.next0_.next0_
        if (res is not None): 
            if (res.name_words_count > 1 and res.typ == "центр"): 
                res.can_be_dep_before_organization = True
            elif (LanguageHelper.endsWith(res.typ, " центр")): 
                res.can_be_dep_before_organization = True
            if (t.isValue("ГПК", None)): 
                if (res.geo is not None): 
                    return None
                gg = t.kit.processReferent("GEO", t.next0_)
                if (gg is not None or not ((isinstance(t.next0_, TextToken))) or t.is_newline_after): 
                    return None
                if (t.next0_.chars.is_all_upper or BracketHelper.canBeStartOfSequence(t.next0_, True, False)): 
                    pass
                else: 
                    return None
        if (res is not None or not ((isinstance(t, TextToken)))): 
            return res
        tt = Utils.asObjectOrNull(t, TextToken)
        term = tt.term
        if (tt.chars.is_all_upper and (((term == "CRM" or term == "IT" or term == "ECM") or term == "BPM" or term == "HR"))): 
            tt2 = t.next0_
            if (tt2 is not None and tt2.is_hiphen): 
                tt2 = tt2.next0_
            res = OrgItemTypeToken.__TryAttach(tt2, True)
            if (res is not None and res.root is not None and OrgProfile.UNIT in res.root.profiles): 
                res.name = "{0} {1}".format(Utils.ifNotNull(res.name, (res.root.canonic_text if res is not None and res.root is not None else None)), term)
                res.begin_token = t
                res.coef = 5
                return res
        if (term == "ВЧ"): 
            tt1 = t.next0_
            if (tt1 is not None and tt1.isValue("ПП", None)): 
                res = OrgItemTypeToken._new1720(t, tt1, 3)
            elif ((isinstance(tt1, NumberToken)) and (tt1.whitespaces_before_count < 3)): 
                res = OrgItemTypeToken(t, t)
            elif (MiscHelper.checkNumberPrefix(tt1) is not None): 
                res = OrgItemTypeToken(t, t)
            elif (((isinstance(tt1, TextToken)) and not tt1.is_whitespace_after and tt1.chars.is_letter) and tt1.length_char == 1): 
                res = OrgItemTypeToken(t, t)
            if (res is not None): 
                res.root = OrgItemTypeToken.__m_military_unit
                res.typ = OrgItemTypeToken.__m_military_unit.canonic_text.lower()
                res.profiles.append(OrgProfile.ARMY)
                return res
        if (term == "КБ"): 
            cou = 0
            ok = False
            ttt = t.next0_
            while ttt is not None and (cou < 30): 
                if (ttt.isValue("БАНК", None)): 
                    ok = True
                    break
                r = ttt.getReferent()
                if (r is not None and r.type_name == "URI"): 
                    vv = r.getStringValue("SCHEME")
                    if ((vv == "БИК" or vv == "Р/С" or vv == "К/С") or vv == "ОКАТО"): 
                        ok = True
                        break
                ttt = ttt.next0_; cou += 1
            if (ok): 
                res = OrgItemTypeToken(t, t)
                res.typ = "коммерческий банк"
                res.profiles.append(OrgProfile.FINANCE)
                res.coef = 3
                return res
        if (term == "ТП" or term == "МП"): 
            num = OrgItemNumberToken.tryAttach(t.next0_, True, None)
            if (num is not None and num.end_token.next0_ is not None): 
                tt1 = num.end_token.next0_
                if (tt1.is_comma and tt1.next0_ is not None): 
                    tt1 = tt1.next0_
                oo = Utils.asObjectOrNull(tt1.getReferent(), OrganizationReferent)
                if (oo is not None): 
                    if ("МИГРАЦ" in str(oo).upper()): 
                        res = OrgItemTypeToken._new1721(t, t, ("территориальный пункт" if term == "ТП" else "миграционный пункт"), 4, True)
                        return res
        if (tt.chars.is_all_upper and term == "МГТУ"): 
            if (tt.next0_.isValue("БАНК", None) or (((isinstance(tt.next0_.getReferent(), OrganizationReferent)) and (Utils.asObjectOrNull(tt.next0_.getReferent(), OrganizationReferent)).kind == OrganizationKind.BANK)) or ((tt.previous is not None and tt.previous.isValue("ОПЕРУ", None)))): 
                res = OrgItemTypeToken._new1722(tt, tt, "главное территориальное управление")
                res.alt_typ = "ГТУ"
                res.name = "МОСКОВСКОЕ"
                res.name_is_name = True
                res.alt_name = "МГТУ"
                res.coef = 3
                res.root = OrgItemTermin(res.name)
                res.profiles.append(OrgProfile.UNIT)
                tt.term = "МОСКОВСКИЙ"
                res.geo = tt.kit.processReferent("GEO", tt)
                tt.term = "МГТУ"
                return res
        if (tt.isValue("СОВЕТ", "РАДА")): 
            if (tt.next0_ is not None and tt.next0_.isValue("ПРИ", None)): 
                rt = tt.kit.processReferent("PERSONPROPERTY", tt.next0_.next0_)
                if (rt is not None): 
                    res = OrgItemTypeToken(tt, tt)
                    res.typ = "совет"
                    res.is_dep = True
                    res.coef = 2
                    return res
            if (tt.next0_ is not None and (isinstance(tt.next0_.getReferent(), GeoReferent)) and not tt.chars.is_all_lower): 
                res = OrgItemTypeToken(tt, tt)
                res.geo = (Utils.asObjectOrNull(tt.next0_, ReferentToken))
                res.typ = "совет"
                res.is_dep = True
                res.coef = 4
                res.profiles.append(OrgProfile.STATE)
                return res
        say = False
        if ((((term == "СООБЩАЕТ" or term == "СООБЩЕНИЮ" or term == "ПИШЕТ") or term == "ПЕРЕДАЕТ" or term == "ПОВІДОМЛЯЄ") or term == "ПОВІДОМЛЕННЯМ" or term == "ПИШЕ") or term == "ПЕРЕДАЄ"): 
            say = True
        if (((say or tt.isValue("ОБЛОЖКА", "ОБКЛАДИНКА") or tt.isValue("РЕДАКТОР", None)) or tt.isValue("КОРРЕСПОНДЕНТ", "КОРЕСПОНДЕНТ") or tt.isValue("ЖУРНАЛИСТ", "ЖУРНАЛІСТ")) or term == "ИНТЕРВЬЮ" or term == "ІНТЕРВЮ"): 
            if (OrgItemTypeToken.__m_pressru is None): 
                OrgItemTypeToken.__m_pressru = OrgItemTermin._new1723("ИЗДАНИЕ", MorphLang.RU, OrgProfile.MEDIA, True, 4)
            if (OrgItemTypeToken.__m_pressua is None): 
                OrgItemTypeToken.__m_pressua = OrgItemTermin._new1723("ВИДАННЯ", MorphLang.UA, OrgProfile.MEDIA, True, 4)
            pres = (OrgItemTypeToken.__m_pressua if tt.kit.base_language.is_ua else OrgItemTypeToken.__m_pressru)
            t1 = t.next0_
            if (t1 is None): 
                return None
            if (t1.chars.is_latin_letter and not t1.chars.is_all_lower): 
                if (tt.isValue("РЕДАКТОР", None)): 
                    return None
                return OrgItemTypeToken._new1725(t, t, pres.canonic_text.lower(), pres, True)
            if (not say): 
                br = BracketHelper.tryParse(t1, BracketParseAttr.NO, 100)
                if ((br is not None and br.is_quote_type and not t1.next0_.chars.is_all_lower) and ((br.end_char - br.begin_char) < 40)): 
                    return OrgItemTypeToken._new1725(t, t, pres.canonic_text.lower(), pres, True)
            npt = NounPhraseHelper.tryParse(t1, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_token.next0_ is not None): 
                t1 = npt.end_token.next0_
                root_ = npt.noun.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                ok = t1.chars.is_latin_letter and not t1.chars.is_all_lower
                if (not ok and BracketHelper.canBeStartOfSequence(t1, True, False)): 
                    ok = True
                if (ok): 
                    if ((root_ == "ИЗДАНИЕ" or root_ == "ИЗДАТЕЛЬСТВО" or root_ == "ЖУРНАЛ") or root_ == "ВИДАННЯ" or root_ == "ВИДАВНИЦТВО"): 
                        res = OrgItemTypeToken._new1722(npt.begin_token, npt.end_token, root_.lower())
                        res.profiles.append(OrgProfile.MEDIA)
                        res.profiles.append(OrgProfile.PRESS)
                        if (len(npt.adjectives) > 0): 
                            for a in npt.adjectives: 
                                rt1 = res.kit.processReferent("GEO", a.begin_token)
                                if (rt1 is not None and rt1.morph.class0_.is_adjective): 
                                    if (res.geo is None): 
                                        res.geo = rt1
                                    else: 
                                        res.geo2 = rt1
                            res.alt_typ = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False).lower()
                        res.root = OrgItemTermin._new1728(root_, True, 4)
                        return res
            rt = t1.kit.processReferent("GEO", t1)
            if (rt is not None and rt.morph.class0_.is_adjective): 
                if (rt.end_token.next0_ is not None and rt.end_token.next0_.chars.is_latin_letter): 
                    res = OrgItemTypeToken._new1729(t1, rt.end_token, pres.canonic_text.lower(), pres)
                    res.geo = rt
                    return res
            tt1 = t1
            if (BracketHelper.canBeStartOfSequence(tt1, True, False)): 
                tt1 = t1.next0_
            if ((((tt1.chars.is_latin_letter and tt1.next0_ is not None and tt1.next0_.isChar('.')) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.chars.is_latin_letter) and (tt1.next0_.next0_.length_char < 4) and tt1.next0_.next0_.length_char > 1) and not tt1.next0_.is_whitespace_after): 
                if (tt1 != t1 and not BracketHelper.canBeEndOfSequence(tt1.next0_.next0_.next0_, True, t1, False)): 
                    pass
                else: 
                    res = OrgItemTypeToken._new1729(t1, tt1.next0_.next0_, pres.canonic_text.lower(), pres)
                    res.name = MiscHelper.getTextValue(t1, tt1.next0_.next0_, GetTextAttr.NO).replace(" ", "")
                    if (tt1 != t1): 
                        res.end_token = res.end_token.next0_
                    res.coef = 4
                return res
        elif ((t.isValue("ЖУРНАЛ", None) or t.isValue("ИЗДАНИЕ", None) or t.isValue("ИЗДАТЕЛЬСТВО", None)) or t.isValue("ВИДАННЯ", None) or t.isValue("ВИДАВНИЦТВО", None)): 
            ok = False
            if (ad is not None): 
                ot_ex_li = ad.local_ontology.tryAttach(t.next0_, None, False)
                if (ot_ex_li is None and t.kit.ontology is not None): 
                    ot_ex_li = t.kit.ontology.attachToken(OrganizationReferent.OBJ_TYPENAME, t.next0_)
                if ((ot_ex_li is not None and len(ot_ex_li) > 0 and ot_ex_li[0].item is not None) and (isinstance(ot_ex_li[0].item.referent, OrganizationReferent))): 
                    if ((Utils.asObjectOrNull(ot_ex_li[0].item.referent, OrganizationReferent)).kind == OrganizationKind.PRESS): 
                        ok = True
            if (t.next0_ is not None and t.next0_.chars.is_latin_letter and not t.next0_.chars.is_all_lower): 
                ok = True
            if (ok): 
                res = OrgItemTypeToken._new1722(t, t, t.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False).lower())
                res.profiles.append(OrgProfile.MEDIA)
                res.profiles.append(OrgProfile.PRESS)
                res.root = OrgItemTermin._new1732(t.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False), OrgItemTermin.Types.ORG, 3, True)
                res.morph = t.morph
                res.chars = t.chars
                if (t.previous is not None and t.previous.morph.class0_.is_adjective): 
                    rt = t.kit.processReferent("GEO", t.previous)
                    if (rt is not None and rt.end_token == t.previous): 
                        res.begin_token = t.previous
                        res.geo = rt
                return res
        elif ((term == "МО" and t.chars.is_all_upper and (isinstance(t.next0_, ReferentToken))) and (isinstance(t.next0_.getReferent(), GeoReferent))): 
            geo_ = Utils.asObjectOrNull(t.next0_.getReferent(), GeoReferent)
            if (geo_ is not None and geo_.is_state): 
                res = OrgItemTypeToken._new1733(t, t, "министерство", "МИНИСТЕРСТВО ОБОРОНЫ", 4, OrgItemTypeToken.__m_mo)
                res.profiles.append(OrgProfile.STATE)
                res.can_be_organization = True
                return res
        elif (term == "ИК" and t.chars.is_all_upper): 
            et = None
            if (OrgItemNumberToken.tryAttach(t.next0_, False, None) is not None): 
                et = t
            elif (t.next0_ is not None and (isinstance(t.next0_, NumberToken))): 
                et = t
            elif ((t.next0_ is not None and t.next0_.is_hiphen and t.next0_.next0_ is not None) and (isinstance(t.next0_.next0_, NumberToken))): 
                et = t.next0_
            if (et is not None): 
                return OrgItemTypeToken._new1734(t, et, "исправительная колония", "колония", OrgItemTypeToken.__m_ispr_kolon, True)
        elif (t.isValue("ПАКЕТ", None) and t.next0_ is not None and t.next0_.isValue("АКЦИЯ", "АКЦІЯ")): 
            return OrgItemTypeToken._new1735(t, t.next0_, 4, True, "")
        else: 
            tok = OrgItemTypeToken._m_pref_words.tryParse(t, TerminParseAttr.NO)
            if (tok is not None and tok.tag is not None): 
                if ((tok.whitespaces_after_count < 2) and BracketHelper.canBeStartOfSequence(tok.end_token.next0_, True, False)): 
                    return OrgItemTypeToken._new1735(t, tok.end_token, 4, True, "")
        if (res is None and term == "АК" and t.chars.is_all_upper): 
            if (OrgItemTypeToken.tryAttach(t.next0_, can_be_first_letter_lower, ad) is not None): 
                return OrgItemTypeToken._new1737(t, t, OrgItemTypeToken.__m_akcion_comp, OrgItemTypeToken.__m_akcion_comp.canonic_text.lower())
        if (term == "В"): 
            if ((t.next0_ is not None and t.next0_.isCharOf("\\/") and t.next0_.next0_ is not None) and t.next0_.next0_.isValue("Ч", None)): 
                if (OrgItemNumberToken.tryAttach(t.next0_.next0_.next0_, True, None) is not None): 
                    return OrgItemTypeToken._new1737(t, t.next0_.next0_, OrgItemTypeToken.__m_military_unit, OrgItemTypeToken.__m_military_unit.canonic_text.lower())
        if (t.morph.class0_.is_adjective and t.next0_ is not None and ((t.next0_.chars.is_all_upper or t.next0_.chars.is_last_lower))): 
            if (t.chars.is_capital_upper or (((t.previous is not None and t.previous.is_hiphen and t.previous.previous is not None) and t.previous.previous.chars.is_capital_upper))): 
                res1 = OrgItemTypeToken.__TryAttach(t.next0_, True)
                if ((res1 is not None and res1.end_token == t.next0_ and res1.name is None) and res1.root is not None): 
                    res1.begin_token = t
                    res1.coef = 5
                    gen = MorphGender.UNDEFINED
                    for ii in range(len(res1.root.canonic_text) - 1, -1, -1):
                        if (ii == 0 or res1.root.canonic_text[ii - 1] == ' '): 
                            mm = Morphology.getWordBaseInfo(res1.root.canonic_text[ii:], MorphLang(), False, False)
                            gen = mm.gender
                            break
                    nam = t.getNormalCaseText(MorphClass.ADJECTIVE, True, gen, False)
                    if (((t.previous is not None and t.previous.is_hiphen and (isinstance(t.previous.previous, TextToken))) and t.previous.previous.chars.is_capital_upper and not t.is_whitespace_before) and not t.previous.is_whitespace_before): 
                        res1.begin_token = t.previous.previous
                        nam = "{0}-{1}".format((Utils.asObjectOrNull(res1.begin_token, TextToken)).term, nam)
                    res1.name = nam
                    return res1
        if (t.morph.class0_.is_adjective and not t.chars.is_all_lower and (t.whitespaces_after_count < 2)): 
            res1 = OrgItemTypeToken.__TryAttach(t.next0_, True)
            if ((res1 is not None and OrgProfile.TRANSPORT in res1.profiles and res1.name is None) and res1.root is not None): 
                nam = t.getNormalCaseText(MorphClass.ADJECTIVE, True, (MorphGender.FEMINIE if res1.root.canonic_text.endswith("ДОРОГА") else MorphGender.MASCULINE), False)
                if (nam is not None): 
                    if (((t.previous is not None and t.previous.is_hiphen and (isinstance(t.previous.previous, TextToken))) and t.previous.previous.chars.is_capital_upper and not t.is_whitespace_before) and not t.previous.is_whitespace_before): 
                        t = t.previous.previous
                        nam = "{0}-{1}".format((Utils.asObjectOrNull(t, TextToken)).term, nam)
                    res1.begin_token = t
                    res1.coef = 5
                    res1.name = "{0} {1}".format(nam, res1.root.canonic_text)
                    res1.can_be_organization = True
                    return res1
        return res
    
    __m_pressru = None
    
    __m_pressua = None
    
    __m_pressia = None
    
    __m_military_unit = None
    
    @staticmethod
    def __TryAttach(t : 'Token', can_be_first_letter_lower : bool) -> 'OrgItemTypeToken':
        from pullenti.ner.org.internal.OrgItemTermin import OrgItemTermin
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (t is None): 
            return None
        li = OrgItemTypeToken.__m_global.tryAttach(t, None, False)
        if (li is not None): 
            if (t.previous is not None and t.previous.is_hiphen and not t.is_whitespace_before): 
                li1 = OrgItemTypeToken.__m_global.tryAttach(t.previous.previous, None, False)
                if (li1 is not None and li1[0].end_token == li[0].end_token): 
                    return None
            res = OrgItemTypeToken(li[0].begin_token, li[0].end_token)
            res.root = (Utils.asObjectOrNull(li[0].termin, OrgItemTermin))
            nn = NounPhraseHelper.tryParse(li[0].begin_token, NounPhraseParseAttr.NO, 0)
            if (nn is not None and ((nn.end_token.next0_ is None or not nn.end_token.next0_.isChar('.')))): 
                res.morph = nn.morph
            else: 
                res.morph = li[0].morph
            res.chars_root = res.chars
            if (res.root.is_pure_prefix): 
                res.typ = res.root.acronym
                if (res.typ is None): 
                    res.typ = res.root.canonic_text.lower()
            else: 
                res.typ = res.root.canonic_text.lower()
            if (res.begin_token != res.end_token and not res.root.is_pure_prefix): 
                npt0 = NounPhraseHelper.tryParse(res.begin_token, NounPhraseParseAttr.NO, 0)
                if (npt0 is not None and npt0.end_token == res.end_token and len(npt0.adjectives) >= res.name_words_count): 
                    s = npt0.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False)
                    if (Utils.compareStrings(s, res.typ, True) != 0): 
                        res.name = s
                        res.can_be_organization = True
            if (res.typ == "сберегательный банк" and res.name is None): 
                res.name = res.typ.upper()
                res.typ = "банк"
            if (res.is_dep and res.typ.startswith("отдел ") and res.name is None): 
                res.name = res.typ.upper()
                res.typ = "отдел"
            if (res.begin_token == res.end_token): 
                if (res.chars.is_capital_upper): 
                    if ((res.length_char < 4) and not res.begin_token.isValue(res.root.canonic_text, None)): 
                        if (not can_be_first_letter_lower): 
                            return None
                if (res.chars.is_all_upper): 
                    if (res.begin_token.isValue("САН", None)): 
                        return None
            if (res.end_token.next0_ is not None and res.end_token.next0_.isChar('(')): 
                li22 = OrgItemTypeToken.__m_global.tryAttach(res.end_token.next0_.next0_, None, False)
                if ((li22 is not None and len(li22) > 0 and li22[0].termin == li[0].termin) and li22[0].end_token.next0_ is not None and li22[0].end_token.next0_.isChar(')')): 
                    res.end_token = li22[0].end_token.next0_
            return res
        if ((isinstance(t, NumberToken)) and t.morph.class0_.is_adjective): 
            pass
        elif (isinstance(t, TextToken)): 
            pass
        else: 
            return None
        if (t.isValue("СБ", None)): 
            if (t.next0_ is not None and (isinstance(t.next0_.getReferent(), GeoReferent))): 
                return OrgItemTypeToken._new1739(t, t, "банк", OrgItemTypeToken.__m_sber_bank, OrgItemTypeToken.__m_sber_bank.canonic_text)
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.IGNOREADJBEST, 0)
        if (npt is None or npt.internal_noun is not None): 
            if (((not t.chars.is_all_lower and t.next0_ is not None and t.next0_.is_hiphen) and not t.is_whitespace_after and not t.next0_.is_whitespace_after) and t.next0_.next0_ is not None and t.next0_.next0_.isValue("БАНК", None)): 
                s = t.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                res = OrgItemTypeToken._new1740(t, t.next0_.next0_, s, t.next0_.next0_.morph, t.chars, t.next0_.next0_.chars)
                res.root = OrgItemTypeToken.__m_bank
                res.typ = "банк"
                return res
            if ((isinstance(t, NumberToken)) and (t.whitespaces_after_count < 3) and (isinstance(t.next0_, TextToken))): 
                res11 = OrgItemTypeToken.__TryAttach(t.next0_, False)
                if (res11 is not None and res11.root is not None and res11.root.can_has_number): 
                    res11.begin_token = t
                    res11.number = str((Utils.asObjectOrNull(t, NumberToken)).value)
                    res11.coef = res11.coef + (1)
                    return res11
            return None
        if (npt.morph.gender == MorphGender.FEMINIE and npt.noun.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False) == "БАНКА"): 
            return None
        if (npt.begin_token == npt.end_token): 
            s = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
            if (LanguageHelper.endsWithEx(s, "БАНК", "БАНКА", "БАНОК", None)): 
                if (LanguageHelper.endsWith(s, "БАНКА")): 
                    s = s[0:0+len(s) - 1]
                elif (LanguageHelper.endsWith(s, "БАНОК")): 
                    s = (s[0:0+len(s) - 2] + "К")
                res = OrgItemTypeToken._new1740(npt.begin_token, npt.end_token, s, npt.morph, npt.chars, npt.chars)
                res.root = OrgItemTypeToken.__m_bank
                res.typ = "банк"
                return res
            return None
        tt = npt.end_token
        first_pass3060 = True
        while True:
            if first_pass3060: first_pass3060 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (tt == npt.begin_token): 
                break
            lii = OrgItemTypeToken.__m_global.tryAttach(tt, None, False)
            if (lii is not None): 
                if (tt == npt.end_token and tt.previous is not None and tt.previous.is_hiphen): 
                    continue
                li = lii
                if (li[0].end_char < npt.end_char): 
                    npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.IGNOREADJBEST, li[0].end_char)
                break
        if (li is None or npt is None): 
            return None
        res = OrgItemTypeToken(npt.begin_token, li[0].end_token)
        for a in npt.adjectives: 
            if (a.isValue("ДОЧЕРНИЙ", None) or a.isValue("ДОЧІРНІЙ", None)): 
                res.is_douter_org = True
                break
        for em in OrgItemTypeToken.M_EMPTY_TYP_WORDS: 
            for a in npt.adjectives: 
                if (a.isValue(em, None)): 
                    npt.adjectives.remove(a)
                    break
        while len(npt.adjectives) > 0:
            if (npt.adjectives[0].begin_token.getMorphClassInDictionary().is_verb): 
                del npt.adjectives[0]
            elif (isinstance(npt.adjectives[0].begin_token, NumberToken)): 
                res.number = str((Utils.asObjectOrNull(npt.adjectives[0].begin_token, NumberToken)).value)
                del npt.adjectives[0]
            else: 
                break
        if (len(npt.adjectives) > 0): 
            res.alt_typ = npt.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False)
            if (li[0].end_char > npt.end_char): 
                res.alt_typ = "{0} {1}".format(res.alt_typ, MiscHelper.getTextValue(npt.end_token.next0_, li[0].end_token, GetTextAttr.NO))
        if (res.number is None): 
            while len(npt.adjectives) > 0:
                if (not npt.adjectives[0].chars.is_all_lower or can_be_first_letter_lower): 
                    break
                if (npt.kit.processReferent("GEO", npt.adjectives[0].begin_token) is not None): 
                    break
                if (OrgItemTypeToken.isStdAdjective(npt.adjectives[0], False)): 
                    break
                bad = False
                if (not npt.noun.chars.is_all_lower or not OrgItemTypeToken.isStdAdjective(npt.adjectives[0], False)): 
                    bad = True
                else: 
                    i = 1
                    first_pass3061 = True
                    while True:
                        if first_pass3061: first_pass3061 = False
                        else: i += 1
                        if (not (i < len(npt.adjectives))): break
                        if (npt.kit.processReferent("GEO", npt.adjectives[i].begin_token) is not None): 
                            continue
                        if (not npt.adjectives[i].chars.is_all_lower): 
                            bad = True
                            break
                if (not bad): 
                    break
                del npt.adjectives[0]
        for a in npt.adjectives: 
            r = npt.kit.processReferent("GEO", a.begin_token)
            if (r is not None): 
                if (a == npt.adjectives[0]): 
                    res2 = OrgItemTypeToken.__TryAttach(a.end_token.next0_, True)
                    if (res2 is not None and res2.end_char > npt.end_char and res2.geo is None): 
                        res2.begin_token = a.begin_token
                        res2.geo = r
                        return res2
                if (res.geo is None): 
                    res.geo = r
                elif (res.geo2 is None): 
                    res.geo2 = r
        if (res.end_token == npt.end_token): 
            res.name = npt.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False)
        if (res.name == res.alt_typ): 
            res.alt_typ = (None)
        if (res.alt_typ is not None): 
            res.alt_typ = res.alt_typ.lower().replace('-', ' ')
        res.root = (Utils.asObjectOrNull(li[0].termin, OrgItemTermin))
        if (res.root.is_pure_prefix and (li[0].length_char < 7)): 
            return None
        res.typ = res.root.canonic_text.lower()
        if (len(npt.adjectives) > 0): 
            i = 0
            while i < len(npt.adjectives): 
                s = npt.getNormalCaseTextWithoutAdjective(i)
                ctli = OrgItemTypeToken.__m_global.findTerminByCanonicText(s)
                if (ctli is not None and len(ctli) > 0 and (isinstance(ctli[0], OrgItemTermin))): 
                    res.root = (Utils.asObjectOrNull(ctli[0], OrgItemTermin))
                    if (res.alt_typ is None): 
                        res.alt_typ = res.root.canonic_text.lower()
                        if (res.alt_typ == res.typ): 
                            res.alt_typ = (None)
                    break
                i += 1
            res.coef = res.root.coeff
            if (res.coef == 0): 
                i = 0
                while i < len(npt.adjectives): 
                    if (OrgItemTypeToken.isStdAdjective(npt.adjectives[i], True)): 
                        res.coef = res.coef + (1)
                        if (((i + 1) < len(npt.adjectives)) and not OrgItemTypeToken.isStdAdjective(npt.adjectives[i + 1], False)): 
                            res.coef = res.coef + (1)
                        if (npt.adjectives[i].isValue("ФЕДЕРАЛЬНЫЙ", "ФЕДЕРАЛЬНИЙ") or npt.adjectives[i].isValue("ГОСУДАРСТВЕННЫЙ", "ДЕРЖАВНИЙ")): 
                            res.is_doubt_root_word = False
                            if (res.is_dep): 
                                res.is_dep = False
                    elif (OrgItemTypeToken.isStdAdjective(npt.adjectives[i], False)): 
                        res.coef = res.coef + .5
                    i += 1
            else: 
                i = 0
                while i < (len(npt.adjectives) - 1): 
                    if (OrgItemTypeToken.isStdAdjective(npt.adjectives[i], True)): 
                        if (((i + 1) < len(npt.adjectives)) and not OrgItemTypeToken.isStdAdjective(npt.adjectives[i + 1], True)): 
                            res.coef = res.coef + (1)
                            res.is_doubt_root_word = False
                            res.can_be_organization = True
                            if (res.is_dep): 
                                res.is_dep = False
                    i += 1
        res.morph = npt.morph
        res.chars = npt.chars
        if (not res.chars.is_all_upper and not res.chars.is_capital_upper and not res.chars.is_all_lower): 
            res.chars = npt.noun.chars
            if (res.chars.is_all_lower): 
                res.chars = res.begin_token.chars
        if (npt.noun is not None): 
            res.chars_root = npt.noun.chars
        return res
    
    @staticmethod
    def isStdAdjective(t : 'Token', only_federal : bool=False) -> bool:
        if (t is None): 
            return False
        if (t.morph.language.is_ua): 
            for a in OrgItemTypeToken.__m_org_adjactivesua: 
                if (t.isValue(a, None)): 
                    return True
            if (not only_federal): 
                for a in OrgItemTypeToken.__m_org_adjactives2ua: 
                    if (t.isValue(a, None)): 
                        return True
        else: 
            for a in OrgItemTypeToken.__m_org_adjactives: 
                if (t.isValue(a, None)): 
                    return True
            if (not only_federal): 
                for a in OrgItemTypeToken.__m_org_adjactives2: 
                    if (t.isValue(a, None)): 
                        return True
        return False
    
    __m_org_adjactives = None
    
    __m_org_adjactivesua = None
    
    __m_org_adjactives2 = None
    
    __m_org_adjactives2ua = None
    
    @staticmethod
    def checkOrgSpecialWordBefore(t : 'Token') -> bool:
        """ Проверка, что перед токеном есть специфическое слово типа "Президент" и т.п.
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return False
        if (t.is_comma_and and t.previous is not None): 
            t = t.previous
        k = 0
        tt = t
        first_pass3062 = True
        while True:
            if first_pass3062: first_pass3062 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            r = tt.getReferent()
            if (r is not None): 
                if (tt == t and (isinstance(r, OrganizationReferent))): 
                    return True
                return False
            if (not ((isinstance(tt, TextToken)))): 
                if (not ((isinstance(tt, NumberToken)))): 
                    break
                k += 1
                continue
            if (tt.is_newline_after): 
                if (not tt.isChar(',')): 
                    return False
                continue
            if (tt.isValue("УПРАВЛЕНИЕ", None) or tt.isValue("УПРАВЛІННЯ", None)): 
                ty = OrgItemTypeToken.tryAttach(tt.next0_, True, None)
                if (ty is not None and ty.is_doubt_root_word): 
                    return False
            if (tt == t and OrgItemTypeToken._m_pref_words.tryParse(tt, TerminParseAttr.NO) is not None): 
                return True
            if (tt == t and tt.isChar('.')): 
                continue
            ty = OrgItemTypeToken.tryAttach(tt, True, None)
            if (ty is not None and ty.end_token.end_char <= t.end_char and ty.end_token == t): 
                if (not ty.is_doubt_root_word): 
                    return True
            if (tt.kit.recurse_level == 0): 
                rt = tt.kit.processReferent("PERSONPROPERTY", tt)
                if (rt is not None and rt.referent is not None and rt.referent.type_name == "PERSONPROPERTY"): 
                    if (rt.end_char >= t.end_char): 
                        return True
            k += 1
            if (k > 4): 
                break
        return False
    
    @staticmethod
    def checkPersonProperty(t : 'Token') -> bool:
        if (t is None or not t.chars.is_cyrillic_letter): 
            return False
        tok = OrgItemTypeToken._m_pref_words.tryParse(t, TerminParseAttr.NO)
        if (tok is None): 
            return False
        if (tok.termin.tag is None): 
            return False
        return True
    
    @staticmethod
    def tryAttachReferenceToExistOrg(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        if (not ((isinstance(t, TextToken)))): 
            return None
        tok = OrgItemTypeToken._m_key_words_for_refs.tryParse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_pronoun): 
            tok = OrgItemTypeToken._m_key_words_for_refs.tryParse(t.next0_, TerminParseAttr.NO)
        abbr = None
        if (tok is None): 
            if (t.length_char > 1 and ((t.chars.is_capital_upper or t.chars.is_last_lower))): 
                abbr = (Utils.asObjectOrNull(t, TextToken)).getLemma()
            else: 
                ty1 = OrgItemTypeToken.__TryAttach(t, True)
                if (ty1 is not None): 
                    abbr = ty1.typ
                else: 
                    return None
        cou = 0
        tt = t.previous
        first_pass3063 = True
        while True:
            if first_pass3063: first_pass3063 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (tt.is_newline_after): 
                cou += 10
            cou += 1
            if (cou > 500): 
                break
            if (not ((isinstance(tt, ReferentToken)))): 
                continue
            refs = tt.getReferents()
            if (refs is None): 
                continue
            for r in refs: 
                if (isinstance(r, OrganizationReferent)): 
                    if (abbr is not None): 
                        if (r.findSlot(OrganizationReferent.ATTR_TYPE, abbr, True) is None): 
                            continue
                        rt = ReferentToken(r, t, t)
                        hi = Utils.asObjectOrNull(r.getSlotValue(OrganizationReferent.ATTR_HIGHER), OrganizationReferent)
                        if (hi is not None and t.next0_ is not None): 
                            for ty in hi.types: 
                                if (t.next0_.isValue(ty.upper(), None)): 
                                    rt.end_token = t.next0_
                                    break
                        return rt
                    if (tok.termin.tag is not None): 
                        ok = False
                        for ty in (Utils.asObjectOrNull(r, OrganizationReferent)).types: 
                            if (Utils.endsWithString(ty, tok.termin.canonic_text, True)): 
                                ok = True
                                break
                        if (not ok): 
                            continue
                    return ReferentToken(r, t, tok.end_token)
        return None
    
    @staticmethod
    def isTypesAntagonisticOO(r1 : 'OrganizationReferent', r2 : 'OrganizationReferent') -> bool:
        k1 = r1.kind
        k2 = r2.kind
        if (k1 != OrganizationKind.UNDEFINED and k2 != OrganizationKind.UNDEFINED): 
            if (OrgItemTypeToken.isTypesAntagonisticKK(k1, k2)): 
                return True
        types1 = r1.types
        types2 = r2.types
        for t1 in types1: 
            if (t1 in types2): 
                return False
        for t1 in types1: 
            for t2 in types2: 
                if (OrgItemTypeToken.isTypesAntagonisticSS(t1, t2)): 
                    return True
        return False
    
    @staticmethod
    def isTypeAccords(r1 : 'OrganizationReferent', t2 : 'OrgItemTypeToken') -> bool:
        if (t2 is None or t2.typ is None): 
            return False
        if (t2.typ == "министерство" or t2.typ == "міністерство" or t2.typ.endswith("штаб")): 
            return r1.findSlot(OrganizationReferent.ATTR_TYPE, t2.typ, True) is not None
        prs = r1.profiles
        for pr in prs: 
            if (pr in t2.profiles): 
                return True
        if (r1.findSlot(OrganizationReferent.ATTR_TYPE, None, True) is None): 
            if (len(prs) == 0): 
                return True
        if (len(t2.profiles) == 0): 
            if (OrgProfile.POLICY in prs): 
                if (t2.typ == "группа" or t2.typ == "организация"): 
                    return True
            if (OrgProfile.MUSIC in prs): 
                if (t2.typ == "группа"): 
                    return True
        for t in r1.types: 
            if (t == t2.typ): 
                return True
            if (t.endswith(t2.typ)): 
                return True
            if (t2.typ == "издание"): 
                if (t.endswith("агентство")): 
                    return True
        if ((t2.typ == "компания" or t2.typ == "корпорация" or t2.typ == "company") or t2.typ == "corporation"): 
            if (len(prs) == 0): 
                return True
            if (OrgProfile.BUSINESS in prs or OrgProfile.FINANCE in prs or OrgProfile.INDUSTRY in prs): 
                return True
        return False
    
    @staticmethod
    def isTypesAntagonisticTT(t1 : 'OrgItemTypeToken', t2 : 'OrgItemTypeToken') -> bool:
        k1 = OrgItemTypeToken._getKind(t1.typ, Utils.ifNotNull(t1.name, ""), None)
        k2 = OrgItemTypeToken._getKind(t2.typ, Utils.ifNotNull(t2.name, ""), None)
        if (k1 == OrganizationKind.JUSTICE and t2.typ.startswith("Ф")): 
            return False
        if (k2 == OrganizationKind.JUSTICE and t1.typ.startswith("Ф")): 
            return False
        if (OrgItemTypeToken.isTypesAntagonisticKK(k1, k2)): 
            return True
        if (OrgItemTypeToken.isTypesAntagonisticSS(t1.typ, t2.typ)): 
            return True
        if (k1 == OrganizationKind.BANK and k2 == OrganizationKind.BANK): 
            if (t1.name is not None and t2.name is not None and t1 != t2): 
                return True
        return False
    
    @staticmethod
    def isTypesAntagonisticSS(typ1 : str, typ2 : str) -> bool:
        if (typ1 == typ2): 
            return False
        uni = "{0} {1} ".format(typ1, typ2)
        if (("служба" in uni or "департамент" in uni or "инспекция" in uni) or "інспекція" in uni): 
            return True
        if ("министерство" in uni or "міністерство" in uni): 
            return True
        if ("правительство" in uni and not "администрация" in uni): 
            return True
        if ("уряд" in uni and not "адміністрація" in uni): 
            return True
        if (typ1 == "управление" and ((typ2 == "главное управление" or typ2 == "пограничное управление"))): 
            return True
        if (typ2 == "управление" and ((typ1 == "главное управление" or typ2 == "пограничное управление"))): 
            return True
        if (typ1 == "керування" and typ2 == "головне управління"): 
            return True
        if (typ2 == "керування" and typ1 == "головне управління"): 
            return True
        if (typ1 == "university"): 
            if (typ2 == "school" or typ2 == "college"): 
                return True
        if (typ2 == "university"): 
            if (typ1 == "school" or typ1 == "college"): 
                return True
        return False
    
    @staticmethod
    def isTypesAntagonisticKK(k1 : 'OrganizationKind', k2 : 'OrganizationKind') -> bool:
        if (k1 == k2): 
            return False
        if (k1 == OrganizationKind.DEPARTMENT or k2 == OrganizationKind.DEPARTMENT): 
            return False
        if (k1 == OrganizationKind.GOVENMENT or k2 == OrganizationKind.GOVENMENT): 
            return True
        if (k1 == OrganizationKind.JUSTICE or k2 == OrganizationKind.JUSTICE): 
            return True
        if (k1 == OrganizationKind.PARTY or k2 == OrganizationKind.PARTY): 
            return True
        if (k1 == OrganizationKind.STUDY): 
            k1 = OrganizationKind.SCIENCE
        if (k2 == OrganizationKind.STUDY): 
            k2 = OrganizationKind.SCIENCE
        if (k1 == OrganizationKind.PRESS): 
            k1 = OrganizationKind.MEDIA
        if (k2 == OrganizationKind.PRESS): 
            k2 = OrganizationKind.MEDIA
        if (k1 == k2): 
            return False
        if (k1 == OrganizationKind.UNDEFINED or k2 == OrganizationKind.UNDEFINED): 
            return False
        return True
    
    @staticmethod
    def checkKind(obj : 'OrganizationReferent') -> 'OrganizationKind':
        t = io.StringIO()
        n = io.StringIO()
        for s in obj.slots: 
            if (s.type_name == OrganizationReferent.ATTR_NAME): 
                print("{0};".format(s.value), end="", file=n, flush=True)
            elif (s.type_name == OrganizationReferent.ATTR_TYPE): 
                print("{0};".format(s.value), end="", file=t, flush=True)
        return OrgItemTypeToken._getKind(Utils.toStringStringIO(t), Utils.toStringStringIO(n), obj)
    
    @staticmethod
    def _getKind(t : str, n : str, r : 'OrganizationReferent'=None) -> 'OrganizationKind':
        if (not LanguageHelper.endsWith(t, ";")): 
            t += ";"
        if ((((((((((((("министерство" in t or "правительство" in t or "администрация" in t) or "префектура" in t or "мэрия;" in t) or "муниципалитет" in t or LanguageHelper.endsWith(t, "совет;")) or "дума;" in t or "собрание;" in t) or "кабинет" in t or "сенат;" in t) or "палата" in t or "рада;" in t) or "парламент;" in t or "конгресс" in t) or "комиссия" in t or "полиция;" in t) or "милиция;" in t or "хурал" in t) or "суглан" in t or "меджлис;" in t) or "хасе;" in t or "ил тумэн" in t) or "курултай" in t or "бундестаг" in t) or "бундесрат" in t): 
            return OrganizationKind.GOVENMENT
        if (((((((((((("міністерство" in t or "уряд" in t or "адміністрація" in t) or "префектура" in t or "мерія;" in t) or "муніципалітет" in t or LanguageHelper.endsWith(t, "рада;")) or "дума;" in t or "збори" in t) or "кабінет;" in t or "сенат;" in t) or "палата" in t or "рада;" in t) or "парламент;" in t or "конгрес" in t) or "комісія" in t or "поліція;" in t) or "міліція;" in t or "хурал" in t) or "суглан" in t or "хасе;" in t) or "іл тумен" in t or "курултай" in t) or "меджліс;" in t): 
            return OrganizationKind.GOVENMENT
        if ("комитет" in t or "комітет" in t): 
            if (r is not None and r.higher is not None and r.higher.kind == OrganizationKind.PARTY): 
                return OrganizationKind.DEPARTMENT
            return OrganizationKind.GOVENMENT
        if ("штаб;" in t): 
            if (r is not None and r.higher is not None and r.higher.kind == OrganizationKind.MILITARY): 
                return OrganizationKind.MILITARY
            return OrganizationKind.GOVENMENT
        tn = t
        if (not Utils.isNullOrEmpty(n)): 
            tn += n
        tn = tn.lower()
        if ((((("служба;" in t or "инспекция;" in t or "управление;" in t) or "департамент" in t or "комитет;" in t) or "комиссия;" in t or "інспекція;" in t) or "керування;" in t or "комітет;" in t) or "комісія;" in t): 
            if ("федеральн" in tn or "государствен" in tn or "державн" in tn): 
                return OrganizationKind.GOVENMENT
            if (r is not None and r.findSlot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                if (r.higher is None and r._m_temp_parent_org is None): 
                    if (not "управление;" in t and not "департамент" in t and not "керування;" in t): 
                        return OrganizationKind.GOVENMENT
        if ((((((((((((((((((((((((((((((((("подразделение" in t or "отдел;" in t or "отдел " in t) or "направление" in t or "отделение" in t) or "кафедра" in t or "инспекция" in t) or "факультет" in t or "лаборатория" in t) or "пресс центр" in t or "пресс служба" in t) or "сектор " in t or t == "группа;") or (("курс;" in t and not "конкурс" in t)) or "филиал" in t) or "главное управление" in t or "пограничное управление" in t) or "главное территориальное управление" in t or "бухгалтерия" in t) or "магистратура" in t or "аспирантура" in t) or "докторантура" in t or "дирекция" in t) or "руководство" in t or "правление" in t) or "пленум;" in t or "президиум" in t) or "стол;" in t or "совет директоров" in t) or "ученый совет" in t or "коллегия" in t) or "аппарат" in t or "представительство" in t) or "жюри;" in t or "підрозділ" in t) or "відділ;" in t or "відділ " in t) or "напрямок" in t or "відділення" in t) or "інспекція" in t or t == "група;") or "лабораторія" in t or "прес центр" in t) or "прес служба" in t or "філія" in t) or "головне управління" in t or "головне територіальне управління" in t) or "бухгалтерія" in t or "магістратура" in t) or "аспірантура" in t or "докторантура" in t) or "дирекція" in t or "керівництво" in t) or "правління" in t or "президія" in t) or "стіл" in t or "рада директорів" in t) or "вчена рада" in t or "колегія" in t) or "апарат" in t or "представництво" in t) or "журі;" in t or "фракция" in t) or "депутатская группа" in t or "фракція" in t) or "депутатська група" in t): 
            return OrganizationKind.DEPARTMENT
        if (("научн" in t or "исследовательск" in t or "науков" in t) or "дослідн" in t): 
            return OrganizationKind.SCIENCE
        if ("агенство" in t or "агентство" in t): 
            if ("федеральн" in tn or "державн" in tn): 
                return OrganizationKind.GOVENMENT
            if ("информацион" in tn or "інформаційн" in tn): 
                return OrganizationKind.PRESS
        if ("холдинг" in t or "группа компаний" in t or "група компаній" in t): 
            return OrganizationKind.HOLDING
        if ("академия" in t or "академія" in t): 
            if ("наук" in tn): 
                return OrganizationKind.SCIENCE
            return OrganizationKind.STUDY
        if (((((((((("школа;" in t or "университет" in t or "учебный " in tn) or "лицей" in t or "колледж" in t) or "детский сад" in t or "училище" in t) or "гимназия" in t or "семинария" in t) or "образовательн" in t or "интернат" in t) or "університет" in t or "навчальний " in tn) or "ліцей" in t or "коледж" in t) or "дитячий садок" in t or "училище" in t) or "гімназія" in t or "семінарія" in t) or "освітн" in t or "інтернат" in t): 
            return OrganizationKind.STUDY
        if ((("больница" in t or "поликлиника" in t or "клиника" in t) or "госпиталь" in t or "санитарн" in tn) or "медико" in tn or "медицин" in tn): 
            return OrganizationKind.MEDICAL
        if (((((("церковь" in t or "храм;" in t or "собор" in t) or "синагога" in t or "мечеть" in t) or "лавра" in t or "монастырь" in t) or "церква" in t or "монастир" in t) or "патриархия" in t or "епархия" in t) or "патріархія" in t or "єпархія" in t): 
            return OrganizationKind.CHURCH
        if ("департамент" in t or "управление" in t or "керування" in t): 
            if (r is not None): 
                if (r.findSlot(OrganizationReferent.ATTR_HIGHER, None, True) is not None): 
                    return OrganizationKind.DEPARTMENT
        if (("академия" in t or "институт" in t or "академія" in t) or "інститут" in t): 
            if (n is not None and ((("НАУК" in n or "НАУЧН" in n or "НАУКОВ" in n) or "ИССЛЕДОВАТ" in n or "ДОСЛІДН" in n))): 
                return OrganizationKind.SCIENCE
        if ("аэропорт" in t or "аеропорт" in t): 
            return OrganizationKind.AIRPORT
        if ((("фестиваль" in t or "чемпионат" in t or "олимпиада" in t) or "конкурс" in t or "чемпіонат" in t) or "олімпіада" in t): 
            return OrganizationKind.FESTIVAL
        if ((((((((("армия" in t or "генеральный штаб" in t or "войсковая часть" in t) or "армія" in t or "генеральний штаб" in t) or "військова частина" in t or "дивизия" in t) or "полк" in t or "батальон" in t) or "рота" in t or "взвод" in t) or "дивізія" in t or "батальйон" in t) or "гарнизон" in t or "гарнізон" in t) or "бригада" in t or "корпус" in t) or "дивизион" in t or "дивізіон" in t): 
            return OrganizationKind.MILITARY
        if ((("партия" in t or "движение" in t or "группировка" in t) or "партія" in t or "рух;" in t) or "групування" in t): 
            return OrganizationKind.PARTY
        if ((((((("газета" in t or "издательство" in t or "информационное агентство" in t) or "риа;" in tn or "журнал" in t) or "издание" in t or "еженедельник" in t) or "таблоид" in t or "видавництво" in t) or "інформаційне агентство" in t or "журнал" in t) or "видання" in t or "тижневик" in t) or "таблоїд" in t or "портал" in t): 
            return OrganizationKind.PRESS
        if ((("телеканал" in t or "телекомпания" in t or "радиостанция" in t) or "киностудия" in t or "телекомпанія" in t) or "радіостанція" in t or "кіностудія" in t): 
            return OrganizationKind.MEDIA
        if ((("завод;" in t or "фабрика" in t or "комбинат" in t) or "производитель" in t or "комбінат" in t) or "виробник" in t): 
            return OrganizationKind.FACTORY
        if (((((("театр;" in t or "концертный зал" in t or "музей" in t) or "консерватория" in t or "филармония" in t) or "галерея" in t or "театр студия" in t) or "дом культуры" in t or "концертний зал" in t) or "консерваторія" in t or "філармонія" in t) or "театр студія" in t or "будинок культури" in t): 
            return OrganizationKind.CULTURE
        if ((((((("федерация" in t or "союз" in t or "объединение" in t) or "фонд;" in t or "ассоциация" in t) or "клуб" in t or "альянс" in t) or "ассамблея" in t or "федерація" in t) or "обєднання" in t or "фонд;" in t) or "асоціація" in t or "асамблея" in t) or "гильдия" in t or "гільдія" in t): 
            return OrganizationKind.FEDERATION
        if (((((("пансионат" in t or "санаторий" in t or "дом отдыха" in t) or "база отдыха" in t or "гостиница" in t) or "отель" in t or "лагерь" in t) or "пансіонат" in t or "санаторій" in t) or "будинок відпочинку" in t or "база відпочинку" in t) or "готель" in t or "табір" in t): 
            return OrganizationKind.HOTEL
        if (((((("суд;" in t or "колония" in t or "изолятор" in t) or "тюрьма" in t or "прокуратура" in t) or "судебный" in t or "трибунал" in t) or "колонія" in t or "ізолятор" in t) or "вязниця" in t or "судовий" in t) or "трибунал" in t): 
            return OrganizationKind.JUSTICE
        if ("банк" in tn or "казначейство" in tn): 
            return OrganizationKind.BANK
        if ("торгов" in tn or "магазин" in tn or "маркет;" in tn): 
            return OrganizationKind.TRADE
        if ("УЗ;" in t): 
            return OrganizationKind.MEDICAL
        if ("центр;" in t): 
            if (("диагностический" in tn or "медицинский" in tn or "діагностичний" in tn) or "медичний" in tn): 
                return OrganizationKind.MEDICAL
            if ((isinstance(r, OrganizationReferent)) and (Utils.asObjectOrNull(r, OrganizationReferent)).higher is not None): 
                if ((Utils.asObjectOrNull(r, OrganizationReferent)).higher.kind == OrganizationKind.DEPARTMENT): 
                    return OrganizationKind.DEPARTMENT
        if ("часть;" in t or "частина;" in t): 
            return OrganizationKind.DEPARTMENT
        if (r is not None): 
            if (r.containsProfile(OrgProfile.POLICY)): 
                return OrganizationKind.PARTY
            if (r.containsProfile(OrgProfile.MEDIA)): 
                return OrganizationKind.MEDIA
        return OrganizationKind.UNDEFINED
    
    __m_global = None
    
    __m_bank = None
    
    __m_mo = None
    
    __m_ispr_kolon = None
    
    __m_sber_bank = None
    
    __m_akcion_comp = None
    
    __m_sovm_pred = None
    
    _m_pref_words = None
    
    _m_key_words_for_refs = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.org.internal.OrgItemTermin import OrgItemTermin
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.TerminCollection import TerminCollection
        if (OrgItemTypeToken.__m_global is not None): 
            return
        OrgItemTypeToken.__m_global = IntOntologyCollection()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        tdat = EpNerOrgInternalResourceHelper.getBytes("OrgTypes.dat")
        if (tdat is None): 
            raise Utils.newException("Can't file resource file OrgTypes.dat in Organization analyzer", None)
        tdat = OrgItemTypeToken._deflate(tdat)
        with io.BytesIO(tdat) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(tmp)
            set0_ = None
            for x in xml0_.getroot(): 
                its = OrgItemTermin.deserializeSrc(x, set0_)
                if (x.tag == "set"): 
                    set0_ = (None)
                    if (its is not None and len(its) > 0): 
                        set0_ = its[0]
                elif (its is not None): 
                    for ii in its: 
                        OrgItemTypeToken.__m_global.add(ii)
        sovs = ["СОВЕТ БЕЗОПАСНОСТИ", "НАЦИОНАЛЬНЫЙ СОВЕТ", "ГОСУДАРСТВЕННЫЙ СОВЕТ", "ОБЛАСТНОЙ СОВЕТ", "РАЙОННЫЙ СОВЕТ", "ГОРОДСКОЙ СОВЕТ", "СЕЛЬСКИЙ СОВЕТ", "КРАЕВОЙ СОВЕТ", "СЛЕДСТВЕННЫЙ КОМИТЕТ", "СЛЕДСТВЕННОЕ УПРАВЛЕНИЕ", "ГОСУДАРСТВЕННОЕ СОБРАНИЕ", "МУНИЦИПАЛЬНОЕ СОБРАНИЕ", "ГОРОДСКОЕ СОБРАНИЕ", "ЗАКОНОДАТЕЛЬНОЕ СОБРАНИЕ", "НАРОДНОЕ СОБРАНИЕ", "ОБЛАСТНАЯ ДУМА", "ГОРОДСКАЯ ДУМА", "КРАЕВАЯ ДУМА", "КАБИНЕТ МИНИСТРОВ"]
        sov2 = ["СОВБЕЗ", "НАЦСОВЕТ", "ГОССОВЕТ", "ОБЛСОВЕТ", "РАЙСОВЕТ", "ГОРСОВЕТ", "СЕЛЬСОВЕТ", "КРАЙСОВЕТ", None, None, "ГОССОБРАНИЕ", "МУНСОБРАНИЕ", "ГОРСОБРАНИЕ", "ЗАКСОБРАНИЕ", "НАРСОБРАНИЕ", "ОБЛДУМА", "ГОРДУМА", "КРАЙДУМА", "КАБМИН"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1742(sovs[i], MorphLang.RU, OrgProfile.STATE, 4, OrgItemTermin.Types.ORG, True, True)
            if (sov2[i] is not None): 
                t.addVariant(sov2[i], False)
                if (sov2[i] == "ГОССОВЕТ" or sov2[i] == "НАЦСОВЕТ" or sov2[i] == "ЗАКСОБРАНИЕ"): 
                    t.coeff = (5)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        sovs = ["РАДА БЕЗПЕКИ", "НАЦІОНАЛЬНА РАДА", "ДЕРЖАВНА РАДА", "ОБЛАСНА РАДА", "РАЙОННА РАДА", "МІСЬКА РАДА", "СІЛЬСЬКА РАДА", "КРАЙОВИЙ РАДА", "СЛІДЧИЙ КОМІТЕТ", "СЛІДЧЕ УПРАВЛІННЯ", "ДЕРЖАВНІ ЗБОРИ", "МУНІЦИПАЛЬНЕ ЗБОРИ", "МІСЬКЕ ЗБОРИ", "ЗАКОНОДАВЧІ ЗБОРИ", "НАРОДНІ ЗБОРИ", "ОБЛАСНА ДУМА", "МІСЬКА ДУМА", "КРАЙОВА ДУМА", "КАБІНЕТ МІНІСТРІВ"]
        sov2 = ["РАДБЕЗ", None, None, "ОБЛРАДА", "РАЙРАДА", "МІСЬКРАДА", "СІЛЬРАДА", "КРАЙРАДА", None, None, "ДЕРЖЗБОРИ", "МУНЗБОРИ", "ГОРСОБРАНИЕ", "ЗАКЗБОРИ", "НАРСОБРАНИЕ", "ОБЛДУМА", "МІСЬКДУМА", "КРАЙДУМА", "КАБМІН"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1742(sovs[i], MorphLang.UA, OrgProfile.STATE, 4, OrgItemTermin.Types.ORG, True, True)
            if (sov2[i] is not None): 
                t.addVariant(sov2[i], False)
            if (sov2[i] == "ГОССОВЕТ" or sov2[i] == "ЗАКЗБОРИ"): 
                t.coeff = (5)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        sovs = ["SECURITY COUNCIL", "NATIONAL COUNCIL", "STATE COUNCIL", "REGIONAL COUNCIL", "DISTRICT COUNCIL", "CITY COUNCIL", "RURAL COUNCIL", "INVESTIGATIVE COMMITTEE", "INVESTIGATION DEPARTMENT", "NATIONAL ASSEMBLY", "MUNICIPAL ASSEMBLY", "URBAN ASSEMBLY", "LEGISLATURE"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1742(sovs[i], MorphLang.EN, OrgProfile.STATE, 4, OrgItemTermin.Types.ORG, True, True)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        t = OrgItemTermin._new1745("ГОСУДАРСТВЕННЫЙ КОМИТЕТ", OrgItemTermin.Types.ORG, OrgProfile.STATE, 2)
        t.addVariant("ГОСКОМИТЕТ", False)
        t.addVariant("ГОСКОМ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1746("ДЕРЖАВНИЙ КОМІТЕТ", MorphLang.UA, OrgItemTermin.Types.ORG, OrgProfile.STATE, 2)
        t.addVariant("ДЕРЖКОМІТЕТ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1747("КРАЕВОЙ КОМИТЕТ ГОСУДАРСТВЕННОЙ СТАТИСТИКИ", OrgItemTermin.Types.DEP, OrgProfile.STATE, 3, True)
        t.addVariant("КРАЙКОМСТАТ", False)
        t._profile = OrgProfile.UNIT
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1747("ОБЛАСТНОЙ КОМИТЕТ ГОСУДАРСТВЕННОЙ СТАТИСТИКИ", OrgItemTermin.Types.DEP, OrgProfile.STATE, 3, True)
        t.addVariant("ОБЛКОМСТАТ", False)
        t._profile = OrgProfile.UNIT
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1747("РАЙОННЫЙ КОМИТЕТ ГОСУДАРСТВЕННОЙ СТАТИСТИКИ", OrgItemTermin.Types.DEP, OrgProfile.STATE, 3, True)
        t.addVariant("РАЙКОМСТАТ", False)
        t._profile = OrgProfile.UNIT
        OrgItemTypeToken.__m_global.add(t)
        sovs = ["ЦЕНТРАЛЬНЫЙ КОМИТЕТ", "РАЙОННЫЙ КОМИТЕТ", "ГОРОДСКОЙ КОМИТЕТ", "КРАЕВОЙ КОМИТЕТ", "ОБЛАСТНОЙ КОМИТЕТ", "ПОЛИТИЧЕСКОЕ БЮРО"]
        sov2 = ["ЦК", "РАЙКОМ", "ГОРКОМ", "КРАЙКОМ", "ОБКОМ", "ПОЛИТБЮРО"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1750(sovs[i], 2, OrgItemTermin.Types.DEP, OrgProfile.UNIT)
            if (i == 0): 
                t.acronym = "ЦК"
                t.can_be_normal_dep = True
            elif (sov2[i] is not None): 
                t.addVariant(sov2[i], False)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        for s in ["Standing Committee", "Political Bureau", "Central Committee"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1751(s.upper(), 3, OrgItemTermin.Types.DEP, OrgProfile.UNIT, True))
        sovs = ["ЦЕНТРАЛЬНИЙ КОМІТЕТ", "РАЙОННИЙ КОМІТЕТ", "МІСЬКИЙ КОМІТЕТ", "КРАЙОВИЙ КОМІТЕТ", "ОБЛАСНИЙ КОМІТЕТ"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1752(sovs[i], MorphLang.UA, 2, OrgItemTermin.Types.DEP, OrgProfile.UNIT)
            if (i == 0): 
                t.acronym = "ЦК"
                t.can_be_normal_dep = True
            elif (sov2[i] is not None): 
                t.addVariant(sov2[i], False)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        t = OrgItemTermin._new1753("КАЗНАЧЕЙСТВО", 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1754("КАЗНАЧЕЙСТВО", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1753("TREASURY", 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1756("ГОСУДАРСТВЕННЫЙ ДЕПАРТАМЕНТ", 5, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ГОСДЕПАРТАМЕНТ", False)
        t.addVariant("ГОСДЕП", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1756("DEPARTMENT OF STATE", 5, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("STATE DEPARTMENT", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1758("ДЕРЖАВНИЙ ДЕПАРТАМЕНТ", MorphLang.UA, 5, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ДЕРЖДЕПАРТАМЕНТ", False)
        t.addVariant("ДЕРЖДЕП", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1759("ДЕПАРТАМЕНТ", 2, OrgItemTermin.Types.ORG))
        t = OrgItemTermin._new1759("DEPARTMENT", 2, OrgItemTermin.Types.ORG)
        t.addAbridge("DEPT.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1761("АГЕНТСТВО", 1, OrgItemTermin.Types.ORG, True)
        t.addVariant("АГЕНСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1761("ADGENCY", 1, OrgItemTermin.Types.ORG, True))
        t = OrgItemTermin._new1750("АКАДЕМИЯ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1764("АКАДЕМІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1750("ACADEMY", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1766("ГЕНЕРАЛЬНЫЙ ШТАБ", 3, OrgItemTermin.Types.DEP, True, True, OrgProfile.ARMY)
        t.addVariant("ГЕНЕРАЛЬНИЙ ШТАБ", False)
        t.addVariant("ГЕНШТАБ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1766("GENERAL STAFF", 3, OrgItemTermin.Types.DEP, True, True, OrgProfile.ARMY)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1768("ФРОНТ", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("ВОЕННЫЙ ОКРУГ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1770("ВІЙСЬКОВИЙ ОКРУГ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1768("ГРУППА АРМИЙ", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1772("ГРУПА АРМІЙ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1768("АРМИЯ", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1772("АРМІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1768("ARMY", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("ГВАРДИЯ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1770("ГВАРДІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("GUARD", 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        t = OrgItemTermin._new1779("ВОЙСКОВАЯ ЧАСТЬ", 3, "ВЧ", OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
        OrgItemTypeToken.__m_military_unit = t
        t.addAbridge("В.Ч.")
        t.addVariant("ВОИНСКАЯ ЧАСТЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("ВІЙСЬКОВА ЧАСТИНА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        t.addAbridge("В.Ч.")
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ДИВИЗИЯ", "ДИВИЗИОН", "ПОЛК", "БАТАЛЬОН", "РОТА", "ВЗВОД", "АВИАДИВИЗИЯ", "АВИАПОЛК", "ПОГРАНПОЛК", "АРТБРИГАДА", "МОТОМЕХБРИГАДА", "ТАНКОВЫЙ КОРПУС", "ГАРНИЗОН"]: 
            t = OrgItemTermin._new1781(s, 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            if (s == "ГАРНИЗОН"): 
                t.can_be_single_geo = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ДИВІЗІЯ", "ДИВІЗІОН", "ПОЛК", "БАТАЛЬЙОН", "РОТА", "ВЗВОД", "АВІАДИВІЗІЯ", "АВІАПОЛК", "ПОГРАНПОЛК", "АРТБРИГАДА", "МОТОМЕХБРИГАДА", "ТАНКОВИЙ КОРПУС", "ГАРНІЗОН"]: 
            t = OrgItemTermin._new1782(s, 3, MorphLang.UA, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            if (s == "ГАРНІЗОН"): 
                t.can_be_single_geo = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["КОРПУС", "БРИГАДА"]: 
            t = OrgItemTermin._new1781(s, 1, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["КОРПУС", "БРИГАДА"]: 
            t = OrgItemTermin._new1782(s, 1, MorphLang.UA, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1750("ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("ДЕРЖАВНИЙ УНІВЕРСИТЕТ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1750("STATE UNIVERSITY", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1750("УНИВЕРСИТЕТ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("УНІВЕРСИТЕТ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1790("UNIVERSITY", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1791("УЧРЕЖДЕНИЕ", 1, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1792("УСТАНОВА", MorphLang.UA, 1, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1791("INSTITUTION", 1, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1759("ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ", 3, OrgItemTermin.Types.ORG))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1795("ДЕРЖАВНА УСТАНОВА", MorphLang.UA, 3, OrgItemTermin.Types.ORG))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1753("STATE INSTITUTION", 3, OrgItemTermin.Types.ORG, True))
        t = OrgItemTermin._new1750("ИНСТИТУТ", 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1764("ІНСТИТУТ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1750("INSTITUTE", 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1800("ОТДЕЛ СУДЕБНЫХ ПРИСТАВОВ", OrgItemTermin.Types.PREFIX, "ОСП", OrgProfile.UNIT, True, True)
        t.profiles.append(OrgProfile.JUSTICE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1800("МЕЖРАЙОННЫЙ ОТДЕЛ СУДЕБНЫХ ПРИСТАВОВ", OrgItemTermin.Types.PREFIX, "МОСП", OrgProfile.UNIT, True, True)
        t.addVariant("МЕЖРАЙОННЫЙ ОСП", False)
        t.profiles.append(OrgProfile.JUSTICE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1800("ОТДЕЛ ВНЕВЕДОМСТВЕННОЙ ОХРАНЫ", OrgItemTermin.Types.PREFIX, "ОВО", OrgProfile.UNIT, True, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1803("ЛИЦЕЙ", 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1804("ЛІЦЕЙ", MorphLang.UA, 2, OrgProfile.EDUCATION, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1803("ИНТЕРНАТ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1804("ІНТЕРНАТ", MorphLang.UA, 3, OrgProfile.EDUCATION, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1807("HIGH SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1807("SECONDARY SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1807("MIDDLE SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1807("PUBLIC SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1807("JUNIOR SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1807("GRAMMAR SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        t = OrgItemTermin._new1813("СРЕДНЯЯ ШКОЛА", 3, "СОШ", OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True)
        t.addVariant("СРЕДНЯЯ ОБРАЗОВАТЕЛЬНАЯ ШКОЛА", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1814("БИЗНЕС ШКОЛА", 3, OrgItemTermin.Types.ORG, True, True, True, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1814("БІЗНЕС ШКОЛА", 3, OrgItemTermin.Types.ORG, True, True, True, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1804("СЕРЕДНЯ ШКОЛА", MorphLang.UA, 3, OrgProfile.EDUCATION, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1750("ВЫСШАЯ ШКОЛА", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("ВИЩА ШКОЛА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("НАЧАЛЬНАЯ ШКОЛА", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("ПОЧАТКОВА ШКОЛА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("СЕМИНАРИЯ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("СЕМІНАРІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("ГИМНАЗИЯ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("ГІМНАЗІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        t = OrgItemTermin._new1781("ДЕТСКИЙ САД", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION)
        t.addVariant("ДЕТСАД", False)
        t.addAbridge("Д.С.")
        t.addAbridge("Д/С")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1820("ДИТЯЧИЙ САДОК", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION)
        t.addVariant("ДИТСАДОК", False)
        t.addAbridge("Д.С.")
        t.addAbridge("Д/З")
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("ШКОЛА", 1, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1828("SCHOOL", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("УЧИЛИЩЕ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("КОЛЛЕДЖ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1828("COLLEGE", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1832("ЦЕНТР", OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1750("НАУЧНЫЙ ЦЕНТР", 3, OrgItemTermin.Types.ORG, OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("НАУКОВИЙ ЦЕНТР", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("БОЛЬНИЦА", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("ЛІКАРНЯ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("МОРГ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("МОРГ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("ХОСПИС", 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("ХОСПІС", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        t = OrgItemTermin._new1781("ГОРОДСКАЯ БОЛЬНИЦА", 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.addAbridge("ГОР.БОЛЬНИЦА")
        t.addVariant("ГОРБОЛЬНИЦА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1820("МІСЬКА ЛІКАРНЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1843("ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА", 3, OrgItemTermin.Types.ORG, True, "ГКБ", OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1844("МІСЬКА КЛІНІЧНА ЛІКАРНЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, "МКЛ", OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1845("КЛАДБИЩЕ", 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("КЛАДОВИЩЕ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("ПОЛИКЛИНИКА", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("ПОЛІКЛІНІКА", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("ГОСПИТАЛЬ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("ГОСПІТАЛЬ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1781("КЛИНИКА", 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1820("КЛІНІКА", MorphLang.UA, 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        t = OrgItemTermin._new1781("МЕДИКО САНИТАРНАЯ ЧАСТЬ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.addVariant("МЕДСАНЧАСТЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1820("МЕДИКО САНІТАРНА ЧАСТИНА", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.addVariant("МЕДСАНЧАСТИНА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1855("МЕДИЦИНСКИЙ ЦЕНТР", 2, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDICINE)
        t.addVariant("МЕДЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1856("МЕДИЧНИЙ ЦЕНТР", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDICINE)
        t.addVariant("МЕДЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1781("РОДИЛЬНЫЙ ДОМ", 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.addVariant("РОДДОМ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1820("ПОЛОГОВИЙ БУДИНОК", MorphLang.UA, 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1859("АЭРОПОРТ", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1860("АЕРОПОРТ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, True)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ТЕАТР", "ТЕАТР-СТУДИЯ", "КИНОТЕАТР", "МУЗЕЙ", "ГАЛЕРЕЯ", "КОНЦЕРТНЫЙ ЗАЛ", "ФИЛАРМОНИЯ", "КОНСЕРВАТОРИЯ", "ДОМ КУЛЬТУРЫ", "ДВОРЕЦ КУЛЬТУРЫ", "ДВОРЕЦ ПИОНЕРОВ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1761(s, 3, OrgItemTermin.Types.ORG, True))
        for s in ["ТЕАТР", "ТЕАТР-СТУДІЯ", "КІНОТЕАТР", "МУЗЕЙ", "ГАЛЕРЕЯ", "КОНЦЕРТНИЙ ЗАЛ", "ФІЛАРМОНІЯ", "КОНСЕРВАТОРІЯ", "БУДИНОК КУЛЬТУРИ", "ПАЛАЦ КУЛЬТУРИ", "ПАЛАЦ ПІОНЕРІВ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1862(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1863("БИБЛИОТЕКА", 3, OrgItemTermin.Types.ORG, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1864("БІБЛІОТЕКА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True))
        for s in ["ЦЕРКОВЬ", "ХРАМ", "СОБОР", "МЕЧЕТЬ", "СИНАГОГА", "МОНАСТЫРЬ", "ЛАВРА", "ПАТРИАРХАТ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1865(s, 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.RELIGION))
        for s in ["ЦЕРКВА", "ХРАМ", "СОБОР", "МЕЧЕТЬ", "СИНАГОГА", "МОНАСТИР", "ЛАВРА", "ПАТРІАРХАТ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1866(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.RELIGION))
        for s in ["ФЕДЕРАЛЬНАЯ СЛУЖБА", "ГОСУДАРСТВЕННАЯ СЛУЖБА", "ФЕДЕРАЛЬНОЕ УПРАВЛЕНИЕ", "ГОСУДАРСТВЕННЫЙ КОМИТЕТ", "ГОСУДАРСТВЕННАЯ ИНСПЕКЦИЯ"]: 
            t = OrgItemTermin._new1867(s, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
            t = OrgItemTermin._new1868(s, 3, OrgItemTermin.Types.ORG, s)
            t.terms.insert(1, Termin.Term._new1869(None, True))
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ФЕДЕРАЛЬНА СЛУЖБА", "ДЕРЖАВНА СЛУЖБА", "ФЕДЕРАЛЬНЕ УПРАВЛІННЯ", "ДЕРЖАВНИЙ КОМІТЕТ УКРАЇНИ", "ДЕРЖАВНА ІНСПЕКЦІЯ"]: 
            t = OrgItemTermin._new1870(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
            t = OrgItemTermin._new1871(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, s)
            t.terms.insert(1, Termin.Term._new1869(None, True))
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1845("СЛЕДСТВЕННЫЙ ИЗОЛЯТОР", 5, OrgItemTermin.Types.ORG, True)
        t.addVariant("СИЗО", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("СЛІДЧИЙ ІЗОЛЯТОР", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        t.addVariant("СІЗО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1845("КОЛОНИЯ-ПОСЕЛЕНИЕ", 3, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("КОЛОНІЯ-ПОСЕЛЕННЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1877("ТЮРЬМА", 3, OrgItemTermin.Types.ORG, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1878("ВЯЗНИЦЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1845("КОЛОНИЯ", 2, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("КОЛОНІЯ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_ispr_kolon = OrgItemTermin._new1881("ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ", 3, OrgItemTermin.Types.ORG, "ИК", True)
        OrgItemTypeToken.__m_global.add(OrgItemTypeToken.__m_ispr_kolon)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ВИПРАВНА КОЛОНІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True))
        for s in ["ПОЛИЦИЯ", "МИЛИЦИЯ"]: 
            t = OrgItemTermin._new1883(s, OrgItemTermin.Types.ORG, 3, True, False)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПОЛІЦІЯ", "МІЛІЦІЯ"]: 
            t = OrgItemTermin._new1884(s, MorphLang.UA, OrgItemTermin.Types.ORG, 3, True, False)
            OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1885("ПАЕВЫЙ ИНВЕСТИЦИОННЫЙ ФОНД", 2, OrgItemTermin.Types.ORG, "ПИФ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1886("РОССИЙСКОЕ ИНФОРМАЦИОННОЕ АГЕНТСТВО", 3, OrgItemTermin.Types.ORG, "РИА", OrgProfile.MEDIA))
        t = OrgItemTermin._new1886("ИНФОРМАЦИОННОЕ АГЕНТСТВО", 3, OrgItemTermin.Types.ORG, "ИА", OrgProfile.MEDIA)
        t.addVariant("ИНФОРМАГЕНТСТВО", False)
        t.addVariant("ИНФОРМАГЕНСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1791("ОТДЕЛ", 1, OrgItemTermin.Types.DEP, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1889("ВІДДІЛ", MorphLang.UA, 1, OrgItemTermin.Types.DEP, True))
        t = OrgItemTermin._new1759("ФАКУЛЬТЕТ", 3, OrgItemTermin.Types.DEP)
        t.addAbridge("ФАК.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1759("КАФЕДРА", 3, OrgItemTermin.Types.DEP)
        t.addAbridge("КАФ.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1759("ЛАБОРАТОРИЯ", 1, OrgItemTermin.Types.DEP)
        t.addAbridge("ЛАБ.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1893("ЛАБОРАТОРІЯ", MorphLang.UA, 1, OrgItemTermin.Types.DEP)
        t.addAbridge("ЛАБ.")
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("ПАТРИАРХИЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("ПАТРІАРХІЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("ЕПАРХИЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1769("ЄПАРХІЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1898("ПРЕДСТАВИТЕЛЬСТВО", OrgItemTermin.Types.DEPADD))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1899("ПРЕДСТАВНИЦТВО", MorphLang.UA, OrgItemTermin.Types.DEPADD))
        t = OrgItemTermin._new1832("ОТДЕЛЕНИЕ", OrgItemTermin.Types.DEPADD, True)
        t.addAbridge("ОТД.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1901("ВІДДІЛЕННЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1832("ИНСПЕКЦИЯ", OrgItemTermin.Types.DEPADD, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1901("ІНСПЕКЦІЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1898("ФИЛИАЛ", OrgItemTermin.Types.DEPADD))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1899("ФІЛІЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD))
        for s in ["ОТДЕЛ ПОЛИЦИИ", "ОТДЕЛ МИЛИЦИИ", "ОТДЕЛЕНИЕ ПОЛИЦИИ", "ОТДЕЛЕНИЕ МИЛИЦИИ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1906(s, OrgItemTermin.Types.DEP, 1.5, True, True))
            if (s.startswith("ОТДЕЛ ")): 
                t = OrgItemTermin._new1906("ГОРОДСКОЙ " + s, OrgItemTermin.Types.DEP, 3, True, True)
                t.addVariant("ГОР" + s, False)
                OrgItemTypeToken.__m_global.add(t)
                t = OrgItemTermin._new1906("РАЙОННЫЙ " + s, OrgItemTermin.Types.DEP, 3, True, True)
                t.addVariant("РАЙ" + s, False)
                OrgItemTypeToken.__m_global.add(t)
        for s in ["ВІДДІЛ ПОЛІЦІЇ", "ВІДДІЛ МІЛІЦІЇ", "ВІДДІЛЕННЯ ПОЛІЦІЇ", "ВІДДІЛЕННЯ МІЛІЦІЇ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1909(s, MorphLang.UA, OrgItemTermin.Types.DEP, 1.5, True, True))
        t = OrgItemTermin._new1910("ГЛАВНОЕ УПРАВЛЕНИЕ", "ГУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1911("ГОЛОВНЕ УПРАВЛІННЯ", MorphLang.UA, "ГУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1910("ГЛАВНОЕ ТЕРРИТОРИАЛЬНОЕ УПРАВЛЕНИЕ", "ГТУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1911("ГОЛОВНЕ ТЕРИТОРІАЛЬНЕ УПРАВЛІННЯ", MorphLang.UA, "ГТУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1910("ОПЕРАЦИОННОЕ УПРАВЛЕНИЕ", "ОПЕРУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1911("ОПЕРАЦІЙНЕ УПРАВЛІННЯ", MorphLang.UA, "ОПЕРУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1916("ТЕРРИТОРИАЛЬНОЕ УПРАВЛЕНИЕ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1917("ТЕРИТОРІАЛЬНЕ УПРАВЛІННЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1832("УПРАВЛЕНИЕ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1901("УПРАВЛІННЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1910("ПОГРАНИЧНОЕ УПРАВЛЕНИЕ", "ПУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ПРЕСС-СЛУЖБА", "ПРЕСС-ЦЕНТР", "КОЛЛ-ЦЕНТР", "БУХГАЛТЕРИЯ", "МАГИСТРАТУРА", "АСПИРАНТУРА", "ДОКТОРАНТУРА", "ОРДИНАТУРА", "СОВЕТ ДИРЕКТОРОВ", "УЧЕНЫЙ СОВЕТ", "КОЛЛЕГИЯ", "ПЛЕНУМ", "АППАРАТ", "НАБЛЮДАТЕЛЬНЫЙ СОВЕТ", "ОБЩЕСТВЕННЫЙ СОВЕТ", "РУКОВОДСТВО", "ДИРЕКЦИЯ", "ПРАВЛЕНИЕ", "ЖЮРИ", "ПРЕЗИДИУМ", "СЕКРЕТАРИАТ", "СИНОД", "PRESS", "PRESS CENTER", "CLIENT CENTER", "CALL CENTER", "ACCOUNTING", "MASTER DEGREE", "POSTGRADUATE", "DOCTORATE", "RESIDENCY", "BOARD OF DIRECTORS", "DIRECTOR BOARD", "ACADEMIC COUNCIL", "BOARD", "PLENARY", "UNIT", "SUPERVISORY BOARD", "PUBLIC COUNCIL", "LEADERSHIP", "MANAGEMENT", "JURY", "BUREAU", "SECRETARIAT"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1921(s, OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT))
        for s in ["ПРЕС-СЛУЖБА", "ПРЕС-ЦЕНТР", "БУХГАЛТЕРІЯ", "МАГІСТРАТУРА", "АСПІРАНТУРА", "ДОКТОРАНТУРА", "ОРДИНАТУРА", "РАДА ДИРЕКТОРІВ", "ВЧЕНА РАДА", "КОЛЕГІЯ", "ПЛЕНУМ", "АПАРАТ", "НАГЛЯДОВА РАДА", "ГРОМАДСЬКА РАДА", "КЕРІВНИЦТВО", "ДИРЕКЦІЯ", "ПРАВЛІННЯ", "ЖУРІ", "ПРЕЗИДІЯ", "СЕКРЕТАРІАТ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1922(s, MorphLang.UA, OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT))
        t = OrgItemTermin._new1921("ОТДЕЛ ИНФОРМАЦИОННОЙ БЕЗОПАСНОСТИ", OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT)
        t.addVariant("ОТДЕЛ ИБ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1921("ОТДЕЛ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ", OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT)
        t.addVariant("ОТДЕЛ ИТ", False)
        t.addVariant("ОТДЕЛ IT", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1832("СЕКТОР", OrgItemTermin.Types.DEP, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("КУРС", OrgItemTermin.Types.DEP, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1927("ГРУППА", OrgItemTermin.Types.DEP, True, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1928("ГРУПА", MorphLang.UA, OrgItemTermin.Types.DEP, True, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1921("ДНЕВНОЕ ОТДЕЛЕНИЕ", OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1922("ДЕННЕ ВІДДІЛЕННЯ", MorphLang.UA, OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1921("ВЕЧЕРНЕЕ ОТДЕЛЕНИЕ", OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1922("ВЕЧІРНЄ ВІДДІЛЕННЯ", MorphLang.UA, OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1916("ДЕЖУРНАЯ ЧАСТЬ", OrgItemTermin.Types.DEP, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1917("ЧЕРГОВА ЧАСТИНА", MorphLang.UA, OrgItemTermin.Types.DEP, True))
        t = OrgItemTermin._new1935("ПАСПОРТНЫЙ СТОЛ", OrgItemTermin.Types.DEP, True)
        t.addAbridge("П/С")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1936("ПАСПОРТНИЙ СТІЛ", MorphLang.UA, OrgItemTermin.Types.DEP, True)
        t.addAbridge("П/С")
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1937("ВЫСШЕЕ УЧЕБНОЕ ЗАВЕДЕНИЕ", OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВУЗ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1938("ВИЩИЙ НАВЧАЛЬНИЙ ЗАКЛАД", MorphLang.UA, OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВНЗ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1937("ВЫСШЕЕ ПРОФЕССИОНАЛЬНОЕ УЧИЛИЩЕ", OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВПУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1938("ВИЩЕ ПРОФЕСІЙНЕ УЧИЛИЩЕ", MorphLang.UA, OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВПУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1937("НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE, "НИИ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1938("НАУКОВО ДОСЛІДНИЙ ІНСТИТУТ", MorphLang.UA, OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE, "НДІ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, "НИЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО ДОСЛІДНИЙ ЦЕНТР", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НДЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ЦЕНТРАЛЬНЫЙ НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, "ЦНИИ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ВСЕРОССИЙСКИЙ НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, "ВНИИ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("РОССИЙСКИЙ НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, "РНИИ", OrgProfile.SCIENCE))
        t = OrgItemTermin._new1948("ИННОВАЦИОННЫЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE)
        t.addVariant("ИННОЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ТЕХНИЧЕСКИЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, "НТЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО ТЕХНІЧНИЙ ЦЕНТР", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НТЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ТЕХНИЧЕСКАЯ ФИРМА", OrgItemTermin.Types.PREFIX, "НТФ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО ВИРОБНИЧА ФІРМА", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВФ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ПРОИЗВОДСТВЕННОЕ ОБЪЕДИНЕНИЕ", OrgItemTermin.Types.PREFIX, "НПО", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО ВИРОБНИЧЕ ОБЄДНАННЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВО", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1948("НАУЧНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО-ВИРОБНИЧИЙ КООПЕРАТИВ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ПРОИЗВОДСТВЕННАЯ КОРПОРАЦИЯ", OrgItemTermin.Types.PREFIX, "НПК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ТЕХНИЧЕСКИЙ КОМПЛЕКС", OrgItemTermin.Types.PREFIX, "НТК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МЕЖОТРАСЛЕВОЙ НАУЧНО ТЕХНИЧЕСКИЙ КОМПЛЕКС", OrgItemTermin.Types.PREFIX, "МНТК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ПРОИЗВОДСТВЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "НПП", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО ВИРОБНИЧЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВП", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ПРОИЗВОДСТВЕННЫЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, "НПЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1944("НАУКОВО ВИРОБНИЧЕ ЦЕНТР", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НАУЧНО ПРОИЗВОДСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "НПУП", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ПРИВАТНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ПП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ ПРОИЗВОДСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧПУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ ИНДИВИДУАЛЬНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧИП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ ОХРАННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧОП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНАЯ ОХРАННАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, "ЧОО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ ТРАНСПОРТНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧТУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ЧАСТНОЕ ТРАНСПОРТНО ЭКСПЛУАТАЦИОННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧТЭУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("НАУЧНО ПРОИЗВОДСТВЕННОЕ КОРПОРАЦИЯ", OrgItemTermin.Types.PREFIX, "НПК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ФГУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ГУП"))
        t = OrgItemTermin._new1965("ГОСУДАРСТВЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ГП")
        t.addVariant("ГОСПРЕДПРИЯТИЕ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1966("ДЕРЖАВНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ДП")
        t.addVariant("ДЕРЖПІДПРИЄМСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ НАУЧНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГНУ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ КАЗЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГКОУ"))
        t = OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГБУ")
        t.addVariant("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ НАУКИ", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ВОЕННО ПРОМЫШЛЕННАЯ КОРПОРАЦИЯ", OrgItemTermin.Types.PREFIX, "ВПК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФБУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ФУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ НЕКОММЕРЧЕСКОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МНУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МБУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МАУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРОИЗВОДСТВЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МУПП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МКП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("МУНИЦИПАЛЬНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("НЕБАНКОВСКАЯ КРЕДИТНАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, "НКО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("РАСЧЕТНАЯ НЕБАНКОВСКАЯ КРЕДИТНАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, "РНКО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГАУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1898("МАЛОЕ ИННОВАЦИОННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("НЕГОСУДАРСТВЕННЫЙ ПЕНСИОННЫЙ ФОНД", OrgItemTermin.Types.PREFIX, "НПФ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ДЕРЖАВНА АКЦІОНЕРНА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ДАК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ДЕРЖАВНА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ДК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("КОЛЕКТИВНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "КП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("КОЛЕКТИВНЕ МАЛЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "КМП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ВИРОБНИЧА ФІРМА", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВФ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ВИРОБНИЧЕ ОБЄДНАННЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ВИРОБНИЧЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ВИРОБНИЧИЙ КООПЕРАТИВ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("СТРАХОВА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "СК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1966("ТВОРЧЕ ОБЄДНАННЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ТО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ФГУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ФКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГАУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ ОБЛАСТНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГОБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ ОБЛАСТНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГОКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НЕГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "НУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ ОБЛАСТНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МОБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МАУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1948("ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ФГУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ФКУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ГАУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ГБУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ ОБЛАСТНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ГОБУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ГКУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ ОБЛАСТНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ГОКУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "МУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("НЕГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "НУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "МБУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "МКУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ ОБЛАСТНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "МОБУК", OrgProfile.ART))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "МАУК", OrgProfile.ART))
        t = OrgItemTermin._new1965("ЧАСТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ЧУК")
        t.addVariant("ЧАСТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ ЛФП", False)
        t.addVariant("ЧУК ЛФП", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ОБРАЗОВАНИЯ", OrgItemTermin.Types.PREFIX, "ГБУО", OrgProfile.EDUCATION))
        t = OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ПРФЕСИОНАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБПОУ", OrgProfile.EDUCATION)
        t.addVariant("ГБ ПОУ", True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБЩЕОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ДОПОЛНИТЕЛЬНОГО ОБРАЗОВАНИЯ", OrgItemTermin.Types.PREFIX, "ГБУДО", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МКОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("МУНИЦИПАЛЬНОЕ ЛЕЧЕБНО ПРОФИЛАКТИЧЕСКОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МЛПУ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ ЛЕЧЕБНО ПРОФИЛАКТИЧЕСКОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФКЛПУ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГБОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ВЫСШЕЕ ПРОФЕССИОНАЛЬНОЕ ОБРАЗОВАНИЕ", OrgItemTermin.Types.PREFIX, "ВПО", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1943("ДОПОЛНИТЕЛЬНОЕ ПРОФЕССИОНАЛЬНОЕ ОБРАЗОВАНИЕ", OrgItemTermin.Types.PREFIX, "ДПО", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2055("ДЕПАРТАМЕНТ ЕДИНОГО ЗАКАЗЧИКА", OrgItemTermin.Types.PREFIX, "ДЕЗ", True, True))
        t = OrgItemTermin._new2056("СОЮЗ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ", OrgItemTermin.Types.PREFIX, "САУ", True)
        t.addVariant("САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ", False)
        t.addVariant("СОАУ", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "АО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АТ"))
        OrgItemTypeToken.__m_sovm_pred = OrgItemTermin._new2057("СОВМЕСТНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, True, "СП")
        OrgItemTypeToken.__m_global.add(OrgItemTypeToken.__m_sovm_pred)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("СПІЛЬНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "СП"))
        OrgItemTypeToken.__m_akcion_comp = OrgItemTermin._new2061("АКЦИОНЕРНАЯ КОМПАНИЯ", OrgItemTermin.Types.PREFIX, True)
        OrgItemTypeToken.__m_global.add(OrgItemTypeToken.__m_akcion_comp)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ЗАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2063("РОССИЙСКОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "РАО", "PAO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("РОССИЙСКОЕ ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "РОАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АКЦИОНЕРНОЕ ОБЩЕСТВО ЗАКРЫТОГО ТИПА", OrgItemTermin.Types.PREFIX, True, "АОЗТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АКЦІОНЕРНЕ ТОВАРИСТВО ЗАКРИТОГО ТИПУ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АТЗТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АКЦИОНЕРНОЕ ОБЩЕСТВО ОТКРЫТОГО ТИПА", OrgItemTermin.Types.PREFIX, True, "АООТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АКЦІОНЕРНЕ ТОВАРИСТВО ВІДКРИТОГО ТИПУ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АТВТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, True, "ОО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("ГРОМАДСЬКА ОРГАНІЗАЦІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ГО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, True, "АНО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АВТОНОМНА НЕКОМЕРЦІЙНА ОРГАНІЗАЦІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АНО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2063("ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ОАО", "OAO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ВІДКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ВАТ", "ВАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("ОТКРЫТОЕ СТРАХОВОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ОСАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2063("ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ", OrgItemTermin.Types.PREFIX, True, "ООО", "OOO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТОВ", "ТОВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ТОВАРИСТВО З ПОВНОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТПВ", "ТПВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТЗОВ", "ТЗОВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ТОВАРИСТВО З ДОДАТКОВОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТДВ", "ТДВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2061("ЧАСТНОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ПРИВАТНЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ПРАТ", "ПРАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2061("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ПУБЛІЧНЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ПАТ", "ПАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2061("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ЗАКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ЗАТ", "ЗАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2061("ОТКРЫТОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2074("ВІДКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ВАТ", "ВАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ПАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("СТРАХОВОЕ ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "СПАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2091("ТОВАРИЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ", OrgItemTermin.Types.PREFIX, "ТОО", "TOO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1965("ПРЕДПРИНИМАТЕЛЬ БЕЗ ОБРАЗОВАНИЯ ЮРИДИЧЕСКОГО ЛИЦА", OrgItemTermin.Types.PREFIX, "ПБОЮЛ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АКЦИОНЕРНЫЙ КОММЕРЧЕСКИЙ БАНК", OrgItemTermin.Types.PREFIX, True, "АКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АКЦІОНЕРНИЙ КОМЕРЦІЙНИЙ БАНК", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АКЦИОНЕРНЫЙ БАНК", OrgItemTermin.Types.PREFIX, True, "АБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АКЦІОНЕРНИЙ БАНК", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2061("КОММЕРЧЕСКИЙ БАНК", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2098("КОМЕРЦІЙНИЙ БАНК", MorphLang.UA, OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2061("КОНСТРУКТОРСКОЕ БЮРО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2098("КОНСТРУКТОРСЬКЕ БЮРО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("ОПЫТНО КОНСТРУКТОРСКОЕ БЮРО", OrgItemTermin.Types.PREFIX, True, "ОКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("ДОСЛІДНО КОНСТРУКТОРСЬКЕ БЮРО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ДКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2056("СПЕЦИАЛЬНОЕ КОНСТРУКТОРСКОЕ БЮРО", OrgItemTermin.Types.PREFIX, "СКБ", True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2104("СПЕЦІАЛЬНЕ КОНСТРУКТОРСЬКЕ БЮРО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "СКБ", True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("АКЦИОНЕРНАЯ СТРАХОВАЯ КОМПАНИЯ", OrgItemTermin.Types.PREFIX, True, "АСК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("АКЦІОНЕРНА СТРАХОВА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АСК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2107("АВТОТРАНСПОРТНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, True, True, "АТП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2108("АВТОТРАНСПОРТНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, True, "АТП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2057("ТЕЛЕРАДИОКОМПАНИЯ", OrgItemTermin.Types.PREFIX, True, "ТРК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2058("ТЕЛЕРАДІОКОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТРК"))
        t = OrgItemTermin._new2056("ОРГАНИЗОВАННАЯ ПРЕСТУПНАЯ ГРУППИРОВКА", OrgItemTermin.Types.PREFIX, "ОПГ", True)
        t.addVariant("ОРГАНИЗОВАННАЯ ПРЕСТУПНАЯ ГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2056("ОРГАНИЗОВАННОЕ ПРЕСТУПНОЕ СООБЩЕСТВО", OrgItemTermin.Types.PREFIX, "ОПС", True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ПОДРОСТКОВО МОЛОДЕЖНЫЙ КЛУБ", OrgItemTermin.Types.PREFIX, "ПМК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("СКЛАД ВРЕМЕННОГО ХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "СВХ", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ЖИЛИЩНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ЖСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГЭК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ГАРАЖНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГПК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ПГСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ГАРАЖНЫЙ СТРОИТЕЛЬНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГСПК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ДСК", True, True))
        t = OrgItemTermin._new2113("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, "СНТ", True, True)
        t.addAbridge("САДОВОЕ НЕКОМ-Е ТОВАРИЩЕСТВО")
        t.addVariant("СНТ ПМК", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2113("ПРЕДПРИЯТИЕ ПОТРЕБИТЕЛЬСКОЙ КООПЕРАЦИИ", OrgItemTermin.Types.PREFIX, "ППК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2124("ПІДПРИЄМСТВО СПОЖИВЧОЇ КООПЕРАЦІЇ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ПСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2125("ФІЗИЧНА ОСОБА ПІДПРИЄМЕЦЬ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ФОП", True, True))
        t = OrgItemTermin._new2126("ЖЕЛЕЗНАЯ ДОРОГА", OrgItemTermin.Types.ORG, OrgProfile.TRANSPORT, True, 3)
        t.addVariant("ЖЕЛЕЗНОДОРОЖНАЯ МАГИСТРАЛЬ", False)
        t.addAbridge("Ж.Д.")
        t.addAbridge("Ж/Д")
        t.addAbridge("ЖЕЛ.ДОР.")
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ЗАВОД", "ФАБРИКА", "БАНК", "КОМБИНАТ", "БАНКОВСКАЯ ГРУППА", "БИРЖА", "ФОНДОВАЯ БИРЖА", "FACTORY", "MANUFACTORY", "BANK"]: 
            t = OrgItemTermin._new2127(s, 3.5, OrgItemTermin.Types.ORG, True, True)
            OrgItemTypeToken.__m_global.add(t)
            if (s == "БАНК" or s == "BANK" or s.endswith("БИРЖА")): 
                t._profile = OrgProfile.FINANCE
                t.coeff = (2)
                t.can_has_latin_name = True
                if (OrgItemTypeToken.__m_bank is None): 
                    OrgItemTypeToken.__m_bank = t
        for s in ["ЗАВОД", "ФАБРИКА", "БАНК", "КОМБІНАТ", "БАНКІВСЬКА ГРУПА", "БІРЖА", "ФОНДОВА БІРЖА"]: 
            t = OrgItemTermin._new2128(s, MorphLang.UA, 3.5, OrgItemTermin.Types.ORG, True, True)
            OrgItemTypeToken.__m_global.add(t)
            if (s == "БАНК" or s.endswith("БІРЖА")): 
                t.coeff = (2)
                t.can_has_latin_name = True
                if (OrgItemTypeToken.__m_bank is None): 
                    OrgItemTypeToken.__m_bank = t
        for s in ["ТУРФИРМА", "ТУРАГЕНТСТВО", "ТУРКОМПАНИЯ", "АВИАКОМПАНИЯ", "КИНОСТУДИЯ", "БИЗНЕС-ЦЕНТР", "КООПЕРАТИВ", "РИТЕЙЛЕР", "ОНЛАЙН РИТЕЙЛЕР", "МЕДИАГИГАНТ", "МЕДИАКОМПАНИЯ", "МЕДИАХОЛДИНГ"]: 
            t = OrgItemTermin._new2129(s, 3.5, OrgItemTermin.Types.ORG, True, True, True)
            if (s.startswith("МЕДИА")): 
                t.profiles.append(OrgProfile.MEDIA)
            if ("РИТЕЙЛЕР" in s): 
                t.addVariant(s.replace("РИТЕЙЛЕР", "РЕТЕЙЛЕР"), False)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ТУРФІРМА", "ТУРАГЕНТСТВО", "ТУРКОМПАНІЯ", "АВІАКОМПАНІЯ", "КІНОСТУДІЯ", "БІЗНЕС-ЦЕНТР", "КООПЕРАТИВ", "РІТЕЙЛЕР", "ОНЛАЙН-РІТЕЙЛЕР", "МЕДІАГІГАНТ", "МЕДІАКОМПАНІЯ", "МЕДІАХОЛДИНГ"]: 
            t = OrgItemTermin._new2130(s, MorphLang.UA, 3.5, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ТУРОПЕРАТОР"]: 
            t = OrgItemTermin._new2129(s, .5, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ТУРОПЕРАТОР"]: 
            t = OrgItemTermin._new2130(s, MorphLang.UA, .5, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2133("СБЕРЕГАТЕЛЬНЫЙ БАНК", 4, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_sber_bank = t
        t.addVariant("СБЕРБАНК", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2134("ОЩАДНИЙ БАНК", MorphLang.UA, 4, OrgItemTermin.Types.ORG, True)
        t.addVariant("ОЩАДБАНК", False)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ОРГАНИЗАЦИЯ", "ПРЕДПРИЯТИЕ", "КОМИТЕТ", "КОМИССИЯ", "ПРОИЗВОДИТЕЛЬ", "ГИГАНТ", "ORGANIZATION", "ENTERPRISE", "COMMITTEE", "COMMISSION", "MANUFACTURER"]: 
            t = OrgItemTermin._new2135(s, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ОБЩЕСТВО", "АССАМБЛЕЯ", "СЛУЖБА", "ОБЪЕДИНЕНИЕ", "ФЕДЕРАЦИЯ", "COMPANY", "ASSEMBLY", "SERVICE", "UNION", "FEDERATION"]: 
            t = OrgItemTermin._new2135(s, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["СООБЩЕСТВО", "ФОНД", "АССОЦИАЦИЯ", "АЛЬЯНС", "ГИЛЬДИЯ", "ОБЩИНА", "СОЮЗ", "КЛУБ", "ГРУППИРОВКА", "ЛИГА", "COMMUNITY", "FOUNDATION", "ASSOCIATION", "ALLIANCE", "GUILD", "UNION", "CLUB", "GROUP", "LEAGUE"]: 
            t = OrgItemTermin._new2137(s, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.UNION)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПАРТИЯ", "ДВИЖЕНИЕ", "PARTY", "MOVEMENT"]: 
            t = OrgItemTermin._new2138(s, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.UNION)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["НОЧНОЙ КЛУБ", "NIGHTCLUB"]: 
            t = OrgItemTermin._new2139(s, OrgItemTermin.Types.ORG, True, True, OrgProfile.MUSIC)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ОРГАНІЗАЦІЯ", "ПІДПРИЄМСТВО", "КОМІТЕТ", "КОМІСІЯ", "ВИРОБНИК", "ГІГАНТ", "СУСПІЛЬСТВО", "СПІЛЬНОТА", "ФОНД", "СЛУЖБА", "АСОЦІАЦІЯ", "АЛЬЯНС", "АСАМБЛЕЯ", "ГІЛЬДІЯ", "ОБЄДНАННЯ", "СОЮЗ", "ПАРТІЯ", "РУХ", "ФЕДЕРАЦІЯ", "КЛУБ", "ГРУПУВАННЯ"]: 
            t = OrgItemTermin._new2140(s, MorphLang.UA, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2141("ДЕПУТАТСКАЯ ГРУППА", OrgItemTermin.Types.ORG, 3, True)
        t.addVariant("ГРУППА ДЕПУТАТОВ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2142("ДЕПУТАТСЬКА ГРУПА", MorphLang.UA, OrgItemTermin.Types.ORG, 3, True)
        t.addVariant("ГРУПА ДЕПУТАТІВ", False)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ФОНД", "СОЮЗ", "ОБЪЕДИНЕНИЕ", "ОРГАНИЗАЦИЯ", "ФЕДЕРАЦИЯ", "ДВИЖЕНИЕ"]: 
            for ss in ["ВСЕМИРНЫЙ", "МЕЖДУНАРОДНЫЙ", "ВСЕРОССИЙСКИЙ", "ОБЩЕСТВЕННЫЙ", "НЕКОММЕРЧЕСКИЙ", "ЕВРОПЕЙСКИЙ", "ВСЕУКРАИНСКИЙ"]: 
                t = OrgItemTermin._new2127("{0} {1}".format(ss, s), 3.5, OrgItemTermin.Types.ORG, True, True)
                if (s == "ОБЪЕДИНЕНИЕ" or s == "ДВИЖЕНИЕ"): 
                    t.canonic_text = "{0}ОЕ {1}".format(ss[0:0+len(ss) - 2], s)
                elif (s == "ОРГАНИЗАЦИЯ" or s == "ФЕДЕРАЦИЯ"): 
                    t.canonic_text = "{0}АЯ {1}".format(ss[0:0+len(ss) - 2], s)
                    t.coeff = (3)
                OrgItemTypeToken.__m_global.add(t)
        for s in ["ФОНД", "СОЮЗ", "ОБЄДНАННЯ", "ОРГАНІЗАЦІЯ", "ФЕДЕРАЦІЯ", "РУХ"]: 
            for ss in ["СВІТОВИЙ", "МІЖНАРОДНИЙ", "ВСЕРОСІЙСЬКИЙ", "ГРОМАДСЬКИЙ", "НЕКОМЕРЦІЙНИЙ", "ЄВРОПЕЙСЬКИЙ", "ВСЕУКРАЇНСЬКИЙ"]: 
                t = OrgItemTermin._new2128("{0} {1}".format(ss, s), MorphLang.UA, 3.5, OrgItemTermin.Types.ORG, True, True)
                bi = Morphology.getWordBaseInfo(s, MorphLang.UA, False, False)
                if (bi is not None and bi.gender != MorphGender.MASCULINE): 
                    adj = Morphology.getWordform(ss, MorphBaseInfo._new514(MorphClass.ADJECTIVE, bi.gender, MorphNumber.SINGULAR, MorphLang.UA))
                    if (adj is not None): 
                        t.canonic_text = "{0} {1}".format(adj, s)
                if (s == "ОРГАНІЗАЦІЯ" or s == "ФЕДЕРАЦІЯ"): 
                    t.coeff = (3)
                OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2127("ИНВЕСТИЦИОННЫЙ ФОНД", 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ИНВЕСТФОНД", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2128("ІНВЕСТИЦІЙНИЙ ФОНД", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ІНВЕСТФОНД", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2127("СОЦИАЛЬНАЯ СЕТЬ", 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("СОЦСЕТЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2128("СОЦІАЛЬНА МЕРЕЖА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("СОЦМЕРЕЖА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2127("ОФФШОРНАЯ КОМПАНИЯ", 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ОФФШОР", False)
        t.addVariant("ОФШОР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2128("ОФШОРНА КОМПАНІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ОФШОР", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2152("ТЕРРОРИСТИЧЕСКАЯ ОРГАНИЗАЦИЯ", 3, OrgItemTermin.Types.ORG, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2153("ТЕРОРИСТИЧНА ОРГАНІЗАЦІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2154("АТОМНАЯ ЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "АЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2155("АТОМНА ЕЛЕКТРОСТАНЦІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, "АЕС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2154("ГИДРОЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "ГЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2155("ГІДРОЕЛЕКТРОСТАНЦІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, "ГЕС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2154("ГИДРОРЕЦИРКУЛЯЦИОННАЯ ЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "ГРЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2154("ТЕПЛОВАЯ ЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "ТЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2154("НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", 3, OrgItemTermin.Types.ORG, "НПЗ", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2155("НАФТОПЕРЕРОБНИЙ ЗАВОД", MorphLang.UA, 3, OrgItemTermin.Types.ORG, "НПЗ", True, True, True))
        for s in ["ФИРМА", "КОМПАНИЯ", "КОРПОРАЦИЯ", "ГОСКОРПОРАЦИЯ", "КОНЦЕРН", "КОНСОРЦИУМ", "ХОЛДИНГ", "МЕДИАХОЛДИНГ", "ТОРГОВЫЙ ДОМ", "ТОРГОВЫЙ ЦЕНТР", "УЧЕБНЫЙ ЦЕНТР", "ИССЛЕДОВАТЕЛЬСКИЙ ЦЕНТР", "КОСМИЧЕСКИЙ ЦЕНТР", "АУКЦИОННЫЙ ДОМ", "ИЗДАТЕЛЬСТВО", "ИЗДАТЕЛЬСКИЙ ДОМ", "ТОРГОВЫЙ КОМПЛЕКС", "ТОРГОВО РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС", "АГЕНТСТВО НЕДВИЖИМОСТИ", "ГРУППА КОМПАНИЙ", "МЕДИАГРУППА", "МАГАЗИН", "ТОРГОВЫЙ КОМПЛЕКС", "ГИПЕРМАРКЕТ", "СУПЕРМАРКЕТ", "КАФЕ", "РЕСТОРАН", "БАР", "АУКЦИОН", "АНАЛИТИЧЕСКИЙ ЦЕНТР", "COMPANY", "CORPORATION"]: 
            t = OrgItemTermin._new2162(s, 3, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "ИЗДАТЕЛЬСТВО"): 
                t.addAbridge("ИЗД-ВО")
                t.addAbridge("ИЗ-ВО")
                t.profiles.append(OrgProfile.MEDIA)
                t.profiles.append(OrgProfile.PRESS)
                t.addVariant("ИЗДАТЕЛЬСКИЙ ДОМ", False)
            elif (s.startswith("ИЗДАТ")): 
                t.profiles.append(OrgProfile.PRESS)
                t.profiles.append(OrgProfile.MEDIA)
            elif (s == "ТОРГОВЫЙ ДОМ"): 
                t.acronym = "ТД"
            elif (s == "ТОРГОВЫЙ ЦЕНТР"): 
                t.acronym = "ТЦ"
            elif (s == "ТОРГОВЫЙ КОМПЛКС"): 
                t.acronym = "ТК"
            elif (s == "ГРУППА КОМПАНИЙ"): 
                t.acronym = "ГК"
            if (s.startswith("МЕДИА")): 
                t.profiles.append(OrgProfile.MEDIA)
            if (s.endswith(" ЦЕНТР")): 
                t.coeff = 3.5
            if (s == "КОМПАНИЯ" or s == "ФИРМА"): 
                t.coeff = (1)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ФІРМА", "КОМПАНІЯ", "КОРПОРАЦІЯ", "ДЕРЖКОРПОРАЦІЯ", "КОНЦЕРН", "КОНСОРЦІУМ", "ХОЛДИНГ", "МЕДІАХОЛДИНГ", "ТОРГОВИЙ ДІМ", "ТОРГОВИЙ ЦЕНТР", "НАВЧАЛЬНИЙ ЦЕНТР", "ВИДАВНИЦТВО", "ВИДАВНИЧИЙ ДІМ", "ТОРГОВИЙ КОМПЛЕКС", "ТОРГОВО-РОЗВАЖАЛЬНИЙ КОМПЛЕКС", "АГЕНТСТВО НЕРУХОМОСТІ", "ГРУПА КОМПАНІЙ", "МЕДІАГРУПА", "МАГАЗИН", "ТОРГОВИЙ КОМПЛЕКС", "ГІПЕРМАРКЕТ", "СУПЕРМАРКЕТ", "КАФЕ", "БАР", "АУКЦІОН", "АНАЛІТИЧНИЙ ЦЕНТР"]: 
            t = OrgItemTermin._new2163(s, MorphLang.UA, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "ВИДАВНИЦТВО"): 
                t.addAbridge("ВИД-ВО")
                t.addVariant("ВИДАВНИЧИЙ ДІМ", False)
            elif (s == "ТОРГОВИЙ ДІМ"): 
                t.acronym = "ТД"
            elif (s == "ТОРГОВИЙ ЦЕНТР"): 
                t.acronym = "ТЦ"
            elif (s == "ТОРГОВИЙ КОМПЛЕКС"): 
                t.acronym = "ТК"
            elif (s == "ГРУПА КОМПАНІЙ"): 
                t.acronym = "ГК"
            elif (s == "КОМПАНІЯ" or s == "ФІРМА"): 
                t.coeff = (1)
            if (s.startswith("МЕДІА")): 
                t.profiles.append(OrgProfile.MEDIA)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2164("РОК ГРУППА", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        t.addVariant("РОКГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2164("ПАНК ГРУППА", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        t.addVariant("ПАНКГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2164("ОРКЕСТР", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2164("ХОР", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2164("МУЗЫКАЛЬНЫЙ КОЛЛЕКТИВ", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        t.addVariant("РОКГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2169("ВОКАЛЬНО ИНСТРУМЕНТАЛЬНЫЙ АНСАМБЛЬ", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True, "ВИА")
        t.addVariant("ИНСТРУМЕНТАЛЬНЫЙ АНСАМБЛЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["НОТАРИАЛЬНАЯ КОНТОРА", "АДВОКАТСКОЕ БЮРО", "СТРАХОВОЕ ОБЩЕСТВО", "ЮРИДИЧЕСКИЙ ДОМ"]: 
            t = OrgItemTermin._new2170(s, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["НОТАРІАЛЬНА КОНТОРА", "АДВОКАТСЬКЕ БЮРО", "СТРАХОВЕ ТОВАРИСТВО"]: 
            t = OrgItemTermin._new2171(s, MorphLang.UA, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ГАЗЕТА", "ЕЖЕНЕДЕЛЬНИК", "ТАБЛОИД", "ЕЖЕНЕДЕЛЬНЫЙ ЖУРНАЛ", "NEWSPAPER", "WEEKLY", "TABLOID", "MAGAZINE"]: 
            t = OrgItemTermin._new2172(s, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            t.profiles.append(OrgProfile.PRESS)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ГАЗЕТА", "ТИЖНЕВИК", "ТАБЛОЇД"]: 
            t = OrgItemTermin._new2173(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            t.profiles.append(OrgProfile.PRESS)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["РАДИОСТАНЦИЯ", "РАДИО", "ТЕЛЕКАНАЛ", "ТЕЛЕКОМПАНИЯ", "НОВОСТНОЙ ПОРТАЛ", "ИНТЕРНЕТ ПОРТАЛ", "ИНТЕРНЕТ ИЗДАНИЕ", "ИНТЕРНЕТ РЕСУРС"]: 
            t = OrgItemTermin._new2172(s, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            if (s == "РАДИО"): 
                t.canonic_text = "РАДИОСТАНЦИЯ"
                t.is_doubt_word = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["РАДІО", "РАДІО", "ТЕЛЕКАНАЛ", "ТЕЛЕКОМПАНІЯ", "НОВИННИЙ ПОРТАЛ", "ІНТЕРНЕТ ПОРТАЛ", "ІНТЕРНЕТ ВИДАННЯ", "ІНТЕРНЕТ РЕСУРС"]: 
            t = OrgItemTermin._new2173(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            if (s == "РАДІО"): 
                t.canonic_text = "РАДІОСТАНЦІЯ"
                t.is_doubt_word = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПАНСИОНАТ", "САНАТОРИЙ", "ДОМ ОТДЫХА", "ОТЕЛЬ", "ГОСТИНИЦА", "SPA-ОТЕЛЬ", "ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", "ДЕТСКИЙ ЛАГЕРЬ", "ПИОНЕРСКИЙ ЛАГЕРЬ", "БАЗА ОТДЫХА", "СПОРТ-КЛУБ"]: 
            t = OrgItemTermin._new2162(s, 3, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "САНАТОРИЙ"): 
                t.addAbridge("САН.")
            elif (s == "ДОМ ОТДЫХА"): 
                t.addAbridge("Д.О.")
                t.addAbridge("ДОМ ОТД.")
                t.addAbridge("Д.ОТД.")
            elif (s == "ПАНСИОНАТ"): 
                t.addAbridge("ПАНС.")
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПАНСІОНАТ", "САНАТОРІЙ", "БУДИНОК ВІДПОЧИНКУ", "ГОТЕЛЬ", "SPA-ГОТЕЛЬ", "ОЗДОРОВЧИЙ ТАБІР", "БАЗА ВІДПОЧИНКУ", "СПОРТ-КЛУБ"]: 
            t = OrgItemTermin._new2177(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "САНАТОРІЙ"): 
                t.addAbridge("САН.")
            OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2178("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", 3, OrgItemTermin.Types.ORG, "ДОЛ", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2178("ДЕТСКИЙ СПОРТИВНЫЙ ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", 3, OrgItemTermin.Types.ORG, "ДСОЛ", True, True, True))
        for s in ["КОЛХОЗ", "САДОВО ОГОРОДНОЕ ТОВАРИЩЕСТВО", "КООПЕРАТИВ", "ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "КРЕСТЬЯНСКО ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "АГРОФИРМА", "КОНЕЗАВОД", "ПТИЦЕФЕРМА", "СВИНОФЕРМА", "ФЕРМА", "ЛЕСПРОМХОЗ"]: 
            t = OrgItemTermin._new2180(s, 3, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["КОЛГОСП", "САДОВО ГОРОДНЄ ТОВАРИСТВО", "КООПЕРАТИВ", "ФЕРМЕРСЬКЕ ГОСПОДАРСТВО", "СЕЛЯНСЬКО ФЕРМЕРСЬКЕ ГОСПОДАРСТВО", "АГРОФІРМА", "КОНЕЗАВОД", "ПТАХОФЕРМА", "СВИНОФЕРМА", "ФЕРМА"]: 
            t = OrgItemTermin._new2181(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("АВТОМОБИЛЬНЫЙ ЗАВОД", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addVariant("АВТОЗАВОД", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("АВТОМОБИЛЬНЫЙ ЦЕНТР", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addVariant("АВТОЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("СОВХОЗ", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addAbridge("С/Х")
        t.addAbridge("С-З")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("ПЛЕМЕННОЕ ХОЗЯЙСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addVariant("ПЛЕМХОЗ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("ЛЕСНОЕ ХОЗЯЙСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addVariant("ЛЕСХОЗ", False)
        OrgItemTypeToken.__m_global.add(t)
        sads = ["Садоводческое некоммерческое товарищество", "СНТ", "Дачное некоммерческое товарищество", "ДНТ", "Огородническое некоммерческое товарищество", "ОНТ", "Садоводческое некоммерческое партнерство", "СНП", "Дачное некоммерческое партнерство", "ДНП", "Огородническое некоммерческое партнерство", "ОНП", "Садоводческий потребительский кооператив", "СПК", "Дачный потребительский кооператив", "ДПК", "Огороднический потребительский кооператив", "ОПК"]
        i = 0
        while i < len(sads): 
            t = OrgItemTermin._new2187(sads[i].upper(), 3, sads[i + 1], OrgItemTermin.Types.ORG, True, True, True)
            t.addAbridge(sads[i + 1])
            if (t.acronym == "СНТ"): 
                t.addAbridge("САДОВ.НЕКОМ.ТОВ.")
            OrgItemTypeToken.__m_global.add(t)
            i += 2
        t = OrgItemTermin._new2180("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addAbridge("САДОВОДЧ.ТОВ.")
        t.addAbridge("САДОВ.ТОВ.")
        t.addAbridge("САД.ТОВ.")
        t.addAbridge("С.Т.")
        t.addVariant("САДОВОЕ ТОВАРИЩЕСТВО", False)
        t.addVariant("САДОВ. ТОВАРИЩЕСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("САДОВОДЧЕСКИЙ КООПЕРАТИВ", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addAbridge("САДОВОДЧ.КООП.")
        t.addAbridge("САДОВ.КООП.")
        t.addVariant("САДОВЫЙ КООПЕРАТИВ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2180("ДАЧНОЕ ТОВАРИЩЕСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.addAbridge("ДАЧН.ТОВ.")
        t.addAbridge("ДАЧ.ТОВ.")
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ФЕСТИВАЛЬ", "ЧЕМПИОНАТ", "ОЛИМПИАДА", "КОНКУРС"]: 
            t = OrgItemTermin._new1761(s, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ФЕСТИВАЛЬ", "ЧЕМПІОНАТ", "ОЛІМПІАДА"]: 
            t = OrgItemTermin._new2192(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1863("ПОГРАНИЧНЫЙ ПОСТ", 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ПОГП", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1863("ПОГРАНИЧНАЯ ЗАСТАВА", 3, OrgItemTermin.Types.ORG, True, True)
        t.addVariant("ПОГЗ", False)
        t.addVariant("ПОГРАНЗАСТАВА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1845("ТЕРРИТОРИАЛЬНЫЙ ПУНКТ", 3, OrgItemTermin.Types.DEP, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1845("МИГРАЦИОННЫЙ ПУНКТ", 3, OrgItemTermin.Types.DEP, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken._m_pref_words = TerminCollection()
        for s in ["КАПИТАЛ", "РУКОВОДСТВО", "СЪЕЗД", "СОБРАНИЕ", "СОВЕТ", "УПРАВЛЕНИЕ", "ДЕПАРТАМЕНТ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin(s))
        for s in ["КАПІТАЛ", "КЕРІВНИЦТВО", "ЗЇЗД", "ЗБОРИ", "РАДА", "УПРАВЛІННЯ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin._new898(s, MorphLang.UA))
        for s in ["АКЦИЯ", "ВЛАДЕЛЕЦ", "ВЛАДЕЛИЦА", "СОВЛАДЕЛЕЦ", "СОВЛАДЕЛИЦА", "КОНКУРЕНТ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin._new118(s, s))
        for s in ["АКЦІЯ", "ВЛАСНИК", "ВЛАСНИЦЯ", "СПІВВЛАСНИК", "СПІВВЛАСНИЦЯ", "КОНКУРЕНТ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin._new119(s, s, MorphLang.UA))
        for k in range(3):
            name_ = ("pattrs_ru.dat" if k == 0 else ("pattrs_ua.dat" if k == 1 else "pattrs_en.dat"))
            dat = EpNerOrgInternalResourceHelper.getBytes(name_)
            if (dat is None): 
                raise Utils.newException("Can't file resource file {0} in Organization analyzer".format(name_), None)
            with io.BytesIO(OrgItemTypeToken._deflate(dat)) as tmp: 
                tmp.seek(0, io.SEEK_SET)
                xml0_ = None # new XmlDocument
                xml0_ = xml.etree.ElementTree.parse(tmp)
                for x in xml0_.getroot(): 
                    if (k == 0): 
                        OrgItemTypeToken._m_pref_words.add(Termin._new118(Utils.getXmlInnerText(x), 1))
                    elif (k == 1): 
                        OrgItemTypeToken._m_pref_words.add(Termin._new119(Utils.getXmlInnerText(x), 1, MorphLang.UA))
                    elif (k == 2): 
                        OrgItemTypeToken._m_pref_words.add(Termin._new119(Utils.getXmlInnerText(x), 1, MorphLang.EN))
        OrgItemTypeToken._m_key_words_for_refs = TerminCollection()
        for s in ["КОМПАНИЯ", "ФИРМА", "ПРЕДПРИЯТИЕ", "КОРПОРАЦИЯ", "ВЕДОМСТВО", "УЧРЕЖДЕНИЕ", "КОМПАНІЯ", "ФІРМА", "ПІДПРИЄМСТВО", "КОРПОРАЦІЯ", "ВІДОМСТВО", "УСТАНОВА"]: 
            OrgItemTypeToken._m_key_words_for_refs.add(Termin(s))
        for s in ["ЧАСТЬ", "БАНК", "ЗАВОД", "ФАБРИКА", "АЭРОПОРТ", "БИРЖА", "СЛУЖБА", "МИНИСТЕРСТВО", "КОМИССИЯ", "КОМИТЕТ", "ГРУППА", "ЧАСТИНА", "БАНК", "ЗАВОД", "ФАБРИКА", "АЕРОПОРТ", "БІРЖА", "СЛУЖБА", "МІНІСТЕРСТВО", "КОМІСІЯ", "КОМІТЕТ", "ГРУПА"]: 
            OrgItemTypeToken._m_key_words_for_refs.add(Termin._new118(s, s))
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    @staticmethod
    def _deflate(zip0_ : bytearray) -> bytearray:
        with io.BytesIO() as unzip: 
            data = io.BytesIO(zip0_)
            data.seek(0, io.SEEK_SET)
            MorphSerializeHelper.deflateGzip(data, unzip)
            data.close()
            return bytearray(unzip.getvalue())
    
    M_EMPTY_TYP_WORDS = None
    
    __m_decree_key_words = None
    
    @staticmethod
    def isDecreeKeyword(t : 'Token', cou : int=1) -> bool:
        if (t is None): 
            return False
        i = 0
        while (i < cou) and t is not None: 
            if (t.is_newline_after): 
                break
            if (not t.chars.is_cyrillic_letter): 
                break
            for d in OrgItemTypeToken.__m_decree_key_words: 
                if (t.isValue(d, None)): 
                    return True
            i += 1; t = t.previous
        return False
    
    @staticmethod
    def _new1720(_arg1 : 'Token', _arg2 : 'Token', _arg3 : float) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.__m_coef = _arg3
        return res
    
    @staticmethod
    def _new1721(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : float, _arg5 : bool) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.coef = _arg4
        res.is_dep = _arg5
        return res
    
    @staticmethod
    def _new1722(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1725(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'OrgItemTermin', _arg5 : bool) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.root = _arg4
        res.is_not_typ = _arg5
        return res
    
    @staticmethod
    def _new1729(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'OrgItemTermin') -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.root = _arg4
        return res
    
    @staticmethod
    def _new1733(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : str, _arg5 : float, _arg6 : 'OrgItemTermin') -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.name = _arg4
        res.coef = _arg5
        res.root = _arg6
        return res
    
    @staticmethod
    def _new1734(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : str, _arg5 : 'OrgItemTermin', _arg6 : bool) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        res.root = _arg5
        res.can_be_organization = _arg6
        return res
    
    @staticmethod
    def _new1735(_arg1 : 'Token', _arg2 : 'Token', _arg3 : float, _arg4 : bool, _arg5 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.coef = _arg3
        res.is_not_typ = _arg4
        res.typ = _arg5
        return res
    
    @staticmethod
    def _new1737(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'OrgItemTermin', _arg4 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.root = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1739(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'OrgItemTermin', _arg5 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.root = _arg4
        res.name = _arg5
        return res
    
    @staticmethod
    def _new1740(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection', _arg5 : 'CharsInfo', _arg6 : 'CharsInfo') -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.name = _arg3
        res.morph = _arg4
        res.chars = _arg5
        res.chars_root = _arg6
        return res
    
    # static constructor for class OrgItemTypeToken
    @staticmethod
    def _static_ctor():
        OrgItemTypeToken.__m_org_adjactives = ["РОССИЙСКИЙ", "ВСЕРОССИЙСКИЙ", "МЕЖДУНАРОДНЫЙ", "ВСЕМИРНЫЙ", "ЕВРОПЕЙСКИЙ", "ГОСУДАРСТВЕННЫЙ", "НЕГОСУДАРСТВЕННЫЙ", "ФЕДЕРАЛЬНЫЙ", "РЕГИОНАЛЬНЫЙ", "ОБЛАСТНОЙ", "ГОРОДСКОЙ", "МУНИЦИПАЛЬНЫЙ", "АВТОНОМНЫЙ", "НАЦИОНАЛЬНЫЙ", "МЕЖРАЙОННЫЙ", "РАЙОННЫЙ", "ОТРАСЛЕВОЙ", "МЕЖОТРАСЛЕВОЙ", "НАРОДНЫЙ", "ВЕРХОВНЫЙ", "УКРАИНСКИЙ", "ВСЕУКРАИНСКИЙ", "РУССКИЙ"]
        OrgItemTypeToken.__m_org_adjactivesua = ["РОСІЙСЬКИЙ", "ВСЕРОСІЙСЬКИЙ", "МІЖНАРОДНИЙ", "СВІТОВИЙ", "ЄВРОПЕЙСЬКИЙ", "ДЕРЖАВНИЙ", "НЕДЕРЖАВНИЙ", "ФЕДЕРАЛЬНИЙ", "РЕГІОНАЛЬНИЙ", "ОБЛАСНИЙ", "МІСЬКИЙ", "МУНІЦИПАЛЬНИЙ", "АВТОНОМНИЙ", "НАЦІОНАЛЬНИЙ", "МІЖРАЙОННИЙ", "РАЙОННИЙ", "ГАЛУЗЕВИЙ", "МІЖГАЛУЗЕВИЙ", "НАРОДНИЙ", "ВЕРХОВНИЙ", "УКРАЇНСЬКИЙ", "ВСЕУКРАЇНСЬКИЙ", "РОСІЙСЬКА"]
        OrgItemTypeToken.__m_org_adjactives2 = ["КОММЕРЧЕСКИЙ", "НЕКОММЕРЧЕСКИЙ", "БЮДЖЕТНЫЙ", "КАЗЕННЫЙ", "БЛАГОТВОРИТЕЛЬНЫЙ", "СОВМЕСТНЫЙ", "ИНОСТРАННЫЙ", "ИССЛЕДОВАТЕЛЬСКИЙ", "ОБРАЗОВАТЕЛЬНЫЙ", "ОБЩЕОБРАЗОВАТЕЛЬНЫЙ", "ВЫСШИЙ", "УЧЕБНЫЙ", "СПЕЦИАЛИЗИРОВАННЫЙ", "ГЛАВНЫЙ", "ЦЕНТРАЛЬНЫЙ", "ТЕХНИЧЕСКИЙ", "ТЕХНОЛОГИЧЕСКИЙ", "ВОЕННЫЙ", "ПРОМЫШЛЕННЫЙ", "ТОРГОВЫЙ", "СИНОДАЛЬНЫЙ", "МЕДИЦИНСКИЙ", "ДИАГНОСТИЧЕСКИЙ", "ДЕТСКИЙ", "АКАДЕМИЧЕСКИЙ", "ПОЛИТЕХНИЧЕСКИЙ", "ИНВЕСТИЦИОННЫЙ", "ТЕРРОРИСТИЧЕСКИЙ", "РАДИКАЛЬНЫЙ", "ИСЛАМИСТСКИЙ", "ЛЕВОРАДИКАЛЬНЫЙ", "ПРАВОРАДИКАЛЬНЫЙ", "ОППОЗИЦИОННЫЙ", "НЕФТЯНОЙ", "ГАЗОВЫЙ", "ВЕЛИКИЙ"]
        OrgItemTypeToken.__m_org_adjactives2ua = ["КОМЕРЦІЙНИЙ", "НЕКОМЕРЦІЙНИЙ", "БЮДЖЕТНИЙ", "КАЗЕННИМ", "БЛАГОДІЙНИЙ", "СПІЛЬНИЙ", "ІНОЗЕМНИЙ", "ДОСЛІДНИЦЬКИЙ", "ОСВІТНІЙ", "ЗАГАЛЬНООСВІТНІЙ", "ВИЩИЙ", "НАВЧАЛЬНИЙ", "СПЕЦІАЛІЗОВАНИЙ", "ГОЛОВНИЙ", "ЦЕНТРАЛЬНИЙ", "ТЕХНІЧНИЙ", "ТЕХНОЛОГІЧНИЙ", "ВІЙСЬКОВИЙ", "ПРОМИСЛОВИЙ", "ТОРГОВИЙ", "СИНОДАЛЬНИЙ", "МЕДИЧНИЙ", "ДІАГНОСТИЧНИЙ", "ДИТЯЧИЙ", "АКАДЕМІЧНИЙ", "ПОЛІТЕХНІЧНИЙ", "ІНВЕСТИЦІЙНИЙ", "ТЕРОРИСТИЧНИЙ", "РАДИКАЛЬНИЙ", "ІСЛАМІЗМ", "ЛІВОРАДИКАЛЬНИЙ", "ПРАВОРАДИКАЛЬНИЙ", "ОПОЗИЦІЙНИЙ", "НАФТОВИЙ", "ГАЗОВИЙ", "ВЕЛИКИЙ"]
        OrgItemTypeToken.M_EMPTY_TYP_WORDS = ["КРУПНЫЙ", "КРУПНЕЙШИЙ", "ИЗВЕСТНЫЙ", "ИЗВЕСТНЕЙШИЙ", "МАЛОИЗВЕСТНЫЙ", "ЗАРУБЕЖНЫЙ", "ВЛИЯТЕЛЬНЫЙ", "ВЛИЯТЕЛЬНЕЙШИЙ", "ЗНАМЕНИТЫЙ", "НАЙБІЛЬШИЙ", "ВІДОМИЙ", "ВІДОМИЙ", "МАЛОВІДОМИЙ", "ЗАКОРДОННИЙ"]
        OrgItemTypeToken.__m_decree_key_words = ["УКАЗ", "УКАЗАНИЕ", "ПОСТАНОВЛЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПРИКАЗ", "ДИРЕКТИВА", "ПИСЬМО", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦИЯ", "РЕШЕНИЕ", "ПОЛОЖЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПОРУЧЕНИЕ", "ДОГОВОР", "СУБДОГОВОР", "АГЕНТСКИЙ ДОГОВОР", "ОПРЕДЕЛЕНИЕ", "СОГЛАШЕНИЕ", "ПРОТОКОЛ", "УСТАВ", "ХАРТИЯ", "РЕГЛАМЕНТ", "КОНВЕНЦИЯ", "ПАКТ", "БИЛЛЬ", "ДЕКЛАРАЦИЯ", "ТЕЛЕФОНОГРАММА", "ТЕЛЕФАКСОГРАММА", "ФАКСОГРАММА", "ПРАВИЛО", "ПРОГРАММА", "ПЕРЕЧЕНЬ", "ПОСОБИЕ", "РЕКОМЕНДАЦИЯ", "НАСТАВЛЕНИЕ", "СТАНДАРТ", "СОГЛАШЕНИЕ", "МЕТОДИКА", "ТРЕБОВАНИЕ", "УКАЗ", "ВКАЗІВКА", "ПОСТАНОВА", "РОЗПОРЯДЖЕННЯ", "НАКАЗ", "ДИРЕКТИВА", "ЛИСТ", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦІЯ", "РІШЕННЯ", "ПОЛОЖЕННЯ", "РОЗПОРЯДЖЕННЯ", "ДОРУЧЕННЯ", "ДОГОВІР", "СУБКОНТРАКТ", "АГЕНТСЬКИЙ ДОГОВІР", "ВИЗНАЧЕННЯ", "УГОДА", "ПРОТОКОЛ", "СТАТУТ", "ХАРТІЯ", "РЕГЛАМЕНТ", "КОНВЕНЦІЯ", "ПАКТ", "БІЛЛЬ", "ДЕКЛАРАЦІЯ", "ТЕЛЕФОНОГРАМА", "ТЕЛЕФАКСОГРАММА", "ФАКСОГРАМА", "ПРАВИЛО", "ПРОГРАМА", "ПЕРЕЛІК", "ДОПОМОГА", "РЕКОМЕНДАЦІЯ", "ПОВЧАННЯ", "СТАНДАРТ", "УГОДА", "МЕТОДИКА", "ВИМОГА"]

OrgItemTypeToken._static_ctor()