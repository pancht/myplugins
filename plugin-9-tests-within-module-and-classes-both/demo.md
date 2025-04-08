1. fixture parameterization through config
9. Marker support by pytest enables categorization of tests and selection
   10. pytest --markers
   11. pytest --co
   12. pytest --co -m <marker>
10. Parallel test execution by pytest-xdist
    11. -n <#tests>
22. Dynamic Test Generation
    23. Tests can be created dynamically using the pytest_generate_tests hook.
24. Skipping/Expected Failures
    25. Use @pytest.mark.skip, @pytest.mark.skipif, or @pytest.mark.xfail.
26. Test filtering by pytest
    12. -k "add" 
13. Allure Reporting Integration
    14. Cool test report overview 
    15. Categories 
    16. Graphs 
    17. Timeline 
    18. Behaviours 
    19. Packages 
    20. Great community support 
    21. Open Source