# Project Estimation

Date:

Version:

# Estimation approach


# Estimate by size

###

|                                                                                                         | Estimate |
| ------------------------------------------------------------------------------------------------------- | -------- |
| NC = Estimated number of classes to be developed                                                        |   60       |
| A = Estimated average size per class, in LOC                                                            |     100 LOC     |
| S = Estimated size of project, in LOC (= NC \* A)                                                       |     6000 LOC     |
| E = Estimated effort, in person hours (here use productivity 10 LOC per person hour)                    |   600 Person hour       |
| C = Estimated cost, in euro (here use 1 person hour cost = 30 euro)                                     |    18000€       |
| Estimated calendar time, in calendar weeks (Assume team of 5 people, 8 hours per day, 5 days per week ) |   3 weeks     |

# Estimate by product decomposition

###

| component name                      | Estimated effort (person hours) |
| ----------------------------------- | ------------------------------- |
| Requirements document               | 70 ph                           |
| System & detailed design document   | 100 ph                           |
| Source code (backend + UI + DB)     | 310 ph                          |
| Test cases & test reports           | 90 ph                           |
| User & operations documentation     | 30 ph                           |
| **Total**                           | **600 ph**                      |

Estimated duration: **≈ 3 weeks** (team of 5 people, 8h/day, 5 days/week)


# Estimate by activity decomposition + Gantt chart

###


| Activity name                          | Estimated effort (person hours) |
|----------------------------------------|---------------------------------|
| Requirements elicitation & analysis    | 40 ph                           |
| Requirements document writing          | 30 ph                           |
| System architecture definition         | 35 ph                           |
| Detailed design (class & sequence)     | 65 ph                           |
| Database schema & repository design    | 20 ph                           |
| Implementation of domain classes       | 50 ph                           |
| Implementation of services/controllers | 90 ph                           |
| Integration with external services     | 70 ph                           |
| UI development (POS + manager UI)      | 80 ph                           |
| Testing (test cases + execution)       | 70 ph                           |
| Bug fixing & refactoring               | 30 ph                           |
| Deployment preparation & documentation | 20 ph                           |
| **TOTAL**                              | **600 ph**                      |




###

## Gantt chart

![](doc/images/gantt1.png)

Estimated duration: **≈ 3 weeks** (team of 5 people, 8h/day, 5 days/week)
# Summary




| Estimation method                         | Estimated effort (ph) | Estimated duration (calendar time, relative) |
|-------------------------------------------|------------------------|-------------------------------------|
| Estimate by size                          | 600 ph                 | 3 weeks                          |
| Estimate by product decomposition         | 600 ph                 | 3 weeks                          |
| Estimate by activity decomposition (Gantt)| 600 ph                 | 3 weeks                          |

