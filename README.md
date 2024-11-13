
##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)


---

##  Overview

Some word game-related  tools, including a complete and functional Wordament Solver that can handle all special tiles (please RTFM first though). Was originally a different Wordament solver I made that had a very shitty OCR component, but that has been deprecated for being, well, shit.

---

##  Features

Two Trie-based solutions - a Wordament solver and a general Un-scrambler/Scrabble rack solver/anagrammer tool. Both GUI, made with customtkinter.

---

##  Project Structure

```sh
└── grammarpuss/
    ├── Pipfile
    ├── Pipfile.lock
    ├── README.md
    ├── anagrams.py
    ├── assets
    │   └── wordament_dictionary.txt
    └── wordup.py
```

##  Getting Started

###  Prerequisites

Before getting started with grammarpuss, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python ^3.10
- **Package Manager:** Pipenv for venv management and dependencies. Pipfile and lock included (or just pip install yourself, or just handle it manually since the depends are very minimal).


###  Installation

Install grammarpuss using one of the following methods:

**Build from source:**

1. Clone the grammarpuss repository:
```
❯ git clone https://github.com/nannerpusser/grammarpuss
```

2. Navigate to the project directory:
```sh
❯ cd grammarpuss
```

3. Install the project dependencies:


**Using `pipenv`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pipenv-3775A9.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pipenv.pypa.io/)

```sh
❯ pipenv install
```




###  Usage
Run grammarpuss using the following command:
**Using `pipenv`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pipenv-3775A9.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pipenv.pypa.io/)

```sh
❯ pipenv shell
❯ python wordup.py
```
---
##  Project Roadmap

- lol, yeah right.

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/nannerpusser/grammarpuss/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/nannerpusser/grammarpuss/issues)**: Submit bugs found or log feature requests for the `grammarpuss` project.

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
