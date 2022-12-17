# TESTING

## Test parameters
- Frame rate
- Resolution
- Launch styles
- Different filtering parameters

## METHOD

- To test the algorithm, a webcam with a laptop should be used.
- Every frame must be stored in a folder and be well-structured with respect to test parameters. 
    - For example, "{FrameRate}_{Resolution}_{LaunchStyle}_{Filter#1}_{Test#1}/{Frame1}.jpeg"
- There must be configurable frame rate and resolution settings in the code.
    - Change one of the parameters while keeping constant the other one 
- Balls will most probably thrown by hand during testing. Thus, whole settings of the launching styles may not be tested.
    - Specific launching parameter must be noted by us 
- Beforehand, 2-3 filtering options can be selected. During testing, above test parameters can be tested again with different filterings. 

## TODOs

- Implement configurable frame rate and resolution settings in the algorithm. 
- Implement structured foldering and naming for tests.
- Implement input selection for launch style
- Research appropriate filtering methods and eliminate the error prone ones.