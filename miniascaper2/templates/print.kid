<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python
from docutils.core import publish_parts
import time, re
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">

<head />

<body>

<div style="width:600px">
    <?python
        posttime = time.strftime('on %A %B %d, %Y at %H:%M:%S',
                                  time.localtime(item.entryid))
        body = publish_parts(item.body,
                             writer_name="html")['html_body']
    ?>
    <div>
        <h2>${item.subject}</h2>
    </div>
    <div>Written by ${item.author} ${posttime}</div>
    <div py:replace="XML(body)">body replace</div>
</div>

</body>
</html>

