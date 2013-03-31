<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:key
    name="footnotes"
    match="footnote"
    use="@id"
    />
    
<xsl:key
    name="anchors"
    match="a[starts-with(@href, '#')]"
    use="substring-after(@href, '#')"
    />
    
<xsl:template match="footnote">
    <p id="{@id}" class="footnote">
        <a name="{@id}"></a>
        
        <xsl:value-of select="concat('[', count(preceding::footnote)+1, '] ')"/>
        <span class="footnote-back-links">
        <xsl:for-each select="key('anchors', @id)">
            <a>
                <xsl:attribute name="href">#<xsl:value-of select="generate-id(.)"/></xsl:attribute>
                <xsl:value-of select="position()"/>
            </a>
            <xsl:choose>
                <xsl:when test="position() != last()">
                    <xsl:text>, </xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text> </xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
        </span>
        
        <xsl:apply-templates select="node()"/>
    </p>
</xsl:template>

<xsl:template match="a[starts-with(@href, '#')][key('footnotes', substring-after(@href, '#'))]">
    <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <xsl:attribute name="id"><xsl:value-of select="generate-id(.)"/></xsl:attribute>
        <xsl:attribute name="name"><xsl:value-of select="generate-id(.)"/></xsl:attribute>
        <xsl:attribute name="class">footnote-link</xsl:attribute>
        
        <xsl:apply-templates select="node()"/>
        <xsl:if test="not(node())">
            <xsl:value-of select="concat('[', count(key('footnotes', substring-after(@href, '#'))/preceding::footnote)+1, ']')"/>
        </xsl:if>
    </xsl:copy>
</xsl:template>

<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>