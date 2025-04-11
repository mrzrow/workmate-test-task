# Test Task

CLI application that analyzes django logs and generates a report.

## Usage

```shell
usage: python main.py [file1 file2 ...] --report [report_name]
                                                              
positional arguments:                                         
  files            log files                                  
                                                              
options:                                                      
  -h, --help       show this help message and exit            
  --report REPORT  report type
```

## Example of Report Generation

```shell
--> python main.py .\log\app1.log --report handlers

HANDLERS             DEBUG       INFO        WARNING     ERROR       CRITICAL    
/api/v1/reviews/     0           5           0           0           0
/admin/dashboard/    0           6           0           2           0
/api/v1/users/       0           4           0           0           0
.............................................................................
                     0           48          0           12          0

Total requests: 60
```

## Creating a New Report Type

To create a new report type, you need to:

+ Create a class that implements the abstract class `AbstractReport` (`./src/reports/abstract_report.py`).
+ Add the class to the `available_reports` variable in the format `"report_name": report_class` in the file `./src/reports/__init.py__`.
+ For testing convenience, add the class to the `__all__` variable in the same `__init__.py` file.
