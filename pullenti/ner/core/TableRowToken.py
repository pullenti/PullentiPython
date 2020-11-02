# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.MetaToken import MetaToken

class TableRowToken(MetaToken):
    # Токен - строка таблицы из текста
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.cells = list()
        self._eor = False
        self._last_row = False
    
    def __str__(self) -> str:
        return "ROW ({0} cells) : {1}".format(len(self.cells), self.get_source_text())