.. _ttt:


Tips, Tricks, Todos and Troubleshooting
==================================================================================

With no particular order, we draw hereafter a list of questions that
may come to the user's mind.  This list will be updated according to
the users' feedback.


How do I add a new parameter to a setup ?
----------------------------------------------------------------------------
Imagine you want to add a real variable ``RHOR`` (density on the right
side) to the set up ``sod1d`` (thus far the right value of the density
in the Riemann problem is hard-coded in ``condinit.c``). Just add a
line such as the following in ``setups/sod1d/sod1d.par``::

  RhoR            0.1

and this is all. A python script which parses this file makes sure
that you have access to a global real variable named ``RHOR``
throughout all the functions of the C code. You can now use this
variable to replace the hard-coded value in
``setups/sod1d/condinit.c``.

.. note:: The variable name in the .par file is case insensitive, but
   C is case sensitive. The name is converted to upper case for the C
   code.  You must help the parser to automagically guess the type of
   the variable. Here "0.1" works, but ".1" would not.


How do I create a new ``Field`` variable?
-----------------------------------------

1. Create a pointer in ``src/global.h``.

   Example: ``Field *Myfield;``

2. Allocate memory with the function ``CreateField()``. To do that, in ``src/LowTasks.c``, inside the function ``CreateFields()``, add:

   ``Myfield = CreateField("myfield",0,0,0,0);``

.. note:: When using the new field inside a function/kernel, do not forget the corresponding ``INPUT/OUTPUT`` statements.


How do I write a ``Field``?
---------------------------

To write the Field ``myField`` in the disk, add

   ``__WriteField(Myfield, TimeStep);``

   in ``src/output.c``, inside the function ``WriteOutputs()``.
   
What is the way to merge the outputs of a run spawned with the ``-k`` flag ?
-----------------------------------------------------------------------------

Spawning a run with the ``-k`` flag keeps one output file per
processor (for a given variable) instead of merging these files to
produce a unique, larger file.

Assume you run ran on 8 processors, and you want to merge the output
#5. You may issue on the command line, in FARGO3D's main directory::

 mpirun -np 8 ./fargo3d -s 5 -0 yourparfile

It will do the trick (restart from fragmented output -lower ``s``-,
then merge outputs, and exit). Edit the above line according to your
needs, or insert it into a bash loop to merge the outputs of an entire
directory.

.. note::
   This technique is non-destructive, in the sense that it does neither
   change nor remove the individual outputs.

.. warning::
   The above instruction requires that the whole simulation may fit on
   your platform's memory. If you issue it on a small laptop for a
   simulation that ran on a large cluster, it may fail if there is not
   enough RAM.


I see lots of "!" or ":" instead of "." at execution. What does that mean?
--------------------------------------------------------------------------------------------------------------------------------

This happens when you have a GPU built, and GPU-GPU communications are
not fully optimized. See the section :ref:`gpucomm` and
:ref:`mpicuda`. Note that periodic boundary conditions are handled
like normal MPI communications, even on a one process run, so that
they transit through the host (CPU) if no CUDA aware version of MPI is
used.


Where my last run data has been output ?
-----------------------------------------------------------------------------------------------------

The path to this directory is given by the parameter 'OUTPUTDIR' in
the parameter file that you specified in your run. If this parameter
begins with a '@', this character should be substituted with the
content of the ``FARGO_OUT`` environment variable, if it exists.  You
can also go to your home directory. There, a directory name
``.fargo3drc`` has been produced, which contains two files:
``history`` and ``lastout``. The latter contains for each run issued a
timestamp and the path to the output directory. The former contains a
timestamp, the command that was issued to run the code, the number of
processes, the list of hosts (and devices for GPU builts) on which the
code was run, and the output directory. The ``lastout`` file is
obsolete.  You may define an alias in your ``.bashrc`` file that
brings you automatically to the last output directory::

  alias fo='cd `tail -n 1 $HOME/.fargo3drc/history`'



My build produces unexpected results. Some files should have been remade and they have not. How do I fix this ?
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Although we have dedicated some care to the chain of rules of the
relatively complex build process, we may have failed to respect some
dependencies. If you believe that your make process is flawed, the
simplest solution is to note your build options with ``make info``,
then issue a ``make mrproper`` and finally rebuild by issuing a new
``make`` command followed by all your build options.


My code does not run much faster on the GPU than on the CPU. Why is this ?
------------------------------------------------------------------------------------------------------------------------------

There are several reasons for this.

* Your setup is very small, and your GPU(s) is/are underused.

* You have default block sizes in your ``.opt`` file that are far from
  optimal, yielding a degradation of performance.

* You have a high end CPU and a low end GPU...

* You may not have tuned sufficiently the GPU build options in
  ``src/makefile``. Make sure to set them to your target GPU
  architecture.

* You have a 2D, YZ setup (see the note below about reductions).

.. warning:: Reductions are operations on a whole mesh that amount to
   obtaining a single number as a function of all cells' content
   (hence the name "reduction"). It may be the sum of the mass or
   momentum content of all cells, or the minimum of all time steps
   allowed on all cells as a result of the CFL criterion: the
   reduction operation can be a sum, a ``min()``, etc. We see that
   there is at least one unavoidable reduction operation per time
   step: the search for the maximum time step allowed. Reduction
   operations are performed in a two stage process:

      * A reduction in the X direction, at the end of which we obtain
	a 2D array in YZ. This reduction is performed on board the
	GPU, using the algorithm described in this `pdf document
	<http://developer.download.nvidia.com/assets/cuda/files/reduction.pdf>`_. This
	corresponds to one of the few kernels that are written
	explicitly in FARGO3D (instead of being produced by the Python
	script). The user should never have to interfere with it.
	
      * A further reduction in the Y an Z dimensions of the previous 2D
	array. This is done on the host, as this has a low computational
	cost. This operation involves a Device->Host communication only,
	of a one cell thick single 2D array, which is not taken into
	account when evaluating 2D communications that yield the ":"
	diagnostic on the terminal (see :ref:`mpicuda`).

The two stage process detailed above is generally not a problem, as we
expect most setups to have a number of zones in X (or azimuth) much
larger than the GPU vs CPU speed up factor (hence it is the first
stage -reduction on board of the GPU- that constitutes the time
consuming part). If however you have a YZ setup, the number of zones
in X is just one, and in this case it is the second stage of the
reduction process (on board the CPU) that constitutes the bottleneck:
it is like if the reduction was entirely performed on the CPU. If you
want to assess how much of your setup's slowness can be put on the
account of this restriction, you may try to hard-code the time step in
``src/algogas.c`` to see if this yields significant improvement. Also,
during this test, you have to deactivate all monitoring in the
``.opt`` file, as monitoring requires reductions which are performed
as described above.


What is this @ sign at the beginning of the outputs' path ?
----------------------------------------------------------------------------------------------------------

Unless you have defined the environment variable ``FARGO_OUT``, this
"@" sign is not used, and you may remove it if you wish. When the
``FARGO_OUT`` environment variable is defined (for instance in your
job script or in your .bashrc file), its value substitutes the "@"
sign in your output path. If, for instance, you have::

   OutputDir   @mri/beta150

in your .par file, and you have defined in your ``.bashrc`` file the
following::

  export FARGO_OUT='/data/myname/fargo3d'

then your run will output its data in
``/data/myname/fargo3d/mri/beta150``.

This trick is version control friendly: you define once for ever the
sub directory where you want your data to be, and the prefix part is
specified in the environment variable out of the version control, so
that if different persons work on the parameter file, it will not
trigger a sequence of different versions.  You may have on one
platform::

  export FARGO_OUT='/data2/pablo/fargo3d'

and on another one::

  export FARGO_OUT='/scratch3/frederic/fargo3d'

and the same parameter file may be used without any editing.


I see that there are .par files in each setup directory, and the same .par files are found in the in/ sub directory. What is this for ?
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The ``.par`` files found in the setup directories are necessary to
build FARGO3D: a python script uses them to determine the set of
global upper case variables that will be available everywhere
throughout the C code, with the value that the user defines for them
in his ``.par`` file. Therefore, these "setup" or "master"``.par``
files must include all variables that can ever be used by the setup,
and they must specify default, fiducial values for all parameters.

Although the user may run the code by using these  "master" parameter
files, e.g.::

  ./fargo3d setups/fargo/fargo.par

this is not customary and any other parameter file, with different
parameter values than those specified in the "master" parfile, may be
used::

  ./fargo3d in/fargo.par

You may have a large set of parameters files with different values,
and you can run the code on them without any rebuild.

.. note:: 
   If a parameter is not defined in a parameter file, the code will
   take its default value from the "master" parameter file, unless
   this parameter is specified as *mandatory*, in which case the user
   *must* specify its value in any parameter file (otherwise an error
   message is issued and the code stops.)

.. warning::
   It is recommended to edit the parameter files of the ``in/``
   directory, rather than interfering with the "master" parameter
   files found in the setups directories.

.. seealso:: :ref:`parfile`.


I have noticed a directory named ``.fargo3drc`` in my home directory. What is it here for ?
---------------------------------------------------------------------------------------------------------------------------

This directory contains two text files (``history`` and ``lastout``)
which are updated at each new run.  Every time a new run is spawned,
two lines are appended to the ``history`` file: a line indicating the
date and time at which the run was launched, and the command line
issued to launch the run. In addition, two new lines are appended to
the ``lastout`` file: a time stamp as previously, and the absolute
path of the output directory.  It can be useful to parse the last line
of this file with a script to go directly where the output is
written::

  alias fo='cd `tail -n 1 $HOME/.fargo3drc/lastout`'

The above line, in the ``.bashrc`` file, will define a command ``fo``
(like Fargo3d Output) which changes the directory to the output
directory of the last run.

**Known issue**:

When the ``-o`` flag is used on the command line, the subsequent
quotation marks are not written to the file ``history``. If one
wishes to cut and paste some line of this file to repeat a given run,
one must ensure to manually edit the line to restore the quotation
marks, when the flag ``-o`` is used.


How can I see the output of python scripts (in particular the CUDA files) ?
---------------------------------------------------------------------------------------------------------------------------


You will find below information to retrieve manually the output of
each of the python scripts involved at build stage. However, starting
from version 1.3, the build process creates an ``arch/`` subdirectory
in which all the source files are archived, even those created
automatically such as those created by the boundary conditions scripts
or the ``c2cuda`` converter.  It is therefore much easier than in
earlier versions to have a glance at the intermediate source files
automatically created at build time.

You may have noticed a long list of files being removed at the end of
the build process, especially on GPU builds. These files are
intermediate files such as CUDA files automatically produced by the
*c2cuda* script, etc. and the make process must remove them upon
completion in order to preserve dependencies. Failing to do so would
result, for instance, in the GPU version of a routine not being
rebuilt if its C source was edited. We do not issue explicitly this
``rm`` command in the makefile. This is done automatically, out of our
control, because make knows that it must preserve dependencies.

This may be frustrating as you cannot have a look at the CUDA files or
boundary source codes produced by the Python scripts. This, sometimes,
can be useful to understand unexpected behaviors. Here we indicate the
manual procedure to produce all the intermediary files used during the
build process. Do not forget to remove them prior to a full build of
the code, or dependencies may be broken !

**Creation of var.c**:

In ``src/``, issue::

  python ../scripts/par.py ../setups/mri/mri.par ../std/stdpar.par 

Naturally substitute the mri setup in the above line with your own setup.

**Creation of param.h, param_noex.h, global_ex.h:**

In ``src/``, issue::

  python ../scripts/varparser.py

**Creation of rescale.c:**

In ``src/``, issue::
  
  python ../scripts/unitparser.py mri

The ``rescale.c`` file is produced in the ``src`` directory

**Creation of boundary source code:**

In ``src/``, issue::

  python ../scripts/boundparser.py ../std/boundaries.txt  ../std/centering.txt ../setups/mri/mri.bound

If you issue the command ``ls -ltr`` you will see new files with name
*[y/z][min/max]_bound.c* that you can examine. Note that since
periodic boundary conditions are not dealt with as other BCs but
rather with communications, they do not generate such files. For
instance, with the ``mri`` setup, you only have the *y* files, not the
*z* files.

**Creation of the CUDA source code:**

It can be done for any of the files which has same radix than those of
the list *GPU_OBJBLOCKS* in the makefile. We take the example here of
the file ``compute_emf.c``. In the ``src/`` directory, issue::
  
  python ../scripts/c2cuda.py -i compute_emf.c -o foo.cu

In this command line, *-i* stands for the input, and *-o* for the
output.  Note that we do not follow here the automatic rule that would
create ``../bin/compute_emf_gpu.o``. As a result, there is no risk to
break dependencies if we forget to remove the file created manually.
You can examine the file ``foo.cu`` and compare it to the input C
file. You may also try to invoke it with the ``-p`` flag that
implements a loop in the wrapper function to determine the best block
size.

Tweaking the CUDA executable for memory optimization
---------------------------------------------------------------------

The default behavior of memory allocation on the GPU is to pad arrays
in order to respect the alignment of all rows. This may consume an
extra amount of memory, which is very parameter dependent. If you wish
to allocate memory like on the host, without padding, you may use the
compilation flag NOPITCH (e.g. in the opt file, add the following
line: ``FARGO_OPT += -DNOPITCH'``, and rebuild). The performance
degradation is negligible and you may be able to use slightly larger
arrays on a given GPU.

Speeding up reduction operations on platform >= 3.5
--------------------------------------------------------------

Reductions are by default implemented as described on a famous
presentation by Mark Harris (NVIDIA), which works for all platforms,
even old ones. On >= 3.5 platforms, one may use the possibility of
warp shuffle, which can significantly speed up reductions. In order to
do that, you must use the compilation flag WARPSHUFFLE (e.g. in the
opt file, add the following line: ``FARGO_OPT += -DWARPSHUFFLE'``, and
rebuild). The new kernel thus called reduces the amount of shared
memory used by the GPU. As described for standard reductions, the
reduction thus executed is done along the X direction only, and the
subsequent reduction in Y and Z is performed on the CPU.

A very incomplete TODO list
----------------------------------------------------------------------------------------------------------------------------------------

We have several projects or improvements in mind for FARGO3D. Some of
them are cosmetic time savers, others are more substantial. Among them:

* Since we can parse the C code to produce CUDA code, we can also, in
  principle, produce automatically OpenCL code. This would enable
  FARGO3D to run on non-NVIDIA's GPUs, and on multi-core platforms.

* We would like to merge FARGO3D and the nested mesh structure of the
  code JUPITER (developed by one of us but never publicly
  released). This would require to have normal ghost zones in the X
  direction (as for Y and Z), a 3D mesh splitting of processing
  elements, and an adaptation of the ghost filling procedure. In this
  `page <http://adsabs.harvard.edu/abs/2014ApJ...782...65S>`_ you can
  see JUPITER at work with a number of nested meshes onto a giant
  planet.
