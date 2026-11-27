Mesh and Fields
================

Mesh
-----

The mesh consists of NX cells in X (hence azimuth in cylindrical and
spherical geometries), NY+2*NGHY cells in Y (radius in cylindrical and
spherical geometries) and NZ+2*NGHZ cells in Z (colatitude in
spherical geometry). Here NGHY and NGHZ stand for the number of ghost
or buffer zones next to the active mesh. If a direction is not
included in the setup (for instance Z in the 2D polar ``fargo``
setup), the corresponding value of NGHY/Z is set to 0.

The variables NX, NY, and NZ are defined in the parameter file (they
default to 1, so there is no need to define, for instance, NZ in a 2D
setup such as ``fargo``, or NX in the 2D setup ``otvortex``, which
corresponds to the Orszag-Tang vortex problem in Y and Z).

In practice, this mesh is split among processors, and locally (within
the scope of a given process) the submesh considered has size Nx,
Ny+2*NGHY and Nz+2*NGHZ.

The information about cells coordinates is stored in 1D arrays

* [xyz]min(index)
* [xyz]med(index)

where *min* refers to the inner edge of a zone (in x, y or z) whereas
*med* refers to the center of a zone (in x, y or z). This notation
should look familiar to former FARGO users.

.. warning::
   [xyz][min/max](index) are not vectors, they are macrocommands. They
   must be invoked with (), not with [].

NGHY and NGHZ are preprocessor variables, defined in the file ``src/define.h``.

Because we have a multi-geometry code, another set of secondary
geometrical variables is defined (surfaces, volumes).
See the end of this section for details.


Fields
------

Fields are structures, and they can be seen as cubes of cells, of size
equal to the mesh size. The location at which a given variable is defined is [xyz]med if
the field is [xyz]-centered, or [xyz]min if the field is
[xyz]-staggered. You can find a comprehensive list of the fields in
``src/global.h``. The place where the fields are created is in
``CreateFields()``, inside ``src/LowTasks.c``.

Internally, all fields are cubes written as 1D-arrays. So we need
indices to work with the 3D-data. We have a set of helpers defined in
``src/define.h``. They are:

* ``l`` : The index of the current zone.
* ``lxp``, ``lxm``: lxplus/lxminnus, the right/left x-neighbor
* ``lyp``, ``lym``: lyplus/lyminnus, the right/left y-neighbor
* ``lzp``, ``lzm``: lzplus/lzminnus, the right/left z-neighbor

These helpers must be used with the proper loop indices::

   int i,j,k;

   for (k=z_lower_bound; k<z_upper_bound; k++) {
     for (j=y_lower_bound; j<y_upper_bound; j++) {
       for (i=x_lower_bound; i<x_upper_bound; i++) {
          field[l] = 3.0;
          field2[l] = (field1[lxp]-field1[l])/(xmed(ixp)-xmed(i));	  //obviously some gradient calculation...
       }
     }
   }

where [kji] always means [zyx]-direction. 

.. warning:: 
   Do not change the order of the indices! The definition of ``l``,
   ``lxp``, ``lxm``, etc. assumes the following correspondence:

   i->x, j->y, k->z

These helpers are extremely useful. No explicit algebra has to be
performed on the indices within a loop (but never use or define a
variable called ``l`` or ``lxp`` !...). Besides, the definition of
``l`` is also correct within GPU kernels (for which the indices
algebra is slightly different owing to memory alignment
considerations), and this is totally transparent to the user who
should never have to worry about this.

In practice, a loop is similar to (isothermal equation of state):

::

          int i,j,k;

	  for (k=0; k<Nz+2*NGHZ; k++) {
	    for (j=0; j<Ny+2*NGHY; j++) {
	      for (i=0; i<Nx; i++ ) {
		pres[l] = dens[l]*cs[l]*cs[l];
	      }
	    }
	  }

.. note::
   Note that the lines of code above do not evaluate, nor define
   ``l``, which is used straight out of the box, since it is a
   preprocessor macrocommand.

Working with fields
--------------------

A field structure is defined as follows (in ``src/structs.h``)::

    struct field {
      char *name;
      real *field_cpu;
      real *field_gpu;
    };

where we have stripped the definition of all extra lines not relevant
at this stage. The ``name`` is a string that is used to determine the
name of output files. ``field_cpu`` is a pointer to a double or float
1D array which has been duly allocated on the RAM prior to any
invocation.

Similarly  ``field_gpu`` is a pointer to a double or float 1D array
which has been duly allocated on the Video RAM prior to any
invocation. The user should never have to invoke directly this
field. Rather, C files will always make use of the ``field_cpu``,
which will be automatically translated to ``field_gpu`` as needed
during the C to CUDA conversion.

Acceding a field value is generally done as follows::

   struct Field *Density;       // Definition at the beginning of a function
   real *density;                   // real is either double or float.
   density = Density->field_cpu;
   ...
   later on in a loop:
   ...
     density[l] = ....;

.. note::

   Note that we define an "array of reals" straight away and
   subsequently only refer to it to manipulate cell values. In order to
   avoid confusion, it is a good idea to have an upper case for the
   initial of Fields*, and lower case for the corresponding real arrays.


Fields on the GPU
-----------------

Similar techniques are used on the GPU, but we have made it totally
transparent to the user, so unless you want to program your CUDA kernels
directly, you should never to worry about this.


Useful variables
-----------------

For the handling of the mesh, a set of useful variables and
macrocommands has been defined. An extensive list with a description is
given below:

_______

**Indices**:

* ``l``: The index of the current cell. It is a function of (``i``,``j``,``k``, ``pitch`` & ``stride``).
* ``lxp``: The index of the "right" neighbor in x of the current 
  cell. It is a function of ``l``. 
* ``lxm``: The index of the "left" neighbor in x of the current 
  cell. It is a function of ``l``. 
* ``lyp``: The index of the "right" neighbor in y of the current 
  cell. It is a function of ``l``. 
* ``lym``: The index of the "left" neighbor in y of the current 
  cell. It is a function of ``l``. 
* ``lzp``: The index of the "right" neighbor in z of the current 
  cell. It is a function of ``l``. 
* ``lzm``: The index of the "left" neighbor in z of the current 
  cell. It is a function of ``l``. 
* ``l2D``: The current index in a 2D field (eg: vmean). It is a function of (``j``,``k``).
* ``l2D_int``: The current index in a 2D integer field (eg: a field of
  shifts). It is a function if (``j``,``k``).
* ``ixm``: ``i``-index of the "left" neighbor in x of the current 
  cell, taking periodicity into account. 
* ``ixp``: ``i``-index of the "right" neighbor in x of the current 
  cell, taking periodicity into account. 

_______

**Coordinates**:

* ``XC``: center of the current cell in X. It is a function of the indices; must to be used *inside a loop*. 
* ``YC``: center of the current cell in Y. It is a function of the indices; must to be used *inside a loop*. 
* ``ZC``: center of the current cell in Z. It is a function of the indices; must to be used *inside a loop*. 
* ``xmin(i)``: The lower x-bound of a cell.
* ``xmed(i)``: The x-center of a cell,   same as XC but can be used outside a loop.
* ``ymin(j)``: The lower y-bound of a cell.
* ``ymed(j)``: The y-center of a cell,  same as YC but can be used outside a loop.
* ``zmin(k)``: The lower z-bound of a cell.
* ``zmed(k)``: The z-center of a cell,  same as ZC but can be used outside a loop.

________

**Length**:

* ``zone_size_x(j,k)``: Face to face distance in the x direction.
* ``zone_size_y(j,k)``: Face to face distance in the y direction.
* ``zone_size_z(j,k)``: Face to face distance in the z direction.
* ``edge_size_x(j,k)``: The same as zone_size_x, but measured on the  lower x-border.
* ``edge_size_y(j,k)``: The same as zone_size_y, but measured on the lower y-border.
* ``edge_size_z(j,k)``: The same as zone_size_z, but measured on the lower z-border.
* ``edge_size_x_middlez_lowy(j,k)``: The same as edge_size_x but measured half a cell above in z.
* ``edge_size_x_middley_lowz(j,k)``: The same as edge_size_x but measured half a cell above in y.

________

**Surfaces**:

* ``SurfX(j,k)``: The lower surface of a cell at x=cte.
* ``SurfY(j,k)``: The lower surface of a cell at y=cte.
* ``SurfZ(j,k)``: The lower surface of a cell at z=cte.

________


**Volumes**:

* ``Vol(j,k)``: The volume of the current cell.
* ``InvVol(j,k)``: The inverse of the current cell's volume.

________


You can see examples on how to use these variables in ``src/``. They
are widely used in many routines.
