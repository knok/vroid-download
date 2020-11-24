# vroid download

voiceroid 立ち絵wikiから画像を取得
(サムネイル画像のみ、zipは扱わない)

## HTMLの取得

`python get_vroid_html.py`

## サムネイルの取得

`python get_images.py`

## 顔画像領域を認識

`python face-cut-raw.py`

faces/ 以下にファイルが生成される。

### lbpcascade_animeface.xml が必要

`wget https://raw.githubusercontent.com/nagadomi/lbpcascade_animeface/master/lbpcascade_animeface.xml`
等で取得。

詳細は[nagadomi/lbpcascade_animeface: A Face detector for anime/manga using OpenCV](https://github.com/nagadomi/lbpcascade_animeface)を参照。

## 64x64にリサイズ

`./resize.sh`

fixed/ 以下にファイルが生成される。

## 利用

[Lightweight GAN](https://github.com/lucidrains/lightweight-gan)の例:

`lightweight_gan --data fixed --image-size 64 --aug-prob 0.25`

# ライセンス

[LICENSE](LICENSE)
* GPL 2 or later or MIT
