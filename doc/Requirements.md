

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

\<Define here Context diagram using UML use case diagram>

\<actors are a subset of stakeholders>

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

|  Actor   | FR1         | FRx |
| :---:    | :---------: | :---: |
| Manager         |             |       |
| Employee         |             |       |
| Supplier         |             |       |
| Inventory         |             |       |
| End Users (Cashier, Store Manager)         |             |       |

# Use case diagram and use cases

## Use case brief
|  UC name                    | Goal                                | Description                |
| :---:                       | :---------:                         | :---:                      |
|Create Account               |Create an account for each user      |Main Actor: Store Manager  Manager creates an account for each employee in the shop|
|Authenticate                 |Recognize the user                   |Main Actor: Store Manager, Employee Users authenticate to enter the software       |
|Modify Inventory             |Update the inventory                 |Main Actor: Store Manager, Employee, System  At the beinning the inventory has to bi filled with all the items availablein the shop by the workers. When the inventory is ready it will be automatically updated after each sell event. When a new order from the supplier has arrived , the employees need to manually update the inventory|
|Process Transaction          |Process the sale                     |Main Actor: Employee, Payment Service, System The employee initiate transaction,the payment service processes the payment,and the inventory is automatically updated  |
|Manage Orders to Supplier    |Replenish stock by ordering products |Main Actor: Store Manager : The System create order for products needed and generate an excell with list,after the manager checks if the list is correct, the system send the order to supplier                  |
| :---:         | :---------:                   | :---:                      |




## Use case diagram
@startuml EZShop_UseCases
' --- USE CASE DIAGRAMS ---

left to right direction

actor "Store Manager" as Manager
actor "Cashier" as Cashier
actor "Shop Asistant" as ShopAsistant
actor "Supplier" as Supplier
actor "Payment Service" as PaymentService
actor "Maintenance Service" as Maintenance
actor "System" as SystemActor
actor "Tax Authority" as TaxAuthority

rectangle "EZShop" {

  ' --- Use cases ---

  usecase "UC1 - Create Account" as UC1_CreateAccount
  usecase "UC2 - Authenticate" as UC2_Authenticate
  usecase "UC3 - Modify Inventory" as UC3_ModifyInventory
  usecase "UC4 - Process Transaction" as UC4_ProcessTransaction
  usecase "UC5 - Manage Orders\nto Supplier" as UC5_ManageOrders
  usecase "UC6 - Manage Returns\nand Exchanges" as UC6_ManageReturns
  usecase "UC7 - Support Accounting\n(Reports & Analytics)" as UC7_SupportAccounting
  usecase "UC8 - Manage Discounts" as UC8_ManageDiscounts
  usecase "UC9 - Manage Loyalty Points" as UC9_ManageLoyalty
  usecase "UC10 - Support Maintenance" as UC10_SupportMaintenance
  usecase "UC11 - Fiscal Transmission\n(Z-Report)" as UC11_FiscalTransmission

  ' --- Optional internal shared UCs (includes/extends) ---

  usecase "Handle Payment" as UC_Payment
  usecase "Generate Report" as UC_GenerateReport

}

' --- Actors to Use Cases ---

' Manager
Manager --> UC1_CreateAccount
Manager --> UC2_Authenticate
Manager --> UC3_ModifyInventory
Manager --> UC5_ManageOrders
Manager --> UC7_SupportAccounting
Manager --> UC8_ManageDiscounts
Manager --> UC10_SupportMaintenance

' Cashier
Cashier --> UC2_Authenticate
Cashier --> UC4_ProcessTransaction
Cashier --> UC6_ManageReturns
Cashier --> UC9_ManageLoyalty
Cashier --> UC10_SupportMaintenance

' ShopAsistant
ShopAsistant --> UC3_ModifyInventory
ShopAsistant --> UC2_Authenticate

' Supplier
Supplier --> UC5_ManageOrders : "receives POs,\nsends deliveries"

' Payment Service
PaymentService --> UC_Payment

' Maintenance
Maintenance --> UC10_SupportMaintenance

' System scheduled tasks
SystemActor --> UC11_FiscalTransmission
SystemActor --> UC7_SupportAccounting

' Tax Authority
TaxAuthority --> UC11_FiscalTransmission

' --- include / extend relations ---

UC4_ProcessTransaction --> UC_Payment : <<include>>
UC6_ManageReturns --> UC_Payment : <<include>>  : "refund"

UC7_SupportAccounting --> UC_GenerateReport : <<include>>

' Fiscal transmission uses reports (Z-report)
UC11_FiscalTransmission --> UC_GenerateReport : <<include>>

@enduml

\<define here UML Use case diagram UCD summarizing all use cases, and their relationships>

\<next describe here each use case in the UCD>

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
