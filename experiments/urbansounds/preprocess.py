
import os.path
import math
import shutil
import sys

import librosa
import numpy
import joblib

import urbansound8k
import features

def feature_extract(y, sr, n_mels=32, n_fft=512, hop_length=256):
    mels = librosa.feature.melspectrogram(y, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    log_mels = librosa.core.power_to_db(mels, top_db=80, ref=numpy.max)
    return log_mels


def feature_path(sample, out_folder, augmentation=None):
    path = urbansound8k.sample_path(sample)
    tokens = path.split(os.sep)
    filename = tokens[-1]
    filename = filename.replace('.wav', '.npz')
    out_fold = os.path.join(out_folder, tokens[-2])
    return os.path.join(out_fold, filename)


def settings_id(settings):
    keys = sorted([ k for k in settings.keys() if k != 'feature' ])
    feature = settings['feature']

    settings_str = ','.join([ "{}={}".format(k, str(settings[k])) for k in keys ])
    return feature + ':' + settings_str

def compute_mels(y, settings):
    sr = settings['samplerate']
    from librosa.feature import melspectrogram 
    mels = melspectrogram(y, sr=sr,
                         n_mels=settings['n_mels'],
                         n_fft=settings['n_fft'],
                         hop_length=settings['hop_length'],
                         fmin=settings['fmin'],
                         fmax=settings['fmax'])
    return mels

# SalomonBello2016 experienced that only pitch shifts helped all classes
# Piczak2015 on the used class-dependent time-shift and pitch-shift
# https://github.com/karoldvl/paper-2015-esc-convnet/blob/master/Code/_Datasets/Setup.ipynb
def augment(audio, sr,
            pitch_shift=(-3, 3),
            time_stretch=(0.9, 1.1),):
    
    stretch = numpy.random.uniform(time_stretch[0], time_stretch[1]) 
    pitch = numpy.random.randint(pitch_shift[0], pitch_shift[1])
    aug = librosa.effects.time_stretch(librosa.effects.pitch_shift(audio, sr, pitch), stretch)

    return aug

def precompute(samples, settings, out_dir, n_jobs=8, verbose=1, force=False):
    out_folder = os.path.join(out_dir, settings_id(settings))
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    def compute(inp, outp):
        if os.path.exists(outp) and not force:
            return outp

        sr = sr=settings['samplerate']
        y, sr = librosa.load(inp, sr=sr)
        f = compute_mels(y, settings)
        numpy.savez(outp, f)

        for aug in range(settings['augmentations']):
            f = compute_mels(augment(y, sr=sr), settings)
            p = outp.replace('.npz', '.aug{}.npz'.format(aug))
            numpy.savez(p, f)

        return outp
    
    def job_spec(sample):
        path = urbansound8k.sample_path(sample)
        out_path = feature_path(sample, out_folder)
        # ensure output folder exists
        f = os.path.split(out_path)[0]
        if not os.path.exists(f):
            os.makedirs(f)

        return path, out_path
        
    jobs = [joblib.delayed(compute)(*job_spec(sample)) for _, sample in samples.iterrows()]
    feature_files = joblib.Parallel(n_jobs=n_jobs, verbose=verbose)(jobs)


sbcnn = dict(
    feature='mels',
    samplerate=44100,
    n_mels=30,
    fmin=0,
    fmax=8000,
    n_fft=512,
    hop_length=256,
    augmentations=0,
)

def parse(args):

    import argparse

    parser = argparse.ArgumentParser(description='Preprocess audio into features')

    a = parser.add_argument

    a('--data', dest='data_dir', default='./data',
        help='%(default)s')
    a('--out', dest='out_dir', default='./features',
        help='%(default)s')

    a('--archive', dest='archive_dir', default='',
        help='%(default)s')

    a('--jobs', type=int, default=8,
        help='Number of parallel jobs')

    # Expose feature settings
    for k, v in features.default_settings.items():
        t = int if k != 'feature' else str
        a('--{}'.format(k), type=t, default=v, help='default: %(default)s')

    parsed = parser.parse_args(args)

    return parsed

def main():
    
    args = parse(sys.argv[1:])

    feature_settings = {}
    for k in features.default_settings.keys():
        feature_settings[k] = args.__dict__[k]

    out_dir = args.out_dir
    data_path = args.data_dir
    archive = args.archive_dir

    urbansound8k.default_path = os.path.join(data_path, 'UrbanSound8K')
    urbansound8k.maybe_download_dataset(data_path)

    data = urbansound8k.load_dataset()

    id = settings_id(feature_settings)
    precompute(data, feature_settings, out_dir=out_dir, verbose=2, force=False, n_jobs=args.jobs)
    if archive:
        features_path = os.path.join(out_dir, id)
        archive_path = os.path.join(archive, id)
        print('Archiving as {}.zip'.format(archive_path)) 
        shutil.make_archive(archive_path, 'zip', features_path) 


if __name__ == '__main__':
    main()
