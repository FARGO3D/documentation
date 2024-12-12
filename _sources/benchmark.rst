.. _benchmark:

GPU vs CPU Benchmarking
==============================

Some acceleration factors
-----------------------------------------

At the present time, FARGO3D has run on a limited number of platforms,
so we have only a limited amount of acceleration factors to quote
between CPU and GPU.


The FARGO_SPEEDUP macrocommand
---------------------------------------------

We have developed a macrocommand named ``FARGO_SPEEDUP``. You can see
its source in the file ``src/define.h``, near the line 475. This
macrocommand is meant to give the speedup factor of a given CUDA kernel
with respect to its CPU counter. Its use is overly simple. Suppose
that we want to know the speedup ratio GPU vs CPU of the function
``SubStep1_x()``, for the setup ``fargo``.

First, we need to identify where this function is invoked. It is
called near the line 73 in the file ``src/algogas.c``::

   #ifdef X  
       FARGO_SAFE(SubStep1_x(dt));
   #endif  
 
Note that the invocation is wrapped in a ``FARGO_SAFE`` macrocommand,
the definition of which is... empty (see file ``src/define.h`` near
line 409). All the substeps of FARGO3D are wrapped similarly into this
macrocommand. In normal use, it does not do anything. However, it may
be redefined (see the alternate definitions commented out near line
409 in ``src/define.h``), so as to provide useful debugging
diagnostics.

What we need to do here to get an automatic evaluation of the speedup
factor is simply to change our wrapper from ``FARGO_SAFE`` to
``FARGO_SPEEDUP``. Note that this new macrocommand will manipulate a
bit the function name (it will subsequently invoke
``SubStep1_x_cpu()`` then ``SubStep1_x_gpu()``.  Since the C
preprocessor is unable to manipulate strings, we need to help it
identify where the sub-string of arguments begins, by inserting a comma::

   #ifdef X 
       FARGO_SPEEDUP(SubStep1_x,(dt));  // <= Note the comma before the '('
   #endif 

We now build the code for the target setup, with the PROFILING and GPU
options enabled::

  make SETUP=mri GPU=1 PROFILING=1

and we run it::

  ./fargo3d in/mri.par

You should see an output such as::

   Wall clock time elapsed during MPI Communications : 0.030 s
   OUTPUTS 0 at Physical Time t = 0.000000 OK
   TotalMass = 0.0271300282 
   
   
   ******
   Check point created
   ******
   
   
   
   ******
   Check point restored
   *******
   
   GPU/CPU speedup in SubStep1_x: 22.775
   CPU time : 91.1 ms
   GPU time : 4 ms


We see that the function is timed both in its CPU and GPU
version (this test was obtained on an Intel(R) Core(TM) i7 950 at 3.07
GHz, and on a Tesla C2050 card). We also
note how execution continues after the evaluation, so that periodically
an evaluation of the speedup of our target function is
provided. It is interesting to see how the macrocommand is expanded by
the preprocessor::

   { 
     SynchronizeHD ();
     SaveState (); 
     InitSpecificTime (&t_speedup_cpu, ""); 
     for (t_speedup_count=0; t_speedup_count < 200; t_speedup_count++) { 
       SubStep1_x_cpu (dt); 
     } 
     time_speedup_cpu = GiveSpecificTime (t_speedup_cpu);
     SynchronizeHD ();
     RestoreState (); 
     InitSpecificTime (&t_speedup_gpu, ""); 
     for (t_speedup_count=0; t_speedup_count < 2000; t_speedup_count++) { 
       SubStep1_x_gpu (dt);
     }
     time_speedup_gpu = GiveSpecificTime (t_speedup_gpu);
     printf ("GPU/CPU speedup in %s: %g\n", "SubStep1_x", time_speedup_cpu/time_speedup_gpu*10.0);
     printf ("CPU time : %g ms\n", 1e3*time_speedup_cpu/200.0); 
     printf ("GPU time : %g ms\n", 1e3*time_speedup_gpu/2000.0);
   };

(a proper indentation has been added for legibility.)

We see that the function is firstly executed 200 times on the CPU,
then 2000 times on the GPU.  The respective single times on CPU and
GPU are inferred, and thus the speedup ratio. 

Note that we have developed another useful macrocommand in the same
spirit, called ``FARGO_DEBUG``, which is meant to automatically
compare the result of the CPU version of one routine with the result
of its GPU counterpart.  It is presented in section :ref:`fargodebug`.







