# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils

from pullenti.ner.denomination.DenominationReferent import DenominationReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.TextToken import TextToken
from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.phone.PhoneReferent import PhoneReferent
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.booklink.internal.BookLinkTyp import BookLinkTyp
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.titlepage.internal.TitleItemToken import TitleItemToken
from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.booklink.internal.BookLinkToken import BookLinkToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class TitleNameToken(MetaToken):
    """ Название статьи """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.rank = 0
        self.begin_name_token = None;
        self.end_name_token = None;
        self.type_value = None;
        self.speciality = None;
    
    def __str__(self) -> str:
        if (self.begin_name_token is None or self.end_name_token is None): 
            return "?"
        mt = MetaToken(self.begin_name_token, self.end_name_token)
        if (self.type_value is None): 
            return "{0}: {1}".format(self.rank, str(mt))
        else: 
            return "{0}: {1} ({2})".format(self.rank, str(mt), self.type_value)
    
    @staticmethod
    def sort(li : typing.List['TitleNameToken']) -> None:
        k = 0
        while k < len(li): 
            ch = False
            i = 0
            while i < (len(li) - 1): 
                if (li[i].rank < li[i + 1].rank): 
                    ch = True
                    v = li[i]
                    li[i] = li[i + 1]
                    li[i + 1] = v
                i += 1
            if (not ch): 
                break
            k += 1
    
    @staticmethod
    def can_be_start_of_text_or_content(begin : 'Token', end : 'Token') -> bool:
        if (begin.is_value("СОДЕРЖАНИЕ", "ЗМІСТ") or begin.is_value("ОГЛАВЛЕНИЕ", None) or begin.is_value("СОДЕРЖИМОЕ", None)): 
            t = begin
            if (t.next0_ is not None and t.next0_.is_char_of(":.")): 
                t = t.next0_
            if (t == end): 
                return True
        if (begin.is_value("ОТ", "ВІД") and begin.next0_ is not None and begin.next0_.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
            if (begin.next0_.next0_ is not None and begin.next0_.next0_.is_char(':')): 
                return True
        words = 0
        verbs = 0
        t = begin
        while t != end.next0_: 
            if (isinstance(t, TextToken)): 
                if (t.chars.is_letter): 
                    words += 1
                if (t.chars.is_all_lower and t.is_pure_verb): 
                    verbs += 1
            t = t.next0_
        if (words > 10 and verbs > 1): 
            return True
        return False
    
    @staticmethod
    def try_parse(begin : 'Token', end : 'Token', min_newlines_count : int) -> 'TitleNameToken':
        res = TitleNameToken(begin, end)
        if (not res.__calc_rank_and_value(min_newlines_count)): 
            return None
        if (res.begin_name_token is None or res.end_name_token is None): 
            return None
        return res
    
    def __calc_rank_and_value(self, min_newlines_count : int) -> bool:
        self.rank = 0
        if (self.begin_token.chars.is_all_lower): 
            self.rank -= 30
        words = 0
        up_words = 0
        notwords = 0
        line_number = 0
        tstart = self.begin_token
        tend = self.end_token
        t = self.begin_token
        first_pass3888 = True
        while True:
            if first_pass3888: first_pass3888 = False
            else: t = t.next0_
            if (not (t != self.end_token.next0_ and t is not None and t.end_char <= self.end_token.end_char)): break
            if (t.is_newline_before): 
                pass
            tit = TitleItemToken.try_attach(t)
            if (tit is not None): 
                if (tit.typ == TitleItemToken.Types.THEME or tit.typ == TitleItemToken.Types.TYPANDTHEME): 
                    if (t != self.begin_token): 
                        if (line_number > 0): 
                            return False
                        notwords = 0
                        up_words = notwords
                        words = up_words
                        tstart = tit.end_token.next0_
                    t = tit.end_token
                    if (t.next0_ is None): 
                        return False
                    if (t.next0_.chars.is_letter and t.next0_.chars.is_all_lower): 
                        self.rank += 20
                    else: 
                        self.rank += 100
                    tstart = t.next0_
                    if (tit.typ == TitleItemToken.Types.TYPANDTHEME): 
                        self.type_value = tit.value
                    continue
                if (tit.typ == TitleItemToken.Types.TYP): 
                    if (t == self.begin_token): 
                        if (tit.end_token.is_newline_after): 
                            self.type_value = tit.value
                            self.rank += 5
                            tstart = tit.end_token.next0_
                    t = tit.end_token
                    words += 1
                    if (tit.begin_token != tit.end_token): 
                        words += 1
                    if (tit.chars.is_all_upper): 
                        up_words += 1
                    continue
                if (tit.typ == TitleItemToken.Types.DUST or tit.typ == TitleItemToken.Types.SPECIALITY): 
                    if (t == self.begin_token): 
                        return False
                    self.rank -= 20
                    if (tit.typ == TitleItemToken.Types.SPECIALITY): 
                        self.speciality = tit.value
                    t = tit.end_token
                    continue
                if (tit.typ == TitleItemToken.Types.CONSULTANT or tit.typ == TitleItemToken.Types.BOSS or tit.typ == TitleItemToken.Types.EDITOR): 
                    t = tit.end_token
                    if (t.next0_ is not None and ((t.next0_.is_char_of(":") or t.next0_.is_hiphen or t.whitespaces_after_count > 4))): 
                        self.rank -= 10
                    else: 
                        self.rank -= 2
                    continue
                return False
            blt = BookLinkToken.try_parse(t, 0)
            if (blt is not None): 
                if (blt.typ == BookLinkTyp.MISC or blt.typ == BookLinkTyp.N or blt.typ == BookLinkTyp.PAGES): 
                    self.rank -= 10
                elif (blt.typ == BookLinkTyp.N or blt.typ == BookLinkTyp.PAGERANGE): 
                    self.rank -= 20
            if (t == self.begin_token and BookLinkToken.try_parse_author(t, FioTemplateType.UNDEFINED) is not None): 
                self.rank -= 20
            if (t.is_newline_before and t != self.begin_token): 
                line_number += 1
                if (line_number > 4): 
                    return False
                if (t.chars.is_all_lower): 
                    self.rank += 10
                elif (t.previous.is_char('.')): 
                    self.rank -= 10
                elif (t.previous.is_char_of(",-")): 
                    self.rank += 10
                else: 
                    npt = NounPhraseHelper.try_parse(t.previous, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.end_char >= t.end_char): 
                        self.rank += 10
            if (t != self.begin_token and t.newlines_before_count > min_newlines_count): 
                self.rank -= (t.newlines_before_count - min_newlines_count)
            bst = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (bst is not None and bst.is_quote_type and bst.end_token.end_char <= self.end_token.end_char): 
                if (words == 0): 
                    tstart = bst.begin_token
                    self.rank += 10
                    if (bst.end_token == self.end_token): 
                        tend = self.end_token
                        self.rank += 10
            rli = t.get_referents()
            if (rli is not None): 
                for r in rli: 
                    if (isinstance(r, OrganizationReferent)): 
                        if (t.is_newline_before): 
                            self.rank -= 10
                        else: 
                            self.rank -= 4
                        continue
                    if ((isinstance(r, GeoReferent)) or (isinstance(r, PersonReferent))): 
                        if (t.is_newline_before): 
                            self.rank -= 5
                            if (t.is_newline_after or t.next0_ is None): 
                                self.rank -= 20
                            elif (t.next0_.is_hiphen or (isinstance(t.next0_, NumberToken)) or (isinstance(t.next0_.get_referent(), DateReferent))): 
                                self.rank -= 20
                            elif (t != self.begin_token): 
                                self.rank -= 20
                        continue
                    if ((isinstance(r, GeoReferent)) or (isinstance(r, DenominationReferent))): 
                        continue
                    if ((isinstance(r, UriReferent)) or (isinstance(r, PhoneReferent))): 
                        return False
                    if (t.is_newline_before): 
                        self.rank -= 4
                    else: 
                        self.rank -= 2
                    if (t == self.begin_token and (isinstance(self.end_token.get_referent(), PersonReferent))): 
                        self.rank -= 10
                words += 1
                if (t.chars.is_all_upper): 
                    up_words += 1
                if (t == self.begin_token): 
                    if (t.is_newline_after): 
                        self.rank -= 10
                    elif (t.next0_ is not None and t.next0_.is_char('.') and t.next0_.is_newline_after): 
                        self.rank -= 10
                continue
            if (isinstance(t, NumberToken)): 
                if (t.typ == NumberSpellingType.WORDS): 
                    words += 1
                    if (t.chars.is_all_upper): 
                        up_words += 1
                else: 
                    notwords += 1
                continue
            pat = PersonAttrToken.try_attach(t, None, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (pat is not None): 
                if (t.is_newline_before): 
                    if (not pat.morph.case_.is_undefined and not pat.morph.case_.is_nominative): 
                        pass
                    elif (pat.chars.is_all_upper): 
                        pass
                    else: 
                        self.rank -= 20
                elif (t.chars.is_all_lower): 
                    self.rank -= 1
                while t is not None: 
                    words += 1
                    if (t.chars.is_all_upper): 
                        up_words += 1
                    if (t == pat.end_token): 
                        break
                    t = t.next0_
                continue
            oitt = OrgItemTypeToken.try_attach(t, True, None)
            if (oitt is not None): 
                if (oitt.morph.number != MorphNumber.PLURAL and not oitt.is_doubt_root_word): 
                    if (not oitt.morph.case_.is_undefined and not oitt.morph.case_.is_nominative): 
                        words += 1
                        if (t.chars.is_all_upper): 
                            up_words += 1
                    else: 
                        self.rank -= 4
                        if (t == self.begin_token): 
                            self.rank -= 5
                else: 
                    words += 1
                    if (t.chars.is_all_upper): 
                        up_words += 1
                t = oitt.end_token
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is not None): 
                if (tt.is_char('©')): 
                    self.rank -= 10
                if (tt.is_char('_')): 
                    self.rank -= 1
                if (tt.chars.is_letter): 
                    if (tt.length_char > 2): 
                        words += 1
                        if (t.chars.is_all_upper): 
                            up_words += 1
                elif (not tt.is_char(',')): 
                    notwords += 1
                if (tt.is_pure_verb): 
                    self.rank -= 30
                    words -= 1
                    break
                if (tt == self.end_token): 
                    if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                        self.rank -= 10
                    elif (tt.is_char('.')): 
                        self.rank += 5
                elif (tt.is_char_of("._")): 
                    self.rank -= 5
        self.rank += words
        self.rank -= notwords
        if ((words < 1) and (self.rank < 50)): 
            return False
        if (tstart is None or tend is None): 
            return False
        if (tstart.end_char > tend.end_char): 
            return False
        tit1 = TitleItemToken.try_attach(self.end_token.next0_)
        if (tit1 is not None and ((tit1.typ == TitleItemToken.Types.TYP or tit1.typ == TitleItemToken.Types.SPECIALITY))): 
            if (tit1.end_token.is_newline_after): 
                self.rank += 15
            else: 
                self.rank += 10
            if (tit1.typ == TitleItemToken.Types.SPECIALITY): 
                self.speciality = tit1.value
        if (up_words > 4 and up_words > (math.floor((0.8 * (words))))): 
            if (tstart.previous is not None and (isinstance(tstart.previous.get_referent(), PersonReferent))): 
                self.rank += (5 + up_words)
        self.begin_name_token = tstart
        self.end_name_token = tend
        return True