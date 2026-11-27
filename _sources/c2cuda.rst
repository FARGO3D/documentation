Cuda translator (C2CUDA.py)
============================

One of the most interesting features of FARGO3D is that it can run on
GPUs. If you look the ``src/`` directory, there are only very few
routines related with CUDA. The philosophy of the development of
FARGO3D was to avoid the kernel-writing process. Instead, following a
set of very simple rules, we were able to develop a python script that
translates the time-consuming C routines into CUDA kernels.

This section is a brief description of the rules and the process of
building CUDA kernels from  C functions.

FARGO3D Mesh Functions
-----------------------

In FARGO3D all the time-consuming functions that are called during a
hydro or MHD time step involve, without exception, a 3D nested loop
over the computational mesh. We call hereafter these functions "mesh
functions". The C to CUDA translator has been developed to convert
these "mesh functions" to CUDA kernels.

The components of any mesh function are:

* A header
* A function type and name
* Arguments
* Global variables
* Local variables
* A loop over the mesh

In some cases, the structure is a bit more complicated, including some
additional lines at the end of the main loop, but this will be discussed below.

The easiest example of a mesh function is the Pressure computation::

	#include "fargo3d.h"
	
	void ComputePressureFieldIso_cpu () {
	
	  real* dens = Density->field_cpu;
	  real* cs   = Energy->field_cpu;
	  real* pres = Pressure->field_cpu;

	  int pitch  = Pitch_cpu;
	  int stride = Stride_cpu;
	  int size_x = Nx;
	  int size_y = Ny+2*NGHY;
	  int size_z = Nz+2*NGHZ;
	
	  int i;
	  int j;
	  int k;
	
	  for (k=0; k<size_z; k++) {
	    for (j=0; j<size_y; j++) {
	      for (i=0; i<size_x; i++ ) {
		pres[l] = dens[l]*cs[l]*cs[l];
	      }
	    }
	  }
	}

As you see, the general structure is very simple. Here is the
explanation of the different blocks:

**Header**::

  #include "fargo3d.h"

This block contains all the includes required to compile the code.

**A function type**::

  void ComputePressureFieldIso_cpu () {

All the mesh functions must return a void. This is very important
because CUDA kernels cannot but return a void (this is one of CUDA
kernels limitations). Until now, the name of the function is not
important, but you can see that its suffix is (must be, actually) ``_cpu``.

**Arguments**

In this simple case, the function has no argument, but in general, you
can have a wide range of arguments. The most commons are integers,
reals & Field variables.

**Global variables** ::

  real* dens = Density->field_cpu;
  real* cs   = Energy->field_cpu;
  real* pres = Pressure->field_cpu;
  int pitch  = Pitch_cpu;
  int stride = Stride_cpu;
  int size_x = Nx;
  int size_y = Ny+2*NGHY;
  int size_z = Nz+2*NGHZ;

This block is related to all the global variables that are not passed
by argument to the function. In practice, here you have all the fields
required to achieve the calculation, the size of each loop, and some
useful variables related to indices.

**Local variables**::
  
  int i;
  int j;
  int k;

This block is devoted to variables that are neither passed as arguments nor global. Indices of the loop are always here, but it is possible to add any variable you want.

**Main Loop**::

  for (k=0; k<size_z; k++) {
    for (j=0; j<size_y; j++) {
      for (i=0; i<size_x; i++ ) {
         pres[l] = dens[l]*cs[l]*cs[l];
      }
    }
  }

This block is where all the expensive computation is done, and all the
parsing process was developed to pass this job to the GPU. Remember
that index ``l`` is a function of (i,j,k, pitch & stride), defined in
``src/define.h``. There is no need to define nor calculate it here, it is
done automatically at build time.


How the script works
--------------------

In order to develop a general GPU "function", there are a few problems that must be solved:

* Develop a proper CUDA header.
* Develop the kernel function, that is the core of the calculation.
* Develop a launcher (or wrapper) function, which is called from the C
  code and constitutes the interface between the mainstream of
  FARGO3D and the CUDA kernel.
* Perform communications between host and device (between CPU and GPU).
* Split the main loop into a lot of threads that are given to the CUDA cores.
* Develop a method for passing global variables to the kernel.
* Develop a method for passing complex structures (eg: Field) to a kernel.
* A method for switching between the C function and the CUDA function,
  are run-time (so that we can, among other things, compare the results of execution on the
  CPU to those on the GPU, in order to validate the correct GPU built).


.. This manual is not a manual of CUDA, so we will not explain the
   main features of our C to CUDA translator, but the main idea you
   have to understand is that if we can to identify the structures
   with all the information needed to do some of the points in the
   previous list, then it is straightforward to develop an automatic
   process for translating all the c-code into a cuda-code.

You can see the structure of a mesh function is really very simple,
and you can see that in all the code, the structure of mesh functions
is the essentially the same. This allows us to develop an automatic
process to generate CUDA code.  A series of special lines were
developed for simplifying the parsing process:

Here you have a complete example ::

	//<FLAGS>
	//#define __GPU
	//#define __NOPROTO
	//<\FLAGS>
	
	//<INCLUDES>
	#include "fargo3d.h"
	//<\INCLUDES>
	
	void ComputePressureFieldIso_cpu () {
	
	//<USER_DEFINED>
	  INPUT(Energy);
	  INPUT(Density);
	  OUTPUT(Pressure);
	//<\USER_DEFINED>
	
	
	//<EXTERNAL>
	  real* dens = Density->field_cpu;
	  real* cs   = Energy->field_cpu;
	  real* pres = Pressure->field_cpu;
	  int pitch  = Pitch_cpu;
	  int stride = Stride_cpu;
	  int size_x = Nx;
	  int size_y = Ny+2*NGHY;
	  int size_z = Nz+2*NGHZ;
	//<\EXTERNAL>
	
	//<INTERNAL>
	  int i;
	  int j;
	  int k;
	  int ll;
	//<\INTERNAL>
	  
	//<MAIN_LOOP>
	
	  i = j = k = 0;
	
	#ifdef Z
	  for (k=0; k<size_z; k++) {
	#endif
	#ifdef Y
	    for (j=0; j<size_y; j++) {
	#endif
	#ifdef X
	      for (i=0; i<size_x; i++ ) {
	#endif
	//<#>
		ll = l;
		pres[ll] = dens[ll]*cs[ll]*cs[ll];
	//<\#>
	#ifdef X
	      }
	#endif
	#ifdef Y
	    }
	#endif
	#ifdef Z
	  }
	#endif
	//<\MAIN_LOOP>
	}


As you see, all the main blocks are identified by some special
comments (C comments on one line begin with ``//``), but also there
are two additional blocks.

We can make an abstract portrait of a general FARGO3D's C mesh function::

  //<FLAGS>
    Your preprocessor variables here (with a heading ``//``
    sign). __GPU and __NOPROTO must be defined, as in the example.
  //<\FLAGS>

  //<INCLUDES>
    your includes here ("fargo3d.h" must be in the list) 
  //<\INCLUDES>

  function_name_cpu(arguments) {  // <== the name MUST end in ``_cpu``
    
  //<USER_DEFINED>
      Some general instructions. 
  //<\USER_DEFINED>

  //<EXTERNAL>
      type internal_name = external_variable;
      type* internal_pointer = external_pointer_cpu; // <== the name MUST end in ``_cpu``.
  //<\EXTERNAL>

  //<INTERNAL>
      type internal_name1 = initialization;
      type internal_name2;
  //<\INTERNAL>
  
  //<CONSTANT>
      //type internal_name1(1);    //Note: these lines begin with a ``//``
      //type array_name2(size);
  //<\CONSTANT>

  //<MAIN_LOOP>
    #ifdef Z
       for (k=0; k<size_z; k++) {
    #endif
    #ifdef Y
         for (j=0; j<size_y; j++) {
    #endif
    #ifdef X
	    for (i=0; i<size_x; i++ ) {
    #endif
  <#>
           Anything you want here.
  <\#>
    #ifdef X
            }
    #endif
    #ifdef Y
         }
    #endif
    #ifdef Z
       }
    #endif
  //<\MAIN_LOOP>

  //<LAST_BLOCK>
      Some final instruction(s).
  //<\LAST_BLOCK>

  }

Below, there is an explanation of each field, and how to use it. You
can browse the source files of mesh functions to see examples. You can
have the list of the corresponding files by having a look at
``src/makefile``. There, you see a block called GPU_OBJBLOCKS. All the
mesh functions are found in the files that have the same prefix as
those found in this list, but with a ``.c`` suffix instead of
``_gpu.o``.

FLAGS
......

**Identifier** ::

  <FLAGS> ... <\FLAGS>

**Parsed as**::

  Textually, with heading comment sign removal.

**Location**::

  Normally, at the top of a  C file.


There are two flags that must be always included::

  //#define __GPU
  //#define __NOPROTO

They are important for a proper header building.

The __GPU  can be used inside a C mesh function to issue specific
lines that should be run only on the GPU version, with the help of the
macrocommand::
  
  #ifdef __GPU
  #endif

INCLUDES
.........

**Identifier** ::

  <INCLUDES> ... <\INCLUDES>

**Parsed as**::

  Textually

**Location**::

  Normally, after the FLAGS block.

The INCLUDES block is the block where all the headers are.
This block must contain at least::

  #include "fargo3d.h"

You may include any other header file.


Function name:
..............

**Identifier** ::

  Implicit, only a string 

**Parsed as**::

  function_name_cpu --> function_name_gpu (for the wrapper or launcher)
                    --> function_name_kernel (for the associated CUDA kernel)

**Location**::

  Normally, after the INCLUDES block.


Arguments:
..........

**Identifier** ::

  Implicit, only a string 

**Parsed as**::

  Field* f --> real f->field_gpu
  non pointer argument --> textually

**Location**::

  Normally, after the INCLUDES block.


Any built-in type is allowed, including FARGO3D's real type. The only
structure allowed is the "Field" structure.

There are two constraints about the arguments field:

* All must be on the same line.
* The Field structures are the last arguments.


USER DEFINED:
.............

**Identifier** ::

  <USER_DEFINED> ... <\USER_DEFINED>

**Parsed as**::

  Textually

**Location**::

  After the function name.

This block can be very general. You can do here a lot of things,
because there is no limitation on syntax, everything inside is parsed
textually. In practice, we use this block mainly to do memory
transfers between host & device when they are needed, by issuing INPUT
and OUTPUT directives.

This block is a kind of pre kernel-execution instructions, will be
executed before the kernel launch, by the launcher (or wrapper)
function.

In a similar way, the post kernel-execution is the block called
LAST_BLOCK.


EXTERNAL:
.........

**Identifier** ::

  <EXTERNAL> ... <\EXTERNAL>

**Parsed as**::

  All the external variables are parsed as arguments of the kernel.
  type variable = global_variable_cpu --> function_name_kernel(type global_variable_gpu)
  type* variable = global_variable_cpu --> function_name_kernel(type* global_variable_gpu)

**Location**::

  After the USER_DEFINED block.


The CUDA kernels cannot see the global host variables. This block is
meant to grant access to these variables to the kernels so that all
the variables dealt with in this block are global. The main rule when
your draw a list of global variables inside the EXTERNAL block is:

* Avoid the use of all capital variables. Instead, declare another
  variable with the same name but without capitals, and declare the
  variable equal to the global variable. example: (real omegaframe =
  OMEGAFRAME).

INTERNAL:
.........

**Identifier** ::

  <INTERNAL> ... <\INTERNAL>

**Parsed as**::

  Textually

**Location**::

  Normally, after the EXTERNAL block.

All the internal variables are work variables, with a very local
scope. You find here the indices of the loops, but you could include
any other variable that you need. Maybe, one of the most interesting
examples on how to use this block is found in ``compute_force.c``.

CONSTANT:
.........

**Identifier** ::

  <CONSTANT> ... <\CONSTANT>

**Parsed as**::

  The variables inside are moved to the constant memory if BIGMEM
  is not defined. If BIGMEM is defined, the variables are moved instead to the
  device's global memory.  Example:

  <CONSTANT>
  // real ymin(Ny+2*NGHY+1);
  <\CONSTANT>

  Is parsed as:

  #define ymin(i) ymin_s[(i)]

  ...

  CONSTANT(real, ymin_s, some_number); 

  Here, some_number is a fraction of the constant memory size, calculated
  by the parser.

  ...

  #ifdef BIGMEM
  #define ymin_d &Ymin_d
  #endif
  CUDAMEMCPY(ymin_s, ymin_d, sizeof(real)*(Ny+2*NGHY+1), 0, cudaMemcpyDeviceToDevice);

  ...

**Location**::

  Normally, after the INTERNAL block.


This is one of the most complex blocks. It is very complex because the
process is complex. We need a way to pass our light arrays to the
constant memory of the GPU (for performance reasons). But there are
some cases where the problem is too big and the constant memory is not
enough. In this case, one can define the build flag BIGMEM. The main
portrait of the process is:

Declare as constant some global variables you want to use without
passing it as external, or use this block for light arrays, similar to
``xmin``, ``sxk``, etc. This block reserves a constant memory segment
and copy the data to this segment. If BIGMEM is activated, the
constant memory is not used but instead, the global memory is
used. CUDAMEMCPY macrocommand is expanded in a manner that depends on
whether BIGMEM is defined and therefore performs the copy to the
correct location (constant or global memory). You can see this in
``src/define.h``. Note that there is a subtlety here: in case you use
BIGMEM, the constant memory is still used to store the pointer to the
array. In the other case, it stores directly the array itself. The
variables for this block are created in ``src/light_global_dev.c``.

The scalar variables are passed as::
  
  // type variable(1)
 
While the array variables are passed as::

  // type variable(size_of_the_array)

Note that all this block is commented out in the C file, with ``//`` at
the beginning of each line.

MAIN LOOP:
..........

**Identifier** ::

  <MAIN_LOOP> ... <\MAIN_LOOP>

**Parsed as**::

  The size of the loops is read and parsed. Also, the indices are initialized:

  Example:

	#ifdef Z
	  for (k=NGHZ; k<size_z; k++) {
	#endif
	#ifdef Y
	    for (j = NGHY; j<size_y; j++) {
	#endif
	#ifdef X
	      for (i = 0; i<size_x; i++) {
	#endif

  is parsed to:

	#ifdef X 
	i = threadIdx.x + blockIdx.x * blockDim.x;
	#else 
	i = 0;
	#endif 
	#ifdef Y 
	j = threadIdx.y + blockIdx.y * blockDim.y;
	#else 
	j = 0;
	#endif 
	#ifdef Z 
	k = threadIdx.z + blockIdx.z * blockDim.z;
	#else 
	k = 0;
	#endif
	
	#ifdef Z
	if(k>=NGHZ && k<size_z) {
	#endif
	#ifdef Y
	if(j >=NGHY && j <size_y) {
	#endif
	#ifdef X
	if(i <size_x) {
	#endif

  The content of the loop is parsed textually, but formally, the
  content is part of another block: "<#> <\#>".

**Location**::

  Before the initialization of the indices i,j,k.


This block is very particular because it must to be closed after the
close of the outermost loop. Remember that the content of the main
loop block, defined by ``<#>..<\#>``, nested within the MAIN_LOOP
block, is parsed textually, so you cannot use global variables inside
it or the generated CUDA code will not work.


LOOP CONTAIN:
.............

**Identifier** ::

  <#> ... <\#>

**Parsed as**::

  Textually.

**Location**::

  After the innermost loop or where you want to have a textual
  parsing inside the main_loop.

If you put the beginning of this block not exactly after the innermost
loop, you can make some interesting things. With this technique, you
can skip some lines devoted to the CPU. You can also achieve this with
the ``_GPU`` flag declared at the beginning, as shown earlier.


LAST_BLOCK
..........

**Identifier** ::

  <LAST_BLOCK> ... <\LAST_BLOCK>

**Parsed as**::

  Textually.

**Location**::

  The last block in the routine.

This block will be executed after the kernel execution. Useful for
reductions, for instance.



Common errors:
--------------

This section describes the most common errors at compilation time using the parser:

* The name of a block has white spaces: all blocks declarations must
  be closed and after that white spaces are not allowed::
    
    <BLOCK>__  --> wrong
    <BLOCK>    --> ok

* The pointer type is not a type: For the parser, the type of a
  variable is a string without spaces. A pointer variables must be
  declared as the pointer type::
    
    real *rho  --> wrong
    real* rho  --> ok (the type is real*)


* Some block was not properly closed: if you have not closed a block,
  undefined behavior may result::

    <BLOCK>
    <BLOCK>      --> wrong

    <BLOCK>
    </BLOCK>     --> wrong

    <BLOCK>
    <\BLOCK>     --> ok


* The end of the name function is not _cpu: The parser cannot find
  the function name if it does not have a valid name, neither can it
  invent a rule to make the wrapper and kernel names.

* The order of the arguments in the function: Remember, pointers to
  Field structures are at the end.

* Only one variable per line may appear in the INTERNAL and EXTERNAL fields.

* Files which have been edited on a Windows machine, and in which
  lines end with '\r\n' instead of ending with '\n', will fail to be
  converted to CUDA. Use a conversion procedure such as ``tr -d '\d' <
  original_file.c > correct_line_ending.c`` prior to the build.

* Values relative to the mesh (such as ``zmin`` or ``xmed``, etc.)
  should be lowercase and should be followed by parentheses, not
  square brackets, because they are considered as macrocommands. You
  can use ``substep1_x.c`` as a template for that.

* Leaving an empty line within the EXTERNAL block::

    <EXTERNAL>
        some variable
        ___           ----> wrong
    <\EXTERNAL>
    <EXTERNAL>
        some variable ----> ok
    <\EXTERNAL>

* Block opening/closing not in first column::

    __<EXTERNAL>
	This block will not be parsed
    __<\EXTERNAL>
    <EXTERNAL>
	This block will be parsed
    <\EXTERNAL>

This list may be completed as we receive users' feedback.
