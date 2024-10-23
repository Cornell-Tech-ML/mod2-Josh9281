[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/YFgwt0yY)
# MiniTorch Module 2

<img src="https://minitorch.github.io/minitorch.svg" width="50%">


* Docs: https://minitorch.github.io/

* Overview: https://minitorch.github.io/module2/module2/

This assignment requires the following files from the previous assignments. You can get these by running

```bash
python sync_previous_module.py previous-module-dir current-module-dir
```

The files that will be synced are:

        minitorch/operators.py minitorch/module.py minitorch/autodiff.py minitorch/scalar.py minitorch/scalar_functions.py minitorch/module.py project/run_manual.py project/run_scalar.py project/datasets.py

---

# Experiment Results

## Dataset: Simple
**Settings:**
- Number of Points: 50
- Size of Hidden Layers: 5
- Learning Rate: 0.05
- Number of Epochs: 1000

### Epoch Data

| Epoch | Loss               | Correct |
|-------|---------------------|---------|
| 10    | 34.274252296769795  | 31      |
| 20    | 33.91584919098648   | 31      |
| 50    | 32.91685543495436   | 31      |
| 100   | 31.942124225864422  | 31      |
| 200   | 28.23000582773265   | 35      |
| 300   | 19.329039886132204  | 48      |
| 400   | 9.671141311590388   | 49      |
| 500   | 4.905388450687159   | 50      |
| 1000  | 1.0533713312016728  | 50      |

Time per epoch: 0.140s

### Result Graph
![Simple Dataset Result Graph](graphs/Simple.png)

### Loss Function Graph
![Simple Dataset Loss Function Graph](graphs/Simple_lg.png)

---

## Dataset: Diag
**Settings:**
- Number of Points: 50
- Size of Hidden Layers: 5
- Learning Rate: 0.05
- Number of Epochs: 1000

### Epoch Data

| Epoch | Loss               | Correct |
|-------|---------------------|---------|
| 10    | 25.654245384771265  | 44      |
| 20    | 20.504266351748086  | 44      |
| 50    | 16.164875164802407  | 44      |
| 100   | 14.796806221914395  | 44      |
| 200   | 12.883006725287384  | 44      |
| 300   | 10.908183117092893  | 44      |
| 400   | 8.770246559569022   | 45      |
| 500   | 7.38342265296124    | 47      |
| 1000  | 3.95701953673952    | 49      |

Time per epoch: 0.139s

### Result Graph
![Diag Dataset Result Graph](graphs/Diag.png)

### Loss Function Graph
![Diag Dataset Loss Function Graph](graphs/Diag_lg.png)

---

## Dataset: Split
**Settings:**
- Number of Points: 50
- Size of Hidden Layers: 15
- Learning Rate: 0.05
- Number of Epochs: 1000

### Epoch Data

| Epoch | Loss               | Correct |
|-------|---------------------|---------|
| 10    | 33.14474466921484   | 32      |
| 20    | 31.559292082280294  | 35      |
| 50    | 29.394633505015808  | 35      |
| 100   | 27.02843564616674   | 42      |
| 200   | 22.00057145097753   | 44      |
| 300   | 17.257289542457023  | 45      |
| 400   | 13.483244471742701  | 48      |
| 500   | 10.850454020195542  | 48      |
| 1000  | 5.371090461166223   | 49      |

Time per epoch: 0.720s

### Result Graph
![Split Dataset Result Graph](graphs/Split.png)

### Loss Function Graph
![Split Dataset Loss Function Graph](graphs/Split_lg.png)

---

## Dataset: Xor
**Settings:**
- Number of Points: 50
- Size of Hidden Layers: 20
- Learning Rate: 0.05
- Number of Epochs: 1000

### Epoch Data

| Epoch | Loss               | Correct |
|-------|---------------------|---------|
| 10    | 33.808181969083634  | 35      |
| 20    | 32.36451586997944   | 37      |
| 50    | 30.59224429807969   | 35      |
| 100   | 28.626462327050746  | 35      |
| 200   | 24.793095520051907  | 40      |
| 300   | 20.81645794303515   | 44      |
| 400   | 17.05382468302207   | 45      |
| 500   | 13.974367470041322  | 47      |
| 1000  | 7.916069335192185   | 49      |

Time per epoch: 1.197s

### Result Graph
![Xor Dataset Result Graph](graphs/Xor.png)

### Loss Function Graph
![Xor Dataset Loss Function Graph](graphs/Xor_lg.png)


