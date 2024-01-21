import os
import re
ENV_NAME = 'futebolstats'

def conda_env_list():
    os.system('CALL conda env list > checks/output/available_envs.txt')

def conda_env_create():
    os.system(f'CALL conda create --name {ENV_NAME} --file requirements/requirements.txt')

def check_if_env_exists(env_name: str) -> bool:
    with open('checks/output/available_envs.txt', 'r') as f:
        text = f.readlines()
        envs = [
            r.group(1)
            for t in text
            if (r:=re.search(r'(\w+)(.*)+', t)) is not None
        ]

        env_exists = env_name in envs

    return env_exists

def run_system_command_n_times(command: str, n: int) -> None:
    for _ in range(n):
        os.system(command=command)

def make_new_check():
    conda_env_list()
    env_exists = check_if_env_exists(ENV_NAME)
    if not env_exists:
        os.system('ECHO Problema ao criar o ambiente. Tentando novamente...')
    else:
        os.system(
            (
                "ECHO Ambiente criado com sucesso!"
                " tente iniciar o aplicativo com um"
                " clique duplo em run.cmd"
             )
        )
    return env_exists



env_exists = check_if_env_exists(ENV_NAME)

if env_exists:
    text_ = (
        "ECHO Requerimentos já satisfeitos!"
        " tente iniciar o aplicativo com um"
        " clique duplo em run.cmd"
    )
    ht = 'ECHO ' + '#' * len(text_)
    run_system_command_n_times(command=ht, n=5)
    os.system(text_)
    run_system_command_n_times(command=ht, n=5)
    os.system('TIMEOUT 30')

else:
    os.system('ECHO criando o ambiente python...')
    conda_env_create()

    n = 0
    while not (env_exists := make_new_check()) or n < 5:
        n += 1
        conda_env_create()
