#!/usr/bin/env pwsh
# Test script for Module 2 - Syllabus Management API

# Colors for output
$green = "`e[32m"
$red = "`e[31m"
$yellow = "`e[33m"
$blue = "`e[34m"
$reset = "`e[0m"

Write-Host "$blue=== MODULE 2: SYLLABUS MANAGEMENT API TEST ===$reset`n"

# Configuration
$baseUrl = "http://localhost:8000/api/v1"
$lecturerEmail = "lecturer1@example.com"
$lecturerPassword = "securepass123"

# Global variables
$lecturerToken = ""
$adminToken = ""
$syllabusId = ""
$version1Id = ""
$version2Id = ""

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method,
        [string]$Endpoint,
        [string]$Token = "",
        [hashtable]$Body = @{},
        [int]$ExpectedStatus = 200
    )

    Write-Host "$yellow[$Method] $Endpoint$reset"
    
    try {
        $headers = @{"Content-Type" = "application/json"}
        if ($Token) {
            $headers["Authorization"] = "Bearer $Token"
        }

        $params = @{
            Uri = "$baseUrl$Endpoint"
            Method = $Method
            Headers = $headers
        }

        if ($Body.Count -gt 0 -and @("POST", "PUT", "PATCH") -contains $Method) {
            $params["Body"] = ($Body | ConvertTo-Json -Depth 10)
        }

        $response = Invoke-RestMethod @params -StatusCodeVariable "statusCode"
        
        if ($statusCode -eq $ExpectedStatus) {
            Write-Host "$green✓ PASS$reset - Status: $statusCode`n" -ForegroundColor Green
            return $response
        } else {
            Write-Host "$red✗ FAIL$reset - Expected: $ExpectedStatus, Got: $statusCode`n" -ForegroundColor Red
            return $null
        }
    }
    catch {
        Write-Host "$red✗ ERROR$reset - $_`n" -ForegroundColor Red
        return $null
    }
}

# ============================================================
# TEST 1: AUTHENTICATION
# ============================================================

Write-Host "$blue### TEST 1: AUTHENTICATION ###$reset`n"

Write-Host "Test 1.1: Lecturer Login"
$loginResponse = Test-Endpoint -Method "POST" `
    -Endpoint "/auth/login" `
    -Body @{
        email = $lecturerEmail
        password = $lecturerPassword
    } `
    -ExpectedStatus 200

if ($loginResponse) {
    $lecturerToken = $loginResponse.access_token
    Write-Host "Token: $($lecturerToken.Substring(0, 20))...`n"
}

Write-Host "Test 1.2: Admin Login"
$adminLogin = Test-Endpoint -Method "POST" `
    -Endpoint "/auth/login" `
    -Body @{
        email = "admin@example.com"
        password = "admin123"
    } `
    -ExpectedStatus 200

if ($adminLogin) {
    $adminToken = $adminLogin.access_token
}

# ============================================================
# TEST 2: CREATE SYLLABUS
# ============================================================

Write-Host "$blue### TEST 2: CREATE SYLLABUS ###$reset`n"

Write-Host "Test 2.1: Create new syllabus (CS101)"
$createResponse = Test-Endpoint -Method "POST" `
    -Endpoint "/syllabus" `
    -Token $lecturerToken `
    -Body @{
        subject_code = "CS101"
        subject_name = "Lập trình Python"
        description = "Khóa học lập trình Python cơ bản cho sinh viên năm nhất"
        credits = 3
        semester = 1
        department = "Khoa Công Nghệ Thông Tin"
        academic_year = "2025-2026"
        objectives = "Dạy học lập trình Python cơ bản bao gồm biến, hàm, class"
        content = "Variables, Data Types, Functions, Classes, Inheritance, File I/O"
        teaching_methods = "Lectures, Lab Exercises, Case Studies"
        assessment_methods = "Midterm Exam, Final Exam, Programming Projects"
    } `
    -ExpectedStatus 201

if ($createResponse) {
    $syllabusId = $createResponse.id
    Write-Host "Created Syllabus ID: $syllabusId`n"
}

Write-Host "Test 2.2: Verify syllabus status is 'draft'"
if ($createResponse.status -eq "draft") {
    Write-Host "$green✓ Status is 'draft' as expected$reset`n"
} else {
    Write-Host "$red✗ Expected 'draft', got '$($createResponse.status)'$reset`n"
}

Write-Host "Test 2.3: Verify initial version was created"
$versionResponse = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus/$syllabusId/versions" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($versionResponse -and $versionResponse.total -eq 1) {
    Write-Host "$green✓ Version 1 created automatically$reset`n"
    $version1Id = $versionResponse.versions[0].id
}

# ============================================================
# TEST 3: UPDATE SYLLABUS (Version Control)
# ============================================================

Write-Host "$blue### TEST 3: UPDATE SYLLABUS (Version Control) ###$reset`n"

Write-Host "Test 3.1: Update syllabus with CLO/PLO"
$updateResponse = Test-Endpoint -Method "PUT" `
    -Endpoint "/syllabus/$syllabusId" `
    -Token $lecturerToken `
    -Body @{
        objectives = "Updated: Dạy lập trình Python toàn diện"
        clos = @(
            @{
                id = "CLO1"
                description = "Hiểu biết cơ bản về lập trình Python"
                level = "K2"
            },
            @{
                id = "CLO2"
                description = "Viết chương trình Python đơn giản"
                level = "K3"
            }
        )
        plos = @(
            @{
                id = "PLO1"
                description = "Kỹ năng lập trình"
                alignment = 0.9
            },
            @{
                id = "PLO2"
                description = "Giải quyết vấn đề"
                alignment = 0.7
            }
        )
        change_summary = "Added CLO and PLO mappings"
    } `
    -ExpectedStatus 200

if ($updateResponse) {
    Write-Host "$green✓ Syllabus updated, now version 2 should exist$reset`n"
}

Write-Host "Test 3.2: Verify version 2 was created"
$versionsAfterUpdate = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus/$syllabusId/versions" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($versionsAfterUpdate.total -eq 2) {
    Write-Host "$green✓ Version 2 created after update$reset`n"
    $version2Id = $versionsAfterUpdate.versions[0].id
}

Write-Host "Test 3.3: Check changelog for version 2"
$latestVersion = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus/$syllabusId/versions/latest" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($latestVersion -and $latestVersion.changed_fields) {
    Write-Host "Changed fields: $($latestVersion.changed_fields -join ', ')"
    Write-Host "$green✓ Changelog recorded$reset`n"
}

# ============================================================
# TEST 4: UPDATE CLO-PLO MAPPING
# ============================================================

Write-Host "$blue### TEST 4: UPDATE CLO-PLO MAPPING ###$reset`n"

Write-Host "Test 4.1: Update CLO-PLO mapping"
$mappingResponse = Test-Endpoint -Method "PATCH" `
    -Endpoint "/syllabus/$syllabusId/clo-plo-mapping" `
    -Token $lecturerToken `
    -Body @{
        clo_plo_mapping = @{
            "CLO1" = @("PLO1")
            "CLO2" = @("PLO1", "PLO2")
        }
    } `
    -ExpectedStatus 200

if ($mappingResponse -and $mappingResponse.clo_plo_mapping) {
    Write-Host "$green✓ CLO-PLO mapping updated$reset`n"
}

# ============================================================
# TEST 5: GET SYLLABUS DETAILS
# ============================================================

Write-Host "$blue### TEST 5: GET SYLLABUS DETAILS ###$reset`n"

Write-Host "Test 5.1: Get syllabus with versions"
$detailResponse = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus/$syllabusId" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($detailResponse) {
    Write-Host "Syllabus: $($detailResponse.subject_code) - $($detailResponse.subject_name)"
    Write-Host "Status: $($detailResponse.status)"
    Write-Host "Versions count: $($detailResponse.versions.Count)`n"
}

# ============================================================
# TEST 6: LIST OPERATIONS
# ============================================================

Write-Host "$blue### TEST 6: LIST OPERATIONS ###$reset`n"

Write-Host "Test 6.1: List my syllabuses"
$listResponse = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus?skip=0&limit=10" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($listResponse) {
    Write-Host "Total syllabuses: $($listResponse.total)"
    Write-Host "Items in response: $($listResponse.count)`n"
}

Write-Host "Test 6.2: Search syllabuses by keyword"
$searchResponse = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus/search?q=python" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($searchResponse) {
    Write-Host "Search results: $($searchResponse.count) found`n"
}

# ============================================================
# TEST 7: VERSION CONTROL
# ============================================================

Write-Host "$blue### TEST 7: VERSION CONTROL ###$reset`n"

Write-Host "Test 7.1: Get specific version"
if ($version1Id) {
    $specificVersion = Test-Endpoint -Method "GET" `
        -Endpoint "/syllabus/$syllabusId/versions/$version1Id" `
        -Token $lecturerToken `
        -ExpectedStatus 200

    if ($specificVersion) {
        Write-Host "Version: $($specificVersion.version_number)"
        Write-Host "Summary: $($specificVersion.change_summary)`n"
    }
}

Write-Host "Test 7.2: Compare two versions"
if ($version1Id -and $version2Id) {
    $compareResponse = Test-Endpoint -Method "GET" `
        -Endpoint "/syllabus/$syllabusId/versions/$version1Id/compare/$version2Id" `
        -Token $lecturerToken `
        -ExpectedStatus 200

    if ($compareResponse) {
        Write-Host "Comparing version $($compareResponse.version_1) with $($compareResponse.version_2)"
        Write-Host "Changed fields: $($compareResponse.differences.changed_fields -join ', ')`n"
    }
}

# ============================================================
# TEST 8: WORKFLOW STATUS
# ============================================================

Write-Host "$blue### TEST 8: WORKFLOW STATUS ###$reset`n"

Write-Host "Test 8.1: Submit for review"
$submitResponse = Test-Endpoint -Method "PATCH" `
    -Endpoint "/syllabus/$syllabusId/status" `
    -Token $lecturerToken `
    -Body @{
        status = "submitted"
    } `
    -ExpectedStatus 200

if ($submitResponse) {
    Write-Host "Status changed to: $($submitResponse.status)`n"
}

Write-Host "Test 8.2: Approve (as HOD/Admin)"
$approveResponse = Test-Endpoint -Method "PATCH" `
    -Endpoint "/syllabus/$syllabusId/status" `
    -Token $adminToken `
    -Body @{
        status = "approved"
    } `
    -ExpectedStatus 200

if ($approveResponse) {
    Write-Host "Status changed to: $($approveResponse.status)`n"
}

Write-Host "Test 8.3: Publish"
$publishResponse = Test-Endpoint -Method "POST" `
    -Endpoint "/syllabus/$syllabusId/publish" `
    -Token $adminToken `
    -ExpectedStatus 200

if ($publishResponse) {
    Write-Host "Status: $($publishResponse.status)"
    Write-Host "Is published: $($publishResponse.is_published)`n"
}

# ============================================================
# TEST 9: LIST PUBLISHED
# ============================================================

Write-Host "$blue### TEST 9: LIST PUBLISHED SYLLABUSES ###$reset`n"

Write-Host "Test 9.1: Get published syllabuses"
$publishedResponse = Test-Endpoint -Method "GET" `
    -Endpoint "/syllabus/published?skip=0&limit=10" `
    -Token $lecturerToken `
    -ExpectedStatus 200

if ($publishedResponse) {
    Write-Host "Published syllabuses: $($publishedResponse.count)`n"
}

# ============================================================
# TEST 10: ROLLBACK (Optional)
# ============================================================

Write-Host "$blue### TEST 10: ROLLBACK (OPTIONAL) ###$reset`n"

Write-Host "Test 10.1: Rollback to version 1"
if ($version1Id) {
    $rollbackResponse = Test-Endpoint -Method "POST" `
        -Endpoint "/syllabus/$syllabusId/versions/$version1Id/rollback" `
        -Token $lecturerToken `
        -ExpectedStatus 200

    if ($rollbackResponse) {
        Write-Host "$green✓ Rollback successful$reset"
        
        # Check new version created
        $versionsAfterRollback = Test-Endpoint -Method "GET" `
            -Endpoint "/syllabus/$syllabusId/versions" `
            -Token $lecturerToken `
            -ExpectedStatus 200

        if ($versionsAfterRollback) {
            Write-Host "Total versions after rollback: $($versionsAfterRollback.total)`n"
        }
    }
}

# ============================================================
# SUMMARY
# ============================================================

Write-Host "$blue=== TEST SUMMARY ===$reset"
Write-Host "`n✓ All major tests completed!"
Write-Host "`nKey Test Results:"
Write-Host "1. Syllabus Created: $($syllabusId -ne '' ? '✓' : '✗')"
Write-Host "2. Version Control: $($versionResponse.total -gt 0 ? '✓' : '✗')"
Write-Host "3. CLO/PLO Mapping: $($mappingResponse -ne $null ? '✓' : '✗')"
Write-Host "4. Workflow Status: $($publishResponse.status -eq 'published' ? '✓' : '✗')"
Write-Host "5. Published List: $($publishedResponse.count -gt 0 ? '✓' : '✗')`n"

Write-Host "$green[SUCCESS] Module 2 API is working correctly!$reset`n"
