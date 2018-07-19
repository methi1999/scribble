# scribble
We particiapted in the 'Institute Technical Summer Project' program here at IIT Bombay. Our main objective was to build a pen which is capable of detecting English letters in real-time. A brief description is given below. The complete documentation can be found here: https://drive.google.com/file/d/1lUH5dwckl_dLwbNdgbxjktIRy_dRRGJi/view?usp=sharing

There are two main sections:

Hardware - It consists of a 3D printed enclosure for the pen. A pressure switch is placed at the end of the refill. On pressing the pen against paper, the refill retracts, gets pressed against the switch and completes a simple circuit which consists of an LED. As the LED glows, a webcam placed below the paper tracks it's motion and saves the keystroke as a jpeg file. The training dataset can be found here: https://drive.google.com/drive/folders/1UDpgp2MzCdYI8azRJeVBtv_bAZIcv9wr?usp=sharing
Then comes the crufcial task of recognising the letter which is described below.

Software - Considering it's high accuracy in image classification tasks, a Convolution Neural Network was used. We generated our own training data by using an OpenCV tracking program. By drawing out letters in front of our laptop's webcam, we wrote a small loop which kept saving the tracked letter to disk. Approximately, 300 images per letter were generated. Using a package called Augmentor, we added random distortions and increased the number to a healthy 5000.
Once our dataset was ready, we trained our CNN. The specifics of the architecture can be found in the documentation.

The repository contains code for the generation of training data, a GUI script for displaying the detected letters and the master program which carries out the core tasks.
