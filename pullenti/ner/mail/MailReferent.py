# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.mail.MailKind import MailKind
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.mail.internal.MetaLetter import MetaLetter
from pullenti.ner.person.PersonReferent import PersonReferent

class MailReferent(Referent):
    """ Сущность - блок письма
    
    """
    
    def __init__(self) -> None:
        super().__init__(MailReferent.OBJ_TYPENAME)
        self.instance_of = MetaLetter._global_meta
    
    OBJ_TYPENAME = "MAIL"
    """ Имя типа сущности TypeName ("MAIL") """
    
    ATTR_KIND = "TYPE"
    """ Имя атрибута - тип блока (MailKind) """
    
    ATTR_TEXT = "TEXT"
    """ Имя атрибута - текст блока """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность """
    
    @property
    def kind(self) -> 'MailKind':
        """ Тип блока письма """
        val = self.get_string_value(MailReferent.ATTR_KIND)
        try: 
            if (val is not None): 
                return Utils.valToEnum(val, MailKind)
        except Exception as ex1605: 
            pass
        return MailKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'MailKind':
        self.add_slot(MailReferent.ATTR_KIND, Utils.enumToString(value).upper(), True, 0)
        return value
    
    @property
    def text(self) -> str:
        """ Текст блока """
        return self.get_string_value(MailReferent.ATTR_TEXT)
    @text.setter
    def text(self, value) -> str:
        self.add_slot(MailReferent.ATTR_TEXT, value, True, 0)
        return value
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        print("{0}: ".format(Utils.enumToString(self.kind)), end="", file=res, flush=True)
        for s in self.slots: 
            if (s.type_name == MailReferent.ATTR_REF and (isinstance(s.value, Referent))): 
                print("{0}, ".format(s.value.to_string(True, lang, lev + 1)), end="", file=res, flush=True)
        if (res.tell() < 100): 
            str0_ = Utils.ifNotNull(self.text, "")
            str0_ = str0_.replace('\r', ' ').replace('\n', ' ')
            if (len(str0_) > 100): 
                str0_ = (str0_[0:0+100] + "...")
            print(str0_, end="", file=res)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        return obj == self
    
    def _add_ref(self, r : 'Referent', lev : int=0) -> None:
        if (r is None or lev > 4): 
            return
        if ((((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent)) or r.type_name == "ORGANIZATION") or r.type_name == "PHONE" or r.type_name == "URI") or (isinstance(r, GeoReferent)) or (isinstance(r, AddressReferent))): 
            self.add_slot(MailReferent.ATTR_REF, r, False, 0)
        for s in r.slots: 
            if (isinstance(s.value, Referent)): 
                self._add_ref(Utils.asObjectOrNull(s.value, Referent), lev + 1)
    
    @staticmethod
    def _new1601(_arg1 : 'MailKind') -> 'MailReferent':
        res = MailReferent()
        res.kind = _arg1
        return res