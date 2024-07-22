.. _optfiles:

.opt files
===========

FARGO3D is a very versatile code. It can solve from a very simple
sod shock tube test to a tridimensional problem with MHD. In order to
keep the versatility without a performance penalty, we have adopted an
extensive use of macrocommand variables. These variables allow one to
activate/deactivate a lot of sections of the code depending on what we
want to solve. For example, if we want to solve a 2D planetary disk
without MHD, the code does not need to know anything about MHD. In this
case, an "``if`` run time sentence checking whether we want to use MHD
or not, would be
expensive. With the help of this ``compiler`` variables through
``#ifdef`` statements, all the
job is done at compilation time.

Most of these variables are defined in the ``.opt`` file, but there
are other ones (for example *FARGO_DISPLAY*), that are defined during the
:ref:`MakePro`.


The variables must be defined inside a container variable, called
``FARGO_OPT``, as follows ::

   FARGO_OPT += -DVARIABLE.

In this version, the list of options/modules that can be activated from the ``.opt`` file is:

------------------------------------------------------------------

**Fluids**

These options are mandatory (see :ref:`ref_multifluid`)

* FLUIDS := 0 1 2 (list starting from 0,...,N-1, with N the number of fluids)
* NFLUIDS = 3     (total number of fluids)
* FARGO_OPT += -DNFLUIDS=${NFLUIDS} (mandatory line in the .opt file)

* DRAGFORCE: Activates the drag force between fluids.
* STOKESNUMBER: The collision rate is computed assuming fluids with constant Stokes Number (in linear regime).
  
------------------------------------------------------------------

**Performance**:

* FLOAT: Uses single precision floating point data. On GPUs,
  the code runs ~2x times faster. If FLOAT is not defined, the code will be run in double precision. 

------------------------------------------------------------------

**Dimensions**:

* X: Activates the X direction.
* Y: Activates the Y direction.
* Z: Activates the Y direction.

Note: Some fields are not available until one specific direction is activated.

------------------------------------------------------------------

**Equation of state**:

* ADIABATIC: The equation of state :math:`P=(\gamma-1)e` will be
  used. The field *Energy* is the volumic internal energy :math:`e`.
* ISOTHERMAL: The equation of state :math:`P=cs^2\rho` will be used.
  The (ill-named) field Energy is then the sound speed of the fluid.

------------------------------------------------------------------

**Additional Physics**:

* MHD: Activates the MHD solver. The options X, Y & Z must be all activated. The options below are enabled for MHD runs.
    * STRICTSYM: It enforces a strict symmetry of the MHD solver.
    * OHMICDIFFUSION: Activates Ohmic resistivity.
    * AMBIPOLARDIFFUSION: Activates ambipolar diffusion.
    * HALLEFFECT: Activates the Hall effect. 
* VISCOSITY: Activates the viscosity module with a constant kinematic viscosity defined by the parameter ``NU``.
* ALPHAVISCOSITY: Activates the viscosity module with a constant alpha viscosity defined by the parameter ``ALPHA`` (Shakura-Sunyaev (1973) Viscosity Prescription).
* POTENTIAL: Activates the gravity module.
* STOCKHOLM: Activates wave killing boundary conditions in Y & Z. Very
  useful for local studies where reflections on the edges must be avoided.
* HILLCUT: Activates a cut for the force computation. Must to be
  defined in order to accept ``ExcludeHill`` parameter file
  variable set to ``yes``.

------------------------------------------------------------------

**Coordinates**:

* CARTESIAN: x,y,z are Cartesian.
* CYLINDRICAL: x --> azimuthal angle, y --> cylindrical radius, z --> z.
* SPHERICAL: x --> azimuthal angle, y --> spherical radius, z --> colatitude.

------------------------------------------------------------------

.. _shearingbox-flags:

**Shearing box**:

Enable Cartesian coodinates (``-DCARTESIAN``) and then add

* SHEARINGBOX: Enables the shearing-box terms.
* SHEARINGBC: Enables shearing-periodic boundaries

.. warning::
	shearing-periodic boundaries only work on the CPU.

------------------------------------------------------------------

**Transport**:

* RAM: Enables the Rapid Advection Algorithm on Arbitrary Meshes (Benítez-Llambay et al. 2023).
  RAM is a time-explicit method to solve the advection equation in problems with large bulk velocity,
  allowing to increase the time step significantly on both uniform and non-uniform domains.
* STANDARD: Forces the standard advection algorithm in x. By default,
  the x-advection is done with the orbital advection (FARGO) algorithm.

------------------------------------------------------------------

**Slopes**:

* DONOR: Activates the donor cell flux limiter for the
  transport. Actually, deactivates the default van Leer's second order
  upwind interpolation.

------------------------------------------------------------------

**Artificial Viscosity**:

* NOSUBSTEP2: If it not defined, the artificial viscosity module, called ``Substep2()``, is invoked.
* STRONG_SHOCK: If strong shocks make the code crash, you may try
  using this variable. It is never used in the tests. It uses a
  linear, rather than quadratic, artificial pressure.

------------------------------------------------------------------

**Boundaries**

* HARDBOUNDARIES: simplifies the creation of boundary files by hand (see :ref:`ref_hardboundaries`)

  
------------------------------------------------------------------


**Cuda blocks**:

The cuda blocks must be defined in the form::

	ifeq (${GPU}, 1)
	FARGO_OPT += -DBLOCK_X=16
	FARGO_OPT += -DBLOCK_Y=8
	FARGO_OPT += -DBLOCK_Z=4
	endif

This is needed to define a default block size for GPU
kernels. Alternatively, for a given platform, you may determine
individually for each CUDA kernel ("routine") which block size gives
best results.

.. seealso:: :ref:`performance`

------------------------------------------------------------------

There is a special set of variables not contained in the FARGO_OPT variable::

	MONITOR_2D
	MONITOR_Y
	MONITOR_Y_RAW
	MONITOR_Z
	MONITOR_Z_RAW
	MONITOR_SCALAR

Those are used *at build time* to request systematic, fine grain monitoring.
The meaning of these variables is explained in :ref:`ref_monitoring`.
