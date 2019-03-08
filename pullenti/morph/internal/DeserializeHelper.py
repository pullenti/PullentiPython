# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

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
            cou = wr.deserialize_int()
            while cou > 0: 
                p1 = wr.deserialize_int()
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy_pos = wr.position
                    wr.seek(p1)
                else: 
                    DeserializeHelper.deserialize_derivate_group(wr, ew)
                dic._m_all_groups.append(ew)
                cou -= 1
            dic._m_root = ExplanTreeNode()
            DeserializeHelper.deserialize_tree_node(wr, dic, dic._m_root, lazy_load)
        return wr
    
    @staticmethod
    def deserialize_derivate_group(str0_ : 'ByteArrayWrapper', dg : 'DerivateGroup') -> None:
        attr = str0_.deserialize_short()
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
        dg.questions = (Utils.valToEnum(str0_.deserialize_short(), NextModelQuestion))
        dg.questions_ref = (Utils.valToEnum(str0_.deserialize_short(), NextModelQuestion))
        dg.prefix = str0_.deserialize_string()
        cou = str0_.deserialize_short()
        while cou > 0: 
            w = DerivateWord(dg)
            w.spelling = str0_.deserialize_string()
            w.class0_ = MorphClass()
            w.class0_.value = (str0_.deserialize_short())
            w.lang = MorphLang._new5(str0_.deserialize_short())
            w.attrs.value = (str0_.deserialize_short())
            dg.words.append(w)
            cou -= 1
        cou = str0_.deserialize_short()
        while cou > 0: 
            pref = Utils.ifNotNull(str0_.deserialize_string(), "")
            cas = MorphCase()
            cas.value = (str0_.deserialize_short())
            if (dg.nexts is None): 
                dg.nexts = dict()
            dg.nexts[pref] = cas
            cou -= 1
        cou = str0_.deserialize_short()
        while cou > 0: 
            pref = Utils.ifNotNull(str0_.deserialize_string(), "")
            cas = MorphCase()
            cas.value = (str0_.deserialize_short())
            if (dg.nexts_ref is None): 
                dg.nexts_ref = dict()
            dg.nexts_ref[pref] = cas
            cou -= 1
    
    @staticmethod
    def deserialize_tree_node(str0_ : 'ByteArrayWrapper', dic : 'DerivateDictionary', tn : 'ExplanTreeNode', lazy_load : bool) -> None:
        cou = str0_.deserialize_short()
        li = (list() if cou > 1 else None)
        while cou > 0: 
            id0_ = str0_.deserialize_int()
            if (id0_ > 0 and id0_ <= len(dic._m_all_groups)): 
                gr = dic._m_all_groups[id0_ - 1]
                if (gr._lazy_pos > 0): 
                    p0 = str0_.position
                    str0_.seek(gr._lazy_pos)
                    DeserializeHelper.deserialize_derivate_group(str0_, gr)
                    gr._lazy_pos = 0
                    str0_.seek(p0)
                if (li is not None): 
                    li.append(gr)
                else: 
                    tn.groups = (gr)
            cou -= 1
        if (li is not None): 
            tn.groups = (li)
        cou = str0_.deserialize_short()
        if (cou == 0): 
            return
        while cou > 0: 
            ke = str0_.deserialize_short()
            p1 = str0_.deserialize_int()
            tn1 = ExplanTreeNode()
            if (tn.nodes is None): 
                tn.nodes = dict()
            if (not ke in tn.nodes): 
                tn.nodes[ke] = tn1
            if (lazy_load): 
                tn1.lazy_pos = str0_.position
                str0_.seek(p1)
            else: 
                DeserializeHelper.deserialize_tree_node(str0_, dic, tn1, False)
            cou -= 1