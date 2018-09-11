# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import datetime
import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Misc import EventHandler
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.StatisticCollection import StatisticCollection
from pullenti.ner.internal.GeneralRelationHelper import GeneralRelationHelper
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper


class AnalysisKit:
    """ Внутренний аналитический контейнер данных """
    
    def __init__(self, sofa_ : 'SourceOfAnalysis'=None, only_tokenizing : bool=False, lang : 'MorphLang'=MorphLang(), progress : EventHandler=None) -> None:
        from pullenti.morph.Morphology import Morphology
        from pullenti.ner.TextToken import TextToken
        self._start_date = datetime.datetime(1, 1, 1, 0, 0, 0)
        self.corrected_tokens = None
        self.first_token = None
        self.__m_entities = list()
        self.ontology = None
        self.base_language = MorphLang()
        self.__m_sofa = None
        self.statistics = None
        self.__m_datas = dict()
        self.misc_data = dict()
        self.processor = None
        self.recurse_level = 0
        self._m_analyzer_stack = list()
        if (sofa_ is None): 
            return
        self.__m_sofa = sofa_
        self._start_date = datetime.datetime.now()
        tokens = Morphology.process(sofa_.text, lang, None)
        t0 = None
        if (tokens is not None): 
            ii = 0
            while ii < len(tokens): 
                mt = tokens[ii]
                if (mt.begin_char == 733860): 
                    pass
                tt = TextToken(mt, self)
                if (sofa_.correction_dict is not None): 
                    inoutarg494 = RefOutArgWrapper(None)
                    inoutres495 = Utils.tryGetValue(sofa_.correction_dict, mt.term, inoutarg494)
                    corw = inoutarg494.value
                    if (inoutres495): 
                        ccc = Morphology.process(corw, lang, None)
                        if (ccc is not None and len(ccc) == 1): 
                            tt1 = TextToken._new493(ccc[0], self, tt.term)
                            tt1.begin_char = tt.begin_char
                            tt1.end_char = tt.end_char
                            tt1.chars = tt.chars
                            tt = tt1
                            if (self.corrected_tokens is None): 
                                self.corrected_tokens = dict()
                            self.corrected_tokens[tt] = tt.get_source_text()
                if (t0 is None): 
                    self.first_token = (tt)
                else: 
                    t0.next0_ = tt
                t0 = (tt)
                ii += 1
        if (sofa_.clear_dust): 
            self.__clear_dust()
        if (sofa_.do_words_merging_by_morph): 
            self.__correct_words_by_merging(lang)
        if (sofa_.do_word_correction_by_morph): 
            self.__correct_words_by_morph(lang)
        self.__merge_letters()
        self.__define_base_language()
        t = self.first_token
        first_pass3699 = True
        while True:
            if first_pass3699: first_pass3699 = False
            else: t = t.next0_
            if (not (t is not None)): break
            nt = NumberHelper._try_parse(t)
            if (nt is None): 
                continue
            self.embed_token(nt)
            t = (nt)
        if (only_tokenizing): 
            return
        t = self.first_token
        first_pass3700 = True
        while True:
            if first_pass3700: first_pass3700 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.morph.class0_.is_preposition): 
                continue
            mc = t.get_morph_class_in_dictionary()
            if (mc.is_undefined and t.chars.is_cyrillic_letter and t.length_char > 4): 
                tail = sofa_.text[t.end_char - 1:t.end_char - 1+2]
                tte = None
                tt = t.previous
                if (tt is not None and ((tt.is_comma_and or tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction))): 
                    tt = tt.previous
                if ((tt is not None and not tt.get_morph_class_in_dictionary().is_undefined and (((tt.morph.class0_.value) & (t.morph.class0_.value))) != 0) and tt.length_char > 4): 
                    tail2 = sofa_.text[tt.end_char - 1:tt.end_char - 1+2]
                    if (tail2 == tail): 
                        tte = tt
                if (tte is None): 
                    tt = t.next0_
                    if (tt is not None and ((tt.is_comma_and or tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction))): 
                        tt = tt.next0_
                    if ((tt is not None and not tt.get_morph_class_in_dictionary().is_undefined and (((tt.morph.class0_.value) & (t.morph.class0_.value))) != 0) and tt.length_char > 4): 
                        tail2 = sofa_.text[tt.end_char - 1:tt.end_char - 1+2]
                        if (tail2 == tail): 
                            tte = tt
                if (tte is not None): 
                    t.morph.remove_items_ex(tte.morph, tte.get_morph_class_in_dictionary())
            continue
        self.__create_statistics()
    
    def _init_from(self, ar : 'AnalysisResult') -> None:
        self.__m_sofa = ar.sofas[0]
        self.first_token = ar.first_token
        self.base_language = ar.base_language
        self.__create_statistics()
    
    def __clear_dust(self) -> None:
        t = self.first_token
        first_pass3701 = True
        while True:
            if first_pass3701: first_pass3701 = False
            else: t = t.next0_
            if (not (t is not None)): break
            cou = AnalysisKit.__calc_abnormal_coef(t)
            norm = 0
            if (cou < 1): 
                continue
            t1 = t
            tt = t
            first_pass3702 = True
            while True:
                if first_pass3702: first_pass3702 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                co = AnalysisKit.__calc_abnormal_coef(tt)
                if (co == 0): 
                    continue
                if (co < 0): 
                    norm += 1
                    if (norm > 1): 
                        break
                else: 
                    norm = 0
                    cou += co
                    t1 = tt
            len0_ = t1.end_char - t.begin_char
            if (cou > 20 and len0_ > 500): 
                p = t.begin_char
                while p < t1.end_char: 
                    if (self.sofa.text[p] == self.sofa.text[p + 1]): 
                        len0_ -= 1
                    p += 1
                if (len0_ > 500): 
                    if (t.previous is not None): 
                        t.previous.next0_ = t1.next0_
                    else: 
                        self.first_token = t1.next0_
                    t = t1
                else: 
                    t = t1
            else: 
                t = t1
    
    @staticmethod
    def __calc_abnormal_coef(t : 'Token') -> int:
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphWordForm import MorphWordForm
        if (isinstance(t, NumberToken)): 
            return 0
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return 0
        if (not tt.chars.is_letter): 
            return 0
        if (not tt.chars.is_latin_letter and not tt.chars.is_cyrillic_letter): 
            return 2
        if (tt.length_char < 4): 
            return 0
        for wf in tt.morph.items: 
            if ((wf if isinstance(wf, MorphWordForm) else None).is_in_dictionary): 
                return -1
        if (tt.length_char > 15): 
            return 2
        return 1
    
    def __correct_words_by_merging(self, lang : 'MorphLang') -> None:
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.Morphology import Morphology
        t = self.first_token
        first_pass3703 = True
        while True:
            if first_pass3703: first_pass3703 = False
            else: t = t.next0_
            if (not (t is not None and t.next0_ is not None)): break
            if (not t.chars.is_letter or (t.length_char < 2)): 
                continue
            mc0 = t.get_morph_class_in_dictionary()
            if (t.morph.contains_attr("прдктв.", MorphClass())): 
                continue
            t1 = t.next0_
            if (t1.is_hiphen and t1.next0_ is not None and not t1.is_newline_after): 
                t1 = t1.next0_
            if (t1.length_char == 1): 
                continue
            if (not t1.chars.is_letter or not t.chars.is_letter or t1.chars.is_latin_letter != t.chars.is_latin_letter): 
                continue
            if (t1.chars.is_all_upper and not t.chars.is_all_upper): 
                continue
            elif (not t1.chars.is_all_lower): 
                continue
            elif (t.chars.is_all_upper): 
                continue
            if (t1.morph.contains_attr("прдктв.", MorphClass())): 
                continue
            mc1 = t1.get_morph_class_in_dictionary()
            if (not mc1.is_undefined and not mc0.is_undefined): 
                continue
            if ((len((t if isinstance(t, TextToken) else None).term) + len((t1 if isinstance(t1, TextToken) else None).term)) < 6): 
                continue
            corw = (t if isinstance(t, TextToken) else None).term + (t1 if isinstance(t1, TextToken) else None).term
            ccc = Morphology.process(corw, lang, None)
            if (ccc is None or len(ccc) != 1): 
                continue
            if (corw == "ПОСТ" or corw == "ВРЕД"): 
                continue
            tt = TextToken(ccc[0], self)
            if (tt.get_morph_class_in_dictionary().is_undefined): 
                continue
            tt.begin_char = t.begin_char
            tt.end_char = t1.end_char
            tt.chars = t.chars
            if (t == self.first_token): 
                self.first_token = (tt)
            else: 
                t.previous.next0_ = tt
            if (t1.next0_ is not None): 
                tt.next0_ = t1.next0_
            t = (tt)
    
    def __correct_words_by_morph(self, lang : 'MorphLang') -> None:
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.Morphology import Morphology
        tt = self.first_token
        first_pass3704 = True
        while True:
            if first_pass3704: first_pass3704 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (not ((isinstance(tt, TextToken)))): 
                continue
            if (tt.morph.contains_attr("прдктв.", MorphClass())): 
                continue
            dd = tt.get_morph_class_in_dictionary()
            if (not dd.is_undefined or (tt.length_char < 4)): 
                continue
            if (tt.morph.class0_.is_proper_surname and not tt.chars.is_all_lower): 
                continue
            if (tt.chars.is_all_upper): 
                continue
            corw = Morphology.correct_word((tt if isinstance(tt, TextToken) else None).term, (lang if tt.morph.language.is_undefined else tt.morph.language))
            if (corw is None): 
                continue
            ccc = Morphology.process(corw, lang, None)
            if (ccc is None or len(ccc) != 1): 
                continue
            tt1 = TextToken._new496(ccc[0], self, tt.chars, tt.begin_char, tt.end_char, (tt if isinstance(tt, TextToken) else None).term)
            mc = tt1.get_morph_class_in_dictionary()
            if (mc.is_proper_surname): 
                continue
            if (tt == self.first_token): 
                self.first_token = (tt1)
            else: 
                tt.previous.next0_ = tt1
            tt1.next0_ = tt.next0_
            tt = (tt1)
            if (self.corrected_tokens is None): 
                self.corrected_tokens = dict()
            self.corrected_tokens[tt] = tt.get_source_text()
    
    def __merge_letters(self) -> None:
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.Morphology import Morphology
        before_word = False
        tmp = io.StringIO()
        t = self.first_token
        first_pass3705 = True
        while True:
            if first_pass3705: first_pass3705 = False
            else: t = t.next0_
            if (not (t is not None)): break
            tt = (t if isinstance(t, TextToken) else None)
            if (not tt.chars.is_letter or tt.length_char != 1): 
                before_word = False
                continue
            i = t.whitespaces_before_count
            if (i > 2 or ((i == 2 and before_word))): 
                pass
            else: 
                before_word = False
                continue
            i = 0
            Utils.setLengthStringIO(tmp, 0)
            print(tt.get_source_text(), end="", file=tmp)
            t1 = t
            while t1.next0_ is not None: 
                tt = (t1.next0_ if isinstance(t1.next0_, TextToken) else None)
                if (tt.length_char != 1 or tt.whitespaces_before_count != 1): 
                    break
                i += 1
                print(tt.get_source_text(), end="", file=tmp)
                t1 = t1.next0_
            if (i > 3 or ((i > 1 and before_word))): 
                pass
            else: 
                before_word = False
                continue
            before_word = False
            mt = Morphology.process(Utils.toStringStringIO(tmp), None, None)
            if (mt is None or len(mt) != 1): 
                t = t1
                continue
            for wf in mt[0].word_forms: 
                if (wf.is_in_dictionary): 
                    before_word = True
                    break
            if (not before_word): 
                t = t1
                continue
            tt = TextToken(mt[0], self)
            if (t == self.first_token): 
                self.first_token = (tt)
            else: 
                tt.previous = t.previous
            tt.next0_ = t1.next0_
            tt.begin_char = t.begin_char
            tt.end_char = t1.end_char
            t = (tt)
    
    def embed_token(self, mt : 'MetaToken') -> None:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextAnnotation import TextAnnotation
        if (mt is None): 
            return
        if (mt.begin_char > mt.end_char): 
            bg = mt.begin_token
            mt.begin_token = mt.end_token
            mt.end_token = bg
        if (mt.begin_char > mt.end_char): 
            return
        if (mt.begin_token == self.first_token): 
            self.first_token = (mt)
        else: 
            tp = mt.begin_token.previous
            mt.previous = tp
        tn = mt.end_token.next0_
        mt.next0_ = tn
        if (isinstance(mt, ReferentToken)): 
            if ((mt if isinstance(mt, ReferentToken) else None).referent is not None): 
                (mt if isinstance(mt, ReferentToken) else None).referent.add_occurence(TextAnnotation._new497(self.sofa, mt.begin_char, mt.end_char))
    
    def debed_token(self, t : 'Token') -> 'Token':
        from pullenti.ner.MetaToken import MetaToken
        r = t.get_referent()
        if (r is not None): 
            for o in r.occurrence: 
                if (o.begin_char == t.begin_char and o.end_char == t.end_char): 
                    r.occurrence.remove(o)
                    break
        mt = (t if isinstance(t, MetaToken) else None)
        if (mt is None): 
            return t
        if (t.next0_ is not None): 
            t.next0_.previous = mt.end_token
        if (t.previous is not None): 
            t.previous.next0_ = mt.begin_token
        if (mt == self.first_token): 
            self.first_token = mt.begin_token
        if (r is not None and len(r.occurrence) == 0): 
            for d in self.__m_datas.values(): 
                if (r in d.referents): 
                    d.remove_referent(r)
                    break
        return mt.begin_token
    
    @property
    def entities(self) -> typing.List['Referent']:
        """ Список сущностей, выделенных в ходе анализа """
        return self.__m_entities
    
    @property
    def sofa(self) -> 'SourceOfAnalysis':
        """ Ссылка на исходный текст """
        if (self.__m_sofa is None): 
            self.__m_sofa = SourceOfAnalysis("")
        return self.__m_sofa
    
    def get_text_character(self, position : int) -> 'char':
        if ((position < 0) or position >= len(self.__m_sofa.text)): 
            return chr(0)
        return self.__m_sofa.text[position]
    
    def get_analyzer_data_by_analyzer_name(self, analyzer_name : str) -> 'AnalyzerData':
        a = self.processor.find_analyzer(analyzer_name)
        if (a is None): 
            return None
        return self.get_analyzer_data(a)
    
    def get_analyzer_data(self, analyzer : 'Analyzer') -> 'AnalyzerData':
        if (analyzer is None or analyzer.name is None): 
            return None
        inoutarg498 = RefOutArgWrapper(None)
        inoutres499 = Utils.tryGetValue(self.__m_datas, analyzer.name, inoutarg498)
        d = inoutarg498.value
        if (inoutres499): 
            d.kit = self
            return d
        default_data = analyzer.create_analyzer_data()
        if (default_data is None): 
            return None
        if (analyzer._persist_referents_regim): 
            if (analyzer._persist_analizer_data is None): 
                analyzer._persist_analizer_data = default_data
            else: 
                default_data = analyzer._persist_analizer_data
        self.__m_datas[analyzer.name] = default_data
        default_data.kit = self
        return default_data
    
    def __create_statistics(self) -> None:
        self.statistics = StatisticCollection()
        self.statistics.prepare(self.first_token)
    
    def __define_base_language(self) -> None:
        from pullenti.ner.TextToken import TextToken
        stat = dict()
        total = 0
        t = self.first_token
        first_pass3706 = True
        while True:
            if first_pass3706: first_pass3706 = False
            else: t = t.next0_
            if (not (t is not None)): break
            tt = (t if isinstance(t, TextToken) else None)
            if (tt is None): 
                continue
            if (tt.morph.language.is_undefined): 
                continue
            if (not tt.morph.language in stat): 
                stat[tt.morph.language] = 1
            else: 
                stat[tt.morph.language] += 1
            total += 1
        for kp in stat.items(): 
            if (kp[1] > (math.floor(total / 2))): 
                self.base_language |= kp[0]
    
    def replace_referent(self, old_referent : 'Referent', new_referent : 'Referent') -> None:
        from pullenti.ner.ReferentToken import ReferentToken
        t = self.first_token
        while t is not None: 
            if (isinstance(t, ReferentToken)): 
                (t if isinstance(t, ReferentToken) else None)._replace_referent(old_referent, new_referent)
            t = t.next0_
        for d in self.__m_datas.values(): 
            for r in d.referents: 
                for s in r.slots: 
                    if (s.value == old_referent): 
                        r.upload_slot(s, new_referent)
            if (old_referent in d.referents): 
                d.referents.remove(old_referent)
    
    def process_referent(self, analyzer_name : str, t : 'Token') -> 'ReferentToken':
        if (self.processor is None): 
            return None
        if (analyzer_name in self._m_analyzer_stack): 
            return None
        if (self.is_recurce_overflow): 
            return None
        a = self.processor.find_analyzer(analyzer_name)
        if (a is None): 
            return None
        self.recurse_level += 1
        self._m_analyzer_stack.append(analyzer_name)
        res = a._process_referent(t, None)
        self._m_analyzer_stack.remove(analyzer_name)
        self.recurse_level -= 1
        return res
    
    def create_referent(self, type_name : str) -> 'Referent':
        if (self.processor is None): 
            return None
        else: 
            for a in self.processor.analyzers: 
                res = a.create_referent(type_name)
                if (res is not None): 
                    return res
        return None
    
    def refresh_generals(self) -> None:
        GeneralRelationHelper.refresh_generals(self.processor, self)
    
    @property
    def is_recurce_overflow(self) -> bool:
        return self.recurse_level > 5
    
    def serialize(self, stream : io.IOBase) -> None:
        self.__m_sofa.serialize(stream)
        SerializerHelper.serialize_int(stream, self.base_language.value)
        if (len(self.__m_entities) == 0): 
            for d in self.__m_datas.items(): 
                self.__m_entities.extend(d[1].referents)
        SerializerHelper.serialize_int(stream, len(self.__m_entities))
        i = 0
        while i < len(self.__m_entities): 
            self.__m_entities[i].tag = (i + 1)
            SerializerHelper.serialize_string(stream, self.__m_entities[i].type_name)
            i += 1
        for e0_ in self.__m_entities: 
            e0_.serialize(stream)
        SerializerHelper.serialize_tokens(stream, self.first_token, 0)
    
    def deserialize(self, stream : io.IOBase) -> None:
        from pullenti.ner.ProcessorService import ProcessorService
        from pullenti.ner.Referent import Referent
        self.__m_sofa = SourceOfAnalysis(None)
        self.__m_sofa.deserialize(stream)
        self.base_language = MorphLang._new6(SerializerHelper.deserialize_int(stream))
        self.__m_entities = list()
        cou = SerializerHelper.deserialize_int(stream)
        i = 0
        while i < cou: 
            typ = SerializerHelper.deserialize_string(stream)
            r = ProcessorService.create_referent(typ)
            if (r is None): 
                r = Referent("UNDEFINED")
            self.__m_entities.append(r)
            i += 1
        i = 0
        while i < cou: 
            self.__m_entities[i].deserialize(stream, self.__m_entities, self.__m_sofa)
            i += 1
        self.first_token = SerializerHelper.deserialize_tokens(stream, self)
        self.__create_statistics()
    
    @staticmethod
    def _new2641(_arg1 : 'Processor', _arg2 : 'ExtOntology') -> 'AnalysisKit':
        res = AnalysisKit()
        res.processor = _arg1
        res.ontology = _arg2
        return res
    
    @staticmethod
    def _new2642(_arg1 : 'SourceOfAnalysis', _arg2 : bool, _arg3 : 'MorphLang', _arg4 : EventHandler, _arg5 : 'ExtOntology', _arg6 : 'Processor') -> 'AnalysisKit':
        res = AnalysisKit(_arg1, _arg2, _arg3, _arg4)
        res.ontology = _arg5
        res.processor = _arg6
        return res