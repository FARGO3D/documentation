N-Body solver
=============

Introduction
-------------

One feature that FARGO3D has inherited from its ancestor FARGO is the
possibility to include a number of point-like masses which can
interact between themselves and which can also gravitationally
interact with the gas. The set of such masses is defined in a
file. This file must be defined in the parameter file with the
parameter `PlanetConfig`. For instance, in the default parameter file
of the fargo setup (that is, ``setups/fargo/fargo.par``), we find the
line::

  PlanetConfig    planets/jupiter.cfg

Throughout this chapter, we call this file the *config file*, or the
*planetary configuration file*.
The content of this file is strictly similar to that defined in the
previous FARGO code::

  ###########################################################
  #   Planetary system initial configuration
  ###########################################################
  
  # Planet Name 	Distance	Mass	 Accretion	Feels Disk	Feels Others
  Jupiter		 1.0		0.001	 0.0	  	NO		NO

Lines beginning with a '#' are ignored. A line containing a valid
planet definition must begin with a letter ('a-z' or 'A-Z'). So far
this name is not reflected in the code output, but it gives a sense
of what kind of planet or planetary system is intended. The second
column gives the semi-major axis in units of `R0`, defined in
`src/fondam.h`. The third column gives the planetary mass in units of
`MSTAR`, defined also in `src/fondam.h`. The fourth column, relative
to accretion, is not used at the present time. So far its only
purpose is to allow backward compatibility with FARGO's planetary
config files. Finally, the content of the last two columns, which is
self-explanatory, indicates whether the planet feels the gravity of
the other planets and whether it feels the gravity of the disk.

.. note::
   Our N-Body solver is a simple fifth order Runge-Kutta
   integrator. This may seem pretty simplistic compared to way more
   sophisticated N-body integrators, which are tailored to follow the
   dynamics of a collection of point-like masses in vacuum over very
   long timescales. It should be remembered that our primary purpose
   is the study of protoplanets embedded in disks. The lifetime of the
   disk is 3 to 4 orders of magnitude shorter than the age of the
   Solar System, and the variation of total energy of planet under a
   disk tide is usually many orders of magnitude larger than that
   inherent to our scheme. The latter is therefore perfectly fine for
   our purpose.

The planets are initialized at :math:`t=0` such that they lie on the
:math:`x` axis, are prograde with the disk, have all same
eccentricity (defined by the parameter `ECCENTRICITY`, which defaults
to zero). Their initial location corresponds to apoastron.

.. warning::
   By default, a central star of mass `MSTAR` (defined in
   `src/fondam.h`) is added at the mesh center. This default behavior
   can be superseded, for instance, to have the mesh centered on the
   center of gravity of the system, or to have a binary star at the center.

The value of `MSTAR` is used to initialize the orbits of the planets,
in all cases.

.. _ref_nodefaultstar:

Removing the default central star
--------------------------------------

In some cases, you want to remove the default central star which is
assumed to exist at the mesh center. In order to do so, so simply need
to add the following line to your `.opt` file and rebuild::

  FARGO_OPT += -DNODEFAULTSTAR


Planets which are stars 
--------------------------------------

Starting from version 1.2, FARGO3D detects in the configuration file
of the planetary system which objects are massive enough to be
considered as stellar, and deals with them in a specific way. Our
arbitrary threshold, defined in `src/fondam.h`, is `0.05*MSTAR`, which
would correspond to a typical brown dwarf if `MSTAR` is one solar
mass. This threshold can be redefined depending on the user's
needs. The number of *stellar* objects detected in the configuration
file can be 0, 1 or 2. Beyond this number, an error message is issued.

The array below summarizes a variety of possible setups. The first
line corresponds to the default behavior. The last two columns
indicate whether the user should define `NODEFAULTSTAR` (in the opt
file) and what value should be given to `MSTAR` (in
`src/fondam.h`). Note that whenever `NODEFAULTSTAR` is defined, all
stellar objects must be explicitly given in the configuration file.

+-------------------------+---------------------+----------------------------+
| Intended setup          |   `NODEFAULTSTAR`   |   `MSTAR`                  |
+=========================+=====================+============================+
| One star at mesh center |                     |     mass of central star   |
+-------------------------+---------------------+----------------------------+
| One star. The mesh is   |                     |                            |
| centered on the center  |    Defined          |     mass of central star   |
| of mass of the star and |                     |                            |
| planets.                |                     |                            |
+-------------------------+---------------------+----------------------------+
| Circumbinary disk       |    Defined          |     mass of binary         |
+-------------------------+---------------------+----------------------------+
| Circumstellar disk in   |                     |     mass of star at disk   |
| binary system           |                     |     center                 |
+-------------------------+---------------------+----------------------------+

.. note::
   What is the reason for defining manually `MSTAR` in the second and
   third rows of this table ? The reason is that this variable is used
   throughout the code to perform a variety of tasks, such as:

   * initialization of the planetary orbits
   * evaluation of the Roche radius (for potential smoothing issues)
   * evaluation of the planet's orbital elements

   so it is important that its value matches that of the mass of the
   object(s) at the disk center. Also, note that the `orbit[i].dat`
   output files contain correct values only for the first kind of
   setup.

   When one uses the third setup in the array above, the code enforces
   that the mesh be centered on the center of mass of the binary (and
   not of the system), and the components of the binary start do not
   feel the gas or the planets. The indirect term, if included, arises
   from the acceleration of both components of the binary, weighted by
   their mass. See the setup ``binary`` for an example.

Initialization of the position and velocities of the stellar objects
------------------------------------------------------------------------

The initial position
and velocity of the stellar objects differ from that of the planets,
in the case in which there is no default central star.

If one stellar object is given, its position and velocity is set so
that the center of mass of the planets and star is at the mesh
center, and so that this point does not move with respect to the mesh.

If two stellar objects are found, the parameters of the second column
of the config file, usually devoted to the distance to the star, takes
a different meaning. For the first star, the value found is used as
the binary period, and for the second star, the value found is used as
the binary eccentricity. The binary system is initialized on the :math:`x`
axis, at apoastron, and the first star has :math:`x>0`. The mesh is centered
on the center of mass of the binary. See the file
``planets/Kepler38.cfg`` for an example.

Indirect term
-------------------------
Whenever the center of the frame is accelerated, an additional
potential term, called the indirect term, is added to the potential,
which corresponds to the fictitious force arising from the frame
acceleration.  This indirect term can be purposely discarded, by
setting the parameter ``IndirectTerm`` to ``NO`` (the default is
``YES``).


Initial eccentricity and inclination
---------------------------------------
All objects are initialized with the same eccentricity, defined by the
``ECCENTRICITY`` parameter (its default value is zero), and they are
initially set at apoastron. If a different setup is needed, some
edition of the file ``src/psys.c`` is required. Alternatively, one may
edit manually the planet files (``planet[i].dat``, see also
:ref:`planet_files`).


In a similar manner, all objects are initialized with the same
inclination, defined by the ``INCLINATION`` parameter (its default
value is zero, and it is given in radians). The :math:`x`- axis
(:math:`x>0`) on which the planets are set at the start of simulation
corresponds to the ascending node: the planets are initialized with
:math:`z=0` and :math:`v_z>0`.


Convenience parameters: ``PLANETMASS``, ``SEMIMAJORAXIS`` and ``ORBITALRADIUS``
-------------------------------------------------------------------------------------------------------------------
In order not to have to edit the planetary configuration file (which
can be useful to spawn easily a parameter space exploration), we have
defined three convenience parameters: ``PLANETMASS``, ``SEMIMAJORAXIS`` and
``ORBITALRADIUS``. Their default value is 0. When the first two
(``PLANETMASS`` and ``SEMIMAJORAXIS``) differ from
zero, they are used to supersede the values given in the planetary
configuration file for the first planet only. When the last one
(``ORBITALRADIUS``) is set to a value different from zero, this value
is used to rescale the semi-major axis of all planets prior to the run
start. This parameter is, therefore, a dimensionless factor that can be
used to expand or shrink the whole planetary system. This is mainly
useful in parameter space explorations.

Correcting the shift of resonances
--------------------------------------------------
The gas in FARGO3D is not self-gravitating: it orbits in the potential
of the star exclusively. On the other hand, a planet which feels the
gas gravity orbits in a slightly different potential, which is the sum
of the stellar and disk potential. The Lindblad and corotation
resonances of an embedded planet are shifted (with respect to a more
consistent situation in which the gas would be self-gravitating) as a
consequence of this mismatch. This has sizable effects on the measured
migration velocity of a planet moving freely in the disk, as shown by
Baruteau and Masset (2008). A workaround to this problem consists in
removing the azimuthally averaged density to the density of each zone
prior to the force evaluation: if the disk were unperturbed, the
planet would exclusively feel the star's gravity. In order to activate
this workaround in the code, one has
to add the following line to the`.opt` file and rebuild::

  FARGO_OPT += -DBM08
