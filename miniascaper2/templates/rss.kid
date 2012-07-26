<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns="http://purl.org/rss/1.0/"
 xmlns:py="http://purl.org/kid/ns#"
>

<channel py:attrs="'rdf:about':'%s/rss' % url">
  <title>${sitename}</title>
  <link>${url}</link>
  <description></description>
  <items>
    <rdf:Seq>
    <rdf:li py:for="item in article[:10]" py:attrs="'rdf:resource':'%s/index?id=%s' % (url,item.entryid)" />
    </rdf:Seq>
  </items>
</channel>

<item py:for="item in article[:10]" py:attrs="'rdf:about':'%s/index?id=%s' % (url,item.entryid)" >
  <title>${item.subject}</title>
  <link>${url}/index?id=${item.entryid}</link>
  <description>${item.body[:100]}</description>
</item>

</rdf:RDF>
