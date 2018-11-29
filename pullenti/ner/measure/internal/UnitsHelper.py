# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.measure.MeasureKind import MeasureKind


class UnitsHelper:
    
    UNITS = None
    
    TERMINS = None
    
    UGRADUS = None
    
    UGRADUSC = None
    
    UGRADUSF = None
    
    UPERCENT = None
    
    UALCO = None
    
    UOM = None
    
    UHOUR = None
    
    USEC = None
    
    __m_inited = False
    
    @staticmethod
    def findUnit(v : str, fact : 'UnitsFactors') -> 'Unit':
        if (fact != UnitsFactors.NO): 
            for u in UnitsHelper.UNITS: 
                if (u.base_unit is not None and u.factor == fact): 
                    if ((u.base_unit.fullname_cyr == v or u.base_unit.fullname_lat == v or u.base_unit.name_cyr == v) or u.base_unit.name_lat == v): 
                        return u
        for u in UnitsHelper.UNITS: 
            if ((u.fullname_cyr == v or u.fullname_lat == v or u.name_cyr == v) or u.name_lat == v): 
                return u
        return None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        if (UnitsHelper.__m_inited): 
            return
        UnitsHelper.__m_inited = True
        UnitsHelper.UNITS = list()
        UnitsHelper.TERMINS = TerminCollection()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        u = Unit._new1550("м", "m", "метр", "meter", MeasureKind.LENGTH)
        u.keywords.extend(["ДЛИНА", "ДЛИННА", "ШИРИНА", "ГЛУБИНА", "ВЫСОТА", "РАЗМЕР", "ГАБАРИТ", "РАССТОЯНИЕ", "РАДИУС", "ПЕРИМЕТР", "ДИАМЕТР", "ТОЛЩИНА", "ПОДАЧА", "НАПОР", "ДАЛЬНОСТЬ", "ТИПОРАЗМЕР", "LENGTH", "WIDTH", "DEPTH", "HEIGHT", "SIZE", "ENVELOPE", "DISTANCE", "RADIUS", "PERIMETER", "DIAMETER", "FLOW", "PRESSURE", "ДОВЖИНА", "ШИРИНА", "ГЛИБИНА", "ВИСОТА", "РОЗМІР", "ГАБАРИТ", "ВІДСТАНЬ", "РАДІУС", "ДІАМЕТР", "НАТИСК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("МЕТР", u)
        t.addVariant("МЕТРОВЫЙ", False)
        t.addVariant("МЕТРОВИЙ", False)
        t.addVariant("METER", False)
        t.addAbridge("М.")
        t.addAbridge("M.")
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.DECI, UnitsFactors.CENTI, UnitsFactors.MILLI, UnitsFactors.MICRO, UnitsFactors.NANO]: 
            UnitsHelper.__addFactor(f, u, "М.", "M.", "МЕТР;МЕТРОВЫЙ", "МЕТР;МЕТРОВИЙ", "METER;METRE")
        uu = Unit._new1550("миль", "mile", "морская миля", "mile", MeasureKind.LENGTH)
        uu.base_unit = u
        uu.base_multiplier = (1852)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МИЛЯ", uu)
        t.addVariant("МОРСКАЯ МИЛЯ", False)
        t.addAbridge("NMI")
        t.addVariant("MILE", False)
        t.addVariant("NAUTICAL MILE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("фут", "ft", "фут", "foot", u, .304799472, MeasureKind.LENGTH)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ФУТ", uu)
        t.addAbridge("FT.")
        t.addVariant("FOOT", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("дюйм", "in", "дюйм", "inch", u, .0254, MeasureKind.LENGTH)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ДЮЙМ", uu)
        t.addAbridge("IN")
        t.addVariant("INCH", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1550("ар", "are", "ар", "are", MeasureKind.AREA)
        u.keywords.extend(["ПЛОЩАДЬ", "ПРОЩИНА", "AREA", "SQWARE", "SPACE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("АР", u)
        t.addVariant("ARE", False)
        t.addVariant("СОТКА", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1550("га", "ga", "гектар", "hectare", MeasureKind.AREA)
        uu.base_unit = u
        uu.base_multiplier = (100)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ГЕКТАР", uu)
        t.addVariant("HECTARE", False)
        t.addAbridge("ГА")
        t.addAbridge("GA")
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1550("г", "g", "грамм", "gram", MeasureKind.WEIGHT)
        u.keywords.extend(["ВЕС", "ТЯЖЕСТЬ", "НЕТТО", "БРУТТО", "МАССА", "НАГРУЗКА", "ЗАГРУЗКА", "WEIGHT", "NET", "GROSS", "MASS", "ВАГА", "ТЯЖКІСТЬ", "МАСА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ГРАММ", u)
        t.addAbridge("Г.")
        t.addAbridge("ГР.")
        t.addAbridge("G.")
        t.addAbridge("GR.")
        t.addVariant("ГРАММОВЫЙ", False)
        t.addVariant("ГРАММНЫЙ", False)
        t.addVariant("ГРАМОВИЙ", False)
        t.addVariant("GRAM", False)
        t.addVariant("GRAMME", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "Г.;ГР;", "G.;GR.", "ГРАМ;ГРАММ;ГРАММНЫЙ", "ГРАМ;ГРАМОВИЙ", "GRAM;GRAMME")
        uu = Unit._new1564("ц", "centner", "центнер", "centner", u, 100000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ЦЕНТНЕР", uu)
        t.addVariant("CENTNER", False)
        t.addVariant("QUINTAL", False)
        t.addAbridge("Ц.")
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("т", "t", "тонна", "tonne", u, 1000000, MeasureKind.WEIGHT)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ТОННА", uu)
        t.addVariant("TONNE", False)
        t.addVariant("TON", False)
        t.addAbridge("Т.")
        t.addAbridge("T.")
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.__addFactor(UnitsFactors.MEGA, uu, "Т", "T", "ТОННА;ТОННЫЙ", "ТОННА;ТОННИЙ", "TONNE;TON")
        u = Unit._new1550("л", "l", "литр", "liter", MeasureKind.VOLUME)
        u.keywords.extend(["ОБЪЕМ", "ЕМКОСТЬ", "ВМЕСТИМОСЬ", "ОБСЯГ", "ЄМНІСТЬ", "МІСТКІСТЬ", "VOLUME", "CAPACITY"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ЛИТР", u)
        t.addAbridge("Л.")
        t.addAbridge("L.")
        t.addVariant("LITER", False)
        t.addVariant("LITRE", False)
        t.addVariant("ЛІТР", False)
        t.addVariant("ЛІТРОВИЙ", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MILLI, UnitsFactors.CENTI]: 
            UnitsHelper.__addFactor(f, u, "Л.", "L.", "ЛИТР;ЛИТРОВЫЙ", "ЛІТР;ЛІТРОВИЙ", "LITER;LITRE")
        uu = Unit._new1554("галлон", "gallon", "галлон", "gallon", u, 4.5461, MeasureKind.VOLUME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ГАЛЛОН", u)
        t.addVariant("ГАЛОН", False)
        t.addVariant("GALLON", False)
        t.addAbridge("ГАЛ")
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("баррель", "bbls", "баррель нефти", "barrel", u, 158.987, MeasureKind.VOLUME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("БАРРЕЛЬ", uu)
        t.addAbridge("BBLS")
        t.addVariant("БАРРЕЛЬ НЕФТИ", False)
        t.addVariant("BARRREL", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1550("сек", "sec", "секунда", "second", MeasureKind.TIME)
        UnitsHelper.USEC = u
        u.keywords.extend(["ВРЕМЯ", "ПРОДОЛЖИТЕЛЬНОСТЬ", "ЗАДЕРЖКА", "ДЛИТЕЛЬНОСТЬ", "ДОЛГОТА", "TIME", "DURATION", "DELAY", "ЧАС", "ТРИВАЛІСТЬ", "ЗАТРИМКА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("СЕКУНДА", u)
        t.addAbridge("С.")
        t.addAbridge("C.")
        t.addAbridge("СЕК")
        t.addAbridge("СЕК")
        t.addAbridge("S.")
        t.addAbridge("SEC")
        t.addVariant("СЕКУНДНЫЙ", False)
        t.addVariant("СЕКУНДНИЙ", False)
        t.addVariant("SECOND", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MILLI, UnitsFactors.MICRO]: 
            UnitsHelper.__addFactor(f, u, "С.;СЕК", "C;S.;SEC;", "СЕКУНДА;СЕКУНДНЫЙ", "СЕКУНДА;СЕКУНДНИЙ", "SECOND")
        uu = Unit._new1550("мин", "min", "минута", "minute", MeasureKind.TIME)
        uu.base_unit = u
        uu.base_multiplier = (60)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МИНУТА", uu)
        t.addAbridge("МИН.")
        t.addAbridge("MIN.")
        t.addVariant("МИНУТНЫЙ", False)
        t.addVariant("ХВИЛИННИЙ", False)
        t.addVariant("ХВИЛИНА", False)
        t.addVariant("МІНУТА", False)
        t.addVariant("MINUTE", False)
        UnitsHelper.TERMINS.add(t)
        u = uu
        uu = Unit._new1554("ч", "h", "час", "hour", u, 60, MeasureKind.TIME)
        UnitsHelper.UHOUR = uu
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ЧАС", uu)
        t.addAbridge("Ч.")
        t.addAbridge("H.")
        t.addVariant("ЧАСОВОЙ", False)
        t.addVariant("HOUR", False)
        t.addVariant("ГОДИННИЙ", False)
        t.addVariant("ГОДИНА", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1550("дн", "d", "день", "day", MeasureKind.TIME)
        u.keywords.extend(UnitsHelper.USEC.keywords)
        u.keywords.extend(["ПОСТАВКА", "СРОК", "РАБОТА", "ЗАВЕРШЕНИЕ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ДЕНЬ", u)
        t.addAbridge("ДН.")
        t.addAbridge("Д.")
        t.addVariant("DAY", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("нед", "week", "неделя", "week", u, 7, MeasureKind.TIME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("НЕДЕЛЯ", uu)
        t.addAbridge("НЕД")
        t.addVariant("WEEK", False)
        t.addVariant("ТИЖДЕНЬ", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("мес", "mon", "месяц", "month", u, 30, MeasureKind.TIME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МЕСЯЦ", uu)
        t.addAbridge("МЕС")
        t.addAbridge("MON")
        t.addVariant("MONTH", False)
        t.addVariant("МІСЯЦЬ", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1554("г", "year", "год", "year", u, 365, MeasureKind.TIME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ГОД", uu)
        t.addAbridge("Г.")
        t.addAbridge("ГД")
        t.addVariant("YEAR", False)
        t.addVariant("РІК", False)
        t.addVariant("ЛЕТ", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUS = Unit("°", "°", "градус", "degree")
        UnitsHelper.UGRADUS.keywords.extend(["ТЕМПЕРАТУРА", "ШИРОТА", "ДОЛГОТА", "АЗИМУТ", "ДОВГОТА", "TEMPERATURE", "LATITUDE", "LONGITUDE", "AZIMUTH"])
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUS)
        t = Termin._new118("ГРАДУС", UnitsHelper.UGRADUS)
        t.addVariant("DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUSC = Unit("°C", "°C", "градус Цельсия", "celsius degree")
        UnitsHelper.UGRADUSC.keywords.append("ТЕМПЕРАТУРА")
        UnitsHelper.UGRADUS.keywords.append("TEMPERATURE")
        UnitsHelper.UGRADUS.psevdo.append(UnitsHelper.UGRADUSC)
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUSC)
        t = Termin._new118("ГРАДУС ЦЕЛЬСИЯ", UnitsHelper.UGRADUSC)
        t.addVariant("ГРАДУС ПО ЦЕЛЬСИЮ", False)
        t.addVariant("CELSIUS DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUSF = Unit("°F", "°F", "градус Фаренгейта", "Fahrenheit degree")
        UnitsHelper.UGRADUSF.keywords = UnitsHelper.UGRADUSC.keywords
        UnitsHelper.UGRADUS.psevdo.append(UnitsHelper.UGRADUSF)
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUSF)
        t = Termin._new118("ГРАДУС ФАРЕНГЕЙТА", UnitsHelper.UGRADUSF)
        t.addVariant("ГРАДУС ПО ФАРЕНГЕЙТУ", False)
        t.addVariant("FAHRENHEIT DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UPERCENT = Unit("%", "%", "процент", "percent")
        UnitsHelper.UNITS.append(UnitsHelper.UPERCENT)
        t = Termin._new118("ПРОЦЕНТ", UnitsHelper.UPERCENT)
        t.addVariant("ПРОЦ", False)
        t.addVariant("PERC", False)
        t.addVariant("PERCENT", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UALCO = Unit("%(об)", "%(vol)", "объёмный процент", "volume percent")
        UnitsHelper.UALCO.keywords.extend(["КРЕПОСТЬ", "АЛКОГОЛЬ", "ALCOHOL", "СПИРТ", "АЛКОГОЛЬНЫЙ", "SPIRIT"])
        UnitsHelper.UPERCENT.psevdo.append(UnitsHelper.UALCO)
        UnitsHelper.UGRADUS.psevdo.append(UnitsHelper.UALCO)
        UnitsHelper.UNITS.append(UnitsHelper.UALCO)
        t = Termin._new118("ОБЪЕМНЫЙ ПРОЦЕНТ", UnitsHelper.UALCO)
        t.addVariant("ГРАДУС", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("об", "rev", "оборот", "revolution")
        UnitsHelper.UGRADUS.keywords.extend(["ЧАСТОТА", "ВРАЩЕНИЕ", "ВРАЩАТЕЛЬНЫЙ", "СКОРОСТЬ", "ОБОРОТ", "FREQUENCY", "ROTATION", "ROTATIONAL", "SPEED", "ОБЕРТАННЯ", "ОБЕРТАЛЬНИЙ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ОБОРОТ", u)
        t.addAbridge("ОБ.")
        t.addAbridge("ROT.")
        t.addAbridge("REV.")
        t.addVariant("ROTATION", False)
        t.addVariant("REVOLUTION", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("В", "V", "вольт", "volt")
        u.keywords.extend(["ЭЛЕКТРИЧЕСКИЙ", "ПОТЕНЦИАЛ", "НАПРЯЖЕНИЕ", "ЭЛЕКТРОДВИЖУЩИЙ", "ПИТАНИЕ", "ТОК", "ПОСТОЯННЫЙ", "ПЕРЕМЕННЫЙ", "ЕЛЕКТРИЧНИЙ", "ПОТЕНЦІАЛ", "НАПРУГА", "ЕЛЕКТРОРУШІЙНОЇ", "ХАРЧУВАННЯ", "СТРУМ", "ПОСТІЙНИЙ", "ЗМІННИЙ", "ELECTRIC", "POTENTIAL", "TENSION", "ELECTROMOTIVE", "FOOD", "CURRENT", "CONSTANT", "VARIABLE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ВОЛЬТ", u)
        t.addVariant("VOLT", False)
        t.addAbridge("V")
        t.addAbridge("В.")
        t.addAbridge("B.")
        t.addVariant("VAC", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.MILLI, UnitsFactors.MILLI, UnitsFactors.MICRO]: 
            UnitsHelper.__addFactor(f, u, "В.", "V.", "ВОЛЬТ;ВОЛЬТНЫЙ", "ВОЛЬТ;ВОЛЬТНІ", "VOLT")
        u = Unit("Вт", "W", "ватт", "watt")
        u.keywords.extend(["МОЩНОСТЬ", "ЭНЕРГИЯ", "ПОТОК", "ИЗЛУЧЕНИЕ", "ЭНЕРГОПОТРЕБЛЕНИЕ", "ПОТУЖНІСТЬ", "ЕНЕРГІЯ", "ПОТІК", "ВИПРОМІНЮВАННЯ", "POWER", "ENERGY", "FLOW", "RADIATION"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ВАТТ", u)
        t.addAbridge("Вт")
        t.addAbridge("W")
        t.addVariant("WATT", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "ВТ.", "W.", "ВАТТ;ВАТТНЫЙ", "ВАТ;ВАТНИЙ", "WATT;WATTS")
        uu = Unit._new1564("л.с.", "hp", "лошадиная сила", "horsepower", u, 735.49875)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ЛОШАДИНАЯ СИЛА", uu)
        t.addAbridge("Л.С.")
        t.addAbridge("ЛОШ.С.")
        t.addAbridge("ЛОШ.СИЛА")
        t.addAbridge("HP")
        t.addAbridge("PS")
        t.addAbridge("SV")
        t.addVariant("HORSEPOWER", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Дж", "J", "джоуль", "joule")
        u.keywords.extend(["РАБОТА", "ЭНЕРГИЯ", "ТЕПЛОТА", "ТЕПЛОВОЙ", "ТЕПЛОВЫДЕЛЕНИЕ", "МОЩНОСТЬ", "ХОЛОДИЛЬНЫЙ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ДЖОУЛЬ", u)
        t.addAbridge("ДЖ")
        t.addAbridge("J")
        t.addVariant("JOULE", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "ДЖ.", "J.", "ДЖОУЛЬ", "ДЖОУЛЬ", "JOULE")
        uu = Unit("БТЕ", "BTU", "британская терминальная единица", "british terminal unit")
        uu.keywords = u.keywords
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("БРИТАНСКАЯ ТЕРМИНАЛЬНАЯ ЕДИНИЦА", uu)
        t.addAbridge("БТЕ")
        t.addAbridge("BTU")
        t.addVariant("BRITISH TERMINAL UNIT", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("К", "K", "кельвин", "kelvin")
        u.keywords.extend(UnitsHelper.UGRADUSC.keywords)
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("КЕЛЬВИН", u)
        t.addAbridge("К.")
        t.addAbridge("K.")
        t.addVariant("KELVIN", False)
        t.addVariant("КЕЛЬВІН", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "К.", "K.", "КЕЛЬВИН", "КЕЛЬВІН", "KELVIN")
        u = Unit("Гц", "Hz", "герц", "herz")
        u.keywords.extend(["ЧАСТОТА", "ЧАСТОТНЫЙ", "ПЕРИОДИЧНОСТЬ", "ПИТАНИЕ", "ЧАСТОТНИЙ", "ПЕРІОДИЧНІСТЬ", "FREQUENCY"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ГЕРЦ", u)
        t.addAbridge("HZ")
        t.addAbridge("ГЦ")
        t.addVariant("ГЕРЦОВЫЙ", False)
        t.addVariant("ГЕРЦОВИЙ", False)
        t.addVariant("HERZ", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO]: 
            UnitsHelper.__addFactor(f, u, "ГЦ.", "W.", "ГЕРЦ;ГЕРЦОВЫЙ", "ГЕРЦ;ГЕРЦОВИЙ", "HERZ")
        u = Unit("Ом", "Ω", "Ом", "Ohm")
        UnitsHelper.UOM = u
        u.keywords.extend(["СОПРОТИВЛЕНИЕ", "РЕЗИСТОР", "РЕЗИСТНЫЙ", "ИМПЕДАНС", "РЕЗИСТОРНЫЙ", "ОПІР", "РЕЗИСТИВНИЙ", "ІМПЕДАНС", "RESISTANCE", "RESISTOR", "RESISTIVE", "IMPEDANCE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ОМ", UnitsHelper.UOM)
        t.addVariant("OHM", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "ОМ", "Ω", "ОМ", "ОМ", "OHM")
        u = Unit("А", "A", "ампер", "ampere")
        u.keywords.extend(["ТОК", "СИЛА", "ЭЛЕКТРИЧЕСКИЙ", "ЭЛЕКТРИЧЕСТВО", "МАГНИТ", "МАГНИТОДВИЖУЩИЙ", "ПОТРЕБЛЕНИЕ", "CURRENT", "POWER", "ELECTRICAL", "ELECTRICITY", "MAGNET", "MAGNETOMOTIVE", "CONSUMPTION", "СТРУМ", "ЕЛЕКТРИЧНИЙ", "ЕЛЕКТРИКА", "МАГНІТ", "МАГНИТОДВИЖУЩИЙ", "СПОЖИВАННЯ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("АМПЕР", u)
        t.addAbridge("A")
        t.addAbridge("А")
        t.addVariant("АМПЕРНЫЙ", False)
        t.addVariant("AMP", False)
        t.addVariant("AMPERE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1604("Ач", "Ah", "ампер-час", "ampere-hour", u, UnitsHelper.UHOUR)
        uu.keywords.extend(["ЗАРЯД", "АККУМУЛЯТОР", "АККУМУЛЯТОРНЫЙ", "ЗАРЯДКА", "БАТАРЕЯ", "CHARGE", "BATTERY", "CHARGING", "АКУМУЛЯТОР", "АКУМУЛЯТОРНИЙ"])
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("АМПЕР ЧАС", uu)
        t.addAbridge("АЧ")
        t.addAbridge("AH")
        t.addVariant("AMPERE HOUR", False)
        t.addVariant("АМПЕРЧАС", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            u1 = UnitsHelper.__addFactor(f, u, "А", "A", "АМПЕР;АМПЕРНЫЙ", "АМПЕР;АМПЕРНИЙ", "AMPERE;AMP")
            uu1 = UnitsHelper.__addFactor(f, uu, "АЧ", "AH", "АМПЕР ЧАС", "АМПЕР ЧАС", "AMPERE HOUR")
            uu1.base_unit = u1
            uu1.mult_unit = UnitsHelper.UHOUR
        uu = Unit("ВА", "VA", "вольт-ампер", "volt-ampere")
        uu.mult_unit = u
        uu.base_unit = UnitsHelper.findUnit("V", UnitsFactors.NO)
        uu.keywords.extend(["ТОК", "СИЛА", "МОЩНОСТЬ", "ЭЛЕКТРИЧЕСКИЙ", "ПЕРЕМЕННЫЙ"])
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("ВОЛЬТ-АМПЕР", uu)
        t.addAbridge("BA")
        t.addAbridge("BA")
        t.addVariant("VA", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            u1 = UnitsHelper.__addFactor(f, uu, "ВА;BA", "VA", "ВОЛЬТ-АМПЕР", "ВОЛЬТ-АМПЕР", "VOLT-AMPERE")
        u = Unit("Б", "B", "белл", "bell")
        u.keywords.extend(["ЗВУК", "ЗВУКОВОЙ", "ШУМ", "ШУМОВОЙ", "ГРОМКОСТЬ", "ГРОМКИЙ", "СИГНАЛ", "УСИЛЕНИЕ", "ЗАТУХАНИЕ", "ГАРМОНИЧЕСКИЙ", "ПОДАВЛЕНИЕ", "ЗВУКОВИЙ", "ШУМОВИЙ", "ГУЧНІСТЬ", "ГУЧНИЙ", "ПОСИЛЕННЯ", "ЗАГАСАННЯ", "ГАРМОНІЙНИЙ", "ПРИДУШЕННЯ", "SOUND", "NOISE", "VOLUME", "LOUD", "SIGNAL", "STRENGTHENING", "ATTENUATION", "HARMONIC", "SUPPRESSION"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БЕЛЛ", u)
        t.addAbridge("Б.")
        t.addAbridge("B.")
        t.addAbridge("В.")
        t.addVariant("БЕЛ", False)
        t.addVariant("BELL", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.__addFactor(UnitsFactors.DECI, u, "Б", "B", "БЕЛЛ;БЕЛ", "БЕЛЛ;БЕЛ", "BELL")
        u = Unit("дБи", "dBi", "коэффициент усиления антенны", "dBi")
        u.keywords.extend(["УСИЛЕНИЕ", "АНТЕННА", "АНТЕНА", "ПОСИЛЕННЯ", "GAIN", "ANTENNA"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("DBI", u)
        t.addVariant("ДБИ", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("дБм", "dBm", "опорная мощность", "dBm")
        u.keywords.extend(["МОЩНОСТЬ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("DBM", u)
        t.addVariant("ДБМ", False)
        t.addVariant("ДВМ", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Ф", "F", "фарад", "farad")
        u.keywords.extend(["ЕМКОСТЬ", "ЭЛЕКТРИЧНСКИЙ", "КОНДЕНСАТОР"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ФАРАД", u)
        t.addAbridge("Ф.")
        t.addAbridge("ФА")
        t.addAbridge("F")
        t.addVariant("FARAD", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO, UnitsFactors.PICO]: 
            UnitsHelper.__addFactor(f, u, "Ф.;ФА.", "F", "ФАРАД", "ФАРАД", "FARAD")
        u = Unit("Н", "N", "ньютон", "newton")
        u.keywords.extend(["СИЛА", "МОМЕНТ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("НЬЮТОН", u)
        t.addAbridge("Н.")
        t.addAbridge("H.")
        t.addAbridge("N.")
        t.addVariant("NEWTON", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "Н.", "N.", "НЬЮТОН", "НЬЮТОН", "NEWTON")
        u = Unit("моль", "mol", "моль", "mol")
        u.keywords.extend(["МОЛЕКУЛА", "МОЛЕКУЛЯРНЫЙ", "КОЛИЧЕСТВО", "ВЕЩЕСТВО"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("МОЛЬ", u)
        t.addAbridge("МЛЬ")
        t.addVariant("MOL", False)
        t.addVariant("ГРАММ МОЛЕКУЛА", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__addFactor(f, u, "МЛЬ", "MOL", "МОЛЬ", "МОЛЬ", "MOL")
        u = Unit("Бк", "Bq", "беккерель", "becquerel")
        u.keywords.extend(["АКТИВНОСТЬ", "РАДИОАКТИВНЫЙ", "ИЗЛУЧЕНИЕ", "ИСТОЧНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БЕККЕРЕЛЬ", u)
        t.addAbridge("БК.")
        t.addVariant("BQ.", False)
        t.addVariant("БЕК", False)
        t.addVariant("БЕКЕРЕЛЬ", False)
        t.addVariant("BECQUEREL", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__addFactor(f, u, "БК.", "BQ.", "БЕККЕРЕЛЬ;БЕК", "БЕКЕРЕЛЬ", "BECQUEREL")
        u = Unit("См", "S", "сименс", "siemens")
        u.keywords.extend(["ПРОВОДИМОСТЬ", "ЭЛЕКТРИЧЕСКИЙ", "ПРОВОДНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("СИМЕНС", u)
        t.addAbridge("СМ.")
        t.addAbridge("CM.")
        t.addVariant("S.", False)
        t.addVariant("SIEMENS", False)
        t.addVariant("СІМЕНС", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__addFactor(f, u, "СМ.", "S.", "СИМЕНС", "СІМЕНС", "SIEMENS")
        u = Unit("кд", "cd", "кандела", "candela")
        u.keywords.extend(["СВЕТ", "СВЕТОВОЙ", "ПОТОК", "ИСТОЧНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("КАНДЕЛА", u)
        t.addAbridge("КД.")
        t.addVariant("CD.", False)
        t.addVariant("КАНДЕЛА", False)
        t.addVariant("CANDELA", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Па", "Pa", "паскаль", "pascal")
        u.keywords.extend(["ДАВЛЕНИЕ", "НАПРЯЖЕНИЕ", "ТЯЖЕСТЬ", "PRESSURE", "STRESS", "ТИСК", "НАПРУГА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ПАСКАЛЬ", u)
        t.addAbridge("ПА")
        t.addAbridge("РА")
        t.addVariant("PA", False)
        t.addVariant("PASCAL", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__addFactor(f, u, "ПА", "PA", "ПАСКАЛЬ", "ПАСКАЛЬ", "PASCAL")
        uu = Unit._new1564("бар", "bar", "бар", "bar", u, 100000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("БАР", uu)
        t.addVariant("BAR", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1564("мм.рт.ст.", "mm Hg", "миллиметр ртутного столба", "millimeter of mercury", u, 133.332)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("МИЛЛИМЕТР РТУТНОГО СТОЛБА", uu)
        t.addAbridge("ММ.РТ.СТ.")
        t.addAbridge("MM.PT.CT")
        t.addAbridge("MM HG")
        t.addVariant("MMGH", False)
        t.addVariant("ТОРР", False)
        t.addVariant("TORR", False)
        t.addVariant("MILLIMETER OF MERCURY", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("бит", "bit", "бит", "bit")
        u.keywords.extend(["СКОРОСТЬ", "ОБЪЕМ", "РАЗМЕР", "ПАМЯТЬ", "ПЕРЕДАЧА", "ПРИЕМ", "ОТПРАВКА", "ОП", "ДИСК", "НАКОПИТЕЛЬ", "КЭШ", "ШВИДКІСТЬ", "ОБСЯГ", "РОЗМІР", "ВІДПРАВЛЕННЯ", "SPEED", "VOLUME", "SIZE", "MEMORY", "TRANSFER", "SEND", "RECEPTION", "RAM", "DISK", "HDD", "RAM", "ROM", "CD-ROM", "CASHE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БИТ", u)
        t.addVariant("BIT", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__addFactor(f, u, "БИТ", "BIT", "БИТ", "БИТ", "BIT")
        uu = Unit("б", "b", "байт", "byte")
        uu.keywords = u.keywords
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("БАЙТ", uu)
        t.addVariant("BYTE", False)
        t.addAbridge("B.")
        t.addAbridge("Б.")
        t.addAbridge("В.")
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__addFactor(f, uu, "Б.", "B.", "БАЙТ", "БАЙТ", "BYTE")
        u = Unit("бод", "Bd", "бод", "baud")
        u.keywords.extend(["СКОРОСТЬ", "ПЕРЕДАЧА", "ПРИЕМ", "ДАННЫЕ", "ОТПРАВКА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("БОД", u)
        t.addAbridge("BD")
        t.addVariant("BAUD", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__addFactor(f, uu, "БОД", "BD.", "БОД", "БОД", "BAUD")
        u = Unit("гс", "gf", "грамм-сила", "gram-force")
        u.keywords.extend(["СИЛА", "ДАВЛЕНИЕ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("ГРАММ СИЛА", u)
        t.addAbridge("ГС")
        t.addVariant("POND", False)
        t.addVariant("ГРАМ СИЛА", False)
        t.addAbridge("GP.")
        t.addVariant("GRAM POND", False)
        t.addVariant("GRAM FORCE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1564("кгс", "kgf", "килограмм-сила", "kilogram-force", u, 1000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new118("КИЛОГРАММ СИЛА", uu)
        t.addAbridge("КГС")
        t.addVariant("KILOPOND", False)
        t.addVariant("КІЛОГРАМ СИЛА", False)
        t.addAbridge("KP.")
        t.addVariant("KILOGRAM POND", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("dpi", "точек на дюйм", "dpi", "dots per inch")
        u.keywords.extend(["РАЗРЕШЕНИЕ", "ЭКРАН", "МОНИТОР"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new118("DOTS PER INCH", u)
        t.addVariant("DPI", False)
        UnitsHelper.TERMINS.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    @staticmethod
    def __addFactor(f : 'UnitsFactors', u0 : 'Unit', abbr_cyr : str, abbr_lat : str, names_ru : str, names_ua : str, names_en : str) -> 'Unit':
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
            mult = .1
        elif (swichVal == UnitsFactors.DECI): 
            pref_cyr = "Д"
            pref_lat = "D"
            pref_ru = "ДЕЦИ"
            pref_ua = "ДЕЦИ"
            pref_en = "DECI"
            mult = .01
        elif (swichVal == UnitsFactors.GIGA): 
            pref_cyr = "Г"
            pref_lat = "G"
            pref_ru = "ГИГА"
            pref_ua = "ГІГА"
            pref_en = "GIGA"
            mult = (1000000000)
        elif (swichVal == UnitsFactors.KILO): 
            pref_cyr = "К"
            pref_lat = "K"
            pref_ru = "КИЛО"
            pref_ua = "КІЛО"
            pref_en = "KILO"
            mult = (1000)
        elif (swichVal == UnitsFactors.MEGA): 
            pref_cyr = "М"
            pref_lat = "M"
            pref_ru = "МЕГА"
            pref_ua = "МЕГА"
            pref_en = "MEGA"
            mult = (1000000)
        elif (swichVal == UnitsFactors.MICRO): 
            pref_cyr = "МК"
            pref_lat = "MK"
            pref_ru = "МИКРО"
            pref_ua = "МІКРО"
            pref_en = "MICRO"
            mult = .0001
        elif (swichVal == UnitsFactors.MILLI): 
            pref_cyr = "М"
            pref_lat = "M"
            pref_ru = "МИЛЛИ"
            pref_ua = "МІЛІ"
            pref_en = "MILLI"
            mult = .001
        elif (swichVal == UnitsFactors.NANO): 
            pref_cyr = "Н"
            pref_lat = "N"
            pref_ru = "НАНО"
            pref_ua = "НАНО"
            pref_en = "NANO"
            mult = .0000000001
        elif (swichVal == UnitsFactors.PICO): 
            pref_cyr = "П"
            pref_lat = "P"
            pref_ru = "ПИКО"
            pref_ua = "ПІКО"
            pref_en = "PICO"
            mult = .0000000000001
        elif (swichVal == UnitsFactors.TERA): 
            pref_cyr = "Т"
            pref_lat = "T"
            pref_ru = "ТЕРА"
            pref_ua = "ТЕРА"
            pref_en = "TERA"
            mult = (1000000000000)
        u = Unit._new1628(pref_cyr.lower() + u0.name_cyr, pref_lat.lower() + u0.name_lat, pref_ru.lower() + u0.fullname_cyr, pref_en.lower() + u0.fullname_lat, f, mult, u0, u0.kind)
        if (f == UnitsFactors.MEGA or f == UnitsFactors.TERA or f == UnitsFactors.GIGA): 
            u.name_cyr = (pref_cyr + u0.name_cyr)
            u.name_lat = (pref_lat + u0.name_lat)
        UnitsHelper.UNITS.append(u)
        nams = Utils.splitString(names_ru, ';', False)
        t = Termin._new118(pref_ru + nams[0], u)
        i = 1
        while i < len(nams): 
            t.addVariant(pref_ru + nams[i], False)
            i += 1
        for n in nams: 
            t.addVariant(pref_cyr + n, False)
        for n in Utils.splitString(names_ua, ';', False): 
            t.addVariant(pref_ua + n, False)
            t.addVariant(pref_cyr + n, False)
        for n in Utils.splitString(names_en, ';', False): 
            t.addVariant(pref_en + n, False)
            t.addVariant(pref_lat + n, False)
        for n in Utils.splitString(abbr_cyr, ';', False): 
            t.addAbridge(pref_cyr + n)
        for n in Utils.splitString(abbr_lat, ';', False): 
            t.addAbridge(pref_lat + n)
        UnitsHelper.TERMINS.add(t)
        return u
    
    # static constructor for class UnitsHelper
    @staticmethod
    def _static_ctor():
        from pullenti.ner.core.TerminCollection import TerminCollection
        UnitsHelper.UNITS = list()
        UnitsHelper.TERMINS = TerminCollection()

UnitsHelper._static_ctor()