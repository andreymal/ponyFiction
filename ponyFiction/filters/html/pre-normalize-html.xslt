<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:re="http://exslt.org/regular-expressions"
    xmlns:str="http://exslt.org/strings"
    extension-element-prefixes="re str">
    
<xsl:template match="body">
    <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <p><xsl:apply-templates select="node()"/></p>
    </xsl:copy>
</xsl:template>
    
<xsl:template match="p">
    <p-splitter/>
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
    <p-splitter/>
</xsl:template>

<xsl:template match="text()">
    <xsl:variable name="text" select="re:replace(., '\n\s*\n', 'g', ' \n\n ')"/>
    <xsl:for-each select="str:split($text, '&#10;&#10;')">
        <xsl:for-each select="str:split(., '&#10;')">
            <text><xsl:value-of select="."/></text>
            <xsl:if test="following-sibling::*">
                <br/>
            </xsl:if>
        </xsl:for-each>
        <xsl:if test="following-sibling::*">
            <p-splitter/>
        </xsl:if>
    </xsl:for-each>
</xsl:template>

<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
</xsl:template>
    
</xsl:stylesheet>