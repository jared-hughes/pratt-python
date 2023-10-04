Pratt-like parser in Python, with a REPL.

```
 $ python3 repl.py 
Basic syntax: 2*sin(pi)+1-(3/4)*5^6. Type :functions for a list of functions.
>>> 2*sin(pi)+1-(3/4)*5^6
-11717.75
>>> atan2(inf,inf)/pi
0.25
>>> :functions
acos   ceil      erfc       frexp     isinf   log1p      sin    perm       inf
acosh  copysign  exp        fsum      isnan   log10      sinh   comb       nan
asin   cos       expm1      gamma     isqrt   log2       sqrt   nextafter
asinh  cosh      fabs       gcd       lcm     modf       tan    ulp      
atan   degrees   factorial  hypot     ldexp   pow        tanh   pi       
atan2  dist      floor      isclose   lgamma  radians    trunc  e        
atanh  erf       fmod       isfinite  log     remainder  prod   tau
```

Ctrl/Cmd+C to interrupt (however you normally stop a running Python terminal program).

Python's `math` functions are exposed. The list is from Python 3.10. If you're on an earlier version, you might have to remove some lines in `frame.py` to avoid errors.
