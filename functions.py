import json


def open_json(file) -> list:
    """
    Функция производит чтение данных из .json файла

    :param file: Файл .json, который необходимо прочитать

    :return: Данные из файла .json
    """
    with open(file, encoding="utf-8") as f:
        json_data = json.load(f)

    return json_data


def write_json(file, data) -> None:
    """
    Функция производит запись данных в .json файл

    :param file: Файл .json, в который необходимо записать данные
    :param data: Данные, которые необходимо записать

    :return: None
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def comments_count(posts_data, comments_data) -> list:
    """
    Функция производит подсчет количества комментариев к постам

    :param posts_data: Данные о размещенных на сайте постах из data.json
    :param comments_data: Данные о комментариях ко всем постам из файла comments.json

    :return: Обновленный список post_data с количеством комментариев для каждого поста
    """
    comments_match = []
    for post in posts_data:
        for comment in comments_data:
            if comment["post_id"] == post["pk"]:
                comments_match.append(post["pk"])
            post["comments"] = comments_match.count(post["pk"])

    return posts_data


def string_crop(posts_data) -> list:
    """
    Функция производит сокращение строки до 50 символов

    :param posts_data: Данные о постах, в которых необходимо сократить строку
    :return: Обновленный posts-data
    """
    for post in posts_data:
        post["content"] = post["content"][:50]

    return posts_data


def get_post(posts_data, post_id) -> dict:
    """
    Функция отдает пост, который соответствует определенному идентификатору

    :param posts_data: Данные о размещенных на сайте постах из data.json
    :param post_id: Параметр, соответсвующий идентификатору

    :return: Пост, соответствующий введенному идентификатору
    """
    output_post = {}
    for post in posts_data:
        if post_id == post["pk"]:
            output_post = post

    return output_post


def get_tags(post) -> list:
    tags = []
    text = post["content"].split(" ")
    for word in text:
        if "#" in word:
            tag = word.replace("#", "")
            tags.append(tag)

    return tags
