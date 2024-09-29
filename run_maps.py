import os
import subprocess
import time

maps = [
    "maps/tournament/g1.json",
    "maps/tournament/g2.json",
    "maps/tournament/g3.json",
    "maps/tournament/g4.json",
    "maps/tournament/g5.json",
    "maps/tournament/g6.json",
    "maps/tournament/g7.json",
    "maps/tournament/g9.json",
]

maximum_frequency = [
    9,
    9,
    13,
    4,
    10,
    1,
    13,
    50,
]

radii = [5, 20, 40, 150]
run = 1  
t = 3600  

log_dir = 'log'
logP = os.path.join(log_dir, 'Group 1.log')
if os.path.exists(logP):
    os.remove(logP)


for i in range(len(maps)):
    map_path = maps[i]
    mf = maximum_frequency[i]
    m_values = [mf, 2 * mf, 'inf']
    for m in m_values:
        if m == 'inf':
            m_arg = '10000000000000' 
            md = 'infinity'
        else:
            m_arg = str(m)
            md = str(m)
        for r in radii:
            command = [
                'python', 'main.py',
                '-m', m_arg,
                '-r', str(r),
                '-s', '7',
                '-mz', map_path,
                '--player', '1',
                '-ng'
            ]
            
            try:
                print(f"Running command: {' '.join(command)}")
                s = time.time()
                subprocess.run(command, timeout=t)
                execution_time = time.time() - s

                if os.path.exists(logP):
                    r_f = f'run_map{i}_m{m}_r{r}.log'
                    with open(logP, 'r') as log:
                        group_log_content = log.read()
                    with open(r_f, 'w') as logf:
                        logf.write(f"r: {r}, m: {md}, map: {map_path}\n")
                        logf.write(f"Execution time: {execution_time:.2f} seconds\n")
                        logf.write(group_log_content)
                    os.remove(logP)
                    run += 1
                else:
                    print(f"{logP} not found after running the command.")
            
            except subprocess.TimeoutExpired:
                if os.path.exists(logP):
                    r_f = f'run_map{i}_m{m}_r{r}.log'
                    with open(logP, 'r') as log:
                        group_log_content = log.read()
                    with open(r_f, 'w') as logf:
                        logf.write(f"r: {r}, m: {md}, map: {map_path}\n")
                        logf.write(f"Error: Simulation timed out after 5 min.\n")
                        logf.write(group_log_content)
                    os.remove(logP)
                    run += 1
                else:
                    print(f"{logP} not found after running the command.")
            
                    r_f = f'run_map{i}_m{m}_r{r}.log'
                    with open(r_f, 'w') as logf:
                        logf.write(f"r: {run}, m: {md}, map: {map_path}\n")
                        logf.write("Error: Simulation timed out after 5 min.\n")
                
                print(f"Command timed out: {' '.join(command)}")
                run += 1
