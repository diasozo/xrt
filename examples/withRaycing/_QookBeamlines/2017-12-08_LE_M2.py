# -*- coding: utf-8 -*-
"""

__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "2017-12-08"

Created with xrtQook




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

Gold = rmats.Material(
    elements=r"Au",
    kind=r"mirror",
    rho=19.3,
    table=r"Henke",
    name=r"M_Au")


def build_beamline():
    LowEnergyM1 = raycing.BeamLine(
        alignE=123,
        alignMode=True)

    LowEnergyM1.LowEnergyIdeal = rsources.Undulator(
        bl=LowEnergyM1,
        name=r"LowEnergyIdeal",
        center=[0, -1800, 0],
        nrays=2e5,
        eE=2.9,
        eI=0.22,
        eEspread=0.0011,
        eEpsilonX=22.7,
        eEpsilonZ=0.1017,
        betaX=9.664,
        betaZ=4.331,
        xPrimeMax=0.516,
        zPrimeMax=0.175,
        targetE=[123.0,1,False],
        eMin=121,
        eMax=125,
        K=r"auto",
        period=180,
        n=20,
        targetOpenCL=[0, 2],
        precisionOpenCL=r"float32")

    LowEnergyM1.rectangularAperture01 = rapts.RectangularAperture(
        bl=LowEnergyM1,
        name=r"WallCollimator",
        center=[0, 11500, 0],
        opening=[-11.115,11.115,-11.115,11.115])

    LowEnergyM1.roundAperture01 = rapts.RoundAperture(
        bl=LowEnergyM1,
        name=r"FixedMask",
        center=[0, 15008, 0],
        r=7.5)

    LowEnergyM1.screen02 = rscreens.Screen(
        bl=LowEnergyM1,
        name=r"FixedMaskScreen",
        center=[0, 15008, 0])

    LowEnergyM1.rectangularAperture02 = rapts.RectangularAperture(
        bl=LowEnergyM1,
        name=r"HorizontalVariableMask",
        center=[0, 15558, 0],
        opening=[-2.5,2.5,-5,5])

    LowEnergyM1.rectangularAperture03 = rapts.RectangularAperture(
        bl=LowEnergyM1,
        name=r"VerticalVariableMask",
        center=[0, 15748, 0],
        opening=[-5,5,-2.5,2.5])

    LowEnergyM1.roundAperture02 = rapts.RoundAperture(
        bl=LowEnergyM1,
        name=r"Collimator",
        center=[0, 17195, 0],
        r=7.5)

    LowEnergyM1.bentFlatMirror01 = roes.BentFlatMirror(
        bl=LowEnergyM1,
        name=r"M1",
        center=[0, 18000, 0],
        pitch=r"1.3 deg",
        roll=r"270 deg",
        material=Gold,
        limPhysX=[-13, 13],
        limOptX=[-13, 13],
        limPhysY=[-215, 215],
        limOptY=[-215, 215],
        R=1.548e6,
        precisionOpenCL=r"float32")

    LowEnergyM1.screen03 = rscreens.Screen(
        bl=LowEnergyM1,
        name=r"PreM2Screen",
        center=[-140, 21000, 0])

    LowEnergyM1.rectangularAperture04 = rapts.RectangularAperture(
        bl=LowEnergyM1,
        name=r"Photon Slits 1",
        center=[45.363, 18998.97, 0],
        opening=[-5,5,-5,5])

    LowEnergyM1.oe01 = roes.OE(
        bl=LowEnergyM1,
        name=r"M2",
        center=[125.156, 20756.16, 0],
        material=Gold,
        limPhysX=[-50, 50],
        limOptX=[-40, 40],
        limPhysY=[-205, 205],
        limOptY=[-195, 195])

    return LowEnergyM1


def run_process(LowEnergyM1):
    LowEnergyIdealbeamGlobal01 = LowEnergyM1.LowEnergyIdeal.shine()

    rectangularAperture01beamLocal01 = LowEnergyM1.rectangularAperture01.propagate(
        beam=LowEnergyIdealbeamGlobal01)

    roundAperture01beamLocal01 = LowEnergyM1.roundAperture01.propagate(
        beam=LowEnergyIdealbeamGlobal01)

    screen02beamLocal01 = LowEnergyM1.screen02.expose(
        beam=LowEnergyIdealbeamGlobal01)

    rectangularAperture02beamLocal01 = LowEnergyM1.rectangularAperture02.propagate(
        beam=LowEnergyIdealbeamGlobal01)

    rectangularAperture03beamLocal01 = LowEnergyM1.rectangularAperture03.propagate(
        beam=LowEnergyIdealbeamGlobal01)

    roundAperture02beamLocal01 = LowEnergyM1.roundAperture02.propagate(
        beam=LowEnergyIdealbeamGlobal01)

    bentFlatMirror01beamGlobal02, bentFlatMirror01beamLocal02 = LowEnergyM1.bentFlatMirror01.reflect(
        beam=LowEnergyIdealbeamGlobal01,
        returnLocalAbsorbed=0)

    screen03beamLocal01 = LowEnergyM1.screen03.expose(
        beam=bentFlatMirror01beamGlobal02)

    rectangularAperture04beamLocal01 = LowEnergyM1.rectangularAperture04.propagate(
        beam=bentFlatMirror01beamGlobal02)

    oe01beamGlobal01, oe01beamLocal01 = LowEnergyM1.oe01.reflect(
        beam=bentFlatMirror01beamGlobal02)

    outDict = {
        'LowEnergyIdealbeamGlobal01': LowEnergyIdealbeamGlobal01,
        'rectangularAperture01beamLocal01': rectangularAperture01beamLocal01,
        'roundAperture01beamLocal01': roundAperture01beamLocal01,
        'screen02beamLocal01': screen02beamLocal01,
        'rectangularAperture02beamLocal01': rectangularAperture02beamLocal01,
        'rectangularAperture03beamLocal01': rectangularAperture03beamLocal01,
        'roundAperture02beamLocal01': roundAperture02beamLocal01,
        'bentFlatMirror01beamGlobal02': bentFlatMirror01beamGlobal02,
        'bentFlatMirror01beamLocal02': bentFlatMirror01beamLocal02,
        'screen03beamLocal01': screen03beamLocal01,
        'rectangularAperture04beamLocal01': rectangularAperture04beamLocal01,
        'oe01beamGlobal01': oe01beamGlobal01,
        'oe01beamLocal01': oe01beamLocal01}
    return outDict


rrun.run_process = run_process



def define_plots():
    plots = []

    plot01 = xrtplot.XYCPlot(
        beam=r"LowEnergyIdealbeamGlobal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"plot01 - LE EPU Source",
        fluxFormatStr=r"%g")
    plots.append(plot01)

    plot02 = xrtplot.XYCPlot(
        beam=r"bentFlatMirror01beamLocal02",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        title=r"plot02 - M1",
        fluxFormatStr=r"%g")
    plots.append(plot02)

    plot03 = xrtplot.XYCPlot(
        beam=r"bentFlatMirror01beamLocal02",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"plot03 - M1 Absorbed Power",
        fluxKind=r"power",
        fluxFormatStr=r"%g")
    plots.append(plot03)

    plot04 = xrtplot.XYCPlot(
        beam=r"oe01beamGlobal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"plot04 - M2")
    plots.append(plot04)
    return plots


def main():
    LowEnergyM1 = build_beamline()
    E0 = 0.5 * (LowEnergyM1.LowEnergyIdeal.eMin +
                LowEnergyM1.LowEnergyIdeal.eMax)
    LowEnergyM1.alignE=E0
    plots = define_plots()
    xrtrun.run_ray_tracing(
        plots=plots,
        repeats=2,
        backend=r"raycing",
        beamLine=LowEnergyM1)


if __name__ == '__main__':
    main()
