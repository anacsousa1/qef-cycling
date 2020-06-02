
# DEFINE FUNCTIONS
def find_body(model,name_body):     # finds bodies
    for body in model.getBodyList():    
        if body.getName() == name_body:
            this_body = body
    return this_body

def find_joint(model,name_joint): # find joints
    for joint in model.getJointList():
        if joint.getName() == name_joint:
            this_joint = joint
    return this_joint