# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class MorphRuleVariantRef:
    
    def __init__(self, rid : int, vid : int, co : int) -> None:
        self.rule_id = 0
        self.variant_id = 0
        self.coef = 0
        self.rule_id = rid
        self.variant_id = vid
        self.coef = co
    
    def __str__(self) -> str:
        return "{0} {1}".format(self.rule_id, self.variant_id)