# Scan system

## Requirements

- Python 3.9
  - Windows10 (if using .bat files to setup and run)
  - conda (Anaconda or Miniconda)
- SR830 (Lock-in amplifier; Stanford Research Systems)
- Mark202 (stage controller; Sigma-Koki)

## Set up

.env ファイルの中にロックインアンプとステージの GPIB アドレスを記入する。.env ファイルが無ければルートディレクトリに作成する。

.env

```
SR830_GPIB_ADDRESS=10
MARK202_GPIB_ADDRESS=12
```

Windows の場合は、`setup.bat` ファイルをダブルクリックして実行する。このとき、`conda`コマンドが使える必要があるので事前に Anaconda か Miniconda をインストールしておく。

## Run program

Windows の場合には `run.bat`をダブルクリックして実行する。
