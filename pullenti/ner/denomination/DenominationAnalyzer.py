# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import datetime
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.Referent import Referent
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.bank.internal.PullentiNerBankInternalResourceHelper import PullentiNerBankInternalResourceHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.denomination.internal.MetaDenom import MetaDenom
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.denomination.DenominationReferent import DenominationReferent
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology

class DenominationAnalyzer(Analyzer):
    """ Анализатор деноминаций и обозначений (типа C#, A-320)
    Специфический анализатор, то есть нужно явно создавать процессор через функцию CreateSpecificProcessor,
    указав имя анализатора.
    Анализатор деноминаций
    """
    
    ANALYZER_NAME = "DENOMINATION"
    """ Имя анализатора ("DENOMINATION") """
    
    @property
    def name(self) -> str:
        return DenominationAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Деноминации"
    
    @property
    def description(self) -> str:
        return "Деноминации и обозначения типа СС-300, АН-24, С++"
    
    def clone(self) -> 'Analyzer':
        return DenominationAnalyzer()
    
    @property
    def progress_weight(self) -> int:
        return 5
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим (IsSpecific = true) """
        return True
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaDenom._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaDenom.DENOM_IMAGE_ID] = PullentiNerBankInternalResourceHelper.get_bytes("denom.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == DenominationReferent.OBJ_TYPENAME): 
            return DenominationReferent()
        return None
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        # Основная функция выделения объектов
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), AnalyzerDataWithOntology)
        for k in range(2):
            detect_new_denoms = False
            dt = datetime.datetime.now()
            t = kit.first_token
            first_pass3640 = True
            while True:
                if first_pass3640: first_pass3640 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_whitespace_before): 
                    pass
                elif (t.previous is not None and ((t.previous.is_char_of(",") or BracketHelper.can_be_start_of_sequence(t.previous, False, False)))): 
                    pass
                else: 
                    continue
                rt0 = self.__try_attach_spec(t)
                if (rt0 is not None): 
                    rt0.referent = ad.register_referent(rt0.referent)
                    kit.embed_token(rt0)
                    t = (rt0)
                    continue
                if (not t.chars.is_letter): 
                    continue
                if (not self.__can_be_start_of_denom(t)): 
                    continue
                ot = None
                ot = ad.local_ontology.try_attach(t, None, False)
                if (ot is not None and (isinstance(ot[0].item.referent, DenominationReferent))): 
                    if (self.__check_attach(ot[0].begin_token, ot[0].end_token)): 
                        cl = Utils.asObjectOrNull(ot[0].item.referent.clone(), DenominationReferent)
                        cl.occurrence.clear()
                        rt = ReferentToken(cl, ot[0].begin_token, ot[0].end_token)
                        kit.embed_token(rt)
                        t = (rt)
                        continue
                if (k > 0): 
                    continue
                if (t is not None and t.kit.ontology is not None): 
                    ot = t.kit.ontology.attach_token(DenominationReferent.OBJ_TYPENAME, t)
                    if ((ot) is not None): 
                        if (self.__check_attach(ot[0].begin_token, ot[0].end_token)): 
                            dr = DenominationReferent()
                            dr.merge_slots(ot[0].item.referent, True)
                            rt = ReferentToken(ad.register_referent(dr), ot[0].begin_token, ot[0].end_token)
                            kit.embed_token(rt)
                            t = (rt)
                            continue
                rt0 = self.try_attach(t, False)
                if (rt0 is not None): 
                    rt0.referent = ad.register_referent(rt0.referent)
                    kit.embed_token(rt0)
                    detect_new_denoms = True
                    t = (rt0)
                    if (len(ad.local_ontology.items) > 1000): 
                        break
            if (not detect_new_denoms): 
                break
    
    def __can_be_start_of_denom(self, t : 'Token') -> bool:
        if ((t is None or not t.chars.is_letter or t.next0_ is None) or t.is_newline_after): 
            return False
        if (not (isinstance(t, TextToken))): 
            return False
        if (t.length_char > 4): 
            return False
        t = t.next0_
        if (t.chars.is_letter): 
            return False
        if (isinstance(t, NumberToken)): 
            return True
        if (t.is_char_of("/\\") or t.is_hiphen): 
            return isinstance(t.next0_, NumberToken)
        if (t.is_char_of("+*&^#@!_")): 
            return True
        return False
    
    def process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        return self.try_attach(begin, False)
    
    def try_attach(self, t : 'Token', for_ontology : bool=False) -> 'ReferentToken':
        if (t is None): 
            return None
        rt0 = self.__try_attach_spec(t)
        if (rt0 is not None): 
            return rt0
        if (t.chars.is_all_lower): 
            if (not t.is_whitespace_after and (isinstance(t.next0_, NumberToken))): 
                if (t.previous is None or t.is_whitespace_before or t.previous.is_char_of(",:")): 
                    pass
                else: 
                    return None
            else: 
                return None
        tmp = io.StringIO()
        t1 = t
        hiph = False
        ok = True
        nums = 0
        chars = 0
        w = t1.next0_
        first_pass3641 = True
        while True:
            if first_pass3641: first_pass3641 = False
            else: w = w.next0_
            if (not (w is not None)): break
            if (w.is_whitespace_before and not for_ontology): 
                break
            if (w.is_char_of("/\\_") or w.is_hiphen): 
                hiph = True
                print('-', end="", file=tmp)
                continue
            hiph = False
            nt = Utils.asObjectOrNull(w, NumberToken)
            if (nt is not None): 
                if (nt.typ != NumberSpellingType.DIGIT): 
                    break
                t1 = (nt)
                print(nt.get_source_text(), end="", file=tmp)
                nums += 1
                continue
            tt = Utils.asObjectOrNull(w, TextToken)
            if (tt is None): 
                break
            if (tt.length_char > 3): 
                ok = False
                break
            if (not str.isalpha(tt.term[0])): 
                if (tt.is_char_of(",:") or BracketHelper.can_be_end_of_sequence(tt, False, None, False)): 
                    break
                if (not tt.is_char_of("+*&^#@!")): 
                    ok = False
                    break
                chars += 1
            t1 = (tt)
            print(tt.get_source_text(), end="", file=tmp)
        if (not for_ontology): 
            if ((tmp.tell() < 1) or not ok or hiph): 
                return None
            if (tmp.tell() > 12): 
                return None
            last = Utils.getCharAtStringIO(tmp, tmp.tell() - 1)
            if (last == '!'): 
                return None
            if ((nums + chars) == 0): 
                return None
            if (not self.__check_attach(t, t1)): 
                return None
        new_dr = DenominationReferent()
        new_dr._add_value(t, t1)
        return ReferentToken(new_dr, t, t1)
    
    def __try_attach_spec(self, t : 'Token') -> 'ReferentToken':
        # Некоторые специфические случаи
        if (t is None): 
            return None
        t0 = t
        nt = Utils.asObjectOrNull(t, NumberToken)
        if (nt is not None and nt.typ == NumberSpellingType.DIGIT and nt.value == "1"): 
            if (t.next0_ is not None and t.next0_.is_hiphen): 
                t = t.next0_
            if ((isinstance(t.next0_, TextToken)) and not t.next0_.is_whitespace_before): 
                if (t.next0_.is_value("C", None) or t.next0_.is_value("С", None)): 
                    dr = DenominationReferent()
                    dr.add_slot(DenominationReferent.ATTR_VALUE, "1С", False, 0)
                    dr.add_slot(DenominationReferent.ATTR_VALUE, "1C", False, 0)
                    return ReferentToken(dr, t0, t.next0_)
        if (((nt is not None and nt.typ == NumberSpellingType.DIGIT and (isinstance(t.next0_, TextToken))) and not t.is_whitespace_after and not t.next0_.chars.is_all_lower) and t.next0_.chars.is_letter): 
            dr = DenominationReferent()
            dr.add_slot(DenominationReferent.ATTR_VALUE, "{0}{1}".format(nt.get_source_text(), t.next0_.term), False, 0)
            return ReferentToken(dr, t0, t.next0_)
        return None
    
    def __check_attach(self, begin : 'Token', end : 'Token') -> bool:
        t = begin
        while t is not None and t != end.next0_: 
            if (t != begin): 
                co = t.whitespaces_before_count
                if (co > 0): 
                    if (co > 1): 
                        return False
                    if (t.chars.is_all_lower): 
                        return False
                    if (t.previous.chars.is_all_lower): 
                        return False
            t = t.next0_
        if (not end.is_whitespace_after and end.next0_ is not None): 
            if (not end.next0_.is_char_of(",;") and not BracketHelper.can_be_end_of_sequence(end.next0_, False, None, False)): 
                return False
        return True
    
    __m_inites = False
    
    @staticmethod
    def initialize() -> None:
        if (DenominationAnalyzer.__m_inites): 
            return
        DenominationAnalyzer.__m_inites = True
        MetaDenom.initialize()
        ProcessorService.register_analyzer(DenominationAnalyzer())