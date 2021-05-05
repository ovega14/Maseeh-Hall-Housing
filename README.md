# Maseeh-Hall-Housing-Points
This repository contains the new scripts I wrote and used to update the Maseeh Hall dormitory currency on a semesterly basis for use in the house rooming lottery. This will describe the uses of the scripts as well as the functions and subtleties therein. 

#
**Residency Points**
The most passive and trivial way to earn housing points in Maseeh is by simply living there. All residents who complete a semester lived in Maseeh Hall receive *20 points per semester lived*. Residents receive these points near the end of each semester for which they gain them, during which time the housing points are being calculated and updated.

#
**Senior Points**
In Maseeh Hall, recall that rising seniors are awarded an *extra 40 housing points*. This stipulation exists consitutionally as a means to ensure that incoming Seniors have the strongest chance of being awarded single rooms (should they preference those). 

#
**Lex's Law**
Lex's Law, devised and implemented originally in [year], is a tool meant to prioritize seniority in a linear fashion, in congruence with the senior points provision. The law and its provisoins are as follows:
- todotodo
- todotodo

#
**Government Points**
Members of the house's student government are 'salaried' in the sense that, they, too, in addition to whatever points they may receive vis-a-vis the above qualifiers, are awarded additional points each semester that they successfully serve a term. The exact point provisions (per semester) are enumerated below:
- President: 40 
- Vice-President: 40
- Treasurer: 40
- Member at Large: 40
- Secretary: 40
- Parliamentarian: 40
- First-Year Representative: 40
- Chief Justice: 30
- Associate Justice(s): [0,20] 

#
**Extra Considerations**
We want to take all of the unique elements from a residents kerberos list, meaning that if we join rosters, residents won't appear more than once if they live in Maseeh across multiple semesters. 
We also want to be able to locate residents if someone claims they are missing (hence received no residency points), and determine easily from which list they were missing so that we can identify the root cause. Often, this might be a failure by Housing and Residential Services (HRS) to continually update resident rosters if/when people move in late.

#
**Instructions on how to process xlsx/csv files for proper use**
- When adding/copying newly added residents to the roster that HRS provides, ensure that you add them to the TOP of the spreadsheet for easy viewing. Additionally, it is helpful to either highlight or color the text differently from the others. 
