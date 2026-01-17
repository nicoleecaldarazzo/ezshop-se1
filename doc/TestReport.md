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
| test_post_products_201_created | ProductRoutes | API | BB / Eq. Partitioning |
| test_post_products_201_created_without_optional_fields | ProductRoutes | API | BB / Boundary |
| test_post_products_400_invalid_barcode | ProductRoutes | API | BB / Eq. Partitioning |
| test_post_products_400_negative_price | ProductRoutes | API | BB / Boundary |
| test_post_products_400_negative_quantity | ProductRoutes | API | BB / Boundary |
| test_post_products_409_duplicate_barcode | ProductRoutes | API | BB / Eq. Partitioning |
| test_put_product_201_updated | ProductRoutes | API | BB / Eq. Partitioning |
| test_put_product_201_partial_update | ProductRoutes | API | BB / Boundary |
| test_put_product_422_invalid_input | ProductRoutes | API | BB / Boundary |
| test_put_product_404_not_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_put_product_409_barcode_conflict | ProductRoutes | API | BB / Eq. Partitioning |
| test_put_product_409_barcode_has_active_sales | ProductRoutes | API | BB / Eq. Partitioning |
| test_create_product_ok | ProductService | Unit | WB / Statement Coverage |
| test_create_product_invalid_barcode_raises | ProductService | Unit | WB / Branch Coverage |
| test_create_product_invalid_price_raises | ProductService | Unit | WB / Branch Coverage |
| test_create_product_negative_quantity_raises | ProductService | Unit | WB / Branch Coverage |
| test_create_product_invalid_position_raises | ProductService | Unit | WB / Branch Coverage |
| test_create_product_without_optional_fields | ProductService | Unit | WB / Branch Coverage |
| test_create_product_repo_failure_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_ok | ProductService | Unit | WB / Statement Coverage |
| test_update_product_invalid_id_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_barcode_with_active_sales_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_invalid_new_barcode_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_repo_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_triggers_quantity_validation | ProductService | Unit | WB / Branch Coverage |
| test_update_product_triggers_position_validation | ProductService | Unit | WB / Branch Coverage |
| test_create_product_success | ProductRepository | Unit | WB / Statement Coverage |
| test_create_product_duplicate_barcode_raises | ProductRepository | Unit | WB / Branch Coverage |
| test_create_product_sets_all_fields | ProductRepository | Unit | WB / Statement Coverage |
| test_update_product_success | ProductRepository | Unit | WB / Statement Coverage |
| test_update_product_not_found_returns_none | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_barcode_conflict_raises | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_same_barcode_allowed | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_partial_update | ProductRepository | Unit | WB / Statement Coverage |
| test_update_product_quantity_field | ProductRepository | Unit | WB / Statement Coverage |
| test_create_product_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_update_product_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_delete_product_204_deleted | ProductRoutes | API | BB / Eq. Partitioning |
| test_delete_product_422_invalid_id | ProductRoutes | API | BB / Boundary |
| test_delete_product_404_not_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_delete_product_409_has_active_sales | ProductRoutes | API | BB / Eq. Partitioning |
| test_delete_product_409_has_active_orders | ProductRoutes | API | BB / Eq. Partitioning |
| test_delete_product_ok | ProductService | Unit | WB / Statement Coverage |
| test_delete_product_invalid_id_raises | ProductService | Unit | WB / Branch Coverage |
| test_delete_product_with_active_sales_raises | ProductService | Unit | WB / Branch Coverage |
| test_delete_product_with_active_orders_raises | ProductService | Unit | WB / Branch Coverage |
| test_delete_product_with_active_returns_raises | ProductService | Unit | WB / Branch Coverage |
| test_delete_product_with_multiple_conflicts_raises | ProductService | Unit | WB / Branch Coverage |
| test_delete_product_repo_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_delete_product_success | ProductRepository | Unit | WB / Statement Coverage |
| test_delete_product_not_found_returns_false | ProductRepository | Unit | WB / Branch Coverage |
| test_delete_product_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_get_products_200_list_of_products | ProductRoutes | API | BB / Eq. Partitioning |
| test_get_products_200_empty_list | ProductRoutes | API | BB / Boundary |
| test_list_products_empty | ProductService | Unit | WB / Branch Coverage |
| test_list_products_multiple | ProductService | Unit | WB / Statement Coverage |
| test_list_products_success | ProductRepository | Unit | WB / Statement Coverage |
| test_list_products_empty | ProductRepository | Unit | WB / Branch Coverage |
| test_list_products_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_get_products_search_200_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_get_products_search_200_no_results | ProductRoutes | API | BB / Boundary |
| test_get_products_search_422_missing_description | ProductRoutes | API | BB / Boundary |
| test_get_products_search_400_empty_description | ProductRoutes | API | BB / Boundary |
| test_get_product_by_barcode_200_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_get_product_by_barcode_422_invalid_format | ProductRoutes | API | BB / Boundary |
| test_get_product_by_barcode_404_not_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_get_product_200_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_get_product_422_invalid_id | ProductRoutes | API | BB / Boundary |
| test_get_product_404_not_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_get_product_ok | ProductService | Unit | WB / Statement Coverage |
| test_get_product_invalid_id_raises | ProductService | Unit | WB / Branch Coverage |
| test_get_product_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_get_product_by_barcode_ok | ProductService | Unit | WB / Statement Coverage |
| test_get_product_by_barcode_invalid_barcode_raises | ProductService | Unit | WB / Branch Coverage |
| test_get_product_by_barcode_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_search_products_ok | ProductService | Unit | WB / Statement Coverage |
| test_search_products_empty_description_raises | ProductService | Unit | WB / Branch Coverage |
| test_search_products_whitespace_only_raises | ProductService | Unit | WB / Branch Coverage |
| test_search_products_no_results | ProductService | Unit | WB / Branch Coverage |
| test_get_product_internal_method_found | ProductService | Unit | WB / Statement Coverage |
| test_get_product_internal_method_not_found | ProductService | Unit | WB / Branch Coverage |
| test_get_product_internal_method_invalid_id | ProductService | Unit | WB / Branch Coverage |
| test_get_product_by_id_found | ProductRepository | Unit | WB / Statement Coverage |
| test_get_product_by_id_not_found | ProductRepository | Unit | WB / Branch Coverage |
| test_get_product_by_barcode_found | ProductRepository | Unit | WB / Statement Coverage |
| test_get_product_by_barcode_not_found | ProductRepository | Unit | WB / Branch Coverage |
| test_search_products_by_description_found | ProductRepository | Unit | WB / Statement Coverage |
| test_search_products_by_description_no_results | ProductRepository | Unit | WB / Branch Coverage |
| test_get_product_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_get_product_by_barcode_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_search_products_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_patch_product_quantity_201_add_quantity | ProductRoutes | API | BB / Eq. Partitioning |
| test_patch_product_quantity_201_subtract_quantity | ProductRoutes | API | BB / Eq. Partitioning |
| test_patch_product_quantity_201_set_to_zero | ProductRoutes | API | BB / Boundary |
| test_patch_product_quantity_422_missing_query | ProductRoutes | API | BB / Boundary |
| test_patch_product_quantity_400_negative_result | ProductRoutes | API | BB / Boundary |
| test_patch_product_quantity_404_not_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_update_product_quantity_add_ok | ProductService | Unit | WB / Statement Coverage |
| test_update_product_quantity_subtract_ok | ProductService | Unit | WB / Statement Coverage |
| test_update_product_quantity_invalid_id_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_quantity_negative_result_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_quantity_repo_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_quantity_add_success | ProductRepository | Unit | WB / Statement Coverage |
| test_update_product_quantity_subtract_success | ProductRepository | Unit | WB / Statement Coverage |
| test_update_product_quantity_not_found_returns_none | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_quantity_negative_result_raises | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_quantity_to_zero | ProductRepository | Unit | WB / Boundary |
| test_update_product_quantity_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_patch_product_position_201_updated | ProductRoutes | API | BB / Eq. Partitioning |
| test_patch_product_position_201_clear_position | ProductRoutes | API | BB / Boundary |
| test_patch_product_position_422_missing_query | ProductRoutes | API | BB / Boundary |
| test_patch_product_position_400_invalid_format | ProductRoutes | API | BB / Eq. Partitioning |
| test_patch_product_position_404_not_found | ProductRoutes | API | BB / Eq. Partitioning |
| test_update_product_position_ok | ProductService | Unit | WB / Statement Coverage |
| test_update_product_position_invalid_format_raises | ProductService | Unit | WB / Branch Coverage |
| test_update_product_position_to_null | ProductService | Unit | WB / Branch Coverage |
| test_update_product_position_empty_string | ProductService | Unit | WB / Branch Coverage |
| test_update_position_repo_not_found_raises | ProductService | Unit | WB / Branch Coverage |
| test_validate_position_empty_string_does_not_raise | ProductService | Unit | WB / Branch Coverage |
| test_update_product_position_success | ProductRepository | Unit | WB / Statement Coverage |
| test_update_product_position_not_found_returns_none | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_position_to_none | ProductRepository | Unit | WB / Branch Coverage |
| test_update_product_position_calls_service | ProductController | Unit | WB / Statement Coverage |
| test_post_payfor_201_created | OrderRoutes | API | BB / Eq. Partitioning |
| test_post_payfor_400_invalid_barcode | OrderRoutes | API | BB / Eq. Partitioning |
| test_post_payfor_400_negative_quantity | OrderRoutes | API | BB / Boundary |
| test_post_payfor_404_product_not_found | OrderRoutes | API | BB / Eq. Partitioning |
| test_create_and_pay_order_success | OrderService | Unit | WB / Statement Coverage |
| test_create_and_pay_order_invalid_barcode_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_and_pay_order_invalid_quantity_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_and_pay_order_product_not_found_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_and_pay_order_repo_returns_none_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_and_pay_order_success | OrderRepository | Unit | WB / Statement Coverage |
| test_create_and_pay_order_uses_product_price | OrderRepository | Unit | WB / Statement Coverage |
| test_create_and_pay_order_product_not_found_raises | OrderRepository | Unit | WB / Branch Coverage |
| test_create_and_pay_order_calls_service | OrderController | Unit | WB / Statement Coverage |
| test_post_orders_201_created | OrderRoutes | API | BB / Eq. Partitioning |
| test_post_orders_400_invalid_barcode | OrderRoutes | API | BB / Eq. Partitioning |
| test_post_orders_400_empty_barcode | OrderRoutes | API | BB / Boundary |
| test_post_orders_400_negative_quantity | OrderRoutes | API | BB / Boundary |
| test_post_orders_400_zero_quantity | OrderRoutes | API | BB / Boundary |
| test_post_orders_400_negative_price | OrderRoutes | API | BB / Boundary |
| test_post_orders_400_zero_price | OrderRoutes | API | BB / Boundary |
| test_post_orders_404_product_not_found | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_pay_order_201_success | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_pay_order_422_invalid_id | OrderRoutes | API | BB / Boundary |
| test_patch_pay_order_404_not_found | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_pay_order_409_wrong_status | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_pay_order_409_already_completed | OrderRoutes | API | BB / Eq. Partitioning |
| test_create_order_success | OrderService | Unit | WB / Statement Coverage |
| test_create_order_invalid_barcode_empty_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_invalid_barcode_whitespace_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_invalid_barcode_format_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_invalid_barcode_non_numeric_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_zero_quantity_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_negative_quantity_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_zero_price_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_negative_price_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_product_not_found_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_repo_returns_none_raises | OrderService | Unit | WB / Branch Coverage |
| test_pay_order_success | OrderService | Unit | WB / Statement Coverage |
| test_pay_order_invalid_id_raises | OrderService | Unit | WB / Branch Coverage |
| test_pay_order_not_found_raises | OrderService | Unit | WB / Branch Coverage |
| test_pay_order_wrong_status_raises | OrderService | Unit | WB / Branch Coverage |
| test_pay_order_repo_returns_none_raises | OrderService | Unit | WB / Branch Coverage |
| test_create_order_success | OrderRepository | Unit | WB / Statement Coverage |
| test_create_order_product_not_found_raises | OrderRepository | Unit | WB / Branch Coverage |
| test_create_order_sets_issued_status | OrderRepository | Unit | WB / Statement Coverage |
| test_pay_order_success | OrderRepository | Unit | WB / Statement Coverage |
| test_pay_order_not_found_returns_none | OrderRepository | Unit | WB / Branch Coverage |
| test_pay_order_not_issued_raises_conflict | OrderRepository | Unit | WB / Branch Coverage |
| test_pay_order_completed_raises_conflict | OrderRepository | Unit | WB / Branch Coverage |
| test_create_order_calls_service | OrderController | Unit | WB / Statement Coverage |
| test_pay_order_calls_service | OrderController | Unit | WB / Statement Coverage |
| test_patch_arrival_201_success | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_arrival_422_invalid_id | OrderRoutes | API | BB / Boundary |
| test_patch_arrival_404_not_found | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_arrival_409_wrong_status | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_arrival_409_already_completed | OrderRoutes | API | BB / Eq. Partitioning |
| test_patch_arrival_404_product_not_found | OrderRoutes | API | BB / Eq. Partitioning |
| test_record_order_arrival_success | OrderService | Unit | WB / Statement Coverage |
| test_record_order_arrival_invalid_id_raises | OrderService | Unit | WB / Branch Coverage |
| test_record_order_arrival_not_found_raises | OrderService | Unit | WB / Branch Coverage |
| test_record_order_arrival_wrong_status_raises | OrderService | Unit | WB / Branch Coverage |
| test_record_order_arrival_product_not_found_raises | OrderService | Unit | WB / Branch Coverage |
| test_record_order_arrival_repo_returns_none_raises | OrderService | Unit | WB / Branch Coverage |
| test_record_order_arrival_success | OrderRepository | Unit | WB / Statement Coverage |
| test_record_order_arrival_order_not_found_returns_none | OrderRepository | Unit | WB / Branch Coverage |
| test_record_order_arrival_not_paid_raises_conflict | OrderRepository | Unit | WB / Branch Coverage |
| test_record_order_arrival_already_completed_raises_conflict | OrderRepository | Unit | WB / Branch Coverage |
| test_record_order_arrival_product_not_found_raises | OrderRepository | Unit | WB / Branch Coverage |
| test_record_order_arrival_updates_product_quantity_correctly | OrderRepository | Unit | WB / Statement Coverage |
| test_record_order_arrival_calls_service | OrderController | Unit | WB / Statement Coverage |
| test_get_orders_200_list_of_orders | OrderRoutes | API | BB / Eq. Partitioning |
| test_get_orders_200_empty_list | OrderRoutes | API | BB / Boundary |
| test_list_orders_success | OrderService | Unit | WB / Statement Coverage |
| test_list_orders_empty | OrderService | Unit | WB / Branch Coverage |
| test_list_orders_success | OrderRepository | Unit | WB / Statement Coverage |
| test_list_orders_empty | OrderRepository | Unit | WB / Branch Coverage |
| test_get_order_by_id_found | OrderRepository | Unit | WB / Statement Coverage |
| test_get_order_by_id_not_found | OrderRepository | Unit | WB / Branch Coverage |
| test_list_orders_calls_service | OrderController | Unit | WB / Statement Coverage |
| test_get_order_helper_invalid_id_raises | OrderService | Unit | WB / Branch Coverage |
| test_get_order_helper_negative_id_raises | OrderService | Unit | WB / Branch Coverage |
| test_get_order_helper_not_found_raises | OrderService | Unit | WB / Branch Coverage |
| test_get_order_helper_success | OrderService | Unit | WB / Statement Coverage |
| test_has_active_sales_true | ProductRepository | Unit | WB / Statement Coverage |
| test_has_active_sales_false | ProductRepository | Unit | WB / Branch Coverage |
| test_has_active_orders_true | ProductRepository | Unit | WB / Statement Coverage |
| test_has_active_orders_false | ProductRepository | Unit | WB / Branch Coverage |
| test_has_active_returns_true | ProductRepository | Unit | WB / Statement Coverage |
| test_has_active_returns_false | ProductRepository | Unit | WB / Branch Coverage |
| test_get_session_returns_existing_session | ProductRepository | Unit | WB / Statement Coverage |
| test_get_session_creates_new_session_if_none | ProductRepository | Unit | WB / Branch Coverage |
| test_get_session_returns_existing_session | OrderRepository | Unit | WB / Statement Coverage |
| test_get_session_creates_new_session_if_none | OrderRepository | Unit | WB / Branch Coverage |

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
| FR3.1 Define a new product type, or modify an existing product type | test_post_products_201_created, test_post_products_201_created_without_optional_fields, test_post_products_400_invalid_barcode, test_post_products_400_negative_price, test_post_products_400_negative_quantity, test_post_products_409_duplicate_barcode, test_put_product_201_updated, test_put_product_201_partial_update, test_put_product_422_invalid_input, test_put_product_404_not_found, test_put_product_409_barcode_conflict, test_put_product_409_barcode_has_active_sales, test_create_product_ok, test_create_product_invalid_barcode_raises, test_create_product_invalid_price_raises, test_create_product_negative_quantity_raises, test_create_product_invalid_position_raises, test_create_product_without_optional_fields, test_create_product_repo_failure_raises, test_update_product_ok, test_update_product_invalid_id_raises, test_update_product_not_found_raises, test_update_product_barcode_with_active_sales_raises, test_update_product_invalid_new_barcode_raises, test_update_product_repo_not_found_raises, test_update_product_triggers_quantity_validation, test_update_product_triggers_position_validation, test_create_product_success, test_create_product_duplicate_barcode_raises, test_create_product_sets_all_fields, test_update_product_success, test_update_product_not_found_returns_none, test_update_product_barcode_conflict_raises, test_update_product_same_barcode_allowed, test_update_product_partial_update, test_update_product_quantity_field, test_create_product_calls_service, test_update_product_calls_service |
| FR3.2 Delete a product type | test_delete_product_204_deleted, test_delete_product_422_invalid_id, test_delete_product_404_not_found, test_delete_product_409_has_active_sales, test_delete_product_409_has_active_orders, test_delete_product_ok, test_delete_product_invalid_id_raises, test_delete_product_with_active_sales_raises, test_delete_product_with_active_orders_raises, test_delete_product_with_active_returns_raises, test_delete_product_with_multiple_conflicts_raises, test_delete_product_repo_not_found_raises, test_delete_product_success, test_delete_product_not_found_returns_false, test_delete_product_calls_service |
| FR3.3 List all products types | test_get_products_200_list_of_products, test_get_products_200_empty_list, test_list_products_empty, test_list_products_multiple, test_list_products_success, test_list_products_empty, test_list_products_calls_service |
| FR3.4 Search a product type (by bar code, by description) | test_get_products_search_200_found, test_get_products_search_200_no_results, test_get_products_search_422_missing_description, test_get_products_search_400_empty_description, test_get_product_by_barcode_200_found, test_get_product_by_barcode_422_invalid_format, test_get_product_by_barcode_404_not_found, test_get_product_200_found, test_get_product_422_invalid_id, test_get_product_404_not_found, test_get_product_ok, test_get_product_invalid_id_raises, test_get_product_not_found_raises, test_get_product_by_barcode_ok, test_get_product_by_barcode_invalid_barcode_raises, test_get_product_by_barcode_not_found_raises, test_search_products_ok, test_search_products_empty_description_raises, test_search_products_whitespace_only_raises, test_search_products_no_results, test_get_product_internal_method_found, test_get_product_internal_method_not_found, test_get_product_internal_method_invalid_id, test_get_product_by_id_found, test_get_product_by_id_not_found, test_get_product_by_barcode_found, test_get_product_by_barcode_not_found, test_search_products_by_description_found, test_search_products_by_description_no_results, test_get_product_calls_service, test_get_product_by_barcode_calls_service, test_search_products_calls_service |
| FR4.1 Modify quantity available for a product type | test_patch_product_quantity_201_add_quantity, test_patch_product_quantity_201_subtract_quantity, test_patch_product_quantity_201_set_to_zero, test_patch_product_quantity_422_missing_query, test_patch_product_quantity_400_negative_result, test_patch_product_quantity_404_not_found, test_update_product_quantity_add_ok, test_update_product_quantity_subtract_ok, test_update_product_quantity_invalid_id_raises, test_update_product_quantity_negative_result_raises, test_update_quantity_repo_not_found_raises, test_update_product_quantity_add_success, test_update_product_quantity_subtract_success, test_update_product_quantity_not_found_returns_none, test_update_product_quantity_negative_result_raises, test_update_product_quantity_to_zero, test_update_product_quantity_calls_service |
| FR4.2 Modify position for a product type | test_patch_product_position_201_updated, test_patch_product_position_201_clear_position, test_patch_product_position_422_missing_query, test_patch_product_position_400_invalid_format, test_patch_product_position_404_not_found, test_update_product_position_ok, test_update_product_position_invalid_format_raises, test_update_product_position_to_null, test_update_product_position_empty_string, test_update_position_repo_not_found_raises, test_validate_position_empty_string_does_not_raise, test_update_product_position_success, test_update_product_position_not_found_returns_none, test_update_product_position_to_none, test_update_product_position_calls_service |
| FR4.4 Send and pay an order for a product type | test_post_payfor_201_created, test_post_payfor_400_invalid_barcode, test_post_payfor_400_negative_quantity, test_post_payfor_404_product_not_found, test_create_and_pay_order_success, test_create_and_pay_order_invalid_barcode_raises, test_create_and_pay_order_invalid_quantity_raises, test_create_and_pay_order_product_not_found_raises, test_create_and_pay_order_repo_returns_none_raises, test_create_and_pay_order_success, test_create_and_pay_order_uses_product_price, test_create_and_pay_order_product_not_found_raises, test_create_and_pay_order_calls_service |
| FR4.5 Pay an issued reorder warning | test_post_orders_201_created, test_post_orders_400_invalid_barcode, test_post_orders_400_empty_barcode, test_post_orders_400_negative_quantity, test_post_orders_400_zero_quantity, test_post_orders_400_negative_price, test_post_orders_400_zero_price, test_post_orders_404_product_not_found, test_patch_pay_order_201_success, test_patch_pay_order_422_invalid_id, test_patch_pay_order_404_not_found, test_patch_pay_order_409_wrong_status, test_patch_pay_order_409_already_completed, test_create_order_success, test_create_order_invalid_barcode_empty_raises, test_create_order_invalid_barcode_whitespace_raises, test_create_order_invalid_barcode_format_raises, test_create_order_invalid_barcode_non_numeric_raises, test_create_order_zero_quantity_raises, test_create_order_negative_quantity_raises, test_create_order_zero_price_raises, test_create_order_negative_price_raises, test_create_order_product_not_found_raises, test_create_order_repo_returns_none_raises, test_pay_order_success, test_pay_order_invalid_id_raises, test_pay_order_not_found_raises, test_pay_order_wrong_status_raises, test_pay_order_repo_returns_none_raises, test_create_order_success, test_create_order_product_not_found_raises, test_create_order_sets_issued_status, test_pay_order_success, test_pay_order_not_found_returns_none, test_pay_order_not_issued_raises_conflict, test_pay_order_completed_raises_conflict, test_create_order_calls_service, test_pay_order_calls_service |
| FR4.6 Record order arrival | test_patch_arrival_201_success, test_patch_arrival_422_invalid_id, test_patch_arrival_404_not_found, test_patch_arrival_409_wrong_status, test_patch_arrival_409_already_completed, test_patch_arrival_404_product_not_found, test_record_order_arrival_success, test_record_order_arrival_invalid_id_raises, test_record_order_arrival_not_found_raises, test_record_order_arrival_wrong_status_raises, test_record_order_arrival_product_not_found_raises, test_record_order_arrival_repo_returns_none_raises, test_record_order_arrival_success, test_record_order_arrival_order_not_found_returns_none, test_record_order_arrival_not_paid_raises_conflict, test_record_order_arrival_already_completed_raises_conflict, test_record_order_arrival_product_not_found_raises, test_record_order_arrival_updates_product_quantity_correctly, test_record_order_arrival_calls_service |
| FR4.7 List all orders (issued, payed, completed) | test_get_orders_200_list_of_orders, test_get_orders_200_empty_list, test_list_orders_success, test_list_orders_empty, test_list_orders_success, test_list_orders_empty, test_get_order_by_id_found, test_get_order_by_id_not_found, test_list_orders_calls_service |

## Coverage white box

Report here the screenshot of coverage values obtained with PyTest
