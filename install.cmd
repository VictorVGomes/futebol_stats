:: call conda env list
CALL conda env list > checks/output/available_envs.txt

:: makes necessary checks for the dashboard initialization
python checks/checks_and_installs_env.py
