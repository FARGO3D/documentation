.. _execflags:

Execution flags.
================

FARGO3D has options that can be activated at run time in the form::

  ./fargo3d -flag parfile


where "flag" is a suitable flag. The extensive list is:


________

**-m**:

.. warning::
   Starting from version 1.2, merging output files is the default
   behavior and the ``-m`` flag is no longer needed. We have kept it for
   backward compatibility.
   
Merge. This flag is used for writing files in the form ``fieldn.dat``
instead ``fieldn_m.dat``, with ``n,m`` integers (``n`` is the output 
number, `m` is the process number). This flag has relevance when you 
work with MPI. In practice, after NINTERM time steps, you will 
have an output, and each processor will write its own piece of mesh on 
the disk. If ``-m`` flag is activated, they will write a single file with 
all the data inside, in the right order, as if the data had been 
written by a single process run. 

________

**-k**:

Keep individual files from the different processes (do not merge
outputs). This flag is required if the different processes output to
different local disks, or if one dumps outputs including the ghost zones.

________

**-o**:

Redefine (overwrite) parameters on the command line. The following
argument must be enclosed between quotes. The parameters are case
insensitive. The syntax for the separators is relatively flexible. The
following example shows a valid instruction::

  ./fargo3d -o "outputdir=/scratch/test, nx:200 Ny=34"  my_parameterfile.par

An error message is issued if the parameter does not exist, or is
redefined several times. If the parameter was defined in the parameter
file (rather than being implicitly set to its default value), an
information string is output at run start.

________

**-s**:

Restart from separate files. This flag must be used in the form::
  
  ./fargo3d -s n parfile

where ``n`` is the output number at which you want to restart the
run. Each normal output could be used as a restart file. It works for
Dat & VTK files. The output files used for the restart are separate,
i.e. they have the shape ``fieldn_m.dat``, and must have been produced
by a run **without** the ``-m`` flag.

________

**-S**:

Restart from merged files. Same as before. It works for Dat & VTK 
files. The only difference is that the output files used for the restart are merged,
i.e. they have the shape ``fieldn.dat``, and must have been produced 
by a run **with** the ``-m`` flag. 

________

**+S**:

Restart and expand a run along the X dimension. This is typically used
to run a prior 2D calculation (radius, colatitude or Z) to enable a
disk to relax toward some equilibrium state. Once this equilibrium
state has been reached, the data is used to make up axisymmetric,
three-dimensional data cubes. Note that this is not considered as a
restart inside the code, but rather a fresh start, except that the
arrays are not filled with the initial condition but rather with the
data at output number *n*, expanded as necessary in X::

  ./fargo3d initial_2D_run.par
  ./fargo3d +S 100 -o 'Nx=628' initial_2D_run.par

In the example above the 2D output number 100 is used to fill the
arrays. The second run is this time 3D, as the number of zones in X
(azimuth) is now larger than one. Since technically this is *not* a
restart, the run will output its data at numbers 0, 1, etc. as for any
fresh start. The flag +S naturally also  works if the mesh is
cylindrical or Cartesian. It can also be used to re-spawn a 1D run, so
as to make it 2D (radius, azimuth).

________

**-D**:

Specify manually the CUDA device. This flag must to be used in the form::

  ./fargo3d -D n parameters.par

where ``n`` is an integer. 

With this flag, you can select manually the device where FARGO3D will run. 

________

**+D**:

Specify the CUDA device file::

  ./fargo3d +D devfile parameters.par

where ``devfile`` is a text file which contains several lines. Each
line must contain a hostname (such as ``compute-0-34``), followed by
one of the three following separators::

  : (column), / (slash), or = (equal)

followed itself by a device number. Example of device file::

  compute-0-0: 0
  compute-0-0: 1
  compute-0-1: 0
  compute-0-1: 1


This device file is intended for a run on two nodes (``compute-0-0`` and
``compute-0-1``), each node having two GPUs (numbered 0 and 1 on each
node). If the run is spawned on nodes not specified in the device
file, the run will fail (technically, if the string returned by
``gethostname()`` does not match the beginning of any line in the device
file).

The device file can be used together with the job scheduler (such as
torque or PBS) to obtain the list of free GPUs on the nodes of the
job, *even if the job scheduler is not GPU aware*.  The public
distribution comes with a directory called ``jobs``, in which you will
find an example of PBS job file called ``devfile`` that parses the
output of ``qstat`` to find the GPUs available.

________

**-V**:

The same as -S, but takes a .dat merged file, and makes VTK
files. Useful if you want to convert some .dat files into VTK files.

________

**-B**:

The same as -S, but takes a VTK merged file, and makes .dat
files. Useful if you want to convert some .vtk files into .dat files.

________

**-t**:
 
Timer. Very useful to follow the execution of a run and get an
estimate of the time remaining to complete. 
If you want more detailed information, you can compile the code with
the PROFILE=1 option (shortcut: make prof) and it will provide
detailed information for each block of the time step. The -t flag is
not required in this case.

________

**-f**:

Execute one elementary time step and exits. Useful for some automatic 
benchmarking (such as optimal block size determination), and also 
(indirectly) useful to merge the output of several processes (see :ref:`ttt`.) 

________

**-0**:

Set the initial arrays (either with ``condinit()`` for a fresh start,
or reading an output if it is a restart), writes them to the disk, and
exits. Might be useful to merge prior outputs if FARGO3D has been run
without the flag ``-m``.

________

**-C**:

Force execution of all functions on CPU (for a GPU built). Obviously 
this flag does nothing if the executable was built for the CPU. 

________

**-p**:

Instruct the code to execute a post restart hook upon loading the 
files from a previous output. This flag is not used in any of the 
files provided in the public release. 

________

**+/-# n**:

Provides a numerical seed to the code, that is used for two things:

   #. The numerical seed is zero padded up to six digits and appended
      to the name of the output directory.
   #. This seed, which is accessible from any part of the code as the
      integer variable ``ArrayNb``, will be used in general as a
      random seed for the initial conditions (``condinit.c`` in the
      setup directory)  or the file ``postrestarthook.c`` (but its use
      may not be limited to that).

In the case of a restart, the name of the output directory is changed
*prior to* reading the data necessary of the restart, if the flag
``+#`` is used. Otherwise, when the flag ``-#`` is used, the data is
read in the directory specified by the string ``outputdir`` of the
parameter file or the command line, then the ``outputdir`` parameter
is changed and the data is output to the new directory. This technique
is very useful to spawn a large number of jobs when used in
conjunction with ``$PBS_ARRAYID``.

Example: we run a master simulation in output directory ``out``::

  ./fargo3d -o 'outputdir=out' parameters.par

We then fork the results of this master simulation by restarting it
with many different random seeds::

  ./fargo3d -S 100 -# number -o 'outputdir=out' parameters.par

We use the output number 100 found in ``out`` for each of the runs
(since we use the ``-#`` flag). ``number`` is either provided by
``$PBS_ARRAY`` or any shell loop index.

Finally, each of the runs can be subsequently  restarted itself as
follows::

  ./fargo3d -S 200 +# number -o 'outputdir=out' parameters.par

We must now use the flag ``+#``, as it is important that run 23 seeks
the data for restart in ``out000023`` and not ``out``.

When no restart is planned, one must use the +# flag instead of -#.
