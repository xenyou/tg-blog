<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python
from docutils.core import publish_parts
import time, re
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<?python
msgs_num = msgs.count()
pages = (msgs_num - 1) / offs
start = int(page) * offs
?>

<head />

<body>

<span>pages : </span>
<span py:for="i in range(0, pages+1)">
<span py:if="int(page)!=i">
<?python
requests['page'] = i
?>
[<a href="${tg.url('/bbs/read', **requests)}">${i}</a>]
</span>
<span py:if="int(page)==i">[${i}]</span>
</span>


<div class="generic_s1">
There are ${msgs_num} messages.
<span py:if="(msgs_num - start) &#x03E; offs">
Following ${offs} data are in this page.
</span>
<span py:if="(msgs_num - start) &#x03C; offs">
Following ${msgs_num - start} data are in this page.
</span>
</div>

<table class="none">
<tr>
<td>

<div py:if="msgs_num == 0" class="bbs">There is no messages.</div>
<div class="article" py:for="item in msgs[start:start+offs]">
  <?python
      postday = time.strftime('%A %B %d, %Y', time.localtime(item.posttime))
      posttime = time.strftime('%H:%M:%S', time.localtime(item.posttime))
      body = publish_parts(item.body, writer_name="html")['html_body']
  ?>
  <div>[id : ${item.id}]</div>
  <div>${XML(body)}</div>
  <div class="bmeta">Posted by ${item.poster}</div>
  <div class="bmeta" py:if="item.signature">signature [${item.signature}]</div>
  <div class="bmeta">on ${postday} at ${posttime}</div>
  <div class="bmeta">
    <a href="${tg.url('/bbs/delete', id=item.id)}">delete</a>
  </div>
</div>

</td>
<td class="biform">

<form action="search" method="post">
    <label class="blabel" for="logkey">Search for message by keyword.</label>
    <div class="bbody">
      <input type="text" name="logkey" id="logkey" size="10" maxlength="100" />
      <input type="submit" value="search" />
    </div>
</form>
<hr/>
<form action="save" method="post">
    <label class="blabel" for="body">Write your message.</label>
    <div class="bbody">
    <textarea name="body" id="body" cols="30" rows="10"/>
    </div>
    <label class="blabel" for="title">Write your name.</label>
    <div class="bbody">
      <input type="text" name="poster" id="title" size="10" maxlength="10" />
      <input type="submit" value="post" />
    </div>
    <label class="blabel" for="signature">Signature (if you need)</label>
    <div class="bbody">
      <input type="text" name="signature" id="signature" size="10" maxlength="10" />
    </div>
</form>

</td>
</tr>
</table>

<span>pages : </span>
<span py:for="i in range(0, pages+1)">
<span py:if="int(page)!=i">
<?python
requests['page'] = i
?>
[<a href="${tg.url('/bbs/read', **requests)}">${i}</a>]
</span>
<span py:if="int(page)==i">[${i}]</span>
</span>

</body>
</html>

