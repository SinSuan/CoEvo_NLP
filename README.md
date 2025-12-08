[FlowChart](https://app.diagrams.net/#G1jZPJl-ub39yaKapU4RwJSkQrHc7fB1Ef#%7B%22pageId%22%3A%22TYXShAZ42i61218cSP02%22%7D)

[EvoPrompt](https://arxiv.org/abs/2309.08532)

ttl = total

instruction

{your_command} 2>&1 | tee {relative_path to log.txt}

### init
```
pip install -r requirements.txt
```

### **Experiment**
```
python main.py --task {name_task_1},{name_task_2},... \
               --full_name_model {full_name_model} \
               --gpu {gpu_index} \
               --strategy {strategy_1},{strategy_2},... \
               --target_score {int} \
               --target_itration {int} \
               --num_experiment {int}
```

### **initialize population** and **create contrastive population**
```
python main.py --task {name_task} \
               --full_name_model {full_name_model} \
               --gpu {gpu_index}
```
