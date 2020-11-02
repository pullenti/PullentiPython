# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Token import Token
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.instrument.internal.ParticipantToken import ParticipantToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.decree.internal.PartToken import PartToken
from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
from pullenti.ner.decree.internal.DecreeToken import DecreeToken
from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.instrument.internal.NumberTypes import NumberTypes
from pullenti.ner.instrument.InstrumentParticipantReferent import InstrumentParticipantReferent
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.instrument.internal.FragToken import FragToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.instrument.internal.InstrToken import InstrToken
from pullenti.ner.core.TableHelper import TableHelper

class InstrToken1(MetaToken):
    
    class Types(IntEnum):
        LINE = 0
        FIRSTLINE = 1
        SIGNS = 2
        APPENDIX = 3
        APPROVED = 4
        BASE = 5
        INDEX = 6
        TITLE = 7
        DIRECTIVE = 8
        CHAPTER = 9
        CLAUSE = 10
        DOCPART = 11
        SECTION = 12
        SUBSECTION = 13
        PARAGRAPH = 14
        SUBPARAGRAPH = 15
        CLAUSEPART = 16
        EDITIONS = 17
        COMMENT = 18
        NOTICE = 19
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class StdTitleType(IntEnum):
        UNDEFINED = 0
        SUBJECT = 1
        REQUISITES = 2
        OTHERS = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.iref = None;
        self.is_expired = False
        self.numbers = list()
        self.min_number = None;
        self.num_typ = NumberTypes.UNDEFINED
        self.num_suffix = None;
        self.num_begin_token = None;
        self.num_end_token = None;
        self.is_num_doubt = False
        self.typ = InstrToken1.Types.LINE
        self.sign_values = list()
        self.value = None;
        self.all_upper = False
        self.has_verb = False
        self.has_many_spec_chars = False
        self.title_typ = InstrToken1.StdTitleType.UNDEFINED
        self.index_no_keyword = False
    
    @property
    def last_number(self) -> int:
        if (len(self.numbers) < 1): 
            return 0
        return PartToken.get_number(self.numbers[len(self.numbers) - 1])
    
    @property
    def first_number(self) -> int:
        if (len(self.numbers) < 1): 
            return 0
        return PartToken.get_number(self.numbers[0])
    
    @property
    def middle_number(self) -> int:
        if (len(self.numbers) < 2): 
            return 0
        return PartToken.get_number(self.numbers[1])
    
    @property
    def last_min_number(self) -> int:
        if (self.min_number is None): 
            return 0
        return PartToken.get_number(self.min_number)
    
    @property
    def has_changes(self) -> bool:
        t = Utils.ifNotNull(self.num_end_token, self.begin_token)
        while t is not None: 
            if (isinstance(t.get_referent(), DecreeChangeReferent)): 
                return True
            if (t.end_char > self.end_char): 
                break
            t = t.next0_
        return False
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} {1} ".format(Utils.enumToString(self.typ), Utils.enumToString(self.num_typ)), end="", file=res, flush=True)
        if (self.is_num_doubt): 
            print("(?) ", end="", file=res)
        if (self.is_expired): 
            print("(Expired) ", end="", file=res)
        if (self.has_changes): 
            print("(HasChanges) ", end="", file=res)
        i = 0
        while i < len(self.numbers): 
            print("{0}{1}".format(("." if i > 0 else ""), self.numbers[i]), end="", file=res, flush=True)
            i += 1
        if (self.num_suffix is not None): 
            print(" Suf='{0}'".format(self.num_suffix), end="", file=res, flush=True)
        if (self.value is not None): 
            print(" '{0}'".format(self.value), end="", file=res, flush=True)
        for s in self.sign_values: 
            print(" [{0}]".format(str(s)), end="", file=res, flush=True)
        if (self.all_upper): 
            print(" AllUpper", end="", file=res)
        if (self.has_verb): 
            print(" HasVerb", end="", file=res)
        if (self.has_many_spec_chars): 
            print(" HasManySpecChars", end="", file=res)
        if (self.title_typ != InstrToken1.StdTitleType.UNDEFINED): 
            print(" {0}".format(Utils.enumToString(self.title_typ)), end="", file=res, flush=True)
        if (self.value is None): 
            print(": {0}".format(self.get_source_text()), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def parse(t : 'Token', ignore_directives : bool, cur : 'FragToken'=None, lev : int=0, prev : 'InstrToken1'=None, is_citat : bool=False, max_char : int=0, can_be_table_cell : bool=False, is_in_index : bool=False) -> 'InstrToken1':
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        if (t is None): 
            return None
        if (t.is_char('(')): 
            edt = None
            fr = FragToken._create_editions(t)
            if (fr is not None): 
                edt = InstrToken1._new1532(fr.begin_token, fr.end_token, InstrToken1.Types.EDITIONS)
            else: 
                t2 = InstrToken1._create_edition(t)
                if (t2 is not None): 
                    edt = InstrToken1._new1532(t, t2, InstrToken1.Types.EDITIONS)
            if (edt is not None): 
                if (edt.end_token.next0_ is not None and edt.end_token.next0_.is_char('.')): 
                    edt.end_token = edt.end_token.next0_
                return edt
        t0 = t
        t00 = None
        res = InstrToken1._new1534(t0, t, True)
        while t is not None: 
            if (not t.is_table_control_char): 
                break
            else: 
                if (t.is_char(chr(0x1E))): 
                    is_table = False
                    rows = TableHelper.try_parse_rows(t, 0, True)
                    if (rows is not None and len(rows) > 0): 
                        is_table = True
                        if (len(rows[0].cells) > 2 or len(rows[0].cells) == 0): 
                            pass
                        elif (lev >= 10): 
                            is_table = False
                        else: 
                            it11 = InstrToken1.parse(rows[0].begin_token, True, None, 10, None, False, max_char, can_be_table_cell, False)
                            if (can_be_table_cell): 
                                if (it11 is not None): 
                                    return it11
                            if (it11 is not None and len(it11.numbers) > 0): 
                                if (it11.typ_container_rank > 0 or it11.last_number == 1 or it11.title_typ != InstrToken1.StdTitleType.UNDEFINED): 
                                    is_table = False
                    if (is_table): 
                        le = 1
                        t = t.next0_
                        while t is not None: 
                            if (t.is_char(chr(0x1E))): 
                                le += 1
                            elif (t.is_char(chr(0x1F))): 
                                le -= 1
                                if (le == 0): 
                                    res.end_token = t
                                    res.has_verb = True
                                    res.all_upper = False
                                    return res
                            t = t.next0_
                if (t is not None): 
                    res.end_token = t
            t = (None if t is None else t.next0_)
        if (t is None): 
            if (isinstance(t0, TextToken)): 
                return None
            t = res.end_token
        dt = DecreeToken.try_attach(t, None, False)
        if (dt is None and (((isinstance(t.get_referent(), PersonReferent)) or (isinstance(t.get_referent(), InstrumentParticipantReferent))))): 
            dt = DecreeToken._new842(t, t, DecreeToken.ItemType.OWNER)
            dt.ref = (Utils.asObjectOrNull(t, ReferentToken))
        if (dt is not None and dt.end_token.is_newline_after): 
            if (dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.NUMBER or dt.typ == DecreeToken.ItemType.OWNER): 
                res.typ = InstrToken1.Types.SIGNS
                res.sign_values.append(dt)
                res.end_token = dt.end_token
                res.all_upper = False
                return res
        if (t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК") and t.morph.case_.is_nominative and t.morph.number == MorphNumber.SINGULAR): 
            if (t.next0_ is not None and ((t.next0_.is_value("В", None) or t.next0_.is_char(':')))): 
                pass
            else: 
                res.typ = InstrToken1.Types.APPENDIX
                if (isinstance(t.get_referent(), DecreePartReferent)): 
                    t = t.kit.debed_token(t)
                t = t.next0_
                first_pass3756 = True
                while True:
                    if first_pass3756: first_pass3756 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if (res.num_end_token is None): 
                        ttt = Utils.ifNotNull(MiscHelper.check_number_prefix(t), t)
                        NumberingHelper.parse_number(ttt, res, prev)
                        if (res.num_end_token is not None): 
                            t = res.num_end_token
                            res.end_token = t
                            continue
                    dt = DecreeToken.try_attach(t, None, False)
                    if (dt is not None): 
                        if (dt.typ == DecreeToken.ItemType.NUMBER): 
                            res.num_begin_token = dt.begin_token
                            res.num_end_token = dt.end_token
                            if (dt.value is not None): 
                                res.numbers.append(dt.value.upper())
                        res.end_token = dt.end_token
                        t = res.end_token
                        continue
                    if ((isinstance(t, NumberToken)) and ((t.is_newline_after or ((t.next0_ is not None and t.next0_.is_char('.') and t.next0_.is_newline_after))))): 
                        res.num_begin_token = t
                        res.numbers.append(str(t.value))
                        if (t.next0_ is not None and t.next0_.is_char('.')): 
                            t = t.next0_
                        res.num_end_token = t
                        res.end_token = t
                        continue
                    if (((isinstance(t, NumberToken)) and (isinstance(t.next0_, TextToken)) and t.next0_.length_char == 1) and ((t.next0_.is_newline_after or ((t.next0_.next0_ is not None and t.next0_.next0_.is_char('.')))))): 
                        res.num_begin_token = t
                        res.numbers.append(str(t.value))
                        res.numbers.append(t.next0_.term)
                        res.num_typ = NumberTypes.COMBO
                        t = t.next0_
                        if (t.next0_ is not None and t.next0_.is_char('.')): 
                            t = t.next0_
                        res.num_end_token = t
                        res.end_token = t
                        continue
                    if (res.num_end_token is None): 
                        NumberingHelper.parse_number(t, res, prev)
                        if (res.num_end_token is not None): 
                            t = res.num_end_token
                            res.end_token = t
                            continue
                    if (t.is_value("К", "ДО") and t.next0_ is not None and (isinstance(t.next0_.get_referent(), DecreeReferent))): 
                        break
                    if (t.chars.is_letter): 
                        lat = NumberHelper.try_parse_roman(t)
                        if (lat is not None and not t.is_value("C", None) and not t.is_value("С", None)): 
                            res.num_begin_token = t
                            res.numbers.append(str(lat.value))
                            res.num_typ = NumberTypes.ROMAN
                            t = lat.end_token
                            if (t.next0_ is not None and ((t.next0_.is_char('.') or t.next0_.is_char(')')))): 
                                t = t.next0_
                            res.num_end_token = t
                            res.end_token = t
                            continue
                        if (t.length_char == 1 and t.chars.is_all_upper): 
                            res.num_begin_token = t
                            res.numbers.append(t.term)
                            res.num_typ = NumberTypes.LETTER
                            if (t.next0_ is not None and ((t.next0_.is_char('.') or t.next0_.is_char(')')))): 
                                t = t.next0_
                            res.num_end_token = t
                            res.end_token = t
                            continue
                    if (InstrToken._check_entered(t) is not None): 
                        break
                    if (isinstance(t, TextToken)): 
                        if (t.is_pure_verb): 
                            res.typ = InstrToken1.Types.LINE
                            break
                    break
                if (res.typ != InstrToken1.Types.LINE): 
                    return res
        if (t.is_newline_before): 
            if (t.is_value("МНЕНИЕ", "ДУМКА") or ((t.is_value("ОСОБОЕ", "ОСОБЛИВА") and t.next0_ is not None and t.next0_.is_value("МНЕНИЕ", "ДУМКА")))): 
                t1 = t.next0_
                if (t1 is not None and t1.is_value("МНЕНИЕ", "ДУМКА")): 
                    t1 = t1.next0_
                ok = False
                if (t1 is not None): 
                    if (t1.is_newline_before or (isinstance(t1.get_referent(), PersonReferent))): 
                        ok = True
                if (ok): 
                    res.typ = InstrToken1.Types.APPENDIX
                    res.end_token = t1.previous
                    return res
            if ((isinstance(t.get_referent(), DecreeReferent)) and t.get_referent().kind == DecreeKind.PUBLISHER): 
                res.typ = InstrToken1.Types.APPROVED
        if (t.is_value("КОНСУЛЬТАНТПЛЮС", None) or t.is_value("ГАРАНТ", None) or ((t.is_value("ИНФОРМАЦИЯ", None) and t.is_newline_before))): 
            t1 = t.next0_
            ok = False
            if (t.is_value("ИНФОРМАЦИЯ", None)): 
                if (((t.next0_ is not None and t.next0_.is_value("О", None) and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("ИЗМЕНЕНИЕ", None) and t.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.is_char(':')): 
                    t1 = t.next0_.next0_.next0_.next0_
                    ok = True
            elif (t1 is not None and t1.is_char(':')): 
                t1 = t1.next0_
                ok = True
            if (t1 is not None and ((t1.is_value("ПРИМЕЧАНИЕ", None) or ok))): 
                if (t1.next0_ is not None and t1.next0_.is_char('.')): 
                    t1 = t1.next0_
                re = InstrToken1._new1532(t, t1, InstrToken1.Types.COMMENT)
                hiph = False
                t1 = t1.next0_
                first_pass3757 = True
                while True:
                    if first_pass3757: first_pass3757 = False
                    else: t1 = t1.next0_
                    if (not (t1 is not None)): break
                    re.end_token = t1
                    if (not t1.is_newline_after): 
                        continue
                    if (t1.next0_ is None): 
                        break
                    if (t1.next0_.is_value("СМ", None) or t1.next0_.is_value("ПУНКТ", None)): 
                        continue
                    if (not t1.next0_.is_hiphen): 
                        hiph = False
                    elif (t1.next0_.is_hiphen): 
                        if (t1.is_char(':')): 
                            hiph = True
                        if (hiph): 
                            continue
                    break
                return re
        check_comment = 0
        ttt = t
        first_pass3758 = True
        while True:
            if first_pass3758: first_pass3758 = False
            else: ttt = ttt.next0_
            if (not (ttt is not None)): break
            if (((ttt.is_newline_before or ttt.is_table_control_char)) and ttt != t): 
                break
            if (ttt.morph.class0_.is_preposition): 
                continue
            npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0, None)
            if (npt is None): 
                break
            if (npt.noun.is_value("ПРИМЕНЕНИЕ", "ЗАСТОСУВАННЯ") or npt.noun.is_value("ВОПРОС", "ПИТАННЯ")): 
                check_comment += 1
                ttt = npt.end_token
            else: 
                break
        if (check_comment > 0 or t.is_value("О", "ПРО")): 
            t1 = None
            ok = False
            dref = None
            ttt = t.next0_
            while ttt is not None: 
                t1 = ttt
                if (t1.is_value("СМ", None) and t1.next0_ is not None and t1.next0_.is_char('.')): 
                    if (check_comment > 0): 
                        ok = True
                    if ((isinstance(t1.next0_.next0_, ReferentToken)) and (((isinstance(t1.next0_.next0_.get_referent(), DecreeReferent)) or (isinstance(t1.next0_.next0_.get_referent(), DecreePartReferent))))): 
                        ok = True
                        dref = (Utils.asObjectOrNull(t1.next0_.next0_.get_referent(), DecreeReferent))
                if (ttt.is_newline_after): 
                    break
                ttt = ttt.next0_
            if (ok): 
                cmt = InstrToken1._new1532(t, t1, InstrToken1.Types.COMMENT)
                if (dref is not None and t1.next0_ is not None and t1.next0_.get_referent() == dref): 
                    if (t1.next0_.next0_ is not None and t1.next0_.next0_.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
                        ttt = t1.next0_.next0_
                        while ttt is not None: 
                            if (ttt.is_newline_before): 
                                break
                            cmt.end_token = ttt
                            ttt = ttt.next0_
                return cmt
        tt = InstrToken._check_approved(t)
        if (tt is not None): 
            res.end_token = tt
            if (tt.next0_ is not None and (isinstance(tt.next0_.get_referent(), DecreeReferent))): 
                res.typ = InstrToken1.Types.APPROVED
                res.end_token = tt.next0_
                return res
            tt1 = tt
            if (tt1.is_char(':') and tt1.next0_ is not None): 
                tt1 = tt1.next0_
            if ((isinstance(tt1.get_referent(), PersonReferent)) or (isinstance(tt1.get_referent(), InstrumentParticipantReferent))): 
                res.typ = InstrToken1.Types.APPROVED
                res.end_token = tt1
                return res
            dt1 = DecreeToken.try_attach(tt.next0_, None, False)
            if (dt1 is not None and dt1.typ == DecreeToken.ItemType.TYP): 
                res.typ = InstrToken1.Types.APPROVED
                err = 0
                ttt = dt1.end_token.next0_
                first_pass3759 = True
                while True:
                    if first_pass3759: first_pass3759 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (DecreeToken.is_keyword(ttt, False) is not None): 
                        break
                    dt1 = DecreeToken.try_attach(ttt, None, False)
                    if (dt1 is not None): 
                        if (dt1.typ == DecreeToken.ItemType.TYP or dt1.typ == DecreeToken.ItemType.NAME): 
                            break
                        ttt = dt1.end_token
                        res.end_token = ttt
                        continue
                    if (ttt.morph.class0_.is_preposition or ttt.morph.class0_.is_conjunction): 
                        continue
                    if (ttt.whitespaces_before_count > 15): 
                        break
                    err += 1
                    if (err > 10): 
                        break
                return res
        val = None
        wrapval1543 = RefOutArgWrapper(None)
        tt2 = InstrToken1._check_directive(t, wrapval1543)
        val = wrapval1543.value
        if (tt2 is not None): 
            if (tt2.is_newline_after or ((tt2.next0_ is not None and ((tt2.next0_.is_char_of(":") or ((tt2.next0_.is_char('.') and tt2 != t)))) and ((tt2.next0_.is_newline_after or t.chars.is_all_upper))))): 
                return InstrToken1._new1538(t, (tt2 if tt2.is_newline_after else tt2.next0_), InstrToken1.Types.DIRECTIVE, val)
        if ((lev < 3) and t is not None): 
            if ((t.is_value("СОДЕРЖИМОЕ", "ВМІСТ") or t.is_value("СОДЕРЖАНИЕ", "ЗМІСТ") or t.is_value("ОГЛАВЛЕНИЕ", "ЗМІСТ")) or ((t.is_value("СПИСОК", None) and t.next0_ is not None and t.next0_.is_value("РАЗДЕЛ", None)))): 
                t11 = t.next0_
                if (t.is_value("СПИСОК", None)): 
                    t11 = t11.next0_
                if (t11 is not None and not t11.is_newline_after): 
                    npt = NounPhraseHelper.try_parse(t11, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.morph.case_.is_genitive): 
                        t11 = npt.end_token.next0_
                if (t11 is not None and t11.is_char_of(":.;")): 
                    t11 = t11.next0_
                if (t11 is not None and t11.is_newline_before): 
                    first = InstrToken1.parse(t11, ignore_directives, None, lev + 1, None, False, 0, False, True)
                    if (first is not None and (first.length_char < 4)): 
                        first = InstrToken1.parse(first.end_token.next0_, ignore_directives, None, lev + 1, None, False, 0, False, False)
                    fstr = MiscHelper.get_text_value_of_meta_token(first, GetTextAttr.NO)
                    if (first is not None): 
                        cou = 0
                        itprev = None
                        has_app = False
                        tt = first.end_token.next0_
                        while tt is not None: 
                            if (tt.is_value("ПРИЛОЖЕНИЕ", None)): 
                                pass
                            if (tt.is_newline_before): 
                                cou += 1
                                if (cou > 400): 
                                    break
                            it = InstrToken1.parse(tt, ignore_directives, None, lev + 1, None, False, 0, False, True)
                            if (it is None): 
                                break
                            ok = False
                            if (len(first.numbers) == 1 and len(it.numbers) == 1): 
                                if (it.typ == InstrToken1.Types.APPENDIX and first.typ != InstrToken1.Types.APPENDIX): 
                                    pass
                                elif (first.numbers[0] == it.numbers[0]): 
                                    ok = True
                            elif (first.value is not None and it.value is not None and first.value.startswith(it.value)): 
                                ok = True
                            else: 
                                str0_ = MiscHelper.get_text_value_of_meta_token(it, GetTextAttr.NO)
                                if (str0_ == fstr): 
                                    ok = True
                            if ((ok and first.typ != InstrToken1.Types.APPENDIX and itprev is not None) and itprev.typ == InstrToken1.Types.APPENDIX): 
                                it2 = InstrToken1.parse(it.end_token.next0_, ignore_directives, None, lev + 1, None, False, 0, False, True)
                                if (it2 is not None and it2.typ == InstrToken1.Types.APPENDIX): 
                                    ok = False
                            if (not ok and cou > 4 and len(first.numbers) > 0): 
                                if (len(it.numbers) == 1 and it.numbers[0] == "1"): 
                                    if (it.title_typ == InstrToken1.StdTitleType.OTHERS): 
                                        ok = True
                            if (ok): 
                                if (t.previous is None): 
                                    return None
                                res.end_token = tt.previous
                                res.typ = InstrToken1.Types.INDEX
                                return res
                            if (it.typ == InstrToken1.Types.APPENDIX): 
                                has_app = True
                            tt = it.end_token
                            itprev = it
                            tt = tt.next0_
                        cou = 0
                        tt = first.begin_token
                        while tt is not None and tt.end_char <= first.end_char: 
                            if (tt.is_table_control_char): 
                                cou += 1
                            tt = tt.next0_
                        if (cou > 5): 
                            res.end_token = first.end_token
                            res.typ = InstrToken1.Types.INDEX
                            return res
        pts = (None if t is None else PartToken.try_attach_list((t.next0_ if t.is_value("ПОЛОЖЕНИЕ", "ПОЛОЖЕННЯ") else t), False, 40))
        if ((pts is not None and len(pts) > 0 and pts[0].typ != PartToken.ItemType.PREFIX) and len(pts[0].values) > 0 and not pts[0].is_newline_after): 
            ok = False
            tt = pts[len(pts) - 1].end_token.next0_
            if (tt is not None and tt.is_char_of(".)]")): 
                pass
            else: 
                while tt is not None: 
                    if (tt.is_value("ПРИМЕНЯТЬСЯ", "ЗАСТОСОВУВАТИСЯ")): 
                        ok = True
                    if ((tt.is_value("ВСТУПАТЬ", "ВСТУПАТИ") and tt.next0_ is not None and tt.next0_.next0_ is not None) and tt.next0_.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
                        ok = True
                    if (tt.is_newline_after): 
                        if (ok): 
                            return InstrToken1._new1532(t, tt, InstrToken1.Types.COMMENT)
                        break
                    tt = tt.next0_
        if (t is not None and (((t.is_newline_before or is_in_index or is_citat) or ((t.previous is not None and t.previous.is_table_control_char)))) and not t.is_table_control_char): 
            ok = True
            if (t.next0_ is not None and t.chars.is_all_lower): 
                if (not t.morph.case_.is_nominative): 
                    ok = False
                elif (t.next0_ is not None and t.next0_.is_char_of(",:;.")): 
                    ok = False
                else: 
                    npt = NounPhraseHelper.try_parse(t.previous, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.end_token == t): 
                        ok = False
            if (ok and (isinstance(t, TextToken))): 
                ok = False
                s = t.term
                if (s == "ГЛАВА" or s == "ГОЛОВА"): 
                    res.typ = InstrToken1.Types.CHAPTER
                    t = t.next0_
                    ok = True
                elif (s == "СТАТЬЯ" or s == "СТАТТЯ"): 
                    res.typ = InstrToken1.Types.CLAUSE
                    t = t.next0_
                    ok = True
                elif (s == "РАЗДЕЛ" or s == "РОЗДІЛ"): 
                    res.typ = InstrToken1.Types.SECTION
                    t = t.next0_
                    ok = True
                elif (s == "ЧАСТЬ" or s == "ЧАСТИНА"): 
                    res.typ = InstrToken1.Types.DOCPART
                    t = t.next0_
                    ok = True
                elif (s == "ПОДРАЗДЕЛ" or s == "ПІДРОЗДІЛ"): 
                    res.typ = InstrToken1.Types.SUBSECTION
                    t = t.next0_
                    ok = True
                elif ((s == "ПРИМЕЧАНИЕ" or s == "ПРИМІТКА" or s == "ПРИМЕЧАНИЯ") or s == "ПРИМІТКИ"): 
                    res.typ = InstrToken1.Types.NOTICE
                    t = t.next0_
                    if (t is not None and t.is_char_of(".:")): 
                        t = t.next0_
                    ok = True
                elif (s == "§" or s == "ПАРАГРАФ"): 
                    res.typ = InstrToken1.Types.PARAGRAPH
                    t = t.next0_
                    ok = True
                if (ok): 
                    ttt = t
                    if (ttt is not None and (isinstance(ttt, NumberToken))): 
                        ttt = ttt.next0_
                    if (ttt is not None and not ttt.is_newline_before): 
                        if (PartToken.try_attach(ttt, None, False, False) is not None): 
                            res.typ = InstrToken1.Types.LINE
                        elif (InstrToken._check_entered(ttt) is not None): 
                            res.typ = InstrToken1.Types.EDITIONS
                            t00 = res.begin_token
                        elif (res.begin_token.chars.is_all_lower): 
                            if (res.begin_token.newlines_before_count > 3): 
                                pass
                            else: 
                                res.typ = InstrToken1.Types.LINE
        num = res.typ != InstrToken1.Types.EDITIONS
        has_letters = False
        is_app = cur is not None and ((cur.kind == InstrumentKind.APPENDIX or cur.kind == InstrumentKind.INTERNALDOCUMENT))
        first_pass3760 = True
        while True:
            if first_pass3760: first_pass3760 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_char > 0 and t.begin_char > max_char): 
                break
            if (t.is_newline_before and t != res.begin_token): 
                if (len(res.numbers) == 2): 
                    if (res.numbers[0] == "3" and res.numbers[1] == "4"): 
                        pass
                is_new_line = True
                if (t.newlines_before_count == 1 and t.previous is not None and t.previous.chars.is_letter): 
                    npt = NounPhraseHelper.try_parse(t.previous, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.end_char > t.begin_char): 
                        is_new_line = False
                    elif (t.previous.get_morph_class_in_dictionary().is_adjective): 
                        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                        if (npt is not None and npt.morph.check_accord(t.previous.morph, False, False)): 
                            is_new_line = False
                    if (not is_new_line): 
                        tes = InstrToken1.parse(t, True, None, 0, None, False, 0, False, False)
                        if (tes is not None and len(tes.numbers) > 0): 
                            break
                    elif (len(res.numbers) > 0): 
                        tes = InstrToken1.parse(t, True, None, 0, None, False, 0, False, False)
                        if (tes is not None and len(tes.numbers) > 0): 
                            break
                if (is_new_line and t.chars.is_letter): 
                    if (not MiscHelper.can_be_start_of_sentence(t)): 
                        if (t.previous is not None and t.previous.is_char_of(":;.")): 
                            pass
                        elif (t.is_value("НЕТ", None) or t.is_value("НЕ", None) or t.is_value("ОТСУТСТВОВАТЬ", None)): 
                            pass
                        elif ((len(res.numbers) > 0 and t.previous is not None and t.previous.chars.is_all_upper) and not t.chars.is_all_upper): 
                            pass
                        elif (t.previous is not None and ((t.previous.is_value("ИЛИ", None) or t.previous.is_comma_and)) and len(res.numbers) > 0): 
                            vvv = InstrToken1.parse(t, True, None, 0, None, False, 0, False, False)
                            if (vvv is not None and len(vvv.numbers) > 0): 
                                is_new_line = True
                        else: 
                            is_new_line = False
                if (is_new_line): 
                    break
                else: 
                    pass
            if (t.is_table_control_char and t != res.begin_token): 
                if (can_be_table_cell or t.is_char(chr(0x1E)) or t.is_char(chr(0x1F))): 
                    break
                if (num and len(res.numbers) > 0): 
                    num = False
                elif (t.previous == res.num_end_token): 
                    pass
                elif (not t.is_newline_after): 
                    continue
                else: 
                    break
            if (is_in_index and not t.is_newline_before and not t.chars.is_all_lower): 
                typ_ = PartToken.try_attach(t, None, False, False)
                if (typ_ is not None): 
                    if (((typ_.typ == PartToken.ItemType.CHAPTER or typ_.typ == PartToken.ItemType.CLAUSE or typ_.typ == PartToken.ItemType.SECTION) or typ_.typ == PartToken.ItemType.SUBSECTION or typ_.typ == PartToken.ItemType.PARAGRAPH) or typ_.typ == PartToken.ItemType.APPENDIX): 
                        if (len(typ_.values) == 1): 
                            break
                dp = Utils.asObjectOrNull(t.get_referent(), DecreePartReferent)
                if (dp is not None): 
                    if (((dp.get_slot_value(DecreePartReferent.ATTR_CHAPTER) is not None or dp.get_slot_value(DecreePartReferent.ATTR_CLAUSE) is not None or dp.get_slot_value(DecreePartReferent.ATTR_SECTION) is not None) or dp.get_slot_value(DecreePartReferent.ATTR_SUBSECTION) is not None or dp.get_slot_value(DecreePartReferent.ATTR_PARAGRAPH) is not None) or dp.get_slot_value(DecreePartReferent.ATTR_APPENDIX) is not None): 
                        t = t.kit.debed_token(t)
                        break
            if ((t.is_char('[') and t == t0 and (isinstance(t.next0_, NumberToken))) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(']')): 
                num = False
                res.numbers.append(str(t.next0_.value))
                res.num_typ = NumberTypes.DIGIT
                res.num_suffix = "]"
                res.num_begin_token = t
                res.num_end_token = t.next0_.next0_
                t = res.num_end_token
                continue
            if (t.is_char('(')): 
                num = False
                if (FragToken._create_editions(t) is not None): 
                    break
                if (InstrToken1._create_edition(t) is not None): 
                    break
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    if (t == res.begin_token): 
                        lat = NumberHelper.try_parse_roman(t.next0_)
                        if (lat is not None and lat.end_token.next0_ == br.end_token): 
                            res.numbers.append(str(lat.value))
                            res.num_suffix = ")"
                            res.num_begin_token = t
                            res.num_end_token = br.end_token
                            res.num_typ = (NumberTypes.ROMAN if lat.typ == NumberSpellingType.ROMAN else NumberTypes.DIGIT)
                        elif (((t == t0 and t.is_newline_before and br.length_char == 3) and br.end_token == t.next0_.next0_ and (isinstance(t.next0_, TextToken))) and t.next0_.chars.is_latin_letter): 
                            res.num_begin_token = t
                            res.num_typ = NumberTypes.LETTER
                            res.numbers.append(t.next0_.term)
                            res.num_end_token = t.next0_.next0_
                            res.end_token = res.num_end_token
                    res.end_token = br.end_token
                    t = res.end_token
                    continue
            if (num): 
                NumberingHelper.parse_number(t, res, prev)
                num = False
                if (len(res.numbers) > 0): 
                    pass
                if (res.num_end_token is not None and res.num_end_token.end_char >= t.end_char): 
                    t = res.num_end_token
                    continue
            if (len(res.numbers) == 0): 
                num = False
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                has_letters = True
                if (t00 is None): 
                    t00 = t
                num = False
                if (t.chars.is_capital_upper and res.length_char > 20): 
                    if (t.is_value("РУКОВОДСТВУЯСЬ", None)): 
                        if (MiscHelper.can_be_start_of_sentence(t) or t.previous.is_comma): 
                            break
                    elif (t.is_value("НА", None) and t.next0_ is not None and t.next0_.is_value("ОСНОВАНИЕ", None)): 
                        ttt = InstrToken1.parse(t, True, None, 0, None, False, 0, False, False)
                        if (ttt is not None and "РУКОВОДСТВУЯСЬ" in str(ttt).upper()): 
                            if (MiscHelper.can_be_start_of_sentence(t)): 
                                break
                if (not t.chars.is_all_upper): 
                    res.all_upper = False
                if (t.is_pure_verb): 
                    if (t.chars.is_cyrillic_letter): 
                        npt = NounPhraseHelper.try_parse((t.next0_ if t.morph.class0_.is_preposition else t), NounPhraseParseAttr.NO, 0, None)
                        if (npt is not None): 
                            pass
                        else: 
                            res.has_verb = True
            elif (isinstance(t, ReferentToken)): 
                has_letters = True
                if (t00 is None): 
                    t00 = t
                num = False
                if (isinstance(t.get_referent(), DecreeChangeReferent)): 
                    res.has_verb = True
                    res.all_upper = False
                if (isinstance(t.get_referent(), InstrumentParticipantReferent)): 
                    if (not t.chars.is_all_upper): 
                        res.all_upper = False
            if (t != res.begin_token and InstrToken1.__is_first_line(t)): 
                break
            wraptmp1540 = RefOutArgWrapper(None)
            tt2 = InstrToken1._check_directive(t, wraptmp1540)
            tmp = wraptmp1540.value
            if (tt2 is not None): 
                if (tt2.next0_ is not None and tt2.next0_.is_char_of(":.") and tt2.next0_.is_newline_after): 
                    if (ignore_directives and not t.is_newline_before): 
                        t = tt2
                    else: 
                        break
            res.end_token = t
        if (res.typ_container_rank > 0 and t00 is not None): 
            if (t00.chars.is_all_lower): 
                res.typ = InstrToken1.Types.LINE
                res.numbers.clear()
                res.num_typ = NumberTypes.UNDEFINED
        if (t00 is not None): 
            len0_ = res.end_char - t00.begin_char
            if (len0_ < 1000): 
                res.value = MiscHelper.get_text_value(t00, res.end_token, GetTextAttr.NO)
                if (LanguageHelper.ends_with(res.value, ".")): 
                    res.value = res.value[0:0+len(res.value) - 1]
        if (not has_letters): 
            res.all_upper = False
        if (res.num_typ != NumberTypes.UNDEFINED and res.begin_token == res.num_begin_token and res.end_token == res.num_end_token): 
            ok = False
            if (prev is not None): 
                if (NumberingHelper.calc_delta(prev, res, True) == 1): 
                    ok = True
            if (not ok): 
                res1 = InstrToken1.parse(res.end_token.next0_, True, None, 0, None, False, 0, False, False)
                if (res1 is not None): 
                    if (NumberingHelper.calc_delta(res, res1, True) == 1): 
                        ok = True
            if (not ok): 
                res.num_typ = NumberTypes.UNDEFINED
                res.numbers.clear()
        if (res.typ == InstrToken1.Types.APPENDIX or res.typ_container_rank > 0): 
            if (res.typ == InstrToken1.Types.CLAUSE and res.last_number == 17): 
                pass
            tt = (Utils.ifNotNull(res.num_end_token, res.begin_token)).next0_
            if (tt is not None): 
                ttt = InstrToken._check_entered(tt)
                if (ttt is not None): 
                    if (tt.is_value("УТРАТИТЬ", None) and tt.previous is not None and tt.previous.is_char('.')): 
                        res.value = (None)
                        res.end_token = tt.previous
                        res.is_expired = True
                    else: 
                        res.typ = InstrToken1.Types.EDITIONS
                        res.numbers.clear()
                        res.num_typ = NumberTypes.UNDEFINED
                        res.value = (None)
        if (res.typ == InstrToken1.Types.DOCPART): 
            pass
        bad_number = False
        if ((res.typ_container_rank > 0 and res.num_typ != NumberTypes.UNDEFINED and res.num_end_token is not None) and not res.num_end_token.is_newline_after and res.num_end_token.next0_ is not None): 
            t1 = res.num_end_token.next0_
            bad = False
            if (t1.chars.is_all_lower): 
                bad = True
            if (bad): 
                bad_number = True
        if (res.num_typ != NumberTypes.UNDEFINED and not is_citat): 
            if (res.is_newline_before or is_in_index): 
                pass
            elif (res.begin_token.previous is not None and res.begin_token.previous.is_table_control_char): 
                pass
            else: 
                bad_number = True
            if (res.num_suffix == "-"): 
                bad_number = True
        if (res.typ == InstrToken1.Types.LINE and len(res.numbers) > 0 and is_citat): 
            tt0 = res.begin_token.previous
            if (BracketHelper.can_be_start_of_sequence(tt0, True, True)): 
                tt0 = tt0.previous
            if (tt0 is not None): 
                tt0 = tt0.previous
            while tt0 is not None: 
                if (tt0.is_value("ГЛАВА", "ГОЛОВА")): 
                    res.typ = InstrToken1.Types.CHAPTER
                elif (tt0.is_value("СТАТЬЯ", "СТАТТЯ")): 
                    res.typ = InstrToken1.Types.CLAUSE
                elif (tt0.is_value("РАЗДЕЛ", "РОЗДІЛ")): 
                    res.typ = InstrToken1.Types.SECTION
                elif (tt0.is_value("ЧАСТЬ", "ЧАСТИНА")): 
                    res.typ = InstrToken1.Types.DOCPART
                elif (tt0.is_value("ПОДРАЗДЕЛ", "ПІДРОЗДІЛ")): 
                    res.typ = InstrToken1.Types.SUBSECTION
                elif (tt0.is_value("ПАРАГРАФ", None)): 
                    res.typ = InstrToken1.Types.PARAGRAPH
                elif (tt0.is_value("ПРИМЕЧАНИЕ", "ПРИМІТКА")): 
                    res.typ = InstrToken1.Types.NOTICE
                if (tt0.is_newline_before): 
                    break
                tt0 = tt0.previous
        if (bad_number): 
            res.typ = InstrToken1.Types.LINE
            res.num_typ = NumberTypes.UNDEFINED
            res.value = (None)
            res.numbers.clear()
            res.num_end_token = None
            res.num_begin_token = res.num_end_token
        if ((res.typ == InstrToken1.Types.SECTION or res.typ == InstrToken1.Types.PARAGRAPH or res.typ == InstrToken1.Types.CHAPTER) or res.typ == InstrToken1.Types.CLAUSE): 
            if (len(res.numbers) == 0): 
                res.typ = InstrToken1.Types.LINE
        if (res.end_token.is_char('>') and res.begin_token.is_value("ПУТЕВОДИТЕЛЬ", None)): 
            res.typ = InstrToken1.Types.COMMENT
            ttt = res.end_token.next0_
            first_pass3761 = True
            while True:
                if first_pass3761: first_pass3761 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                li2 = InstrToken1.parse(ttt, True, None, 0, None, False, 0, False, False)
                if (li2 is not None and li2.end_token.is_char('>')): 
                    ttt = li2.end_token
                    res.end_token = ttt
                    continue
                break
            return res
        if (res.typ == InstrToken1.Types.LINE): 
            if (res.num_typ != NumberTypes.UNDEFINED): 
                ttt = res.begin_token.previous
                if (isinstance(ttt, TextToken)): 
                    if (ttt.is_value("ПУНКТ", None)): 
                        res.num_typ = NumberTypes.UNDEFINED
                        res.value = (None)
                        res.numbers.clear()
                for nn in res.numbers: 
                    wrapvv1541 = RefOutArgWrapper(0)
                    inoutres1542 = Utils.tryParseInt(nn, wrapvv1541)
                    vv = wrapvv1541.value
                    if (inoutres1542): 
                        if (vv > 1000 and res.num_begin_token == res.begin_token): 
                            res.num_typ = NumberTypes.UNDEFINED
                            res.value = (None)
                            res.numbers.clear()
                            break
            if (InstrToken1.__is_first_line(res.begin_token)): 
                res.typ = InstrToken1.Types.FIRSTLINE
            if (res.num_typ == NumberTypes.DIGIT): 
                if (res.num_suffix is None): 
                    res.is_num_doubt = True
            if (len(res.numbers) == 0): 
                pt = PartToken.try_attach(res.begin_token, None, False, False)
                if (pt is not None and pt.typ != PartToken.ItemType.PREFIX): 
                    tt = pt.end_token.next0_
                    if (tt is not None and ((tt.is_char_of(".") or tt.is_hiphen))): 
                        tt = tt.next0_
                    tt = InstrToken._check_entered(tt)
                    if (tt is not None): 
                        res.typ = InstrToken1.Types.EDITIONS
                        res.is_expired = tt.is_value("УТРАТИТЬ", "ВТРАТИТИ")
                else: 
                    tt = InstrToken._check_entered(res.begin_token)
                    if (tt is not None and tt.next0_ is not None and (isinstance(tt.next0_.get_referent(), DecreeReferent))): 
                        res.typ = InstrToken1.Types.EDITIONS
                    elif (res.begin_token.is_value("АБЗАЦ", None) and res.begin_token.next0_ is not None and res.begin_token.next0_.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
                        res.is_expired = True
        if (res.typ == InstrToken1.Types.LINE and res.num_typ == NumberTypes.ROMAN): 
            res1 = InstrToken1.parse(res.end_token.next0_, True, cur, lev + 1, None, False, 0, False, False)
            if (res1 is not None and res1.typ == InstrToken1.Types.CLAUSE): 
                res.typ = InstrToken1.Types.CHAPTER
        specs = 0
        chars_ = 0
        if (len(res.numbers) == 2 and res.numbers[0] == "2" and res.numbers[1] == "3"): 
            pass
        tt = (res.begin_token if res.num_end_token is None else res.num_end_token.next0_)
        first_pass3762 = True
        while True:
            if first_pass3762: first_pass3762 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.end_char > res.end_token.end_char): 
                break
            tto = Utils.asObjectOrNull(tt, TextToken)
            if (tto is None): 
                continue
            if (not tto.chars.is_letter): 
                if (not tto.is_char_of(",;.():") and not BracketHelper.is_bracket(tto, False)): 
                    specs += tto.length_char
            else: 
                chars_ += tto.length_char
        if ((specs + chars_) > 0): 
            if (((math.floor((specs * 100) / ((specs + chars_))))) > 10): 
                res.has_many_spec_chars = True
        res.title_typ = InstrToken1.StdTitleType.UNDEFINED
        words = 0
        tt = (res.begin_token if res.num_begin_token is None else res.num_begin_token.next0_)
        first_pass3763 = True
        while True:
            if first_pass3763: first_pass3763 = False
            else: tt = tt.next0_
            if (not (tt is not None and tt.end_char <= res.end_char)): break
            if (not (isinstance(tt, TextToken)) or tt.is_char('_')): 
                res.title_typ = InstrToken1.StdTitleType.UNDEFINED
                break
            if (not tt.chars.is_letter or tt.morph.class0_.is_conjunction or tt.morph.class0_.is_preposition): 
                continue
            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                words += 1
                ii = 0
                while ii < len(InstrToken1.M_STD_REQ_WORDS): 
                    if (npt.noun.is_value(InstrToken1.M_STD_REQ_WORDS[ii], None)): 
                        break
                    ii += 1
                if (ii < len(InstrToken1.M_STD_REQ_WORDS)): 
                    tt = npt.end_token
                    res.title_typ = InstrToken1.StdTitleType.REQUISITES
                    continue
                if (npt.noun.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or npt.noun.is_value("ВСТУПЛЕНИЕ", "ВСТУП")): 
                    words += 1
                    tt = npt.end_token
                    res.title_typ = InstrToken1.StdTitleType.OTHERS
                    continue
                if (((npt.noun.is_value("ПОЛОЖЕНИЕ", "ПОЛОЖЕННЯ") or npt.noun.is_value("СОКРАЩЕНИЕ", "СКОРОЧЕННЯ") or npt.noun.is_value("ТЕРМИН", "ТЕРМІН")) or npt.noun.is_value("ОПРЕДЕЛЕНИЕ", "ВИЗНАЧЕННЯ") or npt.noun.is_value("АББРЕВИАТУРА", "АБРЕВІАТУРА")) or npt.noun.is_value("ЛИТЕРАТУРА", "ЛІТЕРАТУРА") or npt.noun.is_value("НАЗВАНИЕ", "НАЗВА")): 
                    tt = npt.end_token
                    res.title_typ = InstrToken1.StdTitleType.OTHERS
                    continue
                if (npt.noun.is_value("ПАСПОРТ", None)): 
                    tt = npt.end_token
                    res.title_typ = InstrToken1.StdTitleType.OTHERS
                    npt2 = NounPhraseHelper.try_parse(npt.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
                    if (npt2 is not None and npt2.morph.case_.is_genitive and (npt2.whitespaces_before_count < 3)): 
                        tt = npt2.end_token
                    continue
                if (npt.noun.is_value("ПРЕДМЕТ", None)): 
                    tt = npt.end_token
                    res.title_typ = InstrToken1.StdTitleType.SUBJECT
                    continue
                if (isinstance(npt.end_token, TextToken)): 
                    term = npt.end_token.term
                    if (term == "ПРИЛОЖЕНИЯ" or term == "ПРИЛОЖЕНИЙ"): 
                        tt = npt.end_token
                        res.title_typ = InstrToken1.StdTitleType.OTHERS
                        continue
                if (((npt.noun.is_value("МОМЕНТ", None) or npt.noun.is_value("ЗАКЛЮЧЕНИЕ", "ВИСНОВОК") or npt.noun.is_value("ДАННЫЕ", None)) or npt.is_value("ДОГОВОР", "ДОГОВІР") or npt.is_value("КОНТРАКТ", None)) or npt.is_value("СПИСОК", None) or npt.is_value("ПЕРЕЧЕНЬ", "ПЕРЕЛІК")): 
                    tt = npt.end_token
                    continue
            pp = ParticipantToken.try_attach(tt, None, None, False)
            if (pp is not None and pp.kind == ParticipantToken.Kinds.PURE): 
                tt = pp.end_token
                continue
            res.title_typ = InstrToken1.StdTitleType.UNDEFINED
            break
        if (res.title_typ != InstrToken1.StdTitleType.UNDEFINED and len(res.numbers) == 0): 
            t = res.begin_token
            if (not (isinstance(t, TextToken)) or not t.chars.is_letter or t.chars.is_all_lower): 
                res.title_typ = InstrToken1.StdTitleType.UNDEFINED
        if ((len(res.numbers) == 0 and not res.is_newline_before and res.begin_token.previous is not None) and res.begin_token.previous.is_table_control_char): 
            res.title_typ = InstrToken1.StdTitleType.UNDEFINED
        t = res.end_token.next0_
        while t is not None: 
            if (not t.is_table_control_char): 
                break
            elif (t.is_char(chr(0x1E))): 
                break
            else: 
                res.end_token = t
            t = t.next0_
        return res
    
    M_STD_REQ_WORDS = None
    
    @staticmethod
    def __is_first_line(t : 'Token') -> bool:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        v = tt.term
        if ((((v == "ИСХОДЯ" or v == "ВИХОДЯЧИ")) and t.next0_ is not None and t.next0_.is_value("ИЗ", "З")) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("ИЗЛОЖЕННОЕ", "ВИКЛАДЕНЕ")): 
            return True
        if ((((v == "НА" or v == "HA")) and t.next0_ is not None and t.next0_.is_value("ОСНОВАНИЕ", "ПІДСТАВА")) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("ИЗЛОЖЕННОЕ", "ВИКЛАДЕНЕ")): 
            return True
        if (((v == "УЧИТЫВАЯ" or v == "ВРАХОВУЮЧИ")) and t.next0_ is not None and t.next0_.is_value("ИЗЛОЖЕННОЕ", "ВИКЛАДЕНЕ")): 
            return True
        if ((v == "ЗАСЛУШАВ" or v == "РАССМОТРЕВ" or v == "ЗАСЛУХАВШИ") or v == "РОЗГЛЯНУВШИ"): 
            return True
        if (v == "РУКОВОДСТВУЯСЬ" or v == "КЕРУЮЧИСЬ"): 
            return tt.is_newline_before
        return False
    
    @staticmethod
    def _create_edition(t : 'Token') -> 'Token':
        if (t is None or t.next0_ is None): 
            return None
        ok = False
        t1 = t
        br = 0
        if (t.is_char('(') and t.is_newline_before): 
            ok = True
            br = 1
            t1 = t.next0_
        if (not ok or t1 is None): 
            return None
        ok = False
        dts = PartToken.try_attach_list(t1, True, 40)
        if (dts is not None and len(dts) > 0): 
            t1 = dts[len(dts) - 1].end_token.next0_
        t2 = InstrToken._check_entered(t1)
        if (t2 is None and t1 is not None): 
            t2 = InstrToken._check_entered(t1.next0_)
        if (t2 is not None): 
            ok = True
        if (not ok): 
            return None
        t1 = t2
        while t1 is not None: 
            if (t1.is_char(')')): 
                br -= 1
                if (br == 0): 
                    return t1
            elif (t1.is_char('(')): 
                br += 1
            elif (t1.is_newline_after): 
                break
            t1 = t1.next0_
        return None
    
    @staticmethod
    def _check_directive(t : 'Token', val : str) -> 'Token':
        val.value = (None)
        if (t is None or t.morph.class0_.is_adjective): 
            return None
        ii = 0
        while ii < len(InstrToken._m_directives): 
            if (t.is_value(InstrToken._m_directives[ii], None)): 
                val.value = InstrToken._m_directives_norm[ii]
                if (t.whitespaces_before_count < 7): 
                    if (((((val.value != "ПРИКАЗ" and val.value != "ПОСТАНОВЛЕНИЕ" and val.value != "УСТАНОВЛЕНИЕ") and val.value != "РЕШЕНИЕ" and val.value != "ЗАЯВЛЕНИЕ") and val.value != "НАКАЗ" and val.value != "ПОСТАНОВА") and val.value != "ВСТАНОВЛЕННЯ" and val.value != "РІШЕННЯ") and val.value != "ЗАЯВУ"): 
                        if ((t.next0_ is not None and t.next0_.is_char(':') and t.next0_.is_newline_after) and t.chars.is_all_upper): 
                            pass
                        else: 
                            break
                if (t.next0_ is not None and t.next0_.is_value("СЛЕДУЮЩЕЕ", "НАСТУПНЕ")): 
                    return t.next0_
                if (((val.value == "ЗАЯВЛЕНИЕ" or val.value == "ЗАЯВА")) and t.next0_ is not None and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                    t = t.next0_
                return t
            ii += 1
        if (t.chars.is_letter and t.length_char == 1): 
            if (t.is_newline_before or ((t.next0_ is not None and t.next0_.chars.is_letter and t.next0_.length_char == 1))): 
                ii = 0
                while ii < len(InstrToken._m_directives): 
                    res = MiscHelper.try_attach_word_by_letters(InstrToken._m_directives[ii], t, True)
                    if (res is not None): 
                        val.value = InstrToken._m_directives_norm[ii]
                        return res
                    ii += 1
        return None
    
    @property
    def typ_container_rank(self) -> int:
        res = InstrToken1._calc_rank(self.typ)
        return res
    
    @staticmethod
    def _calc_rank(ty : 'Types') -> int:
        if (ty == InstrToken1.Types.DOCPART): 
            return 1
        if (ty == InstrToken1.Types.SECTION): 
            return 2
        if (ty == InstrToken1.Types.SUBSECTION): 
            return 3
        if (ty == InstrToken1.Types.CHAPTER): 
            return 4
        if (ty == InstrToken1.Types.PARAGRAPH): 
            return 5
        if (ty == InstrToken1.Types.SUBPARAGRAPH): 
            return 6
        if (ty == InstrToken1.Types.CLAUSE): 
            return 7
        return 0
    
    def can_be_container_for(self, lt : 'InstrToken1') -> bool:
        r = InstrToken1._calc_rank(self.typ)
        r1 = InstrToken1._calc_rank(lt.typ)
        if (r > 0 and r1 > 0): 
            return r < r1
        return False
    
    @staticmethod
    def _new1532(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Types') -> 'InstrToken1':
        res = InstrToken1(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1534(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'InstrToken1':
        res = InstrToken1(_arg1, _arg2)
        res.all_upper = _arg3
        return res
    
    @staticmethod
    def _new1538(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Types', _arg4 : str) -> 'InstrToken1':
        res = InstrToken1(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1551(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : 'Types') -> 'InstrToken1':
        res = InstrToken1(_arg1, _arg2)
        res.index_no_keyword = _arg3
        res.typ = _arg4
        return res
    
    # static constructor for class InstrToken1
    @staticmethod
    def _static_ctor():
        InstrToken1.M_STD_REQ_WORDS = list(["РЕКВИЗИТ", "ПОДПИСЬ", "СТОРОНА", "АДРЕС", "ТЕЛЕФОН", "МЕСТО", "НАХОЖДЕНИЕ", "МЕСТОНАХОЖДЕНИЕ", "ТЕРМИН", "ОПРЕДЕЛЕНИЕ", "СЧЕТ", "РЕКВІЗИТ", "ПІДПИС", "СТОРОНА", "АДРЕСА", "МІСЦЕ", "ЗНАХОДЖЕННЯ", "МІСЦЕЗНАХОДЖЕННЯ", "ТЕРМІН", "ВИЗНАЧЕННЯ", "РАХУНОК"])

InstrToken1._static_ctor()