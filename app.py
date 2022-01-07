from flask import Flask, request, render_template, redirect
import functions

app = Flask("mini_insta")


@app.route("/")
def main_page():
    posts_data = functions.open_json("data/data.json")
    comments_data = functions.open_json("data/comments.json")
    bookmarks = functions.open_json("data/bookmarks.json")

    posts_data = functions.string_crop(posts_data)
    posts_data = functions.comments_count(posts_data, comments_data)

    bookmarks_quantity = len(bookmarks)

    return render_template("index.html", posts=posts_data, bookmarks_quantity=bookmarks_quantity)


@app.route("/post/<postid>")
def post_page(postid):
    posts_data = functions.open_json("data/data.json")
    comments_data = functions.open_json("data/comments.json")

    postid = int(postid)

    output_post = functions.get_post(posts_data, postid)
    tags = functions.get_tags(output_post)

    output_comments = []
    for comment in comments_data:
        if postid == comment["post_id"]:
            output_comments.append(comment)

    comments_quantity = len(output_comments)

    return render_template("post.html", post=output_post, comments=output_comments, quantity=comments_quantity,
                           tags=tags)


@app.route("/search/")
def search_page():
    posts_data = functions.open_json("data/data.json")
    comments_data = functions.open_json("data/comments.json")

    s = request.args.get("s")
    if s is None:
        return "Введите параметр для поиска"
    s = s.lower()

    match = []
    for post in posts_data:
        if s in post["content"].lower():
            post["content"] = post["content"][:50]
            match.append(post)
    posts = functions.comments_count(match, comments_data)
    if len(match):
        quantity = len(match)
        return render_template("search.html", posts=posts, s=s, quantity=quantity)
    return "Ничего не найдено"


@app.route("/users/<username>")
def user_feed(username):
    posts_data = functions.open_json("data/data.json")
    comments_data = functions.open_json("data/comments.json")

    match = []
    for post in posts_data:
        if username == post["poster_name"]:
            match.append(post)
    posts = functions.string_crop(match)
    posts = functions.comments_count(match, comments_data)
    return render_template("user-feed.html", posts=posts)


@app.route('/tag/<tagname>')
def tag_page(tagname):
    posts_data = functions.open_json("data/data.json")

    tagname = "#" + tagname
    output_posts = []
    for post in posts_data:
        text = post["content"].split(" ")
        if tagname in text:
            output_posts.append(post)

    return render_template("tag.html", output_posts=output_posts, tagname=tagname)


@app.route("/bookmarks/add/<postid>")
def add_bookmark(postid):
    postid = int(postid)
    posts_data = functions.open_json("data/data.json")

    bookmarked_posts = functions.open_json("data/bookmarks.json")
    for bookmark in bookmarked_posts:
        if postid == bookmark["pk"]:
            return redirect("/", code=302)

    for post in posts_data:
        if postid == post["pk"]:
            bookmarked_posts.append(post)

    functions.write_json("data/bookmarks.json", bookmarked_posts)
    return redirect("/", code=302)


@app.route("/bookmarks/remove/<postid>")
def remove_bookmark(postid):
    postid = int(postid)
    bookmarks = functions.open_json("data/bookmarks.json")

    for bookmark in bookmarks:
        if postid == bookmark["pk"]:
            bookmarks.remove(bookmark)

    functions.write_json("data/bookmarks.json", bookmarks)
    return redirect("/", code=302)


@app.route("/bookmarks")
def bookmarks_page():
    bookmarks = functions.open_json("data/bookmarks.json")
    comments_data = functions.open_json("data/comments.json")

    bookmarks = functions.string_crop(bookmarks)
    bookmarks = functions.comments_count(bookmarks, comments_data)

    return render_template("bookmarks.html", bookmarks=bookmarks)


if __name__ == "__main__":
    app.run(debug=True)
