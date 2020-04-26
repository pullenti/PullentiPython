# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr

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
        from pullenti.ner.core.PrepositionHelper import PrepositionHelper
        from pullenti.ner.core._NounPraseHelperInt import _NounPraseHelperInt
        res = _NounPraseHelperInt.try_parse(t, typ, max_char_pos)
        if (res is not None): 
            return res
        if ((((typ) & (NounPhraseParseAttr.PARSEPREPOSITION))) != (NounPhraseParseAttr.NO)): 
            prep = PrepositionHelper.try_parse(t)
            if (prep is not None and (prep.whitespaces_after_count < 3)): 
                res = _NounPraseHelperInt.try_parse(prep.end_token.next0_, typ, max_char_pos)
                if (res is not None): 
                    res.preposition = prep
                    res.begin_token = t
                    if (not ((prep.next_case) & res.morph.case_).is_undefined): 
                        res.morph.remove_items(prep.next_case, False)
                    elif (t.morph.class0_.is_adverb): 
                        return None
                    return res
        return None