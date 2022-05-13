# B-GAP Enhancements
### Authors 
Kunal Mody, Gavin Garcia, Philip Zeng

### Installation
Using python Version 3.6.x

pip install following dependencies:

```
torch
gym==0.21
highway-env
imageio-ffmpeg
```  

Install rl-agents as module:  
```
cd BGAP-Geom-Final 
cd rl-agents 
pip install -e .  
```

### Running 
Run the model with rubberbanding for 100 episodes
```
python -W ignore experiments.py evaluate configs/HighwayEnv/env.json configs/HighwayEnv/agents/DQNAgent/dqn.json --test --episodes=100 --name-from-config --recover-from=out/brakecheckreal/checkpoint-best.tar
```

Train the model 
```
python -W ignore experiments.py evaluate configs/HighwayEnv/env.json configs/HighwayEnv/agents/DQNAgent/dqn.json --train --episodes=2000 --name-from-config
```
