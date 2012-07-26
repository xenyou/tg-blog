# import logging
# log = logging.getLogger("miniascaper2.controllers")

from miniascaper2.model import *
from turbogears import controllers, expose, widgets, flash, redirect
import time, sys, os, re, sha, datetime, urllib, xml.dom.minidom
import turbogears, cherrypy


# Pre-Script for configuration

STORED = cherrypy.config.get("miniascaper2.uploads", os.path.join(os.getcwd(), "stored"))
if not os.path.exists(STORED):
    os.makedirs(STORED) 

SITENAME= cherrypy.config.get("miniascaper2.sitename", "")
URL = cherrypy.config.get("miniascaper2.url", "")
STOREDURL = URL + "/" + STORED

ARTICLES_PP = cherrypy.config.get("miniascaper2.articles_pp", 60)
MSGS_PP = cherrypy.config.get("miniascaper2.msgs_pp", 10)
FILES_PP = cherrypy.config.get("miniascaper2.upfiles_pp", 10)
ACCESSLOGS = cherrypy.config.get("miniascaper2.accesslogs", 30)


# Common Widgets

def append_providers(vars):
    vars['cnavi'] = CommonNavigator()

turbogears.view.variable_providers.append(append_providers)


class CommonNavigator(widgets.Widget):
    params = ['author', 'session', 'count']

    def __init__(self):
        super(CommonNavigator, self).__init__()
        self.author = User.select()
        self.session = cherrypy.session
        stats = Statistics.select()
        self.count = stats[0].counter

    template = '''
    <div xmlns:py="http://purl.org/kid/ns#">
      <div class="navi">
        <span py:if="'user' in session">
        * ${session['user']} * : [<a href="${tg.url('/admin/register?%s' % session['user'])}">modify</a>]
        [<a href="${tg.url('/admin/logout')}">logout</a>]
        </span>
        <span py:if="not 'user' in session">
        * guest * : [<a href="${tg.url('/admin/register')}">registration</a>]
        </span>
        [<a href="${tg.url('/edit')}">write</a>]
        [<a href="${tg.url('/bbs/read')}">bbs</a>]
        <span> | </span>
        [<a href="${tg.url('/')}">top</a>]
        [<a href="${tg.url('/rss')}">rss</a>]
        [<a href="${tg.url('/uplist')}">uplist</a>]
      </div>
      <div>
        <form action="${tg.url('/search')}" method="post">
        <span>Search log</span>
        <label for="logbydate">by date:</label>
        <input id="logbydate" type="text" size="4" maxlength="4" name="year" />
        <span>/</span>
        <input type="text" size="2" maxlength="2" name="month" />
        <span>/</span>
        <input type="text" size="2" maxlength="2" name="day" />
        <span> or </span>
        <label for="logauthor">by author:</label>
        <select name="author">
          <option value="all" selected="selected">all</option>
          <option py:for="a in author" py:attrs="'value' : '%s' % a.user">
          ${a.user}
          </option>
        </select>
        <span> or </span>
        <label for="logbykey">by keyword:</label>
        <input id="logbykey" type="text" size="10" maxlength="40" name="logkey" />
        <input type="submit" value="search" />
        </form>
      </div>
      <div py:if="not 'user' in session">
        <form action="${tg.url('/admin/login')}" method="post">
        <span>Enter system as </span>
        <label for="userform">user:</label>
        <input id="userform" type="text" size="10" maxlength="10" name="user" />
        <span>and</span>
        <label for="passform">pass:</label>
        <input id="passform" type="password" size="10" maxlength="10" name="password" />
        <input type="submit" value="login" />
        </form>
      </div>
      <div>This page has loaded ${count} times.</div>
      <hr />
    </div>
    '''

# Utility Functions

def superuser():
    if 'privilege' in cherrypy.session and cherrypy.session['privilege'] == 5:
        return True
    else:
        return False


# Controllers

class Admin:
    @expose()
    def login(self, **kw):
        if not 'user' in kw or not 'password' in kw:
            flash('The information you entered is incorrect.')
            raise redirect("/")

        encpass = sha.new(kw['password']).hexdigest()
        ret = User.select(AND(User.q.user==kw['user'], User.q.password==encpass))
        if ret.count() == 0:
            flash('The information you entered is incorrect.')
            raise redirect("/")

        cherrypy.session['user'] = ret[0].user
        cherrypy.session['privilege'] = ret[0].privilege

        flash('Login has been successful.')
        raise redirect("/", author=cherrypy.session['user'])

    @expose()
    def logout(self, **kw):
        if not 'user' in cherrypy.session or not 'privilege' in cherrypy.session:
            raise redirect("/")

        del cherrypy.session['user']
        del cherrypy.session['privilege']

        flash('Logout has been successful.')
        raise redirect("/")

    @expose(template="miniascaper2.templates.regist")
    def register(self, **kw):
        userlist = None
        if superuser():
            userlist = User.select()

        user = None
        if 'user' in cherrypy.session:
            user = User.byUser(cherrypy.session['user'])

        return dict(sitename=SITENAME, userlist=userlist, user=user)

    @expose()
    def register_exec(self, **kw):
        if not 'user' in kw or kw['user'] == "" or \
           not 'password' in kw or kw['password'] == "":
            flash('User registration has failed.')
            raise redirect("/admin/register")

        encpass = sha.new(kw['password']).hexdigest()
        if not 'modify' in kw:
            user_num = User.select().count()
            if user_num == 0:
                # This block is system initialization,
                # Creating administrator and essential data.
                User(user=kw['user'], password=encpass, privilege=5)
                Category(name='non categorized')
            else:
                ret = User.select(User.q.user==kw['user']).count()
                if ret != 0:
                    flash('User "%s" already exists.' % kw['user'])
                    raise redirect("/admin/register")
                User(user=kw['user'], password=encpass, privilege=2)
        else:
            user = User.byUser(kw['user'])
            user.password = encpass

        flash('User registration has been successful.')
        raise redirect("/")

    @expose()
    def admit(self, **kw):
        if superuser():
            user = User.byUser(kw['user'])
            user.privilege = 3
        else:
            flash("This operation is not permitted to you.")
            raise redirect("/")

        flash('User "%s" has been admited.' % kw['user'])
        raise redirect("/admin/register")

    @expose()
    def delete(self, **kw):
        if superuser():
            user = User.byUser(kw['user'])
            User.delete(user.id)
        else:
            flash("This operation is not permitted to you.")
            raise redirect("/")

        flash('User "%s" has been deleted.' % kw['user'])
        raise redirect("/admin/register")

    @expose(template="miniascaper2.templates.notfound")
    def default(self, *args, **kw):
        return dict(sitename=SITENAME)


class RecvTb:
    @expose(template="miniascaper2.templates.tbresponse",
            format="xml", content_type="text/xml")
    def default(self, *args, **kw):
        article_id = int(args[0])
        try:
            article = Article.byEntryid(article_id)
            t = int(time.time())
            tb = Trackback(title=kw['title'], url=kw['url'], excerpt=kw['excerpt'], blog_name=kw['blog_name'], article=article.id, posttime=t)
            err=0
            err_message=""
        except:
            err=1
            err_message = str(sys.exc_info()[1])

        return dict(err=err, message=err_message)


class MsgBd:
    @expose(template="miniascaper2.templates.bbs")
    def read(self, **kw):
        if not 'page' in kw:
            kw['page'] = 0

        if 'id' in kw:
            msgs = Msg.select(Msg.q.id==int(kw['id']))
        elif 'logkey' in kw and kw['logkey'] != "":
            if isinstance(kw['logkey'], unicode):
                kw['logkey'] = kw['logkey'].encode('utf-8')
            msgs = Msg.select(Msg.q.body.contains(kw['logkey']), orderBy='-posttime')
        else:
            msgs = Msg.select(orderBy='-posttime')

        return dict(sitename=SITENAME, msgs=msgs, page=kw['page'], offs=MSGS_PP, requests=kw)

    @expose(template="miniascaper2.templates.notfound")
    def default(self, *args, **kw):
        return dict(sitename=SITENAME)

    @expose()
    def search(self, **kw):
        params = {}
        if 'logkey' in kw:
            params['logkey'] = kw['logkey']

        raise redirect(turbogears.url("/bbs/read"), **params)

    @expose()
    def save(self, **kw):
        if kw['body'] == "":
            raise redirect("/bbs/read")
        if kw['poster'] == "":
            kw['poster'] = 'anonymous'

        t = int(time.time())
        ipaddr = cherrypy.request.remote_addr
        if kw['signature'] != "":
            if isinstance(kw['signature'], unicode):
                kw['signature'] = kw['signature'].encode('utf-8')
            encsig = sha.new(kw['signature']).hexdigest()
            Msg(poster=kw['poster'], body=kw['body'], posttime=t, client=ipaddr, signature=encsig)
        else: 
            Msg(poster=kw['poster'], body=kw['body'], posttime=t, client=ipaddr, signature=None)

        flash("The massage has been posted.")
        raise redirect("/bbs/read")

    @expose()
    def delete(self, **kw):
        if not 'id' in kw:
            raise redirect("/bbs/read")
        else:
            if 'user' in cherrypy.session:
                author=cherrypy.session['user']
            else:
                flash("This operation is not permitted to you.")
                raise redirect("/bbs/read")

            msgs = Msg.select(Msg.q.id==int(kw['id']))
            msg = msgs[0]

            if superuser():
                Msg.delete(msg.id)
            else:
                flash("This operation is not permitted to you.")
                raise redirect("/bbs/read")

        flash("The message has been deleted.")
        raise redirect("/bbs/read")


class Root(controllers.RootController):

    recv = RecvTb()
    bbs = MsgBd()
    admin = Admin()

    @expose(template="miniascaper2.templates.top")
    def index(self, **kw):

        query = ""
        if 'id' in kw:
            query = "Article.q.entryid==%s, " % kw['id']
        if 'author' in kw:
            if kw['author'] != 'all':
                query = query + "Article.q.author=='%s', " % kw['author']
        if 'year' in kw:
            query = query + "Article.q.year==%s, " % kw['year']
        if 'month' in kw:
            query = query + "Article.q.month==%s, " % kw['month']
        if 'day' in kw:
            query = query + "Article.q.day==%s, " % kw['day']
        if 'category' in kw:
            query = query + "Article.q.categoryID==%s, " % kw['category']
        if 'logkey' in kw:
            query = query + "OR(Article.q.body.contains('%s'), Article.q.subject.contains('%s'))" % (kw['logkey'], kw['logkey'])

        if query == "":
            article = Article.select(orderBy='-entryid')
        else: 
            endp = re.compile(r', $')
            endp.sub('', query)
            query="AND(" + query + ")"
            article = Article.select(eval(query), orderBy='-entryid')

        ipaddr = cherrypy.request.remote_addr

        stats = Statistics.select()
        if stats.count() == 0:
            Statistics(counter=0)
        else:
            stats[0].counter = stats[0].counter + 1

        logs = Access.select(orderBy='id')
        if logs.count() >= ACCESSLOGS:
            Access.delete(logs[0].id)
        Access(ipaddress=ipaddr, accesstime=datetime.datetime.now())

        categories = Category.select()

        if not 'page' in kw:
            kw['page'] = 0

        return dict(article=article, sitename=SITENAME, url=URL, stored=STOREDURL,
                    requests=kw, offs=ARTICLES_PP, categories=categories)

    @expose()
    @expose("json")
    def archives(self, **kw):
        archives = Article.select(orderBy=["-year", "-month"], distinct=True)
        ret = []
        prev = None
        for i in archives:
            if prev is None or i.year != prev.year or (i.year == prev.year and i.month != prev.month):
                ret.append(i)
            prev = i
        return dict(archives=ret)

    @expose(template="miniascaper2.templates.print")
    def printpage(self, id=0, **kw):
        try:
            article = Article.byEntryid(int(id))
        except:
            raise redirect("/")
        return dict(item=article)

    @expose(template="miniascaper2.templates.edit")
    def edit(self, **kw):
        if not 'user' in cherrypy.session:
            flash("This operation is not permitted to you.")
            raise redirect(turbogears.url("/"), **kw)

        if 'id' in kw:
            article = Article.byEntryid(int(kw['id']));
            if cherrypy.session['privilege'] < 5 and cherrypy.session['user'] != article.author:
                flash("This operation is not permitted to you.")
                raise redirect("/")
        else:
            article = None
            if cherrypy.session['privilege'] < 3:
                flash("This operation is not permitted to you.")
                raise redirect("/")

        categories = Category.select()

        return dict(sitename=SITENAME, article=article, categories=categories)

    @expose(template="miniascaper2.templates.uplist")
    def uplist(self, **kw):
        if not 'page' in kw:
            kw['page'] = 0
        upfiles = Attached.select(orderBy='-id')
        return dict(sitename=SITENAME, upfiles=upfiles, page=kw['page'], offs=FILES_PP)

    @expose(template="miniascaper2.templates.rss",
            format="xml", content_type="application/rss+xml")
    def rss(self):
        article = Article.select(orderBy='-entryid')
        return dict(article=article, sitename=SITENAME, url=URL)

    @expose(template="miniascaper2.templates.notfound")
    def default(self, *args, **kw):
        return dict(sitename=SITENAME)

    @expose()
    def save(self, **kw):
        if not kw['subject']:
            kw['subject'] = "No title"

        if 'user' in cherrypy.session:
            author=cherrypy.session['user']
        else:
            flash("This operation is not permitted to you.")
            raise redirect("/")

        extfile = re.compile(r'^http*://')
        if 'id' in kw:
            # This case is a modification of existing articles.
            articleid = int(kw['id'])
            article = Article.byEntryid(articleid)
            if superuser() or cherrypy.session['user'] == article.author:
                if kw['file'].filename != "":
                    self.upload(kw['file'], article.id)
                if extfile.match(kw['external']):
                    self.upload(kw['external'], article.id, ext=1, extname=kw['extname'])
                if kw['category'] == "":
                    if kw['new_category'] == "": 
                        default_category = Category.byName("non categorized")
                        article.category = default_category.id
                    else:
                        try:
                            newcategory = Category(name=kw['new_category'])
                        except:
                            newcategory = Category.byName(kw['new_category'])
                        article.category = newcategory.id
                else:
                    article.category = int(kw['category'])
                article.subject = kw['subject']
                article.body = kw['body']
            else:
                flash("This operation is not permitted to you.")
                raise redirect("/")
        else:
            # This case is to create a new article.
            t = int(time.time())
            ts = time.localtime(t)
            articleid = t
            if cherrypy.session['privilege'] >= 3:
                if kw['category'] == "":
                    if kw['new_category'] == "": 
                        default_category = Category.byName("non categorized")
                        category = default_category.id
                    else:
                        try:
                            newcategory = Category(name=kw['new_category'])
                        except:
                            newcategory = Category.byName(kw['new_category'])
                        category = newcategory.id
                else:
                    category = int(kw['category'])
                newarticle = Article(entryid=articleid, subject=kw['subject'], body=kw['body'], year=ts[0], month=ts[1], day=ts[2], author=author, category=category)
                if kw['file'].filename != "":
                    self.upload(kw['file'], newarticle.id)
                if extfile.match(kw['external']):
                    self.upload(kw['external'], newarticle.id, ext=1, extname=kw['extname'])
            else:
                flash("This operation is needed more higher privilege level.")
                raise redirect("/")

        flashmsg = ""
        if extfile.match(kw['tburl']):
            if isinstance(kw['subject'], unicode):
                kw['subject'] = kw['subject'].encode('utf-8')
            if isinstance(kw['body'], unicode):
                kw['body'] = kw['body'].encode('utf-8')
            sitename = SITENAME
            if isinstance(sitename, unicode):
                sitename = sitename.encode('utf-8')
            tbreq = {'title': kw['subject'], 'excerpt': kw['body'][:255], 'url': URL + "?id=%d" % articleid, 'blog_name': sitename}
            try:
                res = urllib.urlopen(kw['tburl'], urllib.urlencode(tbreq))
                tbres = xml.dom.minidom.parse(res).getElementsByTagName('error')
                if tbres[0].firstChild.nodeValue == "0":
                    flashmsg = "Sending trackback request has done. "
                else:
                    flashmsg = "Sending trackback request has failed. "
            except:
                pass

        flash("%sThe article has been written." % flashmsg)
        raise redirect("/")

    @expose()
    def delete(self, **kw):
        if not 'id' in kw:
            raise redirect("/")
        else:
            if not 'user' in cherrypy.session and not 'privilege' in cherrypy.session:
                flash("This operation is not permitted to you.")
                del kw['id']
                raise redirect(turbogears.url("/"), **kw)

            article = Article.byEntryid(int(kw['id']))
            if superuser() or cherrypy.session['user'] == article.author:
                Article.delete(article.id)
            else:
                flash("This operation is not permitted to you.")
                del kw['id']
                raise redirect(turbogears.url("/"), **kw)

        flash("The article has been deleted.")
        del kw['id']
        raise redirect(turbogears.url("/"), **kw)

    @expose()
    def search(self, **kw):
        params = {}
        if 'year' in kw and kw['year'] != "":
            params['year'] = kw['year']
        if 'month' in kw and kw['month'] != "":
            params['month'] = kw['month']
        if 'day' in kw and kw['day'] != "":
            params['day'] = kw['day']

        if 'id' in kw and kw['id'] != "":
            params['id'] = kw['id']

        if 'author' in kw and kw['author'] != "":
            params['author'] = kw['author']

        if 'logkey' in kw and kw['logkey'] != "":
            params['logkey'] = kw['logkey']

        raise redirect(turbogears.url("/"), **params)

    def upload(self, upfile, articleid, ext=0, extname=""):
        ''' if 'ext' is 1, upfile is a strings. '''
        if ext is 0:
            data = upfile.file.read()
            ept = int(time.time())
            on_fs_name = str(ept) + "_" + upfile.filename
            abspath = os.path.join(os.getcwd(), STORED, on_fs_name)
            f = open(abspath, 'w')
            f.write(data)
            f.close()
            try:
                Attached(name=upfile.filename, onfsname=on_fs_name, article=articleid)
            except:
                pass
        else:
            if extname == "":
                extname = "unnamed"
            try:
                Attached(name=extname, onfsname=upfile, article=articleid)
            except:
                pass
        return

    @expose()
    def download(self, **kw):
        if not 'filename' in kw:
            raise redirect(turbogears.url("/"))

        try:
            uf = Attached.byOnfsname(str(kw['filename']))
        except:
            raise redirect(turbogears.url("/"))

        abspath = os.path.join(os.getcwd(), STORED, uf.onfsname)
        if os.path.exists(abspath) is False:
           flash("Sorry, this file has been deleted.")
           raise redirect(turbogears.url("/default"))

        return cherrypy.lib.cptools.serveFile(path=abspath, disposition="attached", name=uf.onfsname)

    @expose()
    def deletefile(self, **kw):
        if not 'filename' in kw:
            raise redirect(turbogears.url("/uplist"))
        if not 'user' in cherrypy.session or not 'privilege' in cherrypy.session:
            flash("This operation is not permitted to you.")
            raise redirect(turbogears.url("/uplist"))

        try:
            uf = Attached.byOnfsname(str(kw['filename']))
            smartname = uf.name
        except:
            raise redirect(turbogears.url("/uplist"))

        if superuser() or \
           (uf.article != None and cherrypy.session['user'] == uf.article.author):
            abspath = os.path.join(os.getcwd(), STORED, uf.onfsname)
            try:
                os.unlink(abspath)
            except OSError:
                # This path expect the file had been already removed.
                pass
            Attached.delete(uf.id)
        else:
            flash("This operation is not permitted to you.")
            raise redirect(turbogears.url("/uplist"))

        flash('File "%s" has been deleted.' % smartname)
        raise redirect(turbogears.url("/uplist"))

    @expose()
    def deltb(self, **kw):
        if not 'id' in kw:
            raise redirect("/")
        else:
            if 'user' in cherrypy.session and 'privilege' in cherrypy.session:
                author=cherrypy.session['user']
            else:
                flash("This operation is not permitted to you.")
                del kw['id']
                raise redirect(turbogears.url("/"), **kw)
        
        tb = Trackback.get(kw['id'])
        if superuser() or tb.article.author == cherrypy.session['user']:
            tb.destroySelf()
        else:
            flash("This operation is not permitted to you.")
            del kw['id']
            raise redirect(turbogears.url("/"), **kw)

        flash("The trackback has been deleted.")
        del kw['id']
        raise redirect(turbogears.url("/"), **kw)

