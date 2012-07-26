<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python
from docutils.core import publish_parts
import time, re
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
<script src="${tg.tg_js}/MochiKit.js"></script>
<script type="text/javascript">
archiveon = 0;
addLoadEvent(function() {
    connect('archives', 'onclick', function(e) {
        e.preventDefault();
        var d = loadJSONDoc("${tg.url('/archives', tg_format='json')}");
        d.addCallback(showArchives);
        }
    );
    }
);
function showArchives(result) {
    var archives = DIV(null, map(row_display, result["archives"]));
    if (archiveon == 1) {
        archives = '';
        archiveon = 0;
    } else {
        archiveon = 1;
    }
    replaceChildNodes("archives_results", archives);
}
function row_display(row) {
    var months = ['Zero', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return DIV({'class': 'entries'}, A({"href" : "${tg.url('/')}" + "?year=" + row.year + "&amp;month=" + row.month}, months[row.month] + ", " +  row.year))
}
</script>
</head>

<body>

<?python
article_num = article.count()
pages = (article_num - 1) / offs
page = int(requests['page'])
start = page * offs

extfile = re.compile(r'^http*://')
?>

<table class="main">
<tr class="main">
<td class="topleft">


<p py:if="'category' in requests">
<span>categories : </span>
<span py:for="category in categories">
<span py:if="category.id != int(requests['category'])">
&lt;<a href="${tg.url('/', category=category.id)}">${category.name}(${len(category.articles)})</a>&gt;
</span>
<span py:if="category.id == int(requests['category'])">&lt;${category.name}(${len(category.articles)})&gt;</span>
</span>
</p>

<p py:if="not 'category' in requests">
<span>categories : </span>
<span py:for="category in categories">
&lt;<a href="${tg.url('/', category=category.id)}">${category.name}(${len(category.articles)})</a>&gt;
</span>
</p>


<span>pages : </span>
<span py:for="i in range(0, pages+1)">
<span py:if="page!=i">
<?python
requests['page'] = i
?>
[<a href="${tg.url('/', **requests)}">${i}</a>]</span>
<span py:if="page==i">[${i}]</span>
</span>

<?python
# reset page number
requests['page'] = page
# to avoid collision of id for 'delete' method
if 'id' in requests:
  del requests['id']
# what a stupid code...
?>

<div class="generic_s1">
There are ${article_num} articles.
<span py:if="(article_num - start) &#x03E; offs">
Following ${offs} data are in this page.
</span>
<span py:if="(article_num - start) &#x03C; offs">
Following ${article_num - start} data are in this page.
</span>
</div>

<div class="article" py:for="item in article[start:start+offs]">
    <?python
        posttime = time.strftime('on %A %B %d, %Y at %H:%M:%S',
                                  time.localtime(item.entryid))
        body = publish_parts(item.body,
                             writer_name="html")['html_body']
    ?>
    <div>
        <span class="subject">${item.subject}</span>
    </div>
    <div py:replace="XML(body)">body replace</div>
    <div class="posttime">Written by ${item.author} ${posttime}</div>
    <div class="generic_s1" align="right">
    Trackback URL: ${url}/recv/$item.entryid
    </div>
    <div class="posttime">
      <span>&lt;<a href="${tg.url('/', category=item.category.id)}">${item.category.name}</a>&gt;</span>
      <span>[<a href="${tg.url('/printpage', id=item.entryid)}">print</a>]</span>
      <span>[<a href="${tg.url('/edit', id=item.entryid)}">modify</a>]</span>
      <span>[<a onclick="return confirm('Are you sure you want to delete?');" href="${tg.url('/delete', id=item.entryid, **requests)}">delete</a>]</span>
    </div>
    <div class="generic_s1" py:if="item.attached_files != []">
    Attached files
    </div>
    <span class="generic_s1" py:for="file in item.attached_files[:4]">
    <span py:if="extfile.match(file.onfsname)"><a href="${file.onfsname}">${file.name}</a></span>
    <span py:if="not extfile.match(file.onfsname)"><a href="${tg.url('/download', filename='%s' % file.onfsname)}">${file.name}</a></span>
    </span>
    <div class="generic_s1" py:if="item.trackbacks != []">
    References to this entry
    </div>
    <div class="generic_s1" py:for="tb in item.trackbacks">
        <?python
            tbtime = time.strftime('%A %B %d, %Y %H:%M:%S',
                                   time.localtime(tb.posttime))
        ?>
        <b><a href="${tb.url}">${tb.title}</a></b>
        <span>@ ${tb.blog_name} (${tbtime})</span>
        <span><a href="${tg.url('deltb', id='%s' % tb.id)}">[delete]</a></span>
        <br/>
        <span py:if="len(tb.excerpt) &#x03C; 255">${tb.excerpt}</span>
        <span py:if="len(tb.excerpt) &#x03E; 255">${tb.excerpt[:252]}...</span>
    </div>
</div>
 
<span>pages : </span>
<span py:for="i in range(0, pages+1)">
<span py:if="page!=i">
<?python
requests['page'] = i
?>
[<a href="${tg.url('/', **requests)}">${i}</a>]</span>
<span py:if="page==i">[${i}]</span>
</span>
</td>

<td width="3" bgcolor="silver" />

<td class="topright">

<p class="archives">
<a id="archives" href="${tg.url('/archives')}">view archives</a>
</p>
<div id="archives_results"></div>

<p class="archives">
Showing Entries
</p>
<div class="entries" py:for="item in article[start:start+offs]">
<a href="${tg.url('/', id='%s' % item.entryid)}">${item.subject}</a>
</div>

</td>
</tr>
</table>

<hr color="silver" />

</body>
</html>
