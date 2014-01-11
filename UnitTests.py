''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      28 December 2013

PROJECT:            Tube Challenge Route Creation
DESCRIPTION:        Contains unit tests for the other modules

#######################################################################################################
'''


import Dijkstras
import RouteOptimisation
import DataInputAndParsing
import RouteCalculation

import Reference as r


''' Data Input and Parsing '''

# Test the STATIONS_DISTANCES_PEAK dictionary is complete
assert DataInputAndParsing.GetNodesFromGraph(r.STATIONS_DISTANCES_PEAK) == r.NODES_COMPLETE

# Test that all single nodes are contained in the complete nodes list
for i in r.NODES_SINGLE:
    if not i in r.NODES_COMPLETE:
        raise ValueError(i + " not found in r.NODES_COMPLETE")

# Test the list of lines and stations is complete
assert DataInputAndParsing.CreateListOfLines(r.CSV_FILE_PATH) == r.LINES_AND_STATIONS


''' Dijkstras '''

TEST_STATION_DISTANCES = {'Station1' : {'Station2': 10, 'Station3': 20}, 'Station2': {'Station1': 10, 'Station3': 5},'Station3': {'Station2': 5}}
Distances_ExpectedResult = ['Station1', 'Station2', 'Station3']

Dijkstras_Test = Dijkstras.DijkstraShortestPath(TEST_STATION_DISTANCES, 'Station1', 'Station3')

assert Dijkstras_Test == Distances_ExpectedResult


''' Route Optimisation '''

ROUTE_TEST = ['ACTON TOWN','ACTON TOWN' , 'ALDGATE', 'ALDGATE EAST', 'ALPERTON', 'AMERSHAM', 'ANGEL', 'ARCHWAY', 'ARNOS GROVE', 'ARSENAL', 'BAKER STREET', 'BALHAM', 'BANK', 'BARBICAN', 'BARKING', 'BARKINGSIDE', 'BARONS COURT', 'BAYSWATER', 'BECONTREE', 'BELSIZE PARK', 'BERMONDSEY', 'BETHNAL GREEN', 'BLACKFRIARS', 'BLACKHORSE ROAD', 'BOND STREET', 'BOROUGH', 'BOSTON MANOR', 'BOUNDS GREEN', 'BOW ROAD', 'BRENT CROSS', 'BRIXTON', 'BROMLEY BY BOW', 'BUCKHURST HILL', 'BURNT OAK', 'CALEDONIAN ROAD', 'CAMDEN TOWN', 'CANADA WATER', 'CANARY WHARF', 'CANNING TOWN', 'CANNON STREET', 'CANONS PARK', 'CHALFONT & LATIMER', 'CHALK FARM', 'CHANCERY LANE', 'CHARING CROSS', 'CHESHAM', 'CHIGWELL', 'CHISWICK PARK', 'CHORLEYWOOD', 'CLAPHAM COMMON', 'CLAPHAM NORTH', 'CLAPHAM SOUTH', 'COCKFOSTERS', 'COLINDALE', 'COLLIERS WOOD', 'COVENT GARDEN', 'CROXLEY', 'DAGENHAM EAST', 'DAGENHAM HEATHWAY', 'DEBDEN', 'DOLLIS HILL', 'EALING BROADWAY', 'EALING COMMON', 'EARLS COURT', 'EAST ACTON', 'EAST FINCHLEY', 'EAST HAM', 'EAST PUTNEY', 'EASTCOTE', 'EDGWARE', 'EDGWARE ROAD', 'ELEPHANT & CASTLE', 'ELM PARK', 'EMBANKMENT', 'EPPING', 'EUSTON', 'EUSTON SQUARE', 'FAIRLOP', 'FARRINGDON', 'FINCHLEY CENTRAL', 'FINCHLEY ROAD', 'FINSBURY PARK', 'FULHAM BROADWAY', 'GANTS HILL', 'GLOUCESTER ROAD', 'GOLDERS GREEN', 'GOLDHAWK ROAD', 'GOODGE STREET', 'GRANGE HILL', 'GREAT PORTLAND STREET', 'GREEN PARK', 'GREENFORD', 'GUNNERSBURY', 'HAINAULT', 'HAMMERSMITH', 'HAMPSTEAD', 'HANGER LANE', 'HARLESDEN', 'HARROW & WEALDSTONE', 'HARROW-ON-THE-HILL', 'HATTON CROSS', 'HEATHROW 123', 'HEATHROW 5', 'HEATHROW TERMINAL FOUR', 'HENDON CENTRAL', 'HIGH BARNET', 'HIGH STREET KENSINGTON', 'HIGHBURY', 'HIGHGATE', 'HILLINGDON', 'HOLBORN', 'HOLLAND PARK', 'HOLLOWAY ROAD', 'HORNCHURCH', 'HOUNSLOW CENTRAL', 'HOUNSLOW EAST', 'HOUNSLOW WEST', 'HYDE PARK CORNER', 'ICKENHAM', 'KENNINGTON', 'KENSAL GREEN', 'KENSINGTON (OLYMPIA)', 'KENTISH TOWN', 'KENTON', 'KEW GARDENS', 'KILBURN', 'KILBURN PARK', 'KINGS CROSS ST PANCRAS', 'KINGSBURY', 'KNIGHTSBRIDGE', 'LADBROKE GROVE', 'LAMBETH NORTH', 'LANCASTER GATE', 'LATIMER ROAD', 'LEICESTER SQUARE', 'LEYTON', 'LEYTONSTONE', 'LIVERPOOL STREET', 'LONDON BRIDGE', 'LOUGHTON', 'MAIDA VALE', 'MANOR HOUSE', 'MANSION HOUSE', 'MARBLE ARCH', 'MARYLEBONE', 'MILE END', 'MILL HILL EAST', 'MONUMENT', 'MOOR PARK', 'MOORGATE', 'MORDEN', 'MORNINGTON CRESCENT', 'NEASDEN', 'NEWBURY PARK', 'NORTH ACTON', 'NORTH EALING', 'NORTH GREENWICH', 'NORTH HARROW', 'NORTH WEMBLEY', 'NORTHFIELDS', 'NORTHOLT', 'NORTHWICK PARK', 'NORTHWOOD', 'NORTHWOOD HILLS', 'NOTTING HILL GATE', 'OAKWOOD', 'OLD STREET', 'OSTERLEY', 'OVAL', 'OXFORD CIRCUS', 'PADDINGTON', 'PARK ROYAL', 'PARSONS GREEN', 'PERIVALE', 'PICCADILLY CIRCUS', 'PIMLICO', 'PINNER', 'PLAISTOW', 'PRESTON ROAD', 'PUTNEY BRIDGE', 'QUEENS PARK', 'QUEENSBURY', 'QUEENSWAY', 'RAVENSCOURT PARK', 'RAYNERS LANE', 'REDBRIDGE', 'REGENTS PARK', 'RICHMOND', 'RICKMANSWORTH', 'RODING VALLEY', 'ROYAL OAK', 'RUISLIP', 'RUISLIP GARDENS', 'RUISLIP MANOR', 'RUSSELL SQUARE', 'SEVEN SISTERS', 'SHEPHERDS BUSH', 'SHEPHERDS BUSH MARKET', 'SLOANE SQUARE', 'SNARESBROOK', 'SOUTH EALING', 'SOUTH HARROW', 'SOUTH KENSINGTON', 'SOUTH KENTON', 'SOUTH RUISLIP', 'SOUTH WIMBLEDON', 'SOUTH WOODFORD', 'SOUTHFIELDS', 'SOUTHGATE', 'SOUTHWARK', 'ST JAMES PARK', 'ST JOHNS WOOD', 'ST PAULS', 'STAMFORD BROOK', 'STANMORE', 'STEPNEY GREEN', 'STOCKWELL', 'STONEBRIDGE PARK', 'STRATFORD', 'SUDBURY HILL', 'SUDBURY TOWN', 'SWISS COTTAGE', 'TEMPLE', 'THEYDON BOIS', 'TOOTING BEC', 'TOOTING BROADWAY', 'TOTTENHAM COURT ROAD', 'TOTTENHAM HALE', 'TOTTERIDGE & WHETSTONE', 'TOWER HILL', 'TUFNELL PARK', 'TURNHAM GREEN', 'TURNPIKE LANE', 'UPMINSTER', 'UPMINSTER BRIDGE', 'UPNEY', 'UPTON PARK', 'UXBRIDGE', 'VAUXHALL', 'VICTORIA', 'WALTHAMSTOW', 'WANSTEAD', 'WARREN STREET', 'WARWICK AVENUE', 'WATERLOO', 'WATFORD', 'WEMBLEY CENTRAL', 'WEMBLEY PARK', 'WEST ACTON', 'WEST BROMPTON', 'WEST FINCHLEY', 'WEST HAM', 'WEST HAMPSTEAD', 'WEST HARROW', 'WEST KENSINGTON', 'WEST RUISLIP', 'WESTBOURNE PARK', 'WESTMINSTER', 'WHITE CITY', 'WHITECHAPEL', 'WILLESDEN GREEN', 'WILLESDEN JUNCTION', 'WIMBLEDON', 'WIMBLEDON PARK', 'WOOD GREEN', 'WOOD LANE', 'WOODFORD', 'WOODSIDE PARK','WOODSIDE PARK', 'WOODFORD', 'WOOD LANE']
Optimisation_Route_ExpectedResult = ['ACTON TOWN', 'ALDGATE', 'ALDGATE EAST', 'ALPERTON', 'AMERSHAM', 'ANGEL', 'ARCHWAY', 'ARNOS GROVE', 'ARSENAL', 'BAKER STREET', 'BALHAM', 'BANK', 'BARBICAN', 'BARKING', 'BARKINGSIDE', 'BARONS COURT', 'BAYSWATER', 'BECONTREE', 'BELSIZE PARK', 'BERMONDSEY', 'BETHNAL GREEN', 'BLACKFRIARS', 'BLACKHORSE ROAD', 'BOND STREET', 'BOROUGH', 'BOSTON MANOR', 'BOUNDS GREEN', 'BOW ROAD', 'BRENT CROSS', 'BRIXTON', 'BROMLEY BY BOW', 'BUCKHURST HILL', 'BURNT OAK', 'CALEDONIAN ROAD', 'CAMDEN TOWN', 'CANADA WATER', 'CANARY WHARF', 'CANNING TOWN', 'CANNON STREET', 'CANONS PARK', 'CHALFONT & LATIMER', 'CHALK FARM', 'CHANCERY LANE', 'CHARING CROSS', 'CHESHAM', 'CHIGWELL', 'CHISWICK PARK', 'CHORLEYWOOD', 'CLAPHAM COMMON', 'CLAPHAM NORTH', 'CLAPHAM SOUTH', 'COCKFOSTERS', 'COLINDALE', 'COLLIERS WOOD', 'COVENT GARDEN', 'CROXLEY', 'DAGENHAM EAST', 'DAGENHAM HEATHWAY', 'DEBDEN', 'DOLLIS HILL', 'EALING BROADWAY', 'EALING COMMON', 'EARLS COURT', 'EAST ACTON', 'EAST FINCHLEY', 'EAST HAM', 'EAST PUTNEY', 'EASTCOTE', 'EDGWARE', 'EDGWARE ROAD', 'ELEPHANT & CASTLE', 'ELM PARK', 'EMBANKMENT', 'EPPING', 'EUSTON', 'EUSTON SQUARE', 'FAIRLOP', 'FARRINGDON', 'FINCHLEY CENTRAL', 'FINCHLEY ROAD', 'FINSBURY PARK', 'FULHAM BROADWAY', 'GANTS HILL', 'GLOUCESTER ROAD', 'GOLDERS GREEN', 'GOLDHAWK ROAD', 'GOODGE STREET', 'GRANGE HILL', 'GREAT PORTLAND STREET', 'GREEN PARK', 'GREENFORD', 'GUNNERSBURY', 'HAINAULT', 'HAMMERSMITH', 'HAMPSTEAD', 'HANGER LANE', 'HARLESDEN', 'HARROW & WEALDSTONE', 'HARROW-ON-THE-HILL', 'HATTON CROSS', 'HEATHROW 123', 'HEATHROW 5', 'HEATHROW TERMINAL FOUR', 'HENDON CENTRAL', 'HIGH BARNET', 'HIGH STREET KENSINGTON', 'HIGHBURY', 'HIGHGATE', 'HILLINGDON', 'HOLBORN', 'HOLLAND PARK', 'HOLLOWAY ROAD', 'HORNCHURCH', 'HOUNSLOW CENTRAL', 'HOUNSLOW EAST', 'HOUNSLOW WEST', 'HYDE PARK CORNER', 'ICKENHAM', 'KENNINGTON', 'KENSAL GREEN', 'KENSINGTON (OLYMPIA)', 'KENTISH TOWN', 'KENTON', 'KEW GARDENS', 'KILBURN', 'KILBURN PARK', 'KINGS CROSS ST PANCRAS', 'KINGSBURY', 'KNIGHTSBRIDGE', 'LADBROKE GROVE', 'LAMBETH NORTH', 'LANCASTER GATE', 'LATIMER ROAD', 'LEICESTER SQUARE', 'LEYTON', 'LEYTONSTONE', 'LIVERPOOL STREET', 'LONDON BRIDGE', 'LOUGHTON', 'MAIDA VALE', 'MANOR HOUSE', 'MANSION HOUSE', 'MARBLE ARCH', 'MARYLEBONE', 'MILE END', 'MILL HILL EAST', 'MONUMENT', 'MOOR PARK', 'MOORGATE', 'MORDEN', 'MORNINGTON CRESCENT', 'NEASDEN', 'NEWBURY PARK', 'NORTH ACTON', 'NORTH EALING', 'NORTH GREENWICH', 'NORTH HARROW', 'NORTH WEMBLEY', 'NORTHFIELDS', 'NORTHOLT', 'NORTHWICK PARK', 'NORTHWOOD', 'NORTHWOOD HILLS', 'NOTTING HILL GATE', 'OAKWOOD', 'OLD STREET', 'OSTERLEY', 'OVAL', 'OXFORD CIRCUS', 'PADDINGTON', 'PARK ROYAL', 'PARSONS GREEN', 'PERIVALE', 'PICCADILLY CIRCUS', 'PIMLICO', 'PINNER', 'PLAISTOW', 'PRESTON ROAD', 'PUTNEY BRIDGE', 'QUEENS PARK', 'QUEENSBURY', 'QUEENSWAY', 'RAVENSCOURT PARK', 'RAYNERS LANE', 'REDBRIDGE', 'REGENTS PARK', 'RICHMOND', 'RICKMANSWORTH', 'RODING VALLEY', 'ROYAL OAK', 'RUISLIP', 'RUISLIP GARDENS', 'RUISLIP MANOR', 'RUSSELL SQUARE', 'SEVEN SISTERS', 'SHEPHERDS BUSH', 'SHEPHERDS BUSH MARKET', 'SLOANE SQUARE', 'SNARESBROOK', 'SOUTH EALING', 'SOUTH HARROW', 'SOUTH KENSINGTON', 'SOUTH KENTON', 'SOUTH RUISLIP', 'SOUTH WIMBLEDON', 'SOUTH WOODFORD', 'SOUTHFIELDS', 'SOUTHGATE', 'SOUTHWARK', 'ST JAMES PARK', 'ST JOHNS WOOD', 'ST PAULS', 'STAMFORD BROOK', 'STANMORE', 'STEPNEY GREEN', 'STOCKWELL', 'STONEBRIDGE PARK', 'STRATFORD', 'SUDBURY HILL', 'SUDBURY TOWN', 'SWISS COTTAGE', 'TEMPLE', 'THEYDON BOIS', 'TOOTING BEC', 'TOOTING BROADWAY', 'TOTTENHAM COURT ROAD', 'TOTTENHAM HALE', 'TOTTERIDGE & WHETSTONE', 'TOWER HILL', 'TUFNELL PARK', 'TURNHAM GREEN', 'TURNPIKE LANE', 'UPMINSTER', 'UPMINSTER BRIDGE', 'UPNEY', 'UPTON PARK', 'UXBRIDGE', 'VAUXHALL', 'VICTORIA', 'WALTHAMSTOW', 'WANSTEAD', 'WARREN STREET', 'WARWICK AVENUE', 'WATERLOO', 'WATFORD', 'WEMBLEY CENTRAL', 'WEMBLEY PARK', 'WEST ACTON', 'WEST BROMPTON', 'WEST FINCHLEY', 'WEST HAM', 'WEST HAMPSTEAD', 'WEST HARROW', 'WEST KENSINGTON', 'WEST RUISLIP', 'WESTBOURNE PARK', 'WESTMINSTER', 'WHITE CITY', 'WHITECHAPEL', 'WILLESDEN GREEN', 'WILLESDEN JUNCTION', 'WIMBLEDON', 'WIMBLEDON PARK', 'WOOD GREEN', 'WOOD LANE', 'WOODFORD', 'WOODSIDE PARK']

RouteOptimisation_Test = RouteOptimisation.ParseListForDuplicates(ROUTE_TEST)

assert RouteOptimisation_Test == Optimisation_Route_ExpectedResult


''' Route Calculation '''

Weighting_Dict_Test = RouteCalculation.CreateWeightedDict({'Station1': 5.0, 'Station2': 6.0, 'Station3': 7.0})
Weighting_Dict_ExpectedResult = {'Station1': 100000.0, 'Station2': 79.04903231199668, 'Station3': 0.06248749509463097} ### Relies on the exponential factor being 50

for i in Weighting_Dict_Test.keys():
    if abs((Weighting_Dict_Test[i]) - (Weighting_Dict_ExpectedResult[i]))>0.01:
        raise ValueError("Weighted_Dict result not equal to expected result")

Route_Length_Test = RouteCalculation.GetLengthOfRoute(ROUTE_TEST)
Route_Length_ExpectedResult = 9131.756

assert abs(Route_Length_Test - Route_Length_ExpectedResult) < 0.0001

# Only return if not broken by assert statement
print "All unit tests passed successfully"
