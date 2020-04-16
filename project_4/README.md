# Project 4 Tools
These tools were developed by @neiljohari during W20 for the Drones iteration
of this project. The scripts should be pretty easy to adapt for future
iterations of this project.

The test generator was developed by @arya-k. 

## Regression Testing 
I made one of these for last project and did it again for this one because I hate submitting something not knowing if I broke everything that previously worked.

This one is definitely less useful than the previous script because of the fact that multiple answers exist (so a simple diff isn't enough anymore). This can't test if your solution is still valid after serious algorithm changes.

All this script does is make sure you still output the right number of vertices + output the same weight you got last time (or for FASTTSP you're within some tolerance margin of the right answer/your generated correct solution). It runs all the spec tests, and your custom tests (assuming you named them correctly, the mode will be inferred).

Usage:
- The script requires `bc` package to do floating point arithmetic for tolerance calculations. This comes with macOS. For Ubuntu, `sudo apt install bc`.
- Make sure the scripts are executable (`chmod +x ./generate_correct_outputs.sh && chmod +x ./regression_test.sh`)
- Run `./generate_correct_outputs.sh` after altering tests or adding tests, but not after changing your codebase
- Run `./regression_test.sh` to run your tests. 
   * If you get `FAILED` for something, either you printed the wrong number of vertices or your weight produced was wrong (it'll say). 
    * If you failed it because of FASTTSP and you're fine with how far off it is, change the `TOLERANCE` variable in the script (this depends on your goals for this project, higher tolerance -> more likely to lose points on the AG for your tour being too long).

Notes: 
- This'll probably be most useful for part C (which is where I'm at so I wrote it to help me). The reason being that you might need to alter your algorithms in A and B a bit to make it work, but you don't want to break them for older tests.
- Might help you with parts A and B in terms of making sure you're getting the right MST weight &amp; number of vertices from the spec examples?


Example output (I didn't start part c yet, hence the failures):
```
eecs281-p4 on part-c [?]
➜ ./regression_test.sh
Running regression test suite with a tolerance of 1% for FASTTSP
PASSED test-1-MST.txt ON MST
PASSED test-2-MST.txt ON MST
PASSED test-3-MST.txt ON MST
PASSED test-4-FASTTSP.txt ON FASTTSP
PASSED test-5-FASTTSP.txt ON FASTTSP
PASSED sample-ab.txt ON MST
PASSED sample-ab.txt ON FASTTSP
PASSED sample-c.txt ON MST
PASSED sample-c.txt ON FASTTSP
FAILED sample-c.txt ON OPTTSP (word counts differ — wrong number of vertices?)
PASSED sample-d.txt ON MST
PASSED sample-d.txt ON FASTTSP
FAILED sample-d.txt ON OPTTSP (word counts differ — wrong number of vertices?)
PASSED sample-e.txt ON MST
PASSED sample-e.txt ON FASTTSP (difference of 0.722% was within tolerance)
FAILED sample-e.txt ON OPTTSP (word counts differ — wrong number of vertices?)
```

## Test Generator
The test-generator.py file was written by @arya-k and can be run with `python3
test-generator.py`. 


