#    Copyright (c) 2012 Connor Sherson
#
#    This file is part of ThisHackishMess
#
#    ThisHackishMess is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from entity import *
import pygame, os
from pygame.locals import *

from masterentityset import *

from picklestuff import *

def levelWarpFunc( givenWarp, givenObject ):
    curPlayState = givenObject.groups()[0].playState
    if givenObject in curPlayState.playersGroup:
        givenWarp.collidedWith.add( givenObject.id )
        if givenObject not in givenWarp.ignore:
            dest = loadPlayState( os.path.join( "data", "maps", givenWarp.tags["warpDest"] ), curPlayState.floor.tileSet )
            if dest is None:
                return None
            targetWarp = None
            for each in dest.levelWarpGroup:
                if each.tags.get("warpKey") == givenWarp.tags["warpKey"]:
                    targetWarp = each
                    break
            if targetWarp is None:
                print "No levelWarp with warpKey: " + givenWarp.tags["warpKey"] + " appears to exist in the destination map."
                return None
            givenObject.removeFromGroup( curPlayState.playersGroup )
            for each in givenObject.children:
                each.removeFromGroup( curPlayState.playersGroup )
            givenObject.body.position = targetWarp.body.position.x, targetWarp.body.position.y
            curPlayState.swap( dest )
            givenObject.addToGroup( curPlayState.playersGroup )
            for each in givenObject.children:
                each.addToGroup( curPlayState.playersGroup )
            targetWarp.ignore.add( givenObject.id )
            targetWarp.collidedWith.add( givenObject.id )
            curPlayState.rerenderEverything = True

def queueLoad( givenWarp, givenObject ):
    curPlayState = givenObject.groups()[0].playState
    curPlayState.postStepQueue.append( ( levelWarpFunc, givenWarp, givenObject ) )

class LevelWarp( Entity ):

    scale = 2 
    
    width = 16
    height = 16

    playStateGroup = "levelWarpGroup"
    setName = "levelwarp"

    sheetFileName = "block.png"
    sheet = loadImage( sheetFileName, scale )

    specialCollision = queueLoad
    collidable = True
    solid = False
    mass = 20

    instanceSpecificVars = None
    
    def __init__( self, pos = [0,0], vel = [0,0], group=None, **kwargs ):
        Entity.__init__( self, pos, [0,0], None, group, pygame.Rect( 0, 0, self.width, self.height ), animated=False, **kwargs )
        if LevelWarp.instanceSpecificVars is None:
            attrList = list( self.__dict__.keys() )

        #self.shape.collision_type = 1
        self.tags["warpKey"] = "prime"
        self.tags["warpDest"] = "testthingy"
        self.ignore = set([])
        self.collidedWith = set([])

        if LevelWarp.instanceSpecificVars is None:
            LevelWarp.instanceSpecificVars = dict( [ ( eachKey, eachVal ) for eachKey, eachVal in self.__dict__.items() if eachKey not in attrList ] )
    
    def update( self, dt ):
        Entity.update( self, dt )
        for each in self.groups()[0].playState.playersGroup:
            if each.id not in self.collidedWith and each.id in self.ignore:
                self.ignore.remove( each.id )
        self.collidedWith = set([])
        

MasterEntitySet.entsToLoad.append( LevelWarp )
