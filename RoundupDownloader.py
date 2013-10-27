from lxml import etree
from lxml.cssselect import CSSSelector

BASE_URL="http://ivyroundup.googlecode.com/svn/trunk/repo"

class IvyModule:
    @staticmethod
    def get_module(moduledef):
        mod = IvyModule(moduledef[0].text)
        for sp in moduledef[2].xpath("//*/span"):
            mod.add_version(sp.text, sp.getparent().get("href"))

    def __init__(self, name):
        self.name = name;
        self.versions = {}

    def add_version(self, version, url):
        self.versions[version] = url

    def get_name(self):
        return self.name


def main():
    xslt = etree.XSLT(etree.parse(BASE_URL+"/xsl/modules.xsl"))
    xml = etree.parse(BASE_URL+"/modules.xml")
    html = xslt(xml)

    rows = html.xpath("//table/tbody/tr");

    ivy = {}

    for row in rows:
        tdlist = list(row)
    
        if not tdlist[1].text in ivy:
            ivy[tdlist[1].text] = [IvyModule.get_module(tdlist)]
        else:
            ivy[tdlist[1].text].append(IvyModule.get_module(tdlist))

        for c in ivy.keys():
            print "%s => %s" % (c, ivy[c][0].get_name())

if __name__ == "__main__":
    main()

                                     
                                     
    


