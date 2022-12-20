## NOTES

* <s>Algorithm is not working properly with white ball since there are white strips on the edges of the table and on the net.</s>
* Now filtering is working with white ball also so any video with proper perspective can be used.

## TODOs

* Tidy up the GUI 
    * Fix the default values - DONE
    * Show the frame rate and resolution
    * Show the radius and position of the ball pixel-wise  - DONE

<br />

* Create an hit detection algorithm
    * Kalman filter is utilized for predicting the path of the ball - DONE <br />
        * <s> Depends on spin, speed, launching angle.. - LEFT </s>
    * If the ball gets out from some error margin, count as hit
    * If it does stay in the prediction and ball goes below the table, count as miss
<br /> <br />

* <s> Collect more test videos with orange ball - CANCEL </s>
    * If possible, gather videos with different resolution and frame rates 

<br /> 


    
