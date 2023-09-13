# Crawing-List-of-Admitted-Schools-for-Students

### get data from using Ctrl+S at [department list](https://www.com.tw/cross/university_030_112.html) each dep.

### TO-DO
- figuring out what's `processing_list` function doing (?count?)

- If want to get the whole number then have to enter the `test place` link, but we cannot enter the website(now we've downloaded whole list of all department using Ctrl+s)

- get all univ & department they had applied and add it into df using for loop.
### Done
- merge dataframe one by one column from different dataframe
- 正取、備取 have limit. using try, except, else functions. We can try to download all of the test place and use substring to enter it and compare to what unis he had apllied to get the whole test number.
    1. download all test place
    1. compare (two if-else statement)
        1. test number first three digits and the last digit to get only few candidates.
            > if first digit is `L`, `l` then change it to `1`.
        1. campare to unis he had applied
    1. get whole test num
