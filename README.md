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
