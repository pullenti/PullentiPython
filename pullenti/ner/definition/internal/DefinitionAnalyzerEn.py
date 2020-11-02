# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.definition.DefinitionKind import DefinitionKind
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Referent import Referent
from pullenti.ner.Token import Token
from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.NounPhraseToken import NounPhraseToken

class DefinitionAnalyzerEn:
    
    @staticmethod
    def process(kit : 'AnalysisKit', ad : 'AnalyzerData') -> None:
        t = kit.first_token
        first_pass3623 = True
        while True:
            if first_pass3623: first_pass3623 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not MiscHelper.can_be_start_of_sentence(t)): 
                continue
            rt = DefinitionAnalyzerEn.__try_parse_thesis(t)
            if (rt is None): 
                continue
            rt.referent = ad.register_referent(rt.referent)
            kit.embed_token(rt)
            t = (rt)
    
    @staticmethod
    def __try_parse_thesis(t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        t0 = t
        tt = t
        mc = tt.get_morph_class_in_dictionary()
        preamb = None
        if (mc.is_conjunction): 
            return None
        if (t.is_value("LET", None)): 
            return None
        if (mc.is_preposition or mc.is_misc or mc.is_adverb): 
            if (not MiscHelper.is_eng_article(tt)): 
                tt = tt.next0_
                first_pass3624 = True
                while True:
                    if first_pass3624: first_pass3624 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_comma): 
                        break
                    if (tt.is_char('(')): 
                        br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            tt = br.end_token
                            continue
                    if (MiscHelper.can_be_start_of_sentence(tt)): 
                        break
                    npt0 = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.REFERENTCANBENOUN), NounPhraseParseAttr), 0, None)
                    if (npt0 is not None): 
                        tt = npt0.end_token
                        continue
                    if (tt.get_morph_class_in_dictionary().is_verb): 
                        break
                if (tt is None or not tt.is_comma or tt.next0_ is None): 
                    return None
                preamb = MetaToken(t0, tt.previous)
                tt = tt.next0_
        t1 = tt
        mc = tt.get_morph_class_in_dictionary()
        npt = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.REFERENTCANBENOUN) | (NounPhraseParseAttr.PARSEADVERBS), NounPhraseParseAttr), 0, None)
        if (npt is None and (isinstance(tt, TextToken))): 
            if (tt.chars.is_all_upper): 
                npt = NounPhraseToken(tt, tt)
            elif (not tt.chars.is_all_lower): 
                if (mc.is_proper or preamb is not None): 
                    npt = NounPhraseToken(tt, tt)
        if (npt is None): 
            return None
        if (mc.is_personal_pronoun): 
            return None
        t2 = npt.end_token.next0_
        if (t2 is None or MiscHelper.can_be_start_of_sentence(t2) or not (isinstance(t2, TextToken))): 
            return None
        if (not t2.get_morph_class_in_dictionary().is_verb): 
            return None
        t3 = t2
        tt = t2.next0_
        while tt is not None: 
            if (not tt.get_morph_class_in_dictionary().is_verb): 
                break
            tt = tt.next0_
        first_pass3625 = True
        while True:
            if first_pass3625: first_pass3625 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.next0_ is None): 
                t3 = tt
                break
            if (tt.is_char_of(".;!?")): 
                if (MiscHelper.can_be_start_of_sentence(tt.next0_)): 
                    t3 = tt
                    break
            if (not (isinstance(tt, TextToken))): 
                continue
            if (BracketHelper.can_be_start_of_sequence(tt, False, False)): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    tt = br.end_token
                    continue
        tt = t3
        if (t3.is_char_of(";.!?")): 
            tt = tt.previous
        txt = MiscHelper.get_text_value(t2, tt, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
        if (txt is None or (len(txt) < 15)): 
            return None
        if (t0 != t1): 
            tt = t1.previous
            if (tt.is_comma): 
                tt = tt.previous
            txt0 = MiscHelper.get_text_value(t0, tt, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
            if (txt0 is not None and len(txt0) > 10): 
                if (t0.chars.is_capital_upper): 
                    txt0 = ((str.lower(txt0[0])) + txt0[1:])
                txt = "{0}, {1}".format(txt, txt0)
        tt = t1
        if (MiscHelper.is_eng_article(tt)): 
            tt = tt.next0_
        nam = MiscHelper.get_text_value(tt, t2.previous, GetTextAttr.KEEPQUOTES)
        if (nam.startswith("SO-CALLED")): 
            nam = nam[9:].strip()
        dr = DefinitionReferent()
        dr.kind = DefinitionKind.ASSERTATION
        dr.add_slot(DefinitionReferent.ATTR_TERMIN, nam, False, 0)
        dr.add_slot(DefinitionReferent.ATTR_VALUE, txt, False, 0)
        return ReferentToken(dr, t0, t3)