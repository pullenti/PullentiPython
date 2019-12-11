# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.DerivateWord import DerivateWord
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.NextModelQuestion import NextModelQuestion
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.DerivateGroup import DerivateGroup
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.internal.ExplanTreeNode import ExplanTreeNode

class DeserializeHelper:
    
    @staticmethod
    def deserializedd(str0_ : io.IOBase, dic : 'DerivateDictionary', lazy_load : bool) -> 'ByteArrayWrapper':
        wr = None
        with io.BytesIO() as tmp: 
            MorphSerializeHelper.deflate_gzip(str0_, tmp)
            wr = ByteArrayWrapper(bytearray(tmp.getvalue()))
            pos = 0
            wrappos9 = RefOutArgWrapper(pos)
            cou = wr.deserialize_int(wrappos9)
            pos = wrappos9.value
            while cou > 0: 
                wrappos7 = RefOutArgWrapper(pos)
                p1 = wr.deserialize_int(wrappos7)
                pos = wrappos7.value
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy_pos = pos
                    pos = p1
                else: 
                    wrappos6 = RefOutArgWrapper(pos)
                    DeserializeHelper.deserialize_derivate_group(wr, ew, wrappos6)
                    pos = wrappos6.value
                dic._m_all_groups.append(ew)
                cou -= 1
            dic._m_root = ExplanTreeNode()
            wrappos8 = RefOutArgWrapper(pos)
            DeserializeHelper.deserialize_tree_node(wr, dic, dic._m_root, lazy_load, wrappos8)
            pos = wrappos8.value
        return wr
    
    @staticmethod
    def deserialize_derivate_group(str0_ : 'ByteArrayWrapper', dg : 'DerivateGroup', pos : int) -> None:
        attr = str0_.deserialize_short(pos)
        if (((attr & 1)) != 0): 
            dg.is_dummy = True
        if (((attr & 2)) != 0): 
            dg.not_generate = True
        if (((attr & 4)) != 0): 
            dg.m_transitive = 0
        if (((attr & 8)) != 0): 
            dg.m_transitive = 1
        if (((attr & 0x10)) != 0): 
            dg.m_rev_agent_case = 0
        if (((attr & 0x20)) != 0): 
            dg.m_rev_agent_case = 1
        if (((attr & 0x40)) != 0): 
            dg.m_rev_agent_case = 2
        dg.questions = (Utils.valToEnum(str0_.deserialize_short(pos), NextModelQuestion))
        dg.questions_ref = (Utils.valToEnum(str0_.deserialize_short(pos), NextModelQuestion))
        dg.prefix = str0_.deserialize_string(pos)
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            w = DerivateWord(dg)
            w.spelling = str0_.deserialize_string(pos)
            w.class0_ = MorphClass()
            w.class0_.value = (str0_.deserialize_short(pos))
            w.lang = MorphLang._new10(str0_.deserialize_short(pos))
            w.attrs.value = (str0_.deserialize_short(pos))
            dg.words.append(w)
            cou -= 1
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            pref = Utils.ifNotNull(str0_.deserialize_string(pos), "")
            cas = MorphCase()
            cas.value = (str0_.deserialize_short(pos))
            if (dg.nexts is None): 
                dg.nexts = dict()
            dg.nexts[pref] = cas
            cou -= 1
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            pref = Utils.ifNotNull(str0_.deserialize_string(pos), "")
            cas = MorphCase()
            cas.value = (str0_.deserialize_short(pos))
            if (dg.nexts_ref is None): 
                dg.nexts_ref = dict()
            dg.nexts_ref[pref] = cas
            cou -= 1
    
    @staticmethod
    def deserialize_tree_node(str0_ : 'ByteArrayWrapper', dic : 'DerivateDictionary', tn : 'ExplanTreeNode', lazy_load : bool, pos : int) -> None:
        cou = str0_.deserialize_short(pos)
        li = (list() if cou > 1 else None)
        while cou > 0: 
            id0_ = str0_.deserialize_int(pos)
            if (id0_ > 0 and id0_ <= len(dic._m_all_groups)): 
                gr = dic._m_all_groups[id0_ - 1]
                if (gr._lazy_pos > 0): 
                    p0 = pos.value
                    pos.value = gr._lazy_pos
                    DeserializeHelper.deserialize_derivate_group(str0_, gr, pos)
                    gr._lazy_pos = 0
                    pos.value = p0
                if (li is not None): 
                    li.append(gr)
                else: 
                    tn.groups = (gr)
            cou -= 1
        if (li is not None): 
            tn.groups = (li)
        cou = str0_.deserialize_short(pos)
        if (cou == 0): 
            return
        while cou > 0: 
            ke = str0_.deserialize_short(pos)
            p1 = str0_.deserialize_int(pos)
            tn1 = ExplanTreeNode()
            if (tn.nodes is None): 
                tn.nodes = dict()
            if (not ke in tn.nodes): 
                tn.nodes[ke] = tn1
            if (lazy_load): 
                tn1.lazy_pos = pos.value
                pos.value = p1
            else: 
                DeserializeHelper.deserialize_tree_node(str0_, dic, tn1, False, pos)
            cou -= 1