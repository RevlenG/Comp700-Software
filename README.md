# CLUSTERING - GUI APPLICATION:
The is a simple Python application with a minimalistic GUI containing textboxes, radio button groups, labels, large output boxes and a button. This application is used to detect customer preferences in review data, using LDA topic modelling in combination with clustering algorithms such as K-means, Hierarchical and DBSCAN. 

## Features
__Textboxes:__ The application provides textboxes for inputting or loading review data, allowing users to customize the dataset to be analyzed.

__Radio Button Groups:__ Users can choose between different clustering algorithms, including K-means, Hierarchical, and DBSCAN.

__Labels:__ Informative labels guide users through the process, providing clarity and context.

__Large Output Boxes:__ Results of the analysis, including customer preferences (likes and dislikes) based on the detected topics and clusters, are displayed in large output boxes. 

__Start Button:__ Triggers the LDA topic modeling and clustering process.

## Prerequisites
Before using this application, you need to have the following prerequisites:
- Python 3.10 installed on your system.
- Necessary Python packages, which can be installed using the provided requirements file. 

## Installation
1. Clone the repository to your local machine or download the ZIP file.
2. Navigate to the project directory.
3. Install the required dependencies using pip. (pip install -r requirements.txt)

## Usage 
1. Open a terminal or command prompt.
2. Navigate to the project directory where the application is located.
3. Run the application by executing the following command: "python gui.py"
4. The application will launch, displaying the GUI with textboxes, radio button groups, labels, large output boxes, and a button.
5. Enter all the required inputs into the textboxes.
6. Select your desired clustering algorithm by choosing one of the radio buttons.
7. Click the button to initiate the analysis.
8. The application will perform LDA topic modeling and clustering based on the selected algorithm.
9. The results, including customer preferences (likes and dislikes) based on the detected topics and clusters, will be displayed in the output boxes.

Dataset: https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment

Github Repo: https://github.com/RevlenG/Comp700-Software
