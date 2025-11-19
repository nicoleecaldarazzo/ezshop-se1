

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
| Accountant         | GUI for PC        |  PC                |
| Maintenance Service         | GUI for PC - Hardware        |  PC                |


# Functional and non functional requirements

## Functional Requirements

\<In the form DO SOMETHING, or VERB NOUN, describe high level capabilities of the system>

\<they match to high level use cases>

|  ID   | Description |
| :---: | :---------: |
|  FR1: Manage Payments| - Manage payment of certain amount given credit card number - Manage payment of certain amount given Apple Pay ID - Manage payment of certain amount given cash            |
|  FR2: Manage User| -Different interfaces for each user type - Authenticate User            |
| FR3: Support Maintenance| ?-Update firmware -Perform diagnostic            |
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
|  NFR1   | Efficiency                                   |   - Opening the software has to take less than 3 seconds - Time to login has to take less than 3 seconds - Processing transactions and propagate changes to the inventory has to take less than 5 seconds          | FR1- FR2- FR4- FR8          |
|  NFR2   | Security                                   | Role based access            |      FR2     |
|  NFR3   | Reliability                                   | - On the front end maximum of 1 defect per 2-3 months - Databases should be available 99% of the times           |  All Functions         |
|  NFR4   | Portability                                   | The software has to work even if the shop changes the computer            | All Functions          |
|  NFR5   | Usability                                   | Users should learn the system in less than 2 days            |   ?        |

# Table of rights

|  Actor   | FR1         | FR2 | FR3 | FR4 | FR5 | FR6 | FR7 | FR8 | FR9 | FR10 |
| :---:    | :---------: | :---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |
| Manager         |    *         |       *|*|*|*|*|*|*|*|*|
| Cashier         |     *        |       ||||||*||*|
| Accountant         |             |       ||||*|||||
| Supplier         |             |       |||*||||||
| Shop Assistant         |             |       ||*|||*||||
| Maintenance Service        |             |       |*||||||||
| Payment Service         |     *        |       ||||||*|||

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
|Support Maintenance          |Report and track technical issues with the system  |Main actor: System, Store Manager, Employees, Maintenance Service  employeeor or manager log a problem system records ??? and contact the maintenance service, marks it as resolved when fixed

## Use case diagram
![](doc/images/use_case.png)


### Use case 1, UC1

| Actors Involved  |                                                                      |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Manager is authenticated in the system = true|
|  Post condition  |New employee account exists in the system and is active; credentials have been generated and stored  |
| Nominal Scenario |The manager creates an account for a new employee by inserting personal data, role and permissions. System validates data and stores the new account.|
|     Variants     |V1: Manager edits an existing account instead of creating a new one.|
|    Exceptions    | E1: Inserted username already exists → system shows error and asks for a different username. E2: Mandatory data missing → system highlights missing fields and does not create the account. |

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
|     Actor's action                                        |  System action                                                            | FR needed |
| :------------:                                            | :------------------------------:                                          |:---:|
|Manager chooses “Create account”                           |Displays account creation form                                             | FR-ACC-1 |
|Manager fills required data (name, role, username, etc.)   |                                                                           |           |
|Manager submits the form                                   |Validates fields and uniqueness of username                                |FR-ACC-2 |
|                                                           |If data valid, creates user record with selected role and default password |FR-ACC-3 |
|                                                           |Shows confirmation and new credentials to the manager                      |FR-ACC-4|


##### Scenario 1.2
steps
|     Actor's action                                                                   |  System action                                                                                   | FR needed |
| :------------:                                                                       | :------------------------------:                                                                 |:---:      |
|Manager opens “Manage accounts” and selects an existing employee                      |System displays the employee’s current information (name, role, salary, status, etc.)             | FR-ACC-5  |
|Manager edits one or more fields (e.g., salary, role, personal data, account status)  |                                                                                                  |           |
|Manager clicks “Save changes”                                                         |System validates updated fields (format, allowed values, role constraints)                        |FR-ACC-6   |

##### Scenario 1.x

### Use case 2, UC2

| Actors Involved  |                                                                      |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |User is not authenticated; user account exists and is active|
|  Post condition  |User is authenticated, session is started, user role is known  |
| Nominal Scenario |The user enters credentials, the system verifies them and gives access depending on the user role.|
|     Variants     |V1: After a period of inactivity (e.g., 15–30 minutes), the system logs the user out automatically. V2: After successful login, the system redirects to different home screens depending on the role: For manager → management dashboard (reports, inventory, users, etc.) For employee → sales/checkout screen|
|    Exceptions    |E1: Wrong username or password → display error, remain on login page|

##### Scenario 2.1

steps
|     Actor's action                            |  System action                                          | FR needed |
| :------------:                                | :------------------------------:                        |:---:      |
|User opens login page                          |Shows login form                                         |FR-AUTH-1 |
|User enters username and password and submits  |Receives credentials                                     |           |
|                                               |Checks credentials against user database                 |FR-AUTH-2  |
|                                               |If valid, opens home page with menu based on role        |FR-AUTH-3  |
|                                               |If invalid, shows error message and logs failed attempt  |FR-AUTH-4 |


### Use case 3, UC3
| Actors Involved  |                                                                      |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |User is authenticated; product list exists|
|  Post condition  |Inventory quantities are updated (after sale, delivery, manual correction) |
| Nominal Scenario |User selects a product and modifies its stock (increase/decrease). System validates and updates the inventory.|
|     Variants     |V1: Automatic update triggered by a sale or return (no manual input).|
|    Exceptions    |E1: Quantity would become negative → system blocks operation and shows error.|

##### Scenario 3.1

steps
|     Actor's action                                      |  System action                                          | FR needed |
| :------------:                                          | :------------------------------:                        |:---:      |
|Manager chooses “Inventory” and selects a product        |Shows current stock for the product                      |FR-INV-1 |
|Manager enters adjustment (+/- quantity)                 |                                                         |           |
|Manager confirms change                                  |Checks that resulting quantity ≥ 0                       |FR-INV-2 |
|                                                         |Updates inventory and logs the change for both correction and after delivery     |FR-INV-3 |
|                                                         |Shows updated stock to the user                          |FR-INV-4 |
##### Scenario 3.2
steps
|     Actor's action                                             |  System action                                                            | FR needed |
| :------------:                                                 | :------------------------------:                                          |:---:      |
|(Cashier completes a sale using the “Process transaction” UC)   |System receives final list of sold products and quantities                 |FR-INV-5|
|                                                                |For each product, system calculates new stock = old stock − sold quantity  |FR-INV-6 |
|                                                                |Validates that stock does not fall below zero (after applying sale)        |FR-INV-7 |
|                                                                |Updates the inventory table and logs the automatic adjustment              |FR-INV-3 |
|                                                                |If new stock is below 10 → system generates a low-stock alert              |FR-INV-8|

### Use case 4, UC4 
| Actors Involved  |                                                                      |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Cashier is authenticated; customer’s items are selected; cart total > 0|
|  Post condition  |Sale is registered, payment status stored, inventory updated, receipt generated|
| Nominal Scenario |Cashier initiates checkout, chooses payment type, payment service |
|     Variants     |V1: Payment type = cash. V2: Payment type = card.|
|    Exceptions    |E1: Card payment refused → transaction cancelled or switched to cash. |

##### Scenario 4.1
steps
|     Actor's action                       |  System action                                                    | FR needed |
| :------------:                           | :------------------------------:                                  |:---:      |
|Cashier presses “Checkout”                |Shows payment options and order summary                            |FR-SALE-1  |
|Cashier selects “Card payment”            |Sends amount & transaction data to payment service                 |FR-SALE-2  |
|                                          |Receives authorization/denial from payment service                 |FR-SALE-3  |
|                                          |If authorized, stores sale, updates inventory and payment status   |FR-SALE-4  |
|                                          |Prints receipt and shows “Payment successful”                      |FR-SALE-5  |

##### Scenario 4.2
steps
|     Actor's action                                  |  System action                                                    | FR needed |
| :------------:                                      | :------------------------------:                                  |:---:      |
|Cashier selects “Cash payment”                       |System shows amount to collect and opens “cash received” field     |FR-SALE-6  |
|Cashier enters the amount received from customer     |                                                                   |         |
|Cashier confirms payment                             |System calculates change to return                                 |FR-SALE-7  |
|                                                     |System stores the sale, updates inventory and payment status (paid-cash)   |FR-SALE-4  |
|                                                     |Prints receipt and shows “Payment completed”                       |FR-SALE-5  |

##### Scenario 4.3
steps
|     Actor's action                                  |  System action                                                     | FR needed |
| :------------:                                      | :------------------------------:                                   |:---:      |
|Cashier selects “Card payment”                       |System sends amount & transaction details to payment service        |FR-SALE-2  |
|                                                     |Payment service returns denial (refused transaction)                |FR-SALE-3  |
|                                                     |System displays error: “Payment refused” with reason (if available) |FR-SALE-8  |
|Cashier chooses between retry or switch to Cash      |System goes back to payment options                                 |FR-SALE-9  |
|                                                     |No sales are stored, no inventory updated until successful payment  |FR-SALE-10 |



# Glossary

![](doc/images/glossary.png)
\<concepts must be used consistently all over the document, ex in use cases, requirements etc>

# System Design

The EZShop system is designed as a multi-tier application composed of:

Client layer (Front-end POS & Back-office UI)

Application layer (Backend services)

Integration layer (external services: payment, fiscal authority, email)

Data layer (relational database + logs)

# Hardware Software architecture

![](doc/images/hwandsw.png)
