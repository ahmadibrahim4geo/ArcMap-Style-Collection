<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:msxsl="urn:schemas-microsoft-com:xslt">
	<xsl:template match="/">
		<html xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:msxsl="urn:schemas-microsoft-com:xslt">
			<head> 
				<META http-equiv="Content-Type" Content="text/html; charset=utf-16" />
			</head> 
			<body>
				<style>
					body { font-family:Arial; font-size:11px } 
					h1 { font-family:Arial; font-size:20px; } 
					h2 { font-family:Arial; font-size:16px; } 
					h3 { font-family:Arial; font-size:12px; } 
					h4 { font-family:Arial; font-size:11px; } 
					h5 { font-family:Arial; font-size:8px; } 
					p { font-family:Arial; font-size:11px } 
					img { border-bottom-style:none; border-left-style:none; border-right-style:none; border-top-style:none; width:200px;} 
					td { width:auto; vertical-align:top; }
					table { font-family:Arial; font-size:11px; table-layout:inherit; width:275px; } 
				</style> 
				<table> 
					<tr>
						<td>
							<xsl:variable name="modifiedDescription">
								<xsl:call-template name="targetBlankWindow">
									<xsl:with-param name="description" select="FieldsDoc/Fields/Field[FieldName = 'Description']/FieldValue" />
								</xsl:call-template>
							</xsl:variable>
							<p>
								<xsl:value-of select="$modifiedDescription" disable-output-escaping="yes"/>
							</p>
						</td>
					</tr> 
					<tr>
						<td>
							<p>
								<xsl:variable name="imageLinkUrl" select="FieldsDoc/Fields/Field[FieldName = 'Image Link URL' or FieldName = 'Image_Link_URL']/FieldValue"/>
								<xsl:variable name="imageLink" select="FieldsDoc/Fields/Field[FieldName = 'Image URL' or FieldName = 'Image_URL']/FieldValue"/>
								<xsl:choose>
									<xsl:when test="$imageLinkUrl != '&lt;Null&gt;'">
										<a target="_blank">
											<xsl:attribute name="href">
												<xsl:value-of select="$imageLinkUrl" />
											</xsl:attribute>
											<img>
												<xsl:attribute name="src">
													<xsl:value-of select="$imageLink"/>
												</xsl:attribute>
											</img>
										</a>
									</xsl:when>
									<xsl:otherwise>
										<xsl:if test="$imageLink != '&lt;Null&gt;'">
											<img>
												<xsl:attribute name="src">
													<xsl:value-of select="$imageLink"/>
												</xsl:attribute>
											</img>
										</xsl:if>
									</xsl:otherwise>
								</xsl:choose>
							</p>
						</td>
					</tr> 
				</table> 
			</body> 
		</html>
	</xsl:template>

	<xsl:template name="targetBlankWindow">
		<xsl:param name="description" />
		<xsl:variable name="oldString" select="'a href'"/>
		<xsl:variable name="newString" select="'a target=&quot;_blank&quot; href'"/>
		<xsl:choose>
			<xsl:when test="contains($description, $oldString)">
				<xsl:value-of select="substring-before($description,$oldString)" />
				<xsl:value-of select="$newString" />
				<xsl:call-template name="targetBlankWindow">
					<xsl:with-param name="description" select="substring-after($description,$oldString)" />
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$description" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>