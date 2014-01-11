''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      11 January 2014

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Outputs the routes created in readable formats

#######################################################################################################
'''

import MySQLdb
import time
import datetime
import logging

import Reference as r
#from RouteCalculation import StationsOnTheSameLine

def InsertHistogramIntoDatabase(TimesHistogram):
    ''' Uploads the TimesHistogram into the database '''
    
    FN_NAME = "InsertHistogramIntoDatabase"
    
    try: 
        if TimesHistogram:
            ListOfKeys = [i for i in TimesHistogram.keys()]
            
            # Establish the connection to the database
            db = MySQLdb.connect(
                                 host=r.DB_HOST,
                                 user=r.DB_USER,
                                 passwd=r.DB_PASSWORD,
                                 db=r.DB_NAME
                                 )
            cur = db.cursor()
            
            # Create the multiple entry SQL query
            HistogramQuery = "UPDATE " + r.DB_TABLE_SUMMARY_STATS + " SET " + r.SUMSTAT_FIELD_FREQ + " = CASE " + r.SUMSTAT_FIELD_TIMESLOT
        
            for i in ListOfKeys:
                HistogramQuery = HistogramQuery + " WHEN " + str(i) + " THEN " + r.SUMSTAT_FIELD_FREQ + " + " + str(TimesHistogram[i])
            
            HistogramQuery = HistogramQuery + " END WHERE " + r.SUMSTAT_FIELD_TIMESLOT + " BETWEEN " + str(min(ListOfKeys)) + " AND " + str(max(ListOfKeys)) + ";"
        
            cur.execute (HistogramQuery)
                            
            db.commit()
            
        else:
            logging.error('%s: No histrogram passed to function', FN_NAME)
    
    except Exception, e:
        logging.error('%s: Generated error in operation', FN_NAME)
        logging.error('%s: Query:\n%s' % (FN_NAME,HistogramQuery))
        logging.exception('Traceback message: \n%s',e)
        
    else:
        logging.debug('%s: Histrogram inserted into table without error', FN_NAME)
        
    finally:
        db.close()

def CreateTimeStamp():
    '''Create a timestamp with which to mark the log entry'''
        
    ts = time.time()
    TimeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return TimeStamp

def GetDatabaseShortestRoute():
    ''' Gets the shortest route from the database so that only routes shorter than that are stored '''
    
    FN_NAME = "GetDatabaseShortestRoute"
    
    try:
        # Establish the connection to the database
        db = MySQLdb.connect(
                             host=r.DB_HOST,
                             user=r.DB_USER,
                             passwd=r.DB_PASSWORD,
                             db=r.DB_NAME
                             )
        cur = db.cursor()
        
        ShortestDistanceQuery = "SELECT MIN(" + r.SHORTROUTE_DISTANCE + ") FROM " + r.DB_TABLE_SHORTEST_ROUTE + ";"
        
        # Retrieve the shortest current route from the database
        cur.execute(ShortestDistanceQuery)
        ShortestDistance = cur.fetchone()
        
    except Exception, e:
        logging.error('%s: Unable to retrieve shortest route from the database', FN_NAME)
        logging.error('%s: Query:\n%s' % (FN_NAME,ShortestDistanceQuery))
        logging.exception('Traceback message: \n%s',e)
        
        ShortestDistance = (1100,) # Value chosen as the approximate lower limit of what the current process is capable of generating
    
    else:
        logging.debug('%s: Shortest route returned from database without error', FN_NAME)
        logging.debug('%s: Shortest route: %s' %(FN_NAME,ShortestDistance[0]))
    
    finally:
        db.close()        
        return ShortestDistance[0]
    

def InsertShortestRouteIntoDatabase(Route, RouteTime):
    ''' Updates the database with a record of the shortest route '''
    
    FN_NAME = "InsertShortestRouteIntoDatabase"
    
    try:
        # Establish the connection to the database
        db = MySQLdb.connect(
                             host=r.DB_HOST,
                             user=r.DB_USER,
                             passwd=r.DB_PASSWORD,
                             db=r.DB_NAME
                             )
        cur = db.cursor()
    
        ShortestDistance = GetDatabaseShortestRoute()
    
        # Test if the new route is shorter than the current shortest route: if so, upload it
        if ShortestDistance == None or RouteTime < ShortestDistance:
            
            RouteDescription_Long = PrintRouteInHTMLFormat(Route)
            DateTime = CreateTimeStamp()
            
            InputRouteQuery = 'INSERT INTO ' + r.DB_TABLE_SHORTEST_ROUTE + '(' + r.SHORTROUTE_DISTANCE + ', ' + r.SHORTROUTE_DESC_LIST + ', ' + r.SHORTROUTE_DESC_LONG + ', ' + r.SHORTROUTE_DATETIME + ') VALUES (' + str(RouteTime) + ', "' + str(Route) + '", "' + RouteDescription_Long + '", "' + str(DateTime) + '");'
            cur.execute (InputRouteQuery)
                        
            db.commit()
            
    except Exception, e:

        logging.error('%s: Unable to populate database with shortest route', FN_NAME)
        logging.error('%s: ShortestDistance: %s' %(FN_NAME,ShortestDistance))
        logging.error('%s: RouteTime: %s' %(FN_NAME,RouteTime))
        logging.error('%s: Query:\n%s' % (FN_NAME,InputRouteQuery))
        logging.exception('Traceback message: \n%s',e)
        
    else:
        logging.debug('%s: Database populated with shortest route without error', FN_NAME)
    
    finally:        
        db.close()

def FindCommonLine(CurrentStation, NextStation):
    ''' Finds a tube line that contains both the stations passed '''
    
    for Line in r.LINES_AND_STATIONS.keys():
        if CurrentStation in r.LINES_AND_STATIONS[Line]:
            if NextStation in r.LINES_AND_STATIONS[Line]:
                return Line
  
    return "(No Line Found)"

def ParseRouteList(Route):
    ''' Removes from the route instances where consecutive stations are duplicated '''
    
    Output = []
    
    Output.append(Route[0])
    
    for i in range(1,len(Route)):
        if Route[i] != Output[-1]:
            Output.append(Route[i])
    
    return Output

def PrintRouteInHTMLFormat(InputRoute):
    ''' Outputs the route to the console in the form of readable user directions '''
    
    FN_NAME = "PrintRouteInHTMLFormat"
    
    Output = ""
    
    try:
        # Tidy the route to remove any duplicates
        Route = ParseRouteList(InputRoute)
        
        ChangeStation = Route[0]
        CurrentLine = 'Piccadilly' # Included as default, if the first station is on a different line the first step below will catch it
    
        StationsEnRoute = []
        
        Output = Output + "Start at " + ChangeStation + "[br/]" # Square brackets to accomodate the 'Allow PHP in Posts and Pages' Wordpress plugin
        
        for i in range(1,len(Route) - 1):
            
            # If the next station is on a different line, find a line that joins them
            if not Route[i] in r.LINES_AND_STATIONS[CurrentLine]:
                CurrentLine = FindCommonLine(Route[i-1], Route[i])
            
            # Pass over any intermediary stations unless they are at the end of the line
            if Route[i+1] in r.LINES_AND_STATIONS[CurrentLine] and not Route[i] in r.NODES_SINGLE:
                StationsEnRoute.append(Route[i])
            
            # Otherwise, output to the console
            else:
        
                if StationsEnRoute == []:                    
                    Output = Output + "Go to " + Route[i] + " on the " + CurrentLine.upper() + " line" + "[br/]" 
                    
                else:
                    Output = Output + "Go to " + Route[i] + " on the " + CurrentLine.upper() + " line via " + str(StationsEnRoute) + "[br/]"
                
                StationsEnRoute = [] # Clear the en route stations for the next iteration
    
        Output = Output + "Finish at " + Route[-1]
    
    except Exception, e:
        logging.error('%s: Unable to generate readable route description', FN_NAME)
        logging.error('%s: InputRoute: \n%s' %(FN_NAME,InputRoute))
        logging.error('%s: CurrentLine: %s' %(FN_NAME,CurrentLine))
        logging.error('%s: StationsEnRoute: %s' %(FN_NAME,StationsEnRoute))
        logging.error('%s: Output before error: \n%s' %(FN_NAME,Output))
        logging.exception('Traceback message: \n%s',e)
        
        Output = "ERROR: Unable to generate readable route description, please check log for details"
    
    else:
        logging.debug('%s: Readable route description created without error', FN_NAME)     
    
    finally:
        return Output
    
