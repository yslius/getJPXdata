import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import config


def print_write_log(str_disp):
    print_log = "{} {}".format(
        datetime.now().strftime("%H:%M:%S"), str_disp)
    print(print_log)
    path_logfile = "log/{}_{}.log".format(
        config.NAME_LOGFILE, datetime.now().strftime("%Y%m%d"))
    with open(path_logfile, "a+") as file_object:
        file_object.writelines(print_log + "\n")


def get_jpx_data001():
    try:
        print_write_log("Start get_jpx_data001")

        # ページを開く
        print_write_log("get_kyuyokaitori_data001 open page")
        req = requests.get(config.URL_BASE + config.URL_TARG)
        req.raise_for_status()
        print_write_log("req.status_code:{}".format(req.status_code))

        # 読み取りやすくする
        req.encoding = req.apparent_encoding
        soup = BeautifulSoup(req.text, "lxml")

        # 要素の取得
        ele_div = soup.find("div", attrs={"class": "component-file"})
        ele_th = ele_div.find("th")

        # 年月の取得
        str_yearmonth = ele_th.text
        str_yearmonth = str_yearmonth[str_yearmonth.find("（") + 1:]
        str_yearmonth = str_yearmonth[:str_yearmonth.find("）")]
        print_write_log("str_yearmonth:{}".format(str_yearmonth))

        # フォルダチェック
        if not os.path.isdir("{}/{}".format(config.PATH_BASE, str_yearmonth)):
            os.mkdir("{}/{}".format(config.PATH_BASE, str_yearmonth))
            print_write_log("os.mkdir(str_date_targ)")
        else:
            print_write_log("Error 既にダウンロード済です")
            return

        # リンクの取得
        ele_a = ele_div.find("a")
        print_write_log("link:{}".format(ele_a.attrs["href"]))
        if ele_a.attrs["href"][-4:] != ".xls":
            print_write_log("Error リンクが正しくありません")
            return

        # ダウンロードファイル名
        str_filename = ele_a.attrs["href"]
        str_filename = str_filename[str_filename.rfind("/") + 1:]

        # ダウンロード実行
        url_data = requests.get(config.URL_BASE + ele_a.attrs["href"]).content
        with open("{}/{}/{}".format(config.PATH_BASE, str_yearmonth, str_filename), mode='wb') as f:
            f.write(url_data)
        print_write_log(
            "Download OK {}/{}/{}".format(config.PATH_BASE, str_yearmonth, str_filename))

    except Exception as e:
        print_write_log("Erorr {}".format(e))

    print_write_log("End get_jpx_data001")


if __name__ == '__main__':

    # ログフォルダを作る
    if not os.path.isdir("./log"):
        os.mkdir("./log")
    get_jpx_data001()
