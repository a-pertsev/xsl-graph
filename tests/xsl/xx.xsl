<xsl:stylesheet xmlns:hh="http://schema.reintegration.hh.ru/types" xmlns:func="http://exslt.org/functions" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" version="1.0" exclude-result-prefixes="hh func">

    <xsl:template match="doc" mode="page-body-ambient">
        <xsl:call-template name="site-exceptions"/>
        <xsl:apply-templates select="." mode="kangaroo"/>
        <xsl:apply-templates select="/doc/resumePublishReminder" mode="applicant-resume-reminder"/>
        <xsl:apply-templates select="." mode="sochi-topmenu"/>
        <xsl:apply-templates select="." mode="page-head-ambient"/>
        <xsl:call-template name="menublock"/>
        <xsl:apply-templates select="." mode="page-center"/>
        <xsl:apply-templates select="." mode="page-foot-ambient"/>
    </xsl:template>

    <xsl:template name="sochi-logo-headblock"><!--some stuff--></xsl:template>

    <xsl:template name="menublock">
        <xsl:call-template name="sochi-index-menu"/>
        <xsl:call-template name="sochi-index-search"/>
    </xsl:template>

    <xsl:template name="sochi-index-menu">
        <xsl:apply-templates select="." mode="sochi-index-menu-items"/>
    </xsl:template>

    <xsl:template match="*" mode="sochi-index-menu-items"><!--some stuff--></xsl:template>

    <xsl:template match="*[key('userType','applicant')]" mode="sochi-index-menu-items"><!--some stuff--></xsl:template>

    <xsl:template match="*[key('userType','employer')]" mode="sochi-index-menu-items"><!--some stuff--></xsl:template>

    <xsl:template name="sochi-index-search">
        <xsl:apply-templates select="/doc/hh:professionalAreaList/professionalArea" mode="professionalarealist-options"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-center">
        <xsl:apply-templates select="key('article', '2226')/body" mode="firstpage-content-articledata"/>
        <xsl:apply-templates select="key('article', '2227')/body" mode="firstpage-content-articledata"/>
        <xsl:apply-templates select="key('article', '2228')/body" mode="firstpage-content-articledata"/>
    </xsl:template>

    <xsl:template match="article/body//h2" mode="firstpage-content-articledata">
        <xsl:apply-templates mode="firstpage-content-articledata"/>
    </xsl:template>

    <xsl:template match="article/body//h3" mode="firstpage-content-articledata">
        <xsl:apply-templates mode="firstpage-content-articledata"/>
    </xsl:template>

    <xsl:template match="article/body//p" mode="firstpage-content-articledata">
        <xsl:apply-templates mode="firstpage-content-articledata"/>
    </xsl:template>

    <xsl:template match="article/body//a" mode="firstpage-content-articledata">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="article/body//a/text()" mode="firstpage-content-articledata"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="verification-codes">
        <xsl:call-template name="common-verifications"/>
    </xsl:template>

    <xsl:template match="hh:professionalAreaList/professionalArea" mode="professionalarealist-options">
        <xsl:apply-templates select="name"/>
    </xsl:template>

    <xsl:template match="professionalArea/name"><!--some stuff--></xsl:template>

    <xsl:template match="professionalArea/name[../id=0]"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="html-guts">
        <xsl:apply-imports/>
    </xsl:template>

    <xsl:template match="doc" mode="fork-page-body">
        <xsl:apply-templates select="." mode="page-body-ambient"/>
    </xsl:template>

    <xsl:template match="doc">
        <xsl:apply-templates select="." mode="html-guts"/>
        <xsl:apply-templates select="current()[not(new-banner-system)]" mode="get-banners"/>
    </xsl:template>

    <xsl:template match="doc" mode="get-banners"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="html-guts">
        <xsl:apply-templates select="." mode="head"/>
        <xsl:apply-templates select="." mode="fork-page-body"/>
    </xsl:template>

    <xsl:template match="*" mode="fork-page-body">
        <xsl:apply-templates select="." mode="page-body"/>
    </xsl:template>

    <xsl:template match="*" mode="page-foot-ambient">
        <xsl:apply-templates select="." mode="footer-counters"/>
    </xsl:template>

    <xsl:template match="doc" mode="ga-reg"/>

    <xsl:template match="doc" mode="footer-counters">
        <xsl:call-template name="ga-load-js-file"/>
        <xsl:apply-templates select="." mode="custom-counters"/>
        <xsl:apply-templates select="current()[key('site','seo-domain') = 'false']" mode="not-seo-counters"/>
        <xsl:apply-templates select="current()[key('site','seo-domain') = 'true']" mode="seo-counters"/>
        <xsl:apply-templates select="/doc/additional-applicant-data" mode="adwolf"/>
        <xsl:apply-templates select="/doc/convertionGoals/goal"/>
        <xsl:apply-templates select="/doc/counterEF"/>
        <xsl:apply-templates select="." mode="track-analytics-event"/>
    </xsl:template>

    <xsl:template match="convertionGoals/goal">
        <xsl:call-template name="track-analytics-event">
            <xsl:with-param name="category" select="@category"/>
            <xsl:with-param name="event" select="@event"/>
            <xsl:with-param name="label" select="@label"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="track-analytics-event"><!--some stuff--></xsl:template>

    <xsl:template match="trackAnalyticsEvent"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="custom-counters"/>

    <xsl:template match="*" mode="not-seo-counters"/>

    <xsl:template match="*" mode="seo-counters"/>

    <xsl:template match="*" mode="track-analytics-event"/>

    <xsl:template match="counterEF"><!--some stuff--></xsl:template>

    <xsl:template match="additional-applicant-data" mode="adwolf">
        <xsl:apply-templates select="." mode="adwolf-p1-param"/>
        <xsl:apply-templates select="/doc/resumes/resume[position()=1]" mode="adwolf-puid-params"/>
    </xsl:template>

    <xsl:template match="resume" mode="adwolf-puid-params">
        <xsl:apply-templates select="gender" mode="adwolf-gender-param"/>
    </xsl:template>

    <xsl:template match="additional-applicant-data[key('site', 'site-id') = '18']" mode="adwolf-p1-param"><!--some stuff--></xsl:template>

    <xsl:template match="additional-applicant-data" mode="adwolf-p1-param"><!--some stuff--></xsl:template>

    <xsl:template match="gender[text()='male']" mode="adwolf-gender-param"><!--some stuff--></xsl:template>

    <xsl:template match="gender[text()='female']" mode="adwolf-gender-param"><!--some stuff--></xsl:template>

    <xsl:template name="ga-load-js-file">
        <xsl:apply-templates select="." mode="ga-js-src"/>
    </xsl:template>

    <xsl:template name="google-counters">
        <xsl:call-template name="ga-common">
            <xsl:with-param name="type" select="'main'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="ga-common">
        <xsl:apply-templates select="." mode="ga-setDomain">
            <xsl:with-param name="type" select="$type"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc" mode="ga-reg">
        <xsl:call-template name="ga-common">
            <xsl:with-param name="type" select="'reg'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="doc" mode="ga-setDomain">
        <xsl:call-template name="ga-setDomain">
            <xsl:with-param name="type" select="$type"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="ga-setDomain"><!--some stuff--></xsl:template>

    <xsl:template match="session" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="session[/doc/botDetected]" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="session[not(hh-session/account)][hhid-session/account]" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="session[hh-session/account/userType]" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="userType" mode="user-custom-vars"/>

    <xsl:template match="userType[. = 'employer']" mode="user-custom-vars"><!--some stuff--></xsl:template>

    <xsl:template match="userType[. = 'applicant']" mode="user-custom-vars">
        <xsl:apply-templates select="/doc/resumes[1]/@total" mode="user-resumes-var">
            <xsl:with-param name="type" select="$type"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="@total" mode="user-resumes-var"><!--some stuff--></xsl:template>

    <xsl:template match="gender" mode="user-gender-var"><!--some stuff--></xsl:template>

    <xsl:template match="age" mode="user-age-var"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="ga-additional-params"/>

    <xsl:template name="ga-additional-tracks"/>

    <xsl:template match="doc" mode="ga-js-src"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="content">
        <xsl:apply-templates select="." mode="page-content-ambient"/>
    </xsl:template>

    <xsl:template match="doc[error[@type='autologin' and @code='409']]" mode="page-content-errorwrap"><!--some stuff--></xsl:template>

    <xsl:template match="doc[error[@code='404' and @blacklisted='true']]" mode="page-content-errorwrap"><!--some stuff--></xsl:template>

    <xsl:template match="doc[error[@code='599' or @code='403' or @code='400' or (@code='404' and @fatal='true')]]" mode="page-content-errorwrap">
        <xsl:apply-templates select="error[1]" mode="page-error"/>
    </xsl:template>

    <xsl:template match="doc[vacancy-wrapper[not(vacancies/vacancy)]/error[position()=last()] or employer-data/error or autosearches/error]" mode="page-content-errorwrap">
        <xsl:apply-templates select="vacancy-wrapper/error[position()=last()]" mode="page-error"/>
        <xsl:apply-templates select="employer-data/error" mode="page-error"/>
        <xsl:apply-templates select="autosearches/error" mode="page-error"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-content-errorwrap">
        <xsl:apply-templates select="." mode="content"/>
    </xsl:template>

    <xsl:template match="doc" mode="content">
        <xsl:apply-templates select="." mode="page-content"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-body-ambient">
        <xsl:call-template name="site-exceptions"/>
        <xsl:apply-templates select="." mode="kangaroo"/>
        <xsl:apply-templates select="/doc/resumePublishReminder" mode="applicant-resume-reminder"/>
        <xsl:apply-templates select="." mode="sochi-topmenu"/>
        <xsl:apply-templates select="." mode="page-head-ambient"/>
        <xsl:apply-templates select="." mode="sochi-menu"/>
        <xsl:apply-templates select="/doc/notifications" mode="global-notification-messages"/>
        <xsl:apply-templates select="." mode="page-center"/>
        <xsl:apply-templates select="." mode="page-foot-ambient"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-center">
        <xsl:apply-templates select="." mode="page-center-without-banner"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-center-without-banner">
        <xsl:call-template name="flashnote"/>
        <xsl:apply-templates select="." mode="page-content-errorwrap"/>
    </xsl:template>

    <xsl:template match="*" mode="rightcell-ambient">
        <xsl:apply-templates select="." mode="insert-banner">
            <xsl:with-param name="id" select="29"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="resumePublishReminder" mode="applicant-resume-reminder">
        <xsl:apply-templates select="." mode="reminder-text"/>
    </xsl:template>

    <xsl:template match="resumePublishReminder[incompleteBlock]" mode="reminder-text"><!--some stuff--></xsl:template>

    <xsl:template match="resumePublishReminder" mode="reminder-text"><!--some stuff--></xsl:template>

    <xsl:template name="flashnote">
        <xsl:apply-templates select="/doc/flashnote" mode="flashnote"/>
    </xsl:template>

    <xsl:template match="flashnote" mode="flashnote">
        <xsl:apply-templates select="@modifier"/>
    </xsl:template>

    <xsl:template match="@modifier[.='error']"><!--some stuff--></xsl:template>

    <xsl:template match="@modifier[.='ok']"><!--some stuff--></xsl:template>

    <xsl:template match="@modifier"/>

    <xsl:template name="site-exceptions">
        <xsl:call-template name="site-exceptions-block"/>
    </xsl:template>

    <xsl:template name="site-exceptions">
        <xsl:call-template name="site-exceptions-block"/>
    </xsl:template>

    <xsl:template name="site-exceptions-block">
        <xsl:apply-templates select="/doc/pagedata/session[@fallback='true' and not(key('cookies', 'ignoreException')='true')]" mode="site-exception"/>
    </xsl:template>

    <xsl:template match="session" mode="site-exception"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="sochi-menu">
        <xsl:apply-templates select="." mode="sochi-menu-applicant"/>
        <xsl:apply-templates select="." mode="sochi-menu-employer"/>
        <xsl:apply-templates select="." mode="sochi-menu-anonymous"/>
    </xsl:template>

    <xsl:template match="*" mode="sochi-menu-anonymous"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="sochi-menu-applicant"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="sochi-menu-employer"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="sochi-topmenu">
        <xsl:apply-templates select="sochiTopMenu/*"/>
    </xsl:template>

    <xsl:template match="menuItem">
        <xsl:apply-templates select="@href"/>
        <xsl:apply-templates select="@en-href"/>
    </xsl:template>

    <xsl:template match="@href[key('site', 'lang') = 'EN']"/>

    <xsl:template match="@en-href[key('site', 'lang') != 'EN']"/>

    <xsl:template match="sochiTopMenu/menuItem[@selected]"><!--some stuff--></xsl:template>

    <xsl:template match="sochiTopMenu/menuItems">
        <xsl:apply-templates select="menuItem"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-head-ambient">
        <xsl:call-template name="sochi-logo-headblock"/>
        <xsl:apply-templates select="." mode="sochi-links-headblock"/>
        <xsl:apply-templates select="." mode="sochi-viewmode"/>
        <xsl:apply-templates select="." mode="sochi-langswitcher"/>
        <xsl:apply-templates select="." mode="sochi-headlogin"/>
    </xsl:template>

    <xsl:template name="sochi-logo-headblock"/>

    <xsl:template match="*" mode="sochi-links-headblock">
        <xsl:apply-templates select="." mode="sochi-cok-logo"/>
        <xsl:apply-templates select="sochiPhone"/>
        <xsl:apply-templates select="." mode="sochi-headlinks"/>
    </xsl:template>

    <xsl:template match="*" mode="sochi-cok-logo"><!--some stuff--></xsl:template>

    <xsl:template match="sochiPhone"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="sochi-headlinks"><!--some stuff--></xsl:template>

    <xsl:template match="*[key('userType','applicant') and key('user', 'frozen') = 'false']" mode="sochi-headlinks">
        <xsl:call-template name="current-user-full-name-iof"/>
    </xsl:template>

    <xsl:template match="*[key('userType','back_office_user')]" mode="sochi-headlinks">
        <xsl:call-template name="current-user-full-name-iof"/>
    </xsl:template>

    <xsl:template match="*[key('userType','employer') or key('sudouser','fullName') or key('user', 'frozen') = 'true']" mode="sochi-headlinks">
        <xsl:apply-templates select="." mode="sochi-username"/>
        <xsl:apply-templates select="." mode="sochi-employerdropdown"/>
    </xsl:template>

    <xsl:template match="*" mode="sochi-employerdropdown">
        <xsl:apply-templates select="." mode="sochi-username"/>
        <xsl:call-template name="sudo-user-full-name-iof"/>
    </xsl:template>

    <xsl:template match="*" mode="sochi-username"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="sochi-viewmode"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="sochi-langswitcher"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="sochi-headlogin"><!--some stuff--></xsl:template>

    <xsl:template match="/doc[error/@code='403']" mode="sochi-headlogin"/>

    <xsl:template match="*" mode="page-topbanner"/>

    <xsl:template match="doc" mode="css-href"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="head">
        <xsl:apply-templates select="." mode="page-header-title-wrapper"/>
        <xsl:apply-templates select="." mode="meta-description"/>
        <xsl:apply-templates select="." mode="meta-keywords"/>
        <xsl:apply-templates select="." mode="meta-og"/>
        <xsl:apply-templates select="." mode="meta-ya-island"/>
        <xsl:apply-templates select="." mode="verification-codes"/>
        <xsl:apply-templates select="." mode="head-links"/>
        <xsl:apply-templates select="." mode="head-rss"/>
        <xsl:apply-templates select="." mode="page-styles"/>
        <xsl:apply-templates select="." mode="css-href"/>
        <xsl:apply-templates select="." mode="window-hh"/>
        <xsl:call-template name="google-counters"/>
        <xsl:apply-templates select="." mode="other-head-scripts"/>
        <xsl:apply-templates select="." mode="other-head-templates"/>
        <xsl:apply-templates select="." mode="canonical-link"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-styles">
        <xsl:apply-templates select="." mode="page-header-style">
            <xsl:with-param name="filename">anonymous.css</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc" mode="window-hh">
        <xsl:apply-templates select="jsxDebug"/>
    </xsl:template>

    <xsl:template match="features/jsx_debug"><!--some stuff--></xsl:template>

    <xsl:template match="doc[(error/@code=404 or error/@code=403) and error/@fatal='true']" mode="page-header-title-wrapper">
        <xsl:apply-templates select="." mode="page-header-title-error"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-header-title-wrapper">
        <xsl:apply-templates select="." mode="page-header-title"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-header-title-error"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="page-header-title"><!--some stuff--></xsl:template>

    <xsl:template name="seo-domains-title"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="meta-description">
        <xsl:apply-templates select="." mode="page-description"/>
    </xsl:template>

    <xsl:template match="doc" mode="page-description"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="meta-ya-island"/>

    <xsl:template match="doc" mode="meta-keywords"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="meta-og">
        <xsl:apply-templates select="." mode="meta-og-imgs"/>
        <xsl:apply-templates select="logo/@ogImageSrc"/>
        <xsl:apply-templates select="." mode="meta-og-description"/>
    </xsl:template>

    <xsl:template match="@ogImageSrc"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="meta-og-imgs"/>

    <xsl:template match="doc" mode="meta-og-description">
        <xsl:apply-templates select="." mode="page-description"/>
    </xsl:template>

    <xsl:template match="doc" mode="verification-codes"/>

    <xsl:template name="common-verifications"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="head-links"/>

    <xsl:template match="doc" mode="head-rss"/>

    <xsl:template match="doc" mode="page-header-styles"/>

    <xsl:template match="doc" mode="unique-page-header-style"/>

    <xsl:template match="doc[key('userType', 'applicant')]" mode="page-header-styles">
        <xsl:apply-templates select="." mode="page-header-style">
            <xsl:with-param name="filename">applicant.css</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc[key('userType', 'employer')]" mode="page-header-styles">
        <xsl:apply-templates select="." mode="page-header-style">
            <xsl:with-param name="filename">employer.css</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc[key('userType', 'back_office_user')]" mode="page-header-styles">
        <xsl:apply-templates select="." mode="page-header-style">
            <xsl:with-param name="filename">applicant.css</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc" mode="page-header-style">
        <xsl:apply-templates select="." mode="css-href"/>
    </xsl:template>

    <xsl:template match="doc" mode="css-href"/>

    <xsl:template match="doc" mode="page-header-media">
        <xsl:apply-templates select="." mode="page-header-style">
            <xsl:with-param name="filename">lite.css</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc" mode="other-head-scripts"/>

    <xsl:template match="doc" mode="other-head-templates"/>

    <xsl:template match="mailru-domain-list" mode="rmr-domains"><!--some stuff--></xsl:template>

    <xsl:template name="region-to-cookie"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="canonical-link"/>

    <xsl:template name="ga-load-js-file">
        <xsl:apply-templates select="." mode="ga-js-src"/>
    </xsl:template>

    <xsl:template name="google-counters">
        <xsl:call-template name="ga-common">
            <xsl:with-param name="type" select="'main'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="ga-common">
        <xsl:apply-templates select="." mode="ga-setDomain">
            <xsl:with-param name="type" select="$type"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="doc" mode="ga-reg">
        <xsl:call-template name="ga-common">
            <xsl:with-param name="type" select="'reg'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="doc" mode="ga-setDomain">
        <xsl:call-template name="ga-setDomain">
            <xsl:with-param name="type" select="$type"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="ga-setDomain"><!--some stuff--></xsl:template>

    <xsl:template match="session" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="session[/doc/botDetected]" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="session[not(hh-session/account)][hhid-session/account]" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="session[hh-session/account/userType]" mode="user-status-var"><!--some stuff--></xsl:template>

    <xsl:template match="userType" mode="user-custom-vars"/>

    <xsl:template match="userType[. = 'employer']" mode="user-custom-vars"><!--some stuff--></xsl:template>

    <xsl:template match="userType[. = 'applicant']" mode="user-custom-vars">
        <xsl:apply-templates select="/doc/resumes[1]/@total" mode="user-resumes-var">
            <xsl:with-param name="type" select="$type"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="@total" mode="user-resumes-var"><!--some stuff--></xsl:template>

    <xsl:template match="gender" mode="user-gender-var"><!--some stuff--></xsl:template>

    <xsl:template match="age" mode="user-age-var"><!--some stuff--></xsl:template>

    <xsl:template match="doc" mode="ga-additional-params"/>

    <xsl:template name="ga-additional-tracks"/>

    <xsl:template match="doc" mode="ga-js-src"><!--some stuff--></xsl:template>

    <xsl:template match="fullName"><!--some stuff--></xsl:template>

    <xsl:template name="current-user-full-name-iof"><!--some stuff--></xsl:template>

    <xsl:template name="current-user-full-name-fio"><!--some stuff--></xsl:template>

    <xsl:template name="sudo-user-full-name-iof"><!--some stuff--></xsl:template>

    <xsl:template name="hhid-user-name"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-urls" mode="loginform-maincol"/>

    <xsl:template match="*" mode="insert-banner"/>

    <xsl:template match="*" mode="google-event"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="kangaroo"/>

    <xsl:template match="*[key('request','kangaroo') or key('cookies','kangaroo') = 'visible' or         key('cookies','kangaroo') = 'hidden']" mode="kangaroo"><!--some stuff--></xsl:template>

    <xsl:template match="/doc/notifications" mode="global-notification-messages">
        <xsl:apply-templates select="notification" mode="global-notification-message"/>
    </xsl:template>

    <xsl:template match="/doc/notifications[count(notification) = 0]" mode="global-notification-messages"/>

    <xsl:template match="notification" mode="global-notification-message">
        <xsl:apply-templates select="." mode="global-notification-message-class"/>
        <xsl:apply-templates select="." mode="global-notification-message-body"/>
    </xsl:template>

    <xsl:template match="notification[         code='billing.cart.activation.ready' or         code='billing.cart.activated'     ]" mode="global-notification-message-class"><!--some stuff--></xsl:template>

    <xsl:template match="notification[         code='billing.cart.insufficient.funds' or         code='billing.cart.irrelevant.status' or         code='billing.cart.system.error'     ]" mode="global-notification-message-class"><!--some stuff--></xsl:template>

    <xsl:template match="notification[         code='billing.cart.insufficient.funds' or         code='billing.cart.irrelevant.status' or         code='billing.cart.system.error'     ]" mode="global-notification-message-body"><!--some stuff--></xsl:template>

    <xsl:template match="notification[code='billing.cart.activated']" mode="global-notification-message-body"><!--some stuff--></xsl:template>

    <xsl:template match="notification[code='billing.cart.activation.ready']" mode="global-notification-message-body"><!--some stuff--></xsl:template>

    <xsl:template match="*"><!--some stuff--></xsl:template>

    <xsl:template match="node()" mode="usergenerate">
        <xsl:apply-templates mode="usergenerate"/>
    </xsl:template>

    <xsl:template match="text()" mode="usergenerate">
        <xsl:call-template name="break">
            <xsl:with-param name="text" select="."/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="break">
        <xsl:call-template name="break">
            <xsl:with-param name="text" select="substring-after($text, '&#10;')"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="div | br" mode="ugc">
        <xsl:apply-templates mode="ugc"/>
    </xsl:template>

    <xsl:template match="@*" mode="ugc"><!--some stuff--></xsl:template>

    <xsl:template match="node()" mode="ugc"/>

    <xsl:template match="text()" mode="ugc"><!--some stuff--></xsl:template>

    <xsl:template match="error"/>

    <xsl:template match="error[@code = 500 or @code = 599]" mode="page-error"><!--some stuff--></xsl:template>

    <xsl:template match="error" mode="page-error"><!--some stuff--></xsl:template>

    <xsl:template match="error[@code='403']" mode="page-error">
        <xsl:apply-templates select="." mode="loginform-maincol"/>
    </xsl:template>

    <xsl:template match="*" mode="loginform-maincol">
        <xsl:apply-templates select="@attention_message"/>
        <xsl:call-template name="password-block"/>
        <xsl:apply-templates select="/doc/oauth-auth-urls" mode="loginform-maincol"/>
        <xsl:call-template name="enter-block"/>
        <xsl:apply-templates select="/doc/oauth-auth-urls" mode="oauth-popup-content"/>
    </xsl:template>

    <xsl:template name="password-block"><!--some stuff--></xsl:template>

    <xsl:template name="enter-block"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-urls" mode="loginform-maincol">
        <xsl:apply-templates select="." mode="social-button"/>
    </xsl:template>

    <xsl:template match="@attention_message"><!--some stuff--></xsl:template>

    <xsl:template match="*[/doc/NoCookiesUser]" mode="loginform-maincol">
        <xsl:call-template name="no-cookies-login-form"/>
    </xsl:template>

    <xsl:template match="loginForm[/doc/NoCookiesUser]" mode="login-ambient">
        <xsl:call-template name="no-cookies-login-form">
            <xsl:with-param name="inputText" select="'error.nocookies.tryAgain.short'"/>
            <xsl:with-param name="nocookiesClass" select="'login_nocookies'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="no-cookies-login-form"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-urls" mode="social-button">
        <xsl:call-template name="rmr-button"/>
        <xsl:apply-templates select="oauth-auth-url[id = 'OK']" mode="social-button"/>
        <xsl:apply-templates select="oauth-auth-url[id = 'VK']" mode="social-button"/>
        <xsl:apply-templates select="oauth-auth-url[id = 'FB']" mode="social-button"/>
        <xsl:apply-templates select="oauth-auth-url[id = 'LI']" mode="social-button"/>
    </xsl:template>

    <xsl:template name="rmr-button"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-url" mode="social-button">
        <xsl:apply-templates select="." mode="social-button-type"/>
    </xsl:template>

    <xsl:template match="oauth-auth-url" mode="social-button-long">
        <xsl:apply-templates select="." mode="social-button-long-type"/>
        <xsl:apply-templates select="." mode="social-button-caption"/>
    </xsl:template>

    <xsl:template match="oauth-auth-url" mode="social-button-type"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-url" mode="social-button-long-type"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-url" mode="social-button-caption"><!--some stuff--></xsl:template>

    <xsl:template match="oauth-auth-urls" mode="oauth-popup-content"><!--some stuff--></xsl:template>

    <xsl:template name="applicant-confirm">
        <xsl:call-template name="applicant-confirm-switcher-text"/>
        <xsl:call-template name="applicant-confirm-component"/>
    </xsl:template>

    <xsl:template name="applicant-confirm-component"><!--some stuff--></xsl:template>

    <xsl:template name="applicant-confirm-switcher-text"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="insert-banner"><!--some stuff--></xsl:template>

    <xsl:template match="pager">
        <xsl:apply-templates select="os"/>
        <xsl:apply-templates select="previous"/>
        <xsl:apply-templates select="os"/>
        <xsl:apply-templates select="next"/>
        <xsl:apply-templates select="item"/>
    </xsl:template>

    <xsl:template match="os[text() = 'Mac']"><!--some stuff--></xsl:template>

    <xsl:template match="os"><!--some stuff--></xsl:template>

    <xsl:template match="previous">
        <xsl:call-template name="item-href"/>
    </xsl:template>

    <xsl:template match="previous[@disabled = 'True']"><!--some stuff--></xsl:template>

    <xsl:template match="next">
        <xsl:call-template name="item-href"/>
    </xsl:template>

    <xsl:template match="next[@disabled = 'True']"><!--some stuff--></xsl:template>

    <xsl:template match="pager/item">
        <xsl:apply-templates select="." mode="pager-item-content"/>
    </xsl:template>

    <xsl:template match="item" mode="pager-item-content">
        <xsl:call-template name="item-href"/>
    </xsl:template>

    <xsl:template match="item[@selected]" mode="pager-item-content"><!--some stuff--></xsl:template>

    <xsl:template name="item-href">
        <xsl:apply-templates select="." mode="item-wo-page-number-query"/>
    </xsl:template>

    <xsl:template match="*[key('wo-query', 'PageNumber') = '?']" mode="item-wo-page-number-query"><!--some stuff--></xsl:template>

    <xsl:template match="*" mode="item-wo-page-number-query"><!--some stuff--></xsl:template>

    <xsl:template match="/" mode="pager">
        <xsl:apply-templates select="/" mode="pager-item-link">
            <xsl:with-param name="href">
                <xsl:value-of select="$href"/><xsl:value-of select="0"/>
            </xsl:with-param>
            <xsl:with-param name="item" select="1"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="/" mode="pager-item">
        <xsl:apply-templates select="/" mode="pager-item-link">
            <xsl:with-param name="href">
                <xsl:value-of select="$href"/><xsl:value-of select="$item"/>
            </xsl:with-param>
            <xsl:with-param name="item" select="$item + 1"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="/" mode="pager-item-link"><!--some stuff--></xsl:template>

    <xsl:template match="*|@*" mode="get-date-from-string"><!--some stuff--></xsl:template>

    <xsl:template match="*|@*" mode="get-short-date-from-string"><!--some stuff--></xsl:template>

    <xsl:template match="*|@*" mode="get-dateandtime-from-string">
        <xsl:apply-templates select="." mode="get-date-from-string"/>
        <xsl:apply-templates select="." mode="get-hoursandminutes-from-string"/>
    </xsl:template>

    <xsl:template match="*|@*" mode="get-hoursandminutes-from-string"><!--some stuff--></xsl:template>

    <xsl:template match="*|@*" mode="conversion"><!--some stuff--></xsl:template>

    <xsl:template match="*|@*" mode="conversion-trl">
        <xsl:apply-templates select="." mode="conversion">
            <xsl:with-param name="num">
                <xsl:value-of select="$num"/>
            </xsl:with-param>
            <xsl:with-param name="one">
                <xsl:value-of select="hh:trl(concat($trl-prefix, '.one'), $lang)"/>
            </xsl:with-param>
            <xsl:with-param name="some">
                <xsl:value-of select="hh:trl(concat($trl-prefix, '.some'), $lang)"/>
            </xsl:with-param>
            <xsl:with-param name="many">
                <xsl:value-of select="hh:trl(concat($trl-prefix, '.many'), $lang)"/>
            </xsl:with-param>
            <xsl:with-param name="zero">
                <xsl:value-of select="hh:trl(concat($trl-prefix, '.some'), $lang)"/>
            </xsl:with-param>
            <xsl:with-param name="with-num" select="$with-num"/>
            <xsl:with-param name="separator" select="$separator"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*|@*" mode="conversion-trl-vacancy-new">
        <xsl:apply-templates select="." mode="conversion-trl">
            <xsl:with-param name="num" select="."/>
            <xsl:with-param name="trl-prefix" select="'autosearches.vacancy.new'"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*|@*" mode="conversion-trl-vacancy">
        <xsl:apply-templates select="." mode="conversion-trl">
            <xsl:with-param name="num" select="."/>
            <xsl:with-param name="trl-prefix" select="'statistics.global.vacancy'"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*|@*" mode="conversion-found">
        <xsl:apply-templates select="." mode="conversion">
            <xsl:with-param name="num" select="."/>
            <!-- &#1053;&#1072;&#1081;&#1076;&#1077;&#1085;&#1072; -->
            <xsl:with-param name="one">
                <xsl:value-of select="hh:trl('vacancySearchResults.found0')"/>
            </xsl:with-param>
            <!-- &#1053;&#1072;&#1081;&#1076;&#1077;&#1085;&#1086; -->
            <xsl:with-param name="some">
                <xsl:value-of select="hh:trl('vacancySearchResults.found1')"/>
            </xsl:with-param>
            <!-- &#1053;&#1072;&#1081;&#1076;&#1077;&#1085;&#1086; -->
            <xsl:with-param name="many">
                <xsl:value-of select="hh:trl('vacancySearchResults.found1')"/>
            </xsl:with-param>
            <!-- &#1053;&#1072;&#1081;&#1076;&#1077;&#1085;&#1086; -->
            <xsl:with-param name="zero">
                <xsl:value-of select="hh:trl('vacancySearchResults.found1')"/>
            </xsl:with-param>
            <xsl:with-param name="with-num" select="false()"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*|@*" mode="conversion-vacancy">
        <xsl:apply-templates select="." mode="conversion">
            <xsl:with-param name="num" select="."/>
            <!-- &#1074;&#1072;&#1082;&#1072;&#1085;&#1089;&#1080;&#1103; -->
            <xsl:with-param name="one">
                <xsl:value-of select="hh:trl('vacancySearchResults.found.vacancyes0')"/>
            </xsl:with-param>
            <!-- &#1074;&#1072;&#1082;&#1072;&#1085;&#1089;&#1080;&#1081; -->
            <xsl:with-param name="some">
                <xsl:value-of select="hh:trl('vacancySearchResults.found.vacancyes2')"/>
            </xsl:with-param>
            <!-- &#1074;&#1072;&#1082;&#1072;&#1085;&#1089;&#1080;&#1080; -->
            <xsl:with-param name="many">
                <xsl:value-of select="hh:trl('vacancySearchResults.found.vacancyes1')"/>
            </xsl:with-param>
            <!-- &#1074;&#1072;&#1082;&#1072;&#1085;&#1089;&#1080;&#1081; -->
            <xsl:with-param name="zero">
                <xsl:value-of select="hh:trl('vacancySearchResults.found.vacancyes2')"/>
            </xsl:with-param>
            <xsl:with-param name="with-num" select="false()"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*" mode="conversion-view">
        <xsl:apply-templates select="." mode="conversion">
            <xsl:with-param name="num" select="."/>
            <!-- &#1087;&#1088;&#1086;&#1089;&#1084;&#1086;&#1090;&#1088; -->
            <xsl:with-param name="one">
                <xsl:value-of select="hh:trl('resumelist.views0')"/>
            </xsl:with-param>
            <!-- &#1087;&#1088;&#1086;&#1089;&#1084;&#1086;&#1090;&#1088;&#1086;&#1074; -->
            <xsl:with-param name="some">
                <xsl:value-of select="hh:trl('resumelist.views1')"/>
            </xsl:with-param>
            <!-- &#1087;&#1088;&#1086;&#1089;&#1084;&#1086;&#1090;&#1088;&#1072; -->
            <xsl:with-param name="many">
                <xsl:value-of select="hh:trl('resumelist.views2')"/>
            </xsl:with-param>
            <!-- &#1085;&#1077;&#1090; &#1087;&#1088;&#1086;&#1089;&#1084;&#1086;&#1090;&#1088;&#1086;&#1074; -->
            <xsl:with-param name="zero">
                <xsl:value-of select="hh:trl('resumelist.views1')"/><!--<xsl:value-of select="hh:trl('resumelist.views3')"/>-->
            </xsl:with-param>
            <xsl:with-param name="with-num" select="false()"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*|@*" mode="conversion-age">
        <xsl:apply-templates select="." mode="conversion">
            <xsl:with-param name="num" select="."/>
            <xsl:with-param name="one" select="hh:trl('age.one', $lang)"/>
            <xsl:with-param name="some" select="hh:trl('age.some', $lang)"/>
            <xsl:with-param name="many" select="hh:trl('age.many', $lang)"/>
            <xsl:with-param name="zero" select="hh:trl('age.zero', $lang)"/>
            <xsl:with-param name="with-num" select="true()"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*|@*" mode="conversion-new-view">
        <xsl:apply-templates select="." mode="conversion">
            <xsl:with-param name="num" select="."/>
            <!-- &#1085;&#1086;&#1074;&#1099;&#1081; -->
            <xsl:with-param name="one">
                <xsl:value-of select="hh:trl('resumelist.newviews1')"/>
            </xsl:with-param>
            <!-- &#1085;&#1086;&#1074;&#1099;&#1093; -->
            <xsl:with-param name="some">
                <xsl:value-of select="hh:trl('resumelist.newviews2')"/>
            </xsl:with-param>
            <!-- &#1085;&#1086;&#1074;&#1099;&#1093; -->
            <xsl:with-param name="many">
                <xsl:value-of select="hh:trl('resumelist.newviews2')"/>
            </xsl:with-param>
            <!-- &#1085;&#1086;&#1074;&#1099;&#1093; -->
            <xsl:with-param name="zero">
                <xsl:value-of select="hh:trl('resumelist.newviews2')"/>
            </xsl:with-param>
            <xsl:with-param name="with-num" select="false()"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template name="hh:trl"><!--some stuff--></xsl:template>

</xsl:stylesheet>