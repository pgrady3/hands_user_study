# Hand-Object User Study

### Installation

First, clone the repository with the following commands
```
git clone https://github.com/pgrady3/hands_user_study.git
cd hands_user_study
```


Python 3.x is required to run the study, however Python 3.9 is not compatible. Install all python dependencies using

```
pip install -r requirements.txt
```
Next, [download the database of grasps here](https://www.dropbox.com/sh/saygfywfgi4458n/AADvnUWyS61IDnkvTyhuhadaa?dl=0). Extract it so `study.pkl` is in the root of the `hands_user_study` folder.


### Running Fine-Grained Study

To run the fine-grained refinement study:
```
python run_study.py
```

### Running Image-Based Study

```
python run_study.py --split=im
```

### Results Submission
Once you are finished, return the results by emailing `results_*.json` to Patrick Grady
