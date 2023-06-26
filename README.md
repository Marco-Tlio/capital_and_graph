# Introduction

This project is based on a technical interview, I was asked to create two functions in Python. One function is responsible for creating a table with data, and the other function is for creating graphs. The project primarily utilizes the pandas and seaborn libraries.
If there are no specific notes regarding replicability, and the scripts are designed to 'just work'.

# Assumptions
Regarding the assumptions, in addition to considering a 4.4% inflation rate, all heads of household are assumed to be heads-of-household (as specified in the [legislation](https://smartasset.com/retirement/savers-match-secure-2-0-act)). The payout reduction only occurs at the ceiling limit of $53,250. However, if you want to explore scenarios where the heads of household are not considered as heads-of-household and/or there is a reduction in the saver's match by a factor of two (e.g., returning 20% or 10% based on the information provided in this [article](https://money.usnews.com/money/retirement/iras/articles/how-to-qualify-for-the-retirement-savers-match#:~:text=How%20to%20Get%20the%20Saver's,to%20a%20qualifying%20retirement%20account.), you can refer to the options "all_equal" and "realistic" in create_new_csv().
