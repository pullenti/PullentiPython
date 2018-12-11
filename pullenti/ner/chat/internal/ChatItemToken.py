# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import datetime
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.chat.VerbType import VerbType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.chat.ChatType import ChatType
from pullenti.ner.chat.ChatAnalyzer import ChatAnalyzer
from pullenti.ner.date.internal.DateExToken import DateExToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper

class ChatItemToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.not0_ = False
        self.typ = ChatType.UNDEFINED
        self.vtyp = VerbType.UNDEFINED
        self.value = None;
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(Utils.enumToString(self.typ), end="", file=tmp)
        if (self.not0_): 
            print(" not", end="", file=tmp)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=tmp, flush=True)
        if (self.vtyp != VerbType.UNDEFINED): 
            print(" [{0}]".format(Utils.enumToString(self.vtyp)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def __isEmptyToken(t : 'Token') -> bool:
        if (not ((isinstance(t, TextToken)))): 
            return False
        if (t.length_char == 1): 
            return True
        mc = t.getMorphClassInDictionary()
        if ((((mc.is_misc or mc.is_adverb or mc.is_conjunction) or mc.is_preposition or mc.is_personal_pronoun) or mc.is_pronoun or mc.is_conjunction) or mc.is_preposition): 
            return True
        return False
    
    @staticmethod
    def tryParse(t : 'Token') -> 'ChatItemToken':
        tok = None
        not0__ = False
        t0 = None
        t1 = None
        has_modal = False
        tt = t
        first_pass2788 = True
        while True:
            if first_pass2788: first_pass2788 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (not ((isinstance(tt, TextToken)))): 
                break
            if (tt != t and tt.is_newline_before): 
                break
            if (tt.isCharOf(".?!")): 
                break
            if (tt.length_char == 1): 
                continue
            tok = ChatItemToken.__m_ontology.tryParse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                break
            dtok = DateExToken.tryParse(tt)
            if (dtok is not None): 
                dt = dtok.getDate((datetime.datetime.now() if ChatAnalyzer.CURRENT_DATE_TIME is None else ChatAnalyzer.CURRENT_DATE_TIME), 1)
                if (dt is not None): 
                    res = ChatItemToken._new457(tt, dtok.end_token, ChatType.DATE)
                    res.value = "{0}.{1}.{2}".format(dt.year, "{:02d}".format(dt.month), "{:02d}".format(dt.day))
                    if (dt.hour > 0 or dt.minute > 0): 
                        res.value = "{0} {1}:{2}".format(res.value, "{:02d}".format(dt.hour), "{:02d}".format(dt.minute))
                    return res
            mc = tt.getMorphClassInDictionary()
            term = (tt).term
            if (term == "НЕ"): 
                not0__ = True
                if (t0 is None): 
                    t0 = tt
                continue
            if ((mc.is_personal_pronoun or mc.is_pronoun or mc.is_conjunction) or mc.is_preposition): 
                continue
            if (tt.isValue("ХОТЕТЬ", None) or tt.isValue("ЖЕЛАТЬ", None) or tt.isValue("МОЧЬ", None)): 
                has_modal = True
                if (t0 is None): 
                    t0 = tt
                t1 = tt
                continue
            if (mc.is_adverb or mc.is_misc): 
                continue
            if (mc.is_verb): 
                res = ChatItemToken(tt, tt)
                res.typ = ChatType.VERB
                res.value = (tt).getLemma()
                if (not0__): 
                    res.not0_ = True
                if (t0 is not None): 
                    res.begin_token = t0
                return res
        if (tok is not None): 
            res = ChatItemToken(tok.begin_token, tok.end_token)
            res.typ = (Utils.valToEnum(tok.termin.tag, ChatType))
            if (isinstance(tok.termin.tag2, VerbType)): 
                res.vtyp = (Utils.valToEnum(tok.termin.tag2, VerbType))
            if (res.typ == ChatType.VERB and tok.begin_token == tok.end_token and (isinstance(tok.begin_token, TextToken))): 
                res.value = (tok.begin_token).getLemma()
            else: 
                res.value = MiscHelper.getTextValueOfMetaToken(res, GetTextAttr.NO)
            if (not0__): 
                res.not0_ = True
            if (t0 is not None): 
                res.begin_token = t0
            if (res.typ == ChatType.REPEAT): 
                tt = tok.end_token.next0_
                first_pass2789 = True
                while True:
                    if first_pass2789: first_pass2789 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (not ((isinstance(tt, TextToken)))): 
                        break
                    if (ChatItemToken.__isEmptyToken(tt)): 
                        continue
                    tok1 = ChatItemToken.__m_ontology.tryParse(tt, TerminParseAttr.NO)
                    if (tok1 is not None): 
                        if ((Utils.valToEnum(tok1.termin.tag, ChatType)) == ChatType.ACCEPT or (Utils.valToEnum(tok1.termin.tag, ChatType)) == ChatType.MISC): 
                            tt = tok1.end_token
                            continue
                        if ((Utils.valToEnum(tok1.termin.tag, ChatType)) == ChatType.REPEAT): 
                            res.end_token = tok1.end_token
                            tt = res.end_token
                            continue
                        break
                    npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                    if (npt is not None): 
                        if (npt.end_token.isValue("ВОПРОС", None) or npt.end_token.isValue("ФРАЗА", None) or npt.end_token.isValue("ПРЕДЛОЖЕНИЕ", None)): 
                            res.end_token = npt.end_token
                            tt = res.end_token
                            res.value = npt.getNormalCaseText(None, False, MorphGender.UNDEFINED, False)
                            continue
                    break
            return res
        if (not0__ and has_modal): 
            res = ChatItemToken(t0, t1)
            res.typ = ChatType.CANCEL
            return res
        return None
    
    __m_ontology = None
    
    @staticmethod
    def initialize() -> None:
        if (ChatItemToken.__m_ontology is not None): 
            return
        ChatItemToken.__m_ontology = TerminCollection()
        t = Termin._new118("ДА", ChatType.ACCEPT)
        t.addVariant("КОНЕЧНО", False)
        t.addVariant("РАЗУМЕЕТСЯ", False)
        t.addVariant("ПОЖАЛУЙСТА", False)
        t.addVariant("ПОЖАЛУЙ", False)
        t.addVariant("ПЛИЗ", False)
        t.addVariant("НЕПРЕМЕННО", False)
        t.addVariant("ЕСТЬ", False)
        t.addVariant("АГА", False)
        t.addVariant("УГУ", False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("НЕТ", ChatType.CANCEL)
        t.addVariant("ДА НЕТ", False)
        t.addVariant("НИ ЗА ЧТО", False)
        t.addVariant("НЕ ХОТЕТЬ", False)
        t.addVariant("ОТСТАТЬ", False)
        t.addVariant("НИКТО", False)
        t.addVariant("НИЧТО", False)
        t.addVariant("НИЧЕГО", False)
        t.addVariant("НИГДЕ", False)
        t.addVariant("НИКОГДА", False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("СПАСИБО", ChatType.THANKS)
        t.addVariant("БЛАГОДАРИТЬ", False)
        t.addVariant("БЛАГОДАРСТВОВАТЬ", False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("НУ", ChatType.MISC)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("ПРИВЕТ", ChatType.MISC)
        for s in ["ЗДРАВСТВУЙ", "ЗДРАВСТВУЙТЕ", "ПРИВЕТИК", "ХЭЛЛОУ", "АЛЛЕ", "ДОБРЫЙ ДЕНЬ", "ДОБРЫЙ ВЕЧЕР", "ДОБРОЕ УТРО", "ДОБРАЯ НОЧЬ", "ЗДОРОВО"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("ПОКА", ChatType.BYE)
        for s in ["ДО СВИДАНИЯ", "ДОСВИДАНИЯ", "ПРОЩАЙ", "ПРОЩАЙТЕ", "ХОРОШЕГО ДНЯ", "ВСЕГО ХОРОШЕГО", "ВСЕГО ДОБРОГО", "ВСЕХ БЛАГ", "СЧАСТЛИВО", "ПРОЩАЙ", "ПРОЩАЙТЕ", "ЧАО", "ГУД БАЙ", "ГУДБАЙ"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new120("ГОВОРИТЬ", ChatType.VERB, VerbType.SAY)
        for s in ["СКАЗАТЬ", "РАЗГОВАРИВАТЬ", "ПРОИЗНЕСТИ", "ПРОИЗНОСИТЬ", "ОТВЕТИТЬ", "ОТВЕЧАТЬ", "СПРАШИВАТЬ", "СПРОСИТЬ", "ПОТОВОРИТЬ", "ОБЩАТЬСЯ", "ПООБЩАТЬСЯ"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new120("ЗВОНИТЬ", ChatType.VERB, VerbType.CALL)
        for s in ["ПЕРЕЗВОНИТЬ", "ПОЗВОНИТЬ", "СДЕЛАТЬ ЗВОНОК", "НАБРАТЬ"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new120("БЫТЬ", ChatType.VERB, VerbType.BE)
        for s in ["ЯВЛЯТЬСЯ"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new120("ИМЕТЬ", ChatType.VERB, VerbType.HAVE)
        for s in ["ОБЛАДАТЬ", "ВЛАДЕТЬ"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("ПОЗЖЕ", ChatType.LATER)
        for s in ["ПОПОЗЖЕ", "ПОЗДНЕЕ", "ПОТОМ", "НЕКОГДА"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("ЗАНЯТ", ChatType.BUSY)
        for s in ["НЕУДОБНО", "НЕ УДОБНО", "НЕТ ВРЕМЕНИ", "ПАРАЛЛЕЛЬНЫЙ ЗВОНОК", "СОВЕЩАНИЕ", "ОБЕД", "ТРАНСПОРТ", "МЕТРО"]: 
            t.addVariant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new118("ПОВТОРИТЬ", ChatType.REPEAT)
        t.addVariant("НЕ РАССЛЫШАТЬ", False)
        t.addVariant("НЕ УСЛЫШАТЬ", False)
        t.addVariant("ПЛОХО СЛЫШНО", False)
        t.addVariant("ПЛОХАЯ СВЯЗЬ", False)
        ChatItemToken.__m_ontology.add(t)
    
    @staticmethod
    def _new457(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ChatType') -> 'ChatItemToken':
        res = ChatItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res