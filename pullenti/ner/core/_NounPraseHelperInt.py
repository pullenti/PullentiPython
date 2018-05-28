# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr


class _NounPraseHelperInt:
    
    @staticmethod
    def try_parse(first : 'Token', typ : 'NounPhraseParseAttr', max_char_pos : int) -> 'NounPhraseToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.ReferentToken import ReferentToken
        if (first is None): 
            return None
        if (first.not_noun_phrase): 
            if (((typ & (((NounPhraseParseAttr.IGNOREPARTICIPLES | NounPhraseParseAttr.REFERENTCANBENOUN | NounPhraseParseAttr.PARSEPRONOUNS) | NounPhraseParseAttr.PARSEADVERBS | NounPhraseParseAttr.PARSENUMERICASADJECTIVE)))) == NounPhraseParseAttr.NO): 
                return None
        cou = 0
        t = first
        while t is not None: 
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if (t.morph.language.is_cyrillic or ((isinstance(t, NumberToken) and t.morph.class0.is_adjective and not t.chars.is_latin_letter)) or ((isinstance(t, ReferentToken) and ((typ & NounPhraseParseAttr.REFERENTCANBENOUN)) != NounPhraseParseAttr.NO))): 
                res = _NounPraseHelperInt.__try_parse_ru(first, typ, max_char_pos)
                if (res is None): 
                    first.not_noun_phrase = True
                return res
            elif (t.chars.is_latin_letter): 
                res = _NounPraseHelperInt.__try_parse_en(first, typ, max_char_pos)
                if (res is None): 
                    first.not_noun_phrase = True
                return res
            else: 
                cou += 1
                if ((cou) > 0): 
                    break
            t = t.next0
        return None
    
    @staticmethod
    def __try_parse_ru(first : 'Token', typ : 'NounPhraseParseAttr', max_char_pos : int) -> 'NounPhraseToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.internal.NounPhraseItem import NounPhraseItem
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.ner.core.NounPhraseToken import NounPhraseToken
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.ner.internal.NounPhraseItemTextVar import NounPhraseItemTextVar
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.Explanatory import Explanatory
        if (first is None): 
            return None
        items = None
        adverbs = None
        internal_noun_prase = None
        conj_before = False
        t = first
        first_pass2586 = True
        while True:
            if first_pass2586: first_pass2586 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if ((t.morph.class0.is_conjunction and not t.morph.class0.is_adjective and not t.morph.class0.is_pronoun) and not t.morph.class0.is_noun): 
                if (conj_before): 
                    break
                if (((typ & NounPhraseParseAttr.CANNOTHASCOMMAAND)) != NounPhraseParseAttr.NO): 
                    break
                if (items is not None and t.is_and): 
                    conj_before = True
                    continue
                break
            elif (t.is_comma): 
                if (conj_before or items is None): 
                    break
                mc = t.previous.get_morph_class_in_dictionary()
                if (mc.is_proper_surname or mc.is_proper_secname): 
                    break
                conj_before = True
                continue
            if (t.chars.is_latin_letter): 
                break
            if (isinstance(t, ReferentToken) and ((typ & NounPhraseParseAttr.REFERENTCANBENOUN)) == NounPhraseParseAttr.NO): 
                break
            it = NounPhraseItem.try_parse(t, items, typ)
            if (it is None or ((not it.can_be_adj and not it.can_be_noun))): 
                if (((typ & NounPhraseParseAttr.PARSEADVERBS)) != NounPhraseParseAttr.NO and isinstance(t, TextToken) and t.morph.class0.is_adverb): 
                    if (items is None): 
                        if (t.previous is not None and t.previous.morph.class0.is_preposition): 
                            pass
                        else: 
                            return None
                    if (adverbs is None): 
                        adverbs = list()
                    adverbs.append(t if isinstance(t, TextToken) else None)
                    continue
                break
            it.conj_before = conj_before
            conj_before = False
            if (not it.can_be_adj and not it.can_be_noun): 
                break
            if (t.is_newline_before): 
                if (((typ & NounPhraseParseAttr.MULTILINES)) != NounPhraseParseAttr.NO): 
                    pass
                elif (items is not None and t.chars != items[len(items) - 1].chars): 
                    if (t.chars.is_all_lower and items[len(items) - 1].chars.is_capital_upper): 
                        pass
                    else: 
                        break
            if (items is None): 
                items = list()
            else: 
                it0 = items[len(items) - 1]
                if (it0.can_be_noun and it0.is_personal_pronoun): 
                    if (it.is_pronoun): 
                        break
                    if (it0.begin_token.previous is not None and it0.begin_token.previous.get_morph_class_in_dictionary().is_verb and not it0.begin_token.previous.get_morph_class_in_dictionary().is_adjective): 
                        if (t.morph.case.is_nominative or t.morph.case.is_accusative): 
                            pass
                        else: 
                            break
                    if (it.can_be_noun and it.is_verb): 
                        break
            items.append(it)
            t = it.end_token
            if (t.is_newline_after and not t.chars.is_all_lower): 
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_proper_surname): 
                    break
                if (t.morph.class0.is_proper_surname and mc.is_undefined): 
                    break
        if (items is None): 
            return None
        if (len(items) == 1 and items[0].can_be_adj): 
            and0 = False
            tt1 = items[0].end_token.next0
            first_pass2587 = True
            while True:
                if first_pass2587: first_pass2587 = False
                else: tt1 = tt1.next0
                if (not (tt1 is not None)): break
                if (tt1.is_and or tt1.is_or): 
                    and0 = True
                    break
                if (tt1.is_comma or tt1.is_value("НО", None) or tt1.is_value("ТАК", None)): 
                    continue
                break
            if (and0): 
                if (items[0].can_be_noun and items[0].is_personal_pronoun): 
                    and0 = False
            if (and0): 
                tt2 = tt1.next0
                if (tt2 is not None and tt2.morph.class0.is_preposition): 
                    tt2 = tt2.next0
                npt1 = _NounPraseHelperInt.__try_parse_ru(tt2, typ, max_char_pos)
                if (npt1 is not None and len(npt1.adjectives) > 0): 
                    ok1 = False
                    for av in items[0].adj_morph: 
                        for v in (npt1.noun if isinstance(npt1.noun, NounPhraseItem) else None).noun_morph: 
                            if (v.check_accord(av, False)): 
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
            elif (it.can_be_noun and it.is_personal_pronoun): 
                check = False
                break
        tt1 = last1.end_token.next0
        if ((tt1 is not None and check and ((tt1.morph.class0.is_preposition or tt1.morph.case.is_instrumental))) and (tt1.whitespaces_before_count < 2)): 
            inp = NounPhraseHelper.try_parse(tt1, Utils.valToEnum(typ | NounPhraseParseAttr.PARSEPREPOSITION, NounPhraseParseAttr), max_char_pos)
            if (inp is not None): 
                tt1 = inp.end_token.next0
                npt1 = _NounPraseHelperInt.__try_parse_ru(tt1, typ, max_char_pos)
                if (npt1 is not None): 
                    ok = True
                    for it in items: 
                        if (not NounPhraseItem.try_accord_adj_and_noun(it, (npt1.noun if isinstance(npt1.noun, NounPhraseItem) else None))): 
                            ok = False
                            break
                    if (ok): 
                        for i in range(len(items)):
                            npt1.adjectives.insert(i, items[i])
                        npt1.internal_noun = inp
                        mmm = MorphCollection(npt1.morph)
                        for it in items: 
                            mmm.remove_items(it.adj_morph[0], False)
                        if (mmm.gender != MorphGender.UNDEFINED or mmm.number != MorphNumber.UNDEFINED or not mmm.case.is_undefined): 
                            npt1.morph = mmm
                        if (adverbs is not None): 
                            if (npt1.adverbs is None): 
                                npt1.adverbs = adverbs
                            else: 
                                npt1.adverbs[0:0] = adverbs
                        return npt1
                if (tt1 is not None and tt1.morph.class0.is_noun): 
                    it = NounPhraseItem.try_parse(tt1, items, typ)
                    if (it is not None and it.can_be_noun): 
                        internal_noun_prase = inp
                        inp.begin_token = items[0].end_token.next0
                        items.append(it)
        ok2 = False
        if ((len(items) == 1 and ((typ & NounPhraseParseAttr.ADJECTIVECANBELAST)) != NounPhraseParseAttr.NO and (items[0].whitespaces_after_count < 3)) and not items[0].is_adverb): 
            if (not items[0].can_be_adj): 
                ok2 = True
            elif (items[0].is_personal_pronoun and items[0].can_be_noun): 
                ok2 = True
        if (ok2): 
            it = NounPhraseItem.try_parse(items[0].end_token.next0, None, typ)
            if (it is not None and it.can_be_adj and it.begin_token.chars.is_all_lower): 
                ok2 = True
                if (it.is_adverb): 
                    ok2 = False
                if (it.is_pronoun and items[0].is_pronoun): 
                    ok2 = False
                    if (it.can_be_adj_for_personal_pronoun and items[0].is_personal_pronoun): 
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
                    if (items[i - 1].is_pronoun and items[i].is_pronoun): 
                        if (items[i].is_pronoun and items[i - 1].can_be_adj_for_personal_pronoun): 
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
        res.noun = noun
        res.internal_noun = internal_noun_prase
        for v in noun.noun_morph: 
            noun.morph.add_item(v)
        res.morph = noun.morph
        if (res.morph.case.is_nominative and first.previous is not None and first.previous.morph.class0.is_preposition): 
            res.morph.case ^= MorphCase.NOMINATIVE
        if (((typ & NounPhraseParseAttr.PARSEPRONOUNS)) == NounPhraseParseAttr.NO and ((res.morph.class0.is_pronoun or res.morph.class0.is_personal_pronoun))): 
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
                for i in range(len(items)):
                    ok = False
                    for av in items[i].adj_morph: 
                        if (v.check_accord(av, False)): 
                            ok = True
                            if (not (av.case & v.case).is_undefined and av.case != v.case): 
                                av.case = av.case & v.case
                                v.case = av.case
                            break
                    if (not ok): 
                        if (items[i].can_be_numeric_adj and items[i].try_accord_var(v)): 
                            ok = True
                            v = (v.clone() if isinstance(v.clone(), NounPhraseItemTextVar) else None)
                            v.number = MorphNumber.PLURAL
                            is_num_not = True
                            v.case = MorphCase()
                            for a in items[i].adj_morph: 
                                v.case |= a.case
                        else: 
                            break
                else: i = len(items)
                if (i >= len(items)): 
                    ok_list.append(v)
            if (len(ok_list) > 0 and (((len(ok_list) < res.morph.items_count) or is_num_not))): 
                res.morph = MorphCollection()
                for v in ok_list: 
                    res.morph.add_item(v)
                if (not is_num_not): 
                    noun.morph = res.morph
        for i in range(len(items)):
            for av in items[i].adj_morph: 
                for v in noun.noun_morph: 
                    if (v.check_accord(av, False)): 
                        if (not (av.case & v.case).is_undefined and av.case != v.case): 
                            av.case = av.case & v.case
                            v.case = av.case
                            need_update_morph = True
                        items[i].morph.add_item(av)
                        if (stat is not None and len(av.normal_value) > 1): 
                            last = av.normal_value[len(av.normal_value) - 1]
                            if (not last in stat): 
                                stat[last] = 1
                            else: 
                                stat[last] += 1
            if (items[i].is_pronoun or items[i].is_personal_pronoun): 
                res.anafor = items[i].begin_token
                if (((typ & NounPhraseParseAttr.PARSEPRONOUNS)) == NounPhraseParseAttr.NO): 
                    continue
            tt = (items[i].begin_token if isinstance(items[i].begin_token, TextToken) else None)
            if (tt is not None and not tt.term.startswith("ВЫСШ")): 
                err = False
                for wf in tt.morph.items: 
                    if (wf.class0.is_adjective): 
                        if (wf.contains_attr("прев.", MorphClass())): 
                            if (((typ & NounPhraseParseAttr.IGNOREADJBEST)) != NounPhraseParseAttr.NO): 
                                err = True
                        if (wf.contains_attr("к.ф.", MorphClass()) and tt.morph.class0.is_personal_pronoun): 
                            return None
                if (err): 
                    continue
            if (res.morph.case.is_nominative): 
                v = MiscHelper.get_text_value_of_meta_token(items[i], GetTextAttr.KEEPQUOTES)
                if (not Utils.isNullOrEmpty(v)): 
                    if (items[i].get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False) != v): 
                        wf = NounPhraseItemTextVar(items[i].morph, None)
                        wf.normal_value = v
                        wf.class0 = MorphClass.ADJECTIVE
                        wf.case = res.morph.case
                        if (res.morph.case.is_prepositional or res.morph.gender == MorphGender.NEUTER or res.morph.gender == MorphGender.FEMINIE): 
                            items[i].morph.add_item(wf)
                        else: 
                            items[i].morph.insert_item(0, wf)
            res.adjectives.append(items[i])
            if (items[i].end_char > res.end_char): 
                res.end_token = items[i].end_token
        i = 0
        first_pass2588 = True
        while True:
            if first_pass2588: first_pass2588 = False
            else: i += 1
            if (not (i < (len(res.adjectives) - 1))): break
            if (res.adjectives[i].whitespaces_after_count > 5): 
                if (res.adjectives[i].chars != res.adjectives[i + 1].chars): 
                    if (not res.adjectives[i + 1].chars.is_all_lower): 
                        return None
                    if (res.adjectives[i].chars.is_all_upper and res.adjectives[i + 1].chars.is_capital_upper): 
                        return None
                    if (res.adjectives[i].chars.is_capital_upper and res.adjectives[i + 1].chars.is_all_upper): 
                        return None
                if (res.adjectives[i].whitespaces_after_count > 10): 
                    if (res.adjectives[i].newlines_after_count == 1): 
                        if (res.adjectives[i].chars.is_capital_upper and i == 0 and res.adjectives[i + 1].chars.is_all_lower): 
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
                if (noun.begin_token.previous.is_comma_and): 
                    if (res.adjectives[0].begin_char > noun.begin_char): 
                        pass
                    else: 
                        return None
            zap = 0
            and0 = 0
            cou = 0
            last_and = False
            i = 0
            while i < (len(res.adjectives) - 1): 
                te = res.adjectives[i].end_token.next0
                if (te is None): 
                    return None
                if (te.is_comma): 
                    zap += 1
                elif (te.is_and): 
                    and0 += 1
                    if (i == (len(res.adjectives) - 2)): 
                        last_and = True
                if (not res.adjectives[i].begin_token.morph.class0.is_pronoun): 
                    cou += 1
                i += 1
            if ((zap + and0) > 0): 
                if (and0 > 1): 
                    return None
                elif (and0 == 1 and not last_and): 
                    return None
                if ((zap + and0) != cou): 
                    if (and0 == 1): 
                        pass
                    else: 
                        return None
                last = (res.adjectives[len(res.adjectives) - 1] if isinstance(res.adjectives[len(res.adjectives) - 1], NounPhraseItem) else None)
                if (last.is_pronoun and not last_and): 
                    return None
        if (stat is not None): 
            for adj in items: 
                if (adj.morph.items_count > 1): 
                    w1 = (adj.morph.get_indexer_item(0) if isinstance(adj.morph.get_indexer_item(0), NounPhraseItemTextVar) else None)
                    w2 = (adj.morph.get_indexer_item(1) if isinstance(adj.morph.get_indexer_item(1), NounPhraseItemTextVar) else None)
                    if ((len(w1.normal_value) < 2) or (len(w2.normal_value) < 2)): 
                        break
                    l1 = w1.normal_value[len(w1.normal_value) - 1]
                    l2 = w2.normal_value[len(w2.normal_value) - 1]
                    i1 = 0
                    i2 = 0
                    inoutarg471 = RefOutArgWrapper(None)
                    Utils.tryGetValue0(stat, l1, inoutarg471)
                    i1 = inoutarg471.value
                    inoutarg470 = RefOutArgWrapper(None)
                    Utils.tryGetValue0(stat, l2, inoutarg470)
                    i2 = inoutarg470.value
                    if (i1 < i2): 
                        adj.morph.remove_item(1)
                        adj.morph.insert_item(0, w2)
        if (res.begin_token.get_morph_class_in_dictionary().is_verb and len(items) > 0): 
            if (not res.begin_token.chars.is_all_lower or res.begin_token.previous is None): 
                pass
            elif (res.begin_token.previous.morph.class0.is_preposition): 
                pass
            else: 
                comma = False
                tt = res.begin_token.previous
                first_pass2589 = True
                while True:
                    if first_pass2589: first_pass2589 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.morph.class0.is_adverb): 
                        continue
                    if (tt.is_char_of(".;")): 
                        break
                    if (tt.is_comma): 
                        comma = True
                        continue
                    if (tt.is_value("НЕ", None)): 
                        continue
                    if (((tt.morph.class0.is_noun or tt.morph.class0.is_proper)) and comma): 
                        for it in res.begin_token.morph.items: 
                            if (it.class0.is_verb and isinstance(it, MorphWordForm)): 
                                if (tt.morph.check_accord(it, False)): 
                                    if (res.morph.case.is_instrumental): 
                                        return None
                                    ews = Explanatory.find_words((it if isinstance(it, MorphWordForm) else None).normal_case, tt.morph.language)
                                    if (ews is not None): 
                                        for ew in ews: 
                                            if (ew.nexts is not None): 
                                                inoutarg472 = RefOutArgWrapper(None)
                                                inoutres473 = Utils.tryGetValue(ew.nexts, "", inoutarg472)
                                                cm = inoutarg472.value
                                                if (inoutres473): 
                                                    if (not (cm & res.morph.case).is_undefined): 
                                                        return None
                    break
        if (res.begin_token == res.end_token): 
            mc = res.begin_token.get_morph_class_in_dictionary()
            if (mc.is_adverb): 
                if (res.begin_token.previous is not None and res.begin_token.previous.morph.class0.is_preposition): 
                    pass
                elif (mc.is_noun and not mc.is_preposition and not mc.is_conjunction): 
                    pass
                elif (res.begin_token.is_value("ВЕСЬ", None)): 
                    pass
                else: 
                    return None
        return res
    
    @staticmethod
    def __try_parse_en(first : 'Token', typ : 'NounPhraseParseAttr', max_char_pos : int) -> 'NounPhraseToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.internal.NounPhraseItem import NounPhraseItem
        from pullenti.ner.core.NounPhraseToken import NounPhraseToken
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.morph.MorphClass import MorphClass
        if (first is None): 
            return None
        items = None
        has_article = False
        has_prop = False
        has_misc = False
        if (first.previous is not None and first.previous.morph.class0.is_preposition and (first.whitespaces_before_count < 3)): 
            has_prop = True
        t = first
        first_pass2590 = True
        while True:
            if first_pass2590: first_pass2590 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if (not t.chars.is_latin_letter): 
                break
            if (t != first and t.whitespaces_before_count > 2): 
                if (((typ & NounPhraseParseAttr.MULTILINES)) != NounPhraseParseAttr.NO): 
                    pass
                else: 
                    break
            tt = (t if isinstance(t, TextToken) else None)
            if (t == first and tt is not None): 
                if (MiscHelper.is_eng_article(tt)): 
                    has_article = True
                    continue
            if (isinstance(t, ReferentToken) and ((typ & NounPhraseParseAttr.REFERENTCANBENOUN)) == NounPhraseParseAttr.NO): 
                break
            if (tt is None): 
                break
            mc = t.get_morph_class_in_dictionary()
            if (mc.is_conjunction or mc.is_preposition): 
                break
            if (mc.is_pronoun or mc.is_personal_pronoun): 
                if (((typ & NounPhraseParseAttr.PARSEPRONOUNS)) == NounPhraseParseAttr.NO): 
                    break
            elif (mc.is_misc): 
                if (t.is_value("THIS", None) or t.is_value("THAT", None)): 
                    has_misc = True
                    if (((typ & NounPhraseParseAttr.PARSEPRONOUNS)) == NounPhraseParseAttr.NO): 
                        break
            if (((has_article or has_prop or has_misc)) and items is None): 
                pass
            else: 
                if (not mc.is_noun and not mc.is_adjective): 
                    if (mc.is_undefined and has_article): 
                        pass
                    elif (items is None and mc.is_undefined and t.chars.is_capital_upper): 
                        pass
                    elif (mc.is_pronoun): 
                        pass
                    else: 
                        break
                if (mc.is_verb): 
                    if (t.next0 is not None and t.next0.morph.class0.is_verb and (t.whitespaces_after_count < 2)): 
                        pass
                    elif (t.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(t)): 
                        pass
                    elif ((t.chars.is_capital_upper and mc.is_noun and isinstance(t.next0, TextToken)) and t.next0.chars.is_capital_upper): 
                        pass
                    else: 
                        break
            if (items is None): 
                items = list()
            it = NounPhraseItem(t, t)
            if (mc.is_noun): 
                it.can_be_noun = True
            if (mc.is_adjective or mc.is_pronoun): 
                it.can_be_adj = True
            items.append(it)
            t = it.end_token
            if (len(items) == 1): 
                if (MiscHelper.is_eng_adj_suffix(t.next0)): 
                    mc.is_noun = False
                    mc.is_adjective = True
                    t = t.next0.next0
        if (items is None): 
            return None
        noun = items[len(items) - 1]
        res = NounPhraseToken(first, noun.end_token)
        res.noun = noun
        res.morph = MorphCollection()
        for v in noun.end_token.morph.items: 
            if (v.class0.is_verb): 
                continue
            if (v.class0.is_proper and noun.begin_token.chars.is_all_lower): 
                continue
            vv = (v.clone() if isinstance(v.clone(), MorphBaseInfo) else None)
            if (has_article and vv.number != MorphNumber.SINGULAR): 
                vv.number = MorphNumber.SINGULAR
            res.morph.add_item(vv)
        if (res.morph.items_count == 0 and has_article): 
            res.morph.add_item(MorphBaseInfo._new210(MorphClass.NOUN, MorphNumber.SINGULAR))
        i = 0
        while i < (len(items) - 1): 
            res.adjectives.append(items[i])
            i += 1
        return res