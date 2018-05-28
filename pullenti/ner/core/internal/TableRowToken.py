# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.MetaToken import MetaToken


class TableRowToken(MetaToken):
    """ Токен - строка таблицы из текста """
    
    def __init__(self, b : 'Token', e0 : 'Token') -> None:
        self.cells = list()
        self._eor = False
        self._last_row = False
        super().__init__(b, e0, None)
    
    def __str__(self) -> str:
        return "ROW ({0} cells) : {1}".format(len(self.cells), self.get_source_text())