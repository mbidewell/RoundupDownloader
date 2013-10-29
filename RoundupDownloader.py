from lxml import etree

import argparse


BASE_URL="http://ivyroundup.googlecode.com/svn/trunk/repo"

class IvyModule:
    @staticmethod
    def get_module(moduledef):
        mod = IvyModule(moduledef[1].text, moduledef[0].text)
        for sp in moduledef[2].xpath("./*/span"):
            mod.add_version(sp.text, sp.getparent().get("href"))
            
	return mod

    def __init__(self, org, name):
        self.org = org
        self.name = name;
        self.versions = {}

    def add_version(self, version, url):
        self.versions[version] = BASE_URL + url

    def get_org(self):
        return self.org
    
    def get_name(self):
        return self.name
      
    def get_versions(self):
        return self.versions

class IvyRepository:
    def __init__(self):
        self.repo = {}

    def add_org_module(self, org, module):
        if not org in self.repo:
            self.repo[org] = [module]
        else:
            self.repo[org].append(module)

    def get_modules(self):
        return list(self.repo.values())

    def search(self, criteria):
        if criteria["org"] in self.repo:
            modules = self.repo[criteria["org"]]
            if "module" in criteria:
                for m in modules:
                    if m.get_name() == criteria["module"]:
                        if "version" in criteria:
                            if criteria["version"] in m.get_versions():
                                return m
                        else:
                            return m

            else:
                return modules



def dump_ivy_object(obj):
    if isinstance(obj, IvyModule):
        print "Organization: %s" % obj.get_org()
        print "Name: %s" % obj.get_name()
        print "Versions: "
        for ver in obj.get_versions().keys():
            print "\t%s => %s" % (ver, obj.get_versions()[ver])
    elif type(obj) == type([]):
        for o in obj:
            dump_ivy_object(o)
            print "=========================="



def initialize_ivyloader():
    global ivy_repo
    xslt = etree.XSLT(etree.parse(BASE_URL+"/xsl/modules.xsl"))
    xml = etree.parse(BASE_URL+"/modules.xml")
    html = xslt(xml)

    rows = html.xpath("//table/tbody/tr");

    ivy_repo = IvyRepository()

    for row in rows:
        tdlist = list(row)
        module = IvyModule.get_module(tdlist)
        ivy_repo.add_org_module(tdlist[1].text, module)

def list_to_dict(keys, values):
    dct = {}
    for i in xrange(len(keys)):
        if i < len(values):
            dct[keys[i]] = values[i]
    return dct


def main():
    parser = argparse.ArgumentParser(description='Search and download from IvyRoundup')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--find", "-f", nargs='+',
			help="Search for ivy component.  At least one of org, module, version required" )
    group.add_argument("--resolve", "-r", nargs=3,  help="Resolve ivy component")
    group.add_argument("--install", "-i", nargs=3, help="Install ivy component")
    group.add_argument("--list", "-l", action="store_true", help="List all ivy components")
    args = parser.parse_args()
    
    print args

    if args.find != None:
        result = ivy_repo.search(list_to_dict(["org", "module", "version"], args.find))
        if result != None:
            dump_ivy_object(result)
    elif args.list:
        dump_ivy_object(ivy_repo.get_modules())





ivy_repo = None

if __name__ == "__main__":
    initialize_ivyloader()
    main()

                                     
                                     
    


