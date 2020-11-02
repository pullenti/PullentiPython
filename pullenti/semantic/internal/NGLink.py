# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseToken import NounPhraseToken
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphMood import MorphMood
from pullenti.semantic.utils.QuestionType import QuestionType
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.semantic.internal.NGLinkType import NGLinkType
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.Token import Token
from pullenti.semantic.SemanticService import SemanticService
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.ner.measure.internal.UnitToken import UnitToken
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken

class NGLink(object):
    
    def __init__(self) -> None:
        self.typ = NGLinkType.UNDEFINED
        self.from0_ = None;
        self.to = None;
        self.to_verb = None;
        self.coef = 0
        self.plural = -1
        self.from_is_plural = False
        self.reverce = False
        self.to_all_list_items = False
        self.can_be_pacient = False
        self.can_be_participle = False
        self.alt_link = None;
    
    @property
    def from_morph(self) -> 'MorphCollection':
        if (self.from0_.source.source is not None): 
            return self.from0_.source.source.morph
        return None
    
    @property
    def from_prep(self) -> str:
        return Utils.ifNotNull(self.from0_.source.prep, "")
    
    @property
    def to_morph(self) -> 'MorphCollection':
        if (self.to is not None and self.to.source.source is not None): 
            return self.to.source.source.morph
        return None
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("{0}: {1} ".format(self.coef, Utils.enumToString(self.typ)), end="", file=tmp, flush=True)
        if (self.plural == 1): 
            print(" PLURAL ", end="", file=tmp)
        elif (self.plural == 0): 
            print(" SINGLE ", end="", file=tmp)
        if (self.reverce): 
            print(" REVERCE ", end="", file=tmp)
        print("{0}".format(str(self.from0_.source)), end="", file=tmp, flush=True)
        if (self.to_all_list_items): 
            print(" ALLLISTITEMS ", end="", file=tmp)
        if (self.to is not None): 
            print(" -> {0}".format(str(self.to.source)), end="", file=tmp, flush=True)
        elif (self.to_verb is not None): 
            print(" -> {0}".format(str(self.to_verb)), end="", file=tmp, flush=True)
        if (self.alt_link is not None): 
            print(" / ALTLINK: {0}".format(str(self.alt_link)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def compareTo(self, other : 'NGLink') -> int:
        if (self.coef > other.coef): 
            return -1
        if (self.coef < other.coef): 
            return 1
        return 0
    
    def calc_coef(self, noplural : bool=False) -> None:
        self.coef = (-1)
        self.can_be_pacient = False
        self.to_all_list_items = False
        self.plural = -1
        if (self.typ == NGLinkType.GENETIVE and self.to is not None): 
            self.__calc_genetive()
        elif (self.typ == NGLinkType.NAME and self.to is not None): 
            self.__calc_name(noplural)
        elif (self.typ == NGLinkType.BE and self.to is not None): 
            self.__calc_be()
        elif (self.typ == NGLinkType.LIST): 
            self.__calc_list()
        elif (self.typ == NGLinkType.PARTICIPLE and self.to is not None): 
            self.__calc_participle(noplural)
        elif (self.to_verb is not None and self.to_verb.first_verb is not None): 
            if (self.typ == NGLinkType.AGENT): 
                self.__calc_agent(noplural)
            elif (self.typ == NGLinkType.PACIENT): 
                self.__calc_pacient(noplural)
            elif (self.typ == NGLinkType.ACTANT): 
                self.__calc_actant()
        elif (self.typ == NGLinkType.ADVERB): 
            self.__calc_adverb()
    
    def __calc_genetive(self) -> None:
        if (not self.from0_.source.can_be_noun): 
            return
        if (self.from0_.source.typ == SentItemType.FORMULA): 
            if (self.to.source.typ != SentItemType.NOUN): 
                return
            self.coef = SemanticService.PARAMS.transitive_coef
            return
        frmorph = self.from_morph
        if (self.to.source.typ == SentItemType.FORMULA): 
            if (self.from0_.source.typ != SentItemType.NOUN): 
                return
            if (frmorph.case_.is_genitive): 
                self.coef = SemanticService.PARAMS.transitive_coef
            elif (frmorph.case_.is_undefined): 
                self.coef = (0)
            return
        if (isinstance(self.from0_.source.source, NumbersWithUnitToken)): 
            if (self.from0_.order != (self.to.order + 1)): 
                return
            num = Utils.asObjectOrNull(self.from0_.source.source, NumbersWithUnitToken)
            ki = UnitToken.calc_kind(num.units)
            if (ki != MeasureKind.UNDEFINED): 
                if (UnitsHelper.check_keyword(ki, self.to.source.source)): 
                    self.coef = (SemanticService.PARAMS.next_model * (3))
                    return
            if (isinstance(self.to.source.source, NumbersWithUnitToken)): 
                return
        non_gen_text = False
        if (Utils.isNullOrEmpty(self.from_prep) and not (isinstance(self.from0_.source.source, VerbPhraseToken))): 
            if (self.from0_.order != (self.to.order + 1)): 
                non_gen_text = True
        if (self.to.source.dr_groups is not None): 
            for gr in self.to.source.dr_groups: 
                if (gr.cm.transitive and Utils.isNullOrEmpty(self.from_prep)): 
                    ok = False
                    if (isinstance(self.to.source.source, VerbPhraseToken)): 
                        if (frmorph.case_.is_accusative): 
                            ok = True
                            self.can_be_pacient = True
                    elif (frmorph.case_.is_genitive and self.from0_.order == (self.to.order + 1)): 
                        ok = True
                    if (ok): 
                        self.coef = SemanticService.PARAMS.transitive_coef
                        return
                if ((((gr.cm.questions) & (QuestionType.WHATTODO))) != (QuestionType.UNDEFINED) and (isinstance(self.from0_.source.source, VerbPhraseToken))): 
                    self.coef = SemanticService.PARAMS.transitive_coef
                    return
                if (gr.cm.nexts is not None): 
                    if (self.from_prep in gr.cm.nexts): 
                        cas = gr.cm.nexts[self.from_prep]
                        if (not ((cas) & frmorph.case_).is_undefined): 
                            if (Utils.isNullOrEmpty(self.from_prep) and self.from0_.order != (self.to.order + 1) and ((cas) & frmorph.case_).is_genitive): 
                                pass
                            else: 
                                self.coef = SemanticService.PARAMS.next_model
                                return
        if (non_gen_text or not Utils.isNullOrEmpty(self.from_prep)): 
            return
        cas0 = frmorph.case_
        if (cas0.is_genitive or cas0.is_instrumental or cas0.is_dative): 
            if ((isinstance(self.to.source.source, NumbersWithUnitToken)) and cas0.is_genitive): 
                self.coef = SemanticService.PARAMS.transitive_coef
            else: 
                self.coef = SemanticService.PARAMS.ng_link
                if (cas0.is_nominative or self.from0_.source.typ == SentItemType.PARTBEFORE): 
                    self.coef /= (2)
                if (not cas0.is_genitive): 
                    self.coef /= (2)
        elif (isinstance(self.from0_.source.source, VerbPhraseToken)): 
            self.coef = 0.1
        if ((isinstance(self.to.source.source, NumbersWithUnitToken)) and self.to.source.end_token.is_value("ЧЕМ", None)): 
            self.coef = (SemanticService.PARAMS.transitive_coef * (2))
    
    def __calc_be(self) -> None:
        if (self.to.source.typ != SentItemType.NOUN or self.from0_.source.typ != SentItemType.NOUN): 
            return
        fm = self.from0_.source.source.morph
        tm = self.to.source.source.morph
        if (not ((tm.case_.is_nominative))): 
            return
        if (not Utils.isNullOrEmpty(self.from_prep)): 
            return
        if (isinstance(self.from0_.source.source, NumbersWithUnitToken)): 
            self.coef = SemanticService.PARAMS.transitive_coef
            return
        if (not fm.case_.is_undefined): 
            if (not fm.case_.is_nominative): 
                return
        self.coef = (0)
    
    def __calc_name(self, noplural : bool) -> None:
        if (not Utils.isNullOrEmpty(self.from_prep)): 
            return
        if (not (isinstance(self.from0_.source.source, NounPhraseToken)) or self.from0_.source.typ != SentItemType.NOUN): 
            return
        if (self.from0_.source.begin_token.chars.is_all_lower): 
            return
        if (not (isinstance(self.to.source.source, NounPhraseToken)) or self.to.source.typ != SentItemType.NOUN): 
            return
        if (self.from0_.order != (self.to.order + 1) and not noplural): 
            return
        fm = self.from0_.source.source.morph
        tm = self.to.source.source.morph
        if (not fm.case_.is_undefined and not tm.case_.is_undefined): 
            if (((tm.case_) & fm.case_).is_undefined): 
                return
        if (fm.number == MorphNumber.PLURAL): 
            if (noplural): 
                if (self.from_is_plural): 
                    pass
                elif (((tm.number) & (MorphNumber.SINGULAR)) != (MorphNumber.UNDEFINED)): 
                    return
            self.plural = 1
            self.coef = SemanticService.PARAMS.verb_plural
        else: 
            if (fm.number == MorphNumber.SINGULAR): 
                self.plural = 0
            if (NGLink.__check_morph_accord(fm, False, tm)): 
                self.coef = SemanticService.PARAMS.morph_accord
    
    def __calc_adverb(self) -> None:
        if (self.to_verb is not None): 
            self.coef = (1)
        elif (self.to is None): 
            return
        elif (self.to.source.typ == SentItemType.ADVERB): 
            self.coef = (1)
        else: 
            self.coef = 0.5
    
    def __calc_list(self) -> None:
        cas0 = self.from_morph.case_
        if (self.to is None): 
            if (self.to_verb is None): 
                return
            return
        if (self.from0_.source.typ != self.to.source.typ): 
            if (self.from0_.source.prep == self.to.source.prep and ((self.from0_.source.typ == SentItemType.NOUN or self.from0_.source.typ == SentItemType.PARTBEFORE or self.from0_.source.typ == SentItemType.PARTAFTER)) and ((self.to.source.typ == SentItemType.NOUN or self.to.source.typ == SentItemType.PARTBEFORE or self.to.source.typ == SentItemType.PARTAFTER))): 
                pass
            else: 
                return
        cas1 = self.to_morph.case_
        if (not ((cas0) & cas1).is_undefined): 
            self.coef = SemanticService.PARAMS.list0_
            if (Utils.isNullOrEmpty(self.from_prep) and not Utils.isNullOrEmpty(self.to.source.prep)): 
                self.coef /= (2)
            elif (not Utils.isNullOrEmpty(self.from_prep) and Utils.isNullOrEmpty(self.to.source.prep)): 
                self.coef /= (4)
        else: 
            if (not cas0.is_undefined and not cas1.is_undefined): 
                return
            if (not Utils.isNullOrEmpty(self.from_prep) and Utils.isNullOrEmpty(self.to.source.prep)): 
                return
            self.coef = SemanticService.PARAMS.list0_
        t1 = Utils.asObjectOrNull(self.from0_.source.end_token, TextToken)
        t2 = Utils.asObjectOrNull(self.to.source.end_token, TextToken)
        if (t1 is not None and t2 is not None): 
            if (t1.is_value(t2.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False), None)): 
                self.coef *= (10)
        if (self.from0_.source.typ != self.to.source.typ): 
            self.coef /= (2)
    
    def __calc_participle(self, noplural : bool) -> float:
        fm = self.from0_.source.source.morph
        tm = self.to.source.source.morph
        if (self.to.source.typ == SentItemType.PARTBEFORE): 
            self.coef = -1
            return self.coef
        if (self.from0_.source.typ == SentItemType.DEEPART): 
            if (not Utils.isNullOrEmpty(self.to.source.prep)): 
                self.coef = -1
                return self.coef
            if (tm.case_.is_nominative): 
                self.coef = SemanticService.PARAMS.morph_accord
                return self.coef
            if (tm.case_.is_undefined): 
                self.coef = 0
                return self.coef
            self.coef = -1
            return self.coef
        if (self.from0_.source.typ != SentItemType.PARTBEFORE and self.from0_.source.typ != SentItemType.SUBSENT): 
            self.coef = -1
            return self.coef
        if (not fm.case_.is_undefined and not tm.case_.is_undefined): 
            if (((fm.case_) & tm.case_).is_undefined): 
                if (self.from0_.source.typ == SentItemType.PARTBEFORE): 
                    self.coef = -1
                    return self.coef
        if (fm.number == MorphNumber.PLURAL): 
            if (noplural): 
                if (self.from_is_plural): 
                    pass
                elif (((tm.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED)): 
                    self.coef = -1
                    return self.coef
            self.plural = 1
            self.coef = SemanticService.PARAMS.verb_plural
        else: 
            if (fm.number == MorphNumber.SINGULAR): 
                self.plural = 0
            if (len(fm.items) > 0): 
                for wf in fm.items: 
                    if (NGLink.__check_morph_accord(tm, False, wf)): 
                        self.coef = SemanticService.PARAMS.morph_accord
                        if (tm.gender != MorphGender.UNDEFINED and wf.gender != MorphGender.UNDEFINED): 
                            if (((tm.gender) & (wf.gender)) == (MorphGender.UNDEFINED)): 
                                self.coef /= (2)
                        break
        return self.coef
    
    def __calc_agent(self, noplural : bool) -> float:
        if (not Utils.isNullOrEmpty(self.from_prep)): 
            self.coef = -1
            return self.coef
        vf = self.to_verb.first_verb.verb_morph
        if (vf is None): 
            self.coef = -1
            return self.coef
        vf2 = self.to_verb.last_verb.verb_morph
        if (vf2 is None): 
            self.coef = -1
            return self.coef
        if (vf.misc.mood == MorphMood.IMPERATIVE): 
            self.coef = -1
            return self.coef
        morph_ = self.from_morph
        if (vf2.misc.voice == MorphVoice.PASSIVE or self.to_verb.last_verb.morph.contains_attr("страд.з.", None)): 
            if (not morph_.case_.is_undefined): 
                if (morph_.case_.is_instrumental): 
                    self.coef = SemanticService.PARAMS.transitive_coef
                    if (vf2.case_.is_instrumental): 
                        self.coef /= (2)
                    return self.coef
                self.coef = -1
                return self.coef
            self.coef = 0
            return self.coef
        if ("инф." in vf.misc.attrs): 
            self.coef = -1
            return self.coef
        if (NGLink.__is_rev_verb(vf2)): 
            ag_case = MorphCase.UNDEFINED
            grs = DerivateService.find_derivates(Utils.ifNotNull(vf2.normal_full, vf2.normal_case), True, None)
            if (grs is not None): 
                for gr in grs: 
                    if (gr.cm_rev.agent is not None): 
                        ag_case = gr.cm_rev.agent.case_
                        break
            if (not morph_.case_.is_undefined): 
                if (ag_case.is_dative): 
                    if (morph_.case_.is_dative): 
                        self.coef = SemanticService.PARAMS.transitive_coef
                        if (morph_.case_.is_genitive): 
                            self.coef /= (2)
                        return self.coef
                    self.coef = -1
                    return self.coef
                if (ag_case.is_instrumental): 
                    if (morph_.case_.is_instrumental): 
                        if (morph_.case_.is_nominative): 
                            self.coef = 0
                            return self.coef
                        self.coef = SemanticService.PARAMS.transitive_coef
                        return self.coef
                    self.coef = -1
                    return self.coef
                if (not morph_.case_.is_nominative): 
                    self.coef = -1
                    return self.coef
            else: 
                self.coef = 0
                return self.coef
        if (vf.number == MorphNumber.PLURAL): 
            if (not morph_.case_.is_undefined): 
                if (vf.case_.is_undefined): 
                    if (not morph_.case_.is_nominative): 
                        self.coef = -1
                        return self.coef
                elif (((vf.case_) & morph_.case_).is_undefined): 
                    self.coef = -1
                    return self.coef
            if (noplural): 
                if (self.from_is_plural): 
                    pass
                elif (((morph_.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED)): 
                    self.coef = -1
                    return self.coef
                elif (not NGLink.__check_morph_accord(morph_, False, vf)): 
                    self.coef = -1
                    return self.coef
                elif (len(morph_.items) > 0 and not vf.case_.is_undefined): 
                    ok = False
                    for it in morph_.items: 
                        if (((it.number) & (MorphNumber.PLURAL)) == (MorphNumber.PLURAL)): 
                            if (not it.case_.is_undefined and ((it.case_) & vf.case_).is_undefined): 
                                continue
                            ok = True
                            break
                    if (not ok): 
                        self.coef = -1
                        return self.coef
            self.plural = 1
            self.coef = SemanticService.PARAMS.verb_plural
            if (vf2.normal_case == "БЫТЬ"): 
                if (morph_.case_.is_undefined and self.from0_.source.begin_token.begin_char > self.to_verb.end_char): 
                    self.coef /= (2)
        else: 
            if (vf.number == MorphNumber.SINGULAR): 
                self.plural = 0
                if (self.from_is_plural): 
                    self.coef = -1
                    return self.coef
            if (not NGLink.__check_morph_accord(morph_, False, vf)): 
                self.coef = -1
                return self.coef
            if (not morph_.case_.is_undefined): 
                if (not morph_.case_.is_nominative): 
                    if (self.to_verb.first_verb.is_participle): 
                        pass
                    else: 
                        self.coef = -1
                        return self.coef
            if (vf.misc.person != MorphPerson.UNDEFINED): 
                if (((vf.misc.person) & (MorphPerson.THIRD)) == (MorphPerson.UNDEFINED)): 
                    if (((vf.misc.person) & (MorphPerson.FIRST)) == (MorphPerson.FIRST)): 
                        if (not morph_.contains_attr("1 л.", None)): 
                            self.coef = -1
                            return self.coef
                    if (((vf.misc.person) & (MorphPerson.SECOND)) == (MorphPerson.SECOND)): 
                        if (not morph_.contains_attr("2 л.", None)): 
                            self.coef = -1
                            return self.coef
            self.coef = SemanticService.PARAMS.morph_accord
            if (morph_.case_.is_undefined): 
                self.coef /= (4)
        return self.coef
    
    @staticmethod
    def __is_rev_verb(vf : 'MorphWordForm') -> bool:
        if ("возвр." in vf.misc.attrs): 
            return True
        if (vf.normal_case is not None): 
            if (vf.normal_case.endswith("СЯ") or vf.normal_case.endswith("СЬ")): 
                return True
        return False
    
    def __calc_pacient(self, noplural : bool) -> float:
        if (not Utils.isNullOrEmpty(self.from_prep)): 
            self.coef = -1
            return self.coef
        vf = self.to_verb.first_verb.verb_morph
        if (vf is None): 
            return -1
        vf2 = self.to_verb.last_verb.verb_morph
        if (vf2 is None): 
            return -1
        morph_ = self.from_morph
        if (vf2.misc.voice == MorphVoice.PASSIVE or self.to_verb.last_verb.morph.contains_attr("страд.з.", None)): 
            if (vf.number == MorphNumber.PLURAL): 
                if (noplural): 
                    if (self.from_is_plural): 
                        pass
                    elif (not NGLink.__check_morph_accord(morph_, False, vf)): 
                        return -1
                    elif (len(morph_.items) > 0 and not vf.case_.is_undefined): 
                        ok = False
                        for it in morph_.items: 
                            if (((it.number) & (MorphNumber.PLURAL)) == (MorphNumber.PLURAL)): 
                                if (not it.case_.is_undefined and ((it.case_) & vf.case_).is_undefined): 
                                    continue
                                ok = True
                                break
                        if (not ok): 
                            self.coef = -1
                            return self.coef
                self.coef = SemanticService.PARAMS.verb_plural
                self.plural = 1
            else: 
                if (vf.number == MorphNumber.SINGULAR): 
                    self.plural = 0
                    if (self.from_is_plural): 
                        return -1
                if (not NGLink.__check_morph_accord(morph_, False, vf)): 
                    return -1
                self.coef = SemanticService.PARAMS.morph_accord
            return self.coef
        is_trans = False
        is_ref_dative = False
        grs = DerivateService.find_derivates(Utils.ifNotNull(vf2.normal_full, vf2.normal_case), True, None)
        if (grs is not None): 
            for gr in grs: 
                if (gr.cm.transitive): 
                    is_trans = True
                if (gr.cm_rev.agent is not None and not gr.cm_rev.agent.case_.is_nominative): 
                    is_ref_dative = True
        if (NGLink.__is_rev_verb(vf2)): 
            if (not Utils.isNullOrEmpty(self.from_prep)): 
                return -1
            if (not morph_.case_.is_undefined): 
                if (is_ref_dative): 
                    if (morph_.case_.is_nominative): 
                        self.coef = SemanticService.PARAMS.transitive_coef
                        return self.coef
                elif (morph_.case_.is_instrumental): 
                    self.coef = SemanticService.PARAMS.transitive_coef
                    return self.coef
                return -1
            self.coef = 0
            return self.coef
        if (vf2 != vf and not is_trans): 
            grs = DerivateService.find_derivates(Utils.ifNotNull(vf.normal_full, vf.normal_case), True, None)
            if (grs is not None): 
                for gr in grs: 
                    if (gr.cm.transitive): 
                        is_trans = True
        if (is_trans): 
            if (not Utils.isNullOrEmpty(self.from_prep)): 
                return -1
            if (not morph_.case_.is_undefined): 
                if (morph_.case_.is_accusative): 
                    self.coef = SemanticService.PARAMS.transitive_coef
                    if (morph_.case_.is_dative): 
                        self.coef /= (2)
                    if (morph_.case_.is_genitive): 
                        self.coef /= (2)
                    if (morph_.case_.is_instrumental): 
                        self.coef /= (2)
                    return self.coef
                else: 
                    return -1
        if (vf2.normal_case == "БЫТЬ"): 
            if (not Utils.isNullOrEmpty(self.from_prep)): 
                return -1
            if (morph_.case_.is_instrumental): 
                self.coef = SemanticService.PARAMS.transitive_coef
                return self.coef
            if (morph_.case_.is_nominative): 
                if (self.from0_.source.begin_token.begin_char > self.to_verb.end_char): 
                    self.coef = SemanticService.PARAMS.transitive_coef
                    return self.coef
                else: 
                    self.coef = SemanticService.PARAMS.transitive_coef / (2)
                    return self.coef
            if (morph_.case_.is_undefined): 
                self.coef = SemanticService.PARAMS.transitive_coef / (2)
                return self.coef
        return -1
    
    def __calc_actant(self) -> float:
        if (self.can_be_participle): 
            self.coef = -1
            return self.coef
        vf2 = self.to_verb.last_verb.verb_morph
        if (vf2 is None): 
            return -1
        if (self.from_prep is None): 
            self.coef = 0
            return self.coef
        fm = self.from0_.source.source.morph
        grs = DerivateService.find_derivates(Utils.ifNotNull(vf2.normal_full, vf2.normal_case), True, None)
        if (grs is not None): 
            for gr in grs: 
                if (gr.cm.nexts is None or not self.from_prep in gr.cm.nexts): 
                    continue
                cas = gr.cm.nexts[self.from_prep]
                if (not ((cas) & fm.case_).is_undefined): 
                    self.coef = SemanticService.PARAMS.next_model
                    if (Utils.isNullOrEmpty(self.from_prep)): 
                        if (fm.case_.is_nominative): 
                            self.coef /= (2)
                        self.coef /= (2)
                    return self.coef
                if (self.from0_.source.source.morph.case_.is_undefined): 
                    self.coef = 0
                    return self.coef
        self.coef = 0.1
        return self.coef
    
    @staticmethod
    def __check_morph_accord(m : 'MorphCollection', plural_ : bool, vf : 'MorphBaseInfo') -> bool:
        coef_ = 0
        if (vf.number == MorphNumber.PLURAL): 
            if (plural_): 
                coef_ += 1
            elif (m.number != MorphNumber.UNDEFINED): 
                if (((m.number) & (MorphNumber.PLURAL)) == (MorphNumber.PLURAL)): 
                    coef_ += 1
                else: 
                    return False
        elif (vf.number == MorphNumber.SINGULAR): 
            if (plural_): 
                return False
            if (m.number != MorphNumber.UNDEFINED): 
                if (((m.number) & (MorphNumber.SINGULAR)) == (MorphNumber.SINGULAR)): 
                    coef_ += 1
                else: 
                    return False
            if (m.gender != MorphGender.UNDEFINED): 
                if (vf.gender != MorphGender.UNDEFINED): 
                    if (m.gender == MorphGender.FEMINIE): 
                        if (((vf.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                            coef_ += 1
                        else: 
                            return False
                    elif (((m.gender) & (vf.gender)) != (MorphGender.UNDEFINED)): 
                        coef_ += 1
                    elif (m.gender == MorphGender.MASCULINE and vf.gender == MorphGender.FEMINIE): 
                        pass
                    else: 
                        return False
        return coef_ >= 0
    
    @staticmethod
    def _new2924(_arg1 : 'NGLinkType', _arg2 : 'NGItem', _arg3 : 'NGItem', _arg4 : bool) -> 'NGLink':
        res = NGLink()
        res.typ = _arg1
        res.from0_ = _arg2
        res.to = _arg3
        res.reverce = _arg4
        return res
    
    @staticmethod
    def _new2926(_arg1 : 'NGLinkType') -> 'NGLink':
        res = NGLink()
        res.typ = _arg1
        return res
    
    @staticmethod
    def _new2927(_arg1 : 'NGItem', _arg2 : 'NGLinkType') -> 'NGLink':
        res = NGLink()
        res.from0_ = _arg1
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new2935(_arg1 : 'NGItem', _arg2 : 'VerbPhraseToken', _arg3 : 'NGLinkType') -> 'NGLink':
        res = NGLink()
        res.from0_ = _arg1
        res.to_verb = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2951(_arg1 : 'NGLinkType', _arg2 : 'NGItem', _arg3 : 'VerbPhraseToken') -> 'NGLink':
        res = NGLink()
        res.typ = _arg1
        res.from0_ = _arg2
        res.to_verb = _arg3
        return res