# BOSCH CODERACE CHALLENGE 2023 ROUND 3
## Topic: Data Migration
Team name: OnePlusTwo

Members:
- Hoang Nghia Viet
- Mai Chien Vi Thien
- Bui Nguyen Hoang

## Usage
### Requirements
Install required packages using the requirements.txt file.

`pip install -r requirements.txt`.

### Config file
To customize the output in `JSON` and `RST` files, please refer to the `UserGuide` sheet in the `config.xlsx` file and configure the necessary values accordingly.

### Github
Set the values of `TOKEN`, `BRANCH_NAME`, and `REPOSITORY_NAME` in the `secret.env` file in order to push the `RST` file to the specified branch in the organizer's GitHub repository.

### Run tasks
Run the command `python task1.py` to generate file `Output/data.json`.

Run the command `python task2.py` to generate file `Output/ECU_Requirement.rst`.

Run the command `python task3.py` to upload the RST file to Github.