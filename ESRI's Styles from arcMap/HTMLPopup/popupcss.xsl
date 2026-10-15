<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<xsl:template match="/">
		<html>
		<head>
			<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
			<!-- Blue heading - alternating blue/white - all black text-->
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: white;}
			tr.shade {background-color: #D4E4F3;}
			th {color: black;background-color: #9CBCE2; border-width: 1px;}
			td {color: black;border-width: 1px;}
			</style>
			
			<!-- Blue heading - alternating blues
			<style type="text/css">
			body{padding: 0px; margin: 0px}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #B8CCE4;}
			tr.shade {background-color: #DBE5F1;}
			th {color: white; background-color: #4F81BD; border-width: 0px 0px 2px 0px;}
			td {border-width: 0px 0px 1px 0px;}
			</style-->

			<!-- Black heading - alternating blues - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #376091;}
			tr.shade {background-color: #4F81BD;}
			th {color: white;background-color: black; border-width: 0px 0px 2px 0px;}
			td {color: white;border-width: 0px;}
			a {color: white;}
			</style-->
			
			<!-- Red heading - alternating blues
			<style type="text/css">
			body{padding: 0px; margin: 0px}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #B8CCE4;}
			tr.shade {background-color: #DBE5F1;}
			th {color: white;background-color: #C0504D; border-width: 0px;}
			td {border-width: 0px;}
			</style-->
			
			<!-- Black heading - alternating red - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #953735;}
			tr.shade {background-color: #C0504D;}
			th {color: white;background-color: black; border-width: 0px 0px 2px 0px;}
			td {color: white;border-width: 0px;}
			a {color: white;}
			</style-->
			
			<!-- Black heading - alternating gray - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #404040;}
			tr.shade {background-color: #737373;}
			th {color: white;background-color: black; border-width: 0px 0px 2px 0px;}
			td {color: white;border-width: 0px;}
			a {color: white;}
			</style-->
			
			<!-- Black heading - alternating light gray - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #A5A5A5;}
			tr.shade {background-color: #D8D8D8;}
			th {color: white;background-color: black; border-width: 0px;}
			td {border-width: 0px;}
			a {color: black;}
			</style-->
			
			<!-- Black heading - alternating greens - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #75923C;}
			tr.shade {background-color: #9BBB59;}
			th {color: white;background-color: black; border-width: 0px 0px 2px 0px;}
			td {color: white;border-width: 0px;}
			a {color: white;}
			</style-->
			
			<!-- Black heading - alternating oranges - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #E46D0A;}
			tr.shade {background-color: #F79646;}
			th {color: white;background-color: black; border-width: 0px 0px 2px 0px;}
			td {color: white;border-width: 0px;}
			a {color: white;}
			</style-->
			
			<!-- Black heading - alternating Purples - all white text
			<style type="text/css">
			body{padding: 0px; margin: 0px;}
			table{font-family:arial; font-size:11pt;}
			tr {background-color: #60497B;}
			tr.shade {background-color: #8064A2;}
			th {color: white;background-color: black; border-width: 0px 0px 2px 0px;}
			td {color: white;border-width: 0px;}
			a {color: white;}
			</style-->
		</head>
		<body>
			<xsl:variable name="nameCol" select="FieldsDoc/Fields/Field/FieldName"/>
			<table border="1" width="300" cellpadding="5" cellspacing="0">
				<tr>
					<xsl:if test="$nameCol">
						<th width="50%" align="left">Field Name</th>
					</xsl:if>
					<th width="50%" align="left">Field Value</th>
				</tr>
				<xsl:for-each select="FieldsDoc/Fields/Field">
				<tr>
					<xsl:if test="(position() +1) mod 2"><xsl:attribute name="class">shade</xsl:attribute></xsl:if>
					<xsl:if test="$nameCol">
					<td><xsl:value-of select="FieldName"/></td>
					</xsl:if>
					<td>
						<xsl:choose>
							<xsl:when test="FieldValue[starts-with(., 'www.')]">
								<a target="_blank"><xsl:attribute name="href">http://<xsl:value-of select="FieldValue"/>
								</xsl:attribute><xsl:value-of select="FieldValue"/>
								</a>
							</xsl:when>
							<xsl:when test="FieldValue[starts-with(., 'http:')]">
								<a target="_blank"><xsl:attribute name="href"><xsl:value-of select="FieldValue"/>
								</xsl:attribute><xsl:value-of select="FieldValue"/>
								</a>  
							</xsl:when>
							<xsl:when test="FieldValue[starts-with(., 'https:')]">
								<a target="_blank"><xsl:attribute name="href"><xsl:value-of select="FieldValue"/>
								</xsl:attribute><xsl:value-of select="FieldValue"/>
								</a>  
							</xsl:when>
							<xsl:when test="FieldValue[starts-with(., '\\')]">
								<a target="_blank"><xsl:attribute name="href"><xsl:value-of select="FieldValue"/>
								</xsl:attribute><xsl:value-of select="FieldValue"/>
								</a>  
							</xsl:when>
							<xsl:when test="FieldValue[starts-with(., '&lt;img ')]">
								<xsl:value-of select="FieldValue" disable-output-escaping="yes" />
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="FieldValue"/>
							</xsl:otherwise>
						</xsl:choose>
					</td>
				</tr>
				</xsl:for-each>

			</table>
		</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
