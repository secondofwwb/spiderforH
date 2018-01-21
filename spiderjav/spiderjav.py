from bs4 import BeautifulSoup
import requests,shutil,re,os,time
from threading import Thread
import multiprocessing
import chardet

get_in_url = 'http://www.j17v.com/cn/'  #找片站
get_magnet_url = 'http://www.diaosisou.org/list/'  #下片站


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}




#获取每个页面的url,返回一个url list
def get_page_url(weburl,page_num):
    params_list = []
    payload = {'page': page_num, 'mode': ''}
    url = weburl + 'vl_bestrated.php'    #高评分页面参数
    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    dump_list = soup.find_all(class_='video')
    for item in dump_list:
        params_list.append(item.get('id')[4:])
    return params_list


#获取页面信息保存至相关文件
def get_imfor(weburl, params_lists):
    file_path = os.getcwd()
    for item in params_lists:
        payload = {'v': item}
        # try:
        print('尝试打开'+item+'网页')
        r = requests.get(weburl, params=payload)
        if r.status_code != 404:
            soup = BeautifulSoup(r.text, 'html.parser')
            av_img_url = soup.find(id='video_jacket_img').get('src')  # 获取封面图片地址
            av_name = soup.find(class_='post-title text').find('a').get_text()  # 片名
            av_id = soup.find(id='video_id').find(class_='text').get_text()  # 番号
            av_star = soup.find(id='video_review').find(class_='score').get_text()  # 评价星数
            av_genre_list = soup.find(id='video_genres').find_all(text=re.compile('[\u4e00-\u9fa5]'))[1:]  # 标签列表 提取中文
            av_actor = soup.find(id='video_cast').find(rel='tag').get_text()  # 演员

            line = av_id + ',' + av_name + ',' + av_actor + ',' + av_star.strip('()') + ',' + ''.join(map(str, av_genre_list)) + '\n'
            av_img = requests.get('http:' + av_img_url, stream=True)
            print(av_img.status_code,av_img_url)
            if av_img.status_code != 404:
                os.mkdir(av_id)
                path = file_path + '/' + av_id + '/'
                with open(path + av_id + '.jpg', 'wb') as out_file:
                    shutil.copyfileobj(av_img.raw, out_file)
                get_magnet(av_id, path)
                print(av_id + '已保存')
            else:
                print('图片404')
            with open('list.log', 'a') as f:
                f.write(line)
        else:
            print('网页404')
            continue

# 获取种子
def get_magnet(av_name,path):
    url = get_magnet_url + av_name + '/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup_url = soup.find(class_='mlist')
    magnet_url = re.findall('\"magnet:\?xt=urn:btih:[a-z0-9]+', str(soup_url))
    name = soup.find_all(class_='BotInfo')
    for (item, url) in zip(name, magnet_url):
        text = item.get_text(strip=True).replace(u'\xa0', '')
        text.replace(' ', '')
        url = url[1:]
        with open(path + av_name+'.log', 'a') as f:
            print(text,url)
            f.write('%s ,%s\n' % (text, url))
    print(av_name+'链接下载完')


if __name__ == '__main__':
    p = multiprocessing.Pool(4)
    with open('list.log', 'w') as f:
        f.write('番号,名称,演员,评分,类别\n')
    for page_num in range(1, 26):
        params_lists = get_page_url(get_in_url, page_num)
        p.apply_async(get_imfor, args=(get_in_url, params_lists))
    p.close()
    p.join()
    print('done')





