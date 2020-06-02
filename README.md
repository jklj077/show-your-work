# Show Your Work

A simple Python3 script for calculating the expected validation performance proposed in [Show Your Work: Improved Reporting of Experimental Results (Dodge, et al, EMNLP 2019) ](https://arxiv.org/abs/1909.03004) and refined in [Showing Your Work Doesn't Always Work (Tang, et al, ACL 2020) ](https://arxiv.org/abs/2004.13705). 

Refer to those papers for the actual caculation. Correctness of the implemenation is not verified.

## Requirement

No requirements. If `scipy` exists or Python>=3.8, the script will use the provided `comb` function.

## Usage
Just import the function `expected_maximum_performance` from the script.

```
Arguments:
    values (List[Number]): the performance measurements from multiple experiments
    biased (bool): if True, use the biased version in (Dodge, et al, 2019); or 
                   use the unbiased version in (Tang, et al, 2020)

Return:
    List[Number]: the expected maximum performance for the number of trials
```


It aslo has a command line interface.
```
usage: show_your_work.py [-h] [-f FILE] [-n [NUM [NUM ...]]] [-b] [-p]

Script to caculate the expected validation performance proposed in (Dodge, et
al, 2019)

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Read values from file (one value per line)
  -n [NUM [NUM ...]], --numbers [NUM [NUM ...]]
                        Values
  -b, --biased          Use the original biased version
  -p, --print           Print the results, a number per line

If neither file or numbers are given, interactive mode will be used. Enter a
number on each line. Empty line to end. The numbers option is preferred over
the file option
```

