# Crawing-List-of-Admitted-Schools-for-Students

### get data from using Ctrl+S at [department list](https://www.com.tw/cross/university_030_112.html) each dep.

### TO-DO
- when csvs all output, then use excel to clean it (下拉cell) it can sort by the rules itself, in the end just check。


- find the department he get into.


- for stuno:
    - If want to get the whole number then have to enter the `test place` link, but we cannot enter the website(now we've downloaded whole list of all department using Ctrl+s)

    - get all univ & department they had applied and add it into df using for loop. Run `get _test_location_url.ipynb` to get a csv file named `whole.csv`. -> Trying to delete which repeat.: We can use excel! Nice!

- try to get the whole `<td` count i:9 and print univ_and_department with accepted univ_and_department. 


### Done
- figuring out what's `processing_list` function doing (?count?)
- merge dataframe one by one column from different dataframe
- 正取、備取 have limit. using try, except, else functions. We can try to download all of the test place and use substring to enter it and compare to what unis he had apllied to get the whole test number.
    1. download all test place
    1. compare (two if-else statement)
        1. test number first three digits and the last digit to get only few candidates.
            > if first digit is `L`, `l` then change it to `1`.
        1. campare to unis he had applied
    1. get whole test num

- Get location link first, use excel to delete which more than one and Ctrl+s by each.

- fixed the sequence of department_name (正1、正2沒有對應到 都會延後兩位)

