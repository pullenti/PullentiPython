# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.SemLinkType import SemLinkType
from pullenti.semantic.SemQuantity import SemQuantity
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.semantic.SemAttributeType import SemAttributeType
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphAspect import MorphAspect
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.semantic.internal.AdverbToken import AdverbToken
from pullenti.semantic.SemAttribute import SemAttribute
from pullenti.semantic.SemObjectType import SemObjectType
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.TextToken import TextToken
from pullenti.semantic.SemObject import SemObject
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.ner.core.NumberHelper import NumberHelper

class CreateHelper:
    
    @staticmethod
    def _set_morph(obj : 'SemObject', wf : 'MorphWordForm') -> None:
        if (wf is None): 
            return
        obj.morph.normal_case = wf.normal_case
        obj.morph.normal_full = (Utils.ifNotNull(wf.normal_full, wf.normal_case))
        obj.morph.number = wf.number
        obj.morph.gender = wf.gender
        obj.morph.misc = wf.misc
    
    @staticmethod
    def _set_morph0(obj : 'SemObject', bi : 'MorphBaseInfo') -> None:
        obj.morph.number = bi.number
        obj.morph.gender = bi.gender
    
    @staticmethod
    def create_noun_group(gr : 'SemGraph', npt : 'NounPhraseToken') -> 'SemObject':
        noun = npt.noun.begin_token
        sem = SemObject(gr)
        sem.tokens.append(npt.noun)
        sem.typ = SemObjectType.NOUN
        if (npt.noun.morph.class0_.is_personal_pronoun): 
            sem.typ = SemObjectType.PERSONALPRONOUN
        elif (npt.noun.morph.class0_.is_pronoun): 
            sem.typ = SemObjectType.PRONOUN
        if (npt.noun.begin_token != npt.noun.end_token): 
            sem.morph.normal_case = npt.noun.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
            sem.morph.normal_full = npt.noun.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
            sem.morph.class0_ = MorphClass.NOUN
            sem.morph.number = npt.morph.number
            sem.morph.gender = npt.morph.gender
            sem.morph.case_ = npt.morph.case_
        elif (isinstance(noun, TextToken)): 
            for wf in noun.morph.items: 
                if (wf.check_accord(npt.morph, False, False) and (isinstance(wf, MorphWordForm))): 
                    CreateHelper._set_morph(sem, Utils.asObjectOrNull(wf, MorphWordForm))
                    break
            if (sem.morph.normal_case is None): 
                sem.morph.normal_case = noun.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                sem.morph.normal_full = noun.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
            grs = DerivateService.find_derivates(sem.morph.normal_full, True, None)
            if (grs is not None and len(grs) > 0): 
                sem.concept = (grs[0])
        elif (isinstance(noun, ReferentToken)): 
            r = noun.referent
            if (r is None): 
                return None
            sem.morph.normal_case = str(r)
            sem.morph.normal_full = sem.morph.normal_case
            sem.concept = (r)
        elif (isinstance(noun, NumberToken)): 
            num = Utils.asObjectOrNull(noun, NumberToken)
            sem.morph.gender = noun.morph.gender
            sem.morph.number = noun.morph.number
            if (num.int_value is not None): 
                sem.morph.normal_case = NumberHelper.get_number_adjective(num.int_value, noun.morph.gender, noun.morph.number)
                sem.morph.normal_full = NumberHelper.get_number_adjective(num.int_value, MorphGender.MASCULINE, MorphNumber.SINGULAR)
            else: 
                sem.morph.normal_case = noun.get_source_text().upper()
                sem.morph.normal_full = sem.morph.normal_case
        noun.tag = (sem)
        if (len(npt.adjectives) > 0): 
            for a in npt.adjectives: 
                if (npt.multi_nouns and a != npt.adjectives[0]): 
                    break
                asem = CreateHelper.create_npt_adj(gr, npt, a)
                if (asem is not None): 
                    gr.add_link(SemLinkType.DETAIL, sem, asem, "какой", False, None)
        if (npt.internal_noun is not None): 
            intsem = CreateHelper.create_noun_group(gr, npt.internal_noun)
            if (intsem is not None): 
                gr.add_link(SemLinkType.DETAIL, sem, intsem, None, False, None)
        gr.objects.append(sem)
        return sem
    
    @staticmethod
    def create_number(gr : 'SemGraph', num : 'NumbersWithUnitToken') -> 'SemObject':
        rs = num.create_refenets_tokens_with_register(None, None, False)
        if (rs is None or len(rs) == 0): 
            return None
        mr = Utils.asObjectOrNull(rs[len(rs) - 1].referent, MeasureReferent)
        sem = SemObject(gr)
        gr.objects.append(sem)
        sem.tokens.append(num)
        sem.morph.normal_case = mr.to_string(True, None, 0)
        sem.morph.normal_full = sem.morph.normal_case
        sem.typ = SemObjectType.NOUN
        sem.measure = mr.kind
        i = 0
        first_pass3930 = True
        while True:
            if first_pass3930: first_pass3930 = False
            else: i += 1
            if (not (i < len(sem.morph.normal_case))): break
            ch = sem.morph.normal_case[i]
            if (str.isdigit(ch) or Utils.isWhitespace(ch) or "[].+-".find(ch) >= 0): 
                continue
            sem.quantity = SemQuantity(sem.morph.normal_case[0:0+i].strip(), num.begin_token, num.end_token)
            sem.morph.normal_case = sem.morph.normal_case[i:].strip()
            if (len(num.units) == 1 and num.units[0].unit is not None): 
                sem.morph.normal_full = num.units[0].unit.fullname_cyr
                if (sem.morph.normal_full == "%"): 
                    sem.morph.normal_full = "процент"
            break
        sem.concept = (mr)
        return sem
    
    @staticmethod
    def create_adverb(gr : 'SemGraph', adv : 'AdverbToken') -> 'SemObject':
        res = SemObject(gr)
        gr.objects.append(res)
        res.tokens.append(adv)
        res.typ = SemObjectType.ADVERB
        res.not0_ = adv.not0_
        res.morph.normal_full = adv.spelling
        res.morph.normal_case = res.morph.normal_full
        grs = DerivateService.find_derivates(res.morph.normal_full, True, None)
        if (grs is not None and len(grs) > 0): 
            res.concept = (grs[0])
        return res
    
    @staticmethod
    def create_npt_adj(gr : 'SemGraph', npt : 'NounPhraseToken', a : 'MetaToken') -> 'SemObject':
        if (a.morph.class0_.is_pronoun): 
            asem = SemObject(gr)
            gr.objects.append(asem)
            asem.tokens.append(a)
            asem.typ = (SemObjectType.PERSONALPRONOUN if a.begin_token.morph.class0_.is_personal_pronoun else SemObjectType.PRONOUN)
            for it in a.begin_token.morph.items: 
                wf = Utils.asObjectOrNull(it, MorphWordForm)
                if (wf is None): 
                    continue
                if (not npt.morph.case_.is_undefined): 
                    if (((npt.morph.case_) & wf.case_).is_undefined): 
                        continue
                CreateHelper._set_morph(asem, wf)
                if (asem.morph.normal_full == "КАКОВ"): 
                    asem.morph.normal_full = "КАКОЙ"
                break
            if (asem.morph.normal_full is None): 
                asem.morph.normal_case = a.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                asem.morph.normal_full = asem.morph.normal_case
            return asem
        if (not a.morph.class0_.is_verb): 
            asem = SemObject(gr)
            gr.objects.append(asem)
            asem.tokens.append(a)
            asem.typ = SemObjectType.ADJECTIVE
            for wf in a.begin_token.morph.items: 
                if (wf.check_accord(npt.morph, False, False) and wf.class0_.is_adjective and (isinstance(wf, MorphWordForm))): 
                    CreateHelper._set_morph(asem, Utils.asObjectOrNull(wf, MorphWordForm))
                    break
            if (asem.morph.normal_case is None): 
                asem.morph.normal_case = a.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                asem.morph.normal_full = a.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE, False)
                CreateHelper._set_morph0(asem, a.begin_token.morph)
            grs = DerivateService.find_derivates(asem.morph.normal_full, True, None)
            if (grs is not None and len(grs) > 0): 
                asem.concept = (grs[0])
            return asem
        return None
    
    @staticmethod
    def create_verb_group(gr : 'SemGraph', vpt : 'VerbPhraseToken') -> 'SemObject':
        sems = list()
        attrs = list()
        adverbs = list()
        i = 0
        first_pass3931 = True
        while True:
            if first_pass3931: first_pass3931 = False
            else: i += 1
            if (not (i < len(vpt.items))): break
            v = vpt.items[i]
            if (v.is_adverb): 
                adv = AdverbToken.try_parse(v.begin_token)
                if (adv is None): 
                    continue
                if (adv.typ != SemAttributeType.UNDEFINED): 
                    attrs.append(SemAttribute._new2908(adv.not0_, adv.typ, adv.spelling))
                    continue
                adverb = CreateHelper.create_adverb(gr, adv)
                if (len(attrs) > 0): 
                    adverb.attrs.extend(attrs)
                    attrs.clear()
                adverbs.append(adverb)
                continue
            if (v.normal == "БЫТЬ"): 
                j = (i + 1)
                while j < len(vpt.items): 
                    if (not vpt.items[j].is_adverb): 
                        break
                    j += 1
                if (j < len(vpt.items)): 
                    continue
            sem = SemObject(gr)
            gr.objects.append(sem)
            sem.tokens.append(v)
            v.tag = (sem)
            CreateHelper._set_morph(sem, v.verb_morph)
            sem.morph.normal_full = v.normal
            sem.morph.normal_case = sem.morph.normal_full
            if (v.is_participle or v.is_dee_participle): 
                sem.typ = SemObjectType.PARTICIPLE
                sem.morph.normal_full = (Utils.ifNotNull(v.end_token.get_normal_case_text(MorphClass.VERB, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), (sem.morph.normal_case if sem is not None and sem.morph is not None else None)))
                sem.morph.normal_case = v.end_token.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                if (sem.morph.normal_case == sem.morph.normal_full and v.normal.endswith("Й")): 
                    grs2 = DerivateService.find_derivates(v.normal, True, None)
                    if (grs2 is not None): 
                        for g in grs2: 
                            for w in g.words: 
                                if (w.lang == v.end_token.morph.language and w.class0_.is_verb and not w.class0_.is_adjective): 
                                    sem.morph.normal_full = w.spelling
                                    break
                elif (sem.morph.normal_case == sem.morph.normal_full and v.is_participle and sem.morph.normal_full.endswith("Ь")): 
                    for it in v.end_token.morph.items: 
                        wf = Utils.asObjectOrNull(it, MorphWordForm)
                        if (wf is None): 
                            continue
                        if (wf.normal_case.endswith("Й") or ((wf.normal_full is not None and wf.normal_full.endswith("Й")))): 
                            sem.morph.normal_case = (Utils.ifNotNull(wf.normal_full, wf.normal_case))
                            break
                    if (sem.morph.normal_case == sem.morph.normal_full): 
                        grs2 = DerivateService.find_derivates(sem.morph.normal_case, True, None)
                        if (grs2 is not None): 
                            for g in grs2: 
                                for w in g.words: 
                                    if (w.lang == v.end_token.morph.language and w.class0_.is_verb and w.class0_.is_adjective): 
                                        sem.morph.normal_case = w.spelling
                                        break
                                break
            else: 
                sem.typ = SemObjectType.VERB
            if (v.verb_morph is not None and v.verb_morph.contains_attr("возвр.", None)): 
                if (sem.morph.normal_full.endswith("СЯ") or sem.morph.normal_full.endswith("СЬ")): 
                    sem.morph.normal_full = sem.morph.normal_full[0:0+len(sem.morph.normal_full) - 2]
            grs = DerivateService.find_derivates(sem.morph.normal_full, True, None)
            if (grs is not None and len(grs) > 0): 
                sem.concept = (grs[0])
                if (v.verb_morph is not None and v.verb_morph.misc.aspect == MorphAspect.IMPERFECTIVE): 
                    for w in grs[0].words: 
                        if (w.class0_.is_verb and not w.class0_.is_adjective): 
                            if (w.aspect == MorphAspect.PERFECTIVE): 
                                sem.morph.normal_full = w.spelling
                                break
            sem.not0_ = v.not0_
            sems.append(sem)
            if (len(attrs) > 0): 
                sem.attrs.extend(attrs)
                attrs.clear()
            if (len(adverbs) > 0): 
                for a in adverbs: 
                    gr.add_link(SemLinkType.DETAIL, sem, a, "как", False, None)
            adverbs.clear()
        if (len(sems) == 0): 
            return None
        if (len(attrs) > 0): 
            sems[len(sems) - 1].attrs.extend(attrs)
        if (len(adverbs) > 0): 
            sem = sems[len(sems) - 1]
            for a in adverbs: 
                gr.add_link(SemLinkType.DETAIL, sem, a, "как", False, None)
        for i in range(len(sems) - 1, 0, -1):
            gr.add_link(SemLinkType.DETAIL, sems[i - 1], sems[i], "что делать", False, None)
        return sems[0]
    
    @staticmethod
    def create_question(li : 'NGItem') -> str:
        res = (Utils.ifNotNull(li.source.prep, "")).lower()
        if (len(res) > 0): 
            res += " "
        cas = li.source.source.morph.case_
        if (not Utils.isNullOrEmpty(li.source.prep)): 
            cas1 = LanguageHelper.get_case_after_preposition(li.source.prep)
            if (not cas1.is_undefined): 
                if (not ((cas1) & cas).is_undefined): 
                    cas = ((cas) & cas1)
        if (cas.is_genitive): 
            res += "чего"
        elif (cas.is_instrumental): 
            res += "чем"
        elif (cas.is_dative): 
            res += "чему"
        elif (cas.is_accusative): 
            res += "что"
        elif (cas.is_prepositional): 
            res += "чём"
        return res