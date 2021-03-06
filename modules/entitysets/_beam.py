# Copyright (c) 2013 Connor Sherson
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#
#    3. This notice may not be removed or altered from any source
#    distribution.

from entity import Entity
import pygame, math

from imageload import loadImageNoAlpha

def queueCollideWithBeam( givenBeam, givenObject ):
    curPlayState = givenObject.groups()[0].playState
    curPlayState.postStepQueue.append( ( collideWithBeam, givenBeam, givenObject ) )

def collideWithBeam( givenBeam, givenObject ):
    if "Missile" in givenObject.__class__.__name__:
        givenObject.kill()

class Beam( Entity ):
    width = 4
    height = 16

    playStateGroup = "genericStuffGroup"
    setName = "genericstuff"

    sheet = pygame.Surface((width,height)).convert()
    sheet.fill( pygame.Color( 0, 255, 0 ) )

    instanceSpecificVars = None

    notEditable = True

    specialCollision = queueCollideWithBeam

    collidable = True
    solid = False
    
    def __init__( self, pos, force, group=None, **kwargs ):
        Entity.__init__( self, pos, [0,0], None, group, pygame.Rect( 0, 0, self.width, self.height ), animated=True, **kwargs )
        self.setRotation( math.atan( force[1]/force[0] )+math.pi/2 )
        self.body.velocity_limit = 400
        if Beam.instanceSpecificVars is None:
            attrList = list( self.__dict__.keys() )
        self.startPos = pos
        self.force = force
        if Beam.instanceSpecificVars is None:
            Beam.instanceSpecificVars = dict( [ ( eachKey, eachVal ) for eachKey, eachVal in self.__dict__.items() if eachKey not in attrList ] )
        self.body.apply_force(force)

    def update( self, dt ):
        Entity.update( self, dt )

entities = { "Beam":Beam }
