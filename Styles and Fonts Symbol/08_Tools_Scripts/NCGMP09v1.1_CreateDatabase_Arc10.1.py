# ncgmp09v1.1_10.0_CreateDatabase_1.py
#   Python script to create an empty NCGMP09-style
#   ArcGIS 10 geodatabase for geologic map data
#
#   Ralph Haugerud, USGS
#
#   Requires that ncgmp09_definition.py be present in the local directory 
#     or in the appropriate Python library directory.
#
# RUN AS TOOLBOX SCRIPT FROM ArcCatalog OR ArcMap

import arcpy, sys, os
from NCGMP09v11_Definition import tableDict

versionString = 'NCGMP09v1.1_CreateDatabase_Arc10.0.py, version of 4 December 2013'

default = '#'

#cartoReps = False # False if cartographic representations will not be used

transDict =     { 'String': 'TEXT',
			'Single': 'FLOAT',
			'Double': 'DOUBLE',
			'NoNulls':'NON_NULLABLE',
			'NullsOK':'NULLABLE',
			'Date'  : 'DATE'  }

usage = """Usage:
   systemprompt> ncgmp09_create.py <directory> <geodatabaseName> <coordSystem>
                <OptionalElements> <#XSections> <AddEditTracking> <AddRepresentations> <AddLTYPE>
   <directory> is existing directory in which new geodatabaseName is to 
      be created, use # for current directory
   <geodatabaseName> is name of gdb to be created, with extension
      .gdb causes a file geodatabase to be created
      .mdb causes a personal geodatabase to be created
   <coordSystem> is a fully-specified ArcGIS coordinate system
   <OptionalElements> is either # or a semicolon-delimited string specifying
      which non-required elements should be created (e.g.,
      OrientationPoints;CartographicLines;RepurposedSymbols )
   <#XSections> is an integer (0, 1, 2, ...) specifying the intended number of
      cross-sections
   <AddEditTracking> is either true or false (default is true). Parameter is ignored if
      ArcGIS version is less than 10.1
   <AddRepresentations> is either true or false (default is false). If true, add
      fields for Cartographic representions to all feature classes
   <AddLTYPE> is either true or false (default is false). If true, add LTYPE field
      to feature classes ContactsAndFaults and GeologicLines, add PTTYPE field
      to feature class OrientationData, and add PTTYPE field to MapUnitPoints    

  Then, in ArcCatalog:
  * If you use the CorrelationOfMapUnits feature data set, note that you will 
    have to manually create the annotation feature class CMUText and add field 
    ParagraphStyle. (I haven't yet found a way to script the creation of an 
    annotation feature class.)
  * If there will be non-standard point feature classes (photos, mineral 
    occurrences, etc.), copy/paste/rename feature class GenericPoint or 
    GenericSample, as appropriate, rename the _ID field, and add necessary
    fields to the new feature class.
  * Load data, if data already are in GIS form. 
  Edit data as needed.

"""

def addMsgAndPrint(msg, severity=0): 
    # prints msg to screen and adds msg to the geoprocessor (in case this is run as a tool) 
    #print msg 
    try: 
        for string in msg.split('\n'): 
            # Add appropriate geoprocessing message 
            if severity == 0: 
                arcpy.AddMessage(string) 
            elif severity == 1: 
                arcpy.AddWarning(string) 
            elif severity == 2: 
                arcpy.AddError(string) 
    except: 
        pass 

def createFeatureClass(thisDB,featureDataSet,featureClass,shapeType,fieldDefs):
    addMsgAndPrint('    Creating feature class '+featureClass+'...')
    try:
        arcpy.env.workspace = thisDB
        arcpy.CreateFeatureclass_management(featureDataSet,featureClass,shapeType)
        thisFC = thisDB+'/'+featureDataSet+'/'+featureClass
        for fDef in fieldDefs:
            try:
                if fDef[1] == 'String':
                    arcpy.AddField_management(thisFC,fDef[0],transDict[fDef[1]],'#','#',fDef[3],'#',transDict[fDef[2]])
                else:
                    arcpy.AddField_management(thisFC,fDef[0],transDict[fDef[1]],'#','#','#','#',transDict[fDef[2]])
            except:
                addMsgAndPrint('Failed to add field '+fDef[0]+' to feature class '+featureClass)
                addMsgAndPrint(arcpy.GetMessages(2))
    except:
        addMsgAndPrint(arcpy.GetMessages())
        addMsgAndPrint('Failed to create feature class '+featureClass+' in dataset '+featureDataSet)
        
def addTracking(tfc):
    if arcpy.Exists(tfc):
        addMsgAndPrint('    Enabling edit tracking in '+tfc)
        try:
            arcpy.EnableEditorTracking_management(tfc,'created_user','created_date','last_edited_user','last_edited_date','ADD_FIELDS','DATABASE_TIME')
        except:
            addMsgAndPrint(tfc)
            addMsgAndPrint(arcpy.GetMessages(2))                      

def cartoRepsExistAndLayer(fc):
    crPath = os.path.join(os.path.dirname(sys.argv[0]),'CartoRepsAZGS')
    hasReps = False
    repLyr = ''
    for repFc in 'ContactsAndFaults','GeologicLines','OrientationPoints':
        if fc.find(repFc) > -1:
            hasReps = True
            repLyr = os.path.join(crPath,repFc+'.lyr')
    return hasReps,repLyr

def main(thisDB,coordSystem,nCrossSections):
    # create feature dataset GeologicMap
    addMsgAndPrint('  Creating feature dataset GeologicMap...')
    try:
        arcpy.CreateFeatureDataset_management(thisDB,'GeologicMap',coordSystem)
    except:
        addMsgAndPrint(arcpy.GetMessages(2))

    # create feature classes in GeologicMap
    # poly feature classes
    featureClasses = ['MapUnitPolys','DataSourcePolys']
    for fc in ['OtherPolys']:
        if fc in OptionalElements:
            featureClasses.append(fc)
    for featureClass in featureClasses:
        fieldDefs = tableDict[featureClass]
        createFeatureClass(thisDB,'GeologicMap',featureClass,'POLYGON',fieldDefs)
            
    # line feature classes
    featureClasses = ['ContactsAndFaults']
    for fc in ['GeologicLines','CartographicLines','IsoValueLines']:
        if fc in OptionalElements:
            featureClasses.append(fc)
    for featureClass in featureClasses:
        fieldDefs = tableDict[featureClass]
        if featureClass in ['ContactsAndFaults','GeologicLines'] and addLTYPE:
            fieldDefs.append(['LTYPE','String','NullsOK',50])
        createFeatureClass(thisDB,'GeologicMap',featureClass,'POLYLINE',fieldDefs)

    # point feature classes
    featureClasses = []
    for fc in ['OrientationPoints','GeochronPoints','FossilPoints','MapUnitPoints','Stations',
                  'GenericSamples','GenericPoints']:
        if fc in OptionalElements:
            featureClasses.append(fc)
    for featureClass in featureClasses:
        if featureClass == 'MapUnitPoints': 
            fieldDefs = tableDict['MapUnitPolys']
            if addLTYPE:
                fieldDefs.append(['PTYPE','String','NullsOK',50])
        else:	
            fieldDefs = tableDict[featureClass]
            if addLTYPE and featureClass in ['OrientationPoints']:
                fieldDefs.append(['PTTYPE','String','NullsOK',50])
        createFeatureClass(thisDB,'GeologicMap',featureClass,'POINT',fieldDefs)

    # create feature dataset CorrelationOfMapUnits
    if 'CorrelationOfMapUnits' in OptionalElements:
        addMsgAndPrint('  Creating feature dataset CorrelationOfMapUnits...')
        arcpy.CreateFeatureDataset_management(thisDB,'CorrelationOfMapUnits')
        fieldDefs = tableDict['CMUMapUnitPolys']
        createFeatureClass(thisDB,'CorrelationOfMapUnits','CMUMapUnitPolys','POLYGON',fieldDefs)
        fieldDefs = tableDict['CMULines']
        createFeatureClass(thisDB,'CorrelationOfMapUnits','CMULines','POLYLINE',fieldDefs)
        fieldDefs = tableDict['CMUPoints']
        createFeatureClass(thisDB,'CorrelationOfMapUnits','CMUPoints','POINT',fieldDefs)
    
    # create CrossSections
    if nCrossSections > 26:
        nCrossSections = 26
    if nCrossSections < 0:
        nCrossSections = 0
    # note space in position 0
    alphabet = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for n in range(1,nCrossSections+1):
        xsLetter = alphabet[n]
        xsName = 'CrossSection'+xsLetter
        xsN = 'CS'+xsLetter
        #create feature dataset CrossSectionA
        addMsgAndPrint('  Creating feature data set CrossSection'+xsLetter+'...')
        arcpy.CreateFeatureDataset_management(thisDB,xsName)
        fieldDefs = tableDict['MapUnitPolys']
        fieldDefs[0][0] = xsN+'MapUnitPolys_ID'
        createFeatureClass(thisDB,xsName,xsN+'MapUnitPolys','POLYGON',fieldDefs)
        fieldDefs = tableDict['ContactsAndFaults']
        if addLTYPE:
            fieldDefs.append(['LTYPE','String','NullsOK',50])
        fieldDefs[0][0] = xsN+'ContactsAndFaults_ID'
        createFeatureClass(thisDB,xsName,xsN+'ContactsAndFaults','POLYLINE',fieldDefs)
        fieldDefs = tableDict['OrientationPoints']
        if addLTYPE:
            fieldDefs.append(['PTTYPE','String','NullsOK',50]) 
        fieldDefs[0][0] = xsN+'OrientationPoints_ID'
        createFeatureClass(thisDB,xsName,xsN+'OrientationPoints','POINT',fieldDefs)

    # create tables
    tables = ['DescriptionOfMapUnits','DataSources','Glossary']
    for tb in ['RepurposedSymbols','StandardLithology','ExtendedAttributes','GeologicEvents']:
        if tb in OptionalElements:
            tables.append(tb)
    for table in tables:
        addMsgAndPrint('  Creating table '+table+'...')
        try:
            arcpy.CreateTable_management(thisDB,table)
            fieldDefs = tableDict[table]
            for fDef in fieldDefs:
                try:
                    if fDef[1] == 'String':
                        arcpy.AddField_management(thisDB+'/'+table,fDef[0],transDict[fDef[1]],'#','#',fDef[3],'#',transDict[fDef[2]])
                    else:
                        arcpy.AddField_management(thisDB+'/'+table,fDef[0],transDict[fDef[1]],'#','#','#','#',transDict[fDef[2]])
                except:
                    addMsgAndPrint('Failed to add field '+fDef[0]+' to table '+table)
                    addMsgAndPrint(arcpy.GetMessages(2))		    
        except:
            addMsgAndPrint(arcpy.GetMessages())

    # if cartoReps, add cartographic representations to all feature classes
    # trackEdits, add editor tracking to all feature classes and tables
    if cartoReps or trackEdits:
        arcpy.env.workspace = thisDB
        tables = arcpy.ListTables()
        datasets = arcpy.ListDatasets()
        for dataset in datasets:
            addMsgAndPrint('  Dataset '+dataset)
            arcpy.env.workspace = thisDB+'/'+dataset
            fcs = arcpy.ListFeatureClasses()
            for fc in fcs:
                hasReps,repLyr = cartoRepsExistAndLayer(fc)
                if cartoReps and hasReps:
                    addMsgAndPrint('    Adding cartographic representations to '+fc)
                    try:
                        arcpy.AddRepresentation_cartography(fc,fc+'_rep1','RuleID1','Override1',default,repLyr,'NO_ASSIGN')
                        """
                            Note the 1 suffix on the representation name (fc+'_rep1') and the RuleID1 and Override1 fields.
                        If at some later time we wish to add additional representations to a feature class, each will
                        require it's own RuleID and Override fields which may be identified, and tied to the appropriate
                        representation, by suffixes 2, 3, ...
                            Naming representations fc+'_rep'+str(n) should be sufficient to identify each representation in a 
                        geodatabase uniquely, and allow for multiple representations within a single feature class.
                            It appears that ArcGIS provides no means of scripting an inventory of representations within
                        feature class or geodatabase. So, the convenience of establishing a coded-value domain that ties
                        representation rule IDs (consecutive integers) to some sort of useful text identifier becomes a
                        necessity for flagging the presence of a representation: One CAN script the inventory of domains
                        in a geodatabase. Run arcpy.da.ListDomains. Check the result for names of the form
                        <featureClassName>_rep??_Rule and voila, you've got a list of representations (and their associated
                        feature classes) in the geodatabase.
                            Moral: If you add a representation, be sure to add an associated coded-value domain and name
                        it appropriately!
                        """
                    except:
                        addMsgAndPrint(arcpy.GetMessages(2))
                if trackEdits:
                    addTracking(fc)
        if trackEdits:
            addMsgAndPrint('  Tables ')
            arcpy.env.workspace = thisDB
            for aTable in tables:
                addTracking(aTable)

def createDatabase(outputDir,thisDB):
    addMsgAndPrint('  Creating geodatabase '+thisDB+'...')
    if arcpy.Exists(outputDir+'/'+thisDB):
        addMsgAndPrint('  Geodatabase '+thisDB+' already exists.')
        addMsgAndPrint('   forcing exit with error')
        raise arcpy.ExecuteError
    try:
        if thisDB[-4:] == '.mdb':
            arcpy.CreatePersonalGDB_management(outputDir,thisDB)
        if thisDB[-4:] == '.gdb':
            arcpy.CreateFileGDB_management(outputDir,thisDB)
        return True
    except:
        addMsgAndPrint('Failed to create geodatabase '+outputDir+'/'+thisDB)
        addMsgAndPrint(arcpy.GetMessages(2))
        return False

#########################################
    
addMsgAndPrint(versionString)

if len(sys.argv) >= 6:
    addMsgAndPrint('Starting script')

    outputDir = sys.argv[1]
    if outputDir == '#':
        outputDir = os.getcwd()
    outputDir = outputDir.replace('\\','/')

    thisDB = sys.argv[2]
    # test for extension; if not given, default to file geodatabase
    if not thisDB[-4:].lower() in ('.gdb','.mdb'):
        thisDB = thisDB+'.gdb'

    coordSystem = sys.argv[3]

    if sys.argv[4] == '#':
        OptionalElements = []
    else:
        OptionalElements = sys.argv[4].split(';')
    
    nCrossSections = int(sys.argv[5])

    try:
        if sys.argv[6] == 'true':
            trackEdits = True
        else:
            trackEdits = False
    except:
        trackEdits = False
        
    if arcpy.GetInstallInfo()['Version'] < '10.1':
        trackEdits = False
        
    try:
        if sys.argv[7] == 'true':
            cartoReps = True
        else:
            cartoReps = False
    except:
        cartoReps = False

    try:
        if sys.argv[8] == 'true':
            addLTYPE = True
        else:
            addLTYPE = False
    except:
        addLTYPE = False
        
    # create personal gdb in output directory and run main routine
    if createDatabase(outputDir,thisDB):
        thisDB = outputDir+'/'+thisDB
        arcpy.RefreshCatalog(thisDB)
        main(thisDB,coordSystem,nCrossSections)

    # try to write a readme within the .gdb
    if thisDB[-4:] == '.gdb':
        try:
            arcpy.env.workspace = ''
            versionFile = open(thisDB+'/00readme.txt','w')
            versionFile.write('Geodatabase created by '+versionString+'\n')
            versionFile.close()
        except:
            addMsgAndPrint('Failed to write '+thisDB+'/00readme.txt')

else:
    addMsgAndPrint(usage)
