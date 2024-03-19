#Development Setup

##Prerequisites Software
* Java 8
* Python >= 3.6.9

## Local Development Box Setup
1. Ensure python, git executables are in your PATH variable.
2. Checkout code using git clone into a directory, say: ROOT
    > git clone <git-repo-path>
3. Change directory to dataflow-task-core
    > cd $ROOT/dataflow-task-core

4. Create Python Virtual environment. Make sure you are using virtualenv belonging to python 3.6.x
    > Linux/macOS  : virtualenv venv  OR  python -m venv venv
5. Open Terminal and activate your virtual environment and install external python modules via below command:
    >(Windows): venv\Scripts\activate
    >(mac): source venv\bin\activate
    >pip install -r requirements.txt
   
## Configure the project in PyCharm IDE

 1. Open python code root directory via menu 
    > File | Open... | Open File or Folder (choose **$ROOT/dataflow-task-core**)
 2. Once opened, configure the Project Interpreter (Python executable)
    
     <sub>**Note:-** PyCharm may already detect venv automatically. So you may not need to perform this step.</sub>
     > File | Settings | Project: dataflow-task-core | Project Interpreter
    
 3. In `Settings` dialog box, click on `settings button` in front of `Project Interpreter` dropdown box <br/> 
    and select `Add..` <br/>
    In `Add Python Interpreter` dialog box choose `Existing environment` option<br/> 
    and select (windows) $ROOT/dataflow-task-core/venv/Scripts/python path.<br/>
    Click `OK` to close the dialog box <br/>
    Now ensure or choose the newly added virtual environment in the drop-down field (on top) <br/>
    Click `Apply` to apply change.<br/>

 4. Configure the pytest as default integrated test runner.
    
     <sub>**Note:-** PyCharm may already detect pytest as default runner automatically. So you may not need to
     perform this step.</sub>
     > File | Settings | Tools | Python Integrated Tools

     Chose `py.test` in dropdown field `Default test Runner:` <br/>
     and click on `Apply` button
 5. 1. Configure default run configuration
    > Run | Edit Configurations...
    
        > File | Settings | Tools | Python Integrated Tools

    Navigate to `Templates` > `Python panel` <br/>
    For field `Working Directory` choose project root path (`$ROOT/dataflow-task-core`) <br/>
    
    Navigate to `Templates` > `Python tests` > `pytest` <br/>
    For field `Working Directory` choose project root path (`$ROOT/dataflow-task-core`) <br/>
    and click on `OK` button to close the `Run/Debug Configurations` dialog box.
    1. For setting any OS ENVIRONMENT variable, you can create the `.env` file at root folder by copying the file 
        `.env.template`. This file is meant to host environment variable meaningful for your local environment only. So 
        never commit this.
 6. # Add Source directories
    1. If Pycharm not treated modules as source directories then we might get `Module not Found` error or 
    compilation error while importing Classes, Methods from the particular modules.
    2. We need to go the below location and remove any existing entry and add `$ROOT/dataflow-task-core` as Sources
    > File | Settings | Project:dataflow-task-root | Project Structure

 7. # Build
    1. Activate the venv, if not already done
        > cd $ROOT/dataflow-task-core<br/>
        (windows)> venv/Scripts/activate
        (mac)> source venv/bin/activate
    2. Code Build
        > No compilation required (as of now)
    3. Python Code style check (report at target/flake-reports/index.html)
    
        See `setup.cfg#flake8` section for custom PEP-8 rule configuration 
        > flake8 
    
        <sub>**Note:-** You may use `# flake8: noqa` for disabling inspection on any code line</sub> 
    4. Python Unit Test (report at target/pytest-report.html)

        You can run all unit test cases from PyCharm too by right-clicking on `tests` directory 
        and `Run pytests in tests` option
        > pytest
    
    5. Python Unit Test with code Coverage (target/coverage-reports/index.html)
    
        See `setup.cfg#coverage:report` section for configuration and coverage threshold 
        > pytest --cov=dataflow-task --cov-report html --cov-report term
    
        1. Cover code under package `task_base`
        1. Generate html report and
        1. Generate terminal report
    6. Generating .whl files for Glue Shell Jobs
        > python setup.py package
    
        1. Generate artifacts under dist/ directory.
