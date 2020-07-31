# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.semantic.utils.ControlModelItemType import ControlModelItemType
from pullenti.semantic.utils.ControlModelItem import ControlModelItem

class ControlModel:
    """ Новая модель управления """
    
    def __init__(self) -> None:
        self.items = list()
        self.pacients = list()
    
    def find_item_by_typ(self, typ : 'ControlModelItemType') -> 'ControlModelItem':
        for it in self.items: 
            if (it.typ == typ): 
                return it
        return None
    
    def find_item(self, w : 'DerivateWord') -> 'ControlModelItem':
        for it in self.items: 
            if (it.check(w)): 
                return it
        return None
    
    @property
    def is_empty(self) -> bool:
        for it in self.items: 
            if (not it.ignorable and len(it.links) > 0): 
                return False
        return len(self.pacients) == 0
    
    def __str__(self) -> str:
        res = io.StringIO()
        for it in self.items: 
            if (it.ignorable): 
                continue
            if (res.tell() > 0): 
                print("; ", end="", file=res)
            print("{0} = {1}".format((it.word if it.typ == ControlModelItemType.WORD else Utils.enumToString(it.typ)), len(it.links)), end="", file=res, flush=True)
        for p in self.pacients: 
            print(" ({0})".format(p), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def correct(self, gr : 'DerivateGroup') -> None:
        has = False
        it = self.find_item_by_typ(ControlModelItemType.VERB)
        if (it is not None): 
            has = True
        elif (self.find_item_by_typ(ControlModelItemType.REFLEXIVE) is not None): 
            has = True
        if (has): 
            for i in range(len(self.items) - 1, -1, -1):
                if (self.items[i].typ == ControlModelItemType.WORD): 
                    self.items[i].links.clear()
    
    def serialize_string(self) -> str:
        res = io.StringIO()
        with XmlWriter.create_string(res, null) as xml0_: 
            self.serialize(xml0_)
        i = Utils.toStringStringIO(res).find('>')
        if (i > 10 and Utils.getCharAtStringIO(res, 1) == '?'): 
            Utils.removeStringIO(res, 0, i + 1)
        str0_ = Utils.toStringStringIO(res)
        return str0_
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("model")
        for it in self.items: 
            if (not it.ignorable): 
                it.serialize_xml(xml0_)
        for p in self.pacients: 
            xml0_.write_element_string("pac", p)
        xml0_.write_end_element()
    
    def deserialize_string(self, str0_ : str) -> None:
        doc = None # new XmlDocument
        doc = Utils.parseXmlFromString(str0_)
        self.deserialize(doc.getroot())
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (x.tag == "item"): 
                it = ControlModelItem()
                it.deserialize_xml(x)
                self.items.append(it)
            elif (x.tag == "pac"): 
                self.pacients.append(Utils.getXmlInnerText(x))