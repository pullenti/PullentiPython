# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class ISemanticOnto:
    """ Интерфейс внешней дополнительной онтологии
    (для улучшения качества семантичсекой обработки)
    Внешняя онтология
    """
    
    def check_link(self, master : str, slave : str) -> bool:
        """ Проверка, что в онтологии слова master и slave образуют устойчивую пару
        
        Args:
            master(str): 
            slave(str): 
        
        """
        return None