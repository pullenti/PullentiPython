# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import gzip
import shutil
from pullenti.unisharp.Utils import Utils
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.DerivateGroup import DerivateGroup
from pullenti.morph.internal.LazyInfo2 import LazyInfo2
from pullenti.morph.internal.ExplanTreeNode import ExplanTreeNode
from pullenti.morph.DerivateWord import DerivateWord


class ExplanSerializeHelper:
    
    @staticmethod
    def serializeDD(res : io.IOBase, dic : 'DerivateDictionary') -> None:
        with io.BytesIO() as tmp: 
            ExplanSerializeHelper.__serializeInt(tmp, len(dic._m_all_groups))
            i = 0
            while i < len(dic._m_all_groups): 
                p0 = tmp.tell()
                ExplanSerializeHelper.__serializeInt(tmp, 0)
                ExplanSerializeHelper.__serializeDerivateGroup(tmp, dic._m_all_groups[i])
                dic._m_all_groups[i].tag = ((i + 1))
                p1 = tmp.tell()
                tmp.seek(p0, io.SEEK_SET)
                ExplanSerializeHelper.__serializeInt(tmp, p1)
                tmp.seek(p1, io.SEEK_SET)
                i += 1
            ExplanSerializeHelper.__serializeTreeNode(tmp, dic._m_root)
            deflate = gzip.GzipFile(fileobj=res, mode='w')
            shutil.copyfileobj(tmp, deflate)
            deflate.close()
    
    @staticmethod
    def deserializeDD(str0_ : io.IOBase, dic : 'DerivateDictionary', lazy_load : bool) -> None:
        with io.BytesIO() as tmp: 
            MorphSerializeHelper.deflateGzip(str0_, tmp)
            wr = ByteArrayWrapper(bytearray(tmp.getvalue()))
            cou = wr.deserializeInt()
            while cou > 0: 
                p1 = wr.deserializeInt()
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy = LazyInfo2._new5(wr.position, wr, dic)
                    wr.seek(p1)
                else: 
                    ExplanSerializeHelper.deserializeDerivateGroup(wr, ew)
                dic._m_all_groups.append(ew)
                cou -= 1
            dic._m_root = ExplanTreeNode()
            ExplanSerializeHelper.deserializeTreeNode(wr, dic, dic._m_root, lazy_load)
    
    @staticmethod
    def __serializeDerivateGroup(res : io.IOBase, dg : 'DerivateGroup') -> None:
        attrs = 0
        if (dg.is_dummy): 
            attrs |= (1)
        if (dg.not_generate): 
            attrs |= (2)
        if (dg.transitive == 0): 
            attrs |= (4)
        if (dg.transitive == 1): 
            attrs |= (8)
        ExplanSerializeHelper.__serializeShort(res, attrs)
        ExplanSerializeHelper.__serializeString(res, dg.prefix)
        for i in range(len(dg.words) - 1, -1, -1):
            if (Utils.isNullOrEmpty(dg.words[i].spelling)): 
                del dg.words[i]
        ExplanSerializeHelper.__serializeShort(res, len(dg.words))
        for w in dg.words: 
            ExplanSerializeHelper.__serializeString(res, w.spelling)
            ExplanSerializeHelper.__serializeShort(res, (0 if w.class0_ is None else w.class0_.value))
            ExplanSerializeHelper.__serializeShort(res, w.lang.value)
            ExplanSerializeHelper.__serializeShort(res, w.attrs._value)
            ExplanSerializeHelper.__serializeShort(res, (0 if w.nexts is None else len(w.nexts)))
            if (w.nexts is not None): 
                for kp in w.nexts.items(): 
                    ExplanSerializeHelper.__serializeString(res, kp[0])
                    ExplanSerializeHelper.__serializeShort(res, kp[1].value)
    
    @staticmethod
    def deserializeDerivateGroup(str0_ : 'ByteArrayWrapper', dg : 'DerivateGroup') -> None:
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.morph.MorphCase import MorphCase
        attr = str0_.deserializeShort()
        if (((attr & 1)) != 0): 
            dg.is_dummy = True
        if (((attr & 2)) != 0): 
            dg.not_generate = True
        if (((attr & 4)) != 0): 
            dg.m_transitive = 0
        if (((attr & 8)) != 0): 
            dg.m_transitive = 1
        dg.prefix = str0_.deserializeString()
        cou = str0_.deserializeShort()
        while cou > 0: 
            w = DerivateWord(dg)
            w.spelling = str0_.deserializeString()
            w.class0_ = MorphClass()
            w.class0_.value = (str0_.deserializeShort())
            w.lang = MorphLang._new6(str0_.deserializeShort())
            w.attrs._value = (str0_.deserializeShort())
            cou1 = str0_.deserializeShort()
            while cou1 > 0: 
                pref = Utils.ifNotNull(str0_.deserializeString(), "")
                cas = MorphCase()
                cas.value = (str0_.deserializeShort())
                if (w.nexts is None): 
                    w.nexts = dict()
                w.nexts[pref] = cas
                cou1 -= 1
            dg.words.append(w)
            cou -= 1
    
    @staticmethod
    def __serializeTreeNode(res : io.IOBase, tn : 'ExplanTreeNode') -> None:
        if (tn.groups is None): 
            ExplanSerializeHelper.__serializeShort(res, 0)
        elif (isinstance(tn.groups, DerivateGroup)): 
            ExplanSerializeHelper.__serializeShort(res, 1)
            ExplanSerializeHelper.__serializeInt(res, (Utils.asObjectOrNull(tn.groups, DerivateGroup)).tag)
        else: 
            li = Utils.asObjectOrNull(tn.groups, list)
            if (li is not None): 
                ExplanSerializeHelper.__serializeShort(res, len(li))
                for gr in li: 
                    ExplanSerializeHelper.__serializeInt(res, gr.tag)
            else: 
                ExplanSerializeHelper.__serializeShort(res, 0)
        if (tn.nodes is None or len(tn.nodes) == 0): 
            ExplanSerializeHelper.__serializeShort(res, 0)
        else: 
            ExplanSerializeHelper.__serializeShort(res, len(tn.nodes))
            for n in tn.nodes.items(): 
                ExplanSerializeHelper.__serializeShort(res, n[0])
                p0 = res.tell()
                ExplanSerializeHelper.__serializeInt(res, 0)
                ExplanSerializeHelper.__serializeTreeNode(res, n[1])
                p1 = res.tell()
                res.seek(p0, io.SEEK_SET)
                ExplanSerializeHelper.__serializeInt(res, p1)
                res.seek(p1, io.SEEK_SET)
    
    @staticmethod
    def deserializeTreeNode(str0_ : 'ByteArrayWrapper', dic : 'DerivateDictionary', tn : 'ExplanTreeNode', lazy_load : bool) -> None:
        cou = str0_.deserializeShort()
        li = (list() if cou > 1 else None)
        while cou > 0: 
            id0_ = str0_.deserializeInt()
            if (id0_ > 0 and id0_ <= len(dic._m_all_groups)): 
                gr = dic._m_all_groups[id0_ - 1]
                if (gr._lazy is not None): 
                    p0 = str0_.position
                    str0_.seek(gr._lazy.begin)
                    ExplanSerializeHelper.deserializeDerivateGroup(str0_, gr)
                    gr._lazy = (None)
                    str0_.seek(p0)
                if (li is not None): 
                    li.append(gr)
                else: 
                    tn.groups = (gr)
            cou -= 1
        if (li is not None): 
            tn.groups = (li)
        cou = str0_.deserializeShort()
        if (cou == 0): 
            return
        while cou > 0: 
            ke = str0_.deserializeShort()
            p1 = str0_.deserializeInt()
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
                ExplanSerializeHelper.deserializeTreeNode(str0_, dic, tn1, False)
            cou -= 1
    
    @staticmethod
    def __serializeByte(res : io.IOBase, val : int) -> None:
        Utils.writeByteIO(res, val)
    
    @staticmethod
    def __serializeShort(res : io.IOBase, val : int) -> None:
        Utils.writeByteIO(res, val)
        Utils.writeByteIO(res, (val >> 8))
    
    @staticmethod
    def __serializeInt(res : io.IOBase, val : int) -> None:
        Utils.writeByteIO(res, val)
        Utils.writeByteIO(res, (val >> 8))
        Utils.writeByteIO(res, (val >> 16))
        Utils.writeByteIO(res, (val >> 24))
    
    @staticmethod
    def __serializeString(res : io.IOBase, s : str) -> None:
        if (s is None): 
            Utils.writeByteIO(res, 0xFF)
        elif (len(s) == 0): 
            Utils.writeByteIO(res, 0)
        else: 
            data = s.encode("UTF-8", 'ignore')
            Utils.writeByteIO(res, len(data))
            Utils.writeIO(res, data, 0, len(data))