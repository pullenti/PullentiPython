# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.morph.MorphGender import MorphGender
from pullenti.semantic.SemObject import SemObject
from pullenti.morph.MorphClass import MorphClass
from pullenti.semantic.SemObjectType import SemObjectType
from pullenti.semantic.SemLinkType import SemLinkType
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.semantic.internal.AnaforHelper import AnaforHelper
from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken

class OptimizerHelper:
    
    @staticmethod
    def optimize(doc : 'SemDocument', pars : 'SemProcessParams') -> None:
        for blk in doc.blocks: 
            for fr in blk.fragments: 
                OptimizerHelper.__optimize_graph(fr.graph)
            objs = list()
            objs.extend(blk.graph.objects)
            for fr in blk.fragments: 
                objs.extend(fr.graph.objects)
            for fr in blk.fragments: 
                for i in range(len(fr.graph.links) - 1, -1, -1):
                    li = fr.graph.links[i]
                    if (not li.source in objs or not li.target in objs): 
                        fr.graph.remove_link(li)
                OptimizerHelper.__process_participles(fr.graph)
                OptimizerHelper.__process_links(fr.graph)
            OptimizerHelper.__sort_objects(objs)
            OptimizerHelper.__process_pointers(objs)
            OptimizerHelper.__process_formulas(objs)
            if (pars.dont_create_anafor): 
                pass
            else: 
                AnaforHelper.process_anafors(objs)
                for fr in blk.fragments: 
                    OptimizerHelper.__collapse_anafors(fr.graph)
    
    @staticmethod
    def __optimize_graph(gr : 'SemGraph') -> None:
        for o in gr.objects: 
            OptimizerHelper.__optimize_tokens(o)
        OptimizerHelper.__sort_objects(gr.objects)
    
    @staticmethod
    def __compare_toks(t1 : 'Token', t2 : 'Token') -> int:
        if (t1.begin_char < t2.begin_char): 
            return -1
        if (t1.begin_char > t2.begin_char): 
            return 1
        if (t1.end_char < t2.end_char): 
            return -1
        if (t1.end_char > t2.end_char): 
            return 1
        return 0
    
    @staticmethod
    def __optimize_tokens(o : 'SemObject') -> None:
        i = 0
        while i < len(o.tokens): 
            ch = False
            j = 0
            while j < (len(o.tokens) - 1): 
                if (OptimizerHelper.__compare_toks(o.tokens[j], o.tokens[j + 1]) > 0): 
                    t = o.tokens[j]
                    o.tokens[j] = o.tokens[j + 1]
                    o.tokens[j + 1] = t
                    ch = True
                j += 1
            if (not ch): 
                break
            i += 1
        i = 0
        while i < (len(o.tokens) - 1): 
            if (o.tokens[i].end_token.next0_ == o.tokens[i + 1].begin_token): 
                o.tokens[i] = MetaToken(o.tokens[i].begin_token, o.tokens[i + 1].end_token)
                del o.tokens[i + 1]
                i -= 1
            i += 1
    
    @staticmethod
    def __sort_objects(objs : typing.List['SemObject']) -> None:
        i = 0
        while i < len(objs): 
            ch = False
            j = 0
            while j < (len(objs) - 1): 
                if (objs[j].compareTo(objs[j + 1]) > 0): 
                    o = objs[j]
                    objs[j] = objs[j + 1]
                    objs[j + 1] = o
                    ch = True
                j += 1
            if (not ch): 
                break
            i += 1
    
    @staticmethod
    def __process_participles(gr : 'SemGraph') -> bool:
        ret = False
        i = 0
        first_pass3944 = True
        while True:
            if first_pass3944: first_pass3944 = False
            else: i += 1
            if (not (i < len(gr.objects))): break
            obj = gr.objects[i]
            if (obj.typ != SemObjectType.PARTICIPLE): 
                continue
            own = None
            has = False
            for li in obj.links_to: 
                if (li.typ == SemLinkType.PARTICIPLE): 
                    own = li
                else: 
                    has = True
            if (not has): 
                continue
            if (own is None): 
                dum = SemObject._new2929(gr, SemObjectType.NOUN)
                if (obj.morph is not None): 
                    dum.morph = MorphWordForm._new2930(MorphClass.NOUN, obj.morph.number, obj.morph.gender, obj.morph.case_)
                gr.objects.append(dum)
                own = gr.add_link(SemLinkType.PARTICIPLE, dum, obj, "какой", False, None)
                ret = True
            for j in range(len(obj.links_to) - 1, -1, -1):
                li = obj.links_to[j]
                if (li.typ == SemLinkType.PARTICIPLE): 
                    continue
                exi = False
                for ll in li.source.links_from: 
                    if (ll.target == own.source): 
                        exi = True
                if (exi): 
                    gr.remove_link(li)
                else: 
                    del obj.links_to[j]
                    li._m_target = own.source
                ret = True
        return ret
    
    @staticmethod
    def __process_links(gr : 'SemGraph') -> bool:
        ret = False
        i = 0
        while i < len(gr.objects): 
            obj = gr.objects[i]
            for j in range(len(obj.links_from) - 1, -1, -1):
                li = obj.links_from[j]
                if (li.typ != SemLinkType.PACIENT): 
                    continue
                exi = False
                for ll in obj.links_from: 
                    if (ll != li and ll.typ == SemLinkType.AGENT and ll.target == li.target): 
                        exi = True
                if (exi): 
                    if (obj.begin_char > li.target.begin_char): 
                        gr.remove_link(li)
                        ret = True
            i += 1
        return ret
    
    @staticmethod
    def __collapse_anafors(gr : 'SemGraph') -> bool:
        ret = False
        i = 0
        first_pass3945 = True
        while True:
            if first_pass3945: first_pass3945 = False
            else: i += 1
            if (not (i < len(gr.objects))): break
            obj = gr.objects[i]
            if (obj.typ == SemObjectType.PERSONALPRONOUN or obj.morph.normal_full == "КОТОРЫЙ"): 
                pass
            else: 
                continue
            if (len(obj.attrs) > 0 or obj.quantity is not None): 
                continue
            if (len(obj.links_from) == 1 and obj.links_from[0].typ == SemLinkType.ANAFOR): 
                pass
            elif (len(obj.links_from) == 2 and obj.links_from[0].typ == SemLinkType.ANAFOR and obj.links_from[0].alt_link == obj.links_from[1]): 
                pass
            else: 
                continue
            alink = obj.links_from[0]
            for li in obj.links_to: 
                nli = gr.add_link(li.typ, li.source, alink.target, li.question, li.is_or, li.preposition)
                if (alink.alt_link is not None): 
                    nli2 = gr.add_link(li.typ, li.source, alink.alt_link.target, li.question, li.is_or, li.preposition)
                    nli2.alt_link = nli
                    nli.alt_link = nli2
            gr.remove_object(obj)
            i -= 1
            ret = True
        return ret
    
    @staticmethod
    def __process_formulas(objs : typing.List['SemObject']) -> bool:
        ret = False
        i = 0
        first_pass3946 = True
        while True:
            if first_pass3946: first_pass3946 = False
            else: i += 1
            if (not (i < len(objs))): break
            o = objs[i]
            if (o.typ != SemObjectType.NOUN or not o.is_value("РАЗ", SemObjectType.UNDEFINED)): 
                continue
            if (o.quantity is None): 
                continue
            if (len(o.links_from) == 0 and len(o.links_to) == 1): 
                pass
            else: 
                continue
            frm = o.links_to[0].source
            for k in range(5):
                brek = False
                for li in frm.links_from: 
                    if (((li.typ == SemLinkType.DETAIL or li.typ == SemLinkType.PACIENT)) and li.target != o): 
                        if (o.begin_char > frm.end_char and (o.begin_char < li.target.begin_char)): 
                            brek = True
                            o.graph.add_link(SemLinkType.DETAIL, o, li.target, "чего", False, None)
                            o.graph.remove_link(li)
                        else: 
                            frm = li.target
                        break
                if (brek): 
                    break
        return ret
    
    @staticmethod
    def __process_pointers(objs : typing.List['SemObject']) -> bool:
        ret = False
        i = 0
        first_pass3947 = True
        while True:
            if first_pass3947: first_pass3947 = False
            else: i += 1
            if (not (i < len(objs))): break
            o = objs[i]
            if (o.typ != SemObjectType.NOUN): 
                continue
            if (o.quantity is not None and o.quantity.spelling == "1"): 
                pass
            else: 
                continue
            if (len(o.links_from) > 0): 
                continue
            ok = False
            for j in range(i - 1, -1, -1):
                oo = objs[j]
                if (oo.typ != SemObjectType.NOUN): 
                    continue
                if (oo.morph.normal_full != o.morph.normal_full): 
                    continue
                if (oo.quantity is not None and oo.quantity.spelling != "1"): 
                    ok = True
                    break
            if (not ok): 
                j = i + 1
                first_pass3948 = True
                while True:
                    if first_pass3948: first_pass3948 = False
                    else: j += 1
                    if (not (j < len(objs))): break
                    oo = objs[j]
                    if (oo.typ != SemObjectType.NOUN): 
                        continue
                    if (oo.morph.normal_full != o.morph.normal_full): 
                        continue
                    if (oo.find_from_object("ДРУГОЙ", SemLinkType.UNDEFINED, SemObjectType.UNDEFINED) is not None or oo.find_from_object("ВТОРОЙ", SemLinkType.UNDEFINED, SemObjectType.UNDEFINED) is not None): 
                        ok = True
                        break
            if (not ok): 
                continue
            first = SemObject._new2929(o.graph, SemObjectType.ADJECTIVE)
            first.tokens.append(o.tokens[0])
            first.morph.normal_full = "ПЕРВЫЙ"
            first.morph.normal_case = ("ПЕРВАЯ" if ((o.morph.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED) else ("ПЕРВОЕ" if ((o.morph.gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED) else "ПЕРВЫЙ"))
            first.morph.gender = o.morph.gender
            o.graph.objects.append(first)
            o.graph.add_link(SemLinkType.DETAIL, o, first, "какой", False, None)
            o.quantity = (None)
            ret = True
        i = 0
        first_pass3949 = True
        while True:
            if first_pass3949: first_pass3949 = False
            else: i += 1
            if (not (i < len(objs))): break
            o = objs[i]
            if (o.typ != SemObjectType.NOUN): 
                continue
            if (o.quantity is not None and o.quantity.spelling == "1"): 
                pass
            else: 
                continue
            other = o.find_from_object("ДРУГОЙ", SemLinkType.UNDEFINED, SemObjectType.UNDEFINED)
            if (other is None): 
                continue
            ok = False
            for j in range(i - 1, -1, -1):
                oo = objs[j]
                if (oo.typ != SemObjectType.NOUN): 
                    continue
                if (oo.morph.normal_full != o.morph.normal_full): 
                    continue
                if (oo.find_from_object("ПЕРВЫЙ", SemLinkType.UNDEFINED, SemObjectType.UNDEFINED) is not None): 
                    ok = True
                    break
            if (ok): 
                other.morph.normal_full = "ВТОРОЙ"
                other.morph.normal_case = ("ВТОРАЯ" if ((o.morph.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED) else ("ВТОРОЕ" if ((o.morph.gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED) else "ВТОРОЙ"))
        return ret