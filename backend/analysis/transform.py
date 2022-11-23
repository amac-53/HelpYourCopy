import librosa
import librosa.display
import argparse
import pathlib
import numpy as np
import matplotlib.pyplot as plt


def transformation(file, time=None):

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

   # ax = fig.add_subplot()
   img1 = librosa.display.specshow(librosa.amplitude_to_db(cqt_amplitude, ref=np.max), sr=sr, x_axis='time', y_axis='cqt_note')
   plt.colorbar(format='%+2.0f dB')
   plt.title('constant-Q power spectrum')
   # plt.show()
   plt.savefig('./analysis/img/spectrum.png')

   # chromagram
   # detail info2
   fig = plt.figure()
   chroma_cq = librosa.feature.chroma_cqt(y=y, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_chroma=n_chroma, n_octaves=n_octaves)
   # ax = fig.add_subplot()
   librosa.display.specshow(chroma_cq, x_axis='time', y_axis='chroma')
   plt.colorbar()
   plt.title('chromagram')
   # plt.show()
   plt.savefig('./analysis/img/chromagram.png')


   # main
   notes = np.array(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
   note_prob = np.array([np.sum(note_seq) for note_seq in chroma_cq])
   # normalize
   note_prob = note_prob / np.sum(note_prob)
   note_prob = sorted(zip(note_prob, notes), reverse=True)
   note_prob = [{'prob': float(i), 'note': str(j)} for i,j in note_prob]  # numpy dtypes to normal 
   return note_prob


def test():
   file = 'D#m_minus5_7th.wav'
   notes = transformation(file)
   # print(notes)
   # for key in notes: 
   #    print(notes[key])
if __name__ == '__main__':
   test()
