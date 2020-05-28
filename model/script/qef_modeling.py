# Import OpenSim libraries
import opensim as osim

# Import other libraries
import pathlib  # get current path
import os.path  # create path
import numpy    # math

# DEFINE KEY MODEL VARIABLES 
pelvisWidth = 0.20;     # ex
thighLength = 0.40;     # ex
shankLength = 0.435;    # ex

# Paths and files
currentPath = pathlib.Path().absolute()
modelName = os.path.join(currentPath, "gait10dof18musc_edit.osim")
newModel = os.path.join(currentPath, "cycling_model.osim")

# DEFINE FUNCTIONS
# Function that finds bodies in the model
def find_body(model,name_body):    
    for body in model.getBodyList():    
        if body.getName() == name_body:
            this_body = body
    return this_body

# Function that finds joints
def find_joint(model,name_joint):
    for joint in model.getJointList():
        if joint.getName() == name_joint:
            this_joint = joint
    return this_joint
    
## Parameters
# === Pedal holder
cleat_mass = 0.25
cleat_inertia = osim.Inertia(1,1,1,0,0,0)
cleat_locParent    = osim.Vec3(0.125,-0.015,0)      # (0.125,-0.018,0)
cleat_orParent = osim.Vec3(0,0,0)
cleat_locChild     = osim.Vec3(0,0,0)
cleat_orChild  = osim.Vec3(0,0,0)

# === Pedal
pedal_mass = 0.5
pedal_inertia = osim.Inertia(1,1,1,0,0,0)     
pedal_orParent = osim.Vec3(0,0,0)
pedal_locChild     = osim.Vec3(0,0,0)
pedal_orChild  = osim.Vec3(0,0,0)

pedal_locParent_r    = osim.Vec3(0.02,  0.133,   0.091)
pedal_locParent_l    = osim.Vec3(0.02, -0.146, -0.091)

# gear
crank_mass = 1                              
crank_inertia = osim.Inertia(1,1,1,0,0,0) 
crank_locParent    = osim.Vec3(0,0,0)   
crank_orParent = osim.Vec3(0,0,0)
crank_locChild     = osim.Vec3(0,0,0)
crank_orChild  = osim.Vec3(0,0,0) 

# body
pelvis_base_tx = 0.085
pelvis_base_ty = 0

# bike geometry
A = 800/1000
F = numpy.deg2rad(73.76)
pelvis_tx_crank = -A*numpy.cos(F)
pelvis_ty_crank = A*numpy.sin(F)

# body pose
lumbar_base = - numpy.deg2rad(50)

# === Contact forces  
contact_loc = osim.Vec3(0,0,0)
contact_or = osim.Vec3(0,0,0)

stiffness = 1e8
dissipation = 25
friction = 0.9
viscosity = 0.6
transition_vel = 0.1

## OPEN MODEL
# Load model
myModel = osim.Model(modelName)
myModel.setName("cycling_model")
myState = myModel.initSystem()

# Find bodies
ground = myModel.getGround()
calcn_r = find_body(myModel,"calcn_r")
calcn_l = find_body(myModel,"calcn_l")

## MODELING GEOMETRIES AND BODIES
# === Crank
crank = osim.Body("crank",crank_mass,crank_orParent,crank_inertia)

crank_geometry = osim.Mesh("gear.stl")
crank_geometry.setColor(osim.Black)
crank.attachGeometry(crank_geometry.clone())

myModel.addBody(crank)

crankToGround = osim.PinJoint("crankToGround",crank,crank_locParent,crank_orParent,ground,crank_locChild,crank_orChild)

myModel.addJoint(crankToGround)

# === Cleats
cleat_r = osim.Body("cleat_r",cleat_mass,cleat_orParent,cleat_inertia)
cleat_l = osim.Body("cleat_l",cleat_mass,cleat_orParent,cleat_inertia)

cleat_geometry = osim.Mesh("cleat_simple.stl")
cleat_geometry.setColor(osim.Red)
cleat_r.attachGeometry(cleat_geometry.clone())
cleat_l.attachGeometry(cleat_geometry.clone())

myModel.addBody(cleat_r)
myModel.addBody(cleat_l)

cleat_r = osim.WeldJoint("cleat_rToCalc",calcn_r,cleat_locParent,cleat_orParent,cleat_r,cleat_locChild,cleat_orChild)
cleat_l = osim.WeldJoint("cleat_lToCalc",calcn_l,cleat_locParent,cleat_orParent,cleat_l,cleat_locChild,cleat_orChild)
myModel.addJoint(cleat_r)
myModel.addJoint(cleat_l)

# ==== Pedals
cleat_r_body = find_body(myModel,"cleat_r")
cleat_l_body = find_body(myModel,"cleat_l")
pedal_r = osim.Body("pedal_r",pedal_mass,pedal_orParent,pedal_inertia)
pedal_l = osim.Body("pedal_l",pedal_mass,pedal_orParent,pedal_inertia)

pedal_geometry = osim.Mesh("pedal_simple.stl")
pedal_geometry.setColor(osim.Orange)
pedal_r.attachGeometry(pedal_geometry.clone())
pedal_l.attachGeometry(pedal_geometry.clone())

myModel.addBody(pedal_r)
myModel.addBody(pedal_l)

pedal_rToCrank = osim.PinJoint("pedal_rToCrank",crank,pedal_locParent_r,pedal_orParent,pedal_r,pedal_locChild,pedal_orChild)
pedal_lToCalc = osim.PinJoint("pedal_lToCalc",crank,pedal_locParent_l,pedal_orParent,pedal_l,pedal_locChild,pedal_orChild)

myModel.addJoint(pedal_rToCrank)
myModel.addJoint(pedal_lToCalc)


## MODELING CONTACT FORCES
# Right
pedal_geo_r = osim.ContactMesh("pedal_simple.stl",contact_loc,contact_or,pedal_r,"pedal_r_contact")
cleat_geo_r = osim.ContactMesh("cleat_simple.stl",contact_loc,contact_or,cleat_r_body,"cleat_r_contact")
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
pedal_geo_l = osim.ContactMesh("pedal_simple.stl",contact_loc,contact_or,pedal_l,"pedal_l_contact")
cleat_geo_l = osim.ContactMesh("cleat_simple.stl",contact_loc,contact_or,cleat_l_body,"cleat_l_contact")
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

## SAVE
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
