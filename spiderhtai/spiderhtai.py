from bs4 import BeautifulSoup
import requests,shutil,re,os,time
from threading import Thread
import multiprocessing




# 获取图片链接,web_src为网页地址
def get_img_src(web_src):
    try:
        r = requests.get(web_src)
        soup = BeautifulSoup(r.text, "html.parser")
        img_src = soup.find_all(id='thumbnail')[0].get('src')
        img_title = soup.find('title').get_text()
        img_title = re.sub("[<>/\\\\:\"\*\?\|]+", "_", img_title) #去除名字中的特殊符号
        # 通过正则获取每一份内容文件数量
        match = re.findall("option", r.text)
        if match:
            count = int(len(match)/2 - 11)
        else:
            count = 0
            print('没有找到图片')

        img_str_list = [str(m).zfill(3) + '.' for m in range(1, count+1)]   # [001 002 ....]

        img_srcs = [re.sub('/\d{3}\.', '/'+str(num), str(img_src)) for num in img_str_list]  # 替换掉编号

        print(img_srcs)
        # img_srcs = [str(img_src).replace('001.jpg', num) for num in img_str_list]
        img_srcs.append(img_title.replace('\\', '_'))
    except:
        return print('打开主网页时发生错误网页')
    print(img_srcs)
    return img_srcs

# 图片存至文件夹
def save_img(img_src,img_path,imgnum):
    try:
        img = requests.get(img_src, stream=True)
    except:
        return print('图片未response')
    if img.status_code != 404:
        file_path = img_path + 'img' + str(imgnum) + '.png'
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(img.raw, out_file)
        return print('save' + img_path + '/_' + str(imgnum))
    else:
        return print('图片不存在')

# 创建保存图片的文件夹
def creat_img_path(imgname):
    try:
        os.mkdir(imgname)
        img_path = os.getcwd()+'/' + imgname + '/'
    except:
        img_path = os.getcwd() + '/' + imgname + '/'

    return img_path

def save_img_pro(img_src,img_path,imgnum):
    Thread(target=save_img, args=(img_src, img_path, imgnum)).start()


if __name__ == '__main__':
    p = multiprocessing.Pool(4)
    for webnum in range(16296, 16365):    #16253
        web_src = 'https://hcomic.me/manga/' + str(webnum) + '.html'
        img_srcs = get_img_src(web_src)
        print(img_srcs)
        img_title = str(webnum) + img_srcs[-1]
        img_path = creat_img_path(img_title)
        for img_src in img_srcs[:len(img_srcs)-1]:
            imgnum = img_srcs.index(img_src) + 1
            p.apply_async(save_img, args=(img_src, img_path, imgnum))
    p.close()
    p.join()
    print('done')









