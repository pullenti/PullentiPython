# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.morph.LanguageHelper import LanguageHelper


class TransportReferent(Referent):
    
    def __init__(self) -> None:
        from pullenti.ner.transport.internal.MetaTransport import MetaTransport
        super().__init__(TransportReferent.OBJ_TYPENAME)
        self.instance_of = MetaTransport._global_meta
    
    OBJ_TYPENAME = "TRANSPORT"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_BRAND = "BRAND"
    
    ATTR_MODEL = "MODEL"
    
    ATTR_CLASS = "CLASS"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_NUMBER_REGION = "NUMBER_REG"
    
    ATTR_KIND = "KIND"
    
    ATTR_STATE = "STATE"
    
    ATTR_ORG = "ORG"
    
    ATTR_DATE = "DATE"
    
    ATTR_ROUTEPOINT = "ROUTEPOINT"
    
    def toString(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = io.StringIO()
        str0_ = None
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_TYPE): 
                n = s.value
                if (str0_ is None or (len(n) < len(str0_))): 
                    str0_ = n
        if (str0_ is not None): 
            print(str0_, end="", file=res)
        elif (self.kind == TransportKind.AUTO): 
            print("автомобиль", end="", file=res)
        elif (self.kind == TransportKind.FLY): 
            print("самолет", end="", file=res)
        elif (self.kind == TransportKind.SHIP): 
            print("судно", end="", file=res)
        elif (self.kind == TransportKind.SPACE): 
            print("космический корабль", end="", file=res)
        else: 
            print(Utils.enumToString(self.kind), end="", file=res)
        str0_ = self.getStringValue(TransportReferent.ATTR_BRAND)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convertFirstCharUpperAndOtherLower(str0_)), end="", file=res, flush=True)
        str0_ = self.getStringValue(TransportReferent.ATTR_MODEL)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convertFirstCharUpperAndOtherLower(str0_)), end="", file=res, flush=True)
        str0_ = self.getStringValue(TransportReferent.ATTR_NAME)
        if ((str0_) is not None): 
            print(" \"{0}\"".format(MiscHelper.convertFirstCharUpperAndOtherLower(str0_)), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == TransportReferent.ATTR_NAME and str0_ != (s.value)): 
                    if (LanguageHelper.isCyrillicChar(str0_[0]) != LanguageHelper.isCyrillicChar((s.value)[0])): 
                        print(" ({0})".format(MiscHelper.convertFirstCharUpperAndOtherLower(s.value)), end="", file=res, flush=True)
                        break
        str0_ = self.getStringValue(TransportReferent.ATTR_CLASS)
        if ((str0_) is not None): 
            print(" класса \"{0}\"".format(MiscHelper.convertFirstCharUpperAndOtherLower(str0_)), end="", file=res, flush=True)
        str0_ = self.getStringValue(TransportReferent.ATTR_NUMBER)
        if ((str0_) is not None): 
            print(", номер {0}".format(str0_), end="", file=res, flush=True)
            str0_ = self.getStringValue(TransportReferent.ATTR_NUMBER_REGION)
            if ((str0_) is not None): 
                print(str0_, end="", file=res)
        if (self.findSlot(TransportReferent.ATTR_ROUTEPOINT, None, True) is not None): 
            print(" (".format(), end="", file=res, flush=True)
            fi = True
            for s in self.slots: 
                if (s.type_name == TransportReferent.ATTR_ROUTEPOINT): 
                    if (fi): 
                        fi = False
                    else: 
                        print(" - ", end="", file=res)
                    if (isinstance(s.value, Referent)): 
                        print((Utils.asObjectOrNull(s.value, Referent)).toString(True, lang, 0), end="", file=res)
                    else: 
                        print(s.value, end="", file=res)
            print(")", end="", file=res)
        if (not short_variant): 
            str0_ = self.getStringValue(TransportReferent.ATTR_STATE)
            if ((str0_) is not None): 
                print("; {0}".format(str0_), end="", file=res, flush=True)
            str0_ = self.getStringValue(TransportReferent.ATTR_ORG)
            if ((str0_) is not None): 
                print("; {0}".format(str0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'TransportKind':
        """ Класс сущности (авто, авиа, аква ...) """
        return self.__getKind(self.getStringValue(TransportReferent.ATTR_KIND))
    @kind.setter
    def kind(self, value) -> 'TransportKind':
        if (value != TransportKind.UNDEFINED): 
            self.addSlot(TransportReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    def __getKind(self, s : str) -> 'TransportKind':
        if (s is None): 
            return TransportKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, TransportKind)
            if (isinstance(res, TransportKind)): 
                return Utils.valToEnum(res, TransportKind)
        except Exception as ex2561: 
            pass
        return TransportKind.UNDEFINED
    
    def _addGeo(self, r : object) -> None:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (isinstance(r, GeoReferent)): 
            self.addSlot(TransportReferent.ATTR_STATE, r, False, 0)
        elif (isinstance(r, ReferentToken)): 
            if (isinstance((Utils.asObjectOrNull(r, ReferentToken)).getReferent(), GeoReferent)): 
                self.addSlot(TransportReferent.ATTR_STATE, (Utils.asObjectOrNull(r, ReferentToken)).getReferent(), True, 0)
                self.addExtReferent(Utils.asObjectOrNull(r, ReferentToken))
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        tr = Utils.asObjectOrNull(obj, TransportReferent)
        if (tr is None): 
            return False
        k1 = self.kind
        k2 = tr.kind
        if (k1 != k2): 
            if (k1 == TransportKind.SPACE and tr.findSlot(TransportReferent.ATTR_TYPE, "КОРАБЛЬ", True) is not None): 
                pass
            elif (k2 == TransportKind.SPACE and self.findSlot(TransportReferent.ATTR_TYPE, "КОРАБЛЬ", True) is not None): 
                k1 = TransportKind.SPACE
            else: 
                return False
        sl = self.findSlot(TransportReferent.ATTR_ORG, None, True)
        if (sl is not None and tr.findSlot(TransportReferent.ATTR_ORG, None, True) is not None): 
            if (tr.findSlot(TransportReferent.ATTR_ORG, sl.value, False) is None): 
                return False
        sl = self.findSlot(TransportReferent.ATTR_STATE, None, True)
        if (sl is not None and tr.findSlot(TransportReferent.ATTR_STATE, None, True) is not None): 
            if (tr.findSlot(TransportReferent.ATTR_STATE, sl.value, True) is None): 
                return False
        s1 = self.getStringValue(TransportReferent.ATTR_NUMBER)
        s2 = tr.getStringValue(TransportReferent.ATTR_NUMBER)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (s1 != s2): 
                    return False
                s1 = self.getStringValue(TransportReferent.ATTR_NUMBER_REGION)
                s2 = tr.getStringValue(TransportReferent.ATTR_NUMBER_REGION)
                if (s1 is not None or s2 is not None): 
                    if (s1 is None or s2 is None): 
                        if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                            return False
                    elif (s1 != s2): 
                        return False
                return True
        s1 = self.getStringValue(TransportReferent.ATTR_BRAND)
        s2 = tr.getStringValue(TransportReferent.ATTR_BRAND)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        s1 = self.getStringValue(TransportReferent.ATTR_MODEL)
        s2 = tr.getStringValue(TransportReferent.ATTR_MODEL)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_NAME): 
                if (tr.findSlot(TransportReferent.ATTR_NAME, s.value, True) is not None): 
                    return True
        if (s1 is not None and s2 is not None): 
            return True
        return False
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().mergeSlots(obj, merge_statistic)
        kinds = list()
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_KIND): 
                ki = self.__getKind(s.value)
                if (not ki in kinds): 
                    kinds.append(ki)
        if (len(kinds) > 0): 
            if (TransportKind.SPACE in kinds): 
                for i in range(len(self.slots) - 1, -1, -1):
                    if (self.slots[i].type_name == TransportReferent.ATTR_KIND and self.__getKind(self.slots[i].value) != TransportKind.SPACE): 
                        del self.slots[i]
    
    def _check(self, on_attach : bool) -> bool:
        ki = self.kind
        if (ki == TransportKind.UNDEFINED): 
            return False
        if (self.findSlot(TransportReferent.ATTR_NUMBER, None, True) is not None): 
            if (self.findSlot(TransportReferent.ATTR_NUMBER_REGION, None, True) is None and (len(self.slots) < 3)): 
                return False
            return True
        model = self.getStringValue(TransportReferent.ATTR_MODEL)
        has_num = False
        if (model is not None): 
            for s in model: 
                if (not str.isalpha(s)): 
                    has_num = True
                    break
        if (ki == TransportKind.AUTO): 
            if (self.findSlot(TransportReferent.ATTR_BRAND, None, True) is not None): 
                if (on_attach): 
                    return True
                if (not has_num and self.findSlot(TransportReferent.ATTR_TYPE, None, True) is None): 
                    return False
                return True
            if (model is not None and on_attach): 
                return True
            return False
        if (model is not None): 
            if (not has_num and ki == TransportKind.FLY and self.findSlot(TransportReferent.ATTR_BRAND, None, True) is None): 
                return False
            return True
        if (self.findSlot(TransportReferent.ATTR_NAME, None, True) is not None): 
            nam = self.getStringValue(TransportReferent.ATTR_NAME)
            if (ki == TransportKind.FLY and nam.startswith("Аэрофлот")): 
                return False
            return True
        if (ki == TransportKind.TRAIN): 
            pass
        return False