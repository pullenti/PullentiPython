# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import gzip
import shutil
from pullenti.ntopy.Utils import Utils
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.DerivateGroup import DerivateGroup
from pullenti.morph.internal.LazyInfo2 import LazyInfo2
from pullenti.morph.internal.ExplanTreeNode import ExplanTreeNode
from pullenti.morph.DerivateWord import DerivateWord


class ExplanSerializeHelper:
    
    @staticmethod
    def serializedd(res : io.IOBase, dic : 'DerivateDictionary') -> None:
        with io.BytesIO() as tmp: 
            ExplanSerializeHelper.__serialize_int(tmp, len(dic._m_all_groups))
            for i in range(len(dic._m_all_groups)):
                p0 = tmp.tell()
                ExplanSerializeHelper.__serialize_int(tmp, 0)
                ExplanSerializeHelper.__serialize_derivate_group(tmp, dic._m_all_groups[i])
                dic._m_all_groups[i].tag = (i + 1)
                p1 = tmp.tell()
                tmp.seek(p0, io.SEEK_SET)
                ExplanSerializeHelper.__serialize_int(tmp, p1)
                tmp.seek(p1, io.SEEK_SET)
            ExplanSerializeHelper.__serialize_tree_node(tmp, dic._m_root)
            deflate = gzip.GzipFile(fileobj=res, mode='w')
            shutil.copyfileobj(tmp, deflate)
            deflate.close()
    
    @staticmethod
    def deserializedd(str0_ : io.IOBase, dic : 'DerivateDictionary', lazy_load : bool) -> None:
        with io.BytesIO() as tmp: 
            MorphSerializeHelper.deflate_gzip(str0_, tmp)
            wr = ByteArrayWrapper(tmp.getvalue())
            cou = wr.deserialize_int()
            while cou > 0: 
                p1 = wr.deserialize_int()
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy = LazyInfo2._new5(wr.position, wr, dic)
                    wr.seek(p1)
                else: 
                    ExplanSerializeHelper.deserialize_derivate_group(wr, ew)
                dic._m_all_groups.append(ew)
                cou -= 1
            dic._m_root = ExplanTreeNode()
            ExplanSerializeHelper.deserialize_tree_node(wr, dic, dic._m_root, lazy_load)
    
    @staticmethod
    def __serialize_derivate_group(res : io.IOBase, dg : 'DerivateGroup') -> None:
        attrs = 0
        if (dg.is_dummy): 
            attrs |= 1
        if (dg.not_generate): 
            attrs |= 2
        if (dg.transitive == 0): 
            attrs |= 4
        if (dg.transitive == 1): 
            attrs |= 8
        ExplanSerializeHelper.__serialize_short(res, attrs)
        ExplanSerializeHelper.__serialize_string(res, dg.prefix)
        for i in range(len(dg.words) - 1, -1, -1):
            if (Utils.isNullOrEmpty(dg.words[i].spelling)): 
                del dg.words[i]
        ExplanSerializeHelper.__serialize_short(res, len(dg.words))
        for w in dg.words: 
            ExplanSerializeHelper.__serialize_string(res, w.spelling)
            ExplanSerializeHelper.__serialize_short(res, (0 if w.class0_ is None else w.class0_.value))
            ExplanSerializeHelper.__serialize_short(res, w.lang.value)
            ExplanSerializeHelper.__serialize_short(res, w.attrs._value)
            ExplanSerializeHelper.__serialize_short(res, (0 if w.nexts is None else len(w.nexts)))
            if (w.nexts is not None): 
                for kp in w.nexts.items(): 
                    ExplanSerializeHelper.__serialize_string(res, kp[0])
                    ExplanSerializeHelper.__serialize_short(res, kp[1].value)
    
    @staticmethod
    def deserialize_derivate_group(str0_ : 'ByteArrayWrapper', dg : 'DerivateGroup') -> None:
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.morph.MorphCase import MorphCase
        attr = str0_.deserialize_short()
        if (((attr & 1)) != 0): 
            dg.is_dummy = True
        if (((attr & 2)) != 0): 
            dg.not_generate = True
        if (((attr & 4)) != 0): 
            dg.m_transitive = 0
        if (((attr & 8)) != 0): 
            dg.m_transitive = 1
        dg.prefix = str0_.deserialize_string()
        cou = str0_.deserialize_short()
        while cou > 0: 
            w = DerivateWord(dg)
            w.spelling = str0_.deserialize_string()
            w.class0_ = MorphClass()
            w.class0_.value = str0_.deserialize_short()
            w.lang = MorphLang._new6(str0_.deserialize_short())
            w.attrs._value = str0_.deserialize_short()
            cou1 = str0_.deserialize_short()
            while cou1 > 0: 
                pref = Utils.ifNotNull(str0_.deserialize_string(), "")
                cas = MorphCase()
                cas.value = str0_.deserialize_short()
                if (w.nexts is None): 
                    w.nexts = dict()
                w.nexts[pref] = cas
                cou1 -= 1
            dg.words.append(w)
            cou -= 1
    
    @staticmethod
    def __serialize_tree_node(res : io.IOBase, tn : 'ExplanTreeNode') -> None:
        if (tn.groups is None): 
            ExplanSerializeHelper.__serialize_short(res, 0)
        elif (isinstance(tn.groups, DerivateGroup)): 
            ExplanSerializeHelper.__serialize_short(res, 1)
            ExplanSerializeHelper.__serialize_int(res, (tn.groups if isinstance(tn.groups, DerivateGroup) else None).tag)
        else: 
            li = (tn.groups if isinstance(tn.groups, list) else None)
            if (li is not None): 
                ExplanSerializeHelper.__serialize_short(res, len(li))
                for gr in li: 
                    ExplanSerializeHelper.__serialize_int(res, gr.tag)
            else: 
                ExplanSerializeHelper.__serialize_short(res, 0)
        if (tn.nodes is None or len(tn.nodes) == 0): 
            ExplanSerializeHelper.__serialize_short(res, 0)
        else: 
            ExplanSerializeHelper.__serialize_short(res, len(tn.nodes))
            for n in tn.nodes.items(): 
                ExplanSerializeHelper.__serialize_short(res, n[0])
                p0 = res.tell()
                ExplanSerializeHelper.__serialize_int(res, 0)
                ExplanSerializeHelper.__serialize_tree_node(res, n[1])
                p1 = res.tell()
                res.seek(p0, io.SEEK_SET)
                ExplanSerializeHelper.__serialize_int(res, p1)
                res.seek(p1, io.SEEK_SET)
    
    @staticmethod
    def deserialize_tree_node(str0_ : 'ByteArrayWrapper', dic : 'DerivateDictionary', tn : 'ExplanTreeNode', lazy_load : bool) -> None:
        cou = str0_.deserialize_short()
        li = (list() if cou > 1 else None)
        while cou > 0: 
            id0_ = str0_.deserialize_int()
            if (id0_ > 0 and id0_ <= len(dic._m_all_groups)): 
                gr = dic._m_all_groups[id0_ - 1]
                if (gr._lazy is not None): 
                    p0 = str0_.position
                    str0_.seek(gr._lazy.begin)
                    ExplanSerializeHelper.deserialize_derivate_group(str0_, gr)
                    gr._lazy = None
                    str0_.seek(p0)
                if (li is not None): 
                    li.append(gr)
                else: 
                    tn.groups = gr
            cou -= 1
        if (li is not None): 
            tn.groups = li
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
                tn1._lazy = LazyInfo2()
                tn1._lazy.begin = str0_.position
                tn1._lazy.data = str0_
                tn1._lazy.dic = dic
                str0_.seek(p1)
            else: 
                ExplanSerializeHelper.deserialize_tree_node(str0_, dic, tn1, False)
            cou -= 1
    
    @staticmethod
    def __serialize_byte(res : io.IOBase, val : int) -> None:
        Utils.writeByteIO(res, val)
    
    @staticmethod
    def __serialize_short(res : io.IOBase, val : int) -> None:
        Utils.writeByteIO(res, val)
        Utils.writeByteIO(res, (val >> 8))
    
    @staticmethod
    def __serialize_int(res : io.IOBase, val : int) -> None:
        Utils.writeByteIO(res, val)
        Utils.writeByteIO(res, (val >> 8))
        Utils.writeByteIO(res, (val >> 16))
        Utils.writeByteIO(res, (val >> 24))
    
    @staticmethod
    def __serialize_string(res : io.IOBase, s : str) -> None:
        if (s is None): 
            Utils.writeByteIO(res, 0xFF)
        elif (len(s) == 0): 
            Utils.writeByteIO(res, 0)
        else: 
            data = s.encode('utf-8', 'ignore')
            Utils.writeByteIO(res, len(data))
            Utils.writeIO(res, data, 0, len(data))