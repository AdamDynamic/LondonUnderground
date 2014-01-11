''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      11 January 2014

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Creates a random tube route and stores them in a database

#######################################################################################################
'''

import random
import logging

import Reference as r
import RouteOptimisation as o
import RouteCalculation as c
import DataOutput as d

FN_NAME = "TubeChallenge"

logging.basicConfig(filename='TubeChallenge_LogFile.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logging.info('%s - START', FN_NAME)

ShortestRoute = []
NumberOfIterations = 1000

# Updates are only written to the database if shorter than the current shortest route in the database
ShortestRouteTime = d.GetDatabaseShortestRoute()

# Used to create performance histrogram to update the summary stats table
TimesHistogram = {i : 0 for i in range(900,4000,10)} 

i = 1

try:

    while i <= NumberOfIterations:
        
        # Choose a random start station from all the single nodes:
        StartStation = random.choice(r.NODES_SINGLE)
        
        # Randomly generate a route starting at the START_STATION
        CurrentRoute = c.CreateRandomRoute(StartStation)
        
        # Optimise the route to remove duplicates and unnecessary loop-backs
        CurrentRoute = o.ParseListForDuplicates(CurrentRoute)
        
        # Measure the length of the route
        CurrentRouteTime = c.GetLengthOfRoute(CurrentRoute)
        
        logging.debug('StartStation: %s', StartStation)
        logging.debug('Iteration %s of %s' % (i,NumberOfIterations))
        logging.debug('Current Route Time: %s', CurrentRouteTime)
        logging.debug('Current Shortest Time: %s', ShortestRouteTime)
        logging.debug('Current Shortest Route: \n%s', ShortestRoute)
        
        # Update the performance metrics
        NearestTimeBucket = int(round(CurrentRouteTime/10.0) * 10.0)
        TimesHistogram[NearestTimeBucket] = TimesHistogram[NearestTimeBucket] + 1
        
        # Update the shortest route if it's quicker
        if CurrentRouteTime < ShortestRouteTime:
            if len(list(set(CurrentRoute))) >= r.TOTAL_NUMBER_OF_STATIONS: # Check that the tour visits all stations
                
                d.InsertShortestRouteIntoDatabase(ShortestRoute,ShortestRouteTime)
                
                ShortestRoute = CurrentRoute
                ShortestRouteTime = CurrentRouteTime
                
            else:
                logging.error('Route created with too few stations')
                logging.error('Number of stations: %s',len(list(set(CurrentRoute))))
  
        i = i+1

except Exception, e:
    
    logging.error('%s generated error in operation', FN_NAME)
    logging.exception('Traceback message: \n%s',e)
    logging.error('%s: Failed on iteration %s of %s' % (FN_NAME,i,NumberOfIterations))
    logging.error('%s: StartStation: %s' % (FN_NAME,StartStation))

finally:
    # Update the summary stats database
    d.InsertHistogramIntoDatabase(TimesHistogram)
    
    logging.debug('%s: ShortestRoute: %s' %(FN_NAME,ShortestRoute))
    logging.info('ShortestRouteTime: %s', ShortestRouteTime)
    logging.info('%s: Number of iterations: %s' %(FN_NAME,i-1))
    
    logging.debug('PerformanceHistogram: \n%s',TimesHistogram)
    
    logging.info('%s - END', FN_NAME)
    print "End"