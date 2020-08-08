from pyquery import PyQuery as pq
import json
import requests
import os
from multiprocessing import Pool

# 需要的 node sass 版本
versions = ["v4.14.1", "v4.14.0", "v4.13.1", "v4.13.0"]

URL = "https://github.com/sass/node-sass/releases/tag/"


def req(_url_, version):
    try:
        html = requests.get(_url_).text
        document = pq(html)
        ele_lis = document(
            ".d-flex.flex-justify-between.flex-items-center.py-1.py-md-2.Box-body.px-2")

        for ele in ele_lis:
            e = pq(ele)
            name = e(".pl-2.flex-auto.min-width-0.text-bold").text()
            link = e(".d-flex.flex-items-center.min-width-0").attr('href')

            print("-> ", name, " --- ", link)

            f = "./" + version.replace(".", "_") + "/"

            flag = os.path.exists(f + name)

            if flag:
                print(f + " 已存在！")
            else:
                content = requests.get("https://github.com" + link)
                mkdir(f)
                with open(f + name, "wb") as code:
                    code.write(content.content)
    except ValueError as err:
        print("❌ 出大问题 ", err)


def mkdir(path):
    try:
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
    except IOError:
        print("Error: 文件夹创建失败")


def main(version_item):
    req(URL + version_item, version_item)
    print("------------------------" + version_item +
          "版本下载完毕！------------------------")


if __name__ == "__main__":
    p = Pool(3)
    p.map(main, [item_ver for item_ver in versions])
    print("全部下载完毕！")
