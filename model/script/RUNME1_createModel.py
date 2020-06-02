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
# ********** Body ********** 
pelvis_base_tx = 0.085
pelvis_base_ty = 0
lumbar_base = - numpy.deg2rad(50)

# ********** Bike geometry ********** 
A = 800/1000
F = numpy.deg2rad(73.76)
pelvis_tx_crank = -A*numpy.cos(F)
pelvis_ty_crank = A*numpy.sin(F)

# ********** Zero vector ********** 
vector_zero = osim.Vec3(0,0,0)

# ********** Pedal ********** 
pedal_mass = 0.5
pedal_inertia = osim.Inertia(1,1,1,0,0,0)
pedal_locParent_r    = osim.Vec3(0.02,  0.133,   0.091)
pedal_locParent_l    = osim.Vec3(0.02, -0.146, -0.091)

# ********** Pedal holder ********** 
cleat_mass = 0.25
cleat_inertia = osim.Inertia(1,1,1,0,0,0)
cleat_locParent    = osim.Vec3(0.125,-0.015,0)      # (0.125,-0.018,0)

# ********** Gear ********** 
crank_mass = 1                              
crank_inertia = osim.Inertia(1,1,1,0,0,0) 

# ********** Contact forces  ********** 
stiffness = 1e8
dissipation = 25
friction = 0.9
viscosity = 0.6
transition_vel = 0.1

# ********** Paths and files ********** 
currentPath = pathlib.Path().absolute()
modelName = os.path.join(currentPath, "gait10dof18musc_edit.osim")
newModel = os.path.join(currentPath, "cycling_model.osim")



## INSTANTIATE AN OPENSIM MODEL
myModel = osim.Model(modelName)
myModel.setName("cycling_model")

## GET REFERENCES TO OBJECTS
ground = myModel.getGround()
calcn_r = osim2.find_body(myModel,"calcn_r")
calcn_l = osim2.find_body(myModel,"calcn_l")

## CONSTRUCT BODIES AND JOINTS HERE
# ********** Crank ********** 
crank = osim.Body("crank",crank_mass,vector_zero,crank_inertia)

crank_geometry = osim.Mesh("gear.stl")
crank_geometry.setColor(osim.Black)
crank.attachGeometry(crank_geometry.clone())

myModel.addBody(crank)

crankToGround = osim.PinJoint("crankToGround",crank,vector_zero,vector_zero,ground,vector_zero,vector_zero)

myModel.addJoint(crankToGround)

# ********** Cleats ********** 
cleat_r = osim.Body("cleat_r",cleat_mass,vector_zero,cleat_inertia)
cleat_l = osim.Body("cleat_l",cleat_mass,vector_zero,cleat_inertia)

cleat_geometry = osim.Mesh("cleat_simple.stl")
cleat_geometry.setColor(osim.Red)
cleat_r.attachGeometry(cleat_geometry.clone())
cleat_l.attachGeometry(cleat_geometry.clone())

myModel.addBody(cleat_r)
myModel.addBody(cleat_l)

cleat_r = osim.WeldJoint("cleat_rToCalc",calcn_r,cleat_locParent,vector_zero,cleat_r,vector_zero,vector_zero)
cleat_l = osim.WeldJoint("cleat_lToCalc",calcn_l,cleat_locParent,vector_zero,cleat_l,vector_zero,vector_zero)
myModel.addJoint(cleat_r)
myModel.addJoint(cleat_l)

# ********** Pedals ********** 
cleat_r_body = osim2.find_body(myModel,"cleat_r")
cleat_l_body = osim2.find_body(myModel,"cleat_l")
pedal_r = osim.Body("pedal_r",pedal_mass,vector_zero,pedal_inertia)
pedal_l = osim.Body("pedal_l",pedal_mass,vector_zero,pedal_inertia)

pedal_geometry = osim.Mesh("pedal_simple.stl")
pedal_geometry.setColor(osim.Orange)
pedal_r.attachGeometry(pedal_geometry.clone())
pedal_l.attachGeometry(pedal_geometry.clone())

myModel.addBody(pedal_r)
myModel.addBody(pedal_l)

pedal_rToCrank = osim.PinJoint("pedal_rToCrank",crank,pedal_locParent_r,vector_zero,pedal_r,vector_zero,vector_zero)
pedal_lToCalc = osim.PinJoint("pedal_lToCalc",crank,pedal_locParent_l,vector_zero,pedal_l,vector_zero,vector_zero)

myModel.addJoint(pedal_rToCrank)
myModel.addJoint(pedal_lToCalc)

## MODELING CONTACT FORCES
# Right
pedal_geo_r = osim.ContactMesh("pedal_simple.stl",vector_zero,vector_zero,pedal_r,"pedal_r_contact")
cleat_geo_r = osim.ContactMesh("cleat_simple.stl",vector_zero,vector_zero,cleat_r_body,"cleat_r_contact")
myModel.addContactGeometry(pedal_geo_r)
myModel.addContactGeometry(cleat_geo_r)

contact_r = osim.ElasticFoundationForce()

contact_r.setDissipation(dissipation)
contact_r.setStiffness(stiffness)
contact_r.setStaticFriction(friction)
contact_r.setDynamicFriction(friction)
contact_r.setViscousFriction(viscosity)
contact_r.setTransitionVelocity(transition_vel)

contact_r.setName("contact_r")
contact_r.addGeometry("pedal_r_contact")
contact_r.addGeometry("cleat_r_contact")

myModel.addForce(contact_r)

# Left
pedal_geo_l = osim.ContactMesh("pedal_simple.stl",vector_zero,vector_zero,pedal_l,"pedal_l_contact")
cleat_geo_l = osim.ContactMesh("cleat_simple.stl",vector_zero,vector_zero,cleat_l_body,"cleat_l_contact")
myModel.addContactGeometry(pedal_geo_l)
myModel.addContactGeometry(cleat_geo_l)

contact_l = osim.ElasticFoundationForce()

contact_l.setDissipation(dissipation)
contact_l.setStiffness(stiffness)
contact_l.setStaticFriction(friction)
contact_l.setDynamicFriction(friction)
contact_l.setViscousFriction(viscosity)
contact_l.setTransitionVelocity(transition_vel)

contact_l.setName("contact_l")
contact_l.addGeometry("pedal_l_contact")
contact_l.addGeometry("cleat_l_contact")

myModel.addForce(contact_l)


## CHANGE POSE-GEOMETRY-DIMENSIONS
# get coord
myCoord = myModel.updCoordinateSet()
pelvis_tx = myCoord.get("pelvis_tx")
pelvis_ty = myCoord.get("pelvis_ty")
pelvis_tz = myCoord.get("pelvis_tz")
pelvis_tilt = myCoord.get("pelvis_tilt")
lumbar = myCoord.get("lumbar_extension")
hip_flexion_r = myCoord.get("hip_flexion_r")
knee_angle_r = myCoord.get("knee_angle_r")
ankle_angle_r = myCoord.get("ankle_angle_r")
hip_flexion_l = myCoord.get("hip_flexion_l")
knee_angle_l = myCoord.get("knee_angle_l")
ankle_angle_l = myCoord.get("ankle_angle_l")

# pelvis-crankset adjustment
pelvis_tx.setDefaultValue(pelvis_base_tx + pelvis_tx_crank)
pelvis_ty.setDefaultValue(pelvis_base_ty + pelvis_ty_crank)

# hip-knee-ankle adjustment
hip_flexion_r.setDefaultValue(numpy.deg2rad(70))
knee_angle_r.setDefaultValue(numpy.deg2rad(-104))
ankle_angle_r.setDefaultValue(numpy.deg2rad(34))

hip_flexion_l.setDefaultValue(numpy.deg2rad(28))
knee_angle_l.setDefaultValue(numpy.deg2rad(-33))
ankle_angle_l.setDefaultValue(numpy.deg2rad(5))

# lumbar
lumbar.setDefaultValue(lumbar_base)


# lock bodies
pelvis_tx.setDefaultLocked (True)
pelvis_ty.setDefaultLocked (True)
pelvis_tz.setDefaultLocked (True)
pelvis_tilt.setDefaultLocked (True)
lumbar.setDefaultLocked (True)

## INITIALIZE THE SYSTEM (CHECKS MODEL CONSISTENCY)
myState = myModel.initSystem()

## SAVE THE MODEL TO A FILE
myModel.finalizeConnections()
myModel.printToXML(newModel)



# building model in matlab: https://simtk-confluence.stanford.edu/display/OpenSim/Building+a+Dynamic+Walker+in+Matlab

# Change states (for the future)
# 
# knee_r.getCoordinate().setLocked(myState, True)
# knee_r.getCoordinate().setValue(myState, numpy.deg2rad(-58))
# myModel.equilibrateMuscles(myState)

# Simulate (for the future) https://github.com/opensim-org/opensim-core/issues/1368
# manager = osim.Manager(myModel)
# myState.setTime(0)
# manager.initialize(myState)
# myState = manager.integrate(1)
