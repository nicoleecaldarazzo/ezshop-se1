

# Requirements Document - EZShop

Date: 23/11/2025

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
| Fiscal Authority | Receives daily sales summaries via Fiscal Device (telematic recorder) |




# Context Diagram and interfaces

## Context Diagram
![](doc/images/context_diagram.png)



## Interfaces



|   Actor          | Logical Interface | Physical Interface |
| :-------:        | :---------------: | :----------------: |
| Store Manager    | GUI for PC        |  PC              |
| Cashier          | GUI POS        |  Cashier station with PC + barcode scanner + receipt printer + card/NFC terminal            |
| Shop Assistant   | GUI P0S        |  PC                |
| Supplier         | GUI for PC        |  PC                |
| Payment Service  | Credit Card Circuit API, Apple Pay API, Cash             |    Internet network (HTTPS) + card terminals provided by the provider                |
| Accountant         | GUI for PC        |  PC              |
| Maintenance Service         | GUI for PC, Development Interface (Code & Deployment Access)      |  PC/remote access               |
| Fiscal Authority| Communication protocol with the Telematic Recorder        | Telematic Recorder connected to the network|




# Functional and non functional requirements

## Functional Requirements


|  ID   | Description |
| :---: | :---------: |
|  FR1: Manage Payments| - Manage payment of certain amount given credit card number - Manage payment of certain amount given Apple Pay ID - Manage payment of certain amount given cash            |
|  FR2: Manage User| -Different interfaces for each user type - Authenticate User            |
| FR3: Support Maintenance|  -Report technical issues done by users  -Perform diagnostic done by maintenance service     |
| FR4: Manage Inventory| - Check the availability of items - Update the availability of items -Update the list of items needed if we are running out of an item          |
| FR5: Manage Order| Prepare the order in which the type and amount of items we need from the supplier is specified            |
| FR6: Support Accounting| Create daily, weekly, monthly report of sales            |
| FR7: Manage Catalogue| Create a table with item and their price            |
| FR8: Manage Returns and Exchanges| -Update stock -Refound customer            |
| FR9: Manage Discounts|-The manager defines discount percentage and dates for selected products -The manager can edit the discount             |
| FR10: Manage Loyalty Points| -Give one point for every 1 euro spent -Give a 10 euros product for free at the customer when he arrives at 100 points            |
| FR11: Manage Hardware Integration |- Initialize and detect connected peripherals (scanner, POS printer, card terminal, electronic cash register) - Receive barcodes from the scanner and add them to the cart during a sale - Communicate with the card terminal to initiate and verify electronic payments - Send sale data to the electronic cash register for receipt issuance - Manage connection errors or peripheral malfunctions |

## Non Functional Requirements

|   ID    | Type (efficiency, reliability, ..) | Description | Refers to |
| :-----: | :--------------------------------: | :---------: | :-------: |
|  NFR1   | Efficiency                                   |   - Opening the software has to take less than 3 seconds - Time to login has to take less than 3 seconds - Processing transactions and propagate changes to the inventory has to take less than 5 seconds          | FR1- FR2- FR4- FR8          |
|  NFR2   | Security                                   | Role based access            |      FR2     |
|  NFR3   | Reliability                                   | - On the front end maximum of 1 defect per 2-3 months - Databases should be available 99% of the times           |  All Functions         |
|  NFR4   | Portability                                   | The software has to work even if the shop changes the computer            | All Functions          |
|  NFR5   | Usability                                   | Users should learn the system in less than 2 days            |   All functions        |

# Table of rights

| Actor              | FR1 | FR2 | FR3 | FR4 | FR5 | FR6 | FR7 | FR8 | FR9 | FR10 | FR11 |
|--------------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:----:|:----:|
| Manager            |  y  |  y  |  y  |  y  |  y  |  y  |  y  |  y  |  y  |  y   |  n  |
| Cashier            |  y  |  n   |  y   |  n   | n    |   n  |  n   |  y  |  n   |    n  | n   |
| Accountant         |   n  |   n  |  y   |   n  |  n   |  y  |   n  |   n  |  n   |   n   |   n   |
| Supplier           |   n  |  n   |  y   |  y  |   n  |  n   | n    |  n   |  n   |  n    |  n    |
| Shop Assistant     |   n  | n    | y    |  y  |  n   |  n   |  n   |  y  |  n   | n     |n   |
| Maintenance Service|  n   |  n   |  y  |   n  |  n   | n    |  n   |  n   | n    |    n  |  y   |
| Payment Service    |  y  |   n  |   n  |   n  |   n  |   n  |   n  |  n   |   n  |  n    |   n   |


# Use case diagram and use cases

## Use case brief
|  UC name                    | Goal                                | Description                |
| :---:                       | :---------:                                       | :---:                      |
|Create Account               |Create an account for each user                    |Main Actor: Store Manager. Description: Manager creates an account for each employee in the shop|
|Authenticate                 |Recognize the user                                 |Main Actor: Store Manager, Employee. Description: users authenticate to enter the software       |
|Modify Inventory             |Update the inventory                               |Main Actor: Store Manager, Employee, System. Description: at the beinning the inventory has to bi filled with all the items availablein the shop by the workers. When the inventory is ready it will be automatically updated after each sell event. When a new order from the supplier has arrived , the employees need to manually update the inventory|
|Process Transaction          |Process the sale                                   |Main Actor: Employee, Payment Service, System. Description: the employee initiate transaction,the payment service processes the payment,and the inventory is automatically updated  |
|Manage Orders to Supplier    |Replenish stock by ordering products               |Main Actor: Store Manager. Description: The System create order for products needed and generate an excel with list,after the manager checks if the list is correct, the system send the order to supplier                  |
|Manage Returns and Exchanges |Handle product Returns or item changes after save  |Main Actor: Employees, Payment Service. Description: register Returned items, update inventory accordingly and manage Payback with payment service     |
|Support Accounting           |Provide financial data                             |Main Actor: System. Description: create a dail - weekly - monthly report of saves        |
|Manage Discounts             |Configure and apply saves promotions               |Main Actor: Store Manager,System.
|Manage Loyalty Points        |Reward costumers with points and free items        |Main Actor: Store Manager. Description: manager creates an account for each employee in the shop|
|Support Maintenance          |Report and track technical issues with the system  |Main actor: System, Store Manager, Employees, Maintenance Service. Description:  employeeor or manager log a problem system records ??? and contact the maintenance service, marks it as resolved when fixed

## Use case diagram
![](doc/images/use_case.png)


### Use case 1, UC1

| Actors Involved  | Store manager (primary)                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Manager is authenticated in the system = true|
|  Post condition  |New employee account exists in the system and is active; credentials have been generated and stored  |
| Nominal Scenario |The manager creates an account for a new employee by inserting personal data, role and permissions. System validates data and stores the new account.|
|     Variants     |V1: Manager edits an existing account instead of creating a new one.|
|    Exceptions    | E1: Inserted username already exists → system shows error and asks for a different username. E2: Mandatory data missing → system highlights missing fields and does not create the account. |

##### Scenario 1.1


|     Actor's action                                        |  System action                                                            | FR needed |
| :------------:                                            | :------------------------------:                                          |:---:|
|Manager chooses “Create account”                           |Displays account creation form                                             | FR-ACC-1 |
|Manager fills required data (name, role, username, etc.)   |                                                                           |           |
|Manager submits the form                                   |Validates fields and uniqueness of username                                |FR-ACC-2 |
|                                                           |If data valid, creates user record with selected role and default password |FR-ACC-3 |
|                                                           |Shows confirmation and new credentials to the manager                      |FR-ACC-4|


##### Scenario 1.2

|     Actor's action                                                                   |  System action                                                                                   | FR needed |
| :------------:                                                                       | :------------------------------:                                                                 |:---:      |
|Manager opens “Manage accounts” and selects an existing employee                      |System displays the employee’s current information (name, role, salary, status, etc.)             | FR-ACC-5  |
|Manager edits one or more fields (e.g., salary, role, personal data, account status)  |                                                                                                  |           |
|Manager clicks “Save changes”                                                         |System validates updated fields (format, allowed values, role constraints)                        |FR-ACC-6   |



### Use case 2, UC2

| Actors Involved  | Store manager, Employee                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |User is not authenticated; user account exists and is active|
|  Post condition  |User is authenticated, session is started, user role is known  |
| Nominal Scenario |The user enters credentials, the system verifies them and gives access depending on the user role.|
|     Variants     |V1: After a period of inactivity (e.g., 15–30 minutes), the system logs the user out automatically. V2: After successful login, the system redirects to different home screens depending on the role: For manager → management dashboard (reports, inventory, users, etc.) For employee → sales/checkout screen|
|    Exceptions    |E1: Wrong username or password → display error, remain on login page|

##### Scenario 2.1

|     Actor's action                            |  System action                                          | FR needed |
| :------------:                                | :------------------------------:                        |:---:      |
|User opens login page                          |Shows login form                                         |FR-AUTH-1 |
|User enters username and password and submits  |Receives credentials                                     |           |
|                                               |Checks credentials against user database                 |FR-AUTH-2  |
|                                               |If valid, opens home page with menu based on role        |FR-AUTH-3  |
|                                               |If invalid, shows error message and logs failed attempt  |FR-AUTH-4 |


### Use case 3, UC3
| Actors Involved  | Store manager, Employee, System                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |User is authenticated; product list exists|
|  Post condition  |Inventory quantities are updated (after sale, delivery, manual correction) |
| Nominal Scenario |User selects a product and modifies its stock (increase/decrease). System validates and updates the inventory.|
|     Variants     |V1: Automatic update triggered by a sale or return (no manual input).|
|    Exceptions    |E1: Quantity would become negative → system blocks operation and shows error.|

##### Scenario 3.1

|     Actor's action                                      |  System action                                          | FR needed |
| :------------:                                          | :------------------------------:                        |:---:      |
|Manager chooses “Inventory” and selects a product        |Shows current stock for the product                      |FR-INV-1 |
|Manager enters adjustment (+/- quantity)                 |                                                         |           |
|Manager confirms change                                  |Checks that resulting quantity ≥ 0                       |FR-INV-2 |
|                                                         |Updates inventory and logs the change for both correction and after delivery     |FR-INV-3 |
|                                                         |Shows updated stock to the user                          |FR-INV-4 |
##### Scenario 3.2

|     Actor's action                                             |  System action                                                            | FR needed |
| :------------:                                                 | :------------------------------:                                          |:---:      |
|(Cashier completes a sale using the “Process transaction” UC)   |System receives final list of sold products and quantities                 |FR-INV-5|
|                                                                |For each product, system calculates new stock = old stock − sold quantity  |FR-INV-6 |
|                                                                |Validates that stock does not fall below zero (after applying sale)        |FR-INV-7 |
|                                                                |Updates the inventory table and logs the automatic adjustment              |FR-INV-3 |
|                                                                |If new stock is below 10 → system generates a low-stock alert              |FR-INV-8|



### Use case 4, UC4 
| Actors Involved  | Employee (cashier), Payment service, System                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Cashier is authenticated; customer’s items are selected; cart total > 0|
|  Post condition  |Sale is registered, payment status stored, inventory updated, receipt generated|
| Nominal Scenario |The cashier scans the items using the barcode scanner, the system builds the cart, and the cashier selects the payment method (cash or card terminal). For electronic payments, EZShop sends the amount to the card terminal and awaits the outcome from the Payment Service. If the payment is successful, the system records the sale, updates the inventory, and sends the data to the Electronic Register for issuing the receipt. |
|     Variants     |V1: Payment type = cash. V2: Payment type = card.|
|    Exceptions    |E1: Card payment refused → transaction cancelled or switched to cash. |

##### Scenario 4.1
| Actor’s action                                | System action                                             | FR needed |
|-----------------------------------------------|-----------------------------------------------------------|-----------|
| Cashier brings the product close to the scanner | The system receives the barcode and identifies the item   | FR11      |
|                                               | The item is added to the cart with updated quantity       | FR4       |
|                                               | The updated total amount is displayed                     | FR4       |



##### Scenario 4.2

|     Actor's action                       |  System action                                                    | FR needed |
| :------------:                           | :------------------------------:                                  |:---:      |
|Cashier presses “Checkout”                |Shows payment options and order summary                            |FR-SALE-1  |
|Cashier selects “Card payment”            |Sends amount & transaction data to payment service                 |FR-SALE-2  |
|                                          |Receives authorization/denial from payment service                 |FR-SALE-3  |
|                                          |If authorized, stores sale, updates inventory and payment status   |FR-SALE-4  |
|                                          |Prints receipt and shows “Payment successful”                      |FR-SALE-5  |

##### Scenario 4.3

|     Actor's action                                  |  System action                                                    | FR needed |
| :------------:                                      | :------------------------------:                                  |:---:      |
|Cashier selects “Cash payment”                       |System shows amount to collect and opens “cash received” field     |FR-SALE-6  |
|Cashier enters the amount received from customer     |                                                                   |         |
|Cashier confirms payment                             |System calculates change to return                                 |FR-SALE-7  |
|                                                     |System stores the sale, updates inventory and payment status (paid-cash)   |FR-SALE-4  |
|                                                     |Prints receipt and shows “Payment completed”                       |FR-SALE-5  |

##### Scenario 4.4

|     Actor's action                                  |  System action                                                     | FR needed |
| :------------:                                      | :------------------------------:                                   |:---:      |
|Cashier selects “Card payment”                       |System sends amount & transaction details to payment service        |FR-SALE-2  |
|                                                     |Payment service returns denial (refused transaction)                |FR-SALE-3  |
|                                                     |System displays error: “Payment refused” with reason (if available) |FR-SALE-8  |
|Cashier chooses between retry or switch to Cash      |System goes back to payment options                                 |FR-SALE-9  |
|                                                     |No sales are stored, no inventory updated until successful payment  |FR-SALE-10 |

### Use case 5, UC5 
| Actors Involved  | Store manager, System, Supplier (external)                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Manager is authenticated; inventory levels are available|
|  Post condition  |Supplier orders are created and stored; optional export/email sent to supplier|
| Nominal Scenario |System generates order for products needed and generates order list, manager checks products to replenish, creates an order, and the order is sent to the supplier. |
|     Variants     |V1: Manager edits order list before sending.|
|    Exceptions    |E1 – Network/email/export failure→ System shows error: “Order could not be sent. Saved as pending.” E2 - Manager closes the order window before confirming →System discards the draft and no order is saved.|

##### Scenario 5.1

|     Actor's action                                                                  |  System action                                                                                             | FR needed |
| :------------:                                                                      | :------------------------------:                                                                           |:---:      |
|Manager opens “Supplier orders”                                                      |System automatically generates a low-stock order list based on inventory thresholds and displays past orders|FR-ORD-1|
|Manager reviews the auto-generated list and adjusts quantities or removes/adds items |Payment service returns denial (refused transaction)                                                        |FR-ORD-5 |
|Manager confirms the final order list                                                |System validates items (supplier assigned)                                                                  |FR-ORD-6 |
|                                                                                     |System generates the order document (PDF/Excel)                                                             |FR-ORD-2  |
|                                                                                     |System stores the order and marks it as “created”                                                           |FR-ORD-3 |
|Manager selects “Send to supplier”                                                   |Manager sends the order to the supplier (email/export); marks order as “sent”                               |FR-ORD-4  |

### Use case 6, UC6 
| Actors Involved  | Employee, Payment service                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Sale exists in the system; returned products are within store return policy|
|  Post condition  |Return or exchange registered, inventory updated, refund or difference managed|
| Nominal Scenario |Cashier searches original sale, selects items to return, system updates inventory and manages refund/exchange via payment service.|
|     Variants     |V1: Exchange with different products instead of refund.|
|    Exceptions    |E1: Sale not found → show error and cancel operation. E2: Return period expired → system informs cashier.|

##### Scenario 6.1

|     Actor's action                                  |  System action                                                      | FR needed |
| :------------:                                      | :------------------------------:                                    |:---:      |
|Cashier opens “Returns” and enters receipt ID        |Retrieves and shows sale detail                                      |FR-RET-1  |
|Cashier selects items and reason for return          |                                                                     |        |
|Cashier confirms refund on card                      |Sends refund request to payment service                              |FR-RET-2|
|                                                     |If approved, records negative sale/credit note and updates inventory |FR-RET-3|
|                                                     |Prints return receipt and shows confirmation                         |FR-RET-4|

##### Scenario 6.2

|     Actor's action                                  |  System action                                                      | FR needed |
| :------------:                                      | :------------------------------:                                    |:---:      |
|Cashier opens “Returns” and enters receipt ID        |Retrieves and shows sale detail                                      |FR-RET-1  |
|Cashier selects items and reason for return          |                                                                     |        |
|Cashier selects “Refund in cash”                     |System calculates total refund amount and displays it                |FR-RET-5|
|Cashier confirms refund                              |System records negative sale/credit note and updates inventory       |FR-RET-3|
|                                                     |System prints return receipt, logs cash refund and shows confirmation|FR-RET-4|

##### Scenario 6.3

|     Actor's action                                                                   |  System action                                                                                                                          | FR needed |
| :------------:                                                                       | :------------------------------:                                                                                                        |:---:      |
|Cashier opens “Returns” and enters receipt ID                                         |Retrieves and shows sale detail                                                                                                          |FR-RET-1  |
|Cashier selects items and reason for return                                           |                                                                                                                                         |        |
|Cashier chooses “Exchange” option                                                     |System calculates value of returned items                                                                                                |FR-RET-7|
|Cashier adds new products chosen by customer to the exchange cart                     |System shows price of new products and difference vs. returned value                                                                     |FR-RET-8|
|Cashier confirms exchange                                                             |System records return + new sale in one operation, updates inventory for both returned and new items, and customer must pay a difference |FR-RET-9|
|If difference to pay or refund exists, cashier completes payment/refund (cash or card)|System handles difference (via payment service or cash), prints exchange receipt and shows confirmation                                  |FR-RET-10|

##### Scenario 6.4

|     Actor's action                            |  System action                                                                                        | FR needed |
| :------------:                                | :------------------------------:                                                                      |:---:      |
|Cashier opens “Returns” and enters receipt ID  |Retrieves and shows sale detail                                                                        |FR-RET-1  |
|Cashier selects items and reason for return    |                                                                                                       |        |
|Cashier attempts to proceed with the return    |System checks store return rules (e.g., expired return period, non-returnable item, missing packaging) |FR-RET-11|
|                                               |System detects that the return violates store policy                                                   |FR-RET-12|
|                                               |System displays a clear message: “Refund not allowed: [Reason]”                                        |FR-RET-13|
|Cashier informs customer                       |System cancels the return flow and does not update inventory or sales records                          |FR-RET-14|

### Use case 7, UC7
| Actors Involved  |  System, Store manager                                                                    |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Sales, returns, payments data exist in the database|
|  Post condition  |Requested report (daily/weekly/monthly) is generated and available for download/view|
| Nominal Scenario |User selects a period and type of report; system aggregates data and produces accounting report.|
|     Variants     |V1: Export report to CSV/Excel.|
|    Exceptions    |E1: No data for selected period → system generates empty report with warning.|

##### Scenario 7.1

|     Actor's action                                                                                         |  System action                                                                                                              | FR needed |
| :------------:                                                                                             | :------------------------------:                                                                                            |:---:      |
|Manager chooses “Reports”                                                                                   |Shows report options (Daily / Weekly / Monthly) and date pickers                                                             |FR-REP-1|
|Manager selects report type (Daily, Weekly or Monthly) and the corresponding period (date / week / month)   |                                                                                                                             |        |
|Manager clicks “Generate”                                                                                   |System checks store return rules (e.g., expired return period, non-returnable item, missing packaging)                       |FR-REP-2|
|                                                                                                            |Displays the report summary (totals, taxes, number of transactions, etc.) and offers a download/export button (PDF/CSV/Excel)|FR-REP-3|
|(Variant V1) Manager clicks “Export”                                                                        |System exports the report in the chosen format (CSV/Excel)                                                                   |FR-REP-4|

##### Scenario 7.2

|     Actor's action                                                                                                  |  System action                                                                                          | FR needed |
| :------------:                                                                                                      | :------------------------------:                                                                        |:---:      |
|Manager chooses “Analytics / Graphs” in the Reports section                                                          |System shows available metrics (e.g., Revenue, Number of sales) and time range options (Monthly / Yearly)|FR-REP-5|
|Manager selects “Revenue” as metric and chooses “Monthly” or “Yearly” view plus the desired period (e.g., year 2025) |                                                                                                         |        |
|Manager clicks “Generate graph”                                                                                      |System aggregates revenue data per month (for yearly view) or per day/week (for monthly view)            |FR-REP-6|
|                                                                                                                     |System displays a graph showing revenues over time for the selected period                               |FR-REP-7|
|clicks “Export graph”                                                                                                |System exports graph as an image or PDF, or includes it in an exported report                            |FR-REP-8|

### Use case 8, UC8
| Actors Involved  | Store manager                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Manager is authenticated; product list exists|
|  Post condition  |New discount is stored and will be automatically applied during sales in its validity period|
| Nominal Scenario |Manager defines promotion (type, percentage, affected products, dates) and system saves and activates it.|
|     Variants     |V1: Discount limited to specific category/brand.|
|    Exceptions    |E1: No products or categories selected → system prevents saving and highlights missing fields|

##### Scenario 8.1

|     Actor's action                                                          |  System action                              | FR needed |
| :------------:                                                              | :------------------------------:            |:---:      |
|Manager opens “discount”                                                     |Shows current and past discounts             |FR-PROM-1|
|Manager clicks “New discount” and fills data (10%, start/end dates, products)|                                             |        |
|Manager saves discount                                                       |Validates dates and products                 |FR-PROM-2|
|                                                                             |Stores discount and schedules its activation |FR-PROM-3|

##### Scenario 8.2

|     Actor's action                                                                    |  System action                                                                       | FR needed |
| :------------:                                                                        | :------------------------------:                                                     |:---:      |
|Manager opens “Discounts” and selects an existing discount                             |System displays current discount details (percentage, dates, products)                |FR-PROM-4|
|Manager updates one or more fields (e.g., percentage, validity dates, list of products)|                                                                                      |        |
|Manager clicks “Save changes”                                                          |System validates updated fields (dates, percentage, overlapping rules)                |FR-PROM-5|
|                                                                                       |If valid, system updates the discount record and adjusts activation schedule if needed|FR-PROM-6|
|                                                                                       |System shows confirmation message: “Discount updated successfully”                    |FR-PROM-7|

### Use case 9, UC9
| Actors Involved  | System, Employee                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |Customer loyalty account exists; sale is in progress or just finished|
|  Post condition  |Customer points updated; free item redeemed if threshold reached|
| Nominal Scenario |Cashier identifies customer, system adds points based on purchase amount and allows redemption if customer has enough points.|
|     Variants     |V1: Customer creates loyalty account during sale.|
|    Exceptions    |E1: Customer not found → system offers to create new loyalty account.|

##### Scenario 9.1

|     Actor's action                      |  System action                              | FR needed |
| :------------:                          | :------------------------------:            |:---:      |
|Cashier identifies customer (card/phone) |Retrieves loyalty profile and current points |FR-LOY-1|
|After sale, cashier confirms “Add points”|Calculates points from sale amount           |FR-LOY-2|     
|Manager clicks “Save changes”            |Updates points balance                       |FR-LOY-3|

##### Scenario 9.2

|     Actor's action                                          |  System action                                                                         | FR needed |
| :------------:                                              | :------------------------------:                                                       |:---:      |
|Cashier identifies customer (phone number)                   |System retrieves loyalty profile and shows current points                               |FR-LOY-1|
|Cashier selects “Redeem free item”                           |System checks if the customer has enough points (e.g., ≥ 100)                           |FR-LOY-4|     
|Cashier selects the free item from the eligible product list |                                                                                        |        |
|Cashier confirms redemption                                  |System deducts the required points from customer’s balance                              |FR-LOY-5|     
|                                                             |System adds the free item to the sale with price = 0                                    |FR-LOY-6|     
|                                                             |System updates loyalty points and shows confirmation: “Free item redeemed successfully” |FR-LOY-7|     

### Use case 10, UC10
| Actors Involved  |  System, Store manager, Employees, Maintenance service (external)                                                                     |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   |User is authenticated; system is running but some component may have problems|
|  Post condition  |Incident is logged with status; optional notification sent to maintenance; status can be updated to resolved|
| Nominal Scenario |Employee or manager reports a technical issue; system records the incident.|
|     Variants     |V1: Manager adds extra notes or attachments (screenshots).|
|    Exceptions    |E1: Mandatory fields missing → incident not created and user is warned.|


##### Scenario 10.1

| Actor's action | System action | FR needed |
| :------------: | :------------------------------: |:---: |
| Employee/Manager opens “Maintenance” section | Shows a list/dashboard with the real-time status (Connected/Disconnected/Malfunctioning) of all connected hardware devices (Scanner, Printer, Card Terminal, RT, etc.) and software components. | FR-MNT-1 |
| Employee/Manager selects the malfunctioning device/component from the list | Opens a details view for the selected component, often showing basic diagnostic data. | |
| Employee/Manager confirms the issue (e.g., clicks "Report Issue") | Records the incident with status "open"; automatically attaches diagnostic data collected from the selected component. | FR-MNT-2 |
| | Notifies the Maintenance Service (via email/system notification) and includes diagnostic information. | FR-MNT-3 |
| Maintenance Service resolves the issue (out of system) | | |
| Maintenance Service (or Manager) later marks the incident as “resolved” in the system | System updates status to “resolved” and logs resolution date. | FR-MNT-4 |


### Use case 11, UC11 – Fiscal Transmission (Z-Report)

| Actors Involved  |                                                                      |
| :--------------: | :------------------------------------------------------------------: |
|   Precondition   | Daily sales exist; Fiscal Device (RT) is configured, connected and operational. |
|  Post condition  | The daily fiscal report (Z-Report) is generated and its transmission result (success/failure) is stored in the system. |
| Nominal Scenario | At the end of the day, the system collects all sales, prepares the fiscal data and sends it to the Fiscal Device (RT), which transmits the Z-Report to the Fiscal Authority. |
|     Variants     | V1: Manual transmission triggered by the Store Manager. |
|    Exceptions    | E1: RT not reachable → system logs failed attempt and notifies the manager. E2: Transmission rejected by Fiscal Authority → system records the error and marks the report as “not transmitted”. |

##### Scenario 11.1 – Automatic daily transmission

 
| Actor's action                                                   | System action                                                                 | FR needed   |
| :--------------------------------------------------------------: | :----------------------------------------------------------------------------:|:-----------:|
| (Time reaches the configured end-of-day closing time)           | Schedules the daily fiscal transmission                                      | FR-FISC-1   |
|                                                                  | Collects all sales of the day                                                | FR-FISC-2   |
|                                                                  | Prepares the fiscal payload according to RT protocol (e.g., XML/JSON)        | FR-FISC-3   |
|                                                                  | Sends the fiscal data to the Fiscal Device (RT)                              | FR-FISC-4   |
|                                                                  | Receives confirmation from RT that the Z-Report has been transmitted         | FR-FISC-5   |
|                                                                  | Stores the transmission result (success) and marks the day as “closed”       | FR-FISC-6   |

##### Scenario 11.2 – Manual retry after failed transmission

  
| Actor's action                                                   | System action                                                                 | FR needed   |
| :--------------------------------------------------------------: | :----------------------------------------------------------------------------:|:-----------:|
| Store Manager opens the “Fiscal report status” section           | Shows the list of recent fiscal transmissions with their status (OK/Failed)  | FR-FISC-7   |
| Store Manager selects a failed transmission and clicks “Retry”   | Reloads the stored fiscal payload for the selected day                        | FR-FISC-8   |
|                                                                  | Sends again the fiscal data to the Fiscal Device (RT)                         | FR-FISC-4   |
|                                                                  | Receives the new result (success or failure) from RT                          | FR-FISC-5   |
|                                                                  | Updates the status of the transmission (e.g., “Success” or “Failed again”)    | FR-FISC-6   |
|                                                                  | Logs the retry attempt with timestamp and result                              | FR-FISC-9   |



# Glossary

![](doc/images/glossary.png)
\<concepts must be used consistently all over the document, ex in use cases, requirements etc>

# System Design

The EZShop system is designed as a multi-tier application composed of:

Client layer (Front-end POS & Back-office UI)

Application layer (Backend services)

Integration layer (external services: payment, fiscal authority, email)

Data layer (relational database + logs).

The Client layer includes both the Back-office GUI (PC interface) and the POS interface used at the cash register. 
The POS interface interacts with hardware peripherals such as the barcode scanner, receipt printer, card/NFC terminal, and the telematic recorder (RT) through the Hardware Abstraction Layer in the Application layer.


# Hardware Software architecture

![](doc/images/hwandsw.png)

The POS terminal includes hardware peripherals such as a barcode scanner, receipt printer, cash drawer, card/NFC terminal and the Fiscal Device (RT). 
These peripherals communicate with the POS software through standard interfaces (USB, Bluetooth, LAN) and are managed by the application through dedicated drivers or provider SDKs.
The backend communicates with external services such as the Payment Service Provider and the Fiscal Authority.

