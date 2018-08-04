# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.chat.ChatType import ChatType
from pullenti.ner.chat.VerbType import VerbType



class ChatReferent(Referent):
    
    def __init__(self) -> None:
        from pullenti.ner.chat.internal.MetaChat import MetaChat
        super().__init__(ChatReferent.OBJ_TYPENAME)
        self.instance_of = MetaChat._global_meta
    
    OBJ_TYPENAME = "CHAT"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_NOT = "NOT"
    
    ATTR_VERBTYPE = "VERBTYPE"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = Utils.newStringIO(None)
        print(Utils.enumToString(self.typ), end="", file=res)
        if (self.not0_): 
            print(" not", end="", file=res)
        val = self.value
        if (val is not None): 
            print(" {0}".format(val), end="", file=res, flush=True)
        vty = self.verb_types
        if (len(vty) > 0): 
            print("[", end="", file=res)
            for i in range(len(vty)):
                if (i > 0): 
                    print(", ", end="", file=res)
                print(Utils.enumToString(vty[i]), end="", file=res)
            print("]", end="", file=res)
        return Utils.toStringStringIO(res)
    
    @property
    def typ(self) -> 'ChatType':
        """ Тип элемента """
        str0_ = self.get_string_value(ChatReferent.ATTR_TYPE)
        if (Utils.isNullOrEmpty(str0_)): 
            return ChatType.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, ChatType)
        except Exception as ex472: 
            pass
        return ChatType.UNDEFINED
    
    @typ.setter
    def typ(self, value_) -> 'ChatType':
        self.add_slot(ChatReferent.ATTR_TYPE, Utils.enumToString(value_).upper(), True, 0)
        return value_
    
    @property
    def not0_(self) -> bool:
        return self.get_string_value(ChatReferent.ATTR_NOT) == "true"
    
    @not0_.setter
    def not0_(self, value_) -> bool:
        if (not value_): 
            self.add_slot(ChatReferent.ATTR_NOT, None, True, 0)
        else: 
            self.add_slot(ChatReferent.ATTR_NOT, "true", True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Базовое значение """
        return self.get_string_value(ChatReferent.ATTR_VALUE)
    
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(ChatReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def verb_types(self) -> typing.List['VerbType']:
        res = list()
        for s in self.slots: 
            if (s.type_name == ChatReferent.ATTR_VERBTYPE): 
                try: 
                    res.append(Utils.valToEnum(s.value if isinstance(s.value, str) else None, VerbType))
                except Exception as ex473: 
                    pass
        return res
    
    def add_verb_type(self, vt : 'VerbType') -> None:
        self.add_slot(ChatReferent.ATTR_VERBTYPE, Utils.enumToString(vt).upper(), False, 0)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        tr = (obj if isinstance(obj, ChatReferent) else None)
        if (tr is None): 
            return False
        if (tr.typ != self.typ): 
            return False
        if (tr.value != self.value): 
            return False
        if (tr.not0_ != self.not0_): 
            return False
        return True

    
    @staticmethod
    def _new471(_arg1 : 'ChatType') -> 'ChatReferent':
        res = ChatReferent()
        res.typ = _arg1
        return res