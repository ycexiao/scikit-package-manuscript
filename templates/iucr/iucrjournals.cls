{% raw %}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is the IUCr LaTeX2e class macro file iucrjournals.cls
% This work has been dedicated to the public domain
% License: CC0 1.0 Universal
% https://creativecommons.org/publicdomain/zero/1.0/
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Usage:
%  \documentclass{iucrjournals}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{iucrjournals}
\date{}

\LoadClass[11pt]{article}

\RequirePackage{lineno}
\linenumbers

\RequirePackage[parfill]{parskip}
\RequirePackage{setspace}
\onehalfspacing

\RequirePackage[margin=1in]{geometry}
\RequirePackage{float}
\RequirePackage{graphicx}

\RequirePackage{xcolor}
\RequirePackage{hyperref}
\hypersetup{colorlinks = true, allcolors = blue}

\RequirePackage{authblk}
\RequirePackage{booktabs}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% bibtex:
\RequirePackage{harvard}
% The following hack addresses a problem with bibtex failing when
% there is whitespace in a comma-separated list of labels passed as
% an argument to \cite - see
% http://tex.stackexchange.com/questions/4517/cite-that-tolerates-whitespace
%
\let\OLDcite\cite
\def\tok@scan#1{%
  \ifx#1\relax
    \let\tok@next\relax
  \else
    \edef\my@list{\my@list#1}%
    \let\tok@next\tok@scan
  \fi
  \tok@next
}
\newcommand{\@strip}[2]{%
  \def\my@list{}\tok@scan#2\relax\let#1\my@list}
\renewcommand{\cite}[1]{\@strip\@args{#1}\OLDcite\@args}

% The iucr.bst BibTeX bibliography style requires the harvard.sty package.
% IUCr citations are similar to the "dcu" style within harvard.sty, but
% require the conjunction to be changed to '&'; also abbreviated citations
% ('et al.') are always used.
\citationstyle{dcu}                              % (Doe, 1990; Soape, 1991)
\renewcommand{\harvardand}{\&}                   % (Doe & Soape, 1990)
\citationmode{abbr}                              % (Doe et al., 1990)
\bibliographystyle{iucr}
\renewcommand{\harvardurl}{\relax}               % incompatibility with hyperref
% \newblock is output by BibTeX to separate logical sections of a reference
% listing. It serves no useful purpose, and can cause extra spacing to
% intrude
\let\newblock\relax
% A complication of the preferred style of citation of IUCr journals
%  is that the volume number for Acta includes the section label,
%  which is NOT printed in bold; to accommodate this, \volbf is defined
%  and generated by iucr.bst. \volbf needs to test just the first character
%  of the volume number
\gdef\@A@{A}%
\gdef\@B@{B}%
\gdef\@C@{C}%
\gdef\@D@{D}%
\gdef\@E@{E}%
\gdef\@F@{F}%
\gdef\@J@{J}%
\gdef\@M@{M}%
\gdef\@S@{S}%
\newif\iffirst\firsttrue
\def\volbf#1{%
  {\firsttrue\v@lbf#1\end}%
}
\def\v@lbf#1{%
  \ifx#1\end
    \let\next=\relax%
  \else
    \let\next=\v@lbf\iffirst
    \def\t@st{#1}
    \if\t@st\@A@{\rmfamily{#1}}\else
      \if\t@st\@B@{\rmfamily{#1}}\else
        \if\t@st\@C@{\rmfamily{#1}}\else
          \if\t@st\@D@{\rmfamily{#1}}\else
            \if\t@st\@E@{\rmfamily{#1}}\else
              \if\t@st\@F@{\rmfamily{#1}}\else
              \textbf{#1}%
              \fi
            \fi
          \fi
        \fi
      \fi
    \fi%
    \firstfalse%
    \else
      {\textbf #1}%
    \fi%
  \fi
  \next%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% nice orcid links for use in author block:
\RequirePackage{tikz}
\usetikzlibrary{svg.path}

\IfFileExists{orcidlink.sty}%
{\RequirePackage{orcidlink}}%
{% orcidlink is post 2020, so include full code if sty file not available
\definecolor{orcidlogocol}{HTML}{A6CE39}
\tikzset{
  orcidlogo/.pic={
    \fill[orcidlogocol] svg{M256,128c0,70.7-57.3,128-128,128C57.3,256,0,198.7,0,128C0,57.3,57.3,0,128,0C198.7,0,256,57.3,256,128z};
    \fill[white] svg{M86.3,186.2H70.9V79.1h15.4v48.4V186.2z}
    svg{M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z}
 svg{M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1C84.2,46.7,88.7,51.3,88.7,56.8z};
  }
}
%% Reciprocal of the height of the svg whose source is above.  The
%% original generates a 256pt high graphic; this macro holds 1/256.
\newcommand{\@OrigHeightRecip}{0.00390625}
%% We will compute the current X height to make the logo the right height
\newlength{\@curXheight}

%% Prevent externalization of the ORCiD logo.
\newcommand{\@preventExternalization}{%
\ifcsname tikz@library@external@loaded\endcsname%
\tikzset{external/export next=false}\else\fi%
}

\newcommand{\orcidlogo}{%
\texorpdfstring{%
\setlength{\@curXheight}{\fontcharht\font`X}%
\XeTeXLinkBox{%
\@preventExternalization%
\begin{tikzpicture}[yscale=-\@OrigHeightRecip*\@curXheight,
xscale=\@OrigHeightRecip*\@curXheight,transform shape]
\pic{orcidlogo};
\end{tikzpicture}%
}}{}}
\DeclareRobustCommand\orcidlinkX[1]{\href{https://orcid.org/##1}{%
\orcidlogo}}
\newcommand{\orcidlink}[1]{\orcidlinkX{##1}}
}
\newcommand{\IUCrOrcidlink}[1]{\orcidlink{#1}\,}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% nice email links for use in author block (based on orcidlink):
\definecolor{IUCr@emaillogocol}{HTML}{AAAAAA}
\tikzset{
  IUCr@emaillogo/.pic={
    \fill[IUCr@emaillogocol]
    svg{M 0 11.755 v 66.489 h 90 V 11.755 H 0 z M 45 50.49 L 7.138 15.755 h 75.724 L 45 50.49 z M 33.099 45 L 4 71.695 V 18.304 L 33.099 45 z M 36.058 47.714 L 45 55.918 l 8.943 -8.204 l 28.919 26.53 H 7.138 L 36.058 47.714 z M 56.901 45 L 86 18.304 v 53.392 L 56.901 45 z};
  }
}
\definecolor{IUCr@cemaillogocol}{HTML}{0000FF}
\tikzset{
  IUCr@cemaillogo/.pic={
    \fill[IUCr@cemaillogocol]
    svg{M 0 11.755 v 66.489 h 90 V 11.755 H 0 z M 45 50.49 L 7.138 15.755 h 75.724 L 45 50.49 z M 33.099 45 L 4 71.695 V 18.304 L 33.099 45 z M 36.058 47.714 L 45 55.918 l 8.943 -8.204 l 28.919 26.53 H 7.138 L 36.058 47.714 z M 56.901 45 L 86 18.304 v 53.392 L 56.901 45 z};
  }
}
\newcommand{\IUCr@OrigHeightRecipE}{0.01400625}
\newlength{\IUCr@curXheightE}
\newcommand{\IUCr@preventExternalizationE}{%
\ifcsname tikz@library@external@loaded\endcsname%
\tikzset{external/export next=false}\else\fi%
}
\newcommand{\IUCr@emaillogo}{%
\texorpdfstring{%
\setlength{\IUCr@curXheightE}{\fontcharht\font`X}%
\XeTeXLinkBox{%
\IUCr@preventExternalizationE%
\begin{tikzpicture}[yscale=-\IUCr@OrigHeightRecipE*\IUCr@curXheightE,
xscale=\IUCr@OrigHeightRecipE*\IUCr@curXheightE,transform shape]
\pic{IUCr@emaillogo};
\end{tikzpicture}%
}}{}}
\newcommand{\IUCr@cemaillogo}{%
\texorpdfstring{%
\setlength{\IUCr@curXheightE}{\fontcharht\font`X}%
\XeTeXLinkBox{%
\IUCr@preventExternalizationE%
\begin{tikzpicture}[yscale=-\IUCr@OrigHeightRecipE*\IUCr@curXheightE,
xscale=\IUCr@OrigHeightRecipE*\IUCr@curXheightE,transform shape]
\pic{IUCr@cemaillogo};
\end{tikzpicture}%
}}{}}
\DeclareRobustCommand\IUCr@emaillinkX[1]{\href{mailto:#1}{%
\IUCr@emaillogo}}
\DeclareRobustCommand\IUCr@cemaillinkX[1]{\href{mailto:#1}{%
\IUCr@cemaillogo}}
\newcommand{\IUCrEmaillink}[1]{\,\IUCr@emaillinkX{#1}\,}
\newcommand{\IUCrCemaillink}[1]{\,\IUCr@cemaillinkX{#1}\,}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% author footnotes for use in author block
% (alternative to using \thanks or \footnote)

\newcounter{IUCr@aufnc}
\setcounter{IUCr@aufnc}{0}
\newcommand{\IUCr@storeaufn}[1]{\stepcounter{IUCr@aufnc}\global\expandafter\def\csname aufnX\theIUCr@aufnc\endcsname{#1}}
\newcommand{\IUCr@printaufn}[1]{\footnotesize\IUCr@fnsymbol{#1}\csname aufnX#1\endcsname\\}
\newcommand{\IUCr@printauthornotes}{%
\ifnum\theIUCr@aufnc>0
\begin{center}
\vskip-22pt
\newcounter{tmpIUCr@aufnc}
\setcounter{tmpIUCr@aufnc}{0}
\loop
\stepcounter{tmpIUCr@aufnc}
%\thetmpIUCr@aufnc
\IUCr@printaufn{\thetmpIUCr@aufnc}%
\addtocounter{IUCr@aufnc}{-1}
\ifnum\theIUCr@aufnc>0
\repeat
\end{center}
\bigskip
\fi
}
\newcommand{\IUCrAufn}[2][0]{%
% store the note as a new macro for later output using \IUCr@printauthornotes
\if0#1%
\IUCr@storeaufn{#2}%
%$^\theIUCr@aufnc$%
\IUCr@fnsymbol{\theIUCr@aufnc}\,%
\else% allows multiple footnote markers pointing to same text
% if the number is greater than \theIUCr@aufnc count, store as new?
\ifnum#1>\theIUCr@aufnc%
\IUCr@storeaufn{#2}%
\fi%
\IUCr@fnsymbol{\theIUCr@aufnc}\,%
\fi%
}

\newcommand{\IUCr@fnsymbol}[1]{%
\ifnum#1<6%
$^\IUCr@fnsymbolsingle{#1}$%
\else%
\newcount\@lrepeat
\@lrepeat=#1
\divide\@lrepeat by 5
%\the\@lrepeat
%modulo gives symbol number:
\newcount\@modsym
\@modsym=#1
\divide\@modsym by 5
\multiply\@modsym by 5
\multiply\@modsym by -1
\advance\@modsym by #1\relax
%\the\@modsym
$^{%
\IUCr@fnsymbolsingle{\@modsym}%
\loop
\IUCr@fnsymbolsingle{\@modsym}%
\advance\@lrepeat by -1
\ifnum\@lrepeat>0
\repeat
}$%
\fi%
}
\newcommand{\IUCr@fnsymbolsingle}[1]{%
  \ensuremath{%
    \ifcase#1% 0
    \or % 1
      \dagger
    \or % 2
      \ddagger
    \or % 3
      \mathsection
    \or % 4
      \mathparagraph
    \or \|
    \else % >= 6
      #1
    \fi
  }%
}

% print author notes after maketitle
\let\IUCr@maketitle=\maketitle
\def\maketitle{%
\IUCr@maketitle
\IUCr@printauthornotes
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% commands and formatting tweaks:

\let\origtitle\title
\renewcommand{\title}[1]{\origtitle{\textbf{#1}}}

\renewenvironment{abstract}
 {%\small
  \begin{center}
  \bfseries \abstractname\vspace{-.5em}\vspace{0pt}
  \end{center}
  \list{}{
    \setlength{\leftmargin}{1cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax}
 {\endlist\bigskip}

\newenvironment{synopsis}%
{%\small
  \begin{center}
  \bfseries Synopsis\vspace{-.5em}\vspace{0pt}
  \end{center}
  \list{}{
    \setlength{\leftmargin}{1cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax}
 {\endlist\bigskip}

\newcommand{\keywords}[1]{
 \begin{center}
 \small
  \list{}{
    \setlength{\leftmargin}{1cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax\textbf{Keywords:} #1\endlist\end{center}\bigskip}

\let\origaffil\affil
\def\affil#1#{\origaffilA{#1}}
\def\origaffilA#1#2{\origaffil#1{\footnotesize #2}}

\newenvironment{acknowledgements}%
{%\small
\bigskip
  %\begin{center}
  {\bfseries\Large Acknowledgements}\vspace{-.5em}\vspace{0pt}
  %\end{center}
  \list{}{
    \setlength{\leftmargin}{0cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax}
 {\endlist\medskip}

\newenvironment{funding}%
{%\small
\medskip
  %\begin{center}
  {\bfseries\Large Funding}\vspace{-.5em}\vspace{0pt}
  %\end{center}
  \list{}{
    \setlength{\leftmargin}{0cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax}
 {\endlist\medskip}

\newcommand{\ConflictsOfInterest}[1]{
 \begin{center}
 \small
  \list{}{
    \setlength{\leftmargin}{0cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax\textbf{Conflicts of interest:} #1\endlist\end{center}\medskip}

\newcommand{\DataAvailability}[1]{
 \begin{center}
 \small
  \list{}{
    \setlength{\leftmargin}{0cm}%
    \setlength{\rightmargin}{\leftmargin}%
  }%
  \item\relax\textbf{Data availability:} #1\endlist\end{center}\medskip}
{% endraw %}
