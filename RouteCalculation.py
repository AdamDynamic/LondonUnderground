''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      11 January 2014

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Contains all code relevant to the random calculation of tours of the London Underground

#######################################################################################################
'''

import MySQLdb
import MySQLdb.cursors

import math
import random
import logging

import Reference as r
import Dijkstras as d

def StationsOnTheSameLine(Station1, Station2):
    ''' Tests whether two stations share the same tube line '''
    
    FN_NAME = "StationsOnTheSameLine"
    
    ProcessResult = False
    
    try:
        ListOfLines = [Line for Line in r.LINES_AND_STATIONS.keys()]
        
        for TubeLine in ListOfLines:
            if Station1 in r.LINES_AND_STATIONS[TubeLine]: 
                if Station2 in r.LINES_AND_STATIONS[TubeLine]:
                    ProcessResult = True
    
    except Exception, e:
        logging.error('%s: Unable to determine if stations are on the same line', FN_NAME)
        logging.exception('Traceback message: \n%s',e)
        
    else:
        logging.debug('%s: Process run without error', FN_NAME)
        
    finally:
        return ProcessResult


def GetLengthOfRoute(RouteList):
    ''' 
    Determines the length of the route using the dictionary of distamce between station 
    Assumes that the passed RouteList is of the format ['Station1', 'Station2', ... , 'Station100']
    '''
    
    FN_NAME = "GetLengthOfRoute"
    
    RouteLength = 0.0
    CurrentStation = ""
    PreviousStation = ""
    NextStation = ""
        
    NumberOfLineChanges = 0
    NumberOfReversals = 0
    
    try:

        DistanceDict = r.STATIONS_DISTANCES_PEAK
        
        for i in range(0,len(RouteList)-1):
            
            CurrentStation = RouteList[i]
            NextStation = RouteList[i+1]
    
            if CurrentStation == NextStation:
                pass
            
            elif NextStation in DistanceDict[CurrentStation].keys():
                
                # Find the distance to the next station
                RouteLength = RouteLength + DistanceDict[CurrentStation][NextStation]
                
                # If the trains are on different lines, add time for a line change between platforms
                if not StationsOnTheSameLine(CurrentStation, NextStation):
                    RouteLength = RouteLength + r.DEFAULT_LINE_CHANGE
                    NumberOfLineChanges = NumberOfLineChanges + 1
    
                # Check if the next station is the same as the previous station (indicates turning around which takes time)
                if NextStation == PreviousStation:
                    RouteLength = RouteLength + r.DEFAULT_LINE_CHANGE
                    NumberOfReversals = NumberOfReversals + 1          
                
                PreviousStation = CurrentStation
            
            else:
                TempRoute = d.DijkstraShortestPath(DistanceDict,CurrentStation,NextStation)
                RouteLength = RouteLength + GetLengthOfRoute(TempRoute) # Iterate the new route back (will not account for changes of lines, platform waits etc when determining the shortest route)
        
        # Add time for the number of pauses at station platforms (ignore instances of reversals and line changes to avoid duplication)
        RouteLength = RouteLength + (r.DEFAULT_STATION_WAIT * (len(RouteList) - 1 - NumberOfLineChanges - NumberOfReversals))
    
    except Exception, e:
        logging.error('%s: Unable to determine the length of the route', FN_NAME)
        logging.error('%s: RouteList: %s' %(FN_NAME,RouteList))
        logging.exception('Traceback message: \n%s',e)
    
    else:
        logging.debug('%s: Process run without error', FN_NAME)
        logging.debug('%s: RouteLength: %s' %(FN_NAME,RouteLength))
    
    finally:    
        return RouteLength

def WeightedStationChoose(InputDict):
    ''' Returns a random station based on the inputted weighted dictionary so that closer stations are strongly preferred '''
    
    FN_NAME = "WeightedStationChoose"
    
    try:
        if InputDict != None:
      
            TotalWeighting = sum(InputDict.itervalues())
        
            if TotalWeighting > 1:
                RandomNumber = random.randrange(0, int(TotalWeighting)-1)
            
                Temp = 0
            
                for key, weight in InputDict.iteritems():
            
                    Temp += weight
                    if RandomNumber < Temp:
                        return key
                    
        else:
            logging.error('%s: No InputDict passed to function', FN_NAME)
            
    except Exception, e:
        
        logging.error('%s: Unable to choose random station', FN_NAME)
        logging.error('%s: InputDict: %s' %(FN_NAME,InputDict))
        logging.exception('Traceback message: \n%s',e)
        
        if InputDict != None:
            return InputDict[0]
            

def CreateWeightedDict(InputDict):
    ''' Creates a weighted dictionary of distances with the nearest station having the highest value '''
    
    FN_NAME = 'CreateWeightedDict'
    
    OutputDict = {}
    
    try:
        if InputDict:
    
            MaxDistance = max(InputDict.values())
            MinDistance = min(InputDict.values()) # The closest station is scaled to have weighting 1.0
            ExponentialScalingFactor = -50.0 # Value chosen by trial and error to give reasonable division of weightings
            
            for Station in InputDict.keys():
    
                ScalingFactor = (ExponentialScalingFactor*((InputDict[Station] - MinDistance) / MaxDistance))
                OutputDict[Station] = (math.exp(ScalingFactor))*100000 
                
            return OutputDict
        
        else:
            logging.error('%s: No InputDict passed to function', FN_NAME)
            
    except Exception, e:
        logging.error('%s: Unable to create weighted dictionary', FN_NAME)
        logging.exception('Traceback message: \n%s',e)


def GetAllDistancesFromDatabase(CurrentStation):
    ''' Returns from the database all distances from the CurrentStation to all other stations on the network '''
    
    FN_NAME = "GetAllDistancesFromDatabase"
    
    OutputDict = {}
    
    try:
        # Establish the connection to the database
        db = MySQLdb.connect(
                             host=r.DB_HOST,
                             user=r.DB_USER,
                             passwd=r.DB_PASSWORD,
                             db=r.DB_NAME,
                             cursorclass=MySQLdb.cursors.DictCursor
                             )
        cur = db.cursor()
        
        # Create a dictionary of unvisited stations with distances to the current station   
        DistanceQuery = "SELECT `StationTo`, `Distance` FROM `tbl_StationDistancesComplete` WHERE `StationFrom` = '" + CurrentStation + "';"
        cur.execute(DistanceQuery)
        
        DistanceResult = cur.fetchall()
        
        if DistanceResult != {}:
            # Unpack the database result into a standard format
            for StationPair in DistanceResult:
                OutputDict[StationPair['StationTo']] = StationPair['Distance']
    
    except Exception, e:
        logging.error('%s: Unable to get all distances from the database', FN_NAME)
        logging.error('%s: Query: \n%s' %(FN_NAME,DistanceQuery))
        logging.exception('Traceback message: \n%s',e)
            
    else:
        logging.debug('%s: Process run without error', FN_NAME)
    
    finally:
        db.close()
        return OutputDict

def RemoveVisitedStationsFromDict(DistancesDict, StationsAlreadyVisited):
    ''' Returns an updated dictionary of distances with entries to stations already visited in the tour removed '''
    
    Output = DistancesDict.copy() # Copy the distances dictionary as del deletes entries from the database in place
    
    for Station in StationsAlreadyVisited:
        if Station in Output.keys():
            del Output[Station]
      
    return Output

def ChooseNextStation(DistancesDict):
    ''' Uses a dictionary of distances to unvisited stations to choose the next station to visit '''
    
    NextStation = ""
    
    WeightedDict = CreateWeightedDict(DistancesDict)
        
    if WeightedDict != {}:    
        NextStation = WeightedStationChoose(WeightedDict)

    if NextStation != None:   
        return NextStation
   
def CreateRandomRoute(CurrentStation):
    '''
    Creates and returns a random route of all stations on the network as an ordered list 
    '''
    
    FN_NAME = "CreateRandomRoute"
    
    StationsAlreadyVisited = [CurrentStation]
    StationsPassedOnRoute = [] 
           
    RouteShortest = [CurrentStation]
     
    try:
        # Continue the process until all of the stations have been visited
        while len(StationsAlreadyVisited) < r.TOTAL_NUMBER_OF_STATIONS:
    
            if CurrentStation == "":
                print "No value in CurrentStation varible"
                break
            
            else:
                
                # Test the adjacent stations, if any of them are unvisited then pass the unvisited stations to the weighting algorithm
                AdjacentStations = r.STATIONS_DISTANCES_PEAK[CurrentStation]            
                AdjacentStationsNotVisited = list(set(AdjacentStations.keys()) - set(StationsAlreadyVisited))
                
                if len(AdjacentStationsNotVisited) != 0:
                    
                    # Remove statoins already visited
                    AdjacentStations = RemoveVisitedStationsFromDict(AdjacentStations,StationsAlreadyVisited)
                    
                    NextStation = ChooseNextStation(AdjacentStations)
                
                else:
                    
                    # Retireve all distances from the database (takes longer than using the References constants so only used if required)
                    AllStationsDict = GetAllDistancesFromDatabase(CurrentStation)
                    
                    # Remove stations already visited from the stations to be considered
                    AllStationsDict = RemoveVisitedStationsFromDict(AllStationsDict,StationsAlreadyVisited)    
                    
                    NextStation = ChooseNextStation(AllStationsDict)
                
                
                if NextStation != None:
                    # Add stations passed en-route to the next station to the StationsAlreadyVisited
                    StationsPassedOnRoute = d.DijkstraShortestPath(r.STATIONS_DISTANCES_PEAK, CurrentStation, NextStation)
                    
                    # Update the tracking data
                    RouteShortest = RouteShortest + StationsPassedOnRoute[1:] # Only add new stations from StationsPassedOnRoute
                else:
                    print "No 'NextStation' selected"
                    break
    
                StationsAlreadyVisited = list(set(StationsAlreadyVisited + [CurrentStation] + StationsPassedOnRoute)) 
                
                # Repeat the process, starting at the new station
                CurrentStation = NextStation
    
    except Exception, e:
        logging.error('%s: Unable to create random route', FN_NAME)
        logging.error('%s: CurrentStation: %s' %(FN_NAME,CurrentStation))
        logging.error('%s: NextStation: %s' %(FN_NAME,NextStation))
        logging.exception('Traceback message: \n%s',e)
    
    else:
        logging.debug('%s: Process run without error', FN_NAME)
        logging.debug('%s: Random route generated: \n%s' %(FN_NAME,RouteShortest))
    
    finally:
        return RouteShortest  







    
    

    