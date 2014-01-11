''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      11 January 2014

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Contains code relevant to the import of data and the creation of constants used in the REFERENCE module
                    The functions are not used during the running of the RouteCalculation processes

#######################################################################################################
'''

import csv
import logging
import MySQLdb

import Reference as r
import Dijkstras as d
from RouteCalculation import GetLengthOfRoute

def CreateDistanceDictionaryFromCsv(CsvFilePath):
    ''' Creates a dictionary of distances from a specially-formated inputted CSV file
     Output format: { CurrentStation : { AdjacentStation1 : 100 , AdjacentStation2 : 50 }} '''
    
    OutputDict = {}
    
    with open(CsvFilePath, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row == ['','','','']: # Prevent blank rows from being imported by stopping when it encounters the first one
                break
            else:
                # If the station exists already, append the new distance, otherwise create a new dictionary
                if row[0]in OutputDict.keys(): 
                    OutputDict[row[0]][row[1]] = float(row[2])
                else:
                    OutputDict[row[0]] = { row[1] : float(row[2]) }

    return OutputDict

def CreateListOfLines(CsvFilePath):
    ''' Creates a dictionary of stations in each tube line '''
    OutputDict = {}
    
    with open(CsvFilePath, mode='r') as infile:
        reader = csv.reader(infile)
        
        for row in reader:
            
            # Check if the line exists
            if row[3] in OutputDict.keys():
                
                # Only add stations that don't already exist in the list
                if row[0] not in OutputDict[row[3]]:
                    OutputDict[row[3]].append(row[0])
                
                if row[1] not in OutputDict[row[3]]:
                    OutputDict[row[3]].append(row[1])
                OutputDict[row[3]]
            # If the line doesn't exist, create it    
            else:
                OutputDict[row[3]] = [row[0], row[1]]
    
    # Sort the list of stations before returning
    for Line in OutputDict.keys():
        OutputDict[Line].sort()
                
    return OutputDict

def CreateCompleteListOfStations(DistanceDict):
    ''' Creates a complete ordered list of all stations '''
    
    OutputList = []
    
    for Station in DistanceDict.keys():
        OutputList.append(Station)
        
        for AdjacentStation in DistanceDict[Station].keys():
            OutputList.append(AdjacentStation)
    
    Output = list(set(OutputList)) # Ensures that the values are unique
    
    Output.sort()
    
    return Output 


def GetNodesFromGraph(StationDistances):
    ''' Returns a list of all stations with 1 or 3+ connecting stations to exclude stations on edges '''
    
    Output = []
    
    for Station in r.STATIONS_COMPLETE:

        # Include nodes where the second station is not connected by the tube
        if (len(StationDistances[Station]) == 2 and (Station in list(set((r.LINES_AND_STATIONS['Bus'] + r.LINES_AND_STATIONS['Overland'] + r.LINES_AND_STATIONS['Walking'])))))  or (len(StationDistances[Station]) != 2):
            
            Output.append(Station)
    
    Output = list(set(Output)) # Ensures that the values are unique
    Output.sort()
    
    return Output


def CreateCompleteDictOfDistances(StationsDistances):
    ''' Given the graph of stations with distances to adjacent stations, returns a complete matrix of all distances between every station using Dijkstras algorithm'''
    
    FN_NAME = "CreateCompleteDictOfDistances"
        
    OutputDict = {}
    
    
    try:
        AllStations = list(set([Station for Station in StationsDistances.keys()]))
    
        # Test every combinations of stations with every other station
        for StartStation in AllStations:
            
            DistancesDict = {}
            
            for TargetStation in AllStations:
                
                if StartStation == TargetStation:
                    pass
                
                else:
                    PathToTargetStation = d.DijkstraShortestPath(r.STATIONS_DISTANCES_PEAK,StartStation,TargetStation)
    
                    # Accounts for times taken to change platform, wait at the station between stops and exit to the street (where relevant) 
                    TotalDistance = GetLengthOfRoute(PathToTargetStation)
                       
                    DistancesDict[TargetStation] = TotalDistance 
              
            OutputDict[StartStation] = DistancesDict
    
    except Exception, e:
        logging.error('%s: Unable to create dictionary of distances', FN_NAME)
        logging.exception('Traceback message: \n%s',e)
        
    else:
        logging.debug('%s: Process run without error', FN_NAME)
        
    finally:            
        return OutputDict

def PopulateDistancesDatabase():
    ''' Populates a MySQL database with a complete list of distances from a station to every other station '''
    
    FN_NAME = 'PopulateDistancesDatabase'
    
    try:
        # Establish the connection to the database
        db = MySQLdb.connect(
                             host=r.DB_HOST,
                             user=r.DB_USER,
                             passwd=r.DB_PASSWORD,
                             db=r.DB_NAME
                             )
        cur = db.cursor()
        
        # Create a dictionary of all distances from each station to every other
        DistancesDict = CreateCompleteDictOfDistances(r.STATIONS_DISTANCES_PEAK)
        
        ListOfStations = list(set([Station for Station in DistancesDict.keys()]))
        
        if ListOfStations:
            
            # Clear the existing data from the database
            cur.execute("TRUNCATE TABLE " + r.DB_TABLE_DISTANCES_COMPLETE + ";" )
            
            for FromStation in ListOfStations:
                for ToStation in ListOfStations:
                    
                    if FromStation == ToStation:
                        pass
                    else:
                    
                        # Define the columns the values will be entered into
                        InsertResultsQuery = "INSERT INTO " + r.DB_TABLE_DISTANCES_COMPLETE + " ( " + r.DISTCOMP_FIELD_STATIONTO + ", " + r.DISTCOMP_FIELD_STATIONFROM + "\
                        , " + r.DISTCOMP_FIELD_DISTANCE + ") VALUES ('" + str(FromStation.strip()) + "', '" + str(ToStation.strip()) + "'\
                        , " + str(DistancesDict[FromStation][ToStation]) + ");" 
                        
                        print InsertResultsQuery
                        
                        cur.execute (InsertResultsQuery)
                        
            db.commit()
             
        else:
            logging.error('%s: No ListOfStations generated', FN_NAME)
    
    except Exception, e:
        logging.error('%s: Unable to populate distances database', FN_NAME)
        logging.error('%s: Query: %s' %(FN_NAME,InsertResultsQuery))
        logging.exception('Traceback message: \n%s',e)
        
    else:
        logging.debug('%s: Process run without error', FN_NAME)
    
    finally:
        db.close()
        
'''
print "Start"

PopulateDistancesDatabase()


Output = CreateDistanceDictionaryFromCsv(r.CSV_FILE_PATH)
a = Output.keys()
a.sort()
for i in a:
    Temp = Output[i]
    #Temp.sort()
    print "'" + i + "' : " + str(Temp) + ","


    
Output = CreateCompleteListOfStations(r.STATIONS_DISTANCES_PEAK)
print Output
#for i in Output:
#    print "'" + i + "'," 
print "End"
'''
