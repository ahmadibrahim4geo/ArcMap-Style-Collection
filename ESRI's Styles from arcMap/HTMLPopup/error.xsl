<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<xsl:template match="/">
		<html>
			<body>
				<table border="1" width="300" cellpadding="5" cellspacing="0">
					<tr bgcolor="#d50000">
						<th width="50%" align="left">Error</th>
					</tr>
					<xsl:variable name="index" select="1"/>
					<xsl:for-each select="ErrorDoc/Errors/Error">
						<tr>
							<td>
								<xsl:value-of select="ErrorText"/>
							</td>
						</tr>
					</xsl:for-each>
				</table>
				<br/>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
