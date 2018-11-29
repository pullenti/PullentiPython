# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
import operator
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.keyword.KeywordType import KeywordType
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr


class KeywordAnalyzer(Analyzer):
    """ Анализатор ключевых комбинаций """
    
    class CompByRank(object):
        
        def compare(self, x : 'Referent', y : 'Referent') -> int:
            from pullenti.ner.keyword.KeywordReferent import KeywordReferent
            d1 = (Utils.asObjectOrNull(x, KeywordReferent)).rank
            d2 = (Utils.asObjectOrNull(y, KeywordReferent)).rank
            if (d1 > d2): 
                return -1
            if (d1 < d2): 
                return 1
            return 0
    
    ANALYZER_NAME = "KEYWORD"
    
    @property
    def name(self) -> str:
        return KeywordAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Ключевые слова"
    
    @property
    def description(self) -> str:
        return "Ключевые слова для различных аналитических систем"
    
    def clone(self) -> 'Analyzer':
        return KeywordAnalyzer()
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ALL"]
    
    @property
    def is_specific(self) -> bool:
        return True
    
    def createAnalyzerData(self) -> 'AnalyzerData':
        from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
        return AnalyzerDataWithOntology()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.keyword.internal.KeywordMeta import KeywordMeta
        return [KeywordMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.keyword.internal.KeywordMeta import KeywordMeta
        res = dict()
        res[KeywordMeta.IMAGE_OBJ] = EpNerCoreInternalResourceHelper.getBytes("kwobject.png")
        res[KeywordMeta.IMAGE_PRED] = EpNerCoreInternalResourceHelper.getBytes("kwpredicate.png")
        res[KeywordMeta.IMAGE_REF] = EpNerCoreInternalResourceHelper.getBytes("kwreferent.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        if (type0_ == KeywordReferent.OBJ_TYPENAME): 
            return KeywordReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        """ Основная функция выделения телефонов
        
        Args:
            cnt: 
            stage: 
        
        """
        from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.Explanatory import Explanatory
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        ad = kit.getAnalyzerData(self)
        has_denoms = False
        for a in kit.processor.analyzers: 
            if ((isinstance(a, DenominationAnalyzer)) and not a.ignore_this_analyzer): 
                has_denoms = True
        if (not has_denoms): 
            a = DenominationAnalyzer()
            a.process(kit)
        li = list()
        tmp = io.StringIO()
        tmp2 = list()
        max0_ = 0
        t = kit.first_token
        while t is not None: 
            max0_ += 1
            t = t.next0_
        cur = 0
        t = kit.first_token
        first_pass3036 = True
        while True:
            if first_pass3036: first_pass3036 = False
            else: t = t.next0_; cur += 1
            if (not (t is not None)): break
            r = t.getReferent()
            if (r is not None): 
                t = self.__addReferents(ad, t, cur, max0_)
                continue
            if (not ((isinstance(t, TextToken)))): 
                continue
            if (not t.chars.is_letter or (t.length_char < 3)): 
                continue
            term = (Utils.asObjectOrNull(t, TextToken)).term
            if (term == "ЕСТЬ"): 
                if ((isinstance(t.previous, TextToken)) and t.previous.morph.class0_.is_verb): 
                    pass
                else: 
                    continue
            npt = None
            npt = NounPhraseHelper.tryParse(t, Utils.valToEnum((NounPhraseParseAttr.ADJECTIVECANBELAST) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0)
            if (npt is None): 
                mc = t.getMorphClassInDictionary()
                if (mc.is_verb and not mc.is_preposition): 
                    if ((Utils.asObjectOrNull(t, TextToken)).is_verb_be): 
                        continue
                    if (t.isValue("МОЧЬ", None) or t.isValue("WOULD", None)): 
                        continue
                    kref = KeywordReferent._new1502(KeywordType.PREDICATE)
                    norm = t.getNormalCaseText(MorphClass.VERB, True, MorphGender.UNDEFINED, False)
                    if (norm is None): 
                        norm = (Utils.asObjectOrNull(t, TextToken)).getLemma()
                    if (norm.endswith("ЬСЯ")): 
                        norm = norm[0:0+len(norm) - 2]
                    kref.addSlot(KeywordReferent.ATTR_VALUE, norm, False, 0)
                    drv = Explanatory.findDerivates(norm, True, t.morph.language)
                    KeywordAnalyzer.__addNormals(kref, drv, norm)
                    kref = (Utils.asObjectOrNull(ad.registerReferent(kref), KeywordReferent))
                    KeywordAnalyzer.__setRank(kref, cur, max0_)
                    rt1 = ReferentToken._new746(ad.registerReferent(kref), t, t, t.morph)
                    kit.embedToken(rt1)
                    t = (rt1)
                    continue
                continue
            if (npt.internal_noun is not None): 
                continue
            if (npt.end_token.isValue("ЦЕЛОМ", None) or npt.end_token.isValue("ЧАСТНОСТИ", None)): 
                if (npt.preposition is not None): 
                    t = npt.end_token
                    continue
            if (npt.end_token.isValue("СТОРОНЫ", None) and npt.preposition is not None and npt.preposition.isValue("С", None)): 
                t = npt.end_token
                continue
            if (npt.begin_token == npt.end_token): 
                mc = t.getMorphClassInDictionary()
                if (mc.is_preposition): 
                    continue
                elif (mc.is_adverb): 
                    if (t.isValue("ПОТОМ", None)): 
                        continue
            else: 
                pass
            li.clear()
            t0 = t
            tt = t
            first_pass3037 = True
            while True:
                if first_pass3037: first_pass3037 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= npt.end_char)): break
                if (not ((isinstance(tt, TextToken)))): 
                    continue
                if (tt.isValue("NATURAL", None)): 
                    pass
                if ((tt.length_char < 3) or not tt.chars.is_letter): 
                    continue
                mc = tt.getMorphClassInDictionary()
                if ((mc.is_preposition or mc.is_pronoun or mc.is_personal_pronoun) or mc.is_conjunction): 
                    if (tt.isValue("ОТНОШЕНИЕ", None)): 
                        pass
                    else: 
                        continue
                if (mc.is_misc): 
                    if (MiscHelper.isEngArticle(tt)): 
                        continue
                kref = KeywordReferent._new1502(KeywordType.OBJECT)
                norm = (Utils.asObjectOrNull(tt, TextToken)).getLemma()
                kref.addSlot(KeywordReferent.ATTR_VALUE, norm, False, 0)
                if (norm != "ЕСТЬ"): 
                    drv = Explanatory.findDerivates(norm, True, tt.morph.language)
                    KeywordAnalyzer.__addNormals(kref, drv, norm)
                kref = (Utils.asObjectOrNull(ad.registerReferent(kref), KeywordReferent))
                KeywordAnalyzer.__setRank(kref, cur, max0_)
                rt1 = ReferentToken._new746(kref, tt, tt, tt.morph)
                kit.embedToken(rt1)
                if (tt == t and len(li) == 0): 
                    t0 = (rt1)
                t = (rt1)
                li.append(kref)
            if (len(li) > 1): 
                kref = KeywordReferent._new1502(KeywordType.OBJECT)
                Utils.setLengthStringIO(tmp, 0)
                tmp2.clear()
                has_norm = False
                for kw in li: 
                    s = kw.getStringValue(KeywordReferent.ATTR_VALUE)
                    if (tmp.tell() > 0): 
                        print(' ', end="", file=tmp)
                    print(s, end="", file=tmp)
                    n = kw.getStringValue(KeywordReferent.ATTR_NORMAL)
                    if (n is not None): 
                        has_norm = True
                        tmp2.append(n)
                    else: 
                        tmp2.append(s)
                    kref.addSlot(KeywordReferent.ATTR_REF, kw, False, 0)
                val = npt.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False)
                kref.addSlot(KeywordReferent.ATTR_VALUE, val, False, 0)
                Utils.setLengthStringIO(tmp, 0)
                tmp2.sort()
                for s in tmp2: 
                    if (tmp.tell() > 0): 
                        print(' ', end="", file=tmp)
                    print(s, end="", file=tmp)
                norm = Utils.toStringStringIO(tmp)
                if (norm != val): 
                    kref.addSlot(KeywordReferent.ATTR_NORMAL, norm, False, 0)
                kref = (Utils.asObjectOrNull(ad.registerReferent(kref), KeywordReferent))
                KeywordAnalyzer.__setRank(kref, cur, max0_)
                rt1 = ReferentToken._new746(kref, t0, t, npt.morph)
                kit.embedToken(rt1)
                t = (rt1)
        cur = 0
        t = kit.first_token
        first_pass3038 = True
        while True:
            if first_pass3038: first_pass3038 = False
            else: t = t.next0_; cur += 1
            if (not (t is not None)): break
            kw = Utils.asObjectOrNull(t.getReferent(), KeywordReferent)
            if (kw is None or kw.typ != KeywordType.OBJECT): 
                continue
            if (t.next0_ is None or kw.child_words > 2): 
                continue
            t1 = t.next0_
            if (t1.isValue("OF", None) and (t1.whitespaces_after_count < 3) and t1.next0_ is not None): 
                t1 = t1.next0_
                if ((isinstance(t1, TextToken)) and MiscHelper.isEngArticle(t1) and t1.next0_ is not None): 
                    t1 = t1.next0_
            elif (not t1.morph.case_.is_genitive or t.whitespaces_after_count > 1): 
                continue
            kw2 = Utils.asObjectOrNull(t1.getReferent(), KeywordReferent)
            if (kw2 is None): 
                continue
            if (kw2.typ != KeywordType.OBJECT or (kw.child_words + kw2.child_words) > 3): 
                continue
            kw_un = KeywordReferent()
            kw_un._union(kw, kw2, MiscHelper.getTextValue(t1, t1, GetTextAttr.NO))
            kw_un = (Utils.asObjectOrNull(ad.registerReferent(kw_un), KeywordReferent))
            KeywordAnalyzer.__setRank(kw_un, cur, max0_)
            rt1 = ReferentToken._new746(kw_un, t, t1, t.morph)
            kit.embedToken(rt1)
            t = (rt1)
        if (KeywordAnalyzer.SORT_KEYWORDS_BY_RANK): 
            all0_ = list(ad.referents)
            all0_.sort(key=operator.attrgetter('rank'), reverse=True)
            ad.referents = all0_
    
    @staticmethod
    def __calcRank(gr : 'DerivateGroup') -> int:
        if (gr.is_dummy): 
            return 0
        res = 0
        for w in gr.words: 
            if (w.lang.is_ru and w.class0_ is not None): 
                if (w.class0_.is_verb and w.class0_.is_adjective): 
                    pass
                else: 
                    res += 1
        if (gr.prefix is None): 
            res += 3
        return res
    
    @staticmethod
    def __addNormals(kref : 'KeywordReferent', grs : typing.List['DerivateGroup'], norm : str) -> None:
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        if (grs is None or len(grs) == 0): 
            return
        k = 0
        while k < len(grs): 
            ch = False
            i = 0
            while i < (len(grs) - 1): 
                if (KeywordAnalyzer.__calcRank(grs[i]) < KeywordAnalyzer.__calcRank(grs[i + 1])): 
                    gr = grs[i]
                    grs[i] = grs[i + 1]
                    grs[i + 1] = gr
                    ch = True
                i += 1
            if (not ch): 
                break
            k += 1
        i = 0
        while (i < 3) and (i < len(grs)): 
            if (not grs[i].is_dummy and len(grs[i].words) > 0): 
                if (grs[i].words[0].spelling != norm): 
                    kref.addSlot(KeywordReferent.ATTR_NORMAL, grs[i].words[0].spelling, False, 0)
            i += 1
    
    def __addReferents(self, ad : 'AnalyzerData', t : 'Token', cur : int, max0_ : int) -> 'Token':
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.morph.MorphLang import MorphLang
        if (not ((isinstance(t, ReferentToken)))): 
            return t
        r = t.getReferent()
        if (r is None): 
            return t
        if (isinstance(r, DenominationReferent)): 
            dr = Utils.asObjectOrNull(r, DenominationReferent)
            kref0 = KeywordReferent._new1502(KeywordType.REFERENT)
            for s in dr.slots: 
                if (s.type_name == DenominationReferent.ATTR_VALUE): 
                    kref0.addSlot(KeywordReferent.ATTR_NORMAL, s.value, False, 0)
            kref0.addSlot(KeywordReferent.ATTR_REF, dr, False, 0)
            rt0 = ReferentToken(ad.registerReferent(kref0), t, t)
            t.kit.embedToken(rt0)
            return rt0
        if ((isinstance(r, PhoneReferent)) or (isinstance(r, UriReferent)) or (isinstance(r, BankDataReferent))): 
            return t
        if (isinstance(r, MoneyReferent)): 
            mr = Utils.asObjectOrNull(r, MoneyReferent)
            kref0 = KeywordReferent._new1502(KeywordType.OBJECT)
            kref0.addSlot(KeywordReferent.ATTR_NORMAL, mr.currency, False, 0)
            rt0 = ReferentToken(ad.registerReferent(kref0), t, t)
            t.kit.embedToken(rt0)
            return rt0
        if (r.type_name == "DATE" or r.type_name == "DATERANGE" or r.type_name == "BOOKLINKREF"): 
            return t
        tt = (Utils.asObjectOrNull(t, MetaToken)).begin_token
        while tt is not None and tt.end_char <= t.end_char: 
            if (isinstance(tt, ReferentToken)): 
                self.__addReferents(ad, tt, cur, max0_)
            tt = tt.next0_
        kref = KeywordReferent._new1502(KeywordType.REFERENT)
        norm = None
        if (r.type_name == "GEO"): 
            norm = r.getStringValue("ALPHA2")
        if (norm is None): 
            norm = r.toString(True, MorphLang(), 0)
        if (norm is not None): 
            kref.addSlot(KeywordReferent.ATTR_NORMAL, norm.upper(), False, 0)
        kref.addSlot(KeywordReferent.ATTR_REF, t.getReferent(), False, 0)
        KeywordAnalyzer.__setRank(kref, cur, max0_)
        rt1 = ReferentToken(ad.registerReferent(kref), t, t)
        t.kit.embedToken(rt1)
        return rt1
    
    @staticmethod
    def __setRank(kr : 'KeywordReferent', cur : int, max0_ : int) -> None:
        from pullenti.ner.Referent import Referent
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        rank = 1
        ty = kr.typ
        if (ty == KeywordType.PREDICATE): 
            rank = (1)
        elif (ty == KeywordType.OBJECT): 
            v = Utils.ifNotNull(kr.getStringValue(KeywordReferent.ATTR_VALUE), kr.getStringValue(KeywordReferent.ATTR_NORMAL))
            if (v is not None): 
                i = 0
                while i < len(v): 
                    if (v[i] == ' ' or v[i] == '-'): 
                        rank += 1
                    i += 1
        elif (ty == KeywordType.REFERENT): 
            rank = (3)
            r = Utils.asObjectOrNull(kr.getSlotValue(KeywordReferent.ATTR_REF), Referent)
            if (r is not None): 
                if (r.type_name == "PERSON"): 
                    rank = (4)
        if (max0_ > 0): 
            rank *= (((1) - (((.5 * (cur)) / (max0_)))))
        kr.rank += rank
    
    SORT_KEYWORDS_BY_RANK = True
    
    M_INITIALIZED = False
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
        from pullenti.ner.ProcessorService import ProcessorService
        if (KeywordAnalyzer.M_INITIALIZED): 
            return
        KeywordAnalyzer.M_INITIALIZED = True
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        DenominationAnalyzer.initialize()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.registerAnalyzer(KeywordAnalyzer())