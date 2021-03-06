# -*- coding: utf-8 -*-
"""

__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "2017-12-08"

Created with xrtQook


BioXAS-Main
____________

This example is based on the layout of the BioXAS-Main beamline (Canadian Light Source) and incorporates most commonly used optical components: the wiggler source, flat and curved X-ray mirrors with different coatings, filters, slits and screens.

.. imagezoom:: _images/ex03_glow.png
   :scale: 60%

Features.
________

1) Thin mirrors on bulk substrate, see the RhOnSi and CVDonSi materials.

.. imagezoom:: _images/ex03_p01.png
   :scale: 60%

2) Automatic alignment procedures, see the beamline alignE, alignMode, SSRL_DCM bragg properties and the centers of the optical elements. Note that the value of SSRL_DCM.bragg overrides that beamLine.alignE value.

.. imagezoom:: _images/ex03_p02.png
   :scale: 60%

3) Absorbed power distributons. See how the parameters of the Mirror1.reflect() function.

.. imagezoom:: _images/ex03_p03a.png
   :scale: 60%

Check the plot properties

.. imagezoom:: _images/ex03_p03b.png
   :scale: 60%

Increase the energy range...

.. imagezoom:: _images/ex03_p03c.png
   :scale: 60%

...to see the effect on the absorbed power spectrum.

.. imagezoom:: _images/ex03_p03d.png
   :scale: 60%



"""

import numpy as np
import sys
sys.path.append(r"/Users/tor/Library/Mobile Documents/com~apple~CloudDocs/Optics/xrtTMP/xrt")
import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.materials as rmats
import xrt.backends.raycing.oes as roes
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.plotter as xrtplot
import xrt.runner as xrtrun

CVD = rmats.Material(
    elements=r"C",
    kind=r"plate",
    rho=3.52,
    name=r"Diamond plate")

Rh = rmats.Material(
    elements=r"Rh",
    kind=r"mirror",
    rho=12.41,
    name=r"Rhodium bulk")

Si220 = rmats.CrystalSi(
    hkl=[2, 2, 0],
    name=r"Si220")

CVDcoating = rmats.Material(
    elements=r"C",
    kind=r"mirror",
    rho=3.52,
    name=r"CVD coating")

Si = rmats.Material(
    elements=r"Si",
    kind=r"mirror",
    rho=2.33,
    name=r"Si bulk")

RhOnSi = rmats.Coated(
    coating=Rh,
    cThickness=30,
    surfaceRoughness=2,
    substrate=Si,
    substRoughness=2,
    name=r"Rhodium on Silicon")

CVDonSi = rmats.Coated(
    coating=CVDcoating,
    cThickness=20,
    surfaceRoughness=2,
    substrate=Si,
    substRoughness=2,
    name=r"CVD on Silicon")

Si220harm = rmats.CrystalHarmonics(
    Nmax=2,
    name=r"Si220 with harmonics",
    hkl=[2, 2, 0],
    a=5.41949,
    tK=297.15)


def build_beamline():
    BioXAS_Main = raycing.BeamLine(
        alignE=8000,
        alignMode=True)

    BioXAS_Main.Wiggler = rsources.Wiggler(
        bl=BioXAS_Main,
        name=r"Flat-Top Wiggler",
        center=[0, 0, 0],
        nrays=200000,
        eE=2.9,
        eI=0.25,
        eEpsilonX=18.1,
        eEpsilonZ=0.0362,
        betaX=9.1,
        betaZ=2.8,
        xPrimeMax=1.,
        zPrimeMax=0.375,
        eMin=7998,
        eMax=8002,
        K=35,
        period=150,
        n=11)

    BioXAS_Main.FEMask = rapts.RectangularAperture(
        bl=BioXAS_Main,
        name=r"Frontend Mask",
        center=[0, 12000, 0],
        opening=[-12, 12, -1.75, 1.75])

    BioXAS_Main.DiamondFilter = roes.Plate(
        bl=BioXAS_Main,
        name=r"Diamond Filter",
        center=[0, 13600, 0],
        pitch=np.pi/2,
        material=CVD,
        limPhysX=[-5, 5],
        limOptX=[-5, 5],
        limPhysY=[-5, 5],
        limOptY=[-5, 5],
        t=0.05)

    BioXAS_Main.WhiteBeamSlits = rapts.RectangularAperture(
        bl=BioXAS_Main,
        name=r"White Beam Slits",
        center=[0, 14000, 0],
        opening=[-10, 10, -1, 1])

    BioXAS_Main.Mirror1 = roes.ToroidMirror(
        bl=BioXAS_Main,
        name=r"M1",
        center=[0, 14600, 0],
        pitch=r"0.15 deg",
        material=RhOnSi,
        limPhysX=[-12, 12],
        limOptX=[-12, 12],
        limPhysY=[-495, 495],
        limOptY=[-495, 495],
        R=7.12e6,
        r=69.81)

    BioXAS_Main.CM_Slits = rapts.RectangularAperture(
        bl=BioXAS_Main,
        name=r"CM Slits",
        center=[0, 15600, r"auto"],
        opening=[-5, 5, -2, 2])

    BioXAS_Main.SSRL_DCM = roes.DCM(
        bl=BioXAS_Main,
        name=r"SSRL channel cut DCM",
        center=[0, 25300, r"auto"],
        bragg=[8000],
        material=Si220,
        limPhysX=[-20, 20],
        limOptX=[-20, 20],
        limPhysY=[-72.3913, 3.8087],
        limOptY=[-72.3913, 3.8087],
        limPhysX2=[-20, 20],
        limPhysY2=[-1.1951, 94.0549],
        limOptX2=[-20, 20],
        limOptY2=[-1.1951, 94.0549],
        cryst2perpTransl=6.5023)

    BioXAS_Main.PreM2Screen = rscreens.Screen(
        bl=BioXAS_Main,
        name=r"M2 Paddle",
        center=[0, 26000, r"auto"])

    BioXAS_Main.Mirror2 = roes.ToroidMirror(
        bl=BioXAS_Main,
        name=r"M2",
        center=[0, 26900, r"auto"],
        pitch=r"-0.15 degree",
        positionRoll=np.pi,
        material=RhOnSi,
        limOptX=[-12, 12],
        limOptY=[-550, 550],
        R=2.5e6,
        r=35.9)

    BioXAS_Main.PhotonShutter = rapts.RectangularAperture(
        bl=BioXAS_Main,
        name=r"PS1",
        center=[0, 28300, r"auto"],
        opening=[-5, 5, -2, 2])

    BioXAS_Main.DBHR1 = roes.OE(
        bl=BioXAS_Main,
        name=r"DBHR1",
        center=[0, 29900, r"auto"],
        pitch=r"0.2 deg",
        material=CVDcoating,
        limPhysX=[-10, 10],
        limOptX=[-10, 10],
        limPhysY=[-75, 75],
        limOptY=[-75, 75])

    BioXAS_Main.DBHR2 = roes.OE(
        bl=BioXAS_Main,
        name=r"DBHR2",
        center=[0, 30075, r"auto"],
        pitch=r"-0.2 deg",
        positionRoll=np.pi,
        material=CVDcoating,
        limPhysX=[-10, 10],
        limOptX=[-10, 10],
        limPhysY=[-75, 75],
        limOptY=[-75, 75])

    BioXAS_Main.JJslits = rapts.RectangularAperture(
        bl=BioXAS_Main,
        name=r"JJ slits",
        center=[0, 30350, r"auto"],
        opening=[-5, 5, -0.2, 0.2])

    BioXAS_Main.SampleScreen = rscreens.Screen(
        bl=BioXAS_Main,
        name=r"Sample",
        center=[0, 30650, r"auto"])

    return BioXAS_Main


def run_process(BioXAS_Main):
    WigglerbeamGlobal01 = BioXAS_Main.Wiggler.shine()

    FEMaskbeamLocal01 = BioXAS_Main.FEMask.propagate(
        beam=WigglerbeamGlobal01)

    C_FilterbeamGlobal01, C_FilterbeamLocal101, CVDFilterAbsorbedPower = BioXAS_Main.DiamondFilter.double_refract(
        beam=WigglerbeamGlobal01,
        returnLocalAbsorbed=0)

    WhiteBeamSlitsbeamLocal01 = BioXAS_Main.WhiteBeamSlits.propagate(
        beam=C_FilterbeamGlobal01)

    M1beamGlobal01, M1AbsorbedPower = BioXAS_Main.Mirror1.reflect(
        beam=C_FilterbeamGlobal01,
        returnLocalAbsorbed=0)

    CM_SlitsbeamLocal01 = BioXAS_Main.CM_Slits.propagate(
        beam=M1beamGlobal01)

    SSRL_DCMbeamGlobal01, SSRL_DCMbeamLocal101, SSRL_DCMbeamLocal201 = BioXAS_Main.SSRL_DCM.double_reflect(
        beam=M1beamGlobal01)

    preM2ScreenFoorprint = BioXAS_Main.PreM2Screen.expose(
        beam=SSRL_DCMbeamGlobal01)

    M2beamGlobal01, M2beamLocal01 = BioXAS_Main.Mirror2.reflect(
        beam=SSRL_DCMbeamGlobal01)

    PhotonShutterbeamLocal01 = BioXAS_Main.PhotonShutter.propagate(
        beam=M2beamGlobal01)

    DBHR1beamGlobal01, DBHR1beamLocal01 = BioXAS_Main.DBHR1.reflect(
        beam=M2beamGlobal01)

    DBHR2beamGlobal01, DBHR2beamLocal01 = BioXAS_Main.DBHR2.reflect(
        beam=DBHR1beamGlobal01)

    JJslitsbeamLocal01 = BioXAS_Main.JJslits.propagate(
        beam=DBHR2beamGlobal01)

    SampleScreenFootprint = BioXAS_Main.SampleScreen.expose(
        beam=DBHR2beamGlobal01)

    outDict = {
        'WigglerbeamGlobal01': WigglerbeamGlobal01,
        'FEMaskbeamLocal01': FEMaskbeamLocal01,
        'C_FilterbeamGlobal01': C_FilterbeamGlobal01,
        'C_FilterbeamLocal101': C_FilterbeamLocal101,
        'CVDFilterAbsorbedPower': CVDFilterAbsorbedPower,
        'WhiteBeamSlitsbeamLocal01': WhiteBeamSlitsbeamLocal01,
        'M1beamGlobal01': M1beamGlobal01,
        'M1AbsorbedPower': M1AbsorbedPower,
        'CM_SlitsbeamLocal01': CM_SlitsbeamLocal01,
        'SSRL_DCMbeamGlobal01': SSRL_DCMbeamGlobal01,
        'SSRL_DCMbeamLocal101': SSRL_DCMbeamLocal101,
        'SSRL_DCMbeamLocal201': SSRL_DCMbeamLocal201,
        'preM2ScreenFoorprint': preM2ScreenFoorprint,
        'M2beamGlobal01': M2beamGlobal01,
        'M2beamLocal01': M2beamLocal01,
        'PhotonShutterbeamLocal01': PhotonShutterbeamLocal01,
        'DBHR1beamGlobal01': DBHR1beamGlobal01,
        'DBHR1beamLocal01': DBHR1beamLocal01,
        'DBHR2beamGlobal01': DBHR2beamGlobal01,
        'DBHR2beamLocal01': DBHR2beamLocal01,
        'JJslitsbeamLocal01': JJslitsbeamLocal01,
        'SampleScreenFootprint': SampleScreenFootprint}
    return outDict


rrun.run_process = run_process



def define_plots():
    plots = []

    plot01 = xrtplot.XYCPlot(
        beam=r"WigglerbeamGlobal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"01 - Wiggler Source",
        fluxFormatStr=r"%g")
    plots.append(plot01)

    plot02 = xrtplot.XYCPlot(
        beam=r"CVDFilterAbsorbedPower",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"y"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        title=r"02 - CVD Filter Absorbed Power",
        fluxKind=r"power",
        fluxFormatStr=r"%g")
    plots.append(plot02)

    plot03 = xrtplot.XYCPlot(
        beam=r"M1AbsorbedPower",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"y"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"03 - Mirror1 Absorbed Power",
        fluxKind=r"power",
        fluxFormatStr=r"%g")
    plots.append(plot03)

    plot04 = xrtplot.XYCPlot(
        beam=r"preM2ScreenFoorprint",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        title=r"04 - preM2 Screen Footprint",
        fluxFormatStr=r"%g")
    plots.append(plot04)

    plot05 = xrtplot.XYCPlot(
        beam=r"SampleScreenFootprint",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV",
            limits=[7998, 8002]),
        title=r"05 - Sample",
        fluxFormatStr=r"%g")
    plots.append(plot05)
    return plots


def main():
    BioXAS_Main = build_beamline()
    E0 = 0.5 * (BioXAS_Main.Wiggler.eMin +
                BioXAS_Main.Wiggler.eMax)
    BioXAS_Main.alignE=E0
    plots = define_plots()
    xrtrun.run_ray_tracing(
        plots=plots,
        repeats=10,
        backend=r"raycing",
        beamLine=BioXAS_Main)


if __name__ == '__main__':
    main()
