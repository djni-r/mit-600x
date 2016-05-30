# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    for x in (300, 150, 75, 0):
        virusPop = []
        #resVirusPop = [0,] * (x + 150)
        for i in range(numTrials):
            viruses = []
            for i in range(100):
                viruses.append(ResistantVirus(0.1, 0.05, {"guttagonol":False}, 0.005))
            tPatient = TreatedPatient(viruses, 1000)
            
            for i in range(x):
                tPatient.update()
            
            tPatient.addPrescription("guttagonol")
            
            for i in range(x, x + 150):
                tPatient.update()
             
            virusPop.append(tPatient.getTotalPop());   
        #for i in range(len(virusPop)):
        #    virusPop[i] = float(virusPop[i])/numTrials
        #
        #for i in range(len(resVirusPop)):
        #    resVirusPop[i] = float(resVirusPop[i])/numTrials
        
        pylab.hist(virusPop, numTrials)
        #pylab.subplot(1, 1, 1)
        #pylab.plot(range(x), resVirusPop)
        pylab.title("Final Virus Population With Delay Of " + str(x) + " Time-steps")
        pylab.xlabel("Virus Population")
        pylab.ylabel("Patients")
        #pylab.legend(["Total", "Resistant"])
        pylab.show()
        #break

#simulationDelayedTreatment(100)



#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    for x in (300, 150, 75, 0):
        virusPop = []
        for i in range(numTrials):
            viruses = []
            for i in range(100):
                viruses.append(ResistantVirus(0.1, 0.05, {"guttagonol":False, "grimpex":False}, 0.01))
            tPatient = TreatedPatient(viruses, 1000)
            
            for i in range(150):
                tPatient.update()
            
            tPatient.addPrescription("guttagonol")
            
            for i in range(x):
                tPatient.update()
            
            tPatient.addPrescription("grimpex")
            
            for i in range(150):
                tPatient.update()
             
            virusPop.append(tPatient.getTotalPop());
        
        pylab.hist(virusPop, numTrials)
        pylab.title("Final Virus Population With Delay Of " + str(x) + " Time-steps")
        pylab.xlabel("Virus Population")
        pylab.ylabel("Patients")
        pylab.show()
        break

simulationTwoDrugsDelayedTreatment(100)