"""
Created on Fri May 29 17:19:38 2020

@author: Ana de Sousa (anacsousa@lara.unb.br)
"""

# IMPORT OPENSIM LIBRARIES
import opensim as osim

# IMPORT OTHER LIBRARIES
import pathlib  # get current path
import os.path  # create path
import numpy    # math
import myFunctions as osim2 # wrap functions

# DEFINE KEY MODEL VARIABLES 
# ********** Paths and files ********** 
currentPath = pathlib.Path().absolute()
modelName = os.path.join(currentPath, "cycling_model.osim")
markerSetFile = "cycling_model_MarkerSet.xml"
modelMarkersFile = "cycling_model_markers.osim"
# newModel = os.path.join(currentPath, "cycling_model.osim")

# ********** Open model, set new name ********** 
myModel = osim.Model(modelName) 
myModel.setName("cycling_model_markers")     

# ********** Get references ********** 
ground = myModel.getGround()
calcn_r = osim2.find_body(myModel,"calcn_r")
calcn_l = osim2.find_body(myModel,"calcn_l")
pedal_r = osim2.find_body(myModel,"pedal_r")
pedal_l = osim2.find_body(myModel,"pedal_l")

## BUILDING A MARKERSET OBJECT FROM FILE AND ATTACHING IT TO A MODEL
# Create the markers set file and attach to model       
newMarkers = osim.MarkerSet()
myModel.updateMarkerSet(newMarkers)

# Create markers
calcn_r_marker = osim.Marker("ANKLE_r",calcn_r, osim.Vec3(0.06,0.05,0.035))
myModel.addMarker(calcn_r_marker)

calcn_l_marker = osim.Marker("ANKLE_l",calcn_l, osim.Vec3(0.06,0.05,-0.035))
myModel.addMarker(calcn_l_marker)

pedal_r_marker = osim.Marker("PEDAL_r",pedal_r, osim.Vec3(0,0,0.05))
myModel.addMarker(pedal_r_marker)

pedal_l_marker = osim.Marker("PEDAL_l",pedal_l, osim.Vec3(0,0,-0.05))
myModel.addMarker(pedal_l_marker)

## SETTING FILES
# TODO ScaleMarkerSet.xml
    # Marker set for the Scale tool. It contains the set of virtual markers that are placed on the body
    # segments of the model.


# TODO subject01_setup_scale.xml, it may include:
    # ScaleTasks: IK tasks for the scale tool, moves the virtual markers on the model so that their
    # position match the experimental maker locations.
    # ScaleMeasurementSet: measurements set for the scale tool. It contains pairs of experimental
    # markers, the distance between which are used to scale the generic musculoskeletal model
    # ScaleScaleSet: scale set for the scale tool. It contains a set of manual scale factors to be
    # applied to the generic musculoskeletal model.
    # FOR NOW, THIS IS AN "EMPTY" FILE


# TODO file.trc

## OUTPUT
myModel.finalizeConnections()
newMarkers.printToXML(markerSetFile)
myModel.printToXML(modelMarkersFile)
# TODO subject01_simbody.osim

