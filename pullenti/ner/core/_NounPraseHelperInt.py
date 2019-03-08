# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.Explanatory import Explanatory
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.internal.NounPhraseItemTextVar import NounPhraseItemTextVar
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseToken import NounPhraseToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.Token import Token
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.internal.NounPhraseItem import NounPhraseItem
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class _NounPraseHelperInt:
    
    @staticmethod
    def try_parse(first : 'Token', typ : 'NounPhraseParseAttr', max_char_pos : int) -> 'NounPhraseToken':
        if (first is None): 
            return None
        if (first.not_noun_phrase): 
            if ((((typ) & (((((NounPhraseParseAttr.IGNOREPARTICIPLES) | (NounPhraseParseAttr.REFERENTCANBENOUN) | (NounPhraseParseAttr.PARSEPRONOUNS)) | (NounPhraseParseAttr.PARSEADVERBS) | (NounPhraseParseAttr.PARSENUMERICASADJECTIVE)) | (NounPhraseParseAttr.IGNOREBRACKETS))))) == (NounPhraseParseAttr.NO)): 
                return None
        cou = 0
        t = first
        while t is not None: 
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if (t.morph.language.is_cyrillic0 or (((isinstance(t, NumberToken)) and t.morph.class0_.is_adjective0 and not t.chars.is_latin_letter0)) or (((isinstance(t, ReferentToken)) and (((typ) & (NounPhraseParseAttr.REFERENTCANBENOUN))) != (NounPhraseParseAttr.NO) and not t.chars.is_latin_letter0))): 
                res = _NounPraseHelperInt.__try_parse_ru(first, typ, max_char_pos)
                if (res is None): 
                    first.not_noun_phrase = True
                return res
            elif (t.chars.is_latin_letter0): 
                res = _NounPraseHelperInt.__try_parse_en(first, typ, max_char_pos)
                if (res is None): 
                    first.not_noun_phrase = True
                return res
            else: 
                cou += 1
                if ((cou) > 0): 
                    break
            t = t.next0_
        return None
    
    @staticmethod
    def __try_parse_ru(first : 'Token', typ : 'NounPhraseParseAttr', max_char_pos : int) -> 'NounPhraseToken':
        if (first is None): 
            return None
        items = None
        adverbs = None
        internal_noun_prase = None
        conj_before = False
        t = first
        first_pass2894 = True
        while True:
            if first_pass2894: first_pass2894 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if ((t.morph.class0_.is_conjunction0 and not t.morph.class0_.is_adjective0 and not t.morph.class0_.is_pronoun0) and not t.morph.class0_.is_noun0): 
                if (conj_before): 
                    break
                if ((((typ) & (NounPhraseParseAttr.CANNOTHASCOMMAAND))) != (NounPhraseParseAttr.NO)): 
                    break
                if (items is not None and t.is_and0): 
                    conj_before = True
                    if ((t.next0_ is not None and t.next0_.is_char_of("\\/") and t.next0_.next0_ is not None) and t.next0_.next0_.is_or0): 
                        t = t.next0_.next0_
                    continue
                break
            elif (t.is_comma0): 
                if (conj_before or items is None): 
                    break
                if ((((typ) & (NounPhraseParseAttr.CANNOTHASCOMMAAND))) != (NounPhraseParseAttr.NO)): 
                    break
                mc = t.previous.get_morph_class_in_dictionary()
                if (mc.is_proper_surname0 or mc.is_proper_secname0): 
                    break
                conj_before = True
                continue
            elif (t.is_char('(')): 
                if (items is None): 
                    return None
                if ((((typ) & (NounPhraseParseAttr.IGNOREBRACKETS))) != (NounPhraseParseAttr.IGNOREBRACKETS)): 
                    break
                brr = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (brr is None): 
                    break
                if (brr.length_char > 100): 
                    break
                t = brr.end_token
                continue
            if (isinstance(t, ReferentToken)): 
                if ((((typ) & (NounPhraseParseAttr.REFERENTCANBENOUN))) == (NounPhraseParseAttr.NO)): 
                    break
            elif (t.chars.is_latin_letter0): 
                break
            it = NounPhraseItem.try_parse(t, items, typ)
            if (it is None or ((not it.can_be_adj and not it.can_be_noun))): 
                if ((((typ) & (NounPhraseParseAttr.PARSEADVERBS))) != (NounPhraseParseAttr.NO) and (isinstance(t, TextToken)) and t.morph.class0_.is_adverb0): 
                    if (items is None): 
                        if (t.previous is not None and t.previous.morph.class0_.is_preposition0): 
                            pass
                        else: 
                            return None
                    if (adverbs is None): 
                        adverbs = list()
                    adverbs.append(Utils.asObjectOrNull(t, TextToken))
                    continue
                break
            it.conj_before = conj_before
            conj_before = False
            if (not it.can_be_adj and not it.can_be_noun): 
                break
            if (t.is_newline_before0 and t != first): 
                if ((((typ) & (NounPhraseParseAttr.MULTILINES))) != (NounPhraseParseAttr.NO)): 
                    pass
                elif (items is not None and t.chars != items[len(items) - 1].chars): 
                    if (t.chars.is_all_lower0 and items[len(items) - 1].chars.is_capital_upper0): 
                        pass
                    else: 
                        break
            if (items is None): 
                items = list()
            else: 
                it0 = items[len(items) - 1]
                if (it0.can_be_noun and it0.is_personal_pronoun0): 
                    if (it.is_pronoun0): 
                        break
                    if ((it0.begin_token.previous is not None and it0.begin_token.previous.get_morph_class_in_dictionary().is_verb0 and not it0.begin_token.previous.get_morph_class_in_dictionary().is_adjective0) and not it0.begin_token.previous.get_morph_class_in_dictionary().is_preposition0): 
                        if (t.morph.case_.is_nominative0 or t.morph.case_.is_accusative0): 
                            pass
                        else: 
                            break
                    if (it.can_be_noun and it.is_verb0): 
                        break
            items.append(it)
            t = it.end_token
            if (t.is_newline_after0 and not t.chars.is_all_lower0): 
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_proper_surname0): 
                    break
                if (t.morph.class0_.is_proper_surname0 and mc.is_undefined0): 
                    break
        if (items is None): 
            return None
        if (len(items) == 1 and items[0].can_be_adj): 
            and0_ = False
            tt1 = items[0].end_token.next0_
            first_pass2895 = True
            while True:
                if first_pass2895: first_pass2895 = False
                else: tt1 = tt1.next0_
                if (not (tt1 is not None)): break
                if (tt1.is_and0 or tt1.is_or0): 
                    and0_ = True
                    break
                if (tt1.is_comma0 or tt1.is_value("НО", None) or tt1.is_value("ТАК", None)): 
                    continue
                break
            if (and0_): 
                if (items[0].can_be_noun and items[0].is_personal_pronoun0): 
                    and0_ = False
            if (and0_): 
                tt2 = tt1.next0_
                if (tt2 is not None and tt2.morph.class0_.is_preposition0): 
                    tt2 = tt2.next0_
                npt1 = _NounPraseHelperInt.__try_parse_ru(tt2, typ, max_char_pos)
                if (npt1 is not None and len(npt1.adjectives) > 0): 
                    ok1 = False
                    for av in items[0].adj_morph: 
                        for v in (npt1.noun).noun_morph: 
                            if (v.check_accord(av, False, False)): 
                                items[0].morph.add_item(av)
                                ok1 = True
                    if (ok1): 
                        npt1.begin_token = items[0].begin_token
                        npt1.end_token = tt1.previous
                        npt1.adjectives.clear()
                        npt1.adjectives.append(items[0])
                        return npt1
        last1 = items[len(items) - 1]
        check = True
        for it in items: 
            if (not it.can_be_adj): 
                check = False
                break
            elif (it.can_be_noun and it.is_personal_pronoun0): 
                check = False
                break
        tt1 = last1.end_token.next0_
        if ((tt1 is not None and check and ((tt1.morph.class0_.is_preposition0 or tt1.morph.case_.is_instrumental0))) and (tt1.whitespaces_before_count < 2)): 
            inp = NounPhraseHelper.try_parse(tt1, Utils.valToEnum((typ) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), max_char_pos)
            if (inp is not None): 
                tt1 = inp.end_token.next0_
                npt1 = _NounPraseHelperInt.__try_parse_ru(tt1, typ, max_char_pos)
                if (npt1 is not None): 
                    ok = True
                    for it in items: 
                        if (not NounPhraseItem.try_accord_adj_and_noun(it, Utils.asObjectOrNull(npt1.noun, NounPhraseItem))): 
                            ok = False
                            break
                    if (ok): 
                        if (npt1.morph.case_.is_genitive0): 
                            ok = False
                    if (ok): 
                        i = 0
                        while i < len(items): 
                            npt1.adjectives.insert(i, items[i])
                            i += 1
                        npt1.internal_noun = inp
                        mmm = MorphCollection(npt1.morph)
                        for it in items: 
                            mmm.remove_items(it.adj_morph[0], False)
                        if (mmm.gender != MorphGender.UNDEFINED or mmm.number != MorphNumber.UNDEFINED or not mmm.case_.is_undefined0): 
                            npt1.morph = mmm
                        if (adverbs is not None): 
                            if (npt1.adverbs is None): 
                                npt1.adverbs = adverbs
                            else: 
                                npt1.adverbs[0:0] = adverbs
                        return npt1
                if (tt1 is not None and tt1.morph.class0_.is_noun0 and not tt1.morph.case_.is_genitive0): 
                    it = NounPhraseItem.try_parse(tt1, items, typ)
                    if (it is not None and it.can_be_noun): 
                        internal_noun_prase = inp
                        inp.begin_token = items[0].end_token.next0_
                        items.append(it)
        ok2 = False
        if ((len(items) == 1 and (((typ) & (NounPhraseParseAttr.ADJECTIVECANBELAST))) != (NounPhraseParseAttr.NO) and (items[0].whitespaces_after_count < 3)) and not items[0].is_adverb0): 
            if (not items[0].can_be_adj): 
                ok2 = True
            elif (items[0].is_personal_pronoun0 and items[0].can_be_noun): 
                ok2 = True
        if (ok2): 
            it = NounPhraseItem.try_parse(items[0].end_token.next0_, None, typ)
            if (it is not None and it.can_be_adj and it.begin_token.chars.is_all_lower0): 
                ok2 = True
                if (it.is_adverb0 or it.is_verb0): 
                    ok2 = False
                if (it.is_pronoun0 and items[0].is_pronoun0): 
                    ok2 = False
                    if (it.can_be_adj_for_personal_pronoun0 and items[0].is_personal_pronoun0): 
                        ok2 = True
                if (ok2 and NounPhraseItem.try_accord_adj_and_noun(it, items[0])): 
                    npt1 = _NounPraseHelperInt.__try_parse_ru(it.begin_token, typ, max_char_pos)
                    if (npt1 is not None and ((npt1.end_char > it.end_char or len(npt1.adjectives) > 0))): 
                        pass
                    else: 
                        items.insert(0, it)
        noun = None
        adj_after = None
        for i in range(len(items) - 1, -1, -1):
            if (items[i].can_be_noun): 
                if (items[i].conj_before): 
                    continue
                if (i > 0 and not items[i - 1].can_be_adj): 
                    continue
                if (i > 0 and items[i - 1].can_be_noun): 
                    if (items[i - 1].is_doubt_adjective): 
                        continue
                    if (items[i - 1].is_pronoun0 and items[i].is_pronoun0): 
                        if (items[i].is_pronoun0 and items[i - 1].can_be_adj_for_personal_pronoun0): 
                            pass
                        else: 
                            continue
                noun = items[i]
                del items[i:i+len(items) - i]
                if (adj_after is not None): 
                    items.append(adj_after)
                break
        if (noun is None): 
            return None
        res = NounPhraseToken(first, noun.end_token)
        if (adverbs is not None): 
            for a in adverbs: 
                if (a.begin_char < noun.begin_char): 
                    if (res.adverbs is None): 
                        res.adverbs = list()
                    res.adverbs.append(a)
        res.noun = (noun)
        res.multi_nouns = noun.multi_nouns
        res.internal_noun = internal_noun_prase
        for v in noun.noun_morph: 
            noun.morph.add_item(v)
        res.morph = noun.morph
        if (res.morph.case_.is_nominative0 and first.previous is not None and first.previous.morph.class0_.is_preposition0): 
            res.morph.case_ = (res.morph.case_) ^ MorphCase.NOMINATIVE
        if ((((typ) & (NounPhraseParseAttr.PARSEPRONOUNS))) == (NounPhraseParseAttr.NO) and ((res.morph.class0_.is_pronoun0 or res.morph.class0_.is_personal_pronoun0))): 
            return None
        stat = None
        if (len(items) > 1): 
            stat = dict()
        need_update_morph = False
        if (len(items) > 0): 
            ok_list = list()
            is_num_not = False
            for vv in noun.noun_morph: 
                v = vv
                i = 0
                while i < len(items): 
                    ok = False
                    for av in items[i].adj_morph: 
                        if (v.check_accord(av, False, False)): 
                            ok = True
                            if (not ((av.case_) & v.case_).is_undefined0 and av.case_ != v.case_): 
                                v.case_ = av.case_ = (av.case_) & v.case_
                            break
                    if (not ok): 
                        if (items[i].can_be_numeric_adj0 and items[i].try_accord_var(v, False)): 
                            ok = True
                            v = (Utils.asObjectOrNull(v.clone(), NounPhraseItemTextVar))
                            v.number = MorphNumber.PLURAL
                            is_num_not = True
                            v.case_ = MorphCase()
                            for a in items[i].adj_morph: 
                                v.case_ = (v.case_) | a.case_
                        else: 
                            break
                    i += 1
                if (i >= len(items)): 
                    ok_list.append(v)
            if (len(ok_list) > 0 and (((len(ok_list) < res.morph.items_count) or is_num_not))): 
                res.morph = MorphCollection()
                for v in ok_list: 
                    res.morph.add_item(v)
                if (not is_num_not): 
                    noun.morph = res.morph
        i = 0
        first_pass2896 = True
        while True:
            if first_pass2896: first_pass2896 = False
            else: i += 1
            if (not (i < len(items))): break
            for av in items[i].adj_morph: 
                for v in noun.noun_morph: 
                    if (v.check_accord(av, False, False)): 
                        if (not ((av.case_) & v.case_).is_undefined0 and av.case_ != v.case_): 
                            v.case_ = av.case_ = (av.case_) & v.case_
                            need_update_morph = True
                        items[i].morph.add_item(av)
                        if (stat is not None and len(av.normal_value) > 1): 
                            last = av.normal_value[len(av.normal_value) - 1]
                            if (not last in stat): 
                                stat[last] = 1
                            else: 
                                stat[last] += 1
            if (items[i].is_pronoun0 or items[i].is_personal_pronoun0): 
                res.anafor = items[i].begin_token
                if ((((typ) & (NounPhraseParseAttr.PARSEPRONOUNS))) == (NounPhraseParseAttr.NO)): 
                    continue
            tt = Utils.asObjectOrNull(items[i].begin_token, TextToken)
            if (tt is not None and not tt.term.startswith("ВЫСШ")): 
                err = False
                for wf in tt.morph.items: 
                    if (wf.class0_.is_adjective0): 
                        if (wf.contains_attr("прев.", None)): 
                            if ((((typ) & (NounPhraseParseAttr.IGNOREADJBEST))) != (NounPhraseParseAttr.NO)): 
                                err = True
                        if (wf.contains_attr("к.ф.", None) and tt.morph.class0_.is_personal_pronoun0): 
                            return None
                if (err): 
                    continue
            if (res.morph.case_.is_nominative0): 
                v = MiscHelper.get_text_value_of_meta_token(items[i], GetTextAttr.KEEPQUOTES)
                if (not Utils.isNullOrEmpty(v)): 
                    if (items[i].get_normal_case_text(None, False, MorphGender.UNDEFINED, False) != v): 
                        wf = NounPhraseItemTextVar(items[i].morph, None)
                        wf.normal_value = v
                        wf.class0_ = MorphClass.ADJECTIVE
                        wf.case_ = res.morph.case_
                        if (res.morph.case_.is_prepositional0 or res.morph.gender == MorphGender.NEUTER or res.morph.gender == MorphGender.FEMINIE): 
                            items[i].morph.add_item(wf)
                        else: 
                            items[i].morph.insert_item(0, wf)
            res.adjectives.append(items[i])
            if (items[i].end_char > res.end_char): 
                res.end_token = items[i].end_token
        i = 0
        first_pass2897 = True
        while True:
            if first_pass2897: first_pass2897 = False
            else: i += 1
            if (not (i < (len(res.adjectives) - 1))): break
            if (res.adjectives[i].whitespaces_after_count > 5): 
                if (res.adjectives[i].chars != res.adjectives[i + 1].chars): 
                    if (not res.adjectives[i + 1].chars.is_all_lower0): 
                        return None
                    if (res.adjectives[i].chars.is_all_upper0 and res.adjectives[i + 1].chars.is_capital_upper0): 
                        return None
                    if (res.adjectives[i].chars.is_capital_upper0 and res.adjectives[i + 1].chars.is_all_upper0): 
                        return None
                if (res.adjectives[i].whitespaces_after_count > 10): 
                    if (res.adjectives[i].newlines_after_count == 1): 
                        if (res.adjectives[i].chars.is_capital_upper0 and i == 0 and res.adjectives[i + 1].chars.is_all_lower0): 
                            continue
                        if (res.adjectives[i].chars == res.adjectives[i + 1].chars): 
                            continue
                    return None
        if (need_update_morph): 
            noun.morph = MorphCollection()
            for v in noun.noun_morph: 
                noun.morph.add_item(v)
            res.morph = noun.morph
        if (len(res.adjectives) > 0): 
            if (noun.begin_token.previous is not None): 
                if (noun.begin_token.previous.is_comma_and0): 
                    if (res.adjectives[0].begin_char > noun.begin_char): 
                        pass
                    else: 
                        return None
            zap = 0
            and0_ = 0
            cou = 0
            last_and = False
            i = 0
            while i < (len(res.adjectives) - 1): 
                te = res.adjectives[i].end_token.next0_
                if (te is None): 
                    return None
                if (te.is_char('(')): 
                    pass
                elif (te.is_comma0): 
                    zap += 1
                elif (te.is_and0): 
                    and0_ += 1
                    if (i == (len(res.adjectives) - 2)): 
                        last_and = True
                if (not res.adjectives[i].begin_token.morph.class0_.is_pronoun0): 
                    cou += 1
                i += 1
            if ((zap + and0_) > 0): 
                if (and0_ > 1): 
                    return None
                elif (and0_ == 1 and not last_and): 
                    return None
                if ((zap + and0_) != cou): 
                    if (and0_ == 1): 
                        pass
                    else: 
                        return None
                last = Utils.asObjectOrNull(res.adjectives[len(res.adjectives) - 1], NounPhraseItem)
                if (last.is_pronoun0 and not last_and): 
                    return None
        if (stat is not None): 
            for adj in items: 
                if (adj.morph.items_count > 1): 
                    w1 = Utils.asObjectOrNull(adj.morph.get_indexer_item(0), NounPhraseItemTextVar)
                    w2 = Utils.asObjectOrNull(adj.morph.get_indexer_item(1), NounPhraseItemTextVar)
                    if ((len(w1.normal_value) < 2) or (len(w2.normal_value) < 2)): 
                        break
                    l1 = w1.normal_value[len(w1.normal_value) - 1]
                    l2 = w2.normal_value[len(w2.normal_value) - 1]
                    i1 = 0
                    i2 = 0
                    wrapi1536 = RefOutArgWrapper(0)
                    Utils.tryGetValue(stat, l1, wrapi1536)
                    i1 = wrapi1536.value
                    wrapi2535 = RefOutArgWrapper(0)
                    Utils.tryGetValue(stat, l2, wrapi2535)
                    i2 = wrapi2535.value
                    if (i1 < i2): 
                        adj.morph.remove_item(1)
                        adj.morph.insert_item(0, w2)
        if (res.begin_token.get_morph_class_in_dictionary().is_verb0 and len(items) > 0): 
            if (not res.begin_token.chars.is_all_lower0 or res.begin_token.previous is None): 
                pass
            elif (res.begin_token.previous.morph.class0_.is_preposition0): 
                pass
            else: 
                comma = False
                tt = res.begin_token.previous
                first_pass2898 = True
                while True:
                    if first_pass2898: first_pass2898 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.morph.class0_.is_adverb0): 
                        continue
                    if (tt.is_char_of(".;")): 
                        break
                    if (tt.is_comma0): 
                        comma = True
                        continue
                    if (tt.is_value("НЕ", None)): 
                        continue
                    if (((tt.morph.class0_.is_noun0 or tt.morph.class0_.is_proper0)) and comma): 
                        for it in res.begin_token.morph.items: 
                            if (it.class0_.is_verb0 and (isinstance(it, MorphWordForm))): 
                                if (tt.morph.check_accord(it, False, False)): 
                                    if (res.morph.case_.is_instrumental0): 
                                        return None
                                    ews = Explanatory.find_derivates((it).normal_case, True, tt.morph.language)
                                    if (ews is not None): 
                                        for ew in ews: 
                                            if (ew.transitive > 0): 
                                                if (res.morph.case_.is_genitive0): 
                                                    return None
                                            if (ew.nexts is not None): 
                                                wrapcm537 = RefOutArgWrapper(None)
                                                inoutres538 = Utils.tryGetValue(ew.nexts, "", wrapcm537)
                                                cm = wrapcm537.value
                                                if (inoutres538): 
                                                    if (not ((cm) & res.morph.case_).is_undefined0): 
                                                        return None
                    break
        if (res.begin_token == res.end_token): 
            mc = res.begin_token.get_morph_class_in_dictionary()
            if (mc.is_adverb0): 
                if (res.begin_token.previous is not None and res.begin_token.previous.morph.class0_.is_preposition0): 
                    pass
                elif (mc.is_noun0 and not mc.is_preposition0 and not mc.is_conjunction0): 
                    pass
                elif (res.begin_token.is_value("ВЕСЬ", None)): 
                    pass
                else: 
                    return None
        return res
    
    @staticmethod
    def __try_parse_en(first : 'Token', typ : 'NounPhraseParseAttr', max_char_pos : int) -> 'NounPhraseToken':
        if (first is None): 
            return None
        items = None
        has_article = False
        has_prop = False
        has_misc = False
        if (first.previous is not None and first.previous.morph.class0_.is_preposition0 and (first.whitespaces_before_count < 3)): 
            has_prop = True
        t = first
        first_pass2899 = True
        while True:
            if first_pass2899: first_pass2899 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if (not t.chars.is_latin_letter0): 
                break
            if (t != first and t.whitespaces_before_count > 2): 
                if ((((typ) & (NounPhraseParseAttr.MULTILINES))) != (NounPhraseParseAttr.NO)): 
                    pass
                elif (MiscHelper.is_eng_article(t.previous)): 
                    pass
                else: 
                    break
            tt = Utils.asObjectOrNull(t, TextToken)
            if (t == first and tt is not None): 
                if (MiscHelper.is_eng_article(tt)): 
                    has_article = True
                    continue
            if (isinstance(t, ReferentToken)): 
                if ((((typ) & (NounPhraseParseAttr.REFERENTCANBENOUN))) == (NounPhraseParseAttr.NO)): 
                    break
            elif (tt is None): 
                break
            if ((t.is_value("SO", None) and t.next0_ is not None and t.next0_.is_hiphen0) and t.next0_.next0_ is not None): 
                if (t.next0_.next0_.is_value("CALL", None)): 
                    t = t.next0_.next0_
                    continue
            mc = t.get_morph_class_in_dictionary()
            if (mc.is_conjunction0 or mc.is_preposition0): 
                break
            if (mc.is_pronoun0 or mc.is_personal_pronoun0): 
                if ((((typ) & (NounPhraseParseAttr.PARSEPRONOUNS))) == (NounPhraseParseAttr.NO)): 
                    break
            elif (mc.is_misc0): 
                if (t.is_value("THIS", None) or t.is_value("THAT", None)): 
                    has_misc = True
                    if ((((typ) & (NounPhraseParseAttr.PARSEPRONOUNS))) == (NounPhraseParseAttr.NO)): 
                        break
            is_adj = False
            if (((has_article or has_prop or has_misc)) and items is None): 
                pass
            elif (isinstance(t, ReferentToken)): 
                pass
            else: 
                if (not mc.is_noun0 and not mc.is_adjective0): 
                    if (mc.is_undefined0 and has_article): 
                        pass
                    elif (items is None and mc.is_undefined0 and t.chars.is_capital_upper0): 
                        pass
                    elif (mc.is_pronoun0): 
                        pass
                    elif (tt.term.endswith("EAN")): 
                        is_adj = True
                    elif (MiscHelper.is_eng_adj_suffix(tt.next0_)): 
                        pass
                    else: 
                        break
                if (mc.is_verb0): 
                    if (t.next0_ is not None and t.next0_.morph.class0_.is_verb0 and (t.whitespaces_after_count < 2)): 
                        pass
                    elif (t.chars.is_capital_upper0 and not MiscHelper.can_be_start_of_sentence(t)): 
                        pass
                    elif ((t.chars.is_capital_upper0 and mc.is_noun0 and (isinstance(t.next0_, TextToken))) and t.next0_.chars.is_capital_upper0): 
                        pass
                    elif (isinstance(t, ReferentToken)): 
                        pass
                    else: 
                        break
            if (items is None): 
                items = list()
            it = NounPhraseItem(t, t)
            if (mc.is_noun0): 
                it.can_be_noun = True
            if (mc.is_adjective0 or mc.is_pronoun0 or is_adj): 
                it.can_be_adj = True
            items.append(it)
            t = it.end_token
            if (len(items) == 1): 
                if (MiscHelper.is_eng_adj_suffix(t.next0_)): 
                    mc.is_noun0 = False
                    mc.is_adjective0 = True
                    t = t.next0_.next0_
        if (items is None): 
            return None
        noun = items[len(items) - 1]
        res = NounPhraseToken(first, noun.end_token)
        res.noun = (noun)
        res.morph = MorphCollection()
        for v in noun.end_token.morph.items: 
            if (v.class0_.is_verb0): 
                continue
            if (v.class0_.is_proper0 and noun.begin_token.chars.is_all_lower0): 
                continue
            vv = Utils.asObjectOrNull(v.clone(), MorphBaseInfo)
            if (has_article and vv.number != MorphNumber.SINGULAR): 
                vv.number = MorphNumber.SINGULAR
            res.morph.add_item(vv)
        if (res.morph.items_count == 0 and has_article): 
            res.morph.add_item(MorphBaseInfo._new211(MorphClass.NOUN, MorphNumber.SINGULAR))
        i = 0
        while i < (len(items) - 1): 
            res.adjectives.append(items[i])
            i += 1
        return res