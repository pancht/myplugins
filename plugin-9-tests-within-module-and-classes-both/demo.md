1. Fixtures for Data Sharing 
   2. Use request object to get context/config.
9. Marker support for grouping of tests and selection (We can only use this feature for test discovery in sentinel and not for test execution)
   10. pytest --markers
   11. pytest --co
   12. pytest --co -m <marker>
1. Testrail id using marker
10. Parallel test execution by pytest-xdist (This pytest feature we can not use in sentinel)
    11. -n <#tests>
22. Dynamic Test Generation 
    23. Tests can be created dynamically using the pytest_generate_tests hook.
        24. pass dynamic data to tests without using @pytest.mark.parametrize. (This pytest feature we can not use in sentinel)
24. Skipping/Expected Failures
    25. Use @pytest.mark.skip, @pytest.mark.skipif, or @pytest.mark.xfail.
    26. @pytest.mark.skip(reason="Not implemented yet")
27. Test filtering by pytest
    12. -k "add" 
13. Allure Reporting Integration
    14. Cool test report overview 
    15. Categories (By each marker)
    16. Graphs 
    17. Timeline 
    18. Behaviours 
    19. Packages 
    20. Fixture teardown logs (It is not coming in sentinel!)
    20. Great community support 
    21. Open Source

With allure reporting
1. We only need a webserver to serve report and no database. This can reduce substantial cost to infra.
2. We can save a lot of Engineer hours in preparing test report and results history. Again reduce cost to people.
3. Since allure reports are displays test results, past results and history in an intuitive and with great visualization, there is no need for explaining details.
With pytest-xdist
1. There is no need to write and maintain custom logics for parallelization of tests.
2. We need single machine with great computation power say
   3. 8-16 core CPU 
   4. 16-32 GB RAM
      5. pytest -n auto --dist=loadscope 
      6. -n auto: uses all available cores. 
      7. --dist=loadscope: groups test classes/functions intelligently across workers.
      8. --durations=10 to analyze slow tests.
      9. 