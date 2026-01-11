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

## Coverage white box

Report here the screenshot of coverage values obtained with PyTest
