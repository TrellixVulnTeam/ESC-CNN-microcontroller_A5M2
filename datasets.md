# Datasets

Audio Classification datasets that are useful for practical tasks
that can be perform on microcontrollers and small embedded systems.

Relevant tasks:

* Wakeword detection
* Keyword spotting
* Speech Command Recognition
* Noise source identification
* Smart home event detection. Firealarm,babycry etc 

Not so relevant:

* (general) Automatic Speech Recognition
* Speaker recognition/identification

## To be reviewed.


* DCASE 2013. Audio Event Detection. Indoor office sounds. 16 classes. Segmented. 19 minutes total.
* DCASE 2016.


## Not relevant 

* [NOIZEUS: A noisy speech corpus for evaluation of speech enhancement algorithms](http://ecs.utdallas.edu/loizou/speech/noizeus/)
30 sentences corrupted by 8 real-world noises. 
* [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/), 100k utterances for 1251 celebrities.
Task: Speaker Reconition.
* [Speakers in the Wild](https://www.sri.com/work/publications/speakers-wild-sitw-speaker-recognition-database)
Task: Speaker Reconition.
* [Google AudioSet](https://research.google.com/audioset/).
2,084,320 human-labeled 10-second sounds, 632 audio event classes. 
Based on YouTube videos.
* Whale Detection Challenge. https://www.kaggle.com/c/whale-detection-challenge
* Mozilla [Common Voice](https://voice.mozilla.org), crowd sourcing.
Compiled dataset [on Kaggle](https://www.kaggle.com/mozillaorg/common-voice), 
500 hours of transcribed sentences.
Has speaker demographics.
Task: Automatic Speech Recognition.
Not something to do on microcontroller.
Could maybe be used for Transfer Learning for more relevant speech tasks.

## Relevant but lacking

* Hey Snips. https://github.com/snipsco/keyword-spotting-research-datasets
Task: Wakeword detetion, Vocal Activity Detection.
Restricted licencese terms. Academic/research use only.
Must contact via email for download.
By Snips, developing Private-by-Design, decentralized, open source voice assistants.

## Relevant

### TUT Rare Sound Events 2017

Used for DCASE2017 Task 2.
Baby crying, Glass Breaking, Gunshot.
3 classes, but separate binary classifiers encouraged.
Part of TUT Acoustic Scenes 2016.
Train 100 hours. Approx 100 sound examples per class isolated, 500 mixtures (weakly labeled).
Event detection.  Event-based error rate. Onset only. 500 ms collar. Also F1 score.
Baseline system available. FC DNN. 40 bands melspec, 5 frames. F1 0.72
Around 11 other systems submitted. Ranging 0.65-0.93 F1 score.
http://www.cs.tut.fi/sgn/arg/dcase2017/challenge/task-rare-sound-event-detection

Relevant as examples of single-function systems, security

### TensorFlow Speech Commands Data Set
Task: Keyword spotting / speech command

Very well explored.

Has state-of-the-art results for microcontroller.
https://arxiv.org/abs/1711.07128
Running on STM32F746G-DISCO. DSCNNL model gives 0.83/84.6% on Kaggle leaderboard
[How to Achieve High-Accuracy Keyword Spotting on Cortex-M Processors](https://community.arm.com/processors/b/blog/posts/high-accuracy-keyword-spotting-on-cortex-m-processors).
Reviews many deep learning approaches. DNN, CNN, RNN, CRNN, DS-CNN.
Considering 3 different sizes of networks, bound by NN memory limit and ops/second limits. Small= 80KB, 6M ops/inference.
Depthwise Separable Convolutional Neural Network (DS-CNN) provides the best accuracy while requiring significantly lower memory and compute resources.
94.5% accuracy for small network.
8-bit weights and 8-bit activations, with KWS running at 10 inferences per second.
Each inference – including memory copying, MFCC feature extraction and DNN execution – takes about 12 ms.
10x inferences/second. Rest sleeping = 12% duty cycle.
!uses MFCC instead of log-melspectrogram. melspec usually performs better?
?what is the compute time balance between MFCC feature calculation and inference?

https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/data

20 core words. Said multiple times per speaker.
"Yes", "No", "Up", "Down", "Left", "Right", "On", "Off", "Stop", "Go", "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", and "Nine".
10 auxiliary words. 1 repetition per speaker.
"Bed", "Bird", "Cat", "Dog", "Happy", "House", "Marvin", "Sheila", "Tree", and "Wow".
Note. Only 12 possible labels for the Test set: yes, no, up, down, left, right, on, off, stop, go, silence, unknown.
Some background noise files are also available.
39 participants scored 0.90-0.91060 (averaged Multiclass Accuracy).
Has 64,727 audio files total.
Lengths trimmed to be around 1 second. Aligned by the loudest utterance.
Released on August 3rd 2017.
Licensed Creative Commons 4.0.
A Special Prize required submissions to:
Have model size below 5MB.
Run in below 200ms on a Raspberry PI3.
They provided a benchmark script for evaluating it.
Winner Heng-Ryan-See * good bug? got 0.90825, very near top of any model.
Explanation of solution, with tips & tricks.
https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/discussion/46945
Used pseudo-labelling to generate "silence" and "unknown" data.
Single model at 0.87-0.88 without augmentation. Using ensembles to get higher.
Says melspectrogram perform better than MFCC.
A simple CNN reaching 0.74. https://www.kaggle.com/alphasis/light-weight-cnn-lb-0-74
A 1D CNN reaching 0.77. https://www.kaggle.com/kcs93023/keras-sequential-conv1d-model-classification
Has a tutorial at https://www.tensorflow.org/tutorials/sequences/audio_recognition
! uses MFCC as input features.
CNN architecture there is based on www.isca-speech.org/archive/interspeech_2015/papers/i15_1478.pdf
Example code for running in streaming mode is also provided (C++).
Has several architecture alternatives.
Ex `low_latency_svdf` with 750K parameters and 750kFLOPS. Reaching 0.85 acc
based Compressing Deep Neural Networks using a Rank-Constrained Topology, https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43813.pdf
`tiny_conv` designed for microcontrollers, 20KB RAM and 32KB FLASH.

Studying the Effects of Feature Extraction Settings on the Accuracy and Memory Requirements of Neural Networks for Keyword Spotting, https://ieeexplore.ieee.org/abstract/document/8576243
Compares MFCC feature extraction settings. 10-40 MFCC bands. 10-40ms size. Compares RAM/ROM use.
! GRU used 0.66 KB RAM with 314KB FLASH reaching 92%.
DS-CNN used 62KB RAM with 161KB FLASH reaching 93.5%

Novel architecture explored
[On-the-fly deterministic binary filters for memory efficient keyword spotting applications on embedded devices](https://dl.acm.org/citation.cfm?id=3212731)
BinaryCmd makes represents weights as a combination of predefined orthogonal binary basis.
that can generate convolutional filters very efficiently on-the-fly.
Deter-ministic Binary Filters, DBF.
Orthogonal variable spreading factor, OVSF
Also using MFCC features.
State of the art results (over Hey Edge) for models under 3MOPs and 30kB of model size.
! but CRNN at 3.3MOP has much higher performance, and smaller variation of CRNN nor DS-CNN not tested...

### ESC-50

[ESC-50: Dataset for Environmental Sound Classification](https://github.com/karoldvl/ESC-50).
2k samples, 50 classes in 5 major categories.
5 seconds each.
Compiled from freesound.org data
! only 40 samples per class.

Github repo has an excellent overview of attempted methods and their results.

* Best models achieving 86.50% accuracy.
* Human accuracy estimated 81.30%.
* Baseline CNN at 64.50%. 
* Baseline MFCC-RF, 44.30%.
* Over 20 CNN variations attempted.

Relevant for context-aware-computing, smarthome?

### Urbansound-8k

[Urbansound-8k](https://urbansounddataset.weebly.com/urbansound8k.html)

8000 samples total. 10 classes.
Compiled from freesound.org data.
Relevant for environmental noise source prediction.

! recommendation. Use the predefined 10 folds and perform 10-fold (not 5-fold) cross validation.
Otherwise will get inflated scores, due to related samples being mixed.

Detection of Anomalous Noise Events on Low-Capacity Acoustic Nodes
for Dynamic Road Traffic Noise Mapping within an Hybrid WASN
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5948866/

## DCASE2018 Task 2, General Purpose Audio Tagging
Task: Acoustic event tagging.
Based on FreeSound data.
41 classes. Using AudioNet ontology
9.5k samples train, ~3.7k manually-verified annotations and ~5.8k non-verified annotations. 
Test  ~1.6k manually-verified annotations.
Systems reach 0.90-0.95 mAP@3.
Baseline CNN on log melspec. 0.70 mAP@3

Relevant for: context-aware-computing, smarthome?

## DCASE2018 Task3, Bird Audio Detection.
Binary classification.

Relevant for on-edge pre-processing / efficient data collection.

## DCASE2018 Task4
Event Detection with precise time information.
Events from domestic tasks. 10 classes.
Subset of Audioset.

Relevant for: smarthome and context-aware-computing


## TUT Urban Acoustic Scenes 2018
Used in DCASE2018 Task 1.

Task: Acoustic Scene Classification.
10 classes. airport,shopping_mall,metro_station
About 30GB of data, around 24 hours training.
One variant dataset has parallel recording with multiple devices, for testing mismatched case.

Relevant for: context-aware-computing?

## TUT Acoustic Scenes 2017. Used for DCASE2017 Task 1.
Scenes from urban environments.
15 classes.
10 second segments.
Baseline system available. 18% F1
Relatively hard, systems achieved 35-55% F1.

Relevant for context-aware-computing?

## DCASE2017 Task 4, Large Scale Sound Event detection
http://www.cs.tut.fi/sgn/arg/dcase2017/challenge/task-large-scale-sound-event-detection
17 classes from 2 categories, Warning sounds and Vehicle sounds.

Relevant for autonomous vehicles?

## TUT Sound Events 2017
Used for DCASE2017 Task 3, Sound event detection in real life audio

Events related to car/driving.
6 classes.
Multiple overlapping events present. Both in training and testing.
Hard, systems only achieved 40%-45% F1.
Quite small. 2 GB dataset total.
Relevant for autonomous vehicles?