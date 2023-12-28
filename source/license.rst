Citing FARGO3D
==============

* A proper way of referencing the FARGO3D code in a publication is by citing the following reference paper:

  * **Benítez-Llambay & Masset, 2016, FARGO3D: A New GPU-Oriented MHD Code, ApJS, 223, 11.**

    The bibtex entry for the main code paper is::

      @article{0067-0049-223-1-11,
      author={Pablo Benítez-Llambay and Frédéric S. Masset},
      title={FARGO3D: A New GPU-oriented MHD Code},
      journal={The Astrophysical Journal Supplement Series},
      volume={223},
      number={1},
      pages={11},
      url={http://stacks.iop.org/0067-0049/223/i=1/a=11},
      year={2016}
      }

    Here is  a `link <http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode=2016ApJS..223...11B&data_type=BIBTEX&db_key=AST&nocookieset=1>`_ to the ADS version of the bibtex record with non-accented characters.


    
* If the hydrodynamics version of the code is used, and the orbital advection algorithm is used (e.g. with setups fargo, p3diso, among others) then the publication should mention that the code uses the orbital advection algorithm of:
  
  * **Masset, 2000, FARGO: A fast eulerian transport algorithm for differentially rotating disks, A&AS, 141, 165.**

    The bibtex entry for this paper is::

      @ARTICLE{2000A&AS..141..165M,
      author = {{Masset}, F.},
      title = "{FARGO: A fast eulerian transport algorithm for differentially rotating
      disks}",
      journal = {Astronomy and Astrophysics Supplement Series},
      year = 2000,
      month = Jan,
      volume = {141},
      pages = {165-173},
      doi = {10.1051/aas:2000116},
      adsurl = {https://ui.adsabs.harvard.edu/\#abs/2000A&AS..141..165M},
      }


* If the magnetohydrodynamics version of the code is used, and the orbital advection algorithm is used (e.g. with the setup mri), then the publication should mention that the code also uses, for the advection of the magnetic field, the orbital advection algorithm of:
  
  * **Stone & Gardiner, 2010, Implementation Of The Shearing Box Approximation In Athena, ApJS, 189, 142.**
    
    The bibtex entry for this paper is::

      @ARTICLE{2010ApJS..189..142S,
      author = {{Stone}, James M. and {Gardiner}, Thomas A.},
      title = "{Implementation of the Shearing Box Approximation in Athena}",
      journal = {The Astrophysical Journal Supplement Series},
      year = 2010,
      month = Jul,
      volume = {189},
      pages = {142-155},
      doi = {10.1088/0067-0049/189/1/142},
      primaryClass = {astro-ph.IM},
      adsurl = {https://ui.adsabs.harvard.edu/\#abs/2010ApJS..189..142S},
      }


* If :ref:`ref_nonuniform` meshes (``SPACING N``) and RAM algorithm (``-DRAM``) are used, the publication should mention the reference paper:

  * **Benítez-Llambay, Krapp, Ramos, Kratter, 2023, RAM: Rapid Advection Algorithm on Arbitrary Meshes**

    The bibtex entry for this paper is::
      
      @ARTICLE{2023ApJ...952..106B,
      author = {{Ben{\'\i}tez-Llambay}, Pablo and {Krapp}, Leonardo and {Ramos}, Ximena S. and {Kratter}, Kaitlin M.},
      title = "{RAM: Rapid Advection Algorithm on Arbitrary Meshes}",
      journal = {\apj},
      keywords = {Algorithms, Hydrodynamics, Accretion, Protoplanetary disks, 1883, 1963, 14, 1300, Astrophysics - Instrumentation and Methods for Astrophysics, Astrophysics - Earth and Planetary Astrophysics, Astrophysics - Astrophysics of Galaxies, Astrophysics - Solar and Stellar Astrophysics, Physics - Computational Physics},
      year = 2023,
      month = aug,
      volume = {952},
      number = {2},
      eid = {106},
      pages = {106},
      doi = {10.3847/1538-4357/acd698},
      archivePrefix = {arXiv},
      eprint = {2305.05362},
      primaryClass = {astro-ph.IM},
      adsurl = {https://ui.adsabs.harvard.edu/abs/2023ApJ...952..106B},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
      }  


* If the :ref:`ref_multifluid` version of the code is used (i.e., ``NFLUIDS>1``), the publication should mention the reference paper:
  
  * **Benítez-Llambay, Krapp, Pessah, 2019, Asymptotically stable numerical Method for multispecies momentum transfer: Gas and Multifluid-dust test suite and implementation in FARGO3D, ApJS, 241, 2**

    
    The bibtex entry for this paper is::

      @ARTICLE{2019ApJS..241...25B,
      author = {{Ben{\'\i}tez-Llambay}, Pablo and {Krapp}, Leonardo and
      {Pessah}, Martin E.},
      title = "{Asymptotically Stable Numerical Method for Multispecies Momentum Transfer:
      Gas and Multifluid Dust Test Suite and Implementation in FARGO3D}",
      journal = {\apjs},
      keywords = {circumstellar matter, hydrodynamics, methods: numerical, planets and
      satellites: formation, protoplanetary disks, Astrophysics -
      Earth and Planetary Astrophysics},
      year = "2019",
      month = "Apr",
      volume = {241},
      number = {2},
      eid = {25},
      pages = {25},
      doi = {10.3847/1538-4365/ab0a0e},
      archivePrefix = {arXiv},
      eprint = {1811.07925},
      primaryClass = {astro-ph.EP},
      adsurl = {https://ui.adsabs.harvard.edu/abs/2019ApJS..241...25B},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
      }


      
* If the :ref:`refdiffusion` is used, the publication should cite:

  * **Weber et al. 2019, Predicting the observational signature of migrating Neptune-sized planets in low-viscosity disks, Apj, 884, 178**

  The bibtex entry for this paper is::

    @ARTICLE{2019ApJ...884..178W,
       author = {{Weber}, Philipp and {P{\'e}rez}, Sebasti{\'a}n and
         {Ben{\'\i}tez-Llambay}, Pablo and {Gressel}, Oliver and
         {Casassus}, Simon and {Krapp}, Leonardo},
        title = "{Predicting the Observational Signature of Migrating Neptune-sized Planets in Low-viscosity Disks}",
      journal = {\apj},
         year = 2019,
        month = oct,
       volume = {884},
       number = {2},
          eid = {178},
        pages = {178},
          doi = {10.3847/1538-4357/ab412f},
	archivePrefix = {arXiv},
	eprint = {1909.01661},
	primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2019ApJ...884..178W},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
      }




* If the the Hall effect and/or ambipolar diffusion are included  in the :ref:`induction_equation`, the publication should cite:

  * **Krapp et al. 2018,  Dust Segregation in Hall-dominated Turbulent Protoplanetary Disks, ApJ, 806, 105**

  The bibtex entry for this paper is::

    @ARTICLE{2018ApJ...865..105K,
       author = {{Krapp}, Leonardo and {Gressel}, Oliver and
         {Ben{\'\i}tez-Llambay}, Pablo and {Downes}, Turlough P. and {Mohand
        as}, Gopakumar and {Pessah}, Martin E.},
        title = "{Dust Segregation in Hall-dominated Turbulent Protoplanetary Disks}",
      journal = {\apj},
         year = 2018,
        month = oct,
       volume = {865},
       number = {2},
          eid = {105},
        pages = {105},
          doi = {10.3847/1538-4357/aadcf0},
	  archivePrefix = {arXiv},
       eprint = {1808.07660},
       primaryClass = {astro-ph.EP},
    }


    

License
=======

FARGO3D is released under the terms of the GNU GENERAL PUBLIC LICENSE

Version 3, 29 June 2007

Copyright © 2007 Free Software Foundation, Inc. <http://www.fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

`Full text <https://github.com/FARGO3D/fargo3d?tab=GPL-3.0-1-ov-file#readme>`_ of the GPL

