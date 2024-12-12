.. _induction_equation:

Induction equation
==================

The magnetic field is updated via the induction equation:

.. math::
   \frac{\partial {\bf B}}{\partial t} = \nabla \times \left[{ {\bf v} \times {\bf B}} \, -  \underbrace{ \eta_{\rm O} {\bf J}}_{\text{Ohmic diffusion}} \, - \underbrace{\eta_{\rm H} \left({\bf J} \times {\bf \hat{B}}\right)}_{\text{Hall effect}} +  \underbrace{\eta_{\rm A} \left({\bf J}\times {\bf \hat{B}} \right)\times {\bf \hat{B}} }_{\text{Ambipolar diffusion}}  \right] 
   
where :math:`{\bf J} = \nabla \times {\bf B}/\mu_0` is the current density, and :math:`\hat{\bf B}` is the unit vector in the direction of :math:`{\bf B}`. The labeled terms correspond to the non-ideal MHD terms.

Both the Ohmic and Ambipolar diffusion terms are added to the EMFs before updating the magnetic field (see `Benitez-Llambay & Masset (2016) <https://ui.adsabs.harvard.edu/abs/2016ApJS..223...11B/abstract>`_ for details). The Hall term is treated with the method described in appendix A `Krapp et al. (2018) <https://ui.adsabs.harvard.edu/abs/2018ApJ...865..105K/abstract>`_ (see also `Bai (2014) <https://ui.adsabs.harvard.edu/abs/2014ApJ...791..137B/abstract>`_).

.. warning:: To activate the non-ideal MHD terms, ``-DOHMICDIFFUSION``, ``-DAMBIPOLARDIFFUSION`` or  ``-DHALLEFFECT`` must be defined in the ``.opt`` file.

	     
Diffusivities
-------------

The user is responsible for defining the diffusivities :math:`\eta_{\rm O}, \eta_{\rm H}, \eta_{\rm A}`. These are defined as the Fields ``EtaOhm``, ``EtaHall``, ``EtaAD``, and filled in the source files:

 - ``src/nimhd_ohmic_diffusion_coeff.c``
 - ``src/nimhd_hall_effect_coeff.c``
 - ``src/nimhd_ambipolar_diffusion_coeff.c``

The resistivities are then filled every time step in ``src/main.c``, before calling the CFL condition. In the standard implementation, the diffusitivies are filled with a "constant" value given by the parameters:

 - ``OhmicDiffusionCoeff`` (global variable ``OHMICDIFFUSIONCOEFF``)
 - ``HallEffectCoeff`` (global variable ``HALLEFFECTCOEFF``)
 - ``AmbipolarDiffusionCoeff`` (global variable ``AMBIPOLARDIFFUSIONCOEFF``)

The value of these parameters should be defined in the ``.par`` file.

.. note:: If the diffusivities do not evolve with time, the user can add a `return` call after the first initialization (see e.g., ``setups/mri/nimhd_ohmic_diffusion_coeff.c``).
