      
Introduction
=============

FARGO3D is a hydrodynamics and magnetohydrodynamics parallel code. It is the successor of the public FARGO code (http://fargo.in2p3.fr). It conserves the main features of FARGO, but includes a lot of new concepts. Although FARGO3D was started inspired on FARGO, it was developed from scratch, allowing a much more versatile code.

Here is a summary of the main features of FARGO3D:

* Eulerian mesh code.
* Multidimensional (1D, 2D & 3D).
* Several geometries (Cartesian, cylindrical and spherical).
* Non-inertial reference frames (including shearing box for Cartesian setups).
* Adiabatic or Isothermal Equation of State (EOS). It is easy to implement another EOS.
* Designed mainly for disks, but works well for general problems. 
* Solves the equations of hydrodynamics (continuity, Navier-Stokes, and energy) and magnetohydrodynamics (MHD).
* Includes ideal MHD (Method Of Characteristics & Constrained Transport).
* Includes non-ideal MHD terms (Ohmic and Ambipolar Diffusion and Hall effect).
* Includes the full viscous stress tensor in the three geometries.
* Simple N-body integrator, for embedded planets.
* FARGO algorithm implemented in Cartesian, cylindrical and spherical coordinates.
* The FARGO or "orbital advection" scheme is also implemented for MHD.
* Possible run-time visualization.
* Multi-platform:

  * Sequential Mode, one process on a CPU.
  * Parallel Mode, for clusters of CPU (distributed memory, with MPI).
  * One GPU (CUDA without MPI).
  * Parallel GPU Mode, for clusters of GPUs (mixed MPI-CUDA version).

Another important feature of FARGO3D is to provide a coherent and simple framework to develop new routines. 
We have developed a coding style which allows one to develop exclusively in C, as in the previous FARGO code, so that the user does not have to learn CUDA (a kind of "GPU programming language"). Automatic conversion of the C code to CUDA code is performed at build time by a Python script. Memory transactions between CPU and GPU are dealt with automatically in the most efficient manner so that the user never has to worry about these details.
For this reason, the built process of FARGO3D is supported by a lot of scripting that does all the hard work. There are scripts for developing new GPU functions (kernels), new boundary conditions and for adding new parameters within the code.

Two important warnings:

* FARGO3D is based on a finite difference scheme. It does enforce mass and momentum conservation to machine accuracy but does not enforce the conservation of total energy. 

* FARGO3D always assumes the *x*-direction as periodic. In cylindrical and spherical coordinates, *x* corresponds to the azimuthal angle. We might in the future develop a more general solution.



A foreword about the terminology used in this manual
...........................................................................................

We are aware that most FARGO3D potential users come from a FORTRAN background, and for this reason, we have avoided as much as possible an uncontrolled use of C and CUDA's jargon. We have tried to explicit specific terms every time we used them. We give hereafter a very short list of the main terms that you may encounter in this manual.

* What is called a *routine* in FORTRAN is a *function* in C. We have nonetheless used frequently the (incorrect) term *routine*, even for C functions. A function is always referred to with trailing empty parentheses (for instance, the ``main()`` function.)

* What is called a *function* in C is called a *kernel* in CUDA. This is not to be confused with the operating system's kernel, of course. A kernel is, therefore, a "function" (generally lightweight, owing to memory constraints on board the streaming multiprocessors of a GPU) that spawns a huge amount of threads on the GPU cores.

* In the GPU's jargon, the CPU and its RAM are usually designed as the *host*, whereas the GPU is called the *device*. Uploading data to the GPU is therefore called a "host to device" communication. The *video RAM* of a GPU is called the "global memory" of the device.

Finally, in the MPI parlance, each instance of a job should be called a *processing element*, PE in short. It should be distinguished from the processor, as several PEs can run on one processor or even on one core. Nonetheless, it is customary to distribute the tasks on clusters so that one PE runs on one core. We frequently commit the abuse of language that consists in saying "processor" instead of PE (e.g.: processor of rank 0).



