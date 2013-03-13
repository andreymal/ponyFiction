<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:re="http://exslt.org/regular-expressions"
    xmlns:str="http://exslt.org/strings"
    extension-element-prefixes="re str">
    
<xsl:template match="body">
    <xsl:copy>
        <!-- <xsl:apply-templates match="@*"/> -->
        <p><xsl:apply-templates match="node()"/></p>
    </xsl:copy>
</xsl:template>
    
<xsl:template match="p">
    <p-splitter/>
    <xsl:copy>
        <xsl:apply-templates match="@*|node()"/>
    </xsl:copy>
    <p-splitter/>
</xsl:template>

<xsl:template match="text()">
    <xsl:variable name="text" select="re:replace(., '\n[\n\s]*\n', 'g', '\n\n')"/>
    
    <!-- str:split skips separator at the beginning of the string. -->
    <xsl:if test="starts-with($text, '&#10;&#10;')">
        <p-splitter/>
    </xsl:if>
    
    <xsl:for-each select="str:split($text, '&#10;&#10;')">
        <text><xsl:value-of select="."/></text><!-- TODO: <br> -->
        <xsl:if test="following-sibling::*">
            <p-splitter/>
        </xsl:if>
    </xsl:for-each>
    
    <!-- str:split skips separator at the end of the string. -->
    <xsl:if test="substring($text, string-length($text) - 1) = '&#10;&#10;'">
        <p-splitter/>
    </xsl:if>
</xsl:template>

<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates match="@*|node()"/>
    </xsl:copy>
</xsl:template>
    
</xsl:stylesheet>