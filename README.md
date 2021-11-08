# Gesture-Controlled-Mouse
## Short Description
#### Used the MediaPipe library to build an interactive way to use the mouse.
&nbsp;
## Medipipe and the HandTracking class
#### The HandTracking class houses under the hood everything you need to manage hand tracking for any application.
#### ```findHandsAndList(img[, list=True])``` - takes the current image from the camera, and returns the modified image with the mesh on it, the list of all the coordinates of the tracked points on the mesh (this can be turned off by setting ```list``` to ```False``` ) and the coordinates of the center of mass of the hand as a tuple ```(gX, gY)```
#### ```setMouseTracking(state)``` - switches the movement of the mouse by the movement of the tracked hand *ON* and *OFF*
#### ```getMouseTracking()``` - returns the current state of the mouse tracking
&nbsp;
## Gesture Tracking
#### The aforementioned class combined with some math to manage to get the gesture tracking to work no matter the distance produces quite a fun tool to use.
### Gestures
#### The gestures that the user can make to control the mouse are quite simple and intuitive, just touching the tips of your fingers:
####        * _Thumb_ and _Index_ Fingers : Left click the mouse
####        * _Thumb_ and _Middle_ Finger : Turn off tracking
&nbsp;
### Quick Math
#### The central point of the palm mesh is computed as the arithmetic mean of the points 0, 5, 9, 13, 17. The trick that makes the 
er work at any fair distance from the camera is the fact that we use ***angles, not distances*** to detect gestures.
#### ![Hand Points](https://google.github.io/mediapipe/images/mobile/hand_landmarks.png)
#### The angle is computed as follows. Take the center of the palm as C. We consider the vectors determined by points (4,C) for the Thumb, (8,C) and (12,C) for the Index and Middle Fingers respectively. Then we compute the angles based ont the Cosine Formula. We consider a value alpha small enough that when an angle is smaller than it, we can consider it as a gesture.
