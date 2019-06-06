import requests
import json
import os


class sijiake(object):
    def __init__(self, sjkid):
        self.id = sjkid

    def parse(self):
        self.detail = self.getdetail()
        self.playlist = self.getplaylist()
        self.projectname = self.detail["title"]
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.videodl()
        self.getdescription()

    def getdetail(self):
        url = "https://api.zhihu.com/remix/albums/" + self.id + "/detail"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        dt = json.loads(requests.get(url, headers=headers).content)
        return dt

    def getplaylist(self):
        url = "https://api.zhihu.com/remix/albums/" + self.id + "/playlist"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        pl = json.loads(requests.get(url, headers=headers).content)
        return pl

    def videodl(self):
        #设置清晰度
        resl = "hd"
        des_resl = input("请输入要下载的清晰度，默认hd")
        if des_resl != "":
            resl = des_resl
        for chapter in self.playlist["album_video_chapters"]:
            chapname = "第%d章 %s" % (chapter["chapter_index"], chapter["title"])
            for segment in chapter["videos"]:
                segmentname = ("%02d %s.mp4" % (segment["video_index"], segment["title"])).replace("|", "")
                segmenturl = segment["playlist_info"][resl]["url"]
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

        briefdes = "[b][size=4]课程简介[/size][/b]"
        content = (self.detail["description"]["content"]).replace("<p>", "").replace("</p>", "")
        content = content.replace("<strong>", "[b]").replace("</strong>", "[/b]")
        content = content.replace("<code>", "").replace("</code>", "")
        content = content.replace("<pre>", "").replace("</pre", "")
        content = content.replace('<img src="', "[img]").replace('" alt="', "[/img]")
        content = content.replace('">', "")
        briefdes += content

        print(authors)
        print(briefdes)


class asijiake(sijiake):
    def parse(self):
        self.detail = self.getdetail()
        """
        self.playlist = self.getplaylist()
        self.projectname = self.detail["title"]
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.audiodl()
        """
        self.getdescription()

    def audiodl(self):
        for track in self.playlist["tracks"]:
            segmentname = "%02d %s.mp3" % (track["index"], track["title"])
            segmenturl = track["audio"]["url"]
            print("-" * 50)
            print("开始下载%s" % segmentname)
            print("aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (
            self.projectname, segmentname, segmenturl))
            os.system(
                "aria2c.exe -d \"%s\" -o \"%s\" -s 16 -x 16 \"%s\"" % (
                self.projectname, segmentname, segmenturl))
        print("-" * 50)
        print("下载完成。")


class alive(object):
    def __init__(self, liveid):
        self.id = liveid

    def parse(self):
        self.content = self.getlive()
        self.outline = self.getoutline()
        self.projectname = self.content["subject"]
        if os.path.exists(self.projectname):
            pass
        else:
            os.mkdir(self.projectname)
        self.alivedl()
        self.getdescription()

    def getlive(self):
        url = "https://api.zhihu.com/nlives/lives/" + self.id + "/play_info"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cookies = '_zap=242cfd18-38a0-4797-bb6a-5182f4e77b33; d_c0="AEDoQbB5aQ6PTsONx3RCit7KIltICFPXFTY=|1540376499"; _xsrf=x2AazYI6mTtymh3mMjAilAWlz472dIwB; __gads=ID=ce46cfc8a9772a2a:T=1543237561:S=ALNI_MYZ7iWziEMk4dVWpl1fY-Qg0qqYRA; capsion_ticket="2|1:0|10:1557710315|14:capsion_ticket|44:Y2JlYmZhZWZmNzI3NDBjMWIyNTk3YmY3ZjA5ZDE1MTg=|190684ce84dd9d9f7d22a535dab905fc8e39c438875129a17683c0367c66d93d"; z_c0="2|1:0|10:1557710317|4:z_c0|92:Mi4xTGgxYUFBQUFBQUFBUU9oQnNIbHBEaVlBQUFCZ0FsVk43UlBHWFFCLW9zZXdyU1NRZV9zeWItWU90RmpnU29OWThB|8cb34c292edefd3e9640658a34174433e1b69b12725673c77e0d4fb11b1e4de0"; q_c1=1a884fa247d349b1a8ec5754371a9bcd|1557710392000|1540376500000; __utmv=51854390.100-1|2=registration_date=20140513=1^3=entry_date=20140513=1; tst=h; __utma=51854390.709010318.1558253844.1559572267.1559780681.3; __utmz=51854390.1559780681.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/hot; tgw_l7_route=73af20938a97f63d9b695ad561c4c10c'
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
        ol = json.loads(requests.get(url, headers=headers).content)
        return ol

    def alivedl(self):
        segmentname = "%s.mp3" % self.projectname
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

        briefdes = "[b][size=4]Live讲座简介[/size][/b]"
        content = self.outline["description_html"] + "\n" + "[b][size=4]内容大纲[/size][/b]\n" + self.outline["outline"]
        content = content.replace("<p>", "").replace("</p>", "")
        content = content.replace("<strong>", "[b]").replace("</strong>", "[/b]")
        content = content.replace("<code>", "").replace("</code>", "")
        content = content.replace("<pre>", "").replace("</pre", "")
        content = content.replace('<img src="', "[img]").replace('" alt="', "[/img]")
        content = content.replace('">', "")
        briefdes += content

        chapters ="序号\t章节标题\t开始时间\t结束时间\t历时"
        for chapter in self.content["chapters"]:
            #开始时间
            start_time = int(chapter["starts_at"]/1000)
            stime = self.seconds2time(start_time)
            end_time = int(chapter["ends_at"]/1000)
            etime = self.seconds2time(end_time)
            dura_time = int(chapter["duration"]/1000)
            dtime = self.seconds2time(dura_time)
            chapters += ("%02d\t%s\t%s\t%s\t%s" % (chapter["idx"], chapter["title"], stime, etime, dtime)) + "\n"

        slides = ""
        for slide in self.content["slides"]:
            slides += ("[img]" + slide["artwork"] + "[/img]\n").replace("_r", "")

        print(authors)
        print(briefdes)
        print(chapters)
        print(slides)

    def seconds2time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return ("%d:%02d:%02d" % (h, m, s))


if __name__ == "__main__":
    zhihu = input("请输入需要下载的知乎资源类型:\n1.视频私家课\n2.音频私家课\n3.Live（音频）\n4.电子书\n")
    if zhihu == "1":
        sjkid = input("请输入要进行下载的知乎音频私家课id:")
        task = sijiake(sjkid)
        task.parse()
    if zhihu == "2":
        sjkid = input("请输入要进行下载的知乎音频私家课id:")
        task = asijiake(sjkid)
        task.parse()
    if zhihu == "3":
        liveid = input("请输入要进行下载的知乎音频Liveid:")
        task = alive(liveid)
        task.parse()
    if zhihu == "4":
        #知乎电子书有drm，暂未找到解密方法
        pass
