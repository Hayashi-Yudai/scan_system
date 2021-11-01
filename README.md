# Scan system

![Django workflow](https://github.com/Hayashi-Yudai/scan_system/actions/workflows/django.yml/badge.svg)
![MIT](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)

## Requirements

- Windows10 (if using .bat files to setup and run)
- Google Chrome (if using `run.bat` to run program)
- Python 3.9
  - conda (Anaconda or Miniconda)
- SR830 (Lock-in amplifier; Stanford Research Systems)
- Mark202 (stage controller; Sigma-Koki)

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
`adconverter.lib`は[このページ](https://github.com/Hayashi-Yudai/adconverter)からダウンロードする。

Windows の場合は、`setup_system.exe` ファイルをダブルクリックして実行する。このとき、`conda`コマンドが使える必要があるので事前に Anaconda か Miniconda をインストールしておく。

## Run program

Windows の場合には `run.bat`をダブルクリックして実行する。
