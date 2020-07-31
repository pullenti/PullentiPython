# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.semantic.core.SemanticRole import SemanticRole
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.semantic.utils.ControlModelItemType import ControlModelItemType
from pullenti.semantic.utils.QuestionType import QuestionType
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.ControlModelQuestion import ControlModelQuestion
from pullenti.semantic.internal.NextModelItem import NextModelItem
from pullenti.semantic.utils.ControlModelItem import ControlModelItem
from pullenti.morph.MorphLang import MorphLang
from pullenti.semantic.utils.DerivateWord import DerivateWord
from pullenti.semantic.utils.DerivateGroup import DerivateGroup
from pullenti.semantic.internal.ExplanTreeNode import ExplanTreeNode
from pullenti.morph.MorphAspect import MorphAspect
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper

class DeserializeHelper:
    
    @staticmethod
    def deserializedd(str0_ : io.IOBase, dic : 'DerivateDictionary', lazy_load : bool) -> 'ByteArrayWrapper':
        wr = None
        with io.BytesIO() as tmp: 
            MorphSerializeHelper.deflate_gzip(str0_, tmp)
            wr = ByteArrayWrapper(bytearray(tmp.getvalue()))
            pos = 0
            wrappos2993 = RefOutArgWrapper(pos)
            cou = wr.deserialize_int(wrappos2993)
            pos = wrappos2993.value
            while cou > 0: 
                wrappos2991 = RefOutArgWrapper(pos)
                p1 = wr.deserialize_int(wrappos2991)
                pos = wrappos2991.value
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy_pos = pos
                    pos = p1
                else: 
                    wrappos2990 = RefOutArgWrapper(pos)
                    DeserializeHelper.deserialize_derivate_group(wr, ew, wrappos2990)
                    pos = wrappos2990.value
                dic._m_all_groups.append(ew)
                cou -= 1
            dic._m_root = ExplanTreeNode()
            wrappos2992 = RefOutArgWrapper(pos)
            DeserializeHelper.deserialize_tree_node(wr, dic, dic._m_root, lazy_load, wrappos2992)
            pos = wrappos2992.value
        return wr
    
    @staticmethod
    def deserialize_derivate_group(str0_ : 'ByteArrayWrapper', dg : 'DerivateGroup', pos : int) -> None:
        attr = str0_.deserialize_short(pos)
        if (((attr & 1)) != 0): 
            dg.is_dummy = True
        if (((attr & 2)) != 0): 
            dg.not_generate = True
        dg.prefix = str0_.deserialize_string(pos)
        DeserializeHelper.deserialize_control_model(str0_, dg.model, pos)
        DeserializeHelper.deserialize_old_control_model(str0_, dg.cm, pos)
        DeserializeHelper.deserialize_old_control_model(str0_, dg.cm_rev, pos)
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            w = DerivateWord(dg)
            w.spelling = str0_.deserialize_string(pos)
            w.class0_ = MorphClass()
            w.class0_.value = (str0_.deserialize_short(pos))
            w.lang = MorphLang._new75(str0_.deserialize_short(pos))
            w.attrs.value = (str0_.deserialize_short(pos))
            w.aspect = (Utils.valToEnum(str0_.deserialize_byte(pos), MorphAspect))
            w.tense = (Utils.valToEnum(str0_.deserialize_byte(pos), MorphTense))
            w.voice = (Utils.valToEnum(str0_.deserialize_byte(pos), MorphVoice))
            cou1 = str0_.deserialize_byte(pos)
            while cou1 > 0: 
                n = str0_.deserialize_string(pos)
                if (w.next_words is None): 
                    w.next_words = list()
                if (n is not None): 
                    w.next_words.append(n)
                cou1 -= 1
            dg.words.append(w)
            cou -= 1
    
    @staticmethod
    def deserialize_control_model(str0_ : 'ByteArrayWrapper', cm : 'ControlModel', pos : int) -> None:
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            it = ControlModelItem()
            cm.items.append(it)
            b = str0_.deserialize_byte(pos)
            if ((((b) & 0x80)) != 0): 
                it.nominative_can_be_agent_and_pacient = True
            it.typ = (Utils.valToEnum(((b) & 0x7F), ControlModelItemType))
            if (it.typ == ControlModelItemType.WORD): 
                it.word = str0_.deserialize_string(pos)
            licou = str0_.deserialize_short(pos)
            while licou > 0: 
                i = str0_.deserialize_byte(pos)
                r = Utils.valToEnum(str0_.deserialize_byte(pos), SemanticRole)
                if (i >= 0 and (i < len(ControlModelQuestion.ITEMS))): 
                    it.links[ControlModelQuestion.ITEMS[i]] = r
                licou -= 1
            cou -= 1
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            p = str0_.deserialize_string(pos)
            if (p is not None): 
                cm.pacients.append(p)
            cou -= 1
    
    @staticmethod
    def deserialize_old_control_model(str0_ : 'ByteArrayWrapper', cm : 'ControlModelOld', pos : int) -> None:
        cm.transitive = str0_.deserialize_byte(pos) != (0)
        cm.questions = (Utils.valToEnum(str0_.deserialize_short(pos), QuestionType))
        sh = str0_.deserialize_short(pos)
        if (sh != 0): 
            pr = str0_.deserialize_string(pos)
            cas = MorphCase()
            cas.value = (sh)
            cm.agent = NextModelItem(pr, cas)
        sh = str0_.deserialize_short(pos)
        if (sh != 0): 
            pr = str0_.deserialize_string(pos)
            cas = MorphCase()
            cas.value = (sh)
            cm.pacient = NextModelItem(pr, cas)
        sh = str0_.deserialize_short(pos)
        if (sh != 0): 
            pr = str0_.deserialize_string(pos)
            cas = MorphCase()
            cas.value = (sh)
            cm.instrument = NextModelItem(pr, cas)
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            pref = Utils.ifNotNull(str0_.deserialize_string(pos), "")
            cas = MorphCase()
            cas.value = (str0_.deserialize_short(pos))
            if (cm.nexts is None): 
                cm.nexts = dict()
            cm.nexts[pref] = cas
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