import librosa
import librosa.display
import argparse
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import collections

notes = np.array(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])

def transformation(file, name=''):

   # mp3 or wav
   # offset: where to start(s)
   # duration: how long(s)
   y, sr = librosa.load(file, sr=44100, offset=0)
   y, index = librosa.effects.trim(y)

   # doing constant Q transformation
   hop_length = 512
   window = 'hann'
   bins_per_octave = 12
   n_octaves = 7
   n_bins = bins_per_octave * n_octaves
   cqt = librosa.cqt(y, sr=sr, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_bins=n_bins,
                     bins_per_octave=bins_per_octave, window=window)
   cqt_amplitude = np.abs(cqt)

   # drawing spectrogram
   # detail info1
   n_chroma = 12
   fig = plt.figure()
   img1 = librosa.display.specshow(librosa.amplitude_to_db(cqt_amplitude, ref=np.max), sr=sr, x_axis='time', y_axis='cqt_note')
   plt.colorbar(format='%+2.0f dB')
   plt.title('constant-Q power spectrum')
   plt.savefig('./analysis/img/spectrum_'+ name +'.png')

   # chromagram
   # detail info2
   fig = plt.figure()
   chroma_cq = librosa.feature.chroma_cqt(y=y, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_chroma=n_chroma, n_octaves=n_octaves)
   librosa.display.specshow(chroma_cq, x_axis='time', y_axis='chroma')
   plt.colorbar()
   plt.title('chromagram')
   plt.savefig('./analysis/img/chromagram_'+ name +'.png')

   # main
   note_prob = np.array([np.sum(note_seq) for note_seq in chroma_cq])
   # normalize
   note_prob = note_prob / np.sum(note_prob)
   note_prob = sorted(zip(note_prob, notes), reverse=True)
   note_prob = [{'prob': float(i), 'note': str(j)} for i,j in note_prob]  # numpy dtypes to normal 
   return note_prob



def root(file_name='bass.wav'):
   """
   rootを判定
   ウォーキングベースみたいなのはとりあえず無視する
   """
   # mp3 or wav
   y, sr = librosa.load(file_name, sr=44100, offset=0)
   y, index = librosa.effects.trim(y)

   # ベース音があるかないかを全体の強度から判定
   # 3013, 2700, 2078, 1未満, 0とか
   hop_length = 512
   window = 'hann'
   bins_per_octave = 12
   n_octaves = 7
   n_bins = bins_per_octave * n_octaves
   cqt = librosa.cqt(y, sr=sr, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_bins=n_bins,
                     bins_per_octave=bins_per_octave, window=window)
   cqt_amplitude = np.abs(cqt)
   print(np.sum(cqt_amplitude))
   if 10 > np.sum(cqt_amplitude):
      return False

   # chroma
   n_chroma = 12
   chroma_cq = librosa.feature.chroma_cqt(y=y, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_chroma=n_chroma, n_octaves=n_octaves)
   note_per_time = np.argmax(chroma_cq, axis=0)
   
   tmp_max = 0
   for key, value in collections.Counter(note_per_time).items():
      if value > tmp_max:
         tmp_max = value
         note_candidate = key
   return note_candidate


def others(file_name):
   """
   他の音を判定
   """
   # mp3 or wav
   y, sr = librosa.load(file_name, sr=44100, offset=0)
   y, index = librosa.effects.trim(y)

   # その楽器の音が存在しているかを判定し，なければfalseを返す
   hop_length = 256
   window = 'hann'
   bins_per_octave = 12
   n_octaves = 7
   n_bins = bins_per_octave * n_octaves
   cqt = librosa.cqt(y, sr=sr, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_bins=n_bins,
                     bins_per_octave=bins_per_octave, window=window)
   cqt_amplitude = np.abs(cqt)
   if 10 > np.sum(cqt_amplitude):
      return False

   # constant Q transformation
   hop_length = 256
   n_octaves = 7
   n_chroma = 12
   chroma_cq = librosa.feature.chroma_cqt(y=y, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_chroma=n_chroma, n_octaves=n_octaves)

   # 足きりラインの設定
   # 0.9以上で音がなった判定
   note_prob = np.array([np.sum(note_seq) if np.max(note_seq) > 0.9 else 0 for note_seq in chroma_cq])
   # normalize
   note_prob = note_prob / np.sum(note_prob)
   note_prob = sorted(zip(note_prob, notes), reverse=True)
   note_prob = [{'prob': float(i), 'note': str(j)} for i,j in note_prob]
   return note_prob


def judge_code(n_stem, file_name):

   # ファイル名とパスの取得
   file_name = file_name[:-4]
   file_path = './outputs/' + str(n_stem) + '/' + file_name + '/'

   # rootの判定
   if root(file_path + 'bass.wav'):
      root_note = root(file_path + 'bass.wav')
   else:
      # とりあえず
      # 低い方から探しに行くコードを後で書く
      if others(file_path + 'other.wav'):
         root_note = [i for i, note in enumerate(notes) if note == (others(file_path + 'other.wav')[0]['note'])][0]
      elif others(file_path + 'piano.wav'):
         root_note = [i for i, note in enumerate(notes) if note == (others(file_path + 'piano.wav')[0]['note'])][0]

   other_notes = others(file_path + 'other.wav')
   piano_notes = others(file_path + 'piano.wav')
   # vocal_notes = others(file_path + 'vocals.wav')

   print(other_notes)
   print(piano_notes)
   # print(vocal_notes)

   # コード判定
   
   # 前の残りの音とかの可能性があるからファイルの最初の音は優先度低くする？

   # 複雑なコードは先に推定しておく
   """
   分数aug(ブラックアダー)，分数コード
   """
   # if in piano_notes:
      # 2, 6, 10



   # 他の音と確立がどれだけ離れたらみたいなことも可能
   # othersに3度の音がなければ，ピアノ，ボーカルで判定する
   ans = str(notes[root_note])
   flag = {
      'major': False,
      'minor': False,
      'sus2': False,
      'sus4': False
   }

   # third
   # ギターとかストリング，ピアノ，ボーカルの順に優先していく
   # ボーカルは入れんほうがいいまである vocal_notes
   minor_prob = 0
   major_prob = 0
   for instrument in [other_notes, piano_notes]:

      # 楽器音がなければスキップ
      if instrument == False:
         continue
      
      # 割合が0.1より大きいうちは探す
      i = 0
      while instrument[i]['prob'] > 0.1 and i+1 < len(instrument):
         if notes[(root_note + 2) % 12] == instrument[i]['note']:
            flag['sus2'] = True
         elif notes[(root_note + 3) % 12] == instrument[i]['note']:
            flag['minor'] = True
            minor_prob += instrument[i]['prob']
            # dim
         elif notes[(root_note + 4) % 12] == instrument[i]['note']:
            flag['major'] = True
            major_prob += instrument[i]['prob']
            # aug
         elif notes[(root_note + 5) % 12] == instrument[i]['note']:
            flag['sus4'] = True
         i += 1
   
   print(flag)
   print(major_prob, minor_prob)
   if np.sum(flag.values()) == 1:
      ans += str([key for key, value in flag.items() if value == True][0])
   else:
      if flag['major'] == True and major_prob >= minor_prob:
         ans += 'major'
      elif flag['minor'] == True and major_prob < minor_prob:
         ans += 'minor'
      else:
         # 最終度のフラグも立っていないなら，
         # 1. keyから定める（前後関係で使用している音を使う） or 2. 無理やりギリギリなってそうな音を採用する
         # もし本当に何もないのであれば，パワーコードとする
         print('なんそれ')

   print(ans)


   # 口笛が7thになるケースあり（ボーカルと判定された後の処理を入れたほうがいいのかも．．．あとあとの話）
   # 85%以上とかが1音を占めてたら考慮してもいい形にするか
   transformation(file_path + 'bass.wav', name='bass')
   transformation(file_path + 'other.wav', name='other')
   transformation(file_path + 'piano.wav', name='piano')
   # transformation(file_path + 'vocals.wav', name='vocal')

   return ans

if __name__ == '__main__':
   file_name = 'cicago_B.mp3'
   n_stem = 5
   judge_code(n_stem, file_name)
