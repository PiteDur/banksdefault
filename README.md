# banksdefault: Introduction to Machine Learning Methods

This Repository [STILL UNDER CONSTRUCTION] aims at presenting ML methods for classification of default events, using synthetic data for public accessible training and evaluation.

It follows Durand, Le Quang and Vialfont (2023).

# Getting Started

## Access to the code

You may use an environment on your own computer (see `INSTALL.txt` for more information about conda environment), after having cloned this repository with :

``````
git clone https://github.com/Durand-LeQuang-Vialfont/banksdefault
``````

Alternatively, you may open the Notebook `banks_default.ipynb` in Google Colaboratory  and execute the first cell for cloning this Github Repository and benefit from a flexible Python environment :

- Click on the `banks_default.ipynb` link inside the current repository, and
- click on the button `Open In Colab`. 

# Content

The unique notebook of this repository makes internal references to synthetic data and functions contained in the following structure :

``````
banksdefault/
├── data
│   └── syntheticdata.txt
├── docs
│   └── Banks_default.pdf
├── functions
│   ├── interpretation.py
│   └── training.py
├── output
│   ├── RFC_train-time=0_02_03_date=2024-02-24__13_09_58_grid_search-results.xlsx
│   └── sum-up_2024-02-24__13_09_59.xlsx
├── .gitattributes
├── .gitignore
├── banks_default_init.ipynb
├── INSTALL.txt
├── LICENSE.txt
├── README.md
├── requirements_colab.txt
└── requirements_colab_extended.txt
``````

Documentation can be found in the `docs/` folder, `output/` contains illustrations of the desired productions, excluding `pickle` files that are filtered due to the `.gitignore` file in order to avoid incompatible versions of the trained models. The file `.gitattributes` insures no modifications are made with git regarding binary files such as `xslx` files. The `requirements_colab.txt` file should be enough for the Google Colaboratory's environment, but `requirements_colab_extended.txt` can be used instead in order to ensure reproducibility over time (session restart needed in this latter case).

# License 

This project is licensed under the terms of the MIT License. See `License.txt` for more information.

# Authors

This Repository was developed by Pierre Durand, Gaëtan Le Quang and Arnold Vialfont.

We thank Carlie Petit for a her meticulous review of the code and comments.
