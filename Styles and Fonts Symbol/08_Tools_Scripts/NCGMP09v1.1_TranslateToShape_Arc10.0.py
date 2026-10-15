#  ncgmp09_TranslateToShape.py
#
#  Converts an NCGMP09-style ArcGIS geodatabase to 
#    open file format
#    	 shape files, .dbf files, and pipe-delimited text files,
#    	 without loss of information.  Field renaming is documented in 
#    	 output file logfile.txt
#    simple shapefile format
#      basic map information in flat shapefiles, with much repetition 
#      of attribute information, long fields truncated, and much 
#      information lost. Field renaming is documented in output 
#	 file logfile.txt
#
#  Ralph Haugerud, USGS, Seattle
#    rhaugerud@usgs.gov

print '  importing arcpy...'
import arcpy, sys, os, glob, time
from NCGMP09v11_utilityFunctions import *

versionString = 'NCGMP09v1.1_TranslateToShape_Arc10.0.py, version of 27 February 2012'

debug = False

# equivalentFraction is used to rank ProportionTerms from most 
#  abundant to least
equivalentFraction =   {'all':1.0,
			'only part':1.0,
			'dominant':0.6,
			'major':0.5,
			'significant':0.4,
			'subordinate':0.3,
			'minor':0.25,
			'trace':0.05,
			'rare':0.02,
			'variable':0.01,
			'present':0.0}

def usage():
	addMsgAndPrint( """
USAGE: ncgmp09_TranslateToShp.py  <geodatabase> <outputWorkspace>

  where <geodatabase> must be an existing ArcGIS geodatabase.
  <geodatabase> may be a personal or file geodatabase, and the 
  .gdb or .mdb extension must be included.
  Output is written to directories <geodatabase (no extension)>-simple
  and <geodatabase (no extension)>-open in <outputWorkspace>. Output 
  directories, if they already exist, will be overwritten.
""")

def remapFieldName(name):
    name2 = name.replace('And','')
    name2 = name2.replace('Of','')
    name2 = name2.replace('Unit','Un')
    name2 = name2.replace('Source','Src')
    name2 = name2.replace('Shape','Shp')
    name2 = name2.replace('Hierarchy','H')
    name2 = name2.replace('Description','Descript')
    name2 = name2.replace('AreaFill','')
    name2 = name2.replace('Structure','Struct')
    name2 = name2.replace('STRUCTURE','STRUCT')
    name2 = name2.replace('user','Usr')
    name2 = name2.replace('created_','Cre')
    name2 = name2.replace('edited_','Ed')
    name2 = name2.replace('date','Dt')
    name2 = name2.replace('last_','Lst')

    newName = ''
    for i in range(0,len(name2)):
        if name2[i] == name2[i].upper():
            newName = newName + name2[i]
            j = 1
        else:
            j = j+1
            if j < 4:
                newName = newName + name2[i]
    if len(newName) > 10:
        if newName[1:3] == newName[1:3].lower():
            newName = newName[0]+newName[3:]
    if len(newName) > 10:
        if newName[3:5] == newName[3:5].lower():
            newName = newName[0:2]+newName[5:]
    if len(newName) > 10:
        addMsgAndPrint('      '+ name + '  ' + newName)
    return newName	

def dumpTable(fc,outName,isSpatial,outputDir,logfile,isOpen,fcName):
    dumpString = '  Dumping '+outName+'...'
    if isSpatial: dumpString = '  '+dumpString
    addMsgAndPrint(dumpString)
    if isSpatial:
        logfile.write('  feature class '+fc+' dumped to shapefile '+outName+'\n')
    else:
        logfile.write('  table '+fc+' dumped to table '+outName+'\n')
    logfile.write('    field name remapping: \n')
    # describe
    fields = arcpy.ListFields(fc)
    longFields = []
    shortFieldName = {}
    for field in fields:
        # translate field names
        #  NEED TO FIX TO DEAL WITH DescriptionOfMapUnits_ and DataSources_
        fName = field.name
        for prefix in ('DescriptionOfMapUnits','DataSources'):
            if fc <> prefix and fName.find(prefix) == 0:
                fName = fName[len(prefix)+1:]
        if len(fName) > 10:
            shortFieldName[field.name] = remapFieldName(fName)
            # write field name translation to logfile
            logfile.write('      '+field.name+' > '+shortFieldName[field.name]+'\n')
        else:
            shortFieldName[field.name] = fName
        if field.length > 254:
            longFields.append(str(field.name))
    # setup field mappings
    fms = arcpy.CreateObject("FieldMappings")
    # and add the table to generate a field map object for each field
    fms.addTable(fc)
    i = 0
    while i < fms.fieldCount:
        # one fieldmap object per field
        fm = fms.getFieldMap(i)
        # get a copy of the field object
        fldout = fm.outputField
        ##addMsgAndPrint(fldout.name+'  output = '+fldout.Type)
        # set the name for the output field through the lookup dictionary
        fldout.name = shortFieldName[fm.getInputFieldName(0)]
        ## fix a bug in ArcGIS
        if fldout.type == 'Integer':
            fldout.type = 'Long'
        # re-apply the fields to the fieldmap object
        fm.outputfield = fldout
        # and replace the existing field map at index i with the updated one.
        if fldout.type == 'String' and fm.getInputFieldName(0) in longFields:
            fm.setStartTextPosition(0,0)
            fm.setEndTextPosition(0,253)
        fms.replaceFieldMap(i, fm)
        i = i + 1
    # export to shapefile (named prefix+name)
    if isSpatial:
        if debug:  print 'dumping ',fc,outputDir,outName
        try:
            arcpy.FeatureClassToFeatureClass_conversion(fc,outputDir,outName,'#',fms)
        except:
            #addMsgAndPrint(arcpy.GetMessages())
            addMsgAndPrint('failed to translate table '+fc)
    else:
        arcpy.TableToTable_conversion(fc,outputDir,outName,'#',fms)
    addMsgAndPrint('    Finished dump')
    # if any field lengths > 255, write csv file of _IDs and long fields
    ## get name of _ID field
    fields = arcpy.ListFields(fc)
    fName = ''
    for field in fields:
        if field.name.find(fc+'_ID') > -1:
            fName = field.name
    # if no _ID field, substitute OBJECTID
    if fName == '':
        for field in fields:
            if field.name.find('OBJECTID') > -1:
                fName = field.name
    if len(longFields) > 0 and isOpen:
        addMsgAndPrint('    Writing CSV file')
        csvFile = open(outputDir+'/'+outName[0:-4]+'.txt','w')
        csvFile.write(fName)
        for field in longFields:
                csvFile.write(','+field)
        csvFile.write('\n')
        rows = arcpy.SearchCursor(fc)
        row = rows.next()
        while row:
            # sometimes field names are qualified (tablename.fieldname) and sometimes
            # they are not (fieldname). Setting arcpy.QualifiedNames = True (or False)
            # doesn't seem to work, so try both forms.
            rowString = str(row.getValue(fName))
            for field in longFields:
                if row.getValue(field) <> None:
                        rowString = rowString+'|'+row.getValue(field)
                else:
                        rowString = rowString+'|'
            try:
                csvFile.write(rowString+'\n')	
            except:
                rStr = ''
                for i in range(len(rowString)):
                    if ord(rowString[i]) < 128:
                        rStr = rStr + rowString[i]
                    else: 
                        rStr = rStr + '<chr('+str(ord(rowString[i]))+')>'
                csvFile.write(rStr+'\n')
            row = rows.next()
        del row, rows
        csvFile.close()

def makeOutputDir(gdb,outWS,isOpen):
    outputDir = outWS+'/'+os.path.basename(gdb)[0:-4]
    if isOpen:
        outputDir = outputDir+'-open'
    else:
        outputDir = outputDir+'-simple'
    addMsgAndPrint('  Making '+outputDir+'/...')
    if os.path.exists(outputDir):
        if os.path.exists(outputDir+'/info'):
            for fl in glob.glob(outputDir+'/info/*'):
                os.remove(fl)
            os.rmdir(outputDir+'/info')
        for fl in glob.glob(outputDir+'/*'):
            os.remove(fl)
        os.rmdir(outputDir)
    os.mkdir(outputDir)
    logfile = open(outputDir+'/logfile.txt','w')
    logfile.write('file written by '+versionString+'\n\n')
    return outputDir, logfile

def dummyVal(pTerm,pVal):
    if pVal == None:
        if pTerm in equivalentFraction:
            return equivalentFraction[pTerm]
        else:
            return 0.0
    else:
        return pVal

def description(unitDesc):
    unitDesc.sort()
    unitDesc.reverse()
    desc = ''
    for uD in unitDesc:
        if uD[3] == '': desc = desc+str(uD[4])+':'
        else:  desc = desc+uD[3]+':'
        desc = desc+uD[2]+'; '
    return desc[:-2]

def makeStdLithDict():
    addMsgAndPrint('  Making StdLith dictionary...')
    stdLithDict = {}
    rows = arcpy.searchcursor('StandardLithology',"","","","MapUnit")
    row = rows.next()
    unit = row.getValue('MapUnit')
    unitDesc = []
    pTerm = row.getValue('ProportionTerm'); pVal = row.getValue('ProportionValue')
    val = dummyVal(pTerm,pVal)
    unitDesc.append([val,row.getValue('PartType'),row.getValue('Lithology'),pTerm,pVal])
    while row:
        #print row.getValue('MapUnit')+'  '+row.getValue('Lithology')
        newUnit = row.getValue('MapUnit')
        if newUnit <> unit:
            stdLithDict[unit] = description(unitDesc)
            unitDesc = []
            unit = newUnit
        pTerm = row.getValue('ProportionTerm'); pVal = row.getValue('ProportionValue')
        val = dummyVal(pTerm,pVal)
        unitDesc.append([val,row.getValue('PartType'),row.getValue('Lithology'),pTerm,pVal])
        row = rows.next()
    del row, rows
    stdLithDict[unit] = description(unitDesc)
    return stdLithDict

def mapUnitPolys(stdLithDict,outputDir,logfile):
    addMsgAndPrint('  Translating GeologicMap/MapUnitPolys...')
    try:
        arcpy.MakeTableView_management('DescriptionOfMapUnits','DMU')
        if stdLithDict <> 'None':
                arcpy.AddField_management('DMU',"StdLith","TEXT",'','','255')
                rows = arcpy.UpdateCursor('DMU'  )
                row = rows.next()
                while row:
                    if row.MapUnit in stdLithDict:
                        row.StdLith = stdLithDict[row.MapUnit]
                        rows.updateRow(row)
                    row = rows.next()
                del row, rows
        arcpy.MakeFeatureLayer_management("GeologicMap/MapUnitPolys","MUP")
        arcpy.AddJoin_management('MUP','MapUnit','DMU','MapUnit')
        arcpy.AddJoin_management('MUP','DataSourceID','DataSources','DataSources_ID')
        arcpy.CopyFeatures_management('MUP','MUP2')
        DM = 'DescriptionOfMapUnits_'
        DS = 'DataSources_'
        for field in ('DataSourceID','MapUnit_1','Label_1', DM+'OBJECTID',  
                           DM+DM+'ID', DM+'DefinitionSourceID',DS+'DefinitionSourceID',
                           DS+'OBJECTID',DS+DS+'ID'):
            arcpy.DeleteField_management('MUP2',field)
        dumpTable('MUP2','MapUnitPolys.shp',True,outputDir,logfile,False,'MapUnitPolys')
    except:
        addMsgAndPrint(arcpy.GetMessages())
        addMsgAndPrint('  Failed to translate MapUnitPolys')

def removeJoins(fc):
    addMsgAndPrint('    Testing '+fc+' for joined tables')
    #addMsgAndPrint('Current workspace is '+arcpy.env.workspace)
    joinedTables = []
    # list fields
    fields = arcpy.ListFields(fc)
    for field in fields:
        # look for fieldName that indicates joined table, and remove jo
        fieldName = field.name
        i = fieldName.find('.')
        if i > -1:
            joinedTableName = fieldName[0:i]
            if not (joinedTableName in joinedTables) and (joinedTableName) <> fc:
                try:
                    joinedTables.append(joinedTableName)
                    arcpy.removeJoin(fc,joinedTableName)
                except:
                    pass
    if len(joinedTables) > 0:
        jts = ''
        for jt in joinedTables:
            jts = jts+' '+jt
        addMsgAndPrint('      removed joined tables '+jts)            

def linesAndPoints(fc,outputDir,logfile):
    addMsgAndPrint('  Translating '+fc+'...')
    cp = fc.find('/')
    fcShp = fc[cp+1:]+'.shp'
    LIN2 = fc[cp+1:]+'2'
    LIN = 'xx'+fc[cp+1:]
    removeJoins(fc)
    addMsgAndPrint('    Making layer '+LIN+' from '+fc)
    #try:
    arcpy.MakeFeatureLayer_management(fc,LIN)
    fieldList = arcpy.ListFields(fc,'')
    if 'Type' in fieldList:
        arcpy.AddField_management(LIN,'Definition','TEXT','#','#','254')
        arcpy.AddJoin_management(LIN,'Type','Glossary','Term')
        arcpy.CalculateField_management(LIN,'Definition','[Glossary.Definition]','VB')
        arcpy.RemoveJoin_management(LIN,'Glossary')
    # command below are 9.3+ specific
    sourceFields = arcpy.ListFields(fc,'*SourceID')
    for sField in sourceFields:
        nFieldName = sField.name[:-2]
        arcpy.AddField_management(LIN,nFieldName,'TEXT','#','#','254')
        arcpy.AddJoin_management(LIN,sField.name,'DataSources','DataSources_ID')
        arcpy.CalculateField_management(LIN,nFieldName,'[DataSources.Source]','VB')
        arcpy.RemoveJoin_management(LIN,'DataSources')
        arcpy.DeleteField_management(LIN,sField.name)
    arcpy.CopyFeatures_management(LIN,LIN2)
    arcpy.Delete_management(LIN)
    dumpTable(LIN2,fcShp,True,outputDir,logfile,False,fc[cp+1:])
    #except:
    #    addMsgAndPrint(arcpy.GetMessages())
    #    addMsgAndPrint('  Failed to translate '+fc)
    #    try:
    #        arcpy.DeleteFeatures_management('LIN')
    #    except:
    #        pass

def main(gdbCopy,outWS,oldgdb):
    #
    # Open version
    #
    isOpen = True
    addMsgAndPrint('')
    outputDir, logfile = makeOutputDir(oldgdb,outWS,isOpen)
    # list featuredatasets
    arcpy.env.workspace = gdbCopy
    fds = arcpy.ListDatasets()
    # for each featuredataset
    for fd in fds:
        arcpy.workspace = gdbCopy
        addMsgAndPrint( '  Processing feature data set '+fd+'...')
        logfile.write('Feature data set '+fd+' \n')
        try:
            spatialRef = arcpy.Describe(fd).SpatialReference
            logfile.write('  spatial reference framework\n')
            logfile.write('    name = '+spatialRef.Name+'\n')
            logfile.write('    spheroid = '+spatialRef.SpheroidName+'\n')
            logfile.write('    projection = '+spatialRef.ProjectionName+'\n')
            logfile.write('    units = '+spatialRef.LinearUnitName+'\n')
        except:
            logfile.write('  spatial reference framework appears to be undefined\n')
        # generate featuredataset prefix
        pfx = ''
        for i in range(0,len(fd)-1):
            if fd[i] == fd[i].upper():
                pfx = pfx + fd[i]
        # for each featureclass in dataset
        arcpy.env.workspace = fd
        fcList = arcpy.ListFeatureClasses()
        if fcList <> None:
            for fc in arcpy.ListFeatureClasses():
                outName = pfx+'_'+fc+'.shp'
                dumpTable(fc,outName,True,outputDir,logfile,isOpen,fc)
        else:
            addMsgAndPrint('   No feature classes in this dataset!')
        logfile.write('\n')
    # list tables
    arcpy.env.workspace = gdbCopy
    for tbl in arcpy.ListTables():
        outName = tbl+'.dbf'
        dumpTable(tbl,outName,False,outputDir,logfile,isOpen,tbl)
    logfile.close()
    #
    # Simple version
    #
    isOpen = False
    addMsgAndPrint('')
    outputDir, logfile = makeOutputDir(oldgdb,outWS,isOpen)
    # point feature classes
    arcpy.env.workspace = gdbCopy
    if 'StandardLithology' in arcpy.ListTables():
        stdLithDict = makeStdLithDict()
    else:
        stdLithDict = 'None'
    mapUnitPolys(stdLithDict,outputDir,logfile)       
    arcpy.env.workspace = 'GeologicMap'
    pointfcs = arcpy.ListFeatureClasses('','POINT')
    linefcs = arcpy.ListFeatureClasses('','LINE')
    arcpy.env.workspace = gdbCopy
    for fc in pointfcs:
        linesAndPoints('GeologicMap/'+fc,outputDir,logfile)	
    for fc in linefcs:
        linesAndPoints('GeologicMap/'+fc,outputDir,logfile)
    linesAndPoints('GeologicMap/DataSourcePolys',outputDir,logfile)
    logfile.close()

### START HERE ###
if len(sys.argv) <> 3 or not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
    usage()
else:
    addMsgAndPrint('  '+versionString)
    gdb = os.path.abspath(sys.argv[1])
    ows = os.path.abspath(sys.argv[2])
    arcpy.env.QualifiedFieldNames = False
    arcpy.env.overwriteoutput = True
    ## fix the new workspace name so it is guaranteed to be novel, no overwrite
    newgdb = ows+'/xx'+os.path.basename(gdb)
    if arcpy.Exists(newgdb):
        arcpy.Delete_management(newgdb)
    addMsgAndPrint('  Copying '+os.path.basename(gdb)+' to temporary geodatabase...')
    arcpy.Copy_management(gdb,newgdb)
    main(newgdb,ows,gdb)
    addMsgAndPrint('\n  Deleting temporary geodatabase...')
    arcpy.env.workspace = ows
    time.sleep(5)
    try:
        arcpy.Delete_management(newgdb)
    except:
        addMsgAndPrint('    As usual, failed to delete temporary geodatabase')
        addMsgAndPrint('    Please delete '+newgdb+'\n')
