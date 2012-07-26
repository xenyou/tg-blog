<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head />

<body>

<form action="save" method="post" enctype="multipart/form-data">
<table>
  <tr>
    <td class="label"><label for="subject">subject : </label></td>
    <td class="body">
      <input py:if="article is None" type="text" name="subject" id="subject" size="50" maxlength="50" value="" />
      <input py:if="article" type="text" name="subject" id="subject" size="50" maxlength="50" value="${article.subject}" />
    </td>
  </tr>
  <tr>
    <td class="label"><label for="body">body text: </label></td>
    <td>
    <textarea py:if="article is None" name="body" id="body" cols="50" rows="10" />
    <textarea py:if="article" name="body" id="body" cols="50" rows="10">${article.body}</textarea>
    </td>
  </tr>
  <tr>
    <td class="label"><label for="category">category : </label></td>
    <td>
    <select name="category" id="category" style="width:25%">
      <option value="">new category</option>
      <option py:if="article and article.category != None" selected="selected" value="${article.category.id}">${article.category.name}</option>
      <option py:for="c in categories" py:attrs="'value' : '%s' % c.id">
      ${c.name}
      </option>
    </select>
    <input type="text" name="new_category" id="new_category" size="20" maxlength="200" />
    </td>
  </tr>
  <tr>
    <td class="label"><label for="file">attached file : </label></td>
    <td><input type="file" name="file" id="file" /></td>
  </tr>
  <tr>
    <td class="label"><label for="external">external resource : </label></td>
    <td><input type="text" name="external" id="external" size="60" maxlength="200" /></td>
  </tr>
  <tr>
    <td class="label"><label for="extname">resource name : </label></td>
    <td><input type="text" name="extname" id="extname" size="30" maxlength="30" /></td>
  </tr>
  <tr>
    <td class="label"><label for="tburl">trackback URL : </label></td>
    <td><input type="text" name="tburl" id="tburl" size="60" maxlength="100" /></td>
  </tr>
  <tr>
    <td></td>
    <td><input type="submit" value="post" /></td>
  </tr>
</table>
<input py:if="article" type="hidden" name="id" value="${article.entryid}" />
</form>

</body>

</html>
