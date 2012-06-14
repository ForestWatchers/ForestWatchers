#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
# This script compares files from a directory to those contemplated
# in a specific mapfile. If the file is not in the mapfile it creates
# a unique name based on the filename and add a new layer in the end
# of the mapfile
#
# Eduardo F. P. Luz
# Jun 2012
# 

import os
import sys

#
#Functions for raster images
#

#To map the location of a raster image to an unique identifier
def getRasterLocation(fname):
    pointLoc = fname.find(".")
    locationTemp = fname[0:pointLoc]
    if locationTemp == "AERONET_Rio_Branco":
        location = "a"
    elif locationTemp == "FAS_Brazil1":
        location = "b"
    elif locationTemp == "FAS_Brazil3":
        location = "c"
    elif locationTemp == "FAS_Brazil6":
        location = "d"
    elif locationTemp == "FAS_Brazil7":
        location = "e"
    elif locationTemp == "Peru":
        location = "f"
    return location

#To map the month (in Julian days) to a string (for raster files)
def getRasterMonth(fname):
    pointLoc = fname.find(".")
    monthTemp = fname[pointLoc+5:pointLoc+8]
    if monthTemp == "031":
        month = "jan"
    elif monthTemp == "059" or monthTemp == "060":
        month = "feb"
    elif monthTemp == "090" or monthTemp == "091":
        month = "mar"
    elif monthTemp == "120" or monthTemp == "121":
        month = "apr"
    elif monthTemp == "151" or monthTemp == "152":
        month = "may"
    elif monthTemp == "181" or monthTemp == "182":
        month = "jun"
    elif monthTemp == "212" or monthTemp == "213":
        month = "jul"
    elif monthTemp == "243" or monthTemp == "244":
        month = "aug"
    elif monthTemp == "273" or monthTemp == "274":
        month = "sep"
    elif monthTemp == "304" or monthTemp == "305":
        month = "oct"
    elif monthTemp == "334" or monthTemp == "335":
        month = "nov"
    elif monthTemp == "365" or monthTemp == "366":
        month = "dec"
    return month

#Writing info of the new raster layer in the file
def writeRasterLayer(linesNew,lastLine,path,fname,nameLayer):
    linesNew.insert(lastLine,    "\n  LAYER")
    linesNew.insert(lastLine+1,  "\n    NAME \""+nameLayer+"\"")
    linesNew.insert(lastLine+2,  "\n    DATA \""+path+fname+"\"")
    linesNew.insert(lastLine+3,  "\n    TYPE RASTER")
    linesNew.insert(lastLine+4,  "\n    STATUS ON")
    linesNew.insert(lastLine+5,  "\n    METADATA")
    linesNew.insert(lastLine+6,  "\n      \"wfs_title\"          \"Amazon Image\"")
    linesNew.insert(lastLine+7,  "\n      \"wfs_srs\"            \"EPSG:4326\"")
    linesNew.insert(lastLine+8,  "\n      \"gml_include_items\"  \"all\"")
    linesNew.insert(lastLine+9,  "\n      \"gml_featureid\"      \"ID\"")
    linesNew.insert(lastLine+10, "\n      \"ows_enable_request\" \"*\"")
    linesNew.insert(lastLine+11, "\n    END")
    linesNew.insert(lastLine+12, "\n  END\n")
    return

#
#Functions for shape files
#

#To map the month to a string (for shape files)
def getShapeMonth(fname):
    pointLoc = fname.find("_")
    monthTemp = fname[pointLoc+5:pointLoc+7]
    if monthTemp == "01":
        month = "jan"
    elif monthTemp == "02":
        month = "feb"
    elif monthTemp == "03":
        month = "mar"
    elif monthTemp == "04":
        month = "apr"
    elif monthTemp == "05":
        month = "may"
    elif monthTemp == "06":
        month = "jun"
    elif monthTemp == "07":
        month = "jul"
    elif monthTemp == "08":
        month = "aug"
    elif monthTemp == "09":
        month = "sep"
    elif monthTemp == "10":
        month = "oct"
    elif monthTemp == "11":
        month = "nov"
    elif monthTemp == "12":
        month = "dec"
    return month

#Writing info of the new shape layer in the file
def writeShapeLayer(linesNew,lastLine,path,fname,nameLayer):
    linesNew.insert(lastLine,    "\n  LAYER")
    linesNew.insert(lastLine+1,  "\n    NAME \""+nameLayer+"\"")
    linesNew.insert(lastLine+2,  "\n    METADATA")
    linesNew.insert(lastLine+3,  "\n      \"wfs_title\"          \"Amazon Cloud\"")
    linesNew.insert(lastLine+4,  "\n      \"wfs_srs\"            \"EPSG:4326\"")
    linesNew.insert(lastLine+5,  "\n      \"gml_include_items\"  \"all\"")
    linesNew.insert(lastLine+6,  "\n      \"gml_featureid\"      \"ID\"")
    linesNew.insert(lastLine+7,  "\n      \"ows_enable_request\" \"*\"")
    linesNew.insert(lastLine+8,  "\n    END")
    linesNew.insert(lastLine+9,  "\n    TYPE POLYGON")
    linesNew.insert(lastLine+10, "\n    STATUS ON")
    linesNew.insert(lastLine+11, "\n    DATA \""+path+fname+"\"")
    linesNew.insert(lastLine+12, "\n    PROJECTION")
    linesNew.insert(lastLine+13, "\n      \"init=epsg:4326\"")
    linesNew.insert(lastLine+14, "\n    END")
    linesNew.insert(lastLine+15, "\n    CLASS")
    linesNew.insert(lastLine+16, "\n      NAME \"Amazon\"")
    linesNew.insert(lastLine+17, "\n      STYLE")
    linesNew.insert(lastLine+18, "\n        COLOR 255 128 128")
    linesNew.insert(lastLine+19, "\n        OUTLINECOLOR 96 96 96")
    linesNew.insert(lastLine+20, "\n      END")
    linesNew.insert(lastLine+21, "\n    END")
    linesNew.insert(lastLine+22, "\n  END\n")
    return


#######################
# Begin of the script #
#######################

#Name of the original map file
origFile = "maps2011.map"

#Let's get a mirror of the original file in the memory
inFile = open(origFile,"r")
textOrig = inFile.read()
inFile.seek(0)
linesOrig = inFile.readlines()
inFile.close()

#Create a copy to build the new mapfile
linesNew = linesOrig

#Get the number of lines in the original file
lastLine = len(linesOrig)

#Set the directory which contains the files (raster and/or shape)
path = "/home/eduardo/Testes/Cloud_2011/"

#Get a list of the files in the directory
dirList = os.listdir(path)

#For each file in the directory
for fname in dirList:
    
    #Let's only look for tif, geotif or shp files
    if fname[-4:] == '.tif' or fname[-7:] == '.geotif' or fname[-4:] == '.shp':
        
        #Set the filename as the search parameter
        search = fname
        
        #Search in the original mapfile
        index = textOrig.find(search)
        
        #If the file name is not found in the original file
        if index == -1:

            #Building an unique ID for the name of the layer
            #First for shapefiles
            if fname[-4:] == '.shp':
                #Let's warn the user
                print "New Shapefile file detected:", fname

                #For shape files it's based on year and month
                pointLoc = fname.find("_")
                year = fname[pointLoc+1:pointLoc+5]
                month = getShapeMonth(fname)
                nameLayer = "shp_cld_"+month+year

                #Get the last line of the new map file
                lastLine = len(linesNew)
            
                #Append the new layer in the new file
                writeShapeLayer(linesNew,lastLine-2,path,fname,nameLayer)

            #Then for raster images
            else:
                #Let's warn the user
                print "New GeoTIFF file detected:", fname            

                #For raster images it's based on the location of the image, year and month
                location = getRasterLocation(fname)
                pointLoc = fname.find(".")
                year = fname[pointLoc+1:pointLoc+5]
                month = getRasterMonth(fname)
                nameLayer = month+year+location
            
                #Get the last line of the new map file
                lastLine = len(linesNew)
            
                #Append the new layer in the new file
                writeRasterLayer(linesNew,lastLine-2,path,fname,nameLayer)

#Write down the new map file
outfile = open("NEW_"+origFile, "w")
outfile.write("".join(linesNew))
outfile.close()

#
#End of the script
#
