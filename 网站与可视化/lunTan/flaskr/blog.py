from flask import Blueprint
from flask import flash
from flask import g, session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username, isOriginal"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    print(posts)
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))


'''
======================================================================
个人帖子列表页面
======================================================================
'''
@bp.route("/essay/self")
@login_required
def selfPage():
    """Show all the posts, most recent first."""
    # 当前用户id
    user = g.user
    userId = user['id']
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id where u.id = {}"
        " ORDER BY created DESC".format(userId)
    ).fetchall()
    return render_template("blog/privateBlog.html", posts=posts)




'''
======================================================================
评论与回复页面
======================================================================
'''

@bp.route("/comment/list")
@login_required
def commentList():
    """Show all the posts, most recent first."""
    # 当前用户id
    # userId = session["user_id"]
    user = g.user
    userId = user['id']
    db = get_db()
    posts = db.execute(
       f"SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/commentList.html", posts=posts)



'''
======================================================================
贴子的详情页面
======================================================================
'''

@bp.route("/content")
@login_required
def content():
    # 当前用户id
    # userId = session["user_id"]
    user = g.user
    userId = user['id']
    if request.method == 'GET':
        # 获取贴子内容
        post_id = request.args.get('id')
        db = get_db()
        essay = db.execute(
           "SELECT p.id, title, body, created, author_id, isOriginal, like_users FROM post p where p.id ={}".format(post_id)
        ).fetchone()
        db.commit()
        # todo 获取评论
        db = get_db()
        commentSql= "select c.content, c.created_at, c.id, p.username from comment c join user p on c.user_id=p.id where c.post_id={} order by c.created_at asc ".format(post_id)
        print(commentSql)
        commentList = db.execute(commentSql).fetchall()
        print(commentList, 'commentlist')

        # 获取点赞情况
        isLike = None
        if essay['like_users']:
            like_users_dict = json.loads(essay['like_users'])
            isLike = like_users_dict.get(userId)
        return render_template("blog/content.html", essay=essay, isLike=isLike, commentList=commentList)
    return redirect(url_for('blog.index'))


@bp.route("/content/comment/add", methods=("POST",'GET'))
@login_required
def commentAdd():
    # 添加评论
    userId = session.get("user_id")
    if request.method == 'POST':
        print(request.form)
        bodyText = request.form.get('body')
        post_id = request.form.get('post_id')
        print(bodyText, post_id)
        if not bodyText:
            error = '评论内容不能为空！'
            flash(error)
        if not post_id:
            flash('当前用户没有权限评论！')
        db = get_db()
        sql = "insert into comment (post_id, user_id, content) VALUES ('{}','{}','{}')".format(post_id, userId, bodyText)
        db.execute(sql)
        db.commit()
        return redirect(url_for('blog.content', id=post_id))
    return redirect(url_for('blog.index'))



    return ''

@bp.route("/content/good/change")
@login_required
def commentGood():
    # 修改点赞状态
    userId = session.get("user_id")
    db = get_db()
    if request.method == 'GET':
        isLike = None
        post_id = request.args.get('id')
        sql = "SELECT p.id, title, body, created, author_id, isOriginal, like_users FROM post p where p.id ={}".format(
                post_id)
        essay = db.execute(sql).fetchone()
        if essay['like_users']:
            like_users_dict = json.loads(essay['like_users'])
            targetUser = like_users_dict.get(str(userId))
            if targetUser:
                like_users_dict[userId] = ''
            else:
                isLike = '1'
                like_users_dict[userId] = '1'
        else:
            isLike = '1'
            like_users_dict = {userId: '1'}
        newLikes = json.dumps(like_users_dict)
        db.execute(
            "update post set like_users='{}' where id={}".format(newLikes,post_id)
        )
        db.commit()
        return redirect(url_for('blog.content', id=post_id))
        # return render_template("blog/content.html", essay=essay, isLike=isLike)
    return redirect(url_for('blog.index'))


@bp.route("/content/share")
@login_required
def commentShare():
    # 转发
    userId = session.get("user_id")
    if request.method == 'GET':
        post_id = request.args.get('id')
        db = get_db()
        sql = "SELECT p.id, title, body, created, author_id, isOriginal, like_users FROM post p where p.id ={}".format(
                post_id)
        targetEssay = db.execute(sql).fetchone()

        sqlTwo = "insert into post (author_id, title, body, isOriginal) values ('{}','{}','{}','{}')".format(
            userId,targetEssay['title'],targetEssay['body'],0)
        db.execute(sqlTwo)
        db.commit()
        flash('转发成功')
        return redirect(url_for('blog.content', id=post_id))

    return redirect(url_for('blog.index'))
