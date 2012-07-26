<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<?python
import re

file_num = upfiles.count()
pages = (file_num - 1) / offs
start = int(page) * offs

extfile = re.compile(r'^http*://')
?>

<head />
<body>

<span>pages : </span>
<span py:for="i in range(0, pages+1)">
<span py:if="int(page)!=i">
[<a href="${tg.url('/uplist', page='%d' % i)}">${i}</a>]
</span>
<span py:if="int(page)==i">[${i}]</span>
</span>

<div class="generic_s1">
There are ${file_num} articles.
<span py:if="(file_num - start) &#x03E; offs">
Following ${offs} data in this page.
</span>
<span py:if="(file_num - start) &#x03C; offs">
Following ${file_num - start} data in this page.
</span>
</div>

<table class="filelisttbl" py:if="upfiles.count()!=0">
  <tr>
      <th class="filelist1">Filename</th>
      <th class="filelist2">Download Link</th>
      <th class="filelist1">Related Article</th>
      <th class="filelist2">Posted User</th>
      <th class="filelist2">Delete File</th>
  </tr>
  <tr py:for="file in upfiles[start:start+offs]">
    <td class="filelist1">${file.name}</td>
    <td class="filelist2">
      <span py:if="extfile.match(file.onfsname)"><a href="${file.onfsname}">
      refer to the file
      </a></span>
      <span py:if="not extfile.match(file.onfsname)"><a href="${tg.url('/download', filename='%s' % file.onfsname)}">
      download file
      </a></span>
    </td> 
    <td class="filelist1">
      <span py:if="file.article is not None">
      <a href="${tg.url('/', id='%s' % file.article.entryid)}">
      ${file.article.subject[:50]}
      </a>
      </span>
      <span py:if="file.article is None">
      unavailable
      </span>
    </td>
    <td class="filelist2">
      <span py:if="file.article is not None">
      <a href="${tg.url('/', author='%s' % file.article.author)}">
      ${file.article.author}
      </a>
      </span>
      <span py:if="file.article is None">
      unavailable
      </span>
    </td>
    <td class="filelist2">
      <a onclick="return confirm('Are you sure you want to delete?');" href="${tg.url('/deletefile', filename='%s' % file.onfsname)}">
      delete file
      </a>
    </td>
  </tr>
</table>

<br/>
<span>pages : </span>
<span py:for="i in range(0, pages+1)">
<span py:if="int(page)!=i">
[<a href="${tg.url('/uplist', page='%d' % i)}">${i}</a>]
</span>
<span py:if="int(page)==i">[${i}]</span>
</span>

</body>
</html>

