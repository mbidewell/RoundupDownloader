from lxml import etree

BASE_URL="http://ivyroundup.googlecode.com/svn/trunk/repo"


def main():
    xslt = etree.XSLT(etree.parse(BASE_URL+"/xsl/modules.xsl"))
    xml = etree.parse(BASE_URL+"/modules.xml")
    html = xslt(xml)

    rows = html.xpath("//table/tbody/tr");

    ivy = {}

    for row in rows:
        tdlist = list(row)
    
        if not tdlist[1].text in ivy:
            ivy[tdlist[1].text] = [tdlist[0].text]
        else:
            ivy[tdlist[1].text].append(tdlist[0].text)

        for c in ivy.keys():
            print "%s => %s" % (c, ','.join(ivy[c]))

if __name__ == "__main__":
    main()

                                     
                                     
    


