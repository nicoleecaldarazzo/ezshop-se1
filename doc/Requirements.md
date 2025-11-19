

# Requirements Document - EZShop

Date: 24/10/2025

Version: 1.0.0

| Version number | Change |
| :------------: | :----: |
|                |        |

# Contents

- [Requirements Document - EzShop](#requirements-document)
- [Contents](#contents)
- [Informal description](#informal-description)
- [Business model](#business-model)
- [Stakeholders](#stakeholders)
- [Context Diagram and interfaces](#context-diagram-and-interfaces)
  - [Context Diagram](#context-diagram)
  - [Interfaces](#interfaces)
- [Functional and non functional requirements](#functional-and-non-functional-requirements)
  - [Functional Requirements](#functional-requirements)
  - [Non Functional Requirements](#non-functional-requirements)
- [Table of Rights](#table-of-rights)
- [Use case diagram and use cases](#use-case-diagram-and-use-cases)
  - [Use case diagram](#use-case-diagram)
    - [Use case 1, UC1](#use-case-1-uc1)
      - [Scenario 1.1](#scenario-11)
      - [Scenario 1.2](#scenario-12)
      - [Scenario 1.x](#scenario-1x)
    - [Use case 2, UC2](#use-case-2-uc2)
    - [Use case x, UCx](#use-case-x-ucx)
- [Glossary](#glossary)
- [System Design](#system-design)
- [Hardware Software architecture](#Hardware-software-architecture)

# Informal description

Small shops require a simple application to support the owner or manager. A small shop (ex a food shop) occupies 50-200 square meters, sells 500-2000 different item types, has two or a few more cash registers. 
EZShop is a software application to:
* manage sales
* manage inventory
* manage orders to suppliers
* support accounting

In the following describe the requirements of the EZShop application. 
You are free to define the application as you deem more useful and effective for the stakeholders. 
You are also free to modify the structure of the document when needed.
The document will be evaluated considering the typical defects in requirements (omissions, ambiguities, contradictions, etc), and syntactic errors in the formalism used (UML diagrams). 
Consider that the document should be delivered to another team (unknown to you)
 which will be in charge of designing and implementing the system. The design team should be able to proceed only with the information in the document.

# Business Model

# Stakeholders

| Stakeholder name | Description |
| :--------------: | :---------: |
| Store manager    | Manages the store and the employees, check the order to the supplier, decides what discount applies on items|
| Cashier          | Operates the register, performs daily transactions |
| Shop assistant   | Helps clients and organizes items in the store |
| Supplier         | Provides the item available in the shop |
| Payment Service  | Handles credit card/Apple Pay transactions via integrated terminals |
| Maintenance      | Provides Hardware/Software maintenance |
| Accountant       | Uses system reports to manage finances|
| Fiscal Authority | Receives daily sales summarie |




# Context Diagram and interfaces

## Context Diagram
![](doc/images/context_diagram.png)



## Interfaces

\<describe here each interface in the context diagram>


|   Actor          | Logical Interface | Physical Interface |
| :-------:        | :---------------: | :----------------: |
| Store Manager    | GUI for PC        |  PC                |
| Cashier          | GUI for PC        |  PC                |
| Shop Assistant   | GUI for PC        |  PC                |
| Supplier         | GUI for PC        |  PC                |
| Payment Service  | Credit Card Circuit API, Apple Pay API, Cash             |    Cash Register                |


# Functional and non functional requirements

## Functional Requirements

\<In the form DO SOMETHING, or VERB NOUN, describe high level capabilities of the system>

\<they match to high level use cases>

|  ID   | Description |
| :---: | :---------: |
|  FR1: Manage Payments| - Manage payment of certain amount given credit card number - Manage payment of certain amount given Apple Pay ID - Manage payment of certain amount given cash            |
|  FR2: Manage User| -Different interfaces for each user type - Authenticate User            |
| FR3: Support Maintenance| -Update firmware -Perform diagnostic            |
| FR4: Manage Inventory| - Check the availability of items - Update the availability of items -Update the list of items needed if we are running out of an item          |
| FR5: Manage Order| Prepare the order in which the type and amount of items we need from the supplier is specified            |
| FR6: Support Accounting| Create daily, weekly, monthly report of sales            |
| FR7: Manage Catalogue| Create a table with item and their price            |
| FR8: Manage Returns and Exchanges| -Update stock -Refound customer            |
| FR9: Manage Discounts|-The manager defines discount percentage and dates for selected products -The manager can edit the discount             |
| FR10: Manage Loyalty Points| -Give one point for every 1 euro spent -Give a 10 euros product for free at the customer when he arrives at 100 points            |

## Non Functional Requirements

\<Describe constraints on functional requirements>

|   ID    | Type (efficiency, reliability, ..) | Description | Refers to |
| :-----: | :--------------------------------: | :---------: | :-------: |
|  NFR1   | Efficiency                                   |   - Opening the software has to take less than 3 seconds - Time to login has to take less than 3 seconds - Processing transactions and propagate changes to the inventory has to take less than 5 seconds          |           |
|  NFR2   | Security                                   | Role based access            |           |
|  NFR3   | Reliability                                   | ?            |           |
|  NFR4   | Portability                                   | The software has to work even if the shop changes the computer            |           |
|  NFR5   | Usability                                   | Cashier should learn the system in less than 2 days            |           |

# Table of rights

|  Actor   | FR1         | FR2 | FR3 | FR4 | FR5 | FR6 | FR7 | FR8 | FR9 | FR10 |
| :---:    | :---------: | :---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |
| Manager         |    *         |       *|*|*|*|*|*|*|*|*|
| Cashier         |     *        |       ||||||*|||
| Accountant         |             |       ||||*|||||
| Supplier         |             |       |||*||||||
| Inventory         |             |       ||*|||||||
| Maintenance         |             |       |*||||||||

# Use case diagram and use cases

## Use case brief
|  UC name                    | Goal                                | Description                |
| :---:                       | :---------:                                       | :---:                      |
|Create Account               |Create an account for each user                    |Main Actor: Store Manager  Manager creates an account for each employee in the shop|
|Authenticate                 |Recognize the user                                 |Main Actor: Store Manager, Employee Users authenticate to enter the software       |
|Modify Inventory             |Update the inventory                               |Main Actor: Store Manager, Employee, System  At the beinning the inventory has to bi filled with all the items availablein the shop by the workers. When the inventory is ready it will be automatically updated after each sell event. When a new order from the supplier has arrived , the employees need to manually update the inventory|
|Process Transaction          |Process the sale                                   |Main Actor: Employee, Payment Service, System The employee initiate transaction,the payment service processes the payment,and the inventory is automatically updated  |
|Manage Orders to Supplier    |Replenish stock by ordering products               |Main Actor: Store Manager : The System create order for products needed and generate an excel with list,after the manager checks if the list is correct, the system send the order to supplier                  |
|Manage Returns and Exchanges |Handle product Returns or item changes after save  |Main Actor: Employees, Payment Service  Register Returned items, update inventory accordingly and manage Payback with payment service     |
|Support Accounting           |Provide financial data                             |Main Actor: System  create a dail - weekly - monthly report of saves        |
|Manage Discounts             |Configure and apply saves promotions               |Main Actor: Store Manager,System
|Manage Loyalty Points        |Reward costumers with points and free items        |Main Actor: Store Manager  Manager creates an account for each employee in the shop|
|Support Maintenance          |Report and track technical issues with the system  |Main actor: System, Store Manager, Employees, Maintenance Service  employeeor or manager log a problem 

## Use case diagram
![](doc/images/use_case.png)


### Use case 1, UC1

| Actors Involved  |                                                                      |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   | \<Boolean expression, must evaluate to true before the UC can start> |
|  Post condition  |  \<Boolean expression, must evaluate to true after UC is finished>   |
| Nominal Scenario |         \<Textual description of actions executed by the UC>         |
|     Variants     |                      \<other normal executions>                      |
|    Exceptions    |                        \<exceptions, errors >                        |

##### Scenario 1.1

\<describe here scenarios instances of UC1>

\<a scenario is a sequence of steps that corresponds to a particular execution of one use case>

\<a scenario is a more formal description of a story>

\<only relevant scenarios should be described>

|  Scenario 1.1  |                                                                            |
| :------------: | :------------------------------------------------------------------------: |
|  Precondition  | \<Boolean expression, must evaluate to true before the scenario can start> |
| Post condition |  \<Boolean expression, must evaluate to true after scenario is finished>   |


Steps

|     Actor's action      |  System action                                                                    | FR needed |
| :------------: | :------------------------------------------------------------------------: |:---:|
|               |                                                                 |  |
|   |  |  |
##### Scenario 1.2

##### Scenario 1.x

### Use case 2, UC2

..

### Use case x, UCx

..

# Glossary

\<use UML class diagram to define important terms, or concepts in the domain of the application, and their relationships>

\<concepts must be used consistently all over the document, ex in use cases, requirements etc>

# System Design

\<describe here system design>

\<must be consistent with Context diagram>

# Hardware Software architecture

\<describe here the hardware software architecture using UML deployment diagram >
