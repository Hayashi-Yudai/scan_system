# Scan system

## Requirements

- Python 3.9.4
- SR830 (Lock-in amplifier; Stanford Research Systems)
- Mark202 (stage controller; Sigma-Koki)

## Set up

.env ファイルの中にロックインアンプとステージの GPIB アドレスを記入する。.env ファイルが無ければルードディレクトリに作成する。

.env

```
SR830_GPIB_ADDRESS=10
MARK202_GPIB_ADDRESS=12
```
