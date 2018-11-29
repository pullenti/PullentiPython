# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.instrument.internal.ILTypes import ILTypes
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.morph.MorphGender import MorphGender


class InstrToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = ILTypes.UNDEFINED
        self.value = None;
        self.ref = None;
        self.has_verb = False
        self.no_words = False
    
    __m_ontology = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (InstrToken.__m_ontology is not None): 
            return
        InstrToken.__m_ontology = TerminCollection()
        t = Termin("МЕСТО ПЕЧАТИ")
        t.addAbridge("М.П.")
        t.addAbridge("M.П.")
        InstrToken.__m_ontology.add(t)
        t = Termin("МІСЦЕ ПЕЧАТКИ", MorphLang.UA)
        t.addAbridge("М.П.")
        t.addAbridge("M.П.")
        InstrToken.__m_ontology.add(t)
        t = Termin("ПОДПИСЬ")
        InstrToken.__m_ontology.add(t)
        t = Termin("ПІДПИС", MorphLang.UA)
        InstrToken.__m_ontology.add(t)
        t = Termin._new113("ФАМИЛИЯ ИМЯ ОТЧЕСТВО", "ФИО")
        t.addAbridge("Ф.И.О.")
        InstrToken.__m_ontology.add(t)
        t = Termin._new1419("ПРІЗВИЩЕ ІМЯ ПО БАТЬКОВІ", MorphLang.UA, "ФИО")
        InstrToken.__m_ontology.add(t)
        t = Termin("ФАМИЛИЯ")
        t.addAbridge("ФАМ.")
        InstrToken.__m_ontology.add(t)
        t = Termin("ПРІЗВИЩЕ", MorphLang.UA)
        t.addAbridge("ФАМ.")
        InstrToken.__m_ontology.add(t)
        InstrToken.__m_ontology.add(Termin("ИМЯ"))
        InstrToken.__m_ontology.add(Termin("ІМЯ", MorphLang.UA))
    
    @property
    def is_pure_person(self) -> bool:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.TextToken import TextToken
        if (isinstance(self.ref, ReferentToken)): 
            rt = Utils.asObjectOrNull(self.ref, ReferentToken)
            if ((isinstance(rt.referent, PersonReferent)) or (isinstance(rt.referent, PersonPropertyReferent))): 
                return True
            if (isinstance(rt.referent, InstrumentParticipant)): 
                t = rt.begin_token
                while t is not None and t.end_char <= rt.end_char: 
                    if ((isinstance(t.getReferent(), PersonReferent)) or (isinstance(t.getReferent(), PersonPropertyReferent))): 
                        return True
                    elif ((isinstance(t, TextToken)) and t.chars.is_letter): 
                        break
                    t = t.next0_
                return False
        return isinstance(self.ref, PersonReferent)
    
    @property
    def is_podpis_storon(self) -> bool:
        if (not self.is_newline_before or not self.is_newline_after): 
            return False
        if (not self.begin_token.isValue("ПОДПИСЬ", "ПІДПИС")): 
            return False
        t = self.begin_token.next0_
        if (t is not None and t.isValue("СТОРОНА", None)): 
            t = t.next0_
        if (t is not None and t.isCharOf(":.")): 
            t = t.next0_
        if (self.end_token.next0_ == t): 
            return True
        return False
    
    @property
    def has_table_chars(self) -> bool:
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if (t.is_table_control_char): 
                return True
            t = t.next0_
        if (self.end_token.next0_ is not None and self.end_token.next0_.is_table_control_char and not self.end_token.next0_.isChar(chr(0x1E))): 
            return True
        if (self.begin_token.previous is not None and self.begin_token.previous.is_table_control_char and not self.begin_token.previous.isChar(chr(0x1F))): 
            return True
        return False
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.is_newline_before): 
            print("<<", end="", file=tmp)
        print(Utils.enumToString(self.typ).format(), end="", file=tmp, flush=True)
        if (self.value is not None): 
            print(" '{0}'".format(self.value), end="", file=tmp, flush=True)
        if (self.ref is not None): 
            print(" -> {0}".format(str(self.ref)), end="", file=tmp, flush=True)
        if (self.has_verb): 
            print(" HasVerb".format(), end="", file=tmp, flush=True)
        if (self.no_words): 
            print(" NoWords", end="", file=tmp)
        if (self.has_table_chars): 
            print(" HasTableChars", end="", file=tmp)
        if (self.is_newline_after): 
            print(">>", end="", file=tmp)
        print(": {0}".format(self.getSourceText()), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def parseList(t0 : 'Token', max_char : int=0) -> typing.List['InstrToken']:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        res = list()
        t = t0
        while t is not None: 
            if (max_char > 0): 
                if (t.begin_char > max_char): 
                    break
            if (len(res) == 63): 
                pass
            it = InstrToken.parse(t, max_char, (res[len(res) - 1] if len(res) > 0 else None))
            if (it is None): 
                break
            if (len(res) == 286): 
                pass
            if (it.typ == ILTypes.APPENDIX): 
                pass
            if (it.typ == ILTypes.TYP): 
                pass
            if (len(res) > 0): 
                if (res[len(res) - 1].end_char > it.begin_char): 
                    break
            if ((isinstance(it.end_token.next0_, TextToken)) and it.end_token.next0_.isChar('.')): 
                it.end_token = it.end_token.next0_
            if (it.typ == ILTypes.UNDEFINED and t.is_newline_before): 
                it1 = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
                if (it1 is not None and it1.has_changes and it1.end_char > it.end_char): 
                    it.end_token = it1.end_token
            res.append(it)
            if (it.end_char > t.begin_char): 
                t = it.end_token
            t = t.next0_
        return res
    
    @staticmethod
    def __correctPerson(res : 'InstrToken') -> 'InstrToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        spec_chars = 0
        if (not res.is_pure_person): 
            res.typ = ILTypes.UNDEFINED
            return res
        t = res.end_token.next0_
        first_pass3000 = True
        while True:
            if first_pass3000: first_pass3000 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if ((isinstance(t, ReferentToken)) and (isinstance(res.ref, ReferentToken))): 
                ok = False
                if (t.getReferent() == (Utils.asObjectOrNull(res.ref, ReferentToken)).referent): 
                    ok = True
                ip = Utils.asObjectOrNull((Utils.asObjectOrNull(res.ref, ReferentToken)).referent, InstrumentParticipant)
                if (ip is not None and ip._containsRef(t.getReferent())): 
                    ok = True
                if (not ok and t.previous is not None and t.previous.is_table_control_char): 
                    if ((isinstance((Utils.asObjectOrNull(res.ref, ReferentToken)).referent, PersonPropertyReferent)) and (isinstance(t.getReferent(), PersonReferent))): 
                        ok = True
                        res.ref = (t)
                if (ok): 
                    res.end_token = t
                    continue
            tok = InstrToken.__m_ontology.tryParse(t, TerminParseAttr.NO)
            if (tok is not None): 
                if ((((tok.termin.canonic_text == "ПОДПИСЬ" or tok.termin.canonic_text == "ПІДПИС")) and t.is_newline_before and t.next0_ is not None) and t.next0_.isValue("СТОРОНА", None)): 
                    break
                t = tok.end_token
                res.end_token = t
                continue
            if (t.isChar(',')): 
                continue
            if (t.is_table_control_char and not t.is_newline_before): 
                continue
            if (t.isCharOf("_/\\")): 
                res.end_token = t
                spec_chars += 1
                continue
            if (t.isChar('(') and t.next0_ is not None): 
                tok = InstrToken.__m_ontology.tryParse(t.next0_, TerminParseAttr.NO)
                if ((tok) is not None): 
                    br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        res.end_token = t
                        continue
            break
        rt0 = Utils.asObjectOrNull(res.ref, ReferentToken)
        if (rt0 is not None and (isinstance(rt0.referent, InstrumentParticipant))): 
            tt = res.begin_token
            while tt is not None and tt.end_char <= res.end_char: 
                if ((isinstance(tt.getReferent(), PersonReferent)) or (isinstance(tt.getReferent(), PersonPropertyReferent))): 
                    res.ref = (tt)
                    return res
                elif ((isinstance(tt, TextToken)) and tt.isCharOf("_/\\")): 
                    spec_chars += 1
                elif (isinstance(tt, MetaToken)): 
                    ttt = (Utils.asObjectOrNull(tt, MetaToken)).begin_token
                    while ttt is not None and ttt.end_char <= tt.end_char: 
                        if ((isinstance(ttt.getReferent(), PersonReferent)) or (isinstance(ttt.getReferent(), PersonPropertyReferent))): 
                            res.ref = (ttt)
                            return res
                        elif ((isinstance(ttt, TextToken)) and ttt.isCharOf("_/\\")): 
                            spec_chars += 1
                        ttt = ttt.next0_
                tt = tt.next0_
            if (spec_chars < 10): 
                res.typ = ILTypes.UNDEFINED
        return res
    
    @staticmethod
    def parse(t : 'Token', max_char : int=0, prev : 'InstrToken'=None) -> 'InstrToken':
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.morph.MorphClass import MorphClass
        is_start_of_line = False
        t00 = t
        if (t is not None): 
            is_start_of_line = t00.is_newline_before
            while t is not None:
                if (t.is_table_control_char and not t.isChar(chr(0x1F))): 
                    if (t.is_newline_after and not is_start_of_line): 
                        is_start_of_line = True
                    t = t.next0_
                else: 
                    break
        if (t is None): 
            return None
        if (t.is_newline_before): 
            is_start_of_line = True
        t0 = t
        t1 = None
        has_word = False
        first_pass3001 = True
        while True:
            if first_pass3001: first_pass3001 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before and t != t0): 
                break
            if (max_char > 0 and t.begin_char > max_char): 
                break
            if (is_start_of_line and t == t0): 
                tt = None
                if ((isinstance(t.getReferent(), PersonReferent)) or (isinstance(t.getReferent(), PersonPropertyReferent)) or (isinstance(t.getReferent(), InstrumentParticipant))): 
                    return InstrToken.__correctPerson(InstrToken._new1420(t00, t, ILTypes.PERSON, t))
                is_ref = False
                if (isinstance(t.getReferent(), PersonPropertyReferent)): 
                    tt = t.next0_
                    is_ref = True
                elif (prev is not None and prev.typ == ILTypes.PERSON): 
                    rt = t.kit.processReferent(PersonAnalyzer.ANALYZER_NAME, t)
                    if (rt is not None): 
                        if (isinstance(rt.referent, PersonReferent)): 
                            return InstrToken._new1421(t00, rt.end_token, ILTypes.PERSON)
                        tt = rt.end_token.next0_
                cou = 0
                t11 = (None if tt is None else tt.previous)
                first_pass3002 = True
                while True:
                    if first_pass3002: first_pass3002 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_table_control_char): 
                        continue
                    re = tt.getReferent()
                    if (isinstance(re, PersonReferent)): 
                        return InstrToken._new1420(t00, tt, ILTypes.PERSON, tt)
                    if (isinstance(re, GeoReferent)): 
                        t11 = tt
                        continue
                    if (re is not None): 
                        break
                    if (DecreeToken.isKeyword(tt, False) is not None): 
                        break
                    if (tt.is_newline_before): 
                        cou += 1
                        if ((cou) > 4): 
                            break
                if (tt is None and is_ref): 
                    return InstrToken._new1420(t00, Utils.ifNotNull(t11, t), ILTypes.PERSON, t)
            dt = DecreeToken.tryAttach(t, None, False)
            if (dt is not None): 
                if (dt.typ == DecreeToken.ItemType.TYP and not t.chars.is_all_lower): 
                    if (t != t0): 
                        break
                    has_verb_ = False
                    tt = dt.end_token
                    while tt is not None: 
                        if (tt.is_newline_before): 
                            break
                        elif ((isinstance(tt, TextToken)) and (Utils.asObjectOrNull(tt, TextToken)).is_pure_verb): 
                            has_verb_ = True
                            break
                        tt = tt.next0_
                    if (not has_verb_): 
                        res2 = InstrToken._new1424(t0, dt.end_token, ILTypes.TYP, Utils.ifNotNull(dt.full_value, dt.value))
                        if (res2.value == "ДОПОЛНИТЕЛЬНОЕ СОГЛАШЕНИЕ" or res2.value == "ДОДАТКОВА УГОДА"): 
                            if (res2.begin_char > 500 and res2.newlines_before_count > 1): 
                                res2.typ = ILTypes.APPENDIX
                        return res2
                if (dt.typ == DecreeToken.ItemType.NUMBER): 
                    if (t != t0): 
                        break
                    return InstrToken._new1424(t0, dt.end_token, ILTypes.REGNUMBER, dt.value)
                if (dt.typ == DecreeToken.ItemType.ORG): 
                    if (t != t0): 
                        break
                    return InstrToken._new1426(t0, dt.end_token, ILTypes.ORGANIZATION, dt.ref, dt.value)
                if (dt.typ == DecreeToken.ItemType.TERR): 
                    if (t != t0): 
                        break
                    re = InstrToken._new1426(t0, dt.end_token, ILTypes.GEO, dt.ref, dt.value)
                    t1 = re.end_token.next0_
                    if (t1 is not None and t1.isChar(',')): 
                        t1 = t1.next0_
                    if (t1 is not None and t1.isValue("КРЕМЛЬ", None)): 
                        re.end_token = t1
                    elif ((t1 is not None and t1.isValue("ДОМ", "БУДИНОК") and t1.next0_ is not None) and t1.next0_.isValue("СОВЕТ", "РАД")): 
                        re.end_token = t1.next0_
                        if (t1.next0_.next0_ is not None and (isinstance(t1.next0_.next0_.getReferent(), GeoReferent))): 
                            re.end_token = t1.next0_.next0_
                    return re
                if (dt.typ == DecreeToken.ItemType.OWNER): 
                    if (t != t0): 
                        break
                    if (dt.ref is not None and str(dt.ref.referent).startswith("агент")): 
                        dt = (None)
                    if (dt is not None): 
                        res1 = InstrToken._new1426(t0, dt.end_token, ILTypes.PERSON, dt.ref, dt.value)
                        return InstrToken.__correctPerson(res1)
            if (BracketHelper.canBeStartOfSequence(t, False, False)): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t1 = br.end_token
                    t = t1
                    continue
                if (t.next0_ is not None and BracketHelper.canBeEndOfSequence(t.next0_, False, None, False)): 
                    t1 = t.next0_
                    t = t1
                    continue
            if (isinstance(t, TextToken)): 
                if (t.isChar('_')): 
                    t1 = t
                    continue
            r = t.getReferent()
            if (isinstance(r, DateReferent)): 
                tt = t
                if (tt.next0_ is not None and tt.next0_.isCharOf(",;")): 
                    tt = tt.next0_
                if (not t.is_newline_before and not tt.is_newline_after): 
                    t1 = tt
                    continue
                if (not has_word): 
                    return InstrToken._new1420(t, tt, ILTypes.DATE, t)
                if (t != t0): 
                    break
            has_word = True
            if (isinstance(r, InstrumentParticipant)): 
                tt = (Utils.asObjectOrNull(t, ReferentToken)).begin_token
                first_pass3003 = True
                while True:
                    if first_pass3003: first_pass3003 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and (tt.end_char < t.end_char))): break
                    rr = tt.getReferent()
                    if (rr is None): 
                        continue
                    if ((isinstance(rr, OrganizationReferent)) or (isinstance(rr, BankDataReferent)) or (isinstance(rr, UriReferent))): 
                        r = (None)
                        break
            if ((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent)) or (isinstance(r, InstrumentParticipant))): 
                if (t != t0): 
                    break
                if (isinstance(r, InstrumentParticipant)): 
                    pass
                res1 = InstrToken._new1420(t, t, ILTypes.PERSON, t)
                return InstrToken.__correctPerson(res1)
            if (isinstance(r, OrganizationReferent)): 
                if (t != t0): 
                    break
                return InstrToken._new1420(t, t, ILTypes.ORGANIZATION, t)
            if (isinstance(r, DecreePartReferent)): 
                dpr = Utils.asObjectOrNull(r, DecreePartReferent)
                if (dpr.appendix is not None): 
                    if (t.is_newline_before or is_start_of_line): 
                        if (t.is_newline_after or t.whitespaces_before_count > 30): 
                            return InstrToken._new1424(t, t, ILTypes.APPENDIX, "ПРИЛОЖЕНИЕ")
                        ok = True
                        tt = t.next0_
                        first_pass3004 = True
                        while True:
                            if first_pass3004: first_pass3004 = False
                            else: tt = tt.next0_
                            if (not (tt is not None)): break
                            if (tt.is_newline_before): 
                                break
                            npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                            if (npt is not None): 
                                tt = npt.end_token
                                continue
                            ok = False
                            break
                        if (ok): 
                            return InstrToken._new1424(t, t, ILTypes.APPENDIX, "ПРИЛОЖЕНИЕ")
            if ((isinstance(r, DecreeReferent)) and (Utils.asObjectOrNull(r, DecreeReferent)).kind == DecreeKind.PUBLISHER and t == t0): 
                res1 = InstrToken._new1421(t, t, ILTypes.APPROVED)
                tt = t.next0_
                first_pass3005 = True
                while True:
                    if first_pass3005: first_pass3005 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.isCharOf(",;")): 
                        continue
                    if ((isinstance(tt.getReferent(), DecreeReferent)) and (Utils.asObjectOrNull(tt.getReferent(), DecreeReferent)).kind == DecreeKind.PUBLISHER): 
                        res1.end_token = t
                    else: 
                        break
                return res1
            if (t.isValue("ЗА", None) and t.next0_ is not None and t.is_newline_before): 
                rr = t.next0_.getReferent()
                if ((isinstance(rr, PersonReferent)) or (isinstance(rr, PersonPropertyReferent)) or (isinstance(rr, InstrumentParticipant))): 
                    if (t != t0): 
                        break
                    res1 = InstrToken._new1420(t, t.next0_, ILTypes.PERSON, t.next0_)
                    t = t.next0_.next0_
                    if ((isinstance(rr, InstrumentParticipant)) and t is not None): 
                        r = t.getReferent()
                        if ((r) is not None): 
                            if ((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent))): 
                                res1.end_token = t
                                res1.ref = (t)
                    return res1
            ii = 0
            while ii < len(InstrToken._m_directives): 
                if (t.isValue(InstrToken._m_directives[ii], None)): 
                    if (t.next0_ is not None and t.next0_.isValue("СЛЕДУЮЩЕЕ", "НАСТУПНЕ")): 
                        if (t != t0): 
                            break
                        t11 = t.next0_
                        ok = False
                        if (t11.next0_ is not None and t11.next0_.isCharOf(":.") and t11.next0_.is_newline_after): 
                            ok = True
                            t11 = t11.next0_
                        if (ok): 
                            return InstrToken._new1424(t, t11, ILTypes.DIRECTIVE, InstrToken._m_directives_norm[ii])
                    if (t.is_newline_after or ((t.next0_ is not None and t.next0_.isChar(':') and t.next0_.is_newline_after))): 
                        if (t != t0): 
                            break
                        if (not t.is_newline_before): 
                            if ((InstrToken._m_directives_norm[ii] != "ПРИКАЗ" and InstrToken._m_directives_norm[ii] != "ПОСТАНОВЛЕНИЕ" and InstrToken._m_directives_norm[ii] != "НАКАЗ") and InstrToken._m_directives_norm[ii] != "ПОСТАНОВУ"): 
                                break
                        return InstrToken._new1424(t, (t if t.is_newline_after else t.next0_), ILTypes.DIRECTIVE, InstrToken._m_directives_norm[ii])
                    break
                ii += 1
            if (t.is_newline_before and t.chars.is_letter and t.length_char == 1): 
                for d in InstrToken._m_directives: 
                    t11 = MiscHelper.tryAttachWordByLetters(d, t, True)
                    if (t11 is not None): 
                        if (t11.next0_ is not None and t11.next0_.isChar(':')): 
                            t11 = t11.next0_
                        return InstrToken._new1421(t, t11, ILTypes.DIRECTIVE)
            tte = ((Utils.asObjectOrNull(t, MetaToken)).begin_token if (isinstance(t, MetaToken)) else t)
            term = ((Utils.asObjectOrNull(tte, TextToken)).term if isinstance(tte, TextToken) else None)
            if (is_start_of_line and not tte.chars.is_all_lower and t == t0): 
                npt = NounPhraseHelper.tryParse(tte, NounPhraseParseAttr.NO, 0)
                if (npt is not None and ((term == "ПРИЛОЖЕНИЯ" or term == "ДОДАТКИ"))): 
                    npt = (None)
                if (npt is not None and npt.morph.case_.is_nominative and (isinstance(npt.end_token, TextToken))): 
                    term1 = (Utils.asObjectOrNull(npt.end_token, TextToken)).term
                    if (((term1 == "ПРИЛОЖЕНИЕ" or term1 == "ДОДАТОК" or term1 == "МНЕНИЕ") or term1 == "ДУМКА" or term1 == "АКТ") or term1 == "ФОРМА" or term == "ЗАЯВКА"): 
                        tt1 = npt.end_token.next0_
                        dt1 = DecreeToken.tryAttach(tt1, None, False)
                        if (dt1 is not None and dt1.typ == DecreeToken.ItemType.NUMBER): 
                            tt1 = dt1.end_token.next0_
                        elif (isinstance(tt1, NumberToken)): 
                            tt1 = tt1.next0_
                        elif ((isinstance(tt1, TextToken)) and tt1.length_char == 1 and tt1.chars.is_letter): 
                            tt1 = tt1.next0_
                        ok = True
                        if (tt1 is None): 
                            ok = False
                        elif (tt1.isValue("В", "У")): 
                            ok = False
                        elif (not tt1.is_newline_before and InstrToken._checkEntered(tt1) is not None): 
                            ok = False
                        elif (tt1 == t.next0_ and ((tt1.isChar(':') or ((tt1.isValue("НА", None) and term1 != "ЗАЯВКА"))))): 
                            ok = False
                        if (ok): 
                            br = BracketHelper.tryParse(tt1, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                tt1 = br.end_token.next0_
                                if (br.end_token.next0_ is None or not br.end_token.is_newline_after or br.end_token.next0_.isCharOf(";,")): 
                                    ok = False
                                if (tt1 is not None and tt1.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                                    ok = False
                        if (prev is not None and prev.typ == ILTypes.APPENDIX): 
                            ok = False
                        if (ok): 
                            cou = 0
                            ttt = tte.previous
                            while ttt is not None and (cou < 300): 
                                if (ttt.is_table_control_char): 
                                    if (not ttt.isChar(chr(0x1F))): 
                                        if (ttt == tte.previous and ttt.isChar(chr(0x1E))): 
                                            pass
                                        else: 
                                            ok = False
                                    break
                                ttt = ttt.previous; cou += 1
                        if (ok): 
                            it1 = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
                            if (it1 is not None): 
                                if (it1.has_verb): 
                                    ok = False
                        if (ok and t.previous is not None): 
                            ttp = t.previous
                            first_pass3006 = True
                            while True:
                                if first_pass3006: first_pass3006 = False
                                else: ttp = ttp.previous
                                if (not (ttp is not None)): break
                                if (ttp.is_table_control_char and not ttp.isChar(chr(0x1F))): 
                                    continue
                                if (BracketHelper.isBracket(ttp, False) and not BracketHelper.canBeEndOfSequence(ttp, False, None, False)): 
                                    continue
                                if (ttp.isCharOf(";:")): 
                                    ok = False
                                break
                        if ((ok and t.previous is not None and (t.newlines_before_count < 3)) and not t.is_newline_after): 
                            lines = 0
                            ttp = t.previous
                            first_pass3007 = True
                            while True:
                                if first_pass3007: first_pass3007 = False
                                else: ttp = ttp.previous
                                if (not (ttp is not None)): break
                                if (not ttp.is_newline_before): 
                                    continue
                                while ttp is not None and (ttp.end_char < t.begin_char): 
                                    if (isinstance(ttp, NumberToken)): 
                                        pass
                                    elif ((isinstance(ttp, TextToken)) and ttp.length_char > 1): 
                                        if (ttp.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                                            ok = False
                                        break
                                    else: 
                                        break
                                    ttp = ttp.next0_
                                lines += 1
                                if ((lines) > 1): 
                                    break
                        if (ok and ((term1 != "ПРИЛОЖЕНИЕ" and term1 != "ДОДАТОК" and term1 != "МНЕНИЕ"))): 
                            if (t.newlines_before_count < 3): 
                                ok = False
                        if (ok): 
                            return InstrToken._new1424(t, t, ILTypes.APPENDIX, term1)
            app = False
            if ((((term == "ОСОБОЕ" or term == "ОСОБЛИВЕ")) and t.next0_ is not None and t.next0_.isValue("МНЕНИЕ", "ДУМКА")) and t == t0 and is_start_of_line): 
                app = True
            if ((((term == "ДОПОЛНИТЕЛЬНОЕ" or term == "ДОДАТКОВА")) and t.next0_ is not None and t.next0_.isValue("СОГЛАШЕНИЕ", "УГОДА")) and t == t0 and is_start_of_line): 
                app = True
            if (app): 
                tt = t.next0_
                while tt is not None: 
                    if (tt.is_newline_before): 
                        break
                    elif (tt.getMorphClassInDictionary() == MorphClass.VERB): 
                        app = False
                        break
                    tt = tt.next0_
                if (app): 
                    return InstrToken._new1421(t, t.next0_, ILTypes.APPENDIX)
            if (not t.chars.is_all_lower and t == t0): 
                tt = InstrToken._checkApproved(t)
                if (tt is not None): 
                    if (tt.next0_ is not None and (isinstance(tt.next0_.getReferent(), DecreeReferent))): 
                        return InstrToken._new1420(t, tt, ILTypes.APPROVED, tt.next0_.getReferent())
                    dt1 = DecreeToken.tryAttach(tt.next0_, None, False)
                    if (dt1 is not None and dt1.typ == DecreeToken.ItemType.TYP): 
                        return InstrToken._new1421(t, tt, ILTypes.APPROVED)
            t1 = t
            is_start_of_line = False
        if (t1 is None): 
            return None
        res = InstrToken._new1421(t00, t1, ILTypes.UNDEFINED)
        res.no_words = True
        t = t0
        first_pass3008 = True
        while True:
            if first_pass3008: first_pass3008 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= t1.end_char)): break
            if (not ((isinstance(t, TextToken)))): 
                if (isinstance(t, ReferentToken)): 
                    res.no_words = False
                continue
            if (not t.chars.is_letter): 
                continue
            res.no_words = False
            if ((Utils.asObjectOrNull(t, TextToken)).is_pure_verb): 
                res.has_verb = True
        if (t0.isValue("ВОПРОС", "ПИТАННЯ") and t0.next0_ is not None and t0.next0_.isCharOf(":.")): 
            res.typ = ILTypes.QUESTION
        return res
    
    @staticmethod
    def _checkApproved(t : 'Token') -> 'Token':
        from pullenti.morph.MorphClass import MorphClass
        if (t is None): 
            return None
        if (((not t.isValue("УТВЕРЖДЕН", "ЗАТВЕРДЖЕНИЙ") and not t.isValue("УТВЕРЖДАТЬ", "СТВЕРДЖУВАТИ") and not t.isValue("УТВЕРДИТЬ", "ЗАТВЕРДИТИ")) and not t.isValue("ВВЕСТИ", None) and not t.isValue("СОГЛАСОВАНО", "ПОГОДЖЕНО")) and not t.isValue("СОГЛАСОВАТЬ", "ПОГОДИТИ")): 
            return None
        if (t.morph.containsAttr("инф.", MorphClass()) and t.morph.containsAttr("сов.в.", MorphClass())): 
            return None
        if (t.morph.containsAttr("возвр.", MorphClass())): 
            return None
        t0 = t
        t1 = t
        t = t.next0_
        first_pass3009 = True
        while True:
            if first_pass3009: first_pass3009 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction): 
                continue
            if (t.isChar(':')): 
                continue
            if (t.isValue("ДЕЙСТВИЕ", "ДІЯ") or t.isValue("ВВЕСТИ", None) or t.isValue("ВВОДИТЬ", "ВВОДИТИ")): 
                t1 = t
                continue
            tt = InstrToken._checkApproved(t)
            if (tt is not None): 
                if (not tt.is_newline_before and tt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False) != t0.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)): 
                    tt = t
                    t1 = tt
                    continue
            break
        return t1
    
    @staticmethod
    def _checkEntered(t : 'Token') -> 'Token':
        if (t is None): 
            return None
        if ((((t.isValue("ВСТУПАТЬ", "ВСТУПАТИ") or t.isValue("ВСТУПИТЬ", "ВСТУПИТИ"))) and t.next0_ is not None and t.next0_.isValue("В", "У")) and t.next0_.next0_ is not None and t.next0_.next0_.isValue("СИЛА", "ЧИННІСТЬ")): 
            return t.next0_.next0_
        if (t.isValue("УТРАТИТЬ", "ВТРАТИТИ") and t.next0_ is not None and t.next0_.isValue("СИЛА", "ЧИННІСТЬ")): 
            return t.next0_
        if (t.isValue("ДЕЙСТВОВАТЬ", "ДІЯТИ") and t.next0_ is not None and t.next0_.isValue("ДО", None)): 
            return t.next0_
        if (((t.isValue("В", None) or t.isValue("B", None))) and t.next0_ is not None): 
            if (t.next0_.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                return t.next0_
            if (t.next0_.isValue("РЕД", None)): 
                if (t.next0_.next0_ is not None and t.next0_.next0_.isChar('.')): 
                    return t.next0_.next0_
                return t.next0_
        if (t.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
            return t.next0_
        if (t.isValue("РЕД", None)): 
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                return t.next0_
            return t
        return InstrToken._checkApproved(t)
    
    _m_directives = None
    
    _m_directives_norm = None
    
    @staticmethod
    def _new1420(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ILTypes', _arg4 : object) -> 'InstrToken':
        res = InstrToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new1421(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ILTypes') -> 'InstrToken':
        res = InstrToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1424(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ILTypes', _arg4 : str) -> 'InstrToken':
        res = InstrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1426(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ILTypes', _arg4 : object, _arg5 : str) -> 'InstrToken':
        res = InstrToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.value = _arg5
        return res
    
    # static constructor for class InstrToken
    @staticmethod
    def _static_ctor():
        InstrToken._m_directives = list(["ПРИКАЗЫВАТЬ", "ПРИКАЗАТЬ", "ОПРЕДЕЛЯТЬ", "ОПРЕДЕЛИТЬ", "ПОСТАНОВЛЯТЬ", "ПОСТАНОВИТЬ", "УСТАНОВИТЬ", "РЕШИЛ", "РЕШИТЬ", "ПРОСИТЬ", "ПРИГОВАРИВАТЬ", "ПРИГОВОРИТЬ", "НАКАЗУВАТИ", "ВИЗНАЧАТИ", "ВИЗНАЧИТИ", "УХВАЛЮВАТИ", "ПОСТАНОВЛЯТИ", "ПОСТАНОВИТИ", "ВСТАНОВИТИ", "ВИРІШИВ", "ВИРІШИТИ", "ПРОСИТИ", "ПРИМОВЛЯТИ", "ЗАСУДИТИ"])
        InstrToken._m_directives_norm = list(["ПРИКАЗ", "ПРИКАЗ", "ОПРЕДЕЛЕНИЕ", "ОПРЕДЕЛЕНИЕ", "ПОСТАНОВЛЕНИЕ", "ПОСТАНОВЛЕНИЕ", "УСТАНОВЛЕНИЕ", "РЕШЕНИЕ", "РЕШЕНИЕ", "ЗАЯВЛЕНИЕ", "ПРИГОВОР", "ПРИГОВОР", "НАКАЗ", "УХВАЛА", "УХВАЛА", "ПОСТАНОВА", "ПОСТАНОВА", "ПОСТАНОВА", "ВСТАНОВЛЕННЯ", "РІШЕННЯ", "РІШЕННЯ", "ЗАЯВА", "ВИРОК", "ВИРОК"])

InstrToken._static_ctor()