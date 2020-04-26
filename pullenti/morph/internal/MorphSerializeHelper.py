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
    def deflate_gzip(str0_ : io.IOBase, res : io.IOBase) -> None:
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
    def deserialize_all(str0 : io.IOBase, me : 'MorphEngine', ignore_rev_tree : bool, lazy_load : bool) -> 'ByteArrayWrapper':
        tmp = io.BytesIO()
        MorphSerializeHelper.deflate_gzip(str0, tmp)
        buf = ByteArrayWrapper(bytearray(tmp.getvalue()))
        me._m_vars.clear()
        me.m_rules.clear()
        me.m_root = MorphTreeNode()
        me.m_root_reverce = MorphTreeNode()
        pos = 0
        wrappos50 = RefOutArgWrapper(pos)
        cou = buf.deserialize_int(wrappos50)
        pos = wrappos50.value
        while cou > 0: 
            mi = MorphMiscInfo()
            wrappos42 = RefOutArgWrapper(pos)
            MorphSerializeHelper.__deserialize_morph_misc_info(buf, mi, wrappos42)
            pos = wrappos42.value
            me._m_vars.append(mi)
            cou -= 1
        wrappos49 = RefOutArgWrapper(pos)
        cou = buf.deserialize_int(wrappos49)
        pos = wrappos49.value
        while cou > 0: 
            wrappos44 = RefOutArgWrapper(pos)
            p1 = buf.deserialize_int(wrappos44)
            pos = wrappos44.value
            r = MorphRule()
            if (lazy_load): 
                r.lazy_pos = pos
                pos = p1
            else: 
                wrappos43 = RefOutArgWrapper(pos)
                MorphSerializeHelper.__deserialize_morph_rule(buf, r, me, wrappos43)
                pos = wrappos43.value
            me.m_rules.append(r)
            cou -= 1
        if (lazy_load): 
            wrappos45 = RefOutArgWrapper(pos)
            MorphSerializeHelper._deserialize_morph_tree_node_lazy(buf, me.m_root, me, wrappos45)
            pos = wrappos45.value
        else: 
            wrappos46 = RefOutArgWrapper(pos)
            MorphSerializeHelper.__deserialize_morph_tree_node(buf, me.m_root, me, wrappos46)
            pos = wrappos46.value
        if (not ignore_rev_tree): 
            if (lazy_load): 
                wrappos47 = RefOutArgWrapper(pos)
                MorphSerializeHelper._deserialize_morph_tree_node_lazy(buf, me.m_root_reverce, me, wrappos47)
                pos = wrappos47.value
            else: 
                wrappos48 = RefOutArgWrapper(pos)
                MorphSerializeHelper.__deserialize_morph_tree_node(buf, me.m_root_reverce, me, wrappos48)
                pos = wrappos48.value
        tmp.close()
        return buf
    
    @staticmethod
    def __serialize_morph_misc_info(res : io.IOBase, mi : 'MorphMiscInfo') -> None:
        MorphSerializeHelper.__serialize_short(res, mi._m_value)
        for a in mi.attrs: 
            MorphSerializeHelper.__serialize_string(res, a)
        Utils.writeByteIO(res, 0xFF)
    
    @staticmethod
    def __deserialize_morph_misc_info(str0_ : 'ByteArrayWrapper', mi : 'MorphMiscInfo', pos : int) -> None:
        mi._m_value = (str0_.deserialize_short(pos))
        while True:
            s = str0_.deserialize_string(pos)
            if (Utils.isNullOrEmpty(s)): 
                break
            mi.attrs.append(s)
    
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
            data = s.encode("UTF-8", 'ignore')
            Utils.writeByteIO(res, len(data))
            Utils.writeIO(res, data, 0, len(data))
    
    @staticmethod
    def __serialize_morph_rule(res : io.IOBase, r : 'MorphRule') -> None:
        MorphSerializeHelper.__serialize_short(res, r._id0_)
        for v in r.variants.items(): 
            MorphSerializeHelper.__serialize_string(res, v[0])
            for m in v[1]: 
                MorphSerializeHelper.__serialize_morph_rule_variant(res, m)
            MorphSerializeHelper.__serialize_short(res, 0)
        Utils.writeByteIO(res, 0xFF)
    
    @staticmethod
    def __deserialize_morph_rule(str0_ : 'ByteArrayWrapper', r : 'MorphRule', me : 'MorphEngine', pos : int) -> None:
        r._id0_ = str0_.deserialize_short(pos)
        while not str0_.iseof(pos.value):
            b = str0_.deserialize_byte(pos)
            if (b == (0xFF)): 
                break
            pos.value -= 1
            key = Utils.ifNotNull(str0_.deserialize_string(pos), "")
            li = list()
            r.variants[key] = li
            r.variants_key.append(key)
            r.variants_list.append(li)
            while not str0_.iseof(pos.value):
                mrv = MorphSerializeHelper.__deserialize_morph_rule_variant(str0_, me, pos)
                if (mrv is None): 
                    break
                mrv.tail = key
                mrv.rule = r
                li.append(mrv)
    
    @staticmethod
    def __serialize_morph_rule_variant(res : io.IOBase, v : 'MorphRuleVariant') -> None:
        MorphSerializeHelper.__serialize_short(res, v.misc_info._id0_)
        MorphSerializeHelper.__serialize_short(res, v.class0_.value)
        MorphSerializeHelper.__serialize_byte(res, v.gender)
        MorphSerializeHelper.__serialize_byte(res, v.number)
        MorphSerializeHelper.__serialize_byte(res, v.case_.value)
        MorphSerializeHelper.__serialize_string(res, v.normal_tail)
        MorphSerializeHelper.__serialize_string(res, v.full_normal_tail)
    
    @staticmethod
    def __deserialize_morph_rule_variant(str0_ : 'ByteArrayWrapper', me : 'MorphEngine', pos : int) -> 'MorphRuleVariant':
        id0_ = str0_.deserialize_short(pos) - 1
        if ((id0_ < 0) or id0_ >= len(me._m_vars)): 
            return None
        mrv = MorphRuleVariant._new51(me._m_vars[id0_])
        mc = MorphClass()
        mc.value = (str0_.deserialize_short(pos))
        if (mc.is_misc and mc.is_proper): 
            mc.is_misc = False
        mrv.class0_ = mc
        mrv.gender = Utils.valToEnum(str0_.deserialize_byte(pos), MorphGender)
        mrv.number = Utils.valToEnum(str0_.deserialize_byte(pos), MorphNumber)
        mca = MorphCase()
        mca.value = (str0_.deserialize_byte(pos))
        mrv.case_ = mca
        mrv.normal_tail = str0_.deserialize_string(pos)
        mrv.full_normal_tail = str0_.deserialize_string(pos)
        return mrv
    
    @staticmethod
    def __serialize_morph_tree_node(res : io.IOBase, tn : 'MorphTreeNode') -> None:
        if (tn.rules is not None): 
            for r in tn.rules: 
                MorphSerializeHelper.__serialize_short(res, r._id0_)
        MorphSerializeHelper.__serialize_short(res, 0)
        if (tn.reverce_variants is not None): 
            for v in tn.reverce_variants: 
                MorphSerializeHelper.__serialize_string(res, Utils.ifNotNull(v.tail, ""))
                if (v.rule is not None): 
                    pass
                MorphSerializeHelper.__serialize_short(res, (0 if v.rule is None else v.rule._id0_))
                MorphSerializeHelper.__serialize_short(res, v.coef)
                MorphSerializeHelper.__serialize_morph_rule_variant(res, v)
        MorphSerializeHelper.__serialize_string(res, None)
        if (tn.nodes is not None): 
            for n in tn.nodes.items(): 
                MorphSerializeHelper.__serialize_short(res, n[0])
                p0 = res.tell()
                MorphSerializeHelper.__serialize_int(res, 0)
                MorphSerializeHelper.__serialize_morph_tree_node(res, n[1])
                p1 = res.tell()
                res.seek(p0, io.SEEK_SET)
                MorphSerializeHelper.__serialize_int(res, p1)
                res.seek(p1, io.SEEK_SET)
        MorphSerializeHelper.__serialize_short(res, 0xFFFF)
    
    @staticmethod
    def __deserialize_morph_tree_node_base(str0_ : 'ByteArrayWrapper', tn : 'MorphTreeNode', me : 'MorphEngine', pos : int) -> None:
        while not str0_.iseof(pos.value):
            i = str0_.deserialize_short(pos)
            i -= 1
            if ((i < 0) or i >= len(me.m_rules)): 
                break
            r = me.m_rules[i]
            if (tn.rules is None): 
                tn.rules = list()
            tn.rules.append(r)
        while not str0_.iseof(pos.value):
            tail = str0_.deserialize_string(pos)
            if (tail is None): 
                break
            rule_id = str0_.deserialize_short(pos)
            coef = str0_.deserialize_short(pos)
            v = MorphSerializeHelper.__deserialize_morph_rule_variant(str0_, me, pos)
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
    def _deserialize_morph_tree_node_lazy(str0_ : 'ByteArrayWrapper', tn : 'MorphTreeNode', me : 'MorphEngine', pos : int) -> None:
        MorphSerializeHelper.__deserialize_morph_tree_node_base(str0_, tn, me, pos)
        while not str0_.iseof(pos.value):
            i = str0_.deserialize_short(pos)
            if (i == 0xFFFF): 
                break
            pp = str0_.deserialize_int(pos)
            child = MorphTreeNode()
            child.lazy_pos = pos.value
            if (tn.nodes is None): 
                tn.nodes = dict()
            tn.nodes[i] = child
            pos.value = pp
        p = pos.value
        if (tn.rules is not None): 
            for r in tn.rules: 
                if (r.lazy_pos > 0): 
                    pos.value = r.lazy_pos
                    MorphSerializeHelper.__deserialize_morph_rule(str0_, r, me, pos)
                    r.lazy_pos = 0
            pos.value = p
    
    @staticmethod
    def __deserialize_morph_tree_node(str0_ : 'ByteArrayWrapper', tn : 'MorphTreeNode', me : 'MorphEngine', pos : int) -> int:
        res = 0
        MorphSerializeHelper.__deserialize_morph_tree_node_base(str0_, tn, me, pos)
        while not str0_.iseof(pos.value):
            i = str0_.deserialize_short(pos)
            if (i == 0xFFFF): 
                break
            pp = str0_.deserialize_int(pos)
            child = MorphTreeNode()
            if (tn.nodes is None): 
                tn.nodes = dict()
            tn.nodes[i] = child
            res += 1
            res += MorphSerializeHelper.__deserialize_morph_tree_node(str0_, child, me, pos)
        return res
    
    MAX_VARIANTS = 0
    
    @staticmethod
    def __manage_reverce_nodes(root : 'MorphTreeNode', tn : 'MorphTreeNode', term : str) -> None:
        if (tn.rules is not None): 
            for r in tn.rules: 
                for v in r.variants.items(): 
                    wf = term + v[0]
                    if (len(wf) <= MorphSerializeHelper.__min_tail_len): 
                        continue
                    rtn = root
                    lev = 0
                    first_pass2901 = True
                    while True:
                        if first_pass2901: first_pass2901 = False
                        else: lev += 1
                        if (not (lev < MorphSerializeHelper.__max_tail_len)): break
                        i = len(wf) - 1 - lev
                        if (i < 0): 
                            break
                        ch = ord(wf[i])
                        if (rtn.nodes is None): 
                            rtn.nodes = dict()
                        next0_ = None
                        wrapnext52 = RefOutArgWrapper(None)
                        inoutres53 = Utils.tryGetValue(rtn.nodes, ch, wrapnext52)
                        next0_ = wrapnext52.value
                        if (not inoutres53): 
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
                MorphSerializeHelper.__manage_reverce_nodes(root, tch[1], "{0}{1}".format(term, (chr(tch[0]))))
    
    __min_tail_len = 4
    
    __max_tail_len = 7