import csv
from pprint import pprint
import requests
import lxml
from bs4 import BeautifulSoup
import os
import time
from retrying import retry
from pushbullet import Pushbullet


# WEBスクレイピング============================================================================
class UrlAndScray:
    def __init__(self, url_files):
        self.base_url = 'https://crowdworks.jp'
        self.url_files = url_files
        # self.old_list = job_list_csv
        self.thumbnail_list = ()
        self.product_page_datas = ()
        with open(self.url_files, 'r') as uf:
            # urlリスト
            self.urls = uf.readlines()

    # サムネイルページページ取得------------------------------------------------------------
    # csvファイルがない場合はこの関数だけ適用する
    def thumbnail_scray(self):
        print('thumbnail scray now')
        thumbnail_list = []
        for url in self.urls:
            # ページソース 取得 タイムアウト対応
            html = requests.get(url, timeout=(10, 10))
            soup = BeautifulSoup(html.text, 'lxml')
            # サムネイルページのID
            thumbnail_urls_tags = soup.select('h3.item_title > a')
            thumbnail_ids = [thumbnail_url.attrs['href'].split('/')[-1]
                             for thumbnail_url in thumbnail_urls_tags]
            # サムネイルページのURL取得
            thumbnail_urls = [self.base_url + thumbnail_url.attrs['href']
                              for thumbnail_url in thumbnail_urls_tags]
            # 結合(ID+URL)
            thumbnail_list.extend(zip(thumbnail_ids, thumbnail_urls))
        print('thumbnail scray done')
        return thumbnail_list

    # ---------------------------------------------------------------------------------
    # メインページ取得
    def mainpage_scray(self, new_urls):
        print('mainpage scray now')
        product_page_datas = []
        for url in new_urls:
            # ページソース　タイムアウト対応
            html = requests.get(url, timeout=(10, 10))
            res = BeautifulSoup(html.text, 'lxml')
            # main title
            title_tag3 = res.select_one('h1')
            title3 = title_tag3.text.replace('\n', '').replace(' ', '')
            # 応募数
            submission = res.select_one('table.application_status_table > tr > td')
            # 報酬
            reward = res.select_one('tbody.thead_nowrap > tr > td > div')
            # Publication Date (掲載日)
            publication_date = res.select('tbody.thead_nowrap > tr > td')
            # title, submission, reward, publication_date
            product_page_datas.append([title3, submission.text, reward.text, publication_date[2].text, url])

        print('mainpage scray done')
        return product_page_datas
    # ---------------------------------------------------------------------------------


# 差分取得やその他
def differential_extraction2(new_list, csv_file):
    # 旧ファイル取得、なければ新規保存　差分取得スキップ
    # 旧ファイルがあった場合　setで取り出し
    if os.path.isfile(csv_file):
        print('incremental sampling')
        with open(csv_file, 'r', encoding='utf-8') as of:
            old_id_list = set()
            [old_id_list.add(row[0]) for row in csv.reader(of)]

        # 差分比較  増分抽出
        add_msg_and_csv = []
        [add_msg_and_csv.append(low) for low in new_list if not low[0] in old_id_list]

        # csv_file に増分追記
        with open(csv_file, 'a', encoding='utf-8', newline='') as af:
            csv.writer(af).writerows(add_msg_and_csv)
        print('incremental sampling done')
        # 通知メッセージ用
        return add_msg_and_csv

    # 旧ファイルがなかった場合　csv_file に new_list を追記
    else:
        print('No csv file, initialized')
        with open(csv_file, 'a', encoding='utf-8', newline='') as af:
            csv.writer(af).writerows(new_list)
        print('initialized done')
        # 通知メッセージ用
        return ["初回更新・データなし"]


# 新着通知(Pushbullet)======================================================================
def send_pushbullet(msg_list):
    if msg_list:
        print('Send messages via Pushbullet')
        # トークンインポート
        with open('pushbullet_token', 'r', encoding='utf-8_sig') as f:
            pushbullet_token = f.readline()
        pd = Pushbullet(pushbullet_token)

        # 送信
        for MessgeList in msg_list:
            # 第一引数はタイトル、第二引数は本文、第三引数はURL
            msg = f"{MessgeList[0]}\n募集人数：{MessgeList[1]}\n" \
                  f"報酬：{MessgeList[2]}\n掲載日：{MessgeList[3]}\n {MessgeList[4]}"
            push = pd.push_note('Scrayping-tool', msg)
        print('Msg send Completed')


if __name__ == '__main__':
    # path entry---------------------------------------
    base_url = 'https://crowdworks.jp/'
    path = os.getcwd()
    csv_file2 = 'joblist_cw2.csv'
    url_file = 'clowdworks_url'
    # -------------------------------------------------
    pass
