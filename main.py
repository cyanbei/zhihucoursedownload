import requests
import json
import os

def parse(url):
    #1.请求获取课程列表json
    headers = {

        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    req = requests.get(url,headers = headers)
    reqj = json.loads(req.content)

    #2.创建下载文件夹
    dirname = input("请输入项目名称：")
    if os.path.exists(dirname):
        pass
    else:
        os.mkdir(dirname)
    '''
    for data in reqj["data"]:
        chapname = "第%d章 %s" % (data["chapter_index"], data["chapter_title"])
        if not os.path.exists(dirname + '/' + chapname):
            os.mkdir(dirname + '/' + chapname)
    '''
    #3.创建下载任务
    resl = ""
    for data in reqj["data"]:
        #4. 显示可选清晰度
        resl_list = data["playlist_info"]
        if "hd" in resl_list:
            print("hd存在")
        if "fhd" in resl_list:
            print("fhd存在")
        if len(resl) == 0:
            resl = input("请选择要下载的清晰度")
        fileurl = resl_list[resl]["url"]
        filename = ("%02d %s.mp4" % (data["index"], data["title"])).replace("|","")
        chapname = "第%d章 %s" % (data["chapter_index"], data["chapter_title"])
        print("开始下载%s" % filename)
        print("aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (dirname + "/" + chapname, filename, fileurl))
        os.system("aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (dirname + "/" + chapname, filename, fileurl))
    print("下载完成。")


if __name__ == "__main__":
    url = input("请输入要进行下载的知乎私家课json地址:")
    parse(url)
