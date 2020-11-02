# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.VerbPhraseItemToken import VerbPhraseItemToken
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.Token import Token
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.PrepositionHelper import PrepositionHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class VerbPhraseHelper:
    """ Работа с глагольными группами (последовательность из глаголов и наречий)
    Хелпер глагольных групп
    """
    
    @staticmethod
    def try_parse(t : 'Token', can_be_partition : bool=False, can_be_adj_partition : bool=False, force_parse : bool=False) -> 'VerbPhraseToken':
        """ Создать глагольную группу
        
        Args:
            t(Token): первый токен группы
            can_be_partition(bool): выделять ли причастия
            can_be_adj_partition(bool): это бывают чистые прилагательные используются в режиме причастий (действия, опасные для жизни)
            force_parse(bool): всегда ли пытаться выделять, даже при сомнительных случаях (false по умолчанию)
        
        Returns:
            VerbPhraseToken: группа или null
        """
        if (not (isinstance(t, TextToken))): 
            return None
        if (not t.chars.is_letter): 
            return None
        if (t.chars.is_cyrillic_letter): 
            return VerbPhraseHelper.__try_parse_ru(t, can_be_partition, can_be_adj_partition, force_parse)
        return None
    
    @staticmethod
    def __try_parse_ru(t : 'Token', can_be_partition : bool, can_be_adj_partition : bool, force_parse : bool) -> 'VerbPhraseToken':
        res = None
        t0 = t
        not0_ = None
        has_verb = False
        verb_be_before = False
        prep = None
        first_pass3563 = True
        while True:
            if first_pass3563: first_pass3563 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not (isinstance(t, TextToken))): 
                break
            tt = Utils.asObjectOrNull(t, TextToken)
            is_participle = False
            if (tt.term == "НЕ"): 
                not0_ = t
                continue
            ty = 0
            norm = None
            mc = tt.get_morph_class_in_dictionary()
            if (tt.term == "НЕТ"): 
                if (has_verb): 
                    break
                ty = 1
            elif (tt.term == "ДОПУСТИМО"): 
                ty = 3
            elif (mc.is_adverb and not mc.is_verb): 
                ty = 2
            elif (tt.is_pure_verb or tt.is_verb_be): 
                ty = 1
                if (has_verb): 
                    if (not tt.morph.contains_attr("инф.", None)): 
                        if (verb_be_before): 
                            pass
                        else: 
                            break
            elif (mc.is_verb): 
                if (mc.is_preposition or mc.is_misc or mc.is_pronoun): 
                    pass
                elif (mc.is_noun): 
                    if (tt.term == "СТАЛИ" or tt.term == "СТЕКЛО" or tt.term == "БЫЛИ"): 
                        ty = 1
                    elif (not tt.chars.is_all_lower and not MiscHelper.can_be_start_of_sentence(tt)): 
                        ty = 1
                    elif (mc.is_adjective and can_be_partition): 
                        ty = 1
                    elif (force_parse): 
                        ty = 1
                elif (mc.is_proper): 
                    if (tt.chars.is_all_lower): 
                        ty = 1
                else: 
                    ty = 1
                if (mc.is_adjective): 
                    is_participle = True
                if (not tt.morph.case_.is_undefined): 
                    is_participle = True
                if (not can_be_partition and is_participle): 
                    break
                if (has_verb): 
                    if (tt.morph.contains_attr("инф.", None)): 
                        pass
                    elif (not is_participle): 
                        pass
                    else: 
                        break
            elif ((mc.is_adjective and tt.morph.contains_attr("к.ф.", None) and tt.term.endswith("О")) and NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None) is None): 
                ty = 2
            elif (mc.is_adjective and ((can_be_partition or can_be_adj_partition))): 
                if (tt.morph.contains_attr("к.ф.", None) and not can_be_adj_partition): 
                    break
                norm = tt.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE, False)
                if (norm.endswith("ЙШИЙ")): 
                    pass
                else: 
                    grs = DerivateService.find_derivates(norm, True, None)
                    if (grs is not None and len(grs) > 0): 
                        hverb = False
                        hpart = False
                        for gr in grs: 
                            for w in gr.words: 
                                if (w.class0_.is_adjective and w.class0_.is_verb): 
                                    if (w.spelling == norm): 
                                        hpart = True
                                elif (w.class0_.is_verb): 
                                    hverb = True
                        if (hpart and hverb): 
                            ty = 3
                        elif (can_be_adj_partition): 
                            ty = 3
                        if (ty != 3 and not Utils.isNullOrEmpty(grs[0].prefix) and norm.startswith(grs[0].prefix)): 
                            hverb = False
                            hpart = False
                            norm1 = norm[len(grs[0].prefix):]
                            grs = DerivateService.find_derivates(norm1, True, None)
                            if (grs is not None and len(grs) > 0): 
                                for gr in grs: 
                                    for w in gr.words: 
                                        if (w.class0_.is_adjective and w.class0_.is_verb): 
                                            if (w.spelling == norm1): 
                                                hpart = True
                                        elif (w.class0_.is_verb): 
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
            it = VerbPhraseItemToken._new603(t, t, MorphCollection(t.morph))
            if (not0_ is not None): 
                it.begin_token = not0_
                it.not0_ = True
                not0_ = (None)
            it.is_adverb = ty == 2
            if (prep is not None and not t.morph.case_.is_undefined and len(res.items) == 0): 
                if (((prep.next_case) & t.morph.case_).is_undefined): 
                    return None
                it.morph.remove_items(prep.next_case, False)
                res.preposition = prep
            if (norm is None): 
                norm = t.get_normal_case_text((MorphClass.ADJECTIVE if ty == 3 else (MorphClass.ADVERB if ty == 2 else MorphClass.VERB)), MorphNumber.SINGULAR, MorphGender.MASCULINE, False)
                if (ty == 1 and not tt.morph.case_.is_undefined): 
                    mi = MorphWordForm._new604(MorphCase.NOMINATIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE)
                    for mit in tt.morph.items: 
                        if (isinstance(mit, MorphWordForm)): 
                            mi.misc = mit.misc
                            break
                    nnn = MorphologyService.get_wordform("КК" + t.term, mi)
                    if (nnn is not None): 
                        norm = nnn[2:]
            it.normal = norm
            res.items.append(it)
            if (not has_verb and ((ty == 1 or ty == 3))): 
                res.morph = it.morph
                has_verb = True
            if (ty == 1 or ty == 3): 
                if (ty == 1 and tt.is_verb_be): 
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