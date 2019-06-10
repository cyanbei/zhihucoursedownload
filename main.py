import requests
import json
import os
import codecs

"""
下载知乎盐选会员资源，支持私家课、Live下载，即将支持读书下载
"""

class Base(object):
    def setcookie(self):
        '''设置cookie'''
        self.cookie = '_zap=242cfd18-38a0-4797-bb6a-5182f4e77b33; d_c0="AEDoQbB5aQ6PTsONx3RCit7KIltICFPXFTY=|1540376499"; _xsrf=x2AazYI6mTtymh3mMjAilAWlz472dIwB; __gads=ID=ce46cfc8a9772a2a:T=1543237561:S=ALNI_MYZ7iWziEMk4dVWpl1fY-Qg0qqYRA; capsion_ticket="2|1:0|10:1557710315|14:capsion_ticket|44:Y2JlYmZhZWZmNzI3NDBjMWIyNTk3YmY3ZjA5ZDE1MTg=|190684ce84dd9d9f7d22a535dab905fc8e39c438875129a17683c0367c66d93d"; z_c0="2|1:0|10:1557710317|4:z_c0|92:Mi4xTGgxYUFBQUFBQUFBUU9oQnNIbHBEaVlBQUFCZ0FsVk43UlBHWFFCLW9zZXdyU1NRZV9zeWItWU90RmpnU29OWThB|8cb34c292edefd3e9640658a34174433e1b69b12725673c77e0d4fb11b1e4de0"; q_c1=1a884fa247d349b1a8ec5754371a9bcd|1557710392000|1540376500000; __utmv=51854390.100-1|2=registration_date=20140513=1^3=entry_date=20140513=1; tst=h; __utma=51854390.709010318.1558253844.1559572267.1559780681.3; __utmz=51854390.1559780681.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/hot; tgw_l7_route=73af20938a97f63d9b695ad561c4c10c'

    @staticmethod
    def standard(name):
        '''标准化文件及文件夹的命名'''
        nm = name.replace("|", "：").replace(":", "：").replace("?", "？").replace("/", "").replace("\\", "").replace("*", "")
        nm = nm.replace("<", "《").replace(">", "》").replace('"', "“")
        return nm

    @staticmethod
    def html2bbcode(html):
        '''将html转化为bbcode'''
        content = html.replace("<p>", "").replace("</p>", "").replace("<p/>", "")
        content = content.replace("<strong>", "[b]").replace("</strong>", "[/b]")
        content = content.replace("<code>", "").replace("</code>", "")
        content = content.replace("<pre>", "").replace("</pre", "")
        content = content.replace('<img src="', "[img]").replace('" alt="', "[/img]")
        content = content.replace('">', "").replace("<br/>", "")
        content = content.replace("<ul>", "").replace("</ul>", "")
        content = content.replace("<ol>", "").replace("</ol>", "")
        content = content.replace("<li>", "").replace("</li>", "")
        content = content.replace("<figure>", "").replace("</figure>", "")
        content = content.replace('" class="', '[/img]')
        content += "\n"
        return content


class Sijiake(Base):
    def __init__(self, sjkid):
        self.id = sjkid

    def parse(self):
        self.setcookie()
        self.detail = self.getdetail()
        self.playlist = self.getplaylist()
        self.projectname = self.standard(self.detail["title"])
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.videodl()
        print(self.getdescription())

    def getdetail(self):
        url = "https://api.zhihu.com/remix/albums/" + self.id + "/detail"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cookies = self.cookie
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        dt = json.loads(requests.get(url, headers=headers, cookies=jar).content)
        return dt

    def getplaylist(self):
        url = "https://api.zhihu.com/remix/albums/" + self.id + "/playlist"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cookies = self.cookie
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        pl = json.loads(requests.get(url, headers=headers, cookies=jar).content)
        return pl

    def videodl(self):
        #设置清晰度
        resl = "hd"
        resl_list = ["sd", "ld", "hd", "fhd"]
        resl_li = []
        for resl_ind in resl_list:
            if resl_ind in self.playlist["album_video_chapters"][0]["videos"][0]["playlist_info"]:
               resl_li.append(resl_ind)
        print("可下载的清晰度有：" + str(resl_li))
        des_resl = input("请输入要下载的清晰度，默认hd")
        if des_resl != "":
            resl = des_resl
        for chapter in self.playlist["album_video_chapters"]:
            chapname = self.standard("第%d章 %s" % (chapter["chapter_index"], chapter["title"]))
            for segment in chapter["videos"]:
                segmentname = self.standard("%02d %s.mp4" % (segment["video_index"], segment["title"]))
                segmenturl = segment["playlist_info"][resl]["url"]
                if os.path.exists("%s/%s/%s" % (self.projectname, chapname, segmentname)):
                    print("%s 分片已存在！" % segmentname)
                    continue
                print("-" * 50)
                print("开始下载%s" % segmentname)
                print("aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (self.projectname + "/" + chapname, segmentname, segmenturl))
                os.system(
                    "aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (self.projectname + "/" + chapname, segmentname, segmenturl))
        print("-" * 50)
        print("下载完成。")

    def getdescription(self):
        authors = ""
        for author in self.detail["authors"]:
            authors += "[img]" + author["user"]["avatar_url"].replace("_r", "") + "[/img]\n" #头像
            authors += "[b][size=4]主讲人：" + author["user"]["name"] + "[/size][/b]\n"
            if len(author["user"]["badge"]) > 0:
                authors += "主讲人头衔：" + author["user"]["badge"][0]["description"] + "\n"
            authors += "主讲人简介：" + author["career"] +"\n"

        briefdes = "[b][size=4]课程简介[/size][/b]\n"
        content = self.html2bbcode(self.detail["description"]["content"])
        briefdes += content
        return (authors + "\n" + briefdes)

    def writedesc(self):
        content = self.getdescription()
        with codecs.open(("%s.txt" % self.projectname), "a+", "utf-8") as f:
            f.write(content)


class ASijiake(Sijiake):
    def parse(self):
        self.setcookie()
        self.detail = self.getdetail()
        self.playlist = self.getplaylist()
        self.projectname = self.standard(self.detail["title"])
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.audiodl()
        print(self.getdescription())

    def audiodl(self):
        for track in self.playlist["tracks"]:
            segmentname = self.standard("%02d %s.mp3" % (track["index"], track["title"]))
            segmenturl = track["audio"]["url"]
            if os.path.exists("%s/%s" % (self.projectname, segmentname)):
                print("%s 分片已存在！" % segmentname)
                continue
            print("-" * 50)
            print("开始下载%s" % segmentname)
            print("aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (
            self.projectname, segmentname, segmenturl))
            os.system(
                "aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (
                self.projectname, segmentname, segmenturl))
        print("-" * 50)
        print("下载完成。")


class ALive(Base):
    def __init__(self, liveid):
        self.id = liveid

    def parse(self):
        self.setcookie()
        self.content = self.getlive()
        self.outline = self.getoutline()
        self.projectname = self.standard(self.content["subject"])
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.alivedl()
        print(self.getdescription())

    def getlive(self):
        url = "https://api.zhihu.com/nlives/lives/" + self.id + "/play_info"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cookies = self.cookie
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        lv = json.loads(requests.get(url, headers=headers, cookies = jar).content)
        return lv

    def getoutline(self):
        url = "https://api.zhihu.com/lives/" + self.id
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cookies = self.cookie
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        ol = json.loads(requests.get(url, headers=headers, cookies=jar).content)
        return ol

    def alivedl(self):
        segmentname = self.standard("%s.mp3" % self.projectname)
        segmenturl = self.content["audio"]["full"][0]["url"]
        print("-" * 50)
        print("开始下载%s" % segmentname)
        print("aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (
        self.projectname, segmentname, segmenturl))
        os.system(
            "aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (
            self.projectname, segmentname, segmenturl))
        print("-" * 50)
        print("下载完成。")

    def getdescription(self):
        authors = ""
        authors += "[img]" + self.content["speaker"]["member"]["avatar_url"].replace("_r", "") + "[/img]\n"  # 头像
        authors += "[b][size=4]主讲人：" + self.content["speaker"]["member"]["name"] + "[/size][/b]\n"
        authors += "主讲人简介：" + self.content["speaker"]["description"] + "\n"

        briefdes = "[b][size=4]Live讲座简介[/size][/b]\n"
        content = self.outline["description_html"] + "\n\n" + "[b][size=4]内容大纲[/size][/b]\n" + self.outline["outline"]
        content = self.html2bbcode(content)
        briefdes += content

        chapters ="[b][size=4]章节信息[/size][/b]\n序号\t章节标题\t开始时间\t结束时间\t历时\n"
        for chapter in self.content["chapters"]:
            #开始时间
            start_time = int(chapter["starts_at"]/1000)
            stime = self.seconds2time(start_time)
            end_time = int(chapter["ends_at"]/1000)
            etime = self.seconds2time(end_time)
            dura_time = int(chapter["duration"]/1000)
            dtime = self.seconds2time(dura_time)
            chapters += ("%02d\t%s\t%s\t%s\t%s" % (chapter["idx"], chapter["title"], stime, etime, dtime)) + "\n"

        slides = "[b][size=4]幻灯片[/size][/b]\n"
        for slide in self.content["slides"]:
            slides += ("[img]" + slide["artwork"] + "[/img]\n").replace("_r", "")

        return (authors + "\n" + briefdes + "\n" + chapters + "\n" + slides)

    def seconds2time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return ("%d:%02d:%02d" % (h, m, s))

    def writedesc(self):
        content = self.getdescription()
        with codecs.open(("%s.txt" % self.projectname), "a+", "utf-8") as f:
            f.write(content)


class Live(Base):
    def __init__(self, liveid):
        self.id = liveid

    def parse(self):
        self.setcookie()
        self.outline = self.getoutline()
        self.projectname = self.standard(self.outline["subject"])
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.livedl()
        self.getdescription()

    def getoutline(self):
        url = "https://api.zhihu.com/lives/" + self.id
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cookies = self.cookie
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        ol = json.loads(requests.get(url, headers=headers, cookies=jar).content)
        return ol

    def livedl(self):
        segmentname = self.standard("%s.mp4" % self.projectname)
        segmenturl = self.outline["video"]["formal_video_tape"]["hls_video_url"]
        print("-" * 50)
        print("开始下载%s" % segmentname)
        """
        这里有问题
        ff = input("是否调用N_m3u8DL-CLI下载文件？（不调用输入N）")
        if ff == "N":
            print("视频下载地址为：%s\n视频名称为：%s\n请使用m3u8下载器下载。" % (segmenturl, segmentname))
        else:
            os.system('N_m3u8DL-CLI_v1.5.1.exe "%s" --workDir "%s" --saveName "%s" --startIndex 0' % (segmenturl, self.projectname, segmentname))
        """
        #暂时下载m3u8然后拖入N_m3u8DL-CLI_v1.5.1
        print("视频下载地址为：%s\n视频名称为：%s\n请使用m3u8下载器下载。" % (segmenturl, segmentname))
        #print("m3u8文件下载完成。")
        print("-" * 50)

    def getdescription(self):
        authors = ""
        authors += "[img]" + self.outline["speaker"]["member"]["avatar_url"].replace("_r", "") + "[/img]\n"  # 头像
        authors += "[b][size=4]主讲人：" + self.outline["speaker"]["member"]["name"] + "[/size][/b]\n"
        authors += "主讲人简介：" + self.outline["speaker"]["description"] + "\n"

        briefdes = "[b][size=4]Live讲座简介[/size][/b]\n"
        content = self.outline["description_html"] + "\n" + "[b][size=4]内容大纲[/size][/b]\n" + self.outline["outline"]
        content = self.html2bbcode(content)
        briefdes += content

        return (authors + "\n" + briefdes)

    def writedesc(self):
        content = self.getdescription()
        with codecs.open(("%s.txt" % self.projectname), "a+", "utf-8") as f:
            f.write(content)

class billboard(Base):
    def __init__(self, typ, cat, page, rows):
        super().setcookie()
        self.typ = typ
        self.cat = cat
        self.page = page
        self.rows = rows

    def show(self):
        self.li = self.list()
        print("-" * 25 + "读取列表中" + "-" * 25)
        index = 0
        while index < self.rows:
            print("%02d\t%s\t%s\t%s\t%s" % (index, self.li["data"][index]["title"],self.li["data"][index]["media_type"],
                                           self.li["data"][index]["chapter_text"], self.li["data"][index]["duration_text"]))
            index += 1
        self.handle()

    def handle(self):
        mode = input("请选择功能:\n1.批量下载本页内容\n2.查看下一页\n3.查看上一页\n")
        if mode == "1":
            mmission = input("请输入要下载的课程序号，用:分隔，如（0:49）\n")
            mmissions, mmissione = mmission.split(":")
            self.massmission(int(mmissions), int(mmissione))
        elif mode == "2":
            albums = billboard(self.typ, self.cat, self.page + 1, self.rows)
            albums.show()
        elif mode == "3":
            if self.page == 1:
                print("已经是第一页，无法查看前一页！")
                self.handle()
            else:
                albums = billboard(self.typ, self.cat, self.page - 1, self.rows)
                albums.show()

    def list(self):
        url = "https://api.zhihu.com/market/categories/all"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        params = {
            'study_type': self.typ,
            'level': 2,
            'dataType': 'new',
            'right_type': '',
            'limit': self.rows,
            'sort_type': self.cat,
            'offset': (self.rows * (self.page - 1))
        }
        cookies = self.cookie
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        ls = json.loads(requests.get(url, headers=headers, params=params, cookies=jar).content)
        return ls

    def massmission(self, start ,end):
        i = start
        while i <= end:
            if self.li["data"][i]["media_type"] == "audio" and self.typ == "album":
                task = ASijiake(self.li["data"][i]["business_id"])
                task.parse()
                task.writedesc()
            elif self.li["data"][i]["media_type"] == "video" and self.typ == "album":
                task = Sijiake(self.li["data"][i]["business_id"])
                task.parse()
                task.writedesc()
            if self.li["data"][i]["media_type"] == "audio" and self.typ == "Live":
                task = ALive(self.li["data"][i]["business_id"])
                task.parse()
                task.writedesc()
            elif self.li["data"][i]["media_type"] == "video" and self.typ == "Live":
                task = Live(self.li["data"][i]["business_id"])
                task.parse()
                task.writedesc()
            else:
                print("第%02d个任务处理失败。" % i)
            i += 1

def entrance():
    zhihu = input("请输入需要下载的知乎资源类型:\n1.知乎私家课\n2.知乎Live\n3.知乎讲书\n")
    if zhihu == "1":
        coursetype = "album"
        dlmethod = input("请选择下载方式\n1.通过列表下载\n2.通过课程id下载\n")
        if dlmethod == "1":
            cate = input("请输入列表排序方式：\n1.按最新发布排序\n2.按最多人感兴趣排序\n")
            if cate == "1":
                albums = billboard(coursetype, "newest", 1 ,50)
                albums.show()
            elif cate == "2":
                albums = billboard(coursetype, "interest", 1, 50)
                albums.show()
        if dlmethod == "2":
            idtype = input("请输入需要下载的私家课id类型：\n1.视频私家课\n2.音频私家课\n")
            if idtype == "1":
                sjkid = input("请输入要进行下载的知乎视频私家课id:")
                task = Sijiake(sjkid)
                task.parse()
            if idtype == "2":
                sjkid = input("请输入要进行下载的知乎音频私家课id:")
                task = ASijiake(sjkid)
                task.parse()
    elif zhihu == "2":
        coursetype = "Live"
        dlmethod = input("请选择下载方式\n1.通过列表下载\n2.通过课程id下载\n")
        if dlmethod == "1":
            cate = input("请输入列表排序方式：\n1.按最新发布排序\n2.按最多人感兴趣排序\n")
            if cate == "1":
                albums = billboard(coursetype, "newest", 1, 50)
                albums.show()
            elif cate == "2":
                albums = billboard(coursetype, "interest", 1, 50)
                albums.show()
        if dlmethod == "2":
            idtype = input("请输入需要下载的Live id类型：\n1.视频Live\n2.音频Liven")
            if idtype == "1":
                liveid = input("请输入要进行下载的知乎视频Live id:")
                task = Live(liveid)
                task.parse()
            if idtype == "2":
                liveid = input("请输入要进行下载的知乎音频Liveid:")
                task = ALive(liveid)
                task.parse()
    elif zhihu == "3":
         # TODO 知乎讲书下载
        pass
    if zhihu == "4":
        # TODO 知乎电子书有drm，暂未找到解密方法
        pass

if __name__ == "__main__":
    entrance()
