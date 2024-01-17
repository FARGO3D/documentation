VTK Compatibility
=================

The Visualization Toolkit (VTK) is an open-source, freely available
software system for 3D computer graphics, image processing, and
visualization. This format is very powerful because there are a lot of
routines developed for it. The format used in FARGO3D is the Legacy
VTK format. We have tested the outputs with Visit.

The output rules in the section "Outputs" do not apply for vtk. The
main structure of a FARGO3D VTK file is:

* A header
* Coordinates
* Data

The VTK file is a mix between an ASCII file and a binary file. The
header is written in ASCII format, while the domains and fields are
written in binary format. This format is compatible with the -m
(merge) and with the -S/-s (restart) execution flags.

The fastest index is not i (x), but now is always j (y). On the other
hand, the structure of a loop for reading a vtk file is
coordinate-dependent. In Cartesian & Cylindrical coordinates, the
order is::

   loop over k
     loop over i
       loop over j

while in Spherical coordinates, the order is::

   loop over i
     loop over k
       loop over j

This format is useful when you are working with Visit and coordinate transformations. 

If you have a run in .dat format and you want to convert its output to
vtk for displaying it with Visit, FARGO3D has two execution flags
devoted to this: -V (Dat2VTK) & -B (VTK2Dat). The flag -V is used when
you have an output file in dat and you want to convert it into
VTK. The opposite holds for the flag -B.


Visit has also a powerful python-script for converting your data into
vtk, but it is not included with FARGO3D.
