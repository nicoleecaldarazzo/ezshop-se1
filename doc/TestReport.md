# Test Report

<The goal of this document is to explain how the application was tested, detailing how the test cases were defined and what they cover>

# Contents

- [Test Report](#test-report)
- [Contents](#contents)
- [Dependency graph](#dependency-graph)
- [Integration approach](#integration-approach)
- [Tests](#tests)
- [Coverage](#coverage)
  - [Coverage of FR](#coverage-of-fr)
  - [Coverage white box](#coverage-white-box)

# Dependency graph

     <report the here the dependency graph of EzShop>

# Integration approach

    <Write here the integration sequence you adopted, in general terms (top down, bottom up, mixed) and as sequence

    (ex: step1: unit A, step 2: unit A+B, step 3: unit A+B+C, etc)>

    <Some steps may  correspond to unit testing (ex step1 in ex above)>

    <One step will  correspond to API testing >

# Tests

<in the table below list the test cases defined For each test report the object tested, the test level (API, integration, unit) and the technique used to define the test case (BB/ eq partitioning, BB/ boundary, WB/ statement coverage, etc)> <split the table if needed>

| Test case name | Object(s) tested | Test level | Technique used |
| :------------: | :--------------: | :--------: | :------------: |
| test_create_user_route_success | UserRoutes | API | BB / Eq. Partitioning |
| test_create_user_missing_password | UserRoutes | API | BB / Boundary |
| test_get_user_not_found | UserRoutes | API | BB / Eq. Partitioning |
| test_create_user_empty_password | UserRoutes | API | BB / Boundary |
| test_create_user_empty_type | UserRoutes | API | BB / Boundary |
| test_get_token_success | AuthController | Unit | WB / Statement Coverage |
| test_get_token_user_not_found | AuthController | Unit | WB / Branch Coverage |
| test_get_token_wrong_password | AuthController | Unit | WB / Branch Coverage |
| test_create_user_success | UserController | Unit | WB / Statement Coverage |
|     test_create_customer_success[admin, manager, cashier]     |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|       test_create_customer_bad_request[invalid payloads]      |   CustomerRoutes   |     API     |       BB / Boundary + Eq. Partitioning       |
|              test_create_customer_unauthenticated             |   CustomerRoutes   |     API     |             BB / Boundary (auth)             |
|     test_update_customer_success[admin, manager, cashier]     |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|     test_update_customer_invalid_payload[invalid payloads]    |   CustomerRoutes   |     API     |                 BB / Boundary                |
|                 test_update_customer_not_found                |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|     test_delete_customer_success[admin, manager, cashier]     |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|                 test_delete_customer_not_found                |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|    test_get_customer_by_id_success[admin, manager, cashier]   |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|             test_get_customer_invalid_id[abc, -1]             |   CustomerRoutes   |     API     |                 BB / Boundary                |
|      test_list_customers_success[admin, manager, cashier]     |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|   test_create_customer_card_success[admin, manager, cashier]  |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|           test_create_customer_card_unauthenticated           |   CustomerRoutes   |     API     |             BB / Boundary (auth)             |
| test_attach_card_to_customer_success[admin, manager, cashier] |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|                   test_attach_card_not_found                  |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|               test_attach_card_already_attached               |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|      test_modify_card_points_add[admin, manager, cashier]     |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|    test_modify_card_points_remove[admin, manager, cashier]    |   CustomerRoutes   |     API     |             BB / Eq. Partitioning            |
|              test_modify_card_points_insufficient             |   CustomerRoutes   |     API     |      BB / Boundary (insufficient points)     |
|                    test_customer_lifecycle                    |   CustomerRoutes   | Integration |       Scenario-based (End-to-End flow)       |
|             test_create_customer_with_card_success            |   CustomerRoutes   | Integration | Scenario-based (customer + card association) |
|           test_post_customers_201_created_with_card           |   CustomerRoutes   | Integration |             BB / Eq. Partitioning            |
|              test_patch_cards_insufficient_points             |   CustomerRoutes   | Integration |                 BB / Boundary                |
|               test_create_customer_calls_service              | CustomerController |     Unit    |            WB / Statement Coverage           |
|                 test_create_card_calls_service                | CustomerController |     Unit    |            WB / Statement Coverage           |
|                 test_attach_card_calls_service                | CustomerController |     Unit    |            WB / Statement Coverage           |
|                 test_create_customer_conflict                 | CustomerRepository |     Unit    |             WB / Branch Coverage             |
|                   test_create_card_conflict                   | CustomerRepository |     Unit    |             WB / Branch Coverage             |
|                test_update_card_points_success                | CustomerRepository |     Unit    |            WB / Statement Coverage           |
|       test_create_customer_invalid_id_raises_bad_request      |   CustomerService  |     Unit    |             WB / Branch Coverage             |
|    test_create_customer_with_existing_card_raises_conflict    |   CustomerService  |     Unit    |             WB / Branch Coverage             |
|       test_update_card_points_insufficient_points_raises      |   CustomerService  |     Unit    |             WB / Branch Coverage             |


# Coverage

## Coverage of FR

<Report in the following table the coverage of functional requirements and scenarios(from official requirements) >

| Functional Requirement or scenario | Test(s) |
| :--------------------------------: | :-----: |
| Scenario 1.1 | test_create_user_route_success, test_create_user_success |
| FR-ACC-2 | test_create_user_missing_password, test_create_user_empty_password, test_create_user_empty_type |
| FR-ACC-3 | test_create_user_route_success, test_create_user_success |
| Scenario 1.2 | test_get_user_not_found |
| FR-ACC-5 | test_get_user_not_found |
| Scenario 2.1 | test_get_token_success, test_get_token_user_not_found, test_get_token_wrong_password |
| FR-AUTH-2 | test_get_token_success, test_get_token_user_not_found, test_get_token_wrong_password |
| FR-AUTH-3 | test_get_token_success |
| FR-AUTH-4 | test_get_token_user_not_found, test_get_token_wrong_password |
|    FR5.1 Define or modify a customer    | test_create_customer_success[admin, manager, cashier], test_create_customer_bad_request[invalid payloads], test_update_customer_success[admin, manager, cashier], test_update_customer_invalid_payload[invalid payloads], test_update_customer_not_found |
|         FR5.2 Delete a customer         |                                                                                   test_delete_customer_success[admin, manager, cashier], test_delete_customer_not_found                                                                                  |
|         FR5.3 Search a customer         |                                                               test_get_customer_by_id_success[admin, manager, cashier], test_get_customer_invalid_id[abc, -1], test_get_customer_not_found                                                               |
|         FR5.4 List all customers        |                                                                                test_list_customers_success[admin, manager, cashier], test_list_customers_includes_created                                                                                |
|       FR5.5 Create a loyalty card       |                                                                           test_create_customer_card_success[admin, manager, cashier], test_create_customer_card_unauthenticated                                                                          |
| FR5.6 Attach loyalty card to a customer |                                             test_attach_card_to_customer_success[admin, manager, cashier], test_attach_card_customer_not_found, test_attach_card_not_found, test_attach_card_already_attached                                            |
|  FR5.7 Modify points on a loyalty card  |                                  test_modify_card_points_add[admin, manager, cashier], test_modify_card_points_remove[admin, manager, cashier], test_modify_card_points_insufficient, test_modify_card_points_not_found                                  |

## Coverage white box

Report here the screenshot of coverage values obtained with PyTest
