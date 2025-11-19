# Project Estimation

Date:

Version:

# Estimation approach

Consider the EZShop project as described in your requirements document, assume that you are going to develop the project INDEPENDENT of the deadlines of the course, and from scratch

# Estimate by size

###

|                                                                                                         | Estimate |
| ------------------------------------------------------------------------------------------------------- | -------- |
| NC = Estimated number of classes to be developed                                                        |   45       |
| A = Estimated average size per class, in LOC                                                            |     100 LOC     |
| S = Estimated size of project, in LOC (= NC \* A)                                                       |     4500 LOC     |
| E = Estimated effort, in person hours (here use productivity 10 LOC per person hour)                    |   450 Person hour       |
| C = Estimated cost, in euro (here use 1 person hour cost = 30 euro)                                     |    13500€       |
| Estimated calendar time, in calendar weeks (Assume team of 5 people, 8 hours per day, 5 days per week ) |    2.25 weeks (~11 working days)      |

# Estimate by product decomposition

###

| component name                      | Estimated effort (person hours) |
| ----------------------------------- | ------------------------------- |
| Requirements document               | 70 ph                           |
| System & detailed design document   | 90 ph                           |
| Source code (backend + UI + DB)     | 200 ph                          |
| Test cases & test reports           | 70 ph                           |
| User & operations documentation     | 20 ph                           |
| **Total**                           | **450 ph**                      |

Estimated duration: **≈ 2.25 weeks** (team of 5 people, 8h/day, 5 days/week)


# Estimate by activity decomposition + Gantt chart

###
step 1: activities (WBS), step 2 Gantt chart

| Activity name                          | Estimated effort (person hours) |
|----------------------------------------|---------------------------------|
| Requirements elicitation & analysis    | 40 ph                           |
| Requirements document writing          | 30 ph                           |
| System architecture definition         | 30 ph                           |
| Detailed design (class & sequence)     | 60 ph                           |
| Database schema & repository design    | 20 ph                           |
| Implementation of domain classes       | 60 ph                           |
| Implementation of services/controllers | 80 ph                           |
| Integration with external services     | 30 ph                           |
| UI development (POS + manager UI)      | 30 ph                           |
| Testing (test cases + execution)       | 60 ph                           |
| Bug fixing & refactoring               | 40 ph                           |
| Deployment preparation & documentation | 20 ph                           |
| **TOTAL**                              | **450 ph**                      |




###

## Gantt chart
Insert here Gantt chart

Estimated duration: (calendar time)

# Summary

Report here the results of the three estimation approaches. The estimates may differ. Discuss here the possible reasons for the difference


| Estimation method                         | Estimated effort (ph) | Estimated duration (calendar time, relative) |
|-------------------------------------------|------------------------|-------------------------------------|
| Estimate by size                          | 450 ph                 | 2.25 weeks                          |
| Estimate by product decomposition         | 450 ph                 | 2.25 weeks                          |
| Estimate by activity decomposition (Gantt)| 450 ph                 | 2.25 weeks                          |

