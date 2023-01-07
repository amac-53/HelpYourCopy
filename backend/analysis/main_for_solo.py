import librosa
import librosa.display
import argparse
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import collections


DEBUG = True
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



def bass_root(file_name='bass.wav'):
   """
   rootを判定
   1. ほとんど１音であればそれを採用 (全体の7割以上)
   2. ウォーキングベースであれば，（強く出ている）１音目を採用
   """
   # ハイパーパラメータ
   # ample_thresold 10以下が普通だが，348でミスってるのがある
   ample_thresold = 350
   note_prob_thresold = 0.7

   # mp3 or wav
   y, sr = librosa.load(file_name, sr=44100, offset=0)
   y, _ = librosa.effects.trim(y)

   hop_length = 512
   window = 'hann'
   bins_per_octave = 12
   n_octaves = 4
   n_bins = bins_per_octave * n_octaves
   cqt = librosa.cqt(y, sr=sr, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_bins=n_bins,
                     bins_per_octave=bins_per_octave, window=window)
   cqt_amplitude = np.abs(cqt)

   # 画像（処理移す可能性あり）
   fig = plt.figure()
   librosa.display.specshow(librosa.amplitude_to_db(cqt_amplitude, ref=np.max), sr=sr, x_axis='time', y_axis='cqt_note')
   plt.colorbar(format='%+2.0f dB')
   plt.title('constant-Q power spectrum')
   plt.savefig('./analysis/img/spectrum_bass.png')

   # ベースがあるかどうかを全体の強度から判定
   print(f'bass amp: {np.sum(cqt_amplitude)}')
   if ample_thresold > np.sum(cqt_amplitude):
      return False

   # chroma
   # (12, the number of seconds)
   n_chroma = 12
   chroma_cq = librosa.feature.chroma_cqt(y=y, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_chroma=n_chroma, n_octaves=n_octaves)
   note_per_time = np.argmax(chroma_cq, axis=0)

   # 画像
   fig = plt.figure()
   librosa.display.specshow(chroma_cq, x_axis='time', y_axis='chroma')
   plt.colorbar()
   plt.title('chromagram')
   plt.savefig('./analysis/img/chromagram_bass.png')


   # 最大確率を算出
   n_data = len(chroma_cq[0])
   tmp_max = 0
   for key, value in collections.Counter(note_per_time).items():
      value /=  n_data 
      print(key, value)
      if value > tmp_max:
         tmp_max = value
         note_candidate = key
   
   # 確率が微妙（ウォーキングベース）なら，最初の音を採用
   if tmp_max < note_prob_thresold:
      note_candidate = note_per_time[0]
   
   return note_candidate



def others(file_name):
   """
   ピアノ・他楽器を判定
   """
   # ハイパーパラメータ
   ample_thresold = 10
   note_ratio = 0.6
   note_prob = 0.23

   # mp3 or wav
   y, sr = librosa.load(file_name, sr=44100, offset=0)
   y, _ = librosa.effects.trim(y)

   # cqt
   # (84, the number of time)
   hop_length = 512
   window = 'hann'
   bins_per_octave = 12
   
   if 'piano' in file_name:
      n_octaves = 7
      n_bins = bins_per_octave * n_octaves
      fmin = librosa.note_to_hz('C1')
   else:
      n_octaves = 6
      n_bins = bins_per_octave * n_octaves
      fmin = librosa.note_to_hz('C2')

   cqt = librosa.cqt(y, sr=sr, hop_length=hop_length, fmin=fmin, n_bins=n_bins,
                     bins_per_octave=bins_per_octave, window=window)
   cqt_amplitude = np.abs(cqt)


   # ピアノがあるかどうかを全体の強度から判定
   if ample_thresold > np.sum(cqt_amplitude):
      return False
   
   # constant Q transformation
   # (12, time sequence)
   hop_length = 512
   n_chroma = 12
   chroma_cq = librosa.feature.chroma_cqt(y=y, hop_length=hop_length, fmin=fmin, n_chroma=n_chroma, n_octaves=n_octaves)

   # なっている音を時間ごとに確定
   # cnt > 0.3 でなっていると確定？
   n_time = len(chroma_cq[0])
   cnt = []
   for i, ample_per_note in enumerate(chroma_cq):
      cnt.append(0)
      for ample in ample_per_note:
         if ample > note_ratio:
            cnt[i] += 1
      cnt[i] /= n_time


   # 音として返す
   # note_prob = sorted(zip(cnt, notes), reverse=True)
   # note_prob = [{'prob': float(i), 'note': str(j)} for i,j in note_prob]
   note_likely = [notes[i] for i, prob in enumerate(cnt) if prob > note_prob]

   # なっている順番を決定 (84,)
   cqt_sum_by_time = np.array([np.sum(cqt) for cqt in cqt_amplitude])

   # 相対的に大きい音をしたから拾う
   # ベースはC4(48)までの中からもっとも大きいやつがあればそれにする
   note_max = [0]*12  # 各音の最大値を保持
   for i, note_strength in enumerate(cqt_sum_by_time):

      # 局所最大値を求める
      # 最大の音のうち，条件を満たした順になっている判定
      if i > 0 and i < len(cqt_sum_by_time)-1 and cqt_sum_by_time[i-1] < note_strength and cqt_sum_by_time[i+1] < note_strength:
         if notes[i%12] in note_likely:  # chromaに存在すれば

            # その音のなっている位置を判定
            # その音の最大値の8割以上であればokとする
            if note_max[i%12] < note_strength: 
               note_max[i%12] = note_strength
            
            # if (i%12) not in note_list:
            #    note_list.append(i%12)
            #    print(i, notes[i%12], note_strength)
   

   # なっている順番判定
   note_list = []
   for i, note_strength in enumerate(cqt_sum_by_time):

      # 局所最大値を求める
      # 最大の音のうち，条件を満たした順になっている判定
      if i > 0 and i < len(cqt_sum_by_time)-1 and cqt_sum_by_time[i-1] < note_strength and cqt_sum_by_time[i+1] < note_strength:
         if notes[i%12] in note_likely:  # chromaに存在すれば

            # その音のなっている位置を判定
            # その音の最大値の8割以上であればokとする
            if note_max[i%12] * 0.8 <= note_strength:             
               note_list.append(i%12)
               print(i, notes[i%12], note_strength)
   
   return note_list


def judge_code(n_stem, file_name):
   """
   コードを判定する
   """
   ans = ''

   # ファイル名とパスの取得
   file_name = file_name[:-4]
   file_path = './outputs/' + str(n_stem) + '/' + file_name + '/'

   # まず，音取り
   bass_note = bass_root(file_path + 'bass.wav')
   piano_notes = others(file_path + 'piano.wav')
   other_notes = others(file_path + 'other.wav')

   if DEBUG:
      print(f'bass_note: {bass_note}')
      print(f'piano_notes: {piano_notes}')
      print(f'other_notes: {other_notes}')

   # ルート音の判定
   # ベースがあれば，それを使う
   # なければ，他の楽器から最低音を探す（優先度 piano -> guitarなど）
   if bass_note:
      print('bass')
      root_note = bass_note
   else:
      if piano_notes:
         print('piano')
         root_note = piano_notes[0]
      elif other_notes:
         print('other')
         root_note = other_notes[0]

   ans += notes[root_note]

   # 内声をとっていく
   # 複雑なコードは先に推定しておく
   """
   分数aug(ブラックアダー)，ドミナント的分数コード
   """
   # サブドミナント / ドミナント
   flag = True
   is4over5 = 0
   is27over5 = False

   # ピアノ and その他の音
   relative_num = []
   if piano_notes:
      for note in piano_notes: 
         relative_num.append((note - root_note + 12)%12)
   if other_notes:
      for note in other_notes:
         note = (note - root_note + 12)%12
         if note not in relative_num:
            relative_num.append(note)

   for num in relative_num:
      if num == 10 or num == 2 or num == 5 or num == 0: # rootあってもいい
         is4over5 += 1
      elif num == 7:
         is27over5 = True
      else:
         flag = False
   
   # 分数コード
   if flag == True:
      if is27over5 >= 3 and is27over5:
         ans += '27over5'
         # return '27over5'
      if is27over5 == 3:
         ans += '4over5'
         # return '4over5'


   """
   トライアド
   aug, dim(or flat5th), sus2, M3, m3, sus4
   """ 
   is_major = False
   is_aug = False
   is_minor = False
   is_dim = False
   is_sus = False

   relative_num = []   
   if piano_notes:
      for note in piano_notes: 
         relative_num.append((note - root_note + 12)%12)
      print(f'piano relative num: {relative_num}')
   if other_notes:
      for note in other_notes:
         note = (note - root_note + 12)%12
         if note not in relative_num:
            relative_num.append(note)
      print(f'other relative num: {relative_num}')


   # 3rdを含むか
   # major, minor, aug, dim を判定
   # major かつ minorみたいなものを避けるために，順番を利用
   flag = False
   for note in relative_num:

      # 基準が見つけられれば終わり
      if flag == True:
         break

      if note == 4:
         flag = True

         if 7 in relative_num:
            is_major = True
            ans += ''
         elif 8 in relative_num:
            ans += 'aug'
         else:
            ans += 'omit5'
      elif note == 3:
         flag = True

         if 7 in relative_num:
            is_minor = True
            ans += 'm'
         elif 6 in relative_num:
            is_dim = True
            ans += 'dim'
         else:
            ans += 'omit5'
      elif note == 2:
         flag = True

         is_sus = True
         ans += 'sus2'
      elif note == 5:
         flag = True

         is_sus = True
         ans += 'sus4'
      # 残りの音の判定をどうするか


   """
   テンションノート
   dim, aug, maj, minorごとに判定
   相性を大切に判定
   """
   print(relative_num)

   # dim, aug, 
   if is_dim:
      if 9 in relative_num:
         ans += '7'
      elif 10 in relative_num:
         ans = notes[root_note] + 'm7(-5)'
   elif is_aug:
      pass
   elif is_minor or is_major:
      # 6th
      if 9 in relative_num:
            ans += '6' 
      elif 10 in relative_num:  # M7, 7はどれでもあり

         # sus or それ以外で表記を変える
         if is_sus:
            ans = '7' + ans
         else:
            ans += '7'

            # 9, 11, 13th
            if is_major or is_minor:
               ans += '('
               # 9
               if 1 in relative_num:
                  ans += '-9'
               elif 2 in relative_num:
                  ans += '9'
               elif 3 in relative_num and is_major == True:
                  ans += '+9'

               # 11 or +11
               if is_minor:
                  if 5 in relative_num:
                     ans += '11'
               elif is_major:
                  if 6 in relative_num:
                     ans += '+11'
               
               # 13 or +13
               if 5 in relative_num:
                  ans += '13'    

               # テンションノートがあるか否か
               if ans[-1] == '(':
                  ans = ans[:-1]
               else:
                  ans += ')'
      elif 11 in relative_num:

         # sus or それ以外で表記を変える
         if is_sus:
            ans = 'maj7' + ans
         else:
            ans += 'M7'

            # 9, 11, 13th
            if is_major or is_minor:
               ans += '('
               # 9
               if 1 in relative_num:
                  ans += '-9'
               elif 2 in relative_num:
                  ans += '9'
               elif 3 in relative_num and is_major == True:
                  ans += '+9'

               # 11 or +11
               if is_minor:
                  if 5 in relative_num:
                     ans += '11, '
               elif is_major:
                  if 6 in relative_num:
                     ans += '+11, '
               
               # 13 or +13
               if 5 in relative_num:
                  ans += '13'

               # テンションノートがあるか否か
               if ans[-1] == '(':
                  ans = ans[:-1]
               else:
                  ans += ')'         
      
   if DEBUG == True:
      print(f'root: {root_note}')
      print(f'ans: {ans}')

   transformation(file_path + 'other.wav', name='other')
   transformation(file_path + 'piano.wav', name='piano')

   return ans

if __name__ == '__main__':
   file_name = 'cicago_B.mp3'
   n_stem = 5
   judge_code(n_stem, file_name)
