<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:msxsl="urn:schemas-microsoft-com:xslt">

                <xsl:template match="/">
                                <html>
                                                <head>      
                                                </head>
                                                <body>
                                                                <table>
                                                                <tr><td style="white-space: nowrap;">
                                                                                <xsl:choose>
                                                                                                <xsl:when test="FieldsDoc/Fields/Field/FieldName">
                                                                                                                <xsl:apply-templates select="FieldsDoc/Fields/Field/FieldName[contains(., 'PopupInfo')]/.." />
                                                                                                </xsl:when>
                                                                                                <xsl:otherwise>
                                                                                                                <xsl:apply-templates select="FieldsDoc/Fields/Field"/>
                                                                                                </xsl:otherwise>
                                                                                </xsl:choose>
                                                                                </td></tr>
                                                                </table>
                                                </body>
                                </html>
                </xsl:template>

                <xsl:template match="Field">
                                <xsl:value-of select="FieldValue" disable-output-escaping="yes"/>
                </xsl:template>               
</xsl:stylesheet>
