Units
=======

Introduction
-------------

Unlike its ancestor FARGO, FARGO3D comes with a variety of unit
systems. The reason for this is twofold:

- Working in a different unit system may help reveal bugs. Let us take
  a simple example to illustrate this: assume that somewhere in an
  azimuthal derivative calculation, a developer has divided by the
  angular step rather than the linear one (or vice-versa), i.e. he has
  forgotten to divide (or multiply) by the cylindrical radius. When
  working in scale-free units, where one usually takes radii
  commensurable to one, this mistake may remain unnoticed for a long
  time, especially if it is hidden in a part which has a small impact
  on the evolution of the flow (such as the viscous stress tensor, for
  instance). If one switches to *MKS* or *cgs*, where the radii have
  values which are typically 10 to 14 orders of magnitude larger, such
  errors appear straight away. In fact, we have developed tests to
  check the dimensional homogeneity of all parts of the code. We run
  it a first time in a given system of units, then we rerun it in
  another system of units and check that the ratio of the two outputs
  is flat, to the machine precision. You may have a look at the test
  named dimp3diso.py in the directory test_suite/. You can run it from
  the main directory by issuing::
 
         make testdimp3diso

- The other reason for implementing a variety of unit systems comes
  from the user feedback of the FARGO code. About half of the
  questions that we received on the code had to do with
  units. Besides, as the code gains in complexity, by the inclusion of
  MHD or radiative transfer, it may become desirable to switch to a
  standard system of units, where constants have a well-known value
  (if you are not convinced, try to work out what is the value of
  Stefan's constant in a system of units where the solar mass is the
  mass unit, one astronomical unit the length unit, such that *G*, the
  gravitational constant, has value one, and where the ratio of the
  ideal gas constant over the mean molecular weight has also value
  one). Finally, the output of FARGO3D may be used by third party
  codes, such as radiative transfer codes that produce a simulated
  image, and having the data in a standard unit system may prove useful.

Specifying the unit system
--------------------------

The unit system must be specified at build time. The different systems
are defined in the file named "fondam.h".  The unit system used to
build the code depends on whether the preprocessor variable MKS, or
CGS, is defined. If none of them is defined, a trivial unit system
(dubbed "scale-free") is adopted. From the makefile, activating one or
another of these preprocessor variables is done as follows::

              make UNITS=MKS

or::

              make UNITS=CGS

Finally, to use the scale-free system of units, issue::

              make UNITS=0


.. note::
  As other build options, the UNITS flag is sticky: is keeps implicitly
  its previous value until it is changed explicitly.


We note that specifying the unit system in the FARGO3D code is done by
giving a numerical value to five constants that have linearly
independent powers of :math:`M`, :math:`L`, :math:`T`, :math:`\theta`
and :math:`I` (mass, length, time, temperature and electric
intensity). These constants are the gravitational constant :math:`G`
(G, with units :math:`M^{-1}L^3T^{-2}\theta^0I^0`), the central star
mass :math:`M_\star` (MSTAR, with units
:math:`M^{1}L^0T^{0}\theta^0I^0`), a length :math:`R_0` (R0, with
units :math:`M^{0}L^1T^{0}\theta^0I^0`), the ratio of the ideal gas
constant to the mean molecular weight :math:`{\cal R}/\mu` (R_MU, with
units :math:`M^{0}L^2T^{-2}\theta^{-1}I^0`), and the value of the
magnetic permeability of vacuum :math:`\mu_0` (MU0, with units
:math:`M^1L^1T^{-2}\theta^{0}I^{-2}`).


Naturally, if you specify the CGS unit system, your parameter file
must provide all real variables in this unit system: YMIN/YMAX must be
in centimeters, and so must be ZMAX/ZMIN in cylindrical or Cartesian
coordinates, and XMIN/XMAX in Cartesian coordinates. Similarly, NU
must be in cm^2/s, the planetary mass in the .cfg file must be in
grams, and so on and so forth. There is, however, an exception to this,
when one uses the RESCALE directive, as we explain below.

Rescaling the input parameters
----------------------------------------

Previous users of FARGO are certainly used to scale-free input
parameters, in which the central star mass is set to one, the planet's
orbital radius set to one, and the gravitational constant set to
one. The orbital period is, therefore :math:`2\pi`. You may require
that FARGO3D be run in a unit system such as cgs or MKS, without
editing your scale-free parameter file. For this purpose, you must
build FARGO3D with the rescale option::

         make UNITS=MKS RESCALE=1

Once the parameters are read from the parameter file, they are
rescaled using rescaling rules. For instance, the value of YMIN (the
mesh minimal radius, in cylindrical or spherical geometry) is
multiplied by :math:`R_0`. Similarly, the value of SIGMA0 (the disk's surface
density, if your setup uses one) is multiplied by
:math:`M_\star/R_0^2`, etc. This allows to get an output in a standard
unit system while keeping scale-free input files, the content of which
is probably more intuitive.

Specifying the scaling rules
------------------------------------------------

A *scaling rule* for a variable is a product of the five dimensionally
independent variables
(:math:`G`,
:math:`M_\star`,
:math:`R_0`,
:math:`{\cal R}/\mu` and
:math:`\mu_0`), each raised to a specific power, that determines
uniquely the dimension of a variable. A scaling rule for a given
variable is unique. If it is cast incorrectly, the code will not pass
the homogeneity test (if this variable is used in the setup tested).

The scaling rules are required exclusively if you build the code with
the *RESCALE* flag activated, so as to have a dimensional output with
scale-free input parameters. You can have a look at the file
``std/standard.units``. You can see that each line looks like C code
(no ; is required at the end), and the right-hand side of the \*=
symbol has the same unit as the left-hand side. The scaling rules for
some variables is trivial (e.g. SIGMA0, which is a surface density, or
PLANETMASS, which is a mass).

During the make process the python script ``scripts/unitparser.py``
is run, which scans all real variables known to the code (that is
everything in the setup .par file found to be a real value). If
it finds it in the scaling rules it has access to (those of
``std/standard.units``
plus, if any, in ``setups/SETUP/SETUP.units``, in case your setup
defines new real variables), it copies that rule in a file made
automatically that is called ``rescale.c``, and which contains the
rescaling routine called before entering the main loop if you have
made a built with the *RESCALE* option.

If it does not find a scaling rule for a variable it issues a warning
asking to check whether this variable is dimensionless. Since the
output of this script is found at the very beginning of the make
process, and may be unnoticed, it can be a good idea to run the script
separately. You have to do that from the ``src/`` directory::

  $ cd src
  $ python ../scripts/unitparser.py mri
  Warning ! Scaling rule not found for FLARINGINDEX. Is it dimensionless ?
  Warning ! Scaling rule not found for SIGMASLOPE. Is it dimensionless ?
  Warning ! Scaling rule not found for BETA. Is it dimensionless ?
  Warning ! Scaling rule not found for NOISE. Is it dimensionless ?
  Warning ! Scaling rule not found for ASPECTRATIO. Is it dimensionless ?

You can verify that each of the variables found by the script is
indeed dimensionless. This list is naturally setup dependent, and the
above example is for the set ``mri``.

.. warning:: 
   Upon completion of the manual run of the script as above, you MUST
   go to the ``../bin`` directory and remove *manually* the file
   ``rescale.c`` leftover by the script. Otherwise, for dependency
   reasons, the makefile will not remake it automatically at the next build.



