# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaBank(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        MetaBank._global_meta = MetaBank()
        MetaBank._global_meta.add_feature(BankDataReferent.ATTR_ITEM, "Элемент", 0, 0).show_as_parent = True
        MetaBank._global_meta.add_feature(BankDataReferent.ATTR_BANK, "Банк", 0, 1)
        MetaBank._global_meta.add_feature(BankDataReferent.ATTR_CORBANK, "Банк К/С", 0, 1)
        MetaBank._global_meta.add_feature(BankDataReferent.ATTR_MISC, "Разное", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        return BankDataReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Банковские реквизиты"
    
    IMAGE_ID = "bankreq"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaBank.IMAGE_ID
    
    _global_meta = None