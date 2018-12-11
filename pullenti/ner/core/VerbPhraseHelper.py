# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.VerbPhraseItemToken import VerbPhraseItemToken
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Token import Token
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken

class VerbPhraseHelper:
    """ Работа с глагольными группами (последовательность из глаголов и наречий) """
    
    @staticmethod
    def tryParse(t : 'Token') -> 'VerbPhraseToken':
        """ Создать глагольную группу
        
        Args:
            t(Token): первый токен группы
        
        Returns:
            VerbPhraseToken: группа или null
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        if (not t.chars.is_letter): 
            return None
        if (t.chars.is_cyrillic_letter): 
            return VerbPhraseHelper.__tryParseRu(t)
        return None
    
    @staticmethod
    def __tryParseRu(t : 'Token') -> 'VerbPhraseToken':
        res = None
        t0 = t
        not0_ = None
        has_verb = False
        first_pass2827 = True
        while True:
            if first_pass2827: first_pass2827 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not ((isinstance(t, TextToken)))): 
                break
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt.term == "НЕ"): 
                not0_ = t
                continue
            ty = 0
            mc = tt.getMorphClassInDictionary()
            if (tt.term == "НЕТ"): 
                ty = 1
            elif (mc.is_adverb): 
                ty = 2
            elif (tt.is_pure_verb or tt.is_verb_be): 
                ty = 1
            elif (mc.is_verb): 
                if (mc.is_preposition or mc.is_misc): 
                    pass
                elif (mc.is_noun): 
                    if (tt.term == "СТАЛИ"): 
                        ty = 1
                    elif (not tt.chars.is_all_lower and not MiscHelper.canBeStartOfSentence(tt)): 
                        ty = 1
                elif (mc.is_proper): 
                    if (tt.chars.is_all_lower): 
                        ty = 1
                else: 
                    ty = 1
            if (ty == 0): 
                break
            if (res is None): 
                res = VerbPhraseToken(t0, t)
            res.end_token = t
            it = VerbPhraseItemToken._new665(t, t, MorphCollection(t.morph))
            if (not0_ is not None): 
                it.begin_token = not0_
                it.not0_ = True
                not0_ = (None)
            it.is_adverb = ty == 2
            it.normal = t.getNormalCaseText((MorphClass.ADVERB if ty == 2 else MorphClass.VERB), False, MorphGender.UNDEFINED, False)
            res.items.append(it)
            if (not has_verb and ty == 1): 
                res.morph = it.morph
                has_verb = True
        if (not has_verb): 
            return None
        return res