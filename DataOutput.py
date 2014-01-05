''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      28 December 2013

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Outputs the routes created in readable formats

#######################################################################################################
'''

import Reference as r
from RouteCalculation import StationsOnTheSameLine

TestRoute =  [' HEATHROW 5', 'HEATHROW 123', 'HATTON CROSS', 'HEATHROW TERMINAL FOUR', 'HEATHROW TERMINAL FOUR', 'HEATHROW 123', 'HATTON CROSS', 'HOUNSLOW WEST', 'HOUNSLOW CENTRAL', 
                      'HOUNSLOW EAST', 'OSTERLEY', 'BOSTON MANOR', 'NORTHFIELDS', 'SOUTH EALING', 'ACTON TOWN', 'CHISWICK PARK', 'TURNHAM GREEN', 'GUNNERSBURY', 'KEW GARDENS', 
                      
                      'RICHMOND', 'RICHMOND', 'KEW GARDENS', 'GUNNERSBURY', 'TURNHAM GREEN', 'STAMFORD BROOK', 'RAVENSCOURT PARK', 'HAMMERSMITH', 'GOLDHAWK ROAD', 'SHEPHERDS BUSH MARKET',
                      'WOOD LANE', 'LATIMER ROAD', 'LADBROKE GROVE', 'WESTBOURNE PARK', 'ROYAL OAK', 'PADDINGTON', 'BAYSWATER', 'NOTTING HILL GATE', 'HIGH STREET KENSINGTON', 
                       
                      'GLOUCESTER ROAD', 'EARLS COURT', 'WEST BROMPTON', 'FULHAM BROADWAY', 'PARSONS GREEN', 'PUTNEY BRIDGE', 'EAST PUTNEY', 'SOUTHFIELDS', 'WIMBLEDON PARK', 'WIMBLEDON', 
                      'SOUTH WIMBLEDON', 'COLLIERS WOOD', 'TOOTING BROADWAY', 'TOOTING BEC', 'BALHAM', 'CLAPHAM SOUTH', 'CLAPHAM COMMON', 'CLAPHAM NORTH', 'STOCKWELL', 'OVAL', 'KENNINGTON',
                        
                      'ELEPHANT & CASTLE', 'BOROUGH', 'LONDON BRIDGE', 'BANK', 'MOORGATE', 'LIVERPOOL STREET', 'ALDGATE EAST', 'WHITECHAPEL', 'STEPNEY GREEN', 'MILE END', 'BOW ROAD',
                      'BROMLEY BY BOW', 'WEST HAM', 'PLAISTOW', 'UPTON PARK', 'EAST HAM', 'BARKING', 'UPNEY', 'BECONTREE', 'DAGENHAM HEATHWAY', 'DAGENHAM EAST', 'ELM PARK', 'HORNCHURCH', 
                        
                      'UPMINSTER BRIDGE', 'UPMINSTER', 'UPMINSTER', 'UPMINSTER BRIDGE', 'HORNCHURCH', 'ELM PARK', 'DAGENHAM EAST', 'DAGENHAM HEATHWAY', 'BECONTREE', 'UPNEY', 'BARKING',
                      'EAST HAM', 'UPTON PARK', 'PLAISTOW', 'WEST HAM', 'CANNING TOWN', 'NORTH GREENWICH', 'CANARY WHARF', 'CANADA WATER', 'BERMONDSEY', 'LONDON BRIDGE', 'SOUTHWARK', 
                         
                      'WATERLOO', 'WESTMINSTER', 'EMBANKMENT', 'TEMPLE', 'BLACKFRIARS', 'MANSION HOUSE', 'CANNON STREET', 'MONUMENT', 'TOWER HILL', 'ALDGATE', 'ALDGATE', 'LIVERPOOL STREET', 
                      'BETHNAL GREEN', 'BETHNAL GREEN', 'LIVERPOOL STREET', 'MOORGATE', 'BARBICAN', 'FARRINGDON', 'KINGS CROSS ST PANCRAS', 'EUSTON SQUARE', 'GREAT PORTLAND STREET', 
                      
                      'BAKER STREET ', 'EDGWARE ROAD', 'MARYLEBONE', 'BAKER STREET', 'REGENTS PARK', 'OXFORD CIRCUS', 'PICCADILLY CIRCUS', 'CHARING CROSS', 'LEICESTER SQUARE', 
                      'TOTTENHAM COURT ROAD', 'GOODGE STREET', 'WARREN STREET', 'EUSTON', 'MORNINGTON CRESCENT', 'CAMDEN TOWN', 'CHALK FARM', 'BELSIZE PARK', 'HAMPSTEAD', 'GOLDERS GREEN', 
                      
                      'BRENT CROSS', 'HENDON CENTRAL', 'COLINDALE', 'BURNT OAK', 'EDGWARE', 'CANONS PARK', 'STANMORE', 'STANMORE', 'CANONS PARK', 'QUEENSBURY', 'KINGSBURY', 'WEMBLEY PARK', 
                      'NEASDEN', 'DOLLIS HILL', 'WILLESDEN GREEN', 'KILBURN', 'WEST HAMPSTEAD', 'FINCHLEY ROAD', 'SWISS COTTAGE', 'ST JOHNS WOOD', 'ST JOHNS WOOD', 'BAKER STREET', 'BOND STREET', 
                      
                      'MARBLE ARCH', 'LANCASTER GATE', 'QUEENSWAY', 'QUEENSWAY', 'LANCASTER GATE', 'MARBLE ARCH', 'BOND STREET', 'GREEN PARK', 'VICTORIA', 'PIMLICO', 'VAUXHALL', 'STOCKWELL', 
                      'BRIXTON', 'BRIXTON', 'STOCKWELL', 'OVAL', 'KENNINGTON', 'ELEPHANT & CASTLE', 'LAMBETH NORTH', 'LAMBETH NORTH', 'WATERLOO', 'WESTMINSTER', 'ST JAMES PARK', 'ST JAMES PARK', 
                      
                      'VICTORIA', 'GREEN PARK', 'HYDE PARK CORNER', 'KNIGHTSBRIDGE', 'SOUTH KENSINGTON', 'SLOANE SQUARE', 'SLOANE SQUARE', 'VICTORIA', 'GREEN PARK', 'PICCADILLY CIRCUS', 
                      'LEICESTER SQUARE', 'COVENT GARDEN', 'HOLBORN', 'RUSSELL SQUARE', 'RUSSELL SQUARE', 'KINGS CROSS ST PANCRAS', 'HIGHBURY', 'FINSBURY PARK', 'SEVEN SISTERS', 'TOTTENHAM HALE', 
                      
                      'BLACKHORSE ROAD', 'WALTHAMSTOW', 'LEYTONSTONE', 'WANSTEAD', 'REDBRIDGE', 'GANTS HILL', 'NEWBURY PARK', 'BARKINGSIDE', 'FAIRLOP', 'HAINAULT', 'GRANGE HILL', 'CHIGWELL', 
                      'RODING VALLEY', 'WOODFORD', 'SOUTH WOODFORD', 'SNARESBROOK', 'SNARESBROOK', 'SOUTH WOODFORD', 'WOODFORD', 'BUCKHURST HILL', 'LOUGHTON', 'DEBDEN', 'THEYDON BOIS', 'EPPING', 
                      
                      'EPPING', 'THEYDON BOIS', 'DEBDEN', 'LOUGHTON', 'BUCKHURST HILL', 'WOODFORD', 'SOUTH WOODFORD', 'SNARESBROOK', 'LEYTONSTONE', 'LEYTON', 'STRATFORD', 'MILE END', 
                      'BETHNAL GREEN', 'LIVERPOOL STREET', 'MOORGATE', 'OLD STREET', 'ANGEL', 'ANGEL', 'KINGS CROSS ST PANCRAS', 'RUSSELL SQUARE', 'HOLBORN', 'CHANCERY LANE', 'ST PAULS', 
                      
                      'ST PAULS', 'CHANCERY LANE', 'HOLBORN', 'RUSSELL SQUARE', 'KINGS CROSS ST PANCRAS', 'CALEDONIAN ROAD', 'HOLLOWAY ROAD', 'ARSENAL', 'ARSENAL', 'FINSBURY PARK', 'MANOR HOUSE', 
                      'TURNPIKE LANE', 'WOOD GREEN', 'BOUNDS GREEN', 'ARNOS GROVE', 'SOUTHGATE', 'OAKWOOD', 'COCKFOSTERS', 'HIGH BARNET', 'TOTTERIDGE & WHETSTONE', 'WOODSIDE PARK', 'WEST FINCHLEY', 
                      
                      'FINCHLEY CENTRAL', 'MILL HILL EAST', 'MILL HILL EAST', 'FINCHLEY CENTRAL', 'EAST FINCHLEY', 'HIGHGATE', 'ARCHWAY', 'TUFNELL PARK', 'KENTISH TOWN', 'KENTISH TOWN', 
                      'CAMDEN TOWN', 'MORNINGTON CRESCENT', 'EUSTON', 'WARREN STREET', 'OXFORD CIRCUS', 'BOND STREET', 'BAKER STREET', 'MARYLEBONE', 'EDGWARE ROAD', 'PADDINGTON', 'WARWICK AVENUE', 
                      
                      'MAIDA VALE', 'KILBURN PARK', 'QUEENS PARK', 'KENSAL GREEN', 'WILLESDEN JUNCTION', 'HARLESDEN', 'STONEBRIDGE PARK', 'WEMBLEY CENTRAL', 'NORTH WEMBLEY', 'SOUTH KENTON', 
                      'KENTON', 'HARROW & WEALDSTONE', 'HARROW & WEALDSTONE', 'KENTON', 'NORTHWICK PARK', 'PRESTON ROAD', 'PRESTON ROAD', 'NORTHWICK PARK', 'HARROW-ON-THE-HILL', 'WEST HARROW', 
                      
                      'RAYNERS LANE', 'EASTCOTE', 'RUISLIP MANOR', 'RUISLIP', 'ICKENHAM', 'HILLINGDON', 'UXBRIDGE', 'UXBRIDGE', 'HILLINGDON', 'ICKENHAM', 'WEST RUISLIP', 'RUISLIP GARDENS', 
                      'SOUTH RUISLIP', 'NORTHOLT', 'GREENFORD', 'PERIVALE', 'HANGER LANE', 'NORTH ACTON', 'EAST ACTON', 'WHITE CITY', 'SHEPHERDS BUSH', 'HOLLAND PARK', 'HOLLAND PARK', 
                      
                      'SHEPHERDS BUSH', 'KENSINGTON (OLYMPIA)', 'KENSINGTON (OLYMPIA)', 'EARLS COURT', 'WEST KENSINGTON', 'BARONS COURT', 'BARONS COURT', 'HAMMERSMITH', 'ACTON TOWN', 
                      'EALING COMMON', 'EALING BROADWAY', 'WEST ACTON', 'NORTH EALING', 'PARK ROYAL', 'ALPERTON', 'SUDBURY TOWN', 'SUDBURY HILL', 'SOUTH HARROW', 'SOUTH HARROW', 
                      
                      'RAYNERS LANE', 'WEST HARROW', 'HARROW-ON-THE-HILL', 'NORTH HARROW', 'PINNER', 'NORTHWOOD HILLS', 'NORTHWOOD', 'MOOR PARK', 'CROXLEY', 'WATFORD', 'WATFORD', 'CROXLEY', 
                      'MOOR PARK', 'RICKMANSWORTH', 'CHORLEYWOOD', 'CHALFONT & LATIMER', 'AMERSHAM', 'AMERSHAM', 'CHALFONT & LATIMER', 'CHESHAM']

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

def PrintRouteInReadableFormat(InputRoute):
    ''' Outputs the route to the console in the form of readable user directions '''
    
    Route = ParseRouteList(InputRoute)
    
    ChangeStation = Route[0]
    CurrentLine = 'Piccadilly'
    
    StationsEnRoute = []
    
    print "Start at " + ChangeStation
    
    for i in range(1,len(Route) - 1):u
        
        # If the next station is on a different line, find a line that joins them
        if not Route[i] in r.LINES_AND_STATIONS[CurrentLine]:
            CurrentLine = FindCommonLine(Route[i-1], Route[i])
        
        # Pass over any intermediary stations unless they are at the end of the line
        if Route[i+1] in r.LINES_AND_STATIONS[CurrentLine] and not Route[i] in r.NODES_SINGLE:
            StationsEnRoute.append(Route[i])
        
        # Otherwise, output to the console
        else:
    
            if StationsEnRoute == []:                    
                print "Go to " + Route[i] + " on the " + CurrentLine.upper() + " Line"
                
            else:
                print "Go to " + Route[i] + " on the " + CurrentLine.upper() + " Line via " + str(StationsEnRoute)
            
            StationsEnRoute = [] # Clear the en route stations for the next iteration

    print "Finish at " + Route[-1]
    
#PrintRouteInReadableFormat(TestRoute)


