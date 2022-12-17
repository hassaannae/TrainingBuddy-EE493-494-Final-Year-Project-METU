## NOTES

* Algorithm is not working properly with white ball since there are white strips on the edges of the table and on the net.

## TODOs

* Tidy up the GUI 
    * Fix the default values
    * Show the frame rate and resolution
    * Show the radius and position of the ball pixel-wise  
<br />

* Create an hit detection algorithm
    * By observing first 3-4 frames predict the future position and size of the ball
        * Depends on spin, speed, launching angle..
    * If the ball gets out from some error margin, count as hit
    * If not and ball is not visible, count as miss
<br /> <br />

* Collect more test videos with orange ball
    * If possible, gather videos with different resolution and frame rates 
