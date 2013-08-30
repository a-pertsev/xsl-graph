<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">


    <xsl:template match="/">
        <xsl:apply-templates select="item"/>
    </xsl:template>

    <xsl:template match="item"/>

    <xsl:template match="some_tem" mode="xx"/>

    <xsl:template match="some_tem[@id]"/>

    <xsl:template match="some_tem/*"/>




</xsl:stylesheet>


