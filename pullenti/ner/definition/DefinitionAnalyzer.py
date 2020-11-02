# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.definition.DefinitionKind import DefinitionKind
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.definition.internal.ParenthesisToken import ParenthesisToken
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.bank.internal.PullentiNerBankInternalResourceHelper import PullentiNerBankInternalResourceHelper
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.Referent import Referent
from pullenti.ner.definition.internal.MetaDefin import MetaDefin
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.definition.internal.DefinitionAnalyzerEn import DefinitionAnalyzerEn
from pullenti.ner.core.Termin import Termin

class DefinitionAnalyzer(Analyzer):
    """ Анализатор определений.
    Специфический анализатор, то есть нужно явно создавать процессор через функцию CreateSpecificProcessor,
    указав имя анализатора. """
    
    ANALYZER_NAME = "THESIS"
    """ Имя анализатора ("THESIS") """
    
    @property
    def name(self) -> str:
        return DefinitionAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Тезисы"
    
    @property
    def description(self) -> str:
        return "Утверждения и определения"
    
    def clone(self) -> 'Analyzer':
        return DefinitionAnalyzer()
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaDefin._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaDefin.IMAGE_DEF_ID] = PullentiNerBankInternalResourceHelper.get_bytes("defin.png")
        res[MetaDefin.IMAGE_ASS_ID] = PullentiNerBankInternalResourceHelper.get_bytes("assert.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == DefinitionReferent.OBJ_TYPENAME): 
            return DefinitionReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ALL"]
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим (IsSpecific = true) """
        return True
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AnalyzerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        # Основная функция выделения объектов
        ad = kit.get_analyzer_data(self)
        if (kit.base_language == MorphLang.EN): 
            DefinitionAnalyzerEn.process(kit, ad)
            return
        glos_regime = False
        onto = None
        oh = dict()
        if (kit.ontology is not None): 
            onto = TerminCollection()
            for it in kit.ontology.items: 
                if (isinstance(it.referent, DefinitionReferent)): 
                    termin = it.referent.get_string_value(DefinitionReferent.ATTR_TERMIN)
                    if (not termin in oh): 
                        oh[termin] = True
                        onto.add(Termin._new1116(termin, termin))
            if (len(onto.termins) == 0): 
                onto = (None)
        t = kit.first_token
        first_pass3627 = True
        while True:
            if first_pass3627: first_pass3627 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not glos_regime and t.is_newline_before): 
                tt = DefinitionAnalyzer.__try_attach_glossary(t)
                if (tt is not None): 
                    t = tt
                    glos_regime = True
                    continue
            max_char = 0
            ok = False
            if (MiscHelper.can_be_start_of_sentence(t)): 
                ok = True
            elif (((t.is_value("ЧТО", None) and t.next0_ is not None and t.previous is not None) and t.previous.is_comma and t.previous.previous is not None) and t.previous.previous.morph.class0_ == MorphClass.VERB): 
                ok = True
                t = t.next0_
                if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    t = t.next0_
            elif (t.is_newline_before and glos_regime): 
                ok = True
            elif (BracketHelper.can_be_start_of_sequence(t, True, False) and t.previous is not None and t.previous.is_char(':')): 
                ok = True
                t = t.next0_
                tt = t.next0_
                while tt is not None: 
                    if (BracketHelper.can_be_end_of_sequence(tt, True, t, False)): 
                        max_char = tt.previous.end_char
                        break
                    tt = tt.next0_
            elif (t.is_newline_before and t.previous is not None and t.previous.is_char_of(";:")): 
                ok = True
            if (not ok): 
                continue
            prs = DefinitionAnalyzer.try_attach(t, glos_regime, onto, max_char, False)
            if (prs is None): 
                prs = self.__try_attach_end(t, onto, max_char)
            if (prs is not None): 
                for pr in prs: 
                    if (pr.referent is not None): 
                        pr.referent = ad.register_referent(pr.referent)
                        pr.referent.add_occurence_of_ref_tok(pr)
                    t = pr.end_token
            else: 
                if (t.is_char('(')): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        continue
                ign = False
                tt = t.next0_
                while tt is not None: 
                    if (MiscHelper.can_be_start_of_sentence(tt)): 
                        if (tt.previous.is_char(';')): 
                            ign = True
                        break
                    tt = tt.next0_
                if (glos_regime and not t.is_newline_before): 
                    pass
                elif (not ign): 
                    glos_regime = False
    
    @staticmethod
    def __try_attach_glossary(t : 'Token') -> 'Token':
        if (t is None or not t.is_newline_before): 
            return None
        while t is not None: 
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                break
            t = t.next0_
        if (t is None): 
            return None
        if (t.is_value("ГЛОССАРИЙ", None) or t.is_value("ОПРЕДЕЛЕНИЕ", None)): 
            t = t.next0_
        elif (t.is_value("СПИСОК", None) and t.next0_ is not None and t.next0_.is_value("ОПРЕДЕЛЕНИЕ", None)): 
            t = t.next0_.next0_
        else: 
            use = False
            ponat = False
            t0 = t
            while t is not None: 
                if (t.is_value("ИСПОЛЬЗОВАТЬ", None)): 
                    use = True
                elif (t.is_value("ПОНЯТИЕ", None) or t.is_value("ОПРЕДЕЛЕНИЕ", None)): 
                    ponat = True
                elif (t.is_char(':')): 
                    if (use and ponat and t.is_newline_after): 
                        return t
                elif (t != t0 and MiscHelper.can_be_start_of_sentence(t)): 
                    break
                t = t.next0_
            return None
        if (t is None): 
            return None
        if (t.is_and and t.next0_ is not None and t.next0_.is_value("СОКРАЩЕНИЕ", None)): 
            t = t.next0_.next0_
        if (t is not None and t.is_char_of(":.")): 
            t = t.next0_
        if (t is not None and t.is_newline_before): 
            return t.previous
        return None
    
    def process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        li = DefinitionAnalyzer.try_attach(begin, False, None, 0, False)
        if (li is None or len(li) == 0): 
            return None
        return li[0]
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        if (begin is None): 
            return None
        t1 = None
        t = begin
        while t is not None: 
            if (t.is_hiphen and ((t.is_whitespace_before or t.is_whitespace_after))): 
                break
            else: 
                t1 = t
            t = t.next0_
        if (t1 is None): 
            return None
        dre = DefinitionReferent()
        dre.add_slot(DefinitionReferent.ATTR_TERMIN, MiscHelper.get_text_value(begin, t1, GetTextAttr.NO), False, 0)
        return ReferentToken(dre, begin, t1)
    
    @staticmethod
    def __ignore_list_prefix(t : 'Token') -> 'Token':
        first_pass3628 = True
        while True:
            if first_pass3628: first_pass3628 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_after): 
                break
            if (isinstance(t, NumberToken)): 
                if (t.typ == NumberSpellingType.WORDS): 
                    break
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0, None)
                if (npt is not None and npt.end_char > t.end_char): 
                    break
                continue
            if (not (isinstance(t, TextToken))): 
                break
            if (not t.chars.is_letter): 
                if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    break
                continue
            if (t.length_char == 1 and t.next0_ is not None and t.next0_.is_char_of(").")): 
                continue
            break
        return t
    
    @staticmethod
    def try_attach(t : 'Token', glos_regime : bool, onto : 'TerminCollection', max_char : int, this_is_def : bool=False) -> typing.List['ReferentToken']:
        if (t is None): 
            return None
        t0 = t
        t = DefinitionAnalyzer.__ignore_list_prefix(t)
        if (t is None): 
            return None
        has_prefix = False
        if (t0 != t): 
            has_prefix = True
        t0 = t
        decree_ = None
        pt = ParenthesisToken.try_attach(t)
        if (pt is not None): 
            decree_ = pt.ref
            t = pt.end_token.next0_
            if (t is not None and t.is_char(',')): 
                t = t.next0_
        if (t is None): 
            return None
        l0 = None
        l1 = None
        alt_name = None
        name0 = None
        normal_left = False
        can_next_sent = False
        coef = DefinitionKind.UNDEFINED
        if (glos_regime): 
            coef = DefinitionKind.DEFINITION
        is_onto_termin = False
        onto_prefix = None
        if (t.is_value("ПОД", None)): 
            t = t.next0_
            normal_left = True
        elif (t.is_value("ИМЕННО", None)): 
            t = t.next0_
        if ((t is not None and t.is_value("УТРАТИТЬ", None) and t.next0_ is not None) and t.next0_.is_value("СИЛА", None)): 
            while t is not None: 
                if (t.is_newline_after): 
                    re0 = list()
                    re0.append(ReferentToken(None, t0, t))
                    return re0
                t = t.next0_
            return None
        misc_token = None
        first_pass3629 = True
        while True:
            if first_pass3629: first_pass3629 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t != t0 and MiscHelper.can_be_start_of_sentence(t)): 
                break
            if (max_char > 0 and t.end_char > max_char): 
                break
            mt = DefinitionAnalyzer.__try_attach_misc_token(t)
            if (mt is not None): 
                misc_token = mt
                t = mt.end_token
                normal_left = mt.morph.case_.is_nominative
                continue
            if (not (isinstance(t, TextToken))): 
                r = t.get_referent()
                if (r is not None and ((r.type_name == "DECREE" or r.type_name == "DECREEPART"))): 
                    decree_ = r
                    if (l0 is None): 
                        if ((t.next0_ is not None and t.next0_.get_morph_class_in_dictionary() == MorphClass.VERB and t.next0_.next0_ is not None) and t.next0_.next0_.is_comma): 
                            t = t.next0_.next0_
                            if (t.next0_ is not None and t.next0_.is_value("ЧТО", None)): 
                                t = t.next0_
                            continue
                        l0 = t
                    l1 = t
                    continue
                if (r is not None and (((r.type_name == "ORGANIZATION" or r.type_name == "PERSONPROPERTY" or r.type_name == "STREET") or r.type_name == "GEO"))): 
                    if (l0 is None): 
                        l0 = t
                    l1 = t
                    continue
                if ((isinstance(t, NumberToken)) and NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None) is not None): 
                    pass
                else: 
                    break
            pt = ParenthesisToken.try_attach(t)
            if (pt is not None and pt.ref is not None): 
                if (pt.ref.type_name == "DECREE" or pt.ref.type_name == "DECREEPART"): 
                    decree_ = pt.ref
                t = pt.end_token.next0_
                if (l0 is None): 
                    continue
                break
            if (not t.chars.is_letter): 
                if (t.is_hiphen): 
                    if (t.is_whitespace_after or t.is_whitespace_before): 
                        break
                    continue
                if (t.is_char('(')): 
                    if (l1 is None): 
                        break
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is None): 
                        break
                    tt1 = t.next0_
                    if (tt1.is_value("ДАЛЕЕ", None)): 
                        tt1 = tt1.next0_
                        if (not tt1.chars.is_letter): 
                            tt1 = tt1.next0_
                        if (tt1 is None): 
                            return None
                    alt_name = MiscHelper.get_text_value(tt1, br.end_token.previous, GetTextAttr.NO)
                    if (br.begin_token.next0_ == br.end_token.previous): 
                        t = br.end_token
                        continue
                    t = br.end_token.next0_
                    break
                if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None and l0 is None and NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None) is not None): 
                        l0 = t.next0_
                        l1 = br.end_token.previous
                        alt_name = (None)
                        t = br.end_token.next0_
                    elif (br is not None and l0 is not None): 
                        l1 = br.end_token
                        alt_name = (None)
                        t = br.end_token
                        continue
                break
            if (t.is_value("ЭТО", None)): 
                break
            if (t.morph.class0_.is_conjunction): 
                if (not glos_regime or not t.is_and): 
                    break
                continue
            if (t.is_value("ДАВАТЬ", None) or t.is_value("ДАТЬ", None) or t.is_value("ФОРМУЛИРОВАТЬ", None)): 
                npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.noun.is_value("ОПРЕДЕЛЕНИЕ", None)): 
                    t = npt.end_token
                    if (t.next0_ is not None and t.next0_.is_value("ПОНЯТИЕ", None)): 
                        t = t.next0_
                    l0 = (None)
                    l1 = (None)
                    normal_left = True
                    can_next_sent = True
                    coef = DefinitionKind.DEFINITION
                    continue
            alt_name = (None)
            if (onto is not None): 
                took = onto.try_parse(t, TerminParseAttr.NO)
                if (took is not None): 
                    if (l0 is not None): 
                        if (onto_prefix is not None): 
                            break
                        onto_prefix = MiscHelper.get_text_value(l0, l1, GetTextAttr.KEEPREGISTER)
                    if (not is_onto_termin): 
                        is_onto_termin = True
                        l0 = t
                    name0 = took.termin.canonic_text
                    l1 = took.end_token
                    t = l1
                    continue
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
            if (npt is not None and npt.internal_noun is not None): 
                break
            if (npt is None): 
                if (l0 is not None): 
                    break
                if (t.morph.class0_.is_preposition or t.morph.class0_.is_verb): 
                    break
                if (t.morph.class0_.is_adjective): 
                    ve = 0
                    tt = t.next0_
                    while tt is not None: 
                        if (tt.get_morph_class_in_dictionary().is_verb): 
                            ve += 1
                        else: 
                            break
                        tt = tt.next0_
                    if ((ve > 0 and tt is not None and tt.is_value("ТАКОЙ", None)) and NounPhraseHelper.try_parse(tt.next0_, NounPhraseParseAttr.NO, 0, None) is not None): 
                        l1 = t
                        l0 = l1
                        t = t.next0_
                        break
                if (not t.chars.is_all_lower and t.length_char > 2 and t.get_morph_class_in_dictionary().is_undefined): 
                    pass
                else: 
                    continue
            if (l0 is None): 
                if (t.morph.class0_.is_preposition): 
                    break
                if (DefinitionAnalyzer.__m_verbot_first_words.try_parse(t, TerminParseAttr.NO) is not None and onto is None): 
                    break
                l0 = t
            elif (t.morph.class0_.is_preposition): 
                if (DefinitionAnalyzer.__m_verbot_last_words.try_parse(npt.noun.begin_token, TerminParseAttr.NO) is not None or DefinitionAnalyzer.__m_verbot_last_words.try_parse(npt.begin_token, TerminParseAttr.NO) is not None): 
                    t = npt.end_token.next0_
                    break
            if (npt is not None): 
                if (DefinitionAnalyzer.__m_verbot_first_words.try_parse(npt.noun.begin_token, TerminParseAttr.NO) is not None and onto is None): 
                    break
                ok1 = True
                if (not glos_regime): 
                    tt = npt.begin_token
                    while tt is not None and tt.end_char <= npt.end_char: 
                        if (tt.morph.class0_.is_pronoun or tt.morph.class0_.is_personal_pronoun): 
                            if (tt.is_value("ИНОЙ", None)): 
                                pass
                            else: 
                                ok1 = False
                                break
                        tt = tt.next0_
                if (not ok1): 
                    break
                l1 = npt.end_token
                t = l1
            else: 
                l1 = t
        if (not (isinstance(t, TextToken)) or ((l1 is None and not is_onto_termin)) or t.next0_ is None): 
            return None
        if (onto is not None and name0 is None): 
            return None
        is_not = False
        r0 = t
        r1 = None
        if (t.is_value("НЕ", None)): 
            t = t.next0_
            if (t is None): 
                return None
            is_not = True
        normal_right = False
        ok = 0
        hasthis = False
        if (t.is_hiphen or t.is_char_of(":") or ((can_next_sent and t.is_char('.')))): 
            if ((isinstance(t.next0_, TextToken)) and t.next0_.term == "ЭТО"): 
                ok = 2
                t = t.next0_.next0_
                hasthis = True
            elif (glos_regime): 
                ok = 2
                t = t.next0_
            elif (is_onto_termin): 
                ok = 1
                t = t.next0_
            elif (t.is_hiphen and t.is_whitespace_before and t.is_whitespace_after): 
                tt = t.next0_
                if (tt is not None and tt.is_value("НЕ", None)): 
                    is_not = True
                    tt = tt.next0_
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.morph.case_.is_nominative): 
                    ok = 2
                    t = tt
                elif ((tt is not None and tt.morph.case_.is_nominative and tt.morph.class0_.is_verb) and tt.morph.class0_.is_adjective): 
                    ok = 2
                    t = tt
            else: 
                rt0 = DefinitionAnalyzer.try_attach(t.next0_, False, None, max_char, False)
                if (rt0 is not None): 
                    for rt in rt0: 
                        if (coef == DefinitionKind.DEFINITION and rt.referent.kind == DefinitionKind.ASSERTATION): 
                            rt.referent.kind = coef
                    return rt0
        elif (t.term == "ЭТО"): 
            npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                ok = 1
                t = t.next0_
                hasthis = True
        elif (t.is_value("ЯВЛЯТЬСЯ", None) or t.is_value("ПРИЗНАВАТЬСЯ", None) or t.is_value("ЕСТЬ", None)): 
            if (t.is_value("ЯВЛЯТЬСЯ", None)): 
                normal_right = True
            t11 = t.next0_
            while t11 is not None: 
                if (t11.is_comma or t11.morph.class0_.is_preposition or t11.morph.class0_.is_conjunction): 
                    pass
                else: 
                    break
                t11 = t11.next0_
            npt = NounPhraseHelper.try_parse(t11, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None or t11.get_morph_class_in_dictionary().is_adjective): 
                ok = 1
                t = t11
                normal_left = True
            elif ((t11 is not None and t11.is_value("ОДИН", None) and t11.next0_ is not None) and t11.next0_.is_value("ИЗ", None)): 
                ok = 1
                t = t11
                normal_left = True
            if (is_onto_termin): 
                ok = 1
            elif (l0 == l1 and npt is not None and l0.morph.class0_.is_adjective): 
                if (((l0.morph.gender) & (npt.morph.gender)) != (MorphGender.UNDEFINED) or ((l0.morph.number) & (npt.morph.number)) == (MorphNumber.PLURAL)): 
                    name0 = "{0} {1}".format(l0.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, npt.morph.gender, False), npt.noun.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, npt.morph.gender, False))
                else: 
                    ok = 0
        elif (t.is_value("ОЗНАЧАТЬ", None) or t.is_value("НЕСТИ", None)): 
            t11 = t.next0_
            if (t11 is not None and t11.is_char(':')): 
                t11 = t11.next0_
            if (t11.is_value("НЕ", None) and t11.next0_ is not None): 
                is_not = True
                t11 = t11.next0_
            npt = NounPhraseHelper.try_parse(t11, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None or is_onto_termin): 
                ok = 1
                t = t11
        elif (t.is_value("ВЫРАЖАТЬ", None)): 
            t11 = t.next0_
            while t11 is not None: 
                if ((t11.morph.class0_.is_pronoun or t11.is_comma or t11.morph.class0_.is_preposition) or t11.morph.class0_.is_conjunction): 
                    pass
                else: 
                    break
                t11 = t11.next0_
            npt = NounPhraseHelper.try_parse(t11, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None or is_onto_termin): 
                ok = 1
                t = t11
        elif (((t.is_value("СЛЕДОВАТЬ", None) or t.is_value("МОЖНО", None))) and t.next0_ is not None and ((t.next0_.is_value("ПОНИМАТЬ", None) or t.next0_.is_value("ОПРЕДЕЛИТЬ", None) or t.next0_.is_value("СЧИТАТЬ", None)))): 
            t11 = t.next0_.next0_
            if (t11 is None): 
                return None
            if (t11.is_value("КАК", None)): 
                t11 = t11.next0_
            ok = 2
            t = t11
        elif (t.is_value("ПРЕДСТАВЛЯТЬ", None) and t.next0_ is not None and t.next0_.is_value("СОБОЙ", None)): 
            t11 = t.next0_.next0_
            if (t11 is None): 
                return None
            npt = NounPhraseHelper.try_parse(t11, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None or t11.morph.class0_.is_adjective or is_onto_termin): 
                ok = 1
                t = t11
        elif ((((t.is_value("ДОЛЖЕН", None) or t.is_value("ДОЛЖНЫЙ", None))) and t.next0_ is not None and t.next0_.is_value("ПРЕДСТАВЛЯТЬ", None)) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("СОБОЙ", None)): 
            t11 = t.next0_.next0_.next0_
            if (t11 is None): 
                return None
            npt = NounPhraseHelper.try_parse(t11, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None or t11.morph.class0_.is_adjective or is_onto_termin): 
                ok = 1
                t = t11
        elif (t.is_value("ДОЛЖНЫЙ", None)): 
            if (t.next0_ is not None and t.next0_.morph.class0_.is_verb): 
                t = t.next0_
            ok = 1
        elif (((((((((t.is_value("МОЖЕТ", None) or t.is_value("МОЧЬ", None) or t.is_value("ВПРАВЕ", None)) or t.is_value("ЗАПРЕЩЕНО", None) or t.is_value("РАЗРЕШЕНО", None)) or t.is_value("ОТВЕЧАТЬ", None) or t.is_value("ПРИЗНАВАТЬ", None)) or t.is_value("ОСВОБОЖДАТЬ", None) or t.is_value("ОСУЩЕСТВЛЯТЬ", None)) or t.is_value("ПРОИЗВОДИТЬ", None) or t.is_value("ПОДЛЕЖАТЬ", None)) or t.is_value("ПРИНИМАТЬ", None) or t.is_value("СЧИТАТЬ", None)) or t.is_value("ИМЕТЬ", None) or t.is_value("ВПРАВЕ", None)) or t.is_value("ОБЯЗАН", None) or t.is_value("ОБЯЗАТЬ", None))): 
            ok = 1
        if (ok == 0): 
            return None
        if (t is None): 
            return None
        if (t.is_value("НЕ", None)): 
            if (not is_onto_termin): 
                return None
        dr = DefinitionReferent()
        normal_left = True
        nam = Utils.ifNotNull(name0, MiscHelper.get_text_value(l0, l1, (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE if normal_left else GetTextAttr.NO)))
        if (nam is None): 
            return None
        if (name0 is None): 
            pass
        if (name0 is None): 
            dr.tag = MetaToken._new836(l0, l1, normal_left)
        if (l0 == l1 and l0.morph.class0_.is_adjective and l0.morph.case_.is_instrumental): 
            if (t is not None and t.is_value("ТАКОЙ", None)): 
                npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.morph.case_.is_nominative): 
                    str0_ = l0.get_normal_case_text(MorphClass.ADJECTIVE, (MorphNumber.SINGULAR if npt.morph.number == MorphNumber.PLURAL else MorphNumber.UNDEFINED), npt.morph.gender, False)
                    if (str0_ is None): 
                        str0_ = l0.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                    nam = "{0} {1}".format(str0_, npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
        if (decree_ is not None): 
            tt = l0
            while tt is not None and tt.end_char <= l1.end_char: 
                if (tt.get_referent() == decree_): 
                    decree_ = (None)
                    break
                tt = tt.next0_
        if (nam.endswith(")") and alt_name is None): 
            ii = nam.rfind('(')
            if (ii > 0): 
                alt_name = nam[ii + 1:ii + 1+len(nam) - ii - 2].strip()
                nam = nam[0:0+ii].strip()
        dr.add_slot(DefinitionReferent.ATTR_TERMIN, nam, False, 0)
        if (alt_name is not None): 
            dr.add_slot(DefinitionReferent.ATTR_TERMIN, alt_name, False, 0)
        if (not is_onto_termin): 
            npt2 = NounPhraseHelper.try_parse(l0, NounPhraseParseAttr.NO, 0, None)
            if (npt2 is not None and npt2.morph.number == MorphNumber.PLURAL): 
                nam = MiscHelper.get_text_value(l0, l1, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)
                if (nam is not None): 
                    dr.add_slot(DefinitionReferent.ATTR_TERMIN, nam, False, 0)
        if (misc_token is not None): 
            if (misc_token.morph.class0_.is_noun): 
                dr.add_slot(DefinitionReferent.ATTR_TERMIN_ADD, Utils.asObjectOrNull(misc_token.tag, str), False, 0)
            else: 
                dr.add_slot(DefinitionReferent.ATTR_MISC, Utils.asObjectOrNull(misc_token.tag, str), False, 0)
        t1 = None
        multi_parts = None
        first_pass3630 = True
        while True:
            if first_pass3630: first_pass3630 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (MiscHelper.can_be_start_of_sentence(t)): 
                break
            if (max_char > 0 and t.end_char > max_char): 
                break
            t1 = t
            if (t.is_char('(') and (isinstance(t.next0_, ReferentToken))): 
                r = t.next0_.get_referent()
                if (r.type_name == "DECREE" or r.type_name == "DECREEPART"): 
                    decree_ = r
                    t = t.next0_
                    t1 = t
                    while t.next0_ is not None:
                        if (t.next0_.is_comma_and and (isinstance(t.next0_.next0_, ReferentToken)) and ((t.next0_.next0_.get_referent().type_name == "DECREE" or t.next0_.next0_.get_referent().type_name == "DECREEPART"))): 
                            t = t.next0_.next0_
                            t1 = t
                        else: 
                            break
                    if (t1.next0_ is not None and t1.next0_.is_char(')')): 
                        t1 = t1.next0_
                        t = t1
                    continue
            if (t.is_char('(') and t.next0_ is not None and t.next0_.is_value("ДАЛЕЕ", None)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t1 = br.end_token
                    t = t1
                    continue
            if (t.is_char(':') and t.is_whitespace_after): 
                mt = DefinitionAnalyzer.__try_parse_list_item(t.next0_)
                if (mt is not None): 
                    multi_parts = list()
                    multi_parts.append(mt)
                    tt = mt.end_token.next0_
                    while tt is not None: 
                        if (max_char > 0 and tt.end_char > max_char): 
                            break
                        mt = DefinitionAnalyzer.__try_parse_list_item(tt)
                        if (mt is None): 
                            break
                        multi_parts.append(mt)
                        tt = mt.end_token
                        tt = tt.next0_
                    break
            if (not t.is_char_of(";.")): 
                r1 = t
        if (r1 is None): 
            return None
        if (r0.next0_ is not None and (isinstance(r0, TextToken)) and not r0.chars.is_letter): 
            r0 = r0.next0_
        normal_right = False
        df = MiscHelper.get_text_value(r0, r1, Utils.valToEnum((((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE if normal_right else GetTextAttr.NO))) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        if (multi_parts is not None): 
            res1 = list()
            dr.kind = (DefinitionKind.NEGATION if is_not else DefinitionKind.ASSERTATION)
            for mp in multi_parts: 
                dr1 = dr.clone()
                tmp = io.StringIO()
                if (df is not None): 
                    print(df, end="", file=tmp)
                    if (tmp.tell() > 0 and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == ':'): 
                        Utils.setLengthStringIO(tmp, tmp.tell() - 1)
                    print(": ", end="", file=tmp)
                    print(MiscHelper.get_text_value(mp.begin_token, mp.end_token, GetTextAttr.KEEPREGISTER), end="", file=tmp)
                dr1.add_slot(DefinitionReferent.ATTR_VALUE, Utils.toStringStringIO(tmp), False, 0)
                res1.append(ReferentToken(dr1, (t0 if len(res1) == 0 else mp.begin_token), mp.end_token))
            return res1
        if (df is None or (len(df) < 20)): 
            return None
        if (onto_prefix is not None): 
            df = "{0} {1}".format(onto_prefix, df)
        if ((coef == DefinitionKind.UNDEFINED and ok > 1 and not is_not) and multi_parts is None): 
            all_nps = True
            cou_npt = 0
            tt = l0
            while tt is not None and tt.end_char <= l1.end_char: 
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None)
                if (npt is None and tt.morph.class0_.is_preposition): 
                    npt = NounPhraseHelper.try_parse(tt.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is None): 
                    all_nps = False
                    break
                cou_npt += 1
                tt = npt.end_token
                tt = tt.next0_
            if (all_nps and (cou_npt < 5)): 
                if ((math.floor(len(df) / 3)) > len(nam)): 
                    coef = DefinitionKind.DEFINITION
        if ((t1.is_char(';') and t1.is_newline_after and onto is not None) and not has_prefix and multi_parts is None): 
            tmp = io.StringIO()
            print(df, end="", file=tmp)
            t = t1.next0_
            first_pass3631 = True
            while True:
                if first_pass3631: first_pass3631 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_char('(')): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        continue
                tt = DefinitionAnalyzer.__ignore_list_prefix(t)
                if (tt is None): 
                    break
                tt1 = None
                ttt1 = tt
                while ttt1 is not None: 
                    if (ttt1.is_newline_after): 
                        tt1 = ttt1
                        break
                    ttt1 = ttt1.next0_
                if (tt1 is None): 
                    break
                df1 = MiscHelper.get_text_value(tt, (tt1.previous if tt1.is_char_of(".;") else tt1), GetTextAttr.KEEPREGISTER)
                if (df1 is None): 
                    break
                print(";\n {0}".format(df1), end="", file=tmp, flush=True)
                t1 = tt1
                t = t1
                if (not tt1.is_char(';')): 
                    break
            df = Utils.toStringStringIO(tmp)
        dr.add_slot(DefinitionReferent.ATTR_VALUE, df, False, 0)
        if (is_not): 
            coef = DefinitionKind.NEGATION
        elif (hasthis and this_is_def): 
            coef = DefinitionKind.DEFINITION
        elif (misc_token is not None and not misc_token.morph.class0_.is_noun): 
            coef = DefinitionKind.ASSERTATION
        if (coef == DefinitionKind.UNDEFINED): 
            coef = DefinitionKind.ASSERTATION
        if (decree_ is not None): 
            dr.add_slot(DefinitionReferent.ATTR_DECREE, decree_, False, 0)
        dr.kind = coef
        res = list()
        res.append(ReferentToken(dr, t0, t1))
        return res
    
    def __try_attach_end(self, t : 'Token', onto : 'TerminCollection', max_char : int) -> typing.List['ReferentToken']:
        # Это распознавание случая, когда термин находится в конце
        if (t is None): 
            return None
        t0 = t
        t = DefinitionAnalyzer.__ignore_list_prefix(t)
        if (t is None): 
            return None
        has_prefix = False
        if (t0 != t): 
            has_prefix = True
        t0 = t
        decree_ = None
        pt = ParenthesisToken.try_attach(t)
        if (pt is not None): 
            decree_ = pt.ref
            t = pt.end_token.next0_
            if (t is not None and t.is_char(',')): 
                t = t.next0_
        if (t is None): 
            return None
        r0 = t0
        r1 = None
        l0 = None
        first_pass3632 = True
        while True:
            if first_pass3632: first_pass3632 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t != t0 and MiscHelper.can_be_start_of_sentence(t)): 
                break
            if (max_char > 0 and t.end_char > max_char): 
                break
            if (t.is_value("НАЗЫВАТЬ", None) or t.is_value("ИМЕНОВАТЬ", None)): 
                pass
            else: 
                continue
            r1 = t.previous
            tt = r1
            while tt is not None: 
                if ((tt.is_value("БУДЕМ", None) or tt.is_value("ДАЛЬНЕЙШИЙ", None) or tt.is_value("ДАЛЕЕ", None)) or tt.is_value("В", None)): 
                    r1 = tt.previous
                else: 
                    break
                tt = tt.previous
            l0 = t.next0_
            tt = l0
            while tt is not None: 
                if ((tt.is_value("БУДЕМ", None) or tt.is_value("ДАЛЬНЕЙШИЙ", None) or tt.is_value("ДАЛЕЕ", None)) or tt.is_value("В", None)): 
                    l0 = tt.next0_
                else: 
                    break
                tt = tt.next0_
            break
        if (l0 is None or r1 is None): 
            return None
        l1 = None
        cou = 0
        t = l0
        while t is not None: 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is None and t != l0 and t.morph.class0_.is_preposition): 
                npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is None): 
                break
            t = npt.end_token
            l1 = t
            cou += 1
            t = t.next0_
        if (l1 is None or cou > 3): 
            return None
        if ((((l1.end_char - l0.end_char)) * 2) > ((r1.end_char - r0.end_char))): 
            return None
        dr = DefinitionReferent._new1118(DefinitionKind.DEFINITION)
        nam = MiscHelper.get_text_value(l0, l1, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
        if (nam is None): 
            return None
        dr.add_slot(DefinitionReferent.ATTR_TERMIN, nam, False, 0)
        df = MiscHelper.get_text_value(r0, r1, GetTextAttr.KEEPREGISTER)
        dr.add_slot(DefinitionReferent.ATTR_VALUE, df, False, 0)
        t = l1.next0_
        if (t is None): 
            pass
        elif (t.is_char_of(".;")): 
            l1 = t
        elif (t.is_comma): 
            l1 = t
        elif (MiscHelper.can_be_start_of_sentence(t)): 
            pass
        else: 
            return None
        res = list()
        res.append(ReferentToken(dr, r0, l1))
        return res
    
    @staticmethod
    def __try_attach_misc_token(t : 'Token') -> 'MetaToken':
        if (t is None): 
            return None
        if (t.is_char('(')): 
            mt = DefinitionAnalyzer.__try_attach_misc_token(t.next0_)
            if (mt is not None and mt.end_token.next0_ is not None and mt.end_token.next0_.is_char(')')): 
                mt.begin_token = t
                mt.end_token = mt.end_token.next0_
                return mt
            return None
        if (t.is_value("КАК", None)): 
            t1 = None
            tt = t.next0_
            first_pass3633 = True
            while True:
                if first_pass3633: first_pass3633 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_newline_before): 
                    break
                npt1 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is None): 
                    break
                if (t1 is None or npt1.morph.case_.is_genitive): 
                    tt = npt1.end_token
                    t1 = tt
                    continue
                break
            if (t1 is not None): 
                res = MetaToken._new836(t, t1, MiscHelper.get_text_value(t, t1, GetTextAttr.KEEPQUOTES))
                res.morph.class0_ = MorphClass.NOUN
                return res
            return None
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0, None)
        if (npt is not None): 
            if (DefinitionAnalyzer.__m_misc_first_words.try_parse(npt.noun.begin_token, TerminParseAttr.NO) is not None): 
                res = MetaToken._new836(t, npt.end_token, npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False))
                res.morph.case_ = MorphCase.NOMINATIVE
                return res
        if (t.is_value("В", None)): 
            npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                if (npt.noun.is_value("СМЫСЛ", None)): 
                    res = MetaToken._new836(t, npt.end_token, MiscHelper.get_text_value(t, npt.end_token, GetTextAttr.NO))
                    res.morph.class0_ = MorphClass.NOUN
                    return res
        return None
    
    @staticmethod
    def __try_parse_list_item(t : 'Token') -> 'MetaToken':
        if (t is None or not t.is_whitespace_before): 
            return None
        tt = None
        pr = 0
        tt = t
        first_pass3634 = True
        while True:
            if first_pass3634: first_pass3634 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_whitespace_before and tt != t): 
                break
            if (isinstance(tt, NumberToken)): 
                pr += 1
                continue
            nex = NumberHelper.try_parse_roman(tt)
            if (nex is not None): 
                pr += 1
                tt = nex.end_token
                continue
            if (not (isinstance(tt, TextToken))): 
                break
            if (not tt.chars.is_letter): 
                if (not tt.is_char('(')): 
                    pr += 1
            elif (tt.length_char > 1 or tt.is_whitespace_after): 
                break
            else: 
                pr += 1
        if (tt is None): 
            return None
        if (pr == 0): 
            if (t.is_char('(')): 
                return None
            if ((isinstance(tt, TextToken)) and tt.chars.is_all_lower): 
                pr += 1
        if (pr == 0): 
            return None
        res = MetaToken(tt, tt)
        while tt is not None: 
            if (tt.is_newline_before and tt != t): 
                break
            else: 
                res.end_token = tt
            tt = tt.next0_
        return res
    
    __m_misc_first_words = None
    
    __m_verbot_first_words = None
    
    __m_verbot_last_words = None
    
    @staticmethod
    def initialize() -> None:
        if (DefinitionAnalyzer.__m_proc0 is not None): 
            return
        MetaDefin.initialize()
        try: 
            DefinitionAnalyzer.__m_proc0 = ProcessorService.create_empty_processor()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            DefinitionAnalyzer.__m_misc_first_words = TerminCollection()
            for s in ["ЧЕРТА", "ХАРАКТЕРИСТИКА", "ОСОБЕННОСТЬ", "СВОЙСТВО", "ПРИЗНАК", "ПРИНЦИП", "РАЗНОВИДНОСТЬ", "ВИД", "ПОКАЗАТЕЛЬ", "ЗНАЧЕНИЕ"]: 
                DefinitionAnalyzer.__m_misc_first_words.add(Termin(s, MorphLang.RU, True))
            DefinitionAnalyzer.__m_verbot_first_words = TerminCollection()
            for s in ["ЦЕЛЬ", "БОЛЬШИНСТВО", "ЧАСТЬ", "ЗАДАЧА", "ИСКЛЮЧЕНИЕ", "ПРИМЕР", "ЭТАП", "ШАГ", "СЛЕДУЮЩИЙ", "ПОДОБНЫЙ", "АНАЛОГИЧНЫЙ", "ПРЕДЫДУЩИЙ", "ПОХОЖИЙ", "СХОЖИЙ", "НАЙДЕННЫЙ", "НАИБОЛЕЕ", "НАИМЕНЕЕ", "ВАЖНЫЙ", "РАСПРОСТРАНЕННЫЙ"]: 
                DefinitionAnalyzer.__m_verbot_first_words.add(Termin(s, MorphLang.RU, True))
            DefinitionAnalyzer.__m_verbot_last_words = TerminCollection()
            for s in ["СТАТЬЯ", "ГЛАВА", "РАЗДЕЛ", "КОДЕКС", "ЗАКОН", "ФОРМУЛИРОВКА", "НАСТОЯЩИЙ", "ВЫШЕУКАЗАННЫЙ", "ДАННЫЙ"]: 
                DefinitionAnalyzer.__m_verbot_last_words.add(Termin(s, MorphLang.RU, True))
            ParenthesisToken.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.register_analyzer(DefinitionAnalyzer())
    
    @staticmethod
    def calc_semantic_coef(text1 : str, text2 : str) -> int:
        """ Вычисление коэффициента семантической близости 2-х текстов.
        Учитываются именные группы (существительные с возможными прилагательными).
        
        Args:
            text1(str): первый текст
            text2(str): второй текст
        
        Returns:
            int: 0 - ничего общего, 100 - полное соответствие (тождество)
        """
        ar1 = DefinitionAnalyzer.__m_proc0.process(SourceOfAnalysis(text1), None, None)
        if (ar1 is None or ar1.first_token is None): 
            return 0
        ar2 = DefinitionAnalyzer.__m_proc0.process(SourceOfAnalysis(text2), None, None)
        if (ar2 is None or ar2.first_token is None): 
            return 0
        terms1 = list()
        terms2 = list()
        for k in range(2):
            terms = (terms1 if k == 0 else terms2)
            t = ((ar1.first_token if k == 0 else ar2.first_token))
            first_pass3635 = True
            while True:
                if first_pass3635: first_pass3635 = False
                else: t = t.next0_
                if (not (t is not None)): break
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    term = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                    if (term is None): 
                        continue
                    if (not term in terms): 
                        terms.append(term)
                    continue
        if (len(terms2) == 0 or len(terms1) == 0): 
            return 0
        coef = 0
        for w in terms1: 
            if (w in terms2): 
                coef += 2
        return math.floor((coef * 100) / ((len(terms1) + len(terms2))))
    
    @staticmethod
    def get_concepts(txt : str, do_normalize_for_english : bool=False) -> typing.List[str]:
        """ Выделить ключевые концепты из текста.
        Концепт - это нормализованная комбинация ключевых слов, причём дериватная нормализация
        (СЛУЖИТЬ -> СЛУЖБА).
        
        Args:
            txt(str): текст
            do_normalize_for_english(bool): делать ли для английского языка нормализацию по дериватам
        
        Returns:
            typing.List[str]: список концептов
        """
        ar = DefinitionAnalyzer.__m_proc0.process(SourceOfAnalysis(txt), None, None)
        res = list()
        tmp = list()
        tmp2 = io.StringIO()
        if (ar is not None): 
            t = ar.first_token
            first_pass3636 = True
            while True:
                if first_pass3636: first_pass3636 = False
                else: t = t.next0_
                if (not (t is not None)): break
                t1 = None
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0, None)
                if (npt is not None): 
                    t1 = npt.end_token
                elif ((isinstance(t, TextToken)) and t.is_pure_verb): 
                    t1 = t
                if (t1 is None): 
                    continue
                tt = t1.next0_
                first_pass3637 = True
                while True:
                    if first_pass3637: first_pass3637 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_and): 
                        npt2 = NounPhraseHelper.try_parse(tt.next0_, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0, None)
                        if (npt2 is not None): 
                            t1 = npt2.end_token
                            tt = t1
                            continue
                        break
                    npt2 = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0, None)
                    if (npt2 is not None): 
                        if (npt2.preposition is not None): 
                            t1 = npt2.end_token
                            tt = t1
                            continue
                        elif (npt2.morph.case_.is_genitive or npt2.morph.case_.is_instrumental): 
                            t1 = npt2.end_token
                            tt = t1
                            continue
                    break
                vars0_ = list()
                tt = t
                first_pass3638 = True
                while True:
                    if first_pass3638: first_pass3638 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= t1.end_char)): break
                    if (not (isinstance(tt, TextToken))): 
                        continue
                    if (tt.is_comma_and or t.morph.class0_.is_preposition): 
                        continue
                    w = tt.lemma
                    if (len(w) < 3): 
                        continue
                    if (tt.chars.is_latin_letter and not do_normalize_for_english): 
                        pass
                    else: 
                        dg = DerivateService.find_derivates(w, True, None)
                        if (dg is not None and len(dg) == 1): 
                            if (len(dg[0].words) > 0): 
                                w = dg[0].words[0].spelling.upper()
                    if (tt.previous is not None and tt.previous.is_comma_and and len(vars0_) > 0): 
                        vars0_[len(vars0_) - 1].append(w)
                    else: 
                        li = list()
                        li.append(w)
                        vars0_.append(li)
                t = t1
                if (len(vars0_) == 0): 
                    continue
                inds = Utils.newArray(len(vars0_), 0)
                while True:
                    tmp.clear()
                    i = 0
                    while i < len(vars0_): 
                        w = vars0_[i][inds[i]]
                        if (not w in tmp): 
                            tmp.append(w)
                        i += 1
                    tmp.sort()
                    Utils.setLengthStringIO(tmp2, 0)
                    i = 0
                    while i < len(tmp): 
                        if (tmp2.tell() > 0): 
                            print(' ', end="", file=tmp2)
                        print(tmp[i], end="", file=tmp2)
                        i += 1
                    ww = Utils.toStringStringIO(tmp2)
                    if (not ww in res): 
                        res.append(ww)
                    for j in range(len(vars0_) - 1, -1, -1):
                        if ((inds[j] + 1) < len(vars0_[j])): 
                            inds[j] += 1
                            break
                        else: 
                            inds[j] = 0
                    else: j = -1
                    if (j < 0): 
                        break
        return res
    
    __m_proc0 = None