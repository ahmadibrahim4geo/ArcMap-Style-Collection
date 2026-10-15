<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<xsl:template match="/">
		<html>
			<head>
				<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
			</head>
			<body>
				<xsl:variable name="nameCol" select="FieldsDoc/Fields/Field/FieldName"/>
				<table border="1" width="300" cellpadding="5" cellspacing="0">
					<tr bgcolor="#d87d34">
						<xsl:if test="string-length($nameCol) != 0">
							<th width="50%" align="left">Field Name</th>
						</xsl:if>
						<th width="50%" align="left">Field Value</th>
					</tr>
					<xsl:variable name="index" select="1"/>
					<xsl:for-each select="FieldsDoc/Fields/Field">
						<tr>
							<xsl:if test="(position() +1) mod 2">
								<xsl:attribute name="bgcolor">#ebbc96</xsl:attribute>
							</xsl:if>
							<xsl:if test="string-length($nameCol) != 0">
								<td>
									<xsl:value-of select="FieldName"/>
								</td>
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
									<xsl:otherwise>
										<xsl:value-of select="FieldValue"/>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
					</xsl:for-each>
				</table>
				<br/>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
