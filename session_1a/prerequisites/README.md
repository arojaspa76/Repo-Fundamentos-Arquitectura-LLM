## 🛠️ Prerequisites

Before starting this course, please make sure you meet the following requirements. These steps will help you get the most out of each session and allow you to follow along with all the hands-on exercises:

### 1. Python Installation
- Install **Python 3.12** or above.  
  [Download Python here](https://www.python.org/downloads/)
- ***If you have a github account, you can also fork the course repository and you can use the **GitHub Codespaces** feature to run the course code online. This allows you to work in a full VSCode environment in the cloud without needing to install Python locally.***

### 2. Code Editor
- Install a code editor such as **VSCode** (recommended) or **PyCharm**.
  - [Download VSCode](https://code.visualstudio.com/)
  - [Download PyCharm](https://www.jetbrains.com/pycharm/download/)
  - **VSCode** is recommended for its simplicity and wide range of extensions, including Jupyter support.
- Codespaces: If you prefer an online environment, you can use **GitHub Codespaces** or **Google Colab**.
  - GitHub Codespaces: https://github.com/user/repository/codespaces
  - Google Colab: https://colab.research.google.com/
  - **github Codespaces** provides a full VSCode experience in the cloud, while **Google Colab** is great for quick experiments and sharing notebooks.

  if you cannot install VSCode or PyCharm, you can use **GitHub Codespaces** to run the course code online. When you open the course repository, you can click on the "Code" button and select "Open with Codespaces" to create a new codespace. This will give you a full VSCode environment in the cloud, where you can run Python code and Jupyter notebooks without any local setup.

  When we begin the Deep Learning section, you can also use Google Colab to run the code. Google Colab is a free Jupyter notebook environment that runs in the cloud and is particularly useful for deep learning tasks. You can access it at [Google Colab](https://colab.research.google.com/). Alternatively, if you don't have access to Google Colab, you will need to install the required packages in your local environment and run the code in VS Code.

### 3. Jupyter Notebook
- Install **Jupyter Notebook** (via Anaconda, Miniconda, or pip).
  - [Jupyter installation guide](https://jupyter.org/install)

### 4. Create a Virtual Environment
- Set up a **virtual environment** for your Python projects (using `venv`, `virtualenv`, or `conda`).
  
  - Example for Windows:
    ```PowerShell
    python -m venv ai-course-env
    .\ai-course-env\Scripts\activate
    ```
    
    Please **<u>ctrl + click</u>** on the image below to watch the video on setting up the virtual environment for Python in Windows 11. 
    
    [AI Fundamentals Bootcamp - Instalación de prerrequisitos de python para Windows 11.](https://youtu.be/fOqisr0Sazk?si=IJ1rnnu4iEKHpvNU)

    <a href="https://youtu.be/fOqisr0Sazk" target="_blank" rel="noopener noreferrer">
      <img src="https://i.imgur.com/GcRenJg.png" alt="AI Fundamentals Bootcamp - Instalación de prerrequisitos de python para Windows 11." width="400"/>
    </a>

  - Example for Linux/Mac/Codespaces:
    ```bash
    python3 -m venv ai-course-env
    source ai-course-env/bin/activate
    ```



### 5. Directory Structure (Best Practices)
- Use this recommended structure for your projects:
    ```
     ai_python_course/
     ├── notebooks/
     ├── data/
     ├── src/
     ├── results/
     ├── README.md
     └── requirements.txt
     ```
- **notebooks/**: Jupyter notebooks for each session  
- **data/**: Datasets used in the course  
- **src/**: Python scripts (functions, utilities, experiments)  
- **results/**: Output files, figures, and models  
- **README.md**: Your course notes and documentation  
- **requirements.txt**: List of required Python packages

### 6. Required Python Packages
- Install the following packages in your virtual environment:
    ```bash
    pip install numpy pandas matplotlib seaborn scikit-learn jupyter
    ```
  *(Additional packages will be introduced as needed in the course, such as `tensorflow`, `torch`, or `opencv`.)*
- Or, Install dependencies using the provided `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```
     
### 7. Basic Command Line Usage
- Be comfortable navigating folders and running commands in the terminal (Command Prompt, PowerShell, or Terminal).

### 8. Recommended: Git (Optional, but useful!)
- Install **Git** for version control and good development practices.
  - [Download Git](https://git-scm.com/downloads)

---

**No previous experience with AI or advanced programming is required! If you have any questions or need help with setup, feel free to reach out before the first session.**


---

## ⚡ Quick Setup Guide

We provide automation scripts and a Makefile to make your setup as easy as possible.  
**Most students use Windows 11 — follow the first set of instructions. Linux/Mac users, see below.**

### 1. Download or Clone the Repository

Download or clone this repository to your computer:
```bash
git clone https://github.com/arojaspa76/AI-Fundamentals.git
cd ai_python_course
```

### 2. Create the Folder Structure Automatically
For Windows 11 (PowerShell):
- Open PowerShell in the folder where you want your project.
- Run:
```bash
.\setup_ai_course.ps1
```
*Note: If you get a permissions error, run as administrator the following:*
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

For Linux/Mac:
- Open your terminal.
- Run:

```bash
bash setup_ai_course.sh
```

*This will create the recommended folders and template files (README.md, requirements.txt, Makefile).*

---

## 🛠️ About the Makefile (Optional, Advanced Users)

A `Makefile` is included to help automate setup tasks, such as creating a virtual environment and installing dependencies. This tool is commonly available on Linux and Mac, but it is **optional on Windows**.

### *Be sure that you are in the `Prerrequisites` folder before running pip install -r requirements.txt. To activate the virtual environment, be sure that you are in the root folder where the virtual environment was created.*

### For Most Windows Users (Recommended)

You do **not** need to install `make`.  
Instead, simply run the commands in each section manually in your Command Prompt or PowerShell, for example:

If the virtual environment is not already created, run as follows:
```PowerShell
python -m venv ai-course-env
.\ai-course-env\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=ai-course-env --display-name="Python (AI Course)"
```

If the virtual environment is already created, run as follows:
```PowerShell
.\ai-course-env\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=ai-course-env --display-name="Python (AI Course)"
```

### For Advanced Users Who Want to Use the Makefile
If you are comfortable installing extra tools, you can use make to automate these commands:

### *Be sure that you are in the `Prerrequisites` folder before running make config-windows-env. To activate the virtual environment, ensure you are in the root folder where the virtual environment will be created. The virtual environment will be created in the folder where you will run the make config-windows-env.*

Option 1: Using Chocolatey (requires administrator privileges)
- Install [Chocolatey](https://chocolatey.org/install).
- Open an administrator PowerShell window.
- Run:
```PowerShell
choco install make
```

- Then, in your course folder Prerrequisites, run:
```PowerShell
make config-windows-env
```

Option 2: Using Git Bash
If you use [Git Bash](https://gitforwindows.org/), it often includes make by default. Just open Git Bash, navigate to your course folder Prerrequisites, and use:
```bash
make config-windows-env
```

Option 3: GnuWin32 Make
Download from [GnuWin32 Make](https://gnuwin32.sourceforge.net/packages/make.htm) and add it to your PATH manually (advanced, not recommended for beginners).

|💡 If this sounds too complex, just stick with the manual commands above!

If you have questions or need help with the setup, reach out to the instructor. The goal is to make your learning experience smooth and enjoyable! 🚀
