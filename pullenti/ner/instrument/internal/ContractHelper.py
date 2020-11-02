# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.core.BracketHelper import BracketHelper

class ContractHelper:
    
    @staticmethod
    def correct_dummy_newlines(fr : 'FragToken') -> None:
        """ Объединение абзацев в один фрагмент, если переход на новую строку
        является сомнительным (для договоров обычно кривые документы)
        
        Args:
            fr(FragToken): 
        """
        i = 0
        while i < len(fr.children): 
            ch = fr.children[i]
            if ((ch.kind == InstrumentKind.KEYWORD or ch.kind == InstrumentKind.NUMBER or ch.kind == InstrumentKind.NAME) or ch.kind == InstrumentKind.EDITIONS or ch.kind == InstrumentKind.COMMENT): 
                pass
            else: 
                break
            i += 1
        if ((i < len(fr.children)) and fr.children[i].kind == InstrumentKind.INDENTION): 
            j = (i + 1)
            while j < len(fr.children): 
                if (fr.children[j].kind != InstrumentKind.INDENTION): 
                    break
                elif (ContractHelper.__calc_newline_between_coef(fr.children[j - 1], fr.children[j]) > 0): 
                    break
                j += 1
            if (j >= len(fr.children)): 
                j -= 1
                fr.children[i].kind = InstrumentKind.CONTENT
                fr.children[i].number = 0
                fr.children[i].end_token = fr.children[j].end_token
                if ((i + 1) < len(fr.children)): 
                    del fr.children[i + 1:i + 1+len(fr.children) - i - 1]
                if (fr.kind == InstrumentKind.PREAMBLE and len(fr.children) == 1): 
                    fr.children.clear()
            else: 
                ch = False
                j = (i + 1)
                while j < len(fr.children): 
                    if (fr.children[j - 1].kind == InstrumentKind.INDENTION and fr.children[j].kind == InstrumentKind.INDENTION and (ContractHelper.__calc_newline_between_coef(fr.children[j - 1], fr.children[j]) < 0)): 
                        fr.children[j - 1].end_token = fr.children[j].end_token
                        del fr.children[j]
                        j -= 1
                        ch = True
                    j += 1
                if (ch): 
                    num = 1
                    j = i
                    while j < len(fr.children): 
                        if (fr.children[j].kind == InstrumentKind.INDENTION): 
                            fr.children[j].number = num
                            num += 1
                        j += 1
        for ch in fr.children: 
            ContractHelper.correct_dummy_newlines(ch)
    
    @staticmethod
    def __calc_newline_between_coef(fr1 : 'FragToken', fr2 : 'FragToken') -> int:
        if (fr1.newlines_after_count > 1): 
            return 1
        tt = fr1.begin_token
        while tt is not None and tt.end_char <= fr1.end_char: 
            if (BracketHelper.can_be_start_of_sequence(tt, False, False)): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.CANBEMANYLINES, 100)
                if (br is not None and br.end_char >= fr2.begin_char): 
                    return -1
            tt = tt.next0_
        t = fr1.end_token
        if (t.is_char_of(":;.")): 
            return 1
        if ((isinstance(t, TextToken)) and ((t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction))): 
            return -1
        t1 = fr2.begin_token
        if (isinstance(t1, TextToken)): 
            if (t1.chars.is_all_lower): 
                return -1
            if (BracketHelper.can_be_start_of_sequence(t1, False, False)): 
                if (t.chars.is_all_lower): 
                    return -1
        elif (isinstance(t1, NumberToken)): 
            if (t.chars.is_all_lower): 
                return -1
        if (t.chars.is_all_lower): 
            if (fr2.end_token.is_char(';')): 
                return -1
        return 0