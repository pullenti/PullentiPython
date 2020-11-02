# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.semantic.utils.ControlModelQuestion import ControlModelQuestion
from pullenti.semantic.utils.ControlModelItemType import ControlModelItemType
from pullenti.ner.MetaToken import MetaToken
from pullenti.semantic.core.SemanticAbstractSlave import SemanticAbstractSlave
from pullenti.semantic.core.SemanticRole import SemanticRole
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.semantic.core.SemanticLink import SemanticLink
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseToken import NounPhraseToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.ner.core.VerbPhraseItemToken import VerbPhraseItemToken

class SemanticHelper:
    """ Полезные фукнции для семантического анализа
    
    Хелпер семантики
    """
    
    @staticmethod
    def get_keyword(mt : 'MetaToken') -> str:
        vpt = Utils.asObjectOrNull(mt, VerbPhraseToken)
        if (vpt is not None): 
            return Utils.ifNotNull(vpt.last_verb.verb_morph.normal_full, vpt.last_verb.verb_morph.normal_case)
        npt = Utils.asObjectOrNull(mt, NounPhraseToken)
        if (npt is not None): 
            return npt.noun.end_token.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
        return None
    
    @staticmethod
    def find_derivates(t : 'Token') -> typing.List['DerivateGroup']:
        res = None
        cla = None
        if (isinstance(t, NounPhraseToken)): 
            t = t.noun.end_token
            cla = MorphClass.NOUN
        if (isinstance(t, TextToken)): 
            for f in t.morph.items: 
                if (isinstance(f, MorphWordForm)): 
                    if (cla is not None): 
                        if (((cla) & f.class0_).is_undefined): 
                            continue
                    res = DerivateService.find_derivates(Utils.ifNotNull(f.normal_full, f.normal_case), True, None)
                    if (res is not None and len(res) > 0): 
                        return res
            return None
        if (isinstance(t, VerbPhraseToken)): 
            return SemanticHelper.find_derivates(t.last_verb)
        if (isinstance(t, VerbPhraseItemToken)): 
            vpt = Utils.asObjectOrNull(t, VerbPhraseItemToken)
            if (vpt.verb_morph is not None): 
                res = DerivateService.find_derivates(vpt.verb_morph.normal_case, True, t.morph.language)
                if (res is None or (len(res) == 0 and vpt.verb_morph.normal_full is not None and vpt.verb_morph.normal_case != vpt.verb_morph.normal_full)): 
                    res = DerivateService.find_derivates(vpt.verb_morph.normal_full, True, t.morph.language)
            return res
        if (isinstance(t, NumberToken)): 
            if (t.value == "1"): 
                return DerivateService.find_derivates("ОДИН", True, MorphLang.RU)
        if (isinstance(t, MetaToken)): 
            return SemanticHelper.find_derivates(t.end_token)
        return None
    
    @staticmethod
    def find_word_in_group(mt : 'MetaToken', gr : 'DerivateGroup') -> 'DerivateWord':
        if (gr is None or mt is None): 
            return None
        t = None
        if (isinstance(mt, NounPhraseToken)): 
            t = mt.noun.end_token
        elif ((isinstance(mt, SemanticAbstractSlave)) and (isinstance(mt.source, NounPhraseToken))): 
            t = mt.source.noun.end_token
        else: 
            t = mt.end_token
        for w in gr.words: 
            if (w.class0_ is not None and w.class0_.is_noun and w.lang.is_ru): 
                if (t.is_value(w.spelling, None)): 
                    return w
        return None
    
    @staticmethod
    def __find_control_item(mt : 'MetaToken', gr : 'DerivateGroup') -> 'ControlModelItem':
        if (gr is None): 
            return None
        if (isinstance(mt, NounPhraseToken)): 
            t = mt.noun.end_token
            for m in gr.model.items: 
                if (m.word is not None): 
                    if (t.is_value(m.word, None)): 
                        return m
            for w in gr.words: 
                if (w.attrs.is_verb_noun): 
                    if (t.is_value(w.spelling, None)): 
                        return gr.model.find_item_by_typ(ControlModelItemType.NOUN)
            return None
        if (isinstance(mt, VerbPhraseItemToken)): 
            ti = Utils.asObjectOrNull(mt, VerbPhraseItemToken)
            rev = ti.is_verb_reversive or ti.is_verb_passive
            for it in gr.model.items: 
                if (rev and it.typ == ControlModelItemType.REFLEXIVE): 
                    return it
                elif (not rev and it.typ == ControlModelItemType.VERB): 
                    return it
        return None
    
    @staticmethod
    def try_create_links(master : 'MetaToken', slave : 'MetaToken', onto : 'ISemanticOnto'=None) -> typing.List['SemanticLink']:
        """ Попробовать создать семантическую связь между элементами.
        Элементом м.б. именная (NounPhraseToken) или глагольная группа (VerbPhraseToken).
        
        Args:
            master(MetaToken): основной элемент
            slave(MetaToken): стыкуемый элемент (также м.б. SemanticAbstractSlave)
            onto(ISemanticOnto): дополнительный онтологический словарь
        
        Returns:
            typing.List[SemanticLink]: список вариантов (возможно, пустой)
        
        """
        res = list()
        vpt1 = Utils.asObjectOrNull(master, VerbPhraseToken)
        vpt2 = Utils.asObjectOrNull(slave, VerbPhraseToken)
        npt1 = Utils.asObjectOrNull(master, NounPhraseToken)
        if (isinstance(slave, NounPhraseToken)): 
            slave = (SemanticAbstractSlave.create_from_noun(Utils.asObjectOrNull(slave, NounPhraseToken)))
        sla2 = Utils.asObjectOrNull(slave, SemanticAbstractSlave)
        if (vpt2 is not None): 
            if (not vpt2.first_verb.is_verb_infinitive or not vpt2.last_verb.is_verb_infinitive): 
                return res
        grs = SemanticHelper.find_derivates(master)
        if (grs is None or len(grs) == 0): 
            rl = (SemanticHelper.__try_create_verb(vpt1, slave, None) if vpt1 is not None else SemanticHelper.__try_create_noun(npt1, slave, None))
            if (rl is not None): 
                res.extend(rl)
        else: 
            for gr in grs: 
                rl = (SemanticHelper.__try_create_verb(vpt1, slave, gr) if vpt1 is not None else SemanticHelper.__try_create_noun(npt1, slave, gr))
                if (rl is None or len(rl) == 0): 
                    continue
                res.extend(rl)
        if ((npt1 is not None and sla2 is not None and sla2.morph.case_.is_genitive) and sla2.preposition is None): 
            if (npt1.noun.begin_token.get_morph_class_in_dictionary().is_personal_pronoun): 
                pass
            else: 
                has_gen = False
                for r in res: 
                    if (r.question == ControlModelQuestion.get_base_genetive()): 
                        has_gen = True
                        break
                if (not has_gen): 
                    res.append(SemanticLink._new2869(True, npt1, sla2, 0.5, ControlModelQuestion.get_base_genetive()))
        if (onto is not None): 
            str1 = SemanticHelper.get_keyword(master)
            str2 = SemanticHelper.get_keyword(slave)
            if (str2 is not None): 
                if (onto.check_link(str1, str2)): 
                    if (len(res) > 0): 
                        for r in res: 
                            r.rank += (3)
                            if (r.role == SemanticRole.COMMON): 
                                r.role = SemanticRole.STRONG
                    else: 
                        res.append(SemanticLink._new2870(SemanticRole.STRONG, master, slave, 3))
        if (npt1 is not None): 
            if (((len(npt1.adjectives) > 0 and npt1.adjectives[0].begin_token.morph.class0_.is_pronoun)) or npt1.anafor is not None): 
                for r in res: 
                    if (r.question == ControlModelQuestion.get_base_genetive()): 
                        r.rank -= 0.5
                        if (r.role == SemanticRole.STRONG): 
                            r.role = SemanticRole.COMMON
        for r in res: 
            if (r.role == SemanticRole.STRONG): 
                for rr in res: 
                    if (rr != r and rr.role != SemanticRole.STRONG): 
                        rr.rank /= (2)
        i = 0
        while i < len(res): 
            j = 0
            while j < (len(res) - 1): 
                if (res[j].compareTo(res[j + 1]) > 0): 
                    r = res[j]
                    res[j] = res[j + 1]
                    res[j + 1] = r
                j += 1
            i += 1
        for r in res: 
            r.master = master
            r.slave = slave
        return res
    
    @staticmethod
    def __try_create_inf(master : 'MetaToken', vpt2 : 'VerbPhraseToken', gr : 'DerivateGroup') -> typing.List['SemanticLink']:
        cit = SemanticHelper.__find_control_item(master, gr)
        res = list()
        rol = Utils.valToEnum(None, SemanticRole)
        if (cit is not None and ControlModelQuestion.get_to_do() in cit.links): 
            rol = cit.links[ControlModelQuestion.get_to_do()]
        if (rol is not None): 
            res.append(SemanticLink._new2871((2 if rol != SemanticRole.COMMON else 1), ControlModelQuestion.get_to_do()))
        return res
    
    @staticmethod
    def __try_create_noun(npt1 : 'NounPhraseToken', slave : 'MetaToken', gr : 'DerivateGroup') -> typing.List['SemanticLink']:
        if (npt1 is None or slave is None): 
            return None
        if (isinstance(slave, VerbPhraseToken)): 
            return SemanticHelper.__try_create_inf(npt1, Utils.asObjectOrNull(slave, VerbPhraseToken), gr)
        sla2 = Utils.asObjectOrNull(slave, SemanticAbstractSlave)
        res = list()
        if (sla2 is None): 
            return res
        cit = SemanticHelper.__find_control_item(npt1, gr)
        SemanticHelper.__create_roles(cit, sla2.preposition, sla2.morph.case_, res, False, False)
        if (len(res) == 1 and res[0].role == SemanticRole.AGENT and res[0].question == ControlModelQuestion.get_base_instrumental()): 
            if (len(gr.model.items) > 0 and gr.model.items[0].typ == ControlModelItemType.VERB and ControlModelQuestion.get_base_instrumental() in gr.model.items[0].links): 
                res[0].role = gr.model.items[0].links[ControlModelQuestion.get_base_instrumental()]
        ok = False
        w = SemanticHelper.find_word_in_group(npt1, gr)
        if (w is not None and w.next_words is not None and len(w.next_words) > 0): 
            for n in w.next_words: 
                if (sla2.source is not None): 
                    if (sla2.source.end_token.is_value(n, None)): 
                        ok = True
                        break
        if (gr is not None and len(gr.model.pacients) > 0): 
            for n in gr.model.pacients: 
                if (sla2.source is not None): 
                    if (sla2.source.end_token.is_value(n, None)): 
                        ok = True
                        break
        if (ok): 
            if (len(res) == 0): 
                res.append(SemanticLink._new2872(ControlModelQuestion.get_base_genetive(), SemanticRole.PACIENT, True))
            for r in res: 
                r.rank += (4)
                if (r.role == SemanticRole.COMMON): 
                    r.role = SemanticRole.STRONG
                if (npt1.end_token.next0_ == sla2.begin_token): 
                    r.rank += (2)
                r.idiom = True
        return res
    
    @staticmethod
    def __try_create_verb(vpt1 : 'VerbPhraseToken', slave : 'MetaToken', gr : 'DerivateGroup') -> typing.List['SemanticLink']:
        if (isinstance(slave, VerbPhraseToken)): 
            return SemanticHelper.__try_create_inf(vpt1, Utils.asObjectOrNull(slave, VerbPhraseToken), gr)
        sla2 = Utils.asObjectOrNull(slave, SemanticAbstractSlave)
        res = list()
        if (sla2 is None): 
            return res
        cit = SemanticHelper.__find_control_item(vpt1.last_verb, gr)
        prep = sla2.preposition
        morph_ = sla2.morph
        is_rev1 = vpt1.last_verb.is_verb_reversive or vpt1.last_verb.is_verb_passive
        no_nomin = False
        no_instr = False
        if (prep is None and morph_.case_.is_nominative and not vpt1.first_verb.is_participle): 
            ok = True
            err = False
            vm = vpt1.first_verb.verb_morph
            if (vm is None): 
                return res
            if (vm.number == MorphNumber.SINGULAR): 
                if (morph_.number == MorphNumber.PLURAL): 
                    if (not vpt1.first_verb.is_verb_infinitive): 
                        ok = False
            if (not SemanticHelper.check_morph_accord(morph_, False, vm, False)): 
                if (not err and not vpt1.first_verb.is_verb_infinitive): 
                    ok = False
            elif (vm.misc.person != MorphPerson.UNDEFINED): 
                if (((vm.misc.person) & (MorphPerson.THIRD)) == (MorphPerson.UNDEFINED)): 
                    if (((vm.misc.person) & (MorphPerson.FIRST)) == (MorphPerson.FIRST)): 
                        if (not morph_.contains_attr("1 л.", None)): 
                            ok = False
                    if (((vm.misc.person) & (MorphPerson.SECOND)) == (MorphPerson.SECOND)): 
                        if (not morph_.contains_attr("2 л.", None)): 
                            ok = False
            no_nomin = True
            if (ok): 
                cit00 = cit
                is_rev0 = is_rev1
                if (vpt1.first_verb != vpt1.last_verb and ((vpt1.first_verb.is_verb_reversive or vpt1.first_verb.is_verb_passive or vpt1.first_verb.normal == "ИМЕТЬ"))): 
                    cit00 = (None)
                    is_rev0 = True
                    grs = SemanticHelper.find_derivates(vpt1.first_verb)
                    if (grs is not None): 
                        for gg in grs: 
                            cit00 = SemanticHelper.__find_control_item(vpt1.first_verb, gg)
                            if ((cit00) is not None): 
                                break
                sl = None
                addagent = False
                if (cit00 is None): 
                    sl = SemanticLink._new2873(True, (SemanticRole.PACIENT if is_rev0 else SemanticRole.AGENT), 1, ControlModelQuestion.get_base_nominative(), is_rev0)
                else: 
                    for kp in cit00.links.items(): 
                        q = kp[0]
                        if (q.check(None, MorphCase.NOMINATIVE)): 
                            sl = SemanticLink._new2874(kp[1], 2, q, is_rev0)
                            if (sl.role == SemanticRole.AGENT): 
                                sl.is_passive = False
                            elif (sl.role == SemanticRole.PACIENT and cit00.nominative_can_be_agent_and_pacient and vpt1.last_verb.is_verb_reversive): 
                                addagent = True
                            break
                if (sl is not None): 
                    if (cit00 is None and morph_.case_.is_instrumental and is_rev0): 
                        sl.rank -= 0.5
                    if (morph_.case_.is_accusative): 
                        sl.rank -= 0.5
                    if (sla2.begin_char > vpt1.begin_char): 
                        sl.rank -= 0.5
                    if (err): 
                        sl.rank -= 0.5
                    res.append(sl)
                    if (addagent): 
                        res.append(SemanticLink._new2875(SemanticRole.AGENT, sl.rank, sl.question))
        if (prep is None and is_rev1 and morph_.case_.is_instrumental): 
            no_instr = True
            cit00 = cit
            sl = None
            if (cit00 is None): 
                sl = SemanticLink._new2873(True, SemanticRole.AGENT, 1, ControlModelQuestion.get_base_instrumental(), True)
            else: 
                for kp in cit00.links.items(): 
                    q = kp[0]
                    if (q.check(None, MorphCase.INSTRUMENTAL)): 
                        sl = SemanticLink._new2875(kp[1], 2, q)
                        if (sl.role == SemanticRole.AGENT): 
                            sl.is_passive = True
                        break
            if (sl is not None): 
                if (cit00 is None and morph_.case_.is_nominative): 
                    sl.rank -= 0.5
                if (morph_.case_.is_accusative): 
                    sl.rank -= 0.5
                if (sla2.begin_char < vpt1.begin_char): 
                    sl.rank -= 0.5
                res.append(sl)
                if ((gr is not None and len(gr.model.items) > 0 and gr.model.items[0].typ == ControlModelItemType.VERB) and ControlModelQuestion.get_base_instrumental() in gr.model.items[0].links): 
                    sl.rank = (0)
                    sl0 = SemanticLink._new2878(sl.question, 1, gr.model.items[0].links[ControlModelQuestion.get_base_instrumental()])
                    res.insert(0, sl0)
        if (prep is None and morph_.case_.is_dative and ((cit is None or not ControlModelQuestion.get_base_dative() in cit.links))): 
            sl = SemanticLink._new2879(cit is None, SemanticRole.STRONG, 1, ControlModelQuestion.get_base_dative())
            if (morph_.case_.is_accusative or morph_.case_.is_nominative): 
                sl.rank -= 0.5
            if (vpt1.end_token.next0_ != sla2.begin_token): 
                sl.rank -= 0.5
            if (cit is not None): 
                sl.rank -= 0.5
            res.append(sl)
        SemanticHelper.__create_roles(cit, prep, morph_.case_, res, no_nomin, no_instr)
        if (gr is not None and len(gr.model.pacients) > 0): 
            ok = False
            for n in gr.model.pacients: 
                if (sla2.source is not None): 
                    if (sla2.source.end_token.is_value(n, None)): 
                        ok = True
                        break
                elif (sla2.end_token.is_value(n, None)): 
                    ok = True
                    break
            if (ok): 
                if (len(res) == 0): 
                    ok = False
                    if (prep is None and is_rev1 and morph_.case_.is_nominative): 
                        ok = True
                    elif (prep is None and not is_rev1 and morph_.case_.is_accusative): 
                        ok = True
                    if (ok): 
                        res.append(SemanticLink._new2880(SemanticRole.PACIENT, (ControlModelQuestion.get_base_nominative() if is_rev1 else ControlModelQuestion.get_base_accusative()), True))
                else: 
                    for r in res: 
                        r.rank += (4)
                        if (r.role == SemanticRole.COMMON): 
                            r.role = SemanticRole.STRONG
                        if (vpt1.end_token.next0_ == sla2.begin_token): 
                            r.rank += (2)
                        r.idiom = True
        return res
    
    @staticmethod
    def __create_roles(cit : 'ControlModelItem', prep : str, cas : 'MorphCase', res : typing.List['SemanticLink'], ignore_nomin_case : bool=False, ignore_instr_case : bool=False) -> None:
        if (cit is None): 
            return
        roles = None
        for li in cit.links.items(): 
            q = li[0]
            if (q.check(prep, cas)): 
                if (ignore_nomin_case and q.case_.is_nominative and q.preposition is None): 
                    continue
                if (ignore_instr_case and q.case_.is_instrumental and q.preposition is None): 
                    continue
                if (roles is None): 
                    roles = dict()
                r = li[1]
                if (q.is_abstract): 
                    qq = q.check_abstract(prep, cas)
                    if (qq is not None): 
                        q = qq
                        r = SemanticRole.COMMON
                if (not q in roles): 
                    roles[q] = r
                elif (r != SemanticRole.COMMON): 
                    roles[q] = r
        if (roles is not None): 
            for kp in roles.items(): 
                sl = SemanticLink._new2875(kp[1], 2, kp[0])
                if (kp[1] == SemanticRole.AGENT): 
                    if (not kp[0].is_base): 
                        sl.role = SemanticRole.COMMON
                if (sl.role == SemanticRole.STRONG): 
                    sl.rank += (2)
                res.append(sl)
    
    @staticmethod
    def check_morph_accord(m : 'MorphBaseInfo', plural : bool, vf : 'MorphBaseInfo', check_case : bool=False) -> bool:
        if (check_case and not m.case_.is_undefined and not vf.case_.is_undefined): 
            if (((m.case_) & vf.case_).is_undefined): 
                return False
        coef = 0
        if (vf.number == MorphNumber.PLURAL): 
            if (plural): 
                coef += 1
            elif (m.number != MorphNumber.UNDEFINED): 
                if (((m.number) & (MorphNumber.PLURAL)) == (MorphNumber.PLURAL)): 
                    coef += 1
                else: 
                    return False
        elif (vf.number == MorphNumber.SINGULAR): 
            if (plural): 
                return False
            if (m.number != MorphNumber.UNDEFINED): 
                if (((m.number) & (MorphNumber.SINGULAR)) == (MorphNumber.SINGULAR)): 
                    coef += 1
                else: 
                    return False
            if (m.gender != MorphGender.UNDEFINED): 
                if (vf.gender != MorphGender.UNDEFINED): 
                    if (m.gender == MorphGender.FEMINIE): 
                        if (((vf.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                            coef += 1
                        else: 
                            return False
                    elif (((m.gender) & (vf.gender)) != (MorphGender.UNDEFINED)): 
                        coef += 1
                    elif (m.gender == MorphGender.MASCULINE and vf.gender == MorphGender.FEMINIE): 
                        pass
                    else: 
                        return False
        return coef >= 0