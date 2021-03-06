# Scan system

![Django workflow](https://github.com/Hayashi-Yudai/scan_system/actions/workflows/django.yml/badge.svg)
![MIT](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)

## Requirements

- Windows10 (if using A/D converter)
- Python 3.10
  - conda (Anaconda or Miniconda)
- SR830 (Lock-in amplifier; Stanford Research Systems)
- Mark202 (stage controller; Sigma-Koki)
- TUSB-0216ADMZ (A/D converter; Turtle industory Co. Ltd.)

## Set up

.env ファイルの中にロックインアンプとステージの GPIB アドレスを記入する。.env ファイルが無ければルートディレクトリに作成する。

.env

```
SR830_GPIB_ADDRESS=10
MARK202_GPIB_ADDRESS=12
DATA_POST_URL=http://localhost:8000/core/rapid-scan-data/
```

A/Dコンバータを制御するためのライブラリを `/core`以下に配置する。
```bash
core
├── TUSB16AD.dll
├── TUSB16AD.lib
└── adconverter.dll
```

`TUSB16AD.dll`と`TUSB16AD.lib`はタートル工業のHPからダウンロード可能。
`adconverter.lib`は[このページ](https://github.com/Hayashi-Yudai/adconverter/releases)からダウンロードする。

Windows の場合は、`setup_system.exe` ファイルをダブルクリックして実行する。このとき、`conda`コマンドが使える必要があるので事前に Anaconda か Miniconda をインストールしておく。

## Run program

Windows の場合には `run.bat`をダブルクリックして実行する。

## Links
- [Install Anaconda](https://www.anaconda.com/products/individual)
- [adconverter](https://github.com/Hayashi-Yudai/adconverter)
- [condaコマンドを使えるようにする](https://qiita.com/momosuke/items/fd6f8f9d01d2f57be90e)
- [タートル工業 - A/Dコンバータ](https://www.turtle-ind.co.jp/products/ad-converters/)


## Credit

本プログラムでは、 [flaskwebgui](https://github.com/ClimenteA/flaskwebgui) のコードを一部改変して用いている。
