<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python
from docutils.core import publish_parts
import time, re
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head />

<body>

<table class="filelisttbl" py:if="not userlist is None">
  <tr>
    <th class="filelist2">user</th>
    <th class="filelist2">privilege</th>
    <th class="filelist2">admit</th>
    <th class="filelist2">delete</th>
  </tr>
  <tr py:for="item in userlist">
    <td class="filelist2">${item.user}</td>
    <td class="filelist2">${item.privilege}</td>
    <td class="filelist2" py:if="item.privilege &#x03C; 5">
      <a href="${tg.url('/admin/admit', user='%s' % item.user)}">admit</a>
    </td>
    <td class="filelist2" py:if="item.privilege == 5">-</td>
    <td class="filelist2" py:if="item.privilege &#x03C; 5">
      <a href="${tg.url('/admin/delete', user='%s' % item.user)}">delete</a>
    </td>
    <td class="filelist2" py:if="item.privilege == 5">-</td>
  </tr>
</table>

<br/>
<form action="register_exec" method="post">
<div py:if="user is None">
<div>
Enter your information.<br/> 
You can join after authentication by administrator.
</div>
<div>
Username: <input type="text" size="10" maxlength="10" name="user" />
Password: <input type="password" size="10" maxlength="10" name="password" />
<input type="submit" value="register" />
</div>
</div>
<div py:if="user">
<div>User "${user.user}" has level ${user.privilege} privilege.</div>
<div>Do you wanna change your information?</div>
Password: <input type="password" size="10" maxlength="10" name="password" />
<input type="hidden" name="user" value="${user.user}" />
<input type="hidden" name="modify" value="1" />
<input type="submit" value="register" />
</div>
</form>

</body>
</html>

