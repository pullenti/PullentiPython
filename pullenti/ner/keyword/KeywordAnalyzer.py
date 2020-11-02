# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import operator
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.keyword.internal.AutoannoSentToken import AutoannoSentToken
from pullenti.ner.money.MoneyReferent import MoneyReferent
from pullenti.ner.denomination.DenominationReferent import DenominationReferent
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.core.Termin import Termin
from pullenti.ner.phone.PhoneReferent import PhoneReferent
from pullenti.ner.bank.BankDataReferent import BankDataReferent
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.ner.keyword.internal.KeywordMeta import KeywordMeta
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.keyword.KeywordReferent import KeywordReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.keyword.KeywordType import KeywordType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class KeywordAnalyzer(Analyzer):
    """ Анализатор ключевых комбинаций.
    Специфический анализатор, то есть нужно явно создавать процессор через функцию CreateSpecificProcessor,
    указав имя анализатора. """
    
    class CompByRank(object):
        
        def compare(self, x : 'Referent', y : 'Referent') -> int:
            from pullenti.ner.keyword.KeywordReferent import KeywordReferent
            d1 = x.rank
            d2 = y.rank
            if (d1 > d2): 
                return -1
            if (d1 < d2): 
                return 1
            return 0
    
    ANALYZER_NAME = "KEYWORD"
    """ Имя анализатора ("KEYWORD") """
    
    @property
    def name(self) -> str:
        return KeywordAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Ключевые комбинации"
    
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
        """ Этот анализатор является специфическим (IsSpecific = true) """
        return True
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AnalyzerDataWithOntology()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [KeywordMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[KeywordMeta.IMAGE_OBJ] = PullentiNerCoreInternalResourceHelper.get_bytes("kwobject.png")
        res[KeywordMeta.IMAGE_PRED] = PullentiNerCoreInternalResourceHelper.get_bytes("kwpredicate.png")
        res[KeywordMeta.IMAGE_REF] = PullentiNerCoreInternalResourceHelper.get_bytes("kwreferent.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == KeywordReferent.OBJ_TYPENAME): 
            return KeywordReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        # Основная функция выделения телефонов
        ad = kit.get_analyzer_data(self)
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
        first_pass3784 = True
        while True:
            if first_pass3784: first_pass3784 = False
            else: t = t.next0_; cur += 1
            if (not (t is not None)): break
            r = t.get_referent()
            if (r is not None): 
                t = self.__add_referents(ad, t, cur, max0_)
                continue
            if (not (isinstance(t, TextToken))): 
                continue
            if (not t.chars.is_letter or (t.length_char < 3)): 
                continue
            term = t.term
            if (term == "ЕСТЬ"): 
                if ((isinstance(t.previous, TextToken)) and t.previous.morph.class0_.is_verb): 
                    pass
                else: 
                    continue
            npt = None
            npt = NounPhraseHelper.try_parse(t, Utils.valToEnum((NounPhraseParseAttr.ADJECTIVECANBELAST) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0, None)
            if (npt is None): 
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_verb and not mc.is_preposition): 
                    if (t.is_verb_be): 
                        continue
                    if (t.is_value("МОЧЬ", None) or t.is_value("WOULD", None)): 
                        continue
                    kref = KeywordReferent._new1591(KeywordType.PREDICATE)
                    norm = t.get_normal_case_text(MorphClass.VERB, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                    if (norm is None): 
                        norm = t.lemma
                    if (norm.endswith("ЬСЯ")): 
                        norm = norm[0:0+len(norm) - 2]
                    kref.add_slot(KeywordReferent.ATTR_VALUE, norm, False, 0)
                    drv = DerivateService.find_derivates(norm, True, t.morph.language)
                    KeywordAnalyzer.__add_normals(kref, drv, norm)
                    kref = (Utils.asObjectOrNull(ad.register_referent(kref), KeywordReferent))
                    KeywordAnalyzer.__set_rank(kref, cur, max0_)
                    rt1 = ReferentToken._new734(ad.register_referent(kref), t, t, t.morph)
                    kit.embed_token(rt1)
                    t = (rt1)
                    continue
                continue
            if (npt.internal_noun is not None): 
                continue
            if (npt.end_token.is_value("ЦЕЛОМ", None) or npt.end_token.is_value("ЧАСТНОСТИ", None)): 
                if (npt.preposition is not None): 
                    t = npt.end_token
                    continue
            if (npt.end_token.is_value("СТОРОНЫ", None) and npt.preposition is not None and npt.preposition.normal == "С"): 
                t = npt.end_token
                continue
            if (npt.begin_token == npt.end_token): 
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_preposition): 
                    continue
                elif (mc.is_adverb): 
                    if (t.is_value("ПОТОМ", None)): 
                        continue
            else: 
                pass
            li.clear()
            t0 = t
            tt = t
            first_pass3785 = True
            while True:
                if first_pass3785: first_pass3785 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= npt.end_char)): break
                if (not (isinstance(tt, TextToken))): 
                    continue
                if (tt.is_value("NATURAL", None)): 
                    pass
                if ((tt.length_char < 3) or not tt.chars.is_letter): 
                    continue
                mc = tt.get_morph_class_in_dictionary()
                if ((mc.is_preposition or mc.is_pronoun or mc.is_personal_pronoun) or mc.is_conjunction): 
                    if (tt.is_value("ОТНОШЕНИЕ", None)): 
                        pass
                    else: 
                        continue
                if (mc.is_misc): 
                    if (MiscHelper.is_eng_article(tt)): 
                        continue
                kref = KeywordReferent._new1591(KeywordType.OBJECT)
                norm = tt.lemma
                kref.add_slot(KeywordReferent.ATTR_VALUE, norm, False, 0)
                if (norm != "ЕСТЬ"): 
                    drv = DerivateService.find_derivates(norm, True, tt.morph.language)
                    KeywordAnalyzer.__add_normals(kref, drv, norm)
                kref = (Utils.asObjectOrNull(ad.register_referent(kref), KeywordReferent))
                KeywordAnalyzer.__set_rank(kref, cur, max0_)
                rt1 = ReferentToken._new734(kref, tt, tt, tt.morph)
                kit.embed_token(rt1)
                if (tt == t and len(li) == 0): 
                    t0 = (rt1)
                t = (rt1)
                li.append(kref)
            if (len(li) > 1): 
                kref = KeywordReferent._new1591(KeywordType.OBJECT)
                Utils.setLengthStringIO(tmp, 0)
                tmp2.clear()
                has_norm = False
                for kw in li: 
                    s = kw.get_string_value(KeywordReferent.ATTR_VALUE)
                    if (tmp.tell() > 0): 
                        print(' ', end="", file=tmp)
                    print(s, end="", file=tmp)
                    n = kw.get_string_value(KeywordReferent.ATTR_NORMAL)
                    if (n is not None): 
                        has_norm = True
                        tmp2.append(n)
                    else: 
                        tmp2.append(s)
                    kref.add_slot(KeywordReferent.ATTR_REF, kw, False, 0)
                val = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                kref.add_slot(KeywordReferent.ATTR_VALUE, val, False, 0)
                Utils.setLengthStringIO(tmp, 0)
                tmp2.sort()
                for s in tmp2: 
                    if (tmp.tell() > 0): 
                        print(' ', end="", file=tmp)
                    print(s, end="", file=tmp)
                norm = Utils.toStringStringIO(tmp)
                if (norm != val): 
                    kref.add_slot(KeywordReferent.ATTR_NORMAL, norm, False, 0)
                kref = (Utils.asObjectOrNull(ad.register_referent(kref), KeywordReferent))
                KeywordAnalyzer.__set_rank(kref, cur, max0_)
                rt1 = ReferentToken._new734(kref, t0, t, npt.morph)
                kit.embed_token(rt1)
                t = (rt1)
        cur = 0
        t = kit.first_token
        first_pass3786 = True
        while True:
            if first_pass3786: first_pass3786 = False
            else: t = t.next0_; cur += 1
            if (not (t is not None)): break
            kw = Utils.asObjectOrNull(t.get_referent(), KeywordReferent)
            if (kw is None or kw.typ != KeywordType.OBJECT): 
                continue
            if (t.next0_ is None or kw.child_words > 2): 
                continue
            t1 = t.next0_
            if (t1.is_value("OF", None) and (t1.whitespaces_after_count < 3) and t1.next0_ is not None): 
                t1 = t1.next0_
                if ((isinstance(t1, TextToken)) and MiscHelper.is_eng_article(t1) and t1.next0_ is not None): 
                    t1 = t1.next0_
            elif (not t1.morph.case_.is_genitive or t.whitespaces_after_count > 1): 
                continue
            kw2 = Utils.asObjectOrNull(t1.get_referent(), KeywordReferent)
            if (kw2 is None): 
                continue
            if (kw == kw2): 
                continue
            if (kw2.typ != KeywordType.OBJECT or (kw.child_words + kw2.child_words) > 3): 
                continue
            kw_un = KeywordReferent()
            kw_un._union(kw, kw2, MiscHelper.get_text_value(t1, t1, GetTextAttr.NO))
            kw_un = (Utils.asObjectOrNull(ad.register_referent(kw_un), KeywordReferent))
            KeywordAnalyzer.__set_rank(kw_un, cur, max0_)
            rt1 = ReferentToken._new734(kw_un, t, t1, t.morph)
            kit.embed_token(rt1)
            t = (rt1)
        if (KeywordAnalyzer.SORT_KEYWORDS_BY_RANK): 
            all0_ = list(ad.referents)
            all0_.sort(key=operator.attrgetter('rank'), reverse=True)
            ad.referents = all0_
        if (KeywordAnalyzer.ANNOTATION_MAX_SENTENCES > 0): 
            ano = AutoannoSentToken.create_annotation(kit, KeywordAnalyzer.ANNOTATION_MAX_SENTENCES)
            if (ano is not None): 
                ad.register_referent(ano)
    
    @staticmethod
    def __calc_rank(gr : 'DerivateGroup') -> int:
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
    def __add_normals(kref : 'KeywordReferent', grs : typing.List['DerivateGroup'], norm : str) -> None:
        if (grs is None or len(grs) == 0): 
            return
        k = 0
        while k < len(grs): 
            ch = False
            i = 0
            while i < (len(grs) - 1): 
                if (KeywordAnalyzer.__calc_rank(grs[i]) < KeywordAnalyzer.__calc_rank(grs[i + 1])): 
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
                    kref.add_slot(KeywordReferent.ATTR_NORMAL, grs[i].words[0].spelling, False, 0)
            i += 1
    
    def __add_referents(self, ad : 'AnalyzerData', t : 'Token', cur : int, max0_ : int) -> 'Token':
        if (not (isinstance(t, ReferentToken))): 
            return t
        r = t.get_referent()
        if (r is None): 
            return t
        if (isinstance(r, DenominationReferent)): 
            dr = Utils.asObjectOrNull(r, DenominationReferent)
            kref0 = KeywordReferent._new1591(KeywordType.REFERENT)
            for s in dr.slots: 
                if (s.type_name == DenominationReferent.ATTR_VALUE): 
                    kref0.add_slot(KeywordReferent.ATTR_NORMAL, s.value, False, 0)
            kref0.add_slot(KeywordReferent.ATTR_REF, dr, False, 0)
            rt0 = ReferentToken(ad.register_referent(kref0), t, t)
            t.kit.embed_token(rt0)
            return rt0
        if ((isinstance(r, PhoneReferent)) or (isinstance(r, UriReferent)) or (isinstance(r, BankDataReferent))): 
            return t
        if (isinstance(r, MoneyReferent)): 
            mr = Utils.asObjectOrNull(r, MoneyReferent)
            kref0 = KeywordReferent._new1591(KeywordType.OBJECT)
            kref0.add_slot(KeywordReferent.ATTR_NORMAL, mr.currency, False, 0)
            rt0 = ReferentToken(ad.register_referent(kref0), t, t)
            t.kit.embed_token(rt0)
            return rt0
        if (r.type_name == "DATE" or r.type_name == "DATERANGE" or r.type_name == "BOOKLINKREF"): 
            return t
        tt = t.begin_token
        while tt is not None and tt.end_char <= t.end_char: 
            if (isinstance(tt, ReferentToken)): 
                self.__add_referents(ad, tt, cur, max0_)
            tt = tt.next0_
        kref = KeywordReferent._new1591(KeywordType.REFERENT)
        norm = None
        if (r.type_name == "GEO"): 
            norm = r.get_string_value("ALPHA2")
        if (norm is None): 
            norm = r.to_string(True, None, 0)
        if (norm is not None): 
            kref.add_slot(KeywordReferent.ATTR_NORMAL, norm.upper(), False, 0)
        kref.add_slot(KeywordReferent.ATTR_REF, t.get_referent(), False, 0)
        KeywordAnalyzer.__set_rank(kref, cur, max0_)
        rt1 = ReferentToken(ad.register_referent(kref), t, t)
        t.kit.embed_token(rt1)
        return rt1
    
    @staticmethod
    def __set_rank(kr : 'KeywordReferent', cur : int, max0_ : int) -> None:
        rank = 1
        ty = kr.typ
        if (ty == KeywordType.PREDICATE): 
            rank = (1)
        elif (ty == KeywordType.OBJECT): 
            v = Utils.ifNotNull(kr.get_string_value(KeywordReferent.ATTR_VALUE), kr.get_string_value(KeywordReferent.ATTR_NORMAL))
            if (v is not None): 
                i = 0
                while i < len(v): 
                    if (v[i] == ' ' or v[i] == '-'): 
                        rank += 1
                    i += 1
        elif (ty == KeywordType.REFERENT): 
            rank = (3)
            r = Utils.asObjectOrNull(kr.get_slot_value(KeywordReferent.ATTR_REF), Referent)
            if (r is not None): 
                if (r.type_name == "PERSON"): 
                    rank = (4)
        if (max0_ > 0): 
            rank *= (((1) - (((0.5 * (cur)) / (max0_)))))
        kr.rank += rank
    
    SORT_KEYWORDS_BY_RANK = True
    """ Сортировать ли в списке Entities ключевые слова в порядке убывания ранга """
    
    ANNOTATION_MAX_SENTENCES = 3
    """ Максимально предложений в автоаннотацию (KeywordReferent с типом Annotation).
    Если 0, то не делать автоаннотацию. По умолчанию = 3. """
    
    M_INITIALIZED = False
    
    @staticmethod
    def initialize() -> None:
        if (KeywordAnalyzer.M_INITIALIZED): 
            return
        KeywordAnalyzer.M_INITIALIZED = True
        try: 
            KeywordMeta.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            DenominationAnalyzer.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            ProcessorService.register_analyzer(KeywordAnalyzer())
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)