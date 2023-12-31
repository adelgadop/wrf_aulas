# Introduction
This is a project for educational purposes about learning WRF-Chem.

# Mighty Scientist's TODO List :V
- [x] Sail to `WPS program`
  - [x] **Geogrid**: Design your amazing domain and choose your fighter (e.g., one, two or three domains)
    - [ ] Create your Python script or improve one I did to replace the ncl script installed by default `plotgrids_new.ncl`
  - [x] **Ungrib** your datasets, and explore the period that your are excited to analize. Explain to yourself why is important for you.
  - [x] **Metgrid** conquer your meteorological and geographic static data
- [x] Find the secret of the `WRF model` and enjoy the glory days
  - [x] Design your `namelist.input`
  - [x] **real.exe**: Run your I/B conditions
  - [x] **wrf.exe**: Run your WRF model
  - [ ] Explore your data with WRF-Python

### Data management plan (tree project)

```
├── data (*) This directory doesn't upload because it'll get input and output modelling data.
├── figs
├── namelists
├── post
├── scripts
└── tabs
```
### Install a Python environment

```
conda env create -f environment.yml
```

### How use GitHub since terminal
  1. Create a branch.  
     - `git checkout <branch name>`
  2. Working in the branch:
     - `git add -A`
     - `git commit -m "Changed name - short description"`
     - `git push`
  3. `pull request` requested
  4. If there isn't overlapping or conflicts with the `main` branch, you can `merge pull request` in the GitHub webpage
  5. If main has already updated:
     - You can update your branch:
        - `git checkout <branch name`
        - `git merge origin/main`
     - We also continue working in our branch, so:
        - `git checkout <branch-name>`
        - `git add -A`
        - `git commit -m ""`
        - `git push`
        - And repeat step 3 and 4.
