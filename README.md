# Herbie 

The concept of self-driving cars has been quite popular over the past 5 years. Companies like Tesla, Google and Uber are trying to develop their own version of self-driving cars that can run on real-world roads. Herbie, is a python project written using Open CV and Tensorflow that aims to apply modern self-driving concepts to a hobby car dubbed "Herbie". Herbie is powered by a Raspberry Pi 4 which uses a Google Edge TPU Accelerator to perform lightning-fast inferences when running on low-powered systems. This project intends to demonstrate my ability at writing a [Lane Keep Assist System (LKAS)](https://www.bianchihonda.com/honda-sensing-lane-keeping-assist-system/) currently running on modern cars (Honda, Toyota and etc) for Herbie using OpenCV. Moreover, this project will also attempt to demonstrate my abilities at building the same system using Deep Learning techiniques while also harnessing the power of transfer learning to develop a traffic object detection system.

Project Structure:

1. Src:

  -> DeepLearningLKAS.ipynb: Deep Learning approach at building a LKAS using Tensorflow and Keras.
  
  -> DeeplearningObkectDetection.ipynb: Applying transfer learning by harnessing the power of the Tensorflow Object Detectopm API
  
  -> dl_lkas.py: Logic needed by Herbie to run the Deep Learning LKAS model.
  
  -> driver.py: 
  
  -> herbie.py: Program entry point and driver of entire Herbie system.
  
  -> image_processing.py: Image processing methods needed to extract lane and headlines lines from Herbie's camera.
  
  -> lane_navigation.py: Logic that powers the LKAS system in Herbie


