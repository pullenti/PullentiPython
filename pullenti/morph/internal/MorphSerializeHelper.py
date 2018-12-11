# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import gzip
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.internal.MorphRuleVariant import MorphRuleVariant
from pullenti.morph.internal.MorphTreeNode import MorphTreeNode
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.internal.MorphRule import MorphRule
from pullenti.morph.MorphMiscInfo import MorphMiscInfo

class MorphSerializeHelper:
    
    @staticmethod
    def deflateGzip(str0_ : io.IOBase, res : io.IOBase) -> None:
        with gzip.GzipFile(fileobj=str0_, mode='r') as deflate: 
            buf = Utils.newArrayOfBytes(100000, 0)
            while True:
                i = -1
                try: 
                    ii = 0
                    while ii < len(buf): 
                        buf[ii] = (0)
                        ii += 1
                    i = Utils.readIO(deflate, buf, 0, len(buf))
                except Exception as ex: 
                    for i in range(len(buf) - 1, -1, -1):
                        if (buf[i] != (0)): 
                            Utils.writeIO(res, buf, 0, i + 1)
                            break
                    else: i = -1
                    break
                if (i < 1): 
                    break
                Utils.writeIO(res, buf, 0, i)
    
    @staticmethod
    def deserializeAll(str0 : io.IOBase, me : 'MorphEngine', ignore_rev_tree : bool, lazy_load : bool) -> 'ByteArrayWrapper':
        tmp = io.BytesIO()
        MorphSerializeHelper.deflateGzip(str0, tmp)
        buf = ByteArrayWrapper(bytearray(tmp.getvalue()))
        me._m_vars.clear()
        me.m_rules.clear()
        me.m_root = MorphTreeNode()
        me.m_root_reverce = MorphTreeNode()
        cou = buf.deserializeInt()
        while cou > 0: 
            mi = MorphMiscInfo()
            MorphSerializeHelper.__deserializeMorphMiscInfo(buf, mi)
            me._m_vars.append(mi)
            cou -= 1
        cou = buf.deserializeInt()
        while cou > 0: 
            p1 = buf.deserializeInt()
            r = MorphRule()
            if (lazy_load): 
                r.lazy_pos = buf.position
                buf.seek(p1)
            else: 
                MorphSerializeHelper.__deserializeMorphRule(buf, r, me)
            me.m_rules.append(r)
            cou -= 1
        if (lazy_load): 
            MorphSerializeHelper._deserializeMorphTreeNodeLazy(buf, me.m_root, me)
        else: 
            MorphSerializeHelper.__deserializeMorphTreeNode(buf, me.m_root, me)
        if (not ignore_rev_tree): 
            if (lazy_load): 
                MorphSerializeHelper._deserializeMorphTreeNodeLazy(buf, me.m_root_reverce, me)
            else: 
                MorphSerializeHelper.__deserializeMorphTreeNode(buf, me.m_root_reverce, me)
        tmp.close()
        return buf
    
    @staticmethod
    def __serializeMorphMiscInfo(res : io.IOBase, mi : 'MorphMiscInfo') -> None:
        MorphSerializeHelper.__serializeShort(res, mi._m_value)
        for a in mi.attrs: 
            MorphSerializeHelper.__serializeString(res, a)
        Utils.writeByteIO(res, 0xFF)
    
    @staticmethod
    def __deserializeMorphMiscInfo(str0_ : 'ByteArrayWrapper', mi : 'MorphMiscInfo') -> None:
        mi._m_value = (str0_.deserializeShort())
        while True:
            s = str0_.deserializeString()
            if (Utils.isNullOrEmpty(s)): 
                break
            mi.attrs.append(s)
    
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
    
    @staticmethod
    def __serializeMorphRule(res : io.IOBase, r : 'MorphRule') -> None:
        MorphSerializeHelper.__serializeShort(res, r._id0_)
        for v in r.variants.items(): 
            MorphSerializeHelper.__serializeString(res, v[0])
            for m in v[1]: 
                MorphSerializeHelper.__serializeMorphRuleVariant(res, m)
            MorphSerializeHelper.__serializeShort(res, 0)
        Utils.writeByteIO(res, 0xFF)
    
    @staticmethod
    def __deserializeMorphRule(str0_ : 'ByteArrayWrapper', r : 'MorphRule', me : 'MorphEngine') -> None:
        r._id0_ = str0_.deserializeShort()
        while not str0_.iseof:
            b = str0_.deserializeByte()
            if (b == (0xFF)): 
                break
            str0_.back()
            key = Utils.ifNotNull(str0_.deserializeString(), "")
            li = list()
            r.variants[key] = li
            r.variants_key.append(key)
            r.variants_list.append(li)
            while not str0_.iseof:
                mrv = MorphSerializeHelper.__deserializeMorphRuleVariant(str0_, me)
                if (mrv is None): 
                    break
                mrv.tail = key
                mrv.rule = r
                li.append(mrv)
    
    @staticmethod
    def __serializeMorphRuleVariant(res : io.IOBase, v : 'MorphRuleVariant') -> None:
        MorphSerializeHelper.__serializeShort(res, v.misc_info._id0_)
        MorphSerializeHelper.__serializeShort(res, v.class0_.value)
        MorphSerializeHelper.__serializeByte(res, v.gender)
        MorphSerializeHelper.__serializeByte(res, v.number)
        MorphSerializeHelper.__serializeByte(res, v.case_.value)
        MorphSerializeHelper.__serializeString(res, v.normal_tail)
        MorphSerializeHelper.__serializeString(res, v.full_normal_tail)
    
    @staticmethod
    def __deserializeMorphRuleVariant(str0_ : 'ByteArrayWrapper', me : 'MorphEngine') -> 'MorphRuleVariant':
        id0_ = str0_.deserializeShort() - 1
        if ((id0_ < 0) or id0_ >= len(me._m_vars)): 
            return None
        mrv = MorphRuleVariant._new37(me._m_vars[id0_])
        mc = MorphClass()
        mc.value = (str0_.deserializeShort())
        if (mc.is_misc and mc.is_proper): 
            mc.is_misc = False
        mrv.class0_ = mc
        mrv.gender = Utils.valToEnum(str0_.deserializeByte(), MorphGender)
        mrv.number = Utils.valToEnum(str0_.deserializeByte(), MorphNumber)
        mca = MorphCase()
        mca.value = (str0_.deserializeByte())
        mrv.case_ = mca
        mrv.normal_tail = str0_.deserializeString()
        mrv.full_normal_tail = str0_.deserializeString()
        return mrv
    
    @staticmethod
    def __serializeMorphTreeNode(res : io.IOBase, tn : 'MorphTreeNode') -> None:
        if (tn.rules is not None): 
            for r in tn.rules: 
                MorphSerializeHelper.__serializeShort(res, r._id0_)
        MorphSerializeHelper.__serializeShort(res, 0)
        if (tn.reverce_variants is not None): 
            for v in tn.reverce_variants: 
                MorphSerializeHelper.__serializeString(res, Utils.ifNotNull(v.tail, ""))
                if (v.rule is not None): 
                    pass
                MorphSerializeHelper.__serializeShort(res, (0 if v.rule is None else v.rule._id0_))
                MorphSerializeHelper.__serializeShort(res, v.coef)
                MorphSerializeHelper.__serializeMorphRuleVariant(res, v)
        MorphSerializeHelper.__serializeString(res, None)
        if (tn.nodes is not None): 
            for n in tn.nodes.items(): 
                MorphSerializeHelper.__serializeShort(res, n[0])
                p0 = res.tell()
                MorphSerializeHelper.__serializeInt(res, 0)
                MorphSerializeHelper.__serializeMorphTreeNode(res, n[1])
                p1 = res.tell()
                res.seek(p0, io.SEEK_SET)
                MorphSerializeHelper.__serializeInt(res, p1)
                res.seek(p1, io.SEEK_SET)
        MorphSerializeHelper.__serializeShort(res, 0xFFFF)
    
    @staticmethod
    def __deserializeMorphTreeNodeBase(str0_ : 'ByteArrayWrapper', tn : 'MorphTreeNode', me : 'MorphEngine') -> None:
        while not str0_.iseof:
            i = str0_.deserializeShort()
            i -= 1
            if ((i < 0) or i >= len(me.m_rules)): 
                break
            r = me.m_rules[i]
            if (tn.rules is None): 
                tn.rules = list()
            tn.rules.append(r)
        while not str0_.iseof:
            tail = str0_.deserializeString()
            if (tail is None): 
                break
            rule_id = str0_.deserializeShort()
            coef = str0_.deserializeShort()
            v = MorphSerializeHelper.__deserializeMorphRuleVariant(str0_, me)
            if (v is None): 
                break
            v.tail = tail
            if (rule_id > 0 and rule_id <= len(me.m_rules)): 
                v.rule = me.m_rules[rule_id - 1]
            else: 
                pass
            if (tn.reverce_variants is None): 
                tn.reverce_variants = list()
            v.coef = (coef)
            tn.reverce_variants.append(v)
    
    @staticmethod
    def _deserializeMorphTreeNodeLazy(str0_ : 'ByteArrayWrapper', tn : 'MorphTreeNode', me : 'MorphEngine') -> None:
        MorphSerializeHelper.__deserializeMorphTreeNodeBase(str0_, tn, me)
        while not str0_.iseof:
            i = str0_.deserializeShort()
            if (i == 0xFFFF): 
                break
            pos = str0_.deserializeInt()
            child = MorphTreeNode()
            child.lazy_pos = str0_.position
            if (tn.nodes is None): 
                tn.nodes = dict()
            tn.nodes[i] = child
            str0_.seek(pos)
        p = str0_.position
        if (tn.rules is not None): 
            for r in tn.rules: 
                if (r.lazy_pos > 0): 
                    str0_.seek(r.lazy_pos)
                    MorphSerializeHelper.__deserializeMorphRule(str0_, r, me)
                    r.lazy_pos = 0
            str0_.seek(p)
    
    @staticmethod
    def __deserializeMorphTreeNode(str0_ : 'ByteArrayWrapper', tn : 'MorphTreeNode', me : 'MorphEngine') -> int:
        res = 0
        MorphSerializeHelper.__deserializeMorphTreeNodeBase(str0_, tn, me)
        while not str0_.iseof:
            i = str0_.deserializeShort()
            if (i == 0xFFFF): 
                break
            pos = str0_.deserializeInt()
            child = MorphTreeNode()
            if (tn.nodes is None): 
                tn.nodes = dict()
            tn.nodes[i] = child
            res += 1
            res += MorphSerializeHelper.__deserializeMorphTreeNode(str0_, child, me)
        return res
    
    MAX_VARIANTS = 0
    
    @staticmethod
    def __manageReverceNodes(root : 'MorphTreeNode', tn : 'MorphTreeNode', term : str) -> None:
        if (tn.rules is not None): 
            for r in tn.rules: 
                for v in r.variants.items(): 
                    wf = term + v[0]
                    if (len(wf) <= MorphSerializeHelper.__min_tail_len): 
                        continue
                    rtn = root
                    lev = 0
                    first_pass2728 = True
                    while True:
                        if first_pass2728: first_pass2728 = False
                        else: lev += 1
                        if (not (lev < MorphSerializeHelper.__max_tail_len)): break
                        i = len(wf) - 1 - lev
                        if (i < 0): 
                            break
                        ch = ord(wf[i])
                        if (rtn.nodes is None): 
                            rtn.nodes = dict()
                        next0_ = None
                        wrapnext38 = RefOutArgWrapper(None)
                        inoutres39 = Utils.tryGetValue(rtn.nodes, ch, wrapnext38)
                        next0_ = wrapnext38.value
                        if (not inoutres39): 
                            next0_ = MorphTreeNode()
                            rtn.nodes[ch] = next0_
                        rtn = next0_
                        if ((lev + 1) < MorphSerializeHelper.__min_tail_len): 
                            continue
                        if (rtn.reverce_variants is None): 
                            rtn.reverce_variants = list()
                        for mrf in v[1]: 
                            has = False
                            for mfv0 in rtn.reverce_variants: 
                                if (mfv0.compare(mrf)): 
                                    mfv0.coef += 1
                                    has = True
                                    break
                            if (not has): 
                                mrf0 = MorphRuleVariant(mrf)
                                mrf0.coef = (1)
                                rtn.reverce_variants.append(mrf0)
                        break
        if (tn.nodes is not None): 
            for tch in tn.nodes.items(): 
                MorphSerializeHelper.__manageReverceNodes(root, tch[1], "{0}{1}".format(term, (chr(tch[0]))))
    
    __min_tail_len = 4
    
    __max_tail_len = 7