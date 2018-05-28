# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import xml.etree.ElementTree
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.org.internal.ResourceHelper import ResourceHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis


class OrgGlobal:
    
    GLOBAL_ORGS = None
    
    GLOBAL_ORGS_UA = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
        from pullenti.ner.ProcessorService import ProcessorService
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.Termin import Termin
        if (OrgGlobal.GLOBAL_ORGS is not None): 
            return
        OrgGlobal.GLOBAL_ORGS = IntOntologyCollection()
        with ProcessorService.create_empty_processor() as geo_proc: 
            geo_proc.add_analyzer(GeoAnalyzer())
            geos = dict()
            for k in range(3):
                lang = (MorphLang.RU if k == 0 else (MorphLang.EN if k == 1 else MorphLang.UA))
                name = ("Orgs_ru.dat" if k == 0 else ("Orgs_en.dat" if k == 1 else "Orgs_ua.dat"))
                dat = ResourceHelper.get_bytes(name)
                if (dat is None): 
                    raise Utils.newException("Can't file resource file {0} in Organization analyzer".format(name), None)
                with io.BytesIO(OrgItemTypeToken._deflate(dat)) as tmp: 
                    tmp.seek(0, io.SEEK_SET)
                    xml0 = None # new XmlDocument
                    xml0 = xml.etree.ElementTree.parse(tmp)
                    for x in xml0.getroot(): 
                        org_ = OrganizationReferent()
                        abbr = None
                        for xx in x: 
                            if (xx.tag == "typ"): 
                                org_.add_slot(OrganizationReferent.ATTR_TYPE, Utils.getXmlInnerText(xx), False, 0)
                            elif (xx.tag == "nam"): 
                                org_.add_slot(OrganizationReferent.ATTR_NAME, Utils.getXmlInnerText(xx), False, 0)
                            elif (xx.tag == "epo"): 
                                org_.add_slot(OrganizationReferent.ATTR_EPONYM, Utils.getXmlInnerText(xx), False, 0)
                            elif (xx.tag == "prof"): 
                                org_.add_slot(OrganizationReferent.ATTR_PROFILE, Utils.getXmlInnerText(xx), False, 0)
                            elif (xx.tag == "abbr"): 
                                abbr = Utils.getXmlInnerText(xx)
                            elif (xx.tag == "geo"): 
                                inoutarg1479 = RefOutArgWrapper(None)
                                inoutres1480 = Utils.tryGetValue(geos, Utils.getXmlInnerText(xx), inoutarg1479)
                                geo_ = inoutarg1479.value
                                if (not inoutres1480): 
                                    ar = geo_proc.process(SourceOfAnalysis(Utils.getXmlInnerText(xx)), None, lang)
                                    if (ar is not None and len(ar.entities) == 1 and isinstance(ar.entities[0], GeoReferent)): 
                                        geo_ = (ar.entities[0] if isinstance(ar.entities[0], GeoReferent) else None)
                                        geos[Utils.getXmlInnerText(xx)] = geo_
                                    else: 
                                        pass
                                if (geo_ is not None): 
                                    org_.add_slot(OrganizationReferent.ATTR_GEO, geo_, False, 0)
                        oi = org_.create_ontology_item_ex(2, True, True)
                        if (oi is None): 
                            continue
                        if (abbr is not None): 
                            oi.termins.append(Termin(abbr))
                        if (k == 2): 
                            OrgGlobal.GLOBAL_ORGS_UA.add_item(oi)
                        else: 
                            OrgGlobal.GLOBAL_ORGS.add_item(oi)
        return
    
    # static constructor for class OrgGlobal
    @staticmethod
    def _static_ctor():
        from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
        OrgGlobal.GLOBAL_ORGS_UA = IntOntologyCollection()

OrgGlobal._static_ctor()