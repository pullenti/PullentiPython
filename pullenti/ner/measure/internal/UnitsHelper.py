# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors


class UnitsHelper:
    
    UNITS = None
    
    TERMINS = None
    
    UGRADUS = None
    
    UGRADUSC = None
    
    UGRADUSF = None
    
    UPERCENT = None
    
    UOM = None
    
    UHOUR = None
    
    USEC = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        UnitsHelper.UNITS = list()
        UnitsHelper.TERMINS = TerminCollection()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        u = Unit("м", "m", "метр", "meter")
        u.keywords.extend(["ДЛИНА", "ДЛИННА", "ШИРИНА", "ГЛУБИНА", "ВЫСОТА", "РАЗМЕР", "ГАБАРИТ", "РАССТОЯНИЕ", "РАДИУС", "ПЕРИМЕТР", "ДИАМЕТР", "ПОДАЧА", "НАПОР", "LENGTH", "WIDTH", "DEPTH", "HEIGHT", "SIZE", "ENVELOPE", "DISTANCE", "RADIUS", "PERIMETER", "DIAMETER", "FLOW", "PRESSURE", "ДОВЖИНА", "ШИРИНА", "ГЛИБИНА", "ВИСОТА", "РОЗМІР", "ГАБАРИТ", "ВІДСТАНЬ", "РАДІУС", "ДІАМЕТР", "НАТИСК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("МЕТР", u)
        t.add_variant("МЕТРОВЫЙ", False)
        t.add_variant("МЕТРОВИЙ", False)
        t.add_variant("METER", False)
        t.add_abridge("М.")
        t.add_abridge("M.")
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.DECI, UnitsFactors.CENTI, UnitsFactors.MILLI, UnitsFactors.MICRO, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "М.", "M.", "МЕТР;МЕТРОВЫЙ", "МЕТР;МЕТРОВИЙ", "METER;METRE")
        uu = Unit("миль", "mile", "морская миля", "mile")
        uu.base_unit = u
        uu.base_multiplier = 1852
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МИЛЯ", uu)
        t.add_variant("МОРСКАЯ МИЛЯ", False)
        t.add_abridge("NMI")
        t.add_variant("MILE", False)
        t.add_variant("NAUTICAL MILE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("фут", "ft", "фут", "foot", u, 0.304799472)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ФУТ", uu)
        t.add_abridge("FT.")
        t.add_variant("FOOT", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("дюйм", "in", "дюйм", "inch", u, 0.0254)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ДЮЙМ", uu)
        t.add_abridge("IN")
        t.add_variant("INCH", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("ар", "are", "ар", "are")
        u.keywords.extend(["ПЛОЩАДЬ", "ПРОЩИНА", "AREA", "SQWARE", "SPACE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("АР", u)
        t.add_variant("ARE", False)
        t.add_variant("СОТКА", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit("га", "ga", "гектар", "hectare")
        uu.base_unit = u
        uu.base_multiplier = 100
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ГЕКТАР", uu)
        t.add_variant("HECTARE", False)
        t.add_abridge("ГА")
        t.add_abridge("GA")
        UnitsHelper.TERMINS.add(t)
        u = Unit("г", "g", "грамм", "gram")
        u.keywords.extend(["ВЕС", "ТЯЖЕСТЬ", "НЕТТО", "БРУТТО", "МАССА", "WEIGHT", "NET", "GROSS", "MASS", "ВАГА", "ТЯЖКІСТЬ", "МАСА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ГРАММ", u)
        t.add_abridge("Г.")
        t.add_abridge("ГР.")
        t.add_abridge("G.")
        t.add_abridge("GR.")
        t.add_variant("ГРАММОВЫЙ", False)
        t.add_variant("ГРАММНЫЙ", False)
        t.add_variant("ГРАМОВИЙ", False)
        t.add_variant("GRAM", False)
        t.add_variant("GRAMME", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "Г.;ГР;", "G.;GR.", "ГРАМ;ГРАММ;ГРАММНЫЙ", "ГРАМ;ГРАМОВИЙ", "GRAM;GRAMME")
        uu = Unit._new1533("ц", "centner", "центнер", "centner", u, 100000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ЦЕНТНЕР", uu)
        t.add_variant("CENTNER", False)
        t.add_variant("QUINTAL", False)
        t.add_abridge("Ц.")
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("т", "t", "тонна", "tonne", u, 1000000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ТОННА", uu)
        t.add_variant("TONNE", False)
        t.add_variant("TON", False)
        t.add_abridge("Т.")
        t.add_abridge("T.")
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.__add_factor(UnitsFactors.MEGA, uu, "Т", "T", "ТОННА;ТОННЫЙ", "ТОННА;ТОННИЙ", "TONNE;TON")
        u = Unit("л", "l", "литр", "liter")
        u.keywords.extend(["ОБЪЕМ", "ЕМКОСТЬ", "ВМЕСТИМОСЬ", "ОБСЯГ", "ЄМНІСТЬ", "МІСТКІСТЬ", "VOLUME", "CAPACITY"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ЛИТР", u)
        t.add_abridge("Л.")
        t.add_abridge("L.")
        t.add_variant("LITER", False)
        t.add_variant("LITRE", False)
        t.add_variant("ЛІТР", False)
        t.add_variant("ЛІТРОВИЙ", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MILLI, UnitsFactors.CENTI]: 
            UnitsHelper.__add_factor(f, u, "Л.", "L.", "ЛИТР;ЛИТРОВЫЙ", "ЛІТР;ЛІТРОВИЙ", "LITER;LITRE")
        uu = Unit._new1533("галлон", "gallon", "галлон", "gallon", u, 4.5461)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ГАЛЛОН", u)
        t.add_variant("ГАЛОН", False)
        t.add_variant("GALLON", False)
        t.add_abridge("ГАЛ")
        UnitsHelper.TERMINS.add(t)
        u = Unit("сек", "sec", "секунда", "second")
        UnitsHelper.USEC = u
        u.keywords.extend(["ВРЕМЯ", "ПРОДОЛЖИТЕЛЬНОСТЬ", "ЗАДЕРЖКА", "ДЛИТЕЛЬНОСТЬ", "ДОЛГОТА", "TIME", "DURATION", "DELAY", "ЧАС", "ТРИВАЛІСТЬ", "ЗАТРИМКА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("СЕКУНДА", u)
        t.add_abridge("С.")
        t.add_abridge("C.")
        t.add_abridge("СЕК")
        t.add_abridge("СЕК")
        t.add_abridge("S.")
        t.add_abridge("SEC")
        t.add_variant("СЕКУНДНЫЙ", False)
        t.add_variant("СЕКУНДНИЙ", False)
        t.add_variant("SECOND", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MILLI, UnitsFactors.MICRO]: 
            UnitsHelper.__add_factor(f, u, "С.;СЕК", "C;S.;SEC;", "СЕКУНДА;СЕКУНДНЫЙ", "СЕКУНДА;СЕКУНДНИЙ", "SECOND")
        uu = Unit("мин", "min", "минута", "minute")
        uu.base_unit = u
        uu.base_multiplier = 60
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МИНУТА", uu)
        t.add_abridge("МИН.")
        t.add_abridge("MIN.")
        t.add_variant("МИНУТНЫЙ", False)
        t.add_variant("ХВИЛИННИЙ", False)
        t.add_variant("ХВИЛИНА", False)
        t.add_variant("МІНУТА", False)
        t.add_variant("MINUTE", False)
        UnitsHelper.TERMINS.add(t)
        u = uu
        uu = Unit._new1533("ч", "h", "час", "hour", u, 60)
        UnitsHelper.UHOUR = uu
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ЧАС", uu)
        t.add_abridge("Ч.")
        t.add_abridge("H.")
        t.add_variant("ЧАСОВОЙ", False)
        t.add_variant("HOUR", False)
        t.add_variant("ГОДИННИЙ", False)
        t.add_variant("ГОДИНА", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("дн", "d", "день", "day")
        u.keywords.extend(UnitsHelper.USEC.keywords)
        u.keywords.extend(["ПОСТАВКА", "СРОК", "РАБОТА", "ЗАВЕРШЕНИЕ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ДЕНЬ", u)
        t.add_abridge("ДН.")
        t.add_abridge("Д.")
        t.add_variant("DAY", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("нед", "week", "неделя", "week", u, 7)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("НЕДЕЛЯ", uu)
        t.add_abridge("НЕД")
        t.add_variant("WEEK", False)
        t.add_variant("ТИЖДЕНЬ", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("мес", "mon", "месяц", "month", u, 30)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МЕСЯЦ", uu)
        t.add_abridge("МЕС")
        t.add_abridge("MON")
        t.add_variant("MONTH", False)
        t.add_variant("МІСЯЦЬ", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("г", "year", "год", "year", u, 365)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ГОД", uu)
        t.add_abridge("Г.")
        t.add_abridge("ГД")
        t.add_variant("YEAR", False)
        t.add_variant("РІК", False)
        t.add_variant("ЛЕТ", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUS = Unit("°", "°", "градус", "degree")
        UnitsHelper.UGRADUS.keywords.extend(["КРЕПОСТЬ", "АЛКОГОЛЬ", "ТЕМПЕРАТУРА", "ШИРОТА", "ДОЛГОТА", "АЗИМУТ", "ДОВГОТА", "ALCOHOL", "TEMPERATURE", "LATITUDE", "LONGITUDE", "AZIMUTH"])
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUS)
        t = Termin._new118("ГРАДУС", UnitsHelper.UGRADUS)
        t.add_variant("DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUSC = Unit("°C", "°C", "градус Цельсия", "celsius degree")
        UnitsHelper.UGRADUSC.keywords.append("ТЕМПЕРАТУРА")
        UnitsHelper.UGRADUS.keywords.append("TEMPERATURE")
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUSC)
        t = Termin._new118("ГРАДУС ЦЕЛЬСИЯ", UnitsHelper.UGRADUSC)
        t.add_variant("ГРАДУС ПО ЦЕЛЬСИЮ", False)
        t.add_variant("CELSIUS DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUSF = Unit("°F", "°F", "градус Фаренгейта", "Fahrenheit degree")
        UnitsHelper.UGRADUSF.keywords = UnitsHelper.UGRADUSC.keywords
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUSF)
        t = Termin._new118("ГРАДУС ФАРЕНГЕЙТА", UnitsHelper.UGRADUSF)
        t.add_variant("ГРАДУС ПО ФАРЕНГЕЙТУ", False)
        t.add_variant("FAHRENHEIT DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UPERCENT = Unit("%", "%", "процент", "percent")
        UnitsHelper.UNITS.append(UnitsHelper.UPERCENT)
        t = Termin._new118("ПРОЦЕНТ", UnitsHelper.UPERCENT)
        t.add_variant("ПРОЦ", False)
        t.add_variant("PERC", False)
        t.add_variant("PERCENT", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("об", "rot", "оборот", "rotation")
        UnitsHelper.UGRADUS.keywords.extend(["ЧАСТОТА", "ВРАЩЕНИЕ", "ВРАЩАТЕЛЬНЫЙ", "FREQUENCY", "ROTATION", "ROTATIONAL", "ОБЕРТАННЯ", "ОБЕРТАЛЬНИЙ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ОБОРОТ", u)
        t.add_abridge("ОБ.")
        t.add_abridge("ROT.")
        t.add_abridge("REV.")
        t.add_variant("ROTATION", False)
        t.add_variant("REVOLUTION", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("В", "V", "вольт", "volt")
        u.keywords.extend(["ЭЛЕКТРИЧЕСКИЙ", "ПОТЕНЦИАЛ", "НАПРЯЖЕНИЕ", "ЭЛЕКТРОДВИЖУЩИЙ", "ПИТАНИЕ", "ТОК", "ПОСТОЯННЫЙ", "ПЕРЕМЕННЫЙ", "ЕЛЕКТРИЧНИЙ", "ПОТЕНЦІАЛ", "НАПРУГА", "ЕЛЕКТРОРУШІЙНОЇ", "ХАРЧУВАННЯ", "СТРУМ", "ПОСТІЙНИЙ", "ЗМІННИЙ", "ELECTRIC", "POTENTIAL", "TENSION", "ELECTROMOTIVE", "FOOD", "CURRENT", "CONSTANT", "VARIABLE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ВОЛЬТ", u)
        t.add_variant("VOLT", False)
        t.add_abridge("V")
        t.add_abridge("В.")
        t.add_abridge("B.")
        t.add_variant("VAC", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.MILLI, UnitsFactors.MILLI, UnitsFactors.MICRO]: 
            UnitsHelper.__add_factor(f, u, "В.", "V.", "ВОЛЬТ;ВОЛЬТНЫЙ", "ВОЛЬТ;ВОЛЬТНІ", "VOLT")
        u = Unit("Вт", "W", "ватт", "watt")
        u.keywords.extend(["МОЩНОСТЬ", "ЭНЕРГИЯ", "ПОТОК", "ИЗЛУЧЕНИЕ", "ПОТУЖНІСТЬ", "ЕНЕРГІЯ", "ПОТІК", "ВИПРОМІНЮВАННЯ", "POWER", "ENERGY", "FLOW", "RADIATION"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ВАТТ", u)
        t.add_abridge("Вт")
        t.add_abridge("W")
        t.add_variant("WATT", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ВТ.", "W.", "ВАТТ;ВАТТНЫЙ", "ВАТ;ВАТНИЙ", "WATT;WATTS")
        uu = Unit._new1533("л.с.", "hp", "лошадиная сила", "horsepower", u, 735.49875)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ЛОШАДИНАЯ СИЛА", uu)
        t.add_abridge("Л.С.")
        t.add_abridge("ЛОШ.С.")
        t.add_abridge("ЛОШ.СИЛА")
        t.add_abridge("HP")
        t.add_abridge("PS")
        t.add_abridge("SV")
        t.add_variant("HORSEPOWER", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Дж", "J", "джоуль", "joule")
        u.keywords.extend(["РАБОТА", "ЭНЕРГИЯ", "ТЕПЛОТА", "ТЕПЛОВОЙ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ДЖОУЛЬ", u)
        t.add_abridge("ДЖ")
        t.add_abridge("J")
        t.add_variant("JOULE", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ДЖ.", "J.", "ДЖОУЛЬ", "ДЖОУЛЬ", "JOULE")
        u = Unit("К", "K", "кельвин", "kelvin")
        u.keywords.extend(UnitsHelper.UGRADUSC.keywords)
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("КЕЛЬВИН", u)
        t.add_abridge("К.")
        t.add_abridge("K.")
        t.add_variant("KELVIN", False)
        t.add_variant("КЕЛЬВІН", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "К.", "K.", "КЕЛЬВИН", "КЕЛЬВІН", "KELVIN")
        u = Unit("Гц", "Hz", "герц", "herz")
        u.keywords.extend(["ЧАСТОТА", "ЧАСТОТНЫЙ", "ПЕРИОДИЧНОСТЬ", "ПИТАНИЕ", "ЧАСТОТНИЙ", "ПЕРІОДИЧНІСТЬ", "FREQUENCY"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ГЕРЦ", u)
        t.add_abridge("HZ")
        t.add_abridge("ГЦ")
        t.add_variant("ГЕРЦОВЫЙ", False)
        t.add_variant("ГЕРЦОВИЙ", False)
        t.add_variant("HERZ", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO]: 
            UnitsHelper.__add_factor(f, u, "ГЦ.", "W.", "ГЕРЦ;ГЕРЦОВЫЙ", "ГЕРЦ;ГЕРЦОВИЙ", "HERZ")
        u = Unit("Ом", "Ω", "Ом", "Ohm")
        UnitsHelper.UOM = u
        u.keywords.extend(["СОПРОТИВЛЕНИЕ", "РЕЗИСТОР", "РЕЗИСТНЫЙ", "ИМПЕДАНС", "РЕЗИСТОРНЫЙ", "ОПІР", "РЕЗИСТИВНИЙ", "ІМПЕДАНС", "RESISTANCE", "RESISTOR", "RESISTIVE", "IMPEDANCE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ОМ", UnitsHelper.UOM)
        t.add_variant("OHM", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ОМ", "Ω", "ОМ", "ОМ", "OHM")
        u = Unit("А", "A", "ампер", "ampere")
        u.keywords.extend(["ТОК", "СИЛА", "ЭЛЕКТРИЧЕСКИЙ", "ЭЛЕКТРИЧЕСТВО", "МАГНИТ", "МАГНИТОДВИЖУЩИЙ", "ПОТРЕБЛЕНИЕ", "CURRENT", "POWER", "ELECTRICAL", "ELECTRICITY", "MAGNET", "MAGNETOMOTIVE", "CONSUMPTION", "СТРУМ", "ЕЛЕКТРИЧНИЙ", "ЕЛЕКТРИКА", "МАГНІТ", "МАГНИТОДВИЖУЩИЙ", "СПОЖИВАННЯ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("АМПЕР", u)
        t.add_abridge("A")
        t.add_abridge("А")
        t.add_variant("АМПЕРНЫЙ", False)
        t.add_variant("AMP", False)
        t.add_variant("AMPERE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1572("Ач", "Ah", "ампер-час", "ampere-hour", u, UnitsHelper.UHOUR)
        uu.keywords.extend(["ЗАРЯД", "АККУМУЛЯТОР", "АККУМУЛЯТОРНЫЙ", "ЗАРЯДКА", "БАТАРЕЯ", "CHARGE", "BATTERY", "CHARGING", "АКУМУЛЯТОР", "АКУМУЛЯТОРНИЙ"])
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("АМПЕР ЧАС", uu)
        t.add_abridge("АЧ")
        t.add_abridge("AH")
        t.add_variant("AMPERE HOUR", False)
        t.add_variant("АМПЕРЧАС", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            u1 = UnitsHelper.__add_factor(f, u, "А", "A", "АМПЕР;АМПЕРНЫЙ", "АМПЕР;АМПЕРНИЙ", "AMPERE;AMP")
            uu1 = UnitsHelper.__add_factor(f, uu, "АЧ", "AH", "АМПЕР ЧАС", "АМПЕР ЧАС", "AMPERE HOUR")
            uu1.base_unit = u1
            uu1.mult_unit = UnitsHelper.UHOUR
        u = Unit("Б", "B", "белл", "bell")
        u.keywords.extend(["ЗВУК", "ЗВУКОВОЙ", "ШУМ", "ШУМОВОЙ", "ГРОМКОСТЬ", "ГРОМКИЙ", "СИГНАЛ", "УСИЛЕНИЕ", "ЗАТУХАНИЕ", "ГАРМОНИЧЕСКИЙ", "ПОДАВЛЕНИЕ", "ЗВУКОВИЙ", "ШУМОВИЙ", "ГУЧНІСТЬ", "ГУЧНИЙ", "ПОСИЛЕННЯ", "ЗАГАСАННЯ", "ГАРМОНІЙНИЙ", "ПРИДУШЕННЯ", "SOUND", "NOISE", "VOLUME", "LOUD", "SIGNAL", "STRENGTHENING", "ATTENUATION", "HARMONIC", "SUPPRESSION"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БЕЛЛ", u)
        t.add_abridge("Б.")
        t.add_abridge("B.")
        t.add_abridge("В.")
        t.add_variant("БЕЛ", False)
        t.add_variant("BELL", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.__add_factor(UnitsFactors.DECI, u, "Б", "B", "БЕЛЛ;БЕЛ", "БЕЛЛ;БЕЛ", "BELL")
        u = Unit("дБи", "dBi", "коэффициент усиления антенны", "dBi")
        u.keywords.extend(["УСИЛЕНИЕ", "АНТЕННА", "АНТЕНА", "ПОСИЛЕННЯ", "GAIN", "ANTENNA"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("DBI", u)
        t.add_variant("ДБИ", False)
        t.add_variant("ДВМ", False)
        t.add_variant("DBM", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Ф", "F", "фарад", "farad")
        u.keywords.extend(["ЕМКОСТЬ", "ЭЛЕКТРИЧНСКИЙ", "КОНДЕНСАТОР"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ФАРАД", u)
        t.add_abridge("Ф.")
        t.add_abridge("ФА")
        t.add_abridge("F")
        t.add_variant("FARAD", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO, UnitsFactors.PICO]: 
            UnitsHelper.__add_factor(f, u, "Ф.;ФА.", "F", "ФАРАД", "ФАРАД", "FARAD")
        u = Unit("Н", "N", "ньютон", "newton")
        u.keywords.extend(["СИЛА", "МОМЕНТ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("НЬЮТОН", u)
        t.add_abridge("Н.")
        t.add_abridge("H.")
        t.add_abridge("N.")
        t.add_variant("NEWTON", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "Н.", "N.", "НЬЮТОН", "НЬЮТОН", "NEWTON")
        u = Unit("моль", "mol", "моль", "mol")
        u.keywords.extend(["МОЛЕКУЛА", "МОЛЕКУЛЯРНЫЙ", "КОЛИЧЕСТВО", "ВЕЩЕСТВО"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("МОЛЬ", u)
        t.add_abridge("МЛЬ")
        t.add_variant("MOL", False)
        t.add_variant("ГРАММ МОЛЕКУЛА", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "МЛЬ", "MOL", "МОЛЬ", "МОЛЬ", "MOL")
        u = Unit("Бк", "Bq", "беккерель", "becquerel")
        u.keywords.extend(["АКТИВНОСТЬ", "РАДИОАКТИВНЫЙ", "ИЗЛУЧЕНИЕ", "ИСТОЧНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БЕККЕРЕЛЬ", u)
        t.add_abridge("БК.")
        t.add_variant("BQ.", False)
        t.add_variant("БЕК", False)
        t.add_variant("БЕКЕРЕЛЬ", False)
        t.add_variant("BECQUEREL", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "БК.", "BQ.", "БЕККЕРЕЛЬ;БЕК", "БЕКЕРЕЛЬ", "BECQUEREL")
        u = Unit("См", "S", "сименс", "siemens")
        u.keywords.extend(["ПРОВОДИМОСТЬ", "ЭЛЕКТРИЧЕСКИЙ", "ПРОВОДНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("СИМЕНС", u)
        t.add_abridge("СМ.")
        t.add_abridge("CM.")
        t.add_variant("S.", False)
        t.add_variant("SIEMENS", False)
        t.add_variant("СІМЕНС", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "СМ.", "S.", "СИМЕНС", "СІМЕНС", "SIEMENS")
        u = Unit("кд", "cd", "кандела", "candela")
        u.keywords.extend(["СВЕТ", "СВЕТОВОЙ", "ПОТОК", "ИСТОЧНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("КАНДЕЛА", u)
        t.add_abridge("КД.")
        t.add_variant("CD.", False)
        t.add_variant("КАНДЕЛА", False)
        t.add_variant("CANDELA", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Па", "Pa", "паскаль", "pascal")
        u.keywords.extend(["ДАВЛЕНИЕ", "НАПРЯЖЕНИЕ", "ТЯЖЕСТЬ", "PRESSURE", "STRESS", "ТИСК", "НАПРУГА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ПАСКАЛЬ", u)
        t.add_abridge("ПА")
        t.add_abridge("РА")
        t.add_variant("PA", False)
        t.add_variant("PASCAL", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ПА", "PA", "ПАСКАЛЬ", "ПАСКАЛЬ", "PASCAL")
        uu = Unit._new1533("бар", "bar", "бар", "bar", u, 100000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("БАР", uu)
        t.add_variant("BAR", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("мм.рт.ст.", "mm Hg", "миллиметр ртутного столба", "millimeter of mercury", u, 133.332)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МИЛЛИМЕТР РТУТНОГО СТОЛБА", uu)
        t.add_abridge("ММ.РТ.СТ.")
        t.add_abridge("MM.PT.CT")
        t.add_abridge("MM HG")
        t.add_variant("MMGH", False)
        t.add_variant("ТОРР", False)
        t.add_variant("TORR", False)
        t.add_variant("MILLIMETER OF MERCURY", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("бит", "bit", "бит", "bit")
        u.keywords.extend(["СКОРОСТЬ", "ОБЪЕМ", "РАЗМЕР", "ПАМЯТЬ", "ПЕРЕДАЧА", "ПРИЕМ", "ОТПРАВКА", "ОП", "ДИСК", "ШВИДКІСТЬ", "ОБСЯГ", "РОЗМІР", "ВІДПРАВЛЕННЯ", "SPEED", "VOLUME", "SIZE", "MEMORY", "TRANSFER", "SEND", "RECEPTION", "RAM", "DISK"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БИТ", u)
        t.add_variant("BIT", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__add_factor(f, u, "БИТ", "BIT", "БИТ", "БИТ", "BIT")
        uu = Unit("б", "b", "байт", "byte")
        uu.keywords = u.keywords
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("БАЙТ", uu)
        t.add_variant("BYTE", False)
        t.add_abridge("B.")
        t.add_abridge("Б.")
        t.add_abridge("В.")
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__add_factor(f, uu, "Б.", "B.", "БАЙТ", "БАЙТ", "BYTE")
        u = Unit("бод", "Bd", "бод", "baud")
        u.keywords.extend(["СКОРОСТЬ", "ПЕРЕДАЧА", "ПРИЕМ", "ДАННЫЕ", "ОТПРАВКА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БОД", u)
        t.add_abridge("BD")
        t.add_variant("BAUD", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__add_factor(f, uu, "БОД", "BD.", "БОД", "БОД", "BAUD")
        u = Unit("гс", "gf", "грамм-сила", "gram-force")
        u.keywords.extend(["СИЛА", "ДАВЛЕНИЕ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ГРАММ СИЛА", u)
        t.add_abridge("ГС")
        t.add_variant("POND", False)
        t.add_variant("ГРАМ СИЛА", False)
        t.add_abridge("GP.")
        t.add_variant("GRAM POND", False)
        t.add_variant("GRAM FORCE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1533("кгс", "kgf", "килограмм-сила", "kilogram-force", u, 1000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("КИЛОГРАММ СИЛА", uu)
        t.add_abridge("КГС")
        t.add_variant("KILOPOND", False)
        t.add_variant("КІЛОГРАМ СИЛА", False)
        t.add_abridge("KP.")
        t.add_variant("KILOGRAM POND", False)
        UnitsHelper.TERMINS.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    @staticmethod
    def __add_factor(f : 'UnitsFactors', u0 : 'Unit', abbr_cyr : str, abbr_lat : str, names_ru : str, names_ua : str, names_en : str) -> 'Unit':
        from pullenti.ner.core.Termin import Termin
        pref_cyr = None
        pref_lat = None
        pref_ru = None
        pref_ua = None
        pref_en = None
        mult = 1
        swichVal = f
        if (swichVal == UnitsFactors.CENTI): 
            pref_cyr = "С"
            pref_lat = "C"
            pref_ru = "САНТИ"
            pref_ua = "САНТИ"
            pref_en = "CENTI"
            mult = 0.1
        elif (swichVal == UnitsFactors.DECI): 
            pref_cyr = "Д"
            pref_lat = "D"
            pref_ru = "ДЕЦИ"
            pref_ua = "ДЕЦИ"
            pref_en = "DECI"
            mult = 0.01
        elif (swichVal == UnitsFactors.GIGA): 
            pref_cyr = "Г"
            pref_lat = "G"
            pref_ru = "ГИГА"
            pref_ua = "ГІГА"
            pref_en = "GIGA"
            mult = 1000000000
        elif (swichVal == UnitsFactors.KILO): 
            pref_cyr = "К"
            pref_lat = "K"
            pref_ru = "КИЛО"
            pref_ua = "КІЛО"
            pref_en = "KILO"
            mult = 1000
        elif (swichVal == UnitsFactors.MEGA): 
            pref_cyr = "М"
            pref_lat = "M"
            pref_ru = "МЕГА"
            pref_ua = "МЕГА"
            pref_en = "MEGA"
            mult = 1000000
        elif (swichVal == UnitsFactors.MICRO): 
            pref_cyr = "МК"
            pref_lat = "MK"
            pref_ru = "МИКРО"
            pref_ua = "МІКРО"
            pref_en = "MICRO"
            mult = 0.0001
        elif (swichVal == UnitsFactors.MILLI): 
            pref_cyr = "М"
            pref_lat = "M"
            pref_ru = "МИЛЛИ"
            pref_ua = "МІЛІ"
            pref_en = "MILLI"
            mult = 0.001
        elif (swichVal == UnitsFactors.NANO): 
            pref_cyr = "Н"
            pref_lat = "N"
            pref_ru = "НАНО"
            pref_ua = "НАНО"
            pref_en = "NANO"
            mult = 0.0000000001
        elif (swichVal == UnitsFactors.PICO): 
            pref_cyr = "П"
            pref_lat = "P"
            pref_ru = "ПИКО"
            pref_ua = "ПІКО"
            pref_en = "PICO"
            mult = 0.0000000000001
        elif (swichVal == UnitsFactors.TERA): 
            pref_cyr = "Т"
            pref_lat = "T"
            pref_ru = "ТЕРА"
            pref_ua = "ТЕРА"
            pref_en = "TERA"
            mult = 1000000000000
        u = Unit._new1593(pref_cyr.lower() + u0.name_cyr, pref_lat.lower() + u0.name_lat, pref_ru.lower() + u0.fullname_cyr, pref_en.lower() + u0.fullname_lat, f, mult, u0)
        if (f == UnitsFactors.MEGA or f == UnitsFactors.TERA or f == UnitsFactors.GIGA): 
            u.name_cyr = (pref_cyr + u0.name_cyr)
            u.name_lat = (pref_lat + u0.name_lat)
        UnitsHelper.UNITS.append(u)
        nams = Utils.splitString(names_ru, ';', False)
        t = Termin._new118(pref_ru + nams[0], u)
        i = 1
        while i < len(nams): 
            t.add_variant(pref_ru + nams[i], False)
            i += 1
        for n in nams: 
            t.add_variant(pref_cyr + n, False)
        for n in Utils.splitString(names_ua, ';', False): 
            t.add_variant(pref_ua + n, False)
            t.add_variant(pref_cyr + n, False)
        for n in Utils.splitString(names_en, ';', False): 
            t.add_variant(pref_en + n, False)
            t.add_variant(pref_lat + n, False)
        for n in Utils.splitString(abbr_cyr, ';', False): 
            t.add_abridge(pref_cyr + n)
        for n in Utils.splitString(abbr_lat, ';', False): 
            t.add_abridge(pref_lat + n)
        UnitsHelper.TERMINS.add(t)
        return u
    
    # static constructor for class UnitsHelper
    @staticmethod
    def _static_ctor():
        from pullenti.ner.core.TerminCollection import TerminCollection
        UnitsHelper.UNITS = list()
        UnitsHelper.TERMINS = TerminCollection()

UnitsHelper._static_ctor()