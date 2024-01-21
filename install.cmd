:: call conda env list
CALL conda env list > checks/output/available_envs.txt

:: waits 4 seconds
PING 127.0.0.1 -n 5 > nul

:: makes necessary checks for the dashboard initialization
CALL python checks/checks_and_installs_env.py
