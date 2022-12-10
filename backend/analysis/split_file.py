from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

# https://github.com/deezer/spleeter/wiki/4.-API-Reference#separator

def split_file(n_stem, file_name):
    """
    n_stem: 分割するstem数
        2: ボーカルとそれ以外
        4: ボーカル・ドラム・ベース・それ以外
        5: ボーカル・ドラム・ピアノ・ベース・それ以外
    入力された数に応じてファイルをスプリットする
    """

    # 分離対象
    input_audio = './uploads/' + file_name

    # 指定されたstem数で分割
    separator = Separator('spleeter:' + str(n_stem) + 'stems')

    # ファイル出力
    # 冗長なので，そのまま解析するのもあり
    separator.separate_to_file(input_audio, './outputs/'+ str(n_stem))


if __name__ == '__main__':
    file_name = 'cicago_B.mp3'
    split_file(5, file_name)