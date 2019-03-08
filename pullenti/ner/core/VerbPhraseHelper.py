# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.VerbPhraseItemToken import VerbPhraseItemToken
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Token import Token
from pullenti.morph.Morphology import Morphology
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.ner.core.PrepositionHelper import PrepositionHelper
from pullenti.morph.Explanatory import Explanatory

class VerbPhraseHelper:
    """ Работа с глагольными группами (последовательность из глаголов и наречий) """
    
    @staticmethod
    def try_parse(t : 'Token', can_be_partition : bool=False) -> 'VerbPhraseToken':
        """ Создать глагольную группу
        
        Args:
            t(Token): первый токен группы
            can_be_partition(bool): выделять ли причастия
        
        Returns:
            VerbPhraseToken: группа или null
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        if (not t.chars.is_letter0): 
            return None
        if (t.chars.is_cyrillic_letter0): 
            return VerbPhraseHelper.__try_parse_ru(t, can_be_partition)
        return None
    
    @staticmethod
    def __try_parse_ru(t : 'Token', can_be_partition : bool) -> 'VerbPhraseToken':
        res = None
        t0 = t
        not0_ = None
        has_verb = False
        verb_be_before = False
        norm = None
        prep = None
        first_pass2920 = True
        while True:
            if first_pass2920: first_pass2920 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not ((isinstance(t, TextToken)))): 
                break
            tt = Utils.asObjectOrNull(t, TextToken)
            is_participle = False
            if (tt.term == "НЕ"): 
                not0_ = t
                continue
            ty = 0
            mc = tt.get_morph_class_in_dictionary()
            if (tt.term == "НЕТ"): 
                if (has_verb): 
                    break
                ty = 1
            elif (mc.is_adverb0): 
                ty = 2
            elif (tt.is_pure_verb0 or tt.is_verb_be0): 
                ty = 1
                if (has_verb): 
                    if (not tt.morph.contains_attr("инф.", None)): 
                        if (verb_be_before): 
                            pass
                        else: 
                            break
            elif (mc.is_verb0): 
                if (mc.is_preposition0 or mc.is_misc0 or mc.is_pronoun0): 
                    pass
                elif (mc.is_noun0): 
                    if (tt.term == "СТАЛИ" or tt.term == "СТЕКЛО" or tt.term == "БЫЛИ"): 
                        ty = 1
                    elif (not tt.chars.is_all_lower0 and not MiscHelper.can_be_start_of_sentence(tt)): 
                        ty = 1
                    elif (mc.is_adjective0 and can_be_partition): 
                        ty = 1
                elif (mc.is_proper0): 
                    if (tt.chars.is_all_lower0): 
                        ty = 1
                else: 
                    ty = 1
                if (mc.is_adjective0): 
                    is_participle = True
                if (not tt.morph.case_.is_undefined0): 
                    is_participle = True
                if (not can_be_partition and is_participle): 
                    break
                if (has_verb): 
                    if (not tt.morph.contains_attr("инф.", None) or is_participle): 
                        break
            elif (mc.is_adjective0 and can_be_partition): 
                if (tt.morph.contains_attr("к.ф.", None)): 
                    break
                norm = tt.get_normal_case_text(MorphClass.ADJECTIVE, True, MorphGender.MASCULINE, False)
                if (norm.endswith("ЙШИЙ")): 
                    pass
                else: 
                    grs = Explanatory.find_derivates(norm, True, None)
                    if (grs is not None and len(grs) > 0): 
                        hverb = False
                        hpart = False
                        for gr in grs: 
                            for w in gr.words: 
                                if (w.class0_.is_adjective0 and w.class0_.is_verb0): 
                                    if (w.spelling == norm): 
                                        hpart = True
                                elif (w.class0_.is_verb0): 
                                    hverb = True
                        if (hpart and hverb): 
                            ty = 3
                        if (ty != 3 and not Utils.isNullOrEmpty(grs[0].prefix) and norm.startswith(grs[0].prefix)): 
                            hverb = False
                            hpart = False
                            norm1 = norm[len(grs[0].prefix):]
                            grs = Explanatory.find_derivates(norm1, True, None)
                            if (grs is not None and len(grs) > 0): 
                                for gr in grs: 
                                    for w in gr.words: 
                                        if (w.class0_.is_adjective0 and w.class0_.is_verb0): 
                                            if (w.spelling == norm1): 
                                                hpart = True
                                        elif (w.class0_.is_verb0): 
                                            hverb = True
                            if (hpart and hverb): 
                                ty = 3
            if (ty == 0 and t == t0 and can_be_partition): 
                prep = PrepositionHelper.try_parse(t)
                if (prep is not None): 
                    t = prep.end_token
                    continue
            if (ty == 0): 
                break
            if (res is None): 
                res = VerbPhraseToken(t0, t)
            res.end_token = t
            it = VerbPhraseItemToken._new656(t, t, MorphCollection(t.morph))
            if (not0_ is not None): 
                it.begin_token = not0_
                it.not0_ = True
                not0_ = (None)
            it.is_adverb = ty == 2
            if (prep is not None and not t.morph.case_.is_undefined0 and len(res.items) == 0): 
                if (((prep.next_case) & t.morph.case_).is_undefined0): 
                    return None
                it.morph.remove_items(prep.next_case, False)
                res.preposition = prep
            if (norm is None): 
                norm = t.get_normal_case_text((MorphClass.ADJECTIVE if ty == 3 else (MorphClass.ADVERB if ty == 2 else MorphClass.VERB)), True, MorphGender.MASCULINE, False)
                if (ty == 1 and not tt.morph.case_.is_undefined0): 
                    mi = MorphWordForm._new657(MorphCase.NOMINATIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE)
                    for mit in tt.morph.items: 
                        if (isinstance(mit, MorphWordForm)): 
                            mi.misc = (mit).misc
                            break
                    nnn = Morphology.get_wordform("КК" + (t).term, mi)
                    if (nnn is not None): 
                        norm = nnn[2:]
            it.normal = norm
            res.items.append(it)
            if (not has_verb and ((ty == 1 or ty == 3))): 
                res.morph = it.morph
                has_verb = True
            if (ty == 1 or ty == 3): 
                if (ty == 1 and tt.is_verb_be0): 
                    verb_be_before = True
                else: 
                    verb_be_before = False
        if (not has_verb): 
            return None
        for i in range(len(res.items) - 1, 0, -1):
            if (res.items[i].is_adverb): 
                del res.items[i]
                res.end_token = res.items[i - 1].end_token
            else: 
                break
        return res