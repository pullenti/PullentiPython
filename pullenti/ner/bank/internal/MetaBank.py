# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.ReferentClass import ReferentClass


class MetaBank(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        super().__init__()
        self.addFeature(BankDataReferent.ATTR_ITEM, "Элемент", 0, 0).show_as_parent = True
        self.addFeature(BankDataReferent.ATTR_BANK, "Банк", 0, 1)
        self.addFeature(BankDataReferent.ATTR_CORBANK, "Банк К/С", 0, 1)
        self.addFeature(BankDataReferent.ATTR_MISC, "Разное", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        return BankDataReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Банковские реквизиты"
    
    IMAGE_ID = "bankreq"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaBank.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaBank
    @staticmethod
    def _static_ctor():
        MetaBank._global_meta = MetaBank()

MetaBank._static_ctor()