# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken

from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType


class TitleItemToken(MetaToken):
    
    class Types(IntEnum):
        UNDEFINED = 0
        TYP = 0 + 1
        THEME = (0 + 1) + 1
        TYPANDTHEME = ((0 + 1) + 1) + 1
        BOSS = (((0 + 1) + 1) + 1) + 1
        WORKER = ((((0 + 1) + 1) + 1) + 1) + 1
        EDITOR = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        CONSULTANT = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
        OPPONENT = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        OTHERROLE = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        TRANSLATE = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        ADOPT = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        DUST = (((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        SPECIALITY = ((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        KEYWORDS = (((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    def __init__(self, begin : 'Token', end : 'Token', typ_ : 'Types') -> None:
        self.typ = TitleItemToken.Types.UNDEFINED
        self.value = None
        super().__init__(begin, end, None)
        self.typ = typ_
    
    def __str__(self) -> str:
        return "{0}: {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, ""))
    
    @staticmethod
    def try_attach(t : 'Token') -> 'TitleItemToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is not None): 
            t1 = tt
            if (tt.term == "ТЕМА"): 
                tit = TitleItemToken.try_attach(tt.next0_)
                if (tit is not None and tit.typ == TitleItemToken.Types.TYP): 
                    t1 = tit.end_token
                    if (t1.next0_ is not None and t1.next0_.is_char(':')): 
                        t1 = t1.next0_
                    return TitleItemToken._new2470(t, t1, TitleItemToken.Types.TYPANDTHEME, tit.value)
                if (tt.next0_ is not None and tt.next0_.is_char(':')): 
                    t1 = tt.next0_
                return TitleItemToken(tt, t1, TitleItemToken.Types.THEME)
            if (tt.term == "ПО" or tt.term == "НА"): 
                if (tt.next0_ is not None and tt.next0_.is_value("ТЕМА", None)): 
                    t1 = tt.next0_
                    if (t1.next0_ is not None and t1.next0_.is_char(':')): 
                        t1 = t1.next0_
                    return TitleItemToken(tt, t1, TitleItemToken.Types.THEME)
            if (tt.term == "ПЕРЕВОД" or tt.term == "ПЕР"): 
                tt2 = tt.next0_
                if (tt2 is not None and tt2.is_char('.')): 
                    tt2 = tt2.next0_
                if (isinstance(tt2, TextToken)): 
                    if ((tt2 if isinstance(tt2, TextToken) else None).term == "C" or (tt2 if isinstance(tt2, TextToken) else None).term == "С"): 
                        tt2 = tt2.next0_
                        if (isinstance(tt2, TextToken)): 
                            return TitleItemToken(t, tt2, TitleItemToken.Types.TRANSLATE)
            if (tt.term == "СЕКЦИЯ" or tt.term == "SECTION" or tt.term == "СЕКЦІЯ"): 
                t1 = tt.next0_
                if (t1 is not None and t1.is_char(':')): 
                    t1 = t1.next0_
                br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t1 = br.end_token
                elif (t1 != tt.next0_): 
                    while t1 is not None: 
                        if (t1.is_newline_after): 
                            break
                        t1 = t1.next0_
                    if (t1 is None): 
                        return None
                if (t1 != tt.next0_): 
                    return TitleItemToken(tt, t1, TitleItemToken.Types.DUST)
            t1 = None
            if (tt.is_value("СПЕЦИАЛЬНОСТЬ", "СПЕЦІАЛЬНІСТЬ")): 
                t1 = tt.next0_
            elif (tt.morph.class0_.is_preposition and tt.next0_ is not None and tt.next0_.is_value("СПЕЦИАЛЬНОСТЬ", "СПЕЦІАЛЬНІСТЬ")): 
                t1 = tt.next0_.next0_
            elif (tt.is_char('/') and tt.is_newline_before): 
                t1 = tt.next0_
            if (t1 is not None): 
                if (t1.is_char_of(":") or t1.is_hiphen): 
                    t1 = t1.next0_
                spec = TitleItemToken.__try_attach_speciality(t1, True)
                if (spec is not None): 
                    spec.begin_token = t
                    return spec
        sss = TitleItemToken.__try_attach_speciality(t, False)
        if (sss is not None): 
            return sss
        if (isinstance(t, ReferentToken)): 
            return None
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
        if (npt is not None): 
            s = npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
            tok = TitleItemToken.__m_termins.try_parse(npt.end_token, TerminParseAttr.NO)
            if (tok is not None): 
                ty = Utils.valToEnum(tok.termin.tag, TitleItemToken.Types)
                if (ty == TitleItemToken.Types.TYP): 
                    tit = TitleItemToken.try_attach(tok.end_token.next0_)
                    if (tit is not None and tit.typ == TitleItemToken.Types.THEME): 
                        return TitleItemToken._new2470(npt.begin_token, tit.end_token, TitleItemToken.Types.TYPANDTHEME, s)
                    if (s == "РАБОТА" or s == "РОБОТА" or s == "ПРОЕКТ"): 
                        return None
                    t1 = tok.end_token
                    if (s == "ДИССЕРТАЦИЯ" or s == "ДИСЕРТАЦІЯ"): 
                        err = 0
                        ttt = t1.next0_
                        first_pass3052 = True
                        while True:
                            if first_pass3052: first_pass3052 = False
                            else: ttt = ttt.next0_
                            if (not (ttt is not None)): break
                            if (ttt.morph.class0_.is_preposition): 
                                continue
                            if (ttt.is_value("СОИСКАНИЕ", "")): 
                                continue
                            npt1 = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0)
                            if (npt1 is not None and npt1.noun.is_value("СТЕПЕНЬ", "СТУПІНЬ")): 
                                ttt = npt1.end_token
                                t1 = ttt
                                continue
                            rt = t1.kit.process_referent("PERSON", ttt)
                            if (rt is not None and isinstance(rt.referent, PersonPropertyReferent)): 
                                ppr = (rt.referent if isinstance(rt.referent, PersonPropertyReferent) else None)
                                if (ppr.name == "доктор наук"): 
                                    t1 = rt.end_token
                                    s = "ДОКТОРСКАЯ ДИССЕРТАЦИЯ"
                                    break
                                elif (ppr.name == "кандидат наук"): 
                                    t1 = rt.end_token
                                    s = "КАНДИДАТСКАЯ ДИССЕРТАЦИЯ"
                                    break
                                elif (ppr.name == "магистр"): 
                                    t1 = rt.end_token
                                    s = "МАГИСТЕРСКАЯ ДИССЕРТАЦИЯ"
                                    break
                            if (ttt.is_value("ДОКТОР", None) or ttt.is_value("КАНДИДАТ", None) or ttt.is_value("МАГИСТР", "МАГІСТР")): 
                                t1 = ttt
                                npt1 = NounPhraseHelper.try_parse(ttt.next0_, NounPhraseParseAttr.NO, 0)
                                if (npt1 is not None and npt1.end_token.is_value("НАУК", None)): 
                                    t1 = npt1.end_token
                                s = ("МАГИСТЕРСКАЯ ДИССЕРТАЦИЯ" if ttt.is_value("МАГИСТР", "МАГІСТР") else ("ДОКТОРСКАЯ ДИССЕРТАЦИЯ" if ttt.is_value("ДОКТОР", None) else "КАНДИДАТСКАЯ ДИССЕРТАЦИЯ"))
                                break
                            err += 1
                            if ((err) > 3): 
                                break
                    if (t1.next0_ is not None and t1.next0_.is_char('.')): 
                        t1 = t1.next0_
                    if (s.endswith("ОТЧЕТ") and t1.next0_ is not None and t1.next0_.is_value("О", None)): 
                        npt1 = NounPhraseHelper.try_parse(t1.next0_, NounPhraseParseAttr.PARSEPREPOSITION, 0)
                        if (npt1 is not None and npt1.morph.case.is_prepositional): 
                            t1 = npt1.end_token
                    return TitleItemToken._new2470(npt.begin_token, t1, ty, s)
        tok1 = TitleItemToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if (tok1 is not None): 
            t1 = tok1.end_token
            re = TitleItemToken(tok1.begin_token, t1, Utils.valToEnum(tok1.termin.tag, TitleItemToken.Types))
            return re
        if (BracketHelper.can_be_start_of_sequence(t, False, False)): 
            tok1 = TitleItemToken.__m_termins.try_parse(t.next0_, TerminParseAttr.NO)
            if (tok1 is not None and BracketHelper.can_be_end_of_sequence(tok1.end_token.next0_, False, None, False)): 
                t1 = tok1.end_token.next0_
                return TitleItemToken(tok1.begin_token, t1, Utils.valToEnum(tok1.termin.tag, TitleItemToken.Types))
        return None
    
    @staticmethod
    def __try_attach_speciality(t : 'Token', key_word_before : bool) -> 'TitleItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (t is None): 
            return None
        susp = False
        if (not key_word_before): 
            if (not t.is_newline_before): 
                susp = True
        val = None
        t0 = t
        dig_count = 0
        for i in range(3):
            nt = (t if isinstance(t, NumberToken) else None)
            if (nt is None): 
                break
            if (nt.typ != NumberSpellingType.DIGIT or nt.morph.class0_.is_adjective): 
                break
            if (val is None): 
                val = Utils.newStringIO(None)
            if (susp and t.length_char != 2): 
                return None
            digs = nt.get_source_text()
            dig_count += len(digs)
            print(digs, end="", file=val)
            if (t.next0_ is None): 
                break
            t = t.next0_
            if (t.is_char_of(".,") or t.is_hiphen): 
                if (susp and (i < 2)): 
                    if (not t.is_char('.') or t.is_whitespace_after or t.is_whitespace_before): 
                        return None
                if (t.next0_ is not None): 
                    t = t.next0_
        if (val is None or (dig_count < 5)): 
            return None
        if (dig_count != 6): 
            if (not key_word_before): 
                return None
        else: 
            Utils.insertStringIO(val, 4, '.')
            Utils.insertStringIO(val, 2, '.')
        tt = t.next0_
        first_pass3053 = True
        while True:
            if first_pass3053: first_pass3053 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                break
            br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
            if (br is not None): 
                tt = br.end_token
                t = tt
                continue
            t = tt
        return TitleItemToken._new2470(t0, t, TitleItemToken.Types.SPECIALITY, Utils.toStringStringIO(val))
    
    __m_termins = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (TitleItemToken.__m_termins is not None): 
            return
        TitleItemToken.__m_termins = TerminCollection()
        for s in ["РАБОТА", "ДИССЕРТАЦИЯ", "ОТЧЕТ", "ОБЗОР", "ДИПЛОМ", "ПРОЕКТ", "СПРАВКА", "АВТОРЕФЕРАТ", "РЕФЕРАТ", "TECHNOLOGY ISSUES", "TECHNOLOGY COURSE", "УЧЕБНИК", "УЧЕБНОЕ ПОСОБИЕ"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.TYP))
        for s in ["РОБОТА", "ДИСЕРТАЦІЯ", "ЗВІТ", "ОГЛЯД", "ДИПЛОМ", "ПРОЕКТ", "ДОВІДКА", "АВТОРЕФЕРАТ", "РЕФЕРАТ"]: 
            TitleItemToken.__m_termins.add(Termin._new477(s, MorphLang.UA, TitleItemToken.Types.TYP))
        for s in ["ДОПУСТИТЬ К ЗАЩИТА", "РЕКОМЕНДОВАТЬ К ЗАЩИТА", "ДОЛЖНОСТЬ", "ЦЕЛЬ РАБОТЫ", "НА ПРАВАХ РУКОПИСИ", "ПО ИЗДАНИЮ", "ПОЛУЧЕНО"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.DUST))
        for s in ["ДОПУСТИТИ ДО ЗАХИСТУ", "РЕКОМЕНДУВАТИ ДО ЗАХИСТ", "ПОСАДА", "МЕТА РОБОТИ", "НА ПРАВАХ РУКОПИСУ", "ПО ВИДАННЮ", "ОТРИМАНО"]: 
            TitleItemToken.__m_termins.add(Termin._new477(s, MorphLang.UA, TitleItemToken.Types.DUST))
        for s in ["УТВЕРЖДАТЬ", "СОГЛАСЕН", "СТВЕРДЖУВАТИ", "ЗГОДЕН"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.ADOPT))
        for s in ["НАУЧНЫЙ РУКОВОДИТЕЛЬ", "РУКОВОДИТЕЛЬ РАБОТА", "НАУКОВИЙ КЕРІВНИК", "КЕРІВНИК РОБОТА"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.BOSS))
        for s in ["НАУЧНЫЙ КОНСУЛЬТАНТ", "КОНСУЛЬТАНТ", "НАУКОВИЙ КОНСУЛЬТАНТ"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.CONSULTANT))
        for s in ["РЕДАКТОР", "РЕДАКТОРСКАЯ ГРУППА", "РЕЦЕНЗЕНТ", "РЕДАКТОРСЬКА ГРУПА"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.EDITOR))
        for s in ["ОФИЦИАЛЬНЫЙ ОППОНЕНТ", "ОППОНЕНТ", "ОФІЦІЙНИЙ ОПОНЕНТ"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.OPPONENT))
        for s in ["ИСПОЛНИТЕЛЬ", "ОТВЕТСТВЕННЫЙ ИСПОЛНИТЕЛЬ", "АВТОР", "ДИПЛОМНИК", "КОЛЛЕКТТИВ ИСПОЛНИТЕЛЕЙ", "ВЫПОЛНИТЬ", "ИСПОЛНИТЬ"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.WORKER))
        for s in ["ВИКОНАВЕЦЬ", "ВІДПОВІДАЛЬНИЙ ВИКОНАВЕЦЬ", "АВТОР", "ДИПЛОМНИК", "КОЛЛЕКТТИВ ВИКОНАВЦІВ", "ВИКОНАТИ", "ВИКОНАТИ"]: 
            TitleItemToken.__m_termins.add(Termin._new477(s, MorphLang.UA, TitleItemToken.Types.WORKER))
        for s in ["КЛЮЧЕВЫЕ СЛОВА", "KEYWORDS", "КЛЮЧОВІ СЛОВА"]: 
            TitleItemToken.__m_termins.add(Termin._new118(s, TitleItemToken.Types.KEYWORDS))

    
    @staticmethod
    def _new2470(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Types', _arg4 : str) -> 'TitleItemToken':
        res = TitleItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        return res