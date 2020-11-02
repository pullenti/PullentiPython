# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class MailLine(MetaToken):
    
    class Types(IntEnum):
        UNDEFINED = 0
        HELLO = 1
        BESTREGARDS = 2
        FROM = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.lev = 0
        self.typ = MailLine.Types.UNDEFINED
        self.refs = list()
        self.must_be_first_line = False
    
    @property
    def chars_count(self) -> int:
        cou = 0
        t = self.begin_token
        while t is not None: 
            cou += t.length_char
            if (t == self.end_token): 
                break
            t = t.next0_
        return cou
    
    @property
    def words(self) -> int:
        cou = 0
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if ((isinstance(t, TextToken)) and t.chars.is_letter and t.length_char > 2): 
                if (t.tag is None): 
                    cou += 1
            t = t.next0_
        return cou
    
    @property
    def is_pure_en(self) -> bool:
        en = 0
        ru = 0
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                if (t.chars.is_cyrillic_letter): 
                    ru += 1
                elif (t.chars.is_latin_letter): 
                    en += 1
            t = t.next0_
        if (en > 0 and ru == 0): 
            return True
        return False
    
    @property
    def is_pure_ru(self) -> bool:
        en = 0
        ru = 0
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                if (t.chars.is_cyrillic_letter): 
                    ru += 1
                elif (t.chars.is_latin_letter): 
                    en += 1
            t = t.next0_
        if (ru > 0 and en == 0): 
            return True
        return False
    
    @property
    def mail_addr(self) -> 'Referent':
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if (t.get_referent() is not None and t.get_referent().type_name == "URI"): 
                if (t.get_referent().get_string_value("SCHEME") == "mailto"): 
                    return t.get_referent()
            t = t.next0_
        return None
    
    @property
    def is_real_from(self) -> bool:
        tt = Utils.asObjectOrNull(self.begin_token, TextToken)
        if (tt is None): 
            return False
        return tt.term == "FROM" or tt.term == "ОТ"
    
    def __str__(self) -> str:
        return "{0}{1} {2}: {3}".format(("(1) " if self.must_be_first_line else ""), self.lev, Utils.enumToString(self.typ), self.get_source_text())
    
    @staticmethod
    def parse(t0 : 'Token', lev_ : int, max_count : int=0) -> 'MailLine':
        if (t0 is None): 
            return None
        res = MailLine(t0, t0)
        pr = True
        cou = 0
        t = t0
        first_pass3787 = True
        while True:
            if first_pass3787: first_pass3787 = False
            else: t = t.next0_; cou += 1
            if (not (t is not None)): break
            if (t.is_newline_before and t0 != t): 
                break
            if (max_count > 0 and cou > max_count): 
                break
            res.end_token = t
            if (t.is_table_control_char or t.is_hiphen): 
                continue
            if (pr): 
                if ((isinstance(t, TextToken)) and t.is_char_of(">|")): 
                    res.lev += 1
                else: 
                    pr = False
                    tok = MailLine.M_FROM_WORDS.try_parse(t, TerminParseAttr.NO)
                    if (tok is not None and tok.end_token.next0_ is not None and tok.end_token.next0_.is_char(':')): 
                        res.typ = MailLine.Types.FROM
                        t = tok.end_token.next0_
                        continue
            if (isinstance(t, ReferentToken)): 
                r = t.get_referent()
                if (r is not None): 
                    if ((((isinstance(r, PersonReferent)) or (isinstance(r, GeoReferent)) or (isinstance(r, AddressReferent))) or r.type_name == "PHONE" or r.type_name == "URI") or (isinstance(r, PersonPropertyReferent)) or r.type_name == "ORGANIZATION"): 
                        res.refs.append(r)
        if (res.typ == MailLine.Types.UNDEFINED): 
            t = t0
            while t is not None and (t.end_char < res.end_char): 
                if (not t.is_hiphen and t.chars.is_letter): 
                    break
                t = t.next0_
            ok = 0
            nams = 0
            oth = 0
            last_comma = None
            first_pass3788 = True
            while True:
                if first_pass3788: first_pass3788 = False
                else: t = t.next0_
                if (not (t is not None and (t.end_char < res.end_char))): break
                if (isinstance(t.get_referent(), PersonReferent)): 
                    nams += 1
                    continue
                if (isinstance(t, TextToken)): 
                    if (not t.chars.is_letter): 
                        last_comma = t
                        continue
                    tok = MailLine.M_HELLO_WORDS.try_parse(t, TerminParseAttr.NO)
                    if (tok is not None): 
                        ok += 1
                        t = tok.end_token
                        continue
                    if (t.is_value("ВСЕ", None) or t.is_value("ALL", None) or t.is_value("TEAM", None)): 
                        nams += 1
                        continue
                    pit = PersonItemToken.try_attach(t, None, PersonItemToken.ParseAttr.NO, None)
                    if (pit is not None): 
                        nams += 1
                        t = pit.end_token
                        continue
                oth += 1
                if (oth > 3): 
                    if (ok > 0 and last_comma is not None): 
                        res.end_token = last_comma
                        oth = 0
                    break
            if ((oth < 3) and ok > 0): 
                res.typ = MailLine.Types.HELLO
        if (res.typ == MailLine.Types.UNDEFINED): 
            ok_words = 0
            if (t0.is_value("HAVE", None)): 
                pass
            t = t0
            first_pass3789 = True
            while True:
                if first_pass3789: first_pass3789 = False
                else: t = t.next0_
                if (not (t is not None and t.end_char <= res.end_char)): break
                if (not (isinstance(t, TextToken))): 
                    continue
                if (t.is_char('<')): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        continue
                if (not t.is_letters or t.is_table_control_char): 
                    continue
                tok = MailLine.M_REGARD_WORDS.try_parse(t, TerminParseAttr.NO)
                if (tok is not None): 
                    ok_words += 1
                    while t is not None and t.end_char <= tok.end_char: 
                        t.tag = (tok.termin)
                        t = t.next0_
                    t = tok.end_token
                    if ((isinstance(t.next0_, TextToken)) and t.next0_.morph.case_.is_genitive): 
                        t = t.next0_
                        first_pass3790 = True
                        while True:
                            if first_pass3790: first_pass3790 = False
                            else: t = t.next0_
                            if (not (t.end_char <= res.end_char)): break
                            if (t.morph.class0_.is_conjunction): 
                                continue
                            npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                            if (npt1 is None): 
                                break
                            if (not npt1.morph.case_.is_genitive): 
                                break
                            while t.end_char < npt1.end_char: 
                                t.tag = (t)
                                t = t.next0_
                            t.tag = (t)
                    continue
                if ((t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction or t.morph.class0_.is_misc) or t.is_value("C", None)): 
                    continue
                if ((ok_words > 0 and t.previous is not None and t.previous.is_comma) and t.previous.begin_char > t0.begin_char and not t.chars.is_all_lower): 
                    res.end_token = t.previous
                    break
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt is None): 
                    if ((res.end_char - t.end_char) > 10): 
                        ok_words = 0
                    break
                tok = MailLine.M_REGARD_WORDS.try_parse(npt.end_token, TerminParseAttr.NO)
                if (tok is not None and (isinstance(npt.end_token, TextToken))): 
                    term = npt.end_token.term
                    if (term == "ДЕЛ"): 
                        tok = (None)
                if (tok is None): 
                    if (npt.noun.is_value("НАДЕЖДА", None)): 
                        t.tag = (t)
                    elif (ok_words > 0 and t.is_value("NICE", None) and ((res.end_char - npt.end_char) < 13)): 
                        t.tag = (t)
                    else: 
                        ok_words = 0
                    break
                ok_words += 1
                while t is not None and t.end_char <= tok.end_char: 
                    t.tag = (tok.termin)
                    t = t.next0_
                t = tok.end_token
            if (ok_words > 0): 
                res.typ = MailLine.Types.BESTREGARDS
        if (res.typ == MailLine.Types.UNDEFINED): 
            t = t0
            while t is not None and (t.end_char < res.end_char): 
                if (not (isinstance(t, TextToken))): 
                    break
                elif (not t.is_hiphen and t.chars.is_letter): 
                    break
                t = t.next0_
            if (t is not None): 
                if (t != t0): 
                    pass
                if (((t.is_value("ПЕРЕСЫЛАЕМОЕ", None) or t.is_value("ПЕРЕАДРЕСОВАННОЕ", None))) and t.next0_ is not None and t.next0_.is_value("СООБЩЕНИЕ", None)): 
                    res.typ = MailLine.Types.FROM
                    res.must_be_first_line = True
                elif ((t.is_value("НАЧАЛО", None) and t.next0_ is not None and ((t.next0_.is_value("ПЕРЕСЫЛАЕМОЕ", None) or t.next0_.is_value("ПЕРЕАДРЕСОВАННОЕ", None)))) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("СООБЩЕНИЕ", None)): 
                    res.typ = MailLine.Types.FROM
                    res.must_be_first_line = True
                elif (t.is_value("ORIGINAL", None) and t.next0_ is not None and ((t.next0_.is_value("MESSAGE", None) or t.next0_.is_value("APPOINTMENT", None)))): 
                    res.typ = MailLine.Types.FROM
                    res.must_be_first_line = True
                elif (t.is_value("ПЕРЕСЛАНО", None) and t.next0_ is not None and t.next0_.is_value("ПОЛЬЗОВАТЕЛЕМ", None)): 
                    res.typ = MailLine.Types.FROM
                    res.must_be_first_line = True
                elif (((t.get_referent() is not None and t.get_referent().type_name == "DATE")) or ((t.is_value("IL", None) and t.next0_ is not None and t.next0_.is_value("GIORNO", None))) or ((t.is_value("ON", None) and (isinstance(t.next0_, ReferentToken)) and t.next0_.get_referent().type_name == "DATE"))): 
                    has_from = False
                    has_date = t.get_referent() is not None and t.get_referent().type_name == "DATE"
                    if (t.is_newline_after and (lev_ < 5)): 
                        res1 = MailLine.parse(t.next0_, lev_ + 1, 0)
                        if (res1 is not None and res1.typ == MailLine.Types.HELLO): 
                            res.typ = MailLine.Types.FROM
                    next0__ = MailLine.parse(res.end_token.next0_, lev_ + 1, 0)
                    if (next0__ is not None): 
                        if (next0__.typ != MailLine.Types.UNDEFINED): 
                            next0__ = (None)
                    tmax = res.end_char
                    if (next0__ is not None): 
                        tmax = next0__.end_char
                    br1 = None
                    while t is not None and t.end_char <= tmax: 
                        if (t.is_value("ОТ", None) or t.is_value("FROM", None)): 
                            has_from = True
                        elif (t.get_referent() is not None and ((t.get_referent().type_name == "URI" or (isinstance(t.get_referent(), PersonReferent))))): 
                            if (t.get_referent().type_name == "URI" and has_date): 
                                if (br1 is not None): 
                                    has_from = True
                                    next0__ = (None)
                                if (t.previous.is_char('<') and t.next0_ is not None and t.next0_.is_char('>')): 
                                    t = t.next0_
                                    if (t.next0_ is not None and t.next0_.is_char(':')): 
                                        t = t.next0_
                                    if (t.is_newline_after): 
                                        has_from = True
                                        next0__ = (None)
                            t = t.next0_
                            while t is not None and t.end_char <= res.end_char: 
                                if (t.is_value("HA", None) and t.next0_ is not None and t.next0_.is_value("SCRITTO", None)): 
                                    has_from = True
                                    break
                                elif (((t.is_value("НАПИСАТЬ", None) or t.is_value("WROTE", None))) and ((res.end_char - t.end_char) < 10)): 
                                    has_from = True
                                    break
                                t = t.next0_
                            if (has_from): 
                                res.typ = MailLine.Types.FROM
                                if (next0__ is not None and t.end_char >= next0__.begin_char): 
                                    res.end_token = next0__.end_token
                            break
                        elif (br1 is None and not t.is_char('<') and BracketHelper.can_be_start_of_sequence(t, True, False)): 
                            br1 = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                            if (br1 is not None): 
                                t = br1.end_token
                        t = t.next0_
                else: 
                    has_uri = False
                    while t is not None and (t.end_char < res.end_char): 
                        if (t.get_referent() is not None and ((t.get_referent().type_name == "URI" or (isinstance(t.get_referent(), PersonReferent))))): 
                            has_uri = True
                        elif (t.is_value("ПИСАТЬ", None) and has_uri): 
                            if (t.next0_ is not None and t.next0_.is_char('(')): 
                                if (has_uri): 
                                    res.typ = MailLine.Types.FROM
                                break
                        t = t.next0_
        return res
    
    M_REGARD_WORDS = None
    
    M_FROM_WORDS = None
    
    M_HELLO_WORDS = None
    
    @staticmethod
    def is_keyword(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (MailLine.M_REGARD_WORDS.try_parse(t, TerminParseAttr.NO) is not None): 
            return True
        if (MailLine.M_FROM_WORDS.try_parse(t, TerminParseAttr.NO) is not None): 
            return True
        if (MailLine.M_HELLO_WORDS.try_parse(t, TerminParseAttr.NO) is not None): 
            return True
        return False
    
    @staticmethod
    def initialize() -> None:
        if (MailLine.M_REGARD_WORDS is not None): 
            return
        MailLine.M_REGARD_WORDS = TerminCollection()
        for s in ["УВАЖЕНИЕ", "ПОЧТЕНИЕ", "С УВАЖЕНИЕМ", "ПОЖЕЛАНИE", "ДЕНЬ", "ХОРОШЕГО ДНЯ", "ИСКРЕННЕ ВАШ", "УДАЧА", "СПАСИБО", "ЦЕЛОВАТЬ", "ПОВАГА", "З ПОВАГОЮ", "ПОБАЖАННЯ", "ДЕНЬ", "ЩИРО ВАШ", "ДЯКУЮ", "ЦІЛУВАТИ", "BEST REGARDS", "REGARDS", "BEST WISHES", "KIND REGARDS", "GOOD BYE", "BYE", "THANKS", "THANK YOU", "MANY THANKS", "DAY", "VERY MUCH", "HAVE", "LUCK", "Yours sincerely", "sincerely Yours", "Looking forward", "Ar cieņu"]: 
            MailLine.M_REGARD_WORDS.add(Termin(s.upper()))
        MailLine.M_FROM_WORDS = TerminCollection()
        for s in ["FROM", "TO", "CC", "SENT", "SUBJECT", "SENDER", "TIME", "ОТ КОГО", "КОМУ", "ДАТА", "ТЕМА", "КОПИЯ", "ОТ", "ОТПРАВЛЕНО", "WHEN", "WHERE"]: 
            MailLine.M_FROM_WORDS.add(Termin(s))
        MailLine.M_HELLO_WORDS = TerminCollection()
        for s in ["HI", "HELLO", "DEAR", "GOOD MORNING", "GOOD DAY", "GOOD EVENING", "GOOD NIGHT", "ЗДРАВСТВУЙ", "ЗДРАВСТВУЙТЕ", "ПРИВЕТСТВУЮ", "ПРИВЕТ", "ПРИВЕТИК", "УВАЖАЕМЫЙ", "ДОРОГОЙ", "ЛЮБЕЗНЫЙ", "ДОБРОЕ УТРО", "ДОБРЫЙ ДЕНЬ", "ДОБРЫЙ ВЕЧЕР", "ДОБРОЙ НОЧИ", "ЗДРАСТУЙ", "ЗДРАСТУЙТЕ", "ВІТАЮ", "ПРИВІТ", "ПРИВІТ", "ШАНОВНИЙ", "ДОРОГИЙ", "ЛЮБИЙ", "ДОБРОГО РАНКУ", "ДОБРИЙ ДЕНЬ", "ДОБРИЙ ВЕЧІР", "ДОБРОЇ НОЧІ"]: 
            MailLine.M_HELLO_WORDS.add(Termin(s))