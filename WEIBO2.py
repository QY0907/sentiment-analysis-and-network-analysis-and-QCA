import requests
import csv
import random
import time

# 设置请求头，需要替换Cookie和Referer
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "Cookie": "SINAGLOBAL=8742851900092.377.1720168458737; SCF=ApTA8vlP7EhYTbIWu8-u9WGYaXaQE9bX2XFExs-iXVdKfwYqHeUL5hV8kr4m2TAPDAoyznvZ1zkudP5TlloCj5A.; ALF=1743681155; SUB=_2A25KwpnTDeRhGeFL6VQW9i7MzzmIHXVpoZMbrDV8PUJbkNAYLWPWkW1NQlFIiykdpWQI-EXk8J0spANXhQ7JlJLw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFxsDZMl4D9G0GKPbueHgqX5JpX5KMhUgL.FoMfeoqNSo57Sh-2dJLoIEqLxKBLBonL12BLxKnLBKqL1h2LxKqL1h-L12eLxKqL1h-L12SyIBtt; XSRF-TOKEN=fHKwOe4gKJ3Exnmh6QW1QGMQ; _s_tentry=weibo.com; Apache=1052601511482.4694.1741144718622; ULV=1741144718650:49:5:4:1052601511482.4694.1741144718622:1741089170132; WBPSESS=kKvJ0l1ShLKfwCHl8l3VFmlHY2SL5WqYv9fav_vxycwNaJwiyuvItC_ufw8m0TK6O8OuFjcMnuvJhiqYHX7y9UXur2N7Mw6LPtihXcYgvnHuI0HvzOLU2IYg1vh-V936YILvzC6ncp28W7N9MwmD3g==",
    "Referer": "https://weibo.com/1644114654/JoXw45qNz"
}
url = "https://weibo.com/ajax/statuses/buildComments?"
# 打开文件
f = open("新京报",mode="a",encoding="utf-8-sig",newline="")

# 写入表头，根据实际情况修改列名
writer = csv.writer(f)
writer.writerow(["user","comments","created_at","gender","location"])

# 定义爬取二级评论的第一页的函数的参数
def setFirstParams(id,max_id):
    # 需要替换uid
    """
    :param id: 一级评论的id
    :param max_id: 一级评论的max_id
    :return: 二级评论的参数
    """
    params = {
        "is_reload": "1",
        "id":id,
        "is_show_bulletin": "2",
        "is_mix": "1",
        "fetch_level": "1",
        "max_id": max_id,
        "count": "20",
        "uid": "1644114654",
        "locale": "zh-CN"
    }
    return params

# 定义爬取二级评论的第一页的函数
def crawl2(id, max_id):
    """
    :param id: 一级评论的id
    :param max_id: 一级评论的max_id
    :return: 一级评论的id和max_id
    """
    # 计数
    i = 1
    # 请求数据
    response = requests.get(url=url,params=setFirstParams(id=id,max_id=max_id), headers=headers).json()
    # 获取数据
    data_list = response["data"]
    for data in data_list:
        # 遍历data_list，获取每一条二级评论数据
        user=data["user"]["screen_name"]
        comments = data["text_raw"]
        created_at = data["created_at"]
        gender = data["user"]["gender"]
        location = data["user"]["location"]

        # 写入文件
        writer.writerow([user,comments,created_at,gender,location])
        print(f"本页第{i}条评论已爬取")
        i += 1
        # 获取第一页二级评论的id和max_id
        id = str(data["id"])
        max_id = "max_id=" + str(response["max_id"])
    # 当存在下一页时，递归调用
    if response["max_id"] != 0:
        try:
            time.sleep(random.randint(1,3))
            # 使用crawl3函数爬取二级评论的下一页
            crawl3(id,max_id)
        except Exception as e:
            print(e)
    # 当不存在下一页时，返回第一页二级评论的id和max_id
    return id, max_id

# 定义爬取二级评论的下一页的函数的参数
def setSecondParams(id, max_id):
    """
    :param id: 二级评论的id
    :param max_id: 二级评论的max_id
    :return: 二级评论的参数
    """
    params = {
        "flow": "1",
        "is_reload": "1",
        "id": id,
        "is_show_bulletin": "2",
        "is_mix": "1",
        "fetch_level": "1",
        "max_id": max_id,
        "count": "20",
        "uid": "1644114654",
        "locale": "zh-CN",
    }
    return params

# 定义爬取二级评论的下一页的函数
def crawl3(id, max_id):
    """
    :param id: 二级评论的id
    :param max_id: 二级评论的max_id
    :return: 二级评论的id和max_id
    """
    print("开始爬取二级评论的下一页!")
    # 请求数据
    response = requests.get(url=url,params=setSecondParams(id=id,max_id=max_id), headers=headers).json()
    # 遍历data_list，获取每二级评论数据
    data_list = response["data"]
    for data in data_list:
        # 获取数据
        user = data["user"]["screen_name"]
        comments = data["text_raw"]
        created_at = data["created_at"]
        gender = data["user"]["gender"]
        location = data["user"]["location"]
        # 写入文件
        writer.writerow([user,comments,created_at,gender,location])
        # 获取下一页二级评论的id和max_id
        id = str(data["id"])
        max_id = "max_id=" + str(response["max_id"])

    # 当存在下一页时，递归调用
    if response["max_id"] != 0:
        try:
            time.sleep(random.randint(1,3))
            crawl3(id,max_id)
        except Exception as e:
            print(e)
    return id, max_id

# 定义爬取一级评论的函数，需要替换url并且将链接中的"count=10"替换为"{next}"
def crawl(next = "count=10"):
    """
    :param next: 一级评论的翻页参数，默认为count=10，此后的参数为max_id
    :return: None
    """
    # 页数计数
    global page
    try:
        # 爬取一级评论
        url = f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4559486561294657&is_show_bulletin=2&is_mix=0&{next}&uid=1644114654&fetch_level=0&locale=zh-CN"
        response = requests.get(url=url, headers=headers).json()
        # 遍历data_list，获取每一条一级评论数据
        data_list = response["data"]
        for data in data_list:
            # 获取数据
            user = data["user"]["screen_name"]
            comments = data["text_raw"]
            created_at = data["created_at"]
            gender = data["user"]["gender"]
            location = data["user"]["location"]
            # 写入文件
            writer.writerow([user,comments,created_at,gender,location])
            # 获取下一页一级评论的id和max_id
            id = data["id"]
            max_id = "max_id=" + str(response["max_id"])

            # 如果data中的[total_number]不为0，表明存在二级评论，调用crawl2爬取第一页二级评论
            if data["total_number"] != 0:
            # if len(data["comments"]) != 0:
                try:
                    time.sleep(random.randint(1,3))
                    crawl2(id,max_id)
                except Exception as e:
                    print(e)

        print(f"------第{page}页已爬取！-------")
        page += 1

        # 当未爬取完所有评论时，递归调用
        if response["max_id"] != 0:
            try:
                time.sleep(random.randint(1,3))
                crawl(max_id)
            except Exception as e:
                print(e)
                f.close()
        print("----爬取结束！-----")
        f.close()
    except Exception as e:
        print(e)
        f.close()

if __name__ == '__main__':
    # 页数计数
    page = 1
    # 调用crawl函数
    crawl()