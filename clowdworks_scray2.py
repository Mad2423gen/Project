"""
CloudworksスクレイピングツールVer.2

"""

import csv
import os
import time
from pprint import pprint
import datetime
import sub_func2 as sf


# full_project
def mainfunc():
    # csv_file2 があれば差分取得、無ければ初期化
    #     サムネイル取得 → 差分で条件分岐 → 差分があれば通知及びcsv保存

    # csvあり
    if os.path.isfile(csv_file2):
        clowdworks2 = sf.UrlAndScray(target_url_file)

        # サムネイル取得
        thumbnail_list = clowdworks2.thumbnail_scray()

        # 差分取得 thumb_list と csv_file2 の差分を取得、csv追記
        #   thumb_list の要素は、id, url、 idで比較するメソッド、増分id,URLが返る
        update = sf.differential_extraction2(thumbnail_list, csv_file2)

        # 差分があればメインページ取得しメッセージ送信
        if update:
            # メインページ取得用のURLリスト作成
            new_list = []
            [new_list.append(low[1]) for low in update]
            # メインページ取得
            mainpage_list = clowdworks2.mainpage_scray(new_list)
            # 通知メッセージ送信
            sf.send_pushbullet(mainpage_list)
        else:
            print('No update')

    # csvなし
    else:
        print('No csv file, initialized')
        clowdworks2 = sf.UrlAndScray(target_url_file)
        # サムネイル取得
        thumbnail_list = clowdworks2.thumbnail_scray()

        # csv_file2 に thumbnail_list を追記
        with open(csv_file2, 'a', encoding='utf-8', newline='') as af:
            csv.writer(af).writerows(thumbnail_list)
        print('INITIALIZATION_AND_COMPLETION_OF_ALL_PROCESSES')


if __name__ == '__main__':
    # path entry---------------------------------------
    path = os.getcwd()
    csv_file2 = 'joblist_cw2.csv'
    target_url_file = 'clowdworks_url'
    # -------------------------------------------------

    # 待機時間
    wait_time = 180

    # 動作テスト 0:動作テスト 1:本番
    mode = 1

    # ツールの開始直後は初期化する　以降処理ループする
    if mode == 0:
        pass
    else:
        os.path.isfile(csv_file2) or os.remove(csv_file2)

    while True:
        now = datetime.datetime.now()
        dt = now.strftime('\n%Y/%m/%d %H:%M:%S')
        print(dt)
        mainfunc()
        print('\ntime waite')
        time.sleep(int(wait_time))
