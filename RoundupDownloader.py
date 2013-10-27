from lxml import etree

import argparse


BASE_URL="http://ivyroundup.googlecode.com/svn/trunk/repo"

class IvyModule:
    @staticmethod
    def get_module(moduledef):
        mod = IvyModule(moduledef[0].text)
        for sp in moduledef[2].xpath("./*/span"):
            mod.add_version(sp.text, sp.getparent().get("href"))
            
	return mod

    def __init__(self, name):
        self.name = name;
        self.versions = {}

    def add_version(self, version, url):
        self.versions[version] = url

    def get_name(self):
        return self.name
      
    def get_versions(self):
        return self.versions.keys()


def initialize_ivyloader():
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


def main():
    parser = argparse.ArgumentParser(description='Search and download from IvyRoundup')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--find", "-f", nargs='+',
			help="Search for ivy component.  At least one of org, module, version required" )
    group.add_argument("--resolve", "-r", nargs=3,  help="Resolve ivy component")
    group.add_argument("--install", "-i", nargs=3, help="Install ivy component")
    group.add_argument("--list", "-l", help="List all ivy components")
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()

                                     
                                     
    


