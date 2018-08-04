# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core._NounPraseHelperInt import _NounPraseHelperInt
from pullenti.morph.LanguageHelper import LanguageHelper


class NounPhraseHelper:
    """ Выделение именных групп (существительсно с согласованными прилагательными (если они есть). """
    
    @staticmethod
    def try_parse(t : 'Token', typ : 'NounPhraseParseAttr'=NounPhraseParseAttr.NO, max_char_pos : int=0) -> 'NounPhraseToken':
        """ Попробовать создать именную группу с указанного токена
        
        Args:
            t(Token): начальный токен
            typ(NounPhraseParseAttr): параметры (можно битовую маску)
            max_char_pos(int): максимальная позиция в тексте, до которой выделять, если 0, то без ограничений
        
        Returns:
            NounPhraseToken: именная группа или null
        """
        from pullenti.ner.TextToken import TextToken
        res = _NounPraseHelperInt.try_parse(t, typ, max_char_pos)
        if (res is not None): 
            return res
        if (((typ & NounPhraseParseAttr.PARSEPREPOSITION)) != NounPhraseParseAttr.NO): 
            if (isinstance(t, TextToken) and t.morph.class0_.is_preposition and (t.whitespaces_after_count < 3)): 
                res = _NounPraseHelperInt.try_parse(t.next0_, typ, max_char_pos)
                if (res is not None): 
                    mc = LanguageHelper.get_case_after_preposition((t if isinstance(t, TextToken) else None).lemma)
                    res.preposition = t
                    res.begin_token = t
                    if (not (mc & res.morph.case).is_undefined): 
                        res.morph.remove_items(mc, False)
                    elif (t.morph.class0_.is_adverb): 
                        return None
                    return res
        return None