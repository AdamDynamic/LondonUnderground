''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      11 January 2014

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Given a generated route, contains functions designed to optimise the route

#######################################################################################################
'''

import logging

import Reference as r

def ParseListForDuplicates(InputRoute):
    ''' Parses the route to remove duplicates '''
    
    FN_NAME = 'ParseListForDuplicates'
    
    OutputRoute = []
    TotalStations = r.STATIONS_COMPLETE[:]
    
    try:
        if InputRoute:
            OutputRoute.append(InputRoute[0])
            TotalStations = [Station for Station in TotalStations if Station != InputRoute[0] ] 
            
            # Continue while there are stations that remain unvisited
            while True:
            
                # Remove instances where the same station appears twice in succession
                for i in range(1,len(InputRoute)):
        
                    if not InputRoute[i] == OutputRoute[-1]:
                        
                        OutputRoute.append(InputRoute[i]) 
                        
                        TotalStations = [Station for Station in TotalStations if Station != InputRoute[i] ]  
                        
                        # Once all stations are visited, return the result
                        if len(TotalStations) == 0:
                            
                            return OutputRoute
        else:
            logging.error('%s: No InputRoute passed to function', FN_NAME)

    
    except Exception, e:
        logging.error('%s: Unable to parse list for duplicates', FN_NAME)
        logging.error('%s: InputRoute: \n%s' %(FN_NAME,InputRoute))
        logging.exception('Traceback message: \n%s',e)

