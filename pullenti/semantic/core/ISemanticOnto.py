# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


class ISemanticOnto:
    """ Интерфейс внешней дополнительной онтологии
     (для улучшения качества семантичсекой обработки) """
    
    def check_link(self, master : str, slave : str) -> bool:
        """ Проверка, что в онтологии слова master и slave образуют устойчивую пару
        
        Args:
            master(str): 
            slave(str): 
        
        """
        return None