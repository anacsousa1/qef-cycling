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

# DEFINE KEY MODEL VARIABLES 
# ********** Paths and files ********** 
currentPath = pathlib.Path().absolute()
modelName = os.path.join(currentPath, "cycling_model.osim")
markerSetFile = "cycling_model_MarkerSet.xml"    
# newModel = os.path.join(currentPath, "cycling_model.osim")

## BUILDING A MARKERSET OBJECT FROM FILE AND ATTACHING IT TO A MODEL
# TODO model.osim
myModel = osim.Model(modelName)             
# newMarkers = osim.MarkerSet(myModel, markerSetFile)
# myModel.updateMarkerSet(newMarkers)

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
# TODO subject01_simbody.osim

