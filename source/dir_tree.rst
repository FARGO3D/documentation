Directory tree
===============

FARGO3D was developed as a general code. It solves a set of coupled
differential equations on a mesh. Because it was developed as a
general solver, it is necessary to keep certain general features
isolated from other, more specific ones (that correspond to a specific
problem).

A simple example of that is the initial condition (IC) of a
problem. Obviously, the IC is a problem-dependent feature, and a
mechanism is needed to keep it isolated from another problem. Touching
the main structure of the code only to change the IC is not a good
idea (yes, you can, but this is ugly, error-prone and wreaks havoc
with versioning systems). This kind of problem is solved using the
concept of SETUPS, and with the help of the *VPATH* Makefile
variable. If you know the RAMSES code
(https://bitbucket.org/rteyssie/ramses), you will see
that we use the same patch concept.

.. warning:: In practice, when using FARGO3D you do not need to know
   about the ``VPATH`` variable, but if you want to develop some new
   features, it is a good idea to keep in mind that it is used under
   the hood.

Another problem is related to the different modules of the code. For
example, in some situations, we need to use the MHD module, but for
another set of problems, the MHD is irrelevant. In order to avoid a
lot of logical runtime tests inside the code (``if``'s), we prefer to
use *MACROCOMMAND* variables. These variables are interpreted prior to
compilation time, by the so-called *preprocessor*, and
activate/deactivate certain features (lines) of the code, allowing a
tailor-made executable, built for a specific problem. All these
variables are activated from the Makefile (they are defined actually
in the .opt files that we shall see below).

The most important file to ultimately build a FARGO3D executable is
obviously the Makefile.  For this reason, there is a section devoted
to this particular file. But, because FARGO3D uses a lot of scripting
at compilation time, the process of building the code does not simply
reduce to the Makefile. We refer to the FARGO3D building process as
"the make process".

A given instance of FARGO3D has many different properties, and storing
each one in an organized manner is achieved through a number of
different subdirectories.  In this section, we give a brief
explanation of each one.

Directories
------------

src/
....

The directory where the main sources are stored is the ``src/``
directory. Inside it, you will find all the files related to the
initialization, evolution, and visualization of the data. All the
sources are pure C files, plus some headers and a very few CUDA
files. Also, in this folder, you can find the main makefile
(src/makefile).  This makefile should never be called directly. All
the fundamental changes to the code must be done here.

scripts/
........

In the ``scripts/`` directory you will find the fundamental
python-scripts used at compilation time. There are scripts for:

* Defining the variables.
* Analyzing the boundary conditions.
* Analyzing and defining the units.
* Generating the CUDA files automatically.
* Improving the CUDA blocks.
* Accelerating the make process (executing the makefile in parallel).
* Making general tests (mandatory for new improvements).

bin/
....

This directory is empty by default, but during compilation, this is
where all the object files and script-residual data are stored. In
practice, this directory is useful for avoiding a mixing between
sources and objects, a very useful behavior when you are developing
new routines.

outputs/
........

The ``outputs/`` directory is the default output directory for all the
FARGO3D standard setups. As you could see in the first run, the data
were stored in ``outputs/fargo``. By default all the data is stored in
``outputs/setup_name``, where setup_name is one of the setups in the
``setups/`` directory.

setups/
.......

This directory is where all the different setups are. By default, the
make process looks here if the setup is defined, eg::

  $: make SETUP=otvortex

After that, the makefile will search inside ``setups/`` whether there
is a directory called ``setups/otvortex``. Inside the ``otvortex/``
directory we find all the files necessary to set up the problem and
build the code.

planets/
........

Inside this directory are the default planetary system files to run a
simulation with one or several planets, considered as point-like
masses that interact between them and with the disk (onto which they
act as an external potential). The syntax of planetary files is for
the former FARGO code.  It is not mandatory to store your planetary
data here, but it is recommended.

std/
....

the name ``std`` comes from "standard". This directory stores all the
standard configuration files. In this version, these are:

* ``boundaries.txt``: where the boundary conditions are defined.
* ``boundary_template.c``: A build helper for the boundaries
  scripting.
* ``centering.txt``: A file describing the centering of the different
  fields with respect to the mesh (helper for boundary conditions
  scripting).
* ``defaultflags``: A file with all the default flags for the make
  process.
* ``std.par``: Default parameters. It is used when you have not
  defined the value of a certain parameter in your parameter file. It
  is used for compatibility with some specific problems related to
  disks simulations and some plot-related parameters.
* ``standard.units``: The scaling rules for all standard real
  variables of the code.
* ``func_arch.cfg``: The standard architecture file. This file selects
  where each function will run (CPU or GPU). It only makes sense if
  the compilation was done with GPU-Compatibility (GPU=1). By default,
  all the function run on the GPU, but this file is a great tool for
  debugging the code (one of the best tools to develop a kernel!).

test_suite/
...........

This directory was developed to ensure a stable development of the
code. Here there is a set of test files written in python. All of them
use the script test.py. They are easy to understand. The main idea is:
if your recent developments pass all the tests, at least, your new
improvements do not interfere with the main code and do not alter its
behavior.

utils/
......

Here is a set of routines to analyze the data. The content inside are
self-documented. Feel free to explore it.

doc/
....

The ``doc/`` directory is where these documentation files
reside. Also, here are some files related to the license of the
code.

setups/SETUP directory
----------------------

The directory ``setups/SETUP`` is one of the most complex directories
in FARGO3D. The complexity arises because inside are stored all the
information required for a given, specific problem. The extensive list
of the files stored for each setup is:

* condinit.c: this is the file where the initial conditions are
  written. Thanks to the use of the ``VPATH`` variable in the
  makefile, this file supersedes the file ``src/condinit.c`` of the
  main source.
* SETUP.par: the parameters required for this setup.
* SETUP.opt: all the directives for the makefile (this is where you
  decide the number of dimensions, the equation of state, the
  geometry, whether you use orbital advection -aka FARGO algorithm-,
  MHD, etc.)
* SETUP.bound: set the boundary conditions used in the setup (taken
  from boundaries.txt).
* SETUP.mandatories: A list of parameters that must be always explicit
  in your .par files.
* SETUP.units: The scale rules for the parameters not explicit in
  ``std/standard_units``.
* SETUP.objects: Additional objects you want to include. (Your own
  developments).

.. warning::

   Any file here has priority over the file with the same name in the
   ``src/`` directory. So, in theory, inside a SETUP directory, you
   could have a complete copy of the ``src/`` directory, and the make
   process will be done with this sources, but in practice, only a few
   files are needed, for example, depending on your needs:
   ``resistivity.c``, ``potential.c``, etc.
