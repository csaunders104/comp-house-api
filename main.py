import os.path
import api
import answers as a
import globals as g

file_exists: bool = os.path.exists(g.json_file)

def main():
    '''Collect everything together. Either create
    data.json or use already existing to save time'''

    # checks if data already exists in path
    if file_exists is False:
        df = api.read_from_api()
    if file_exists is True:
        df = api.read_from_json()

    run = a.Answers()
    run.collate_answers(df)

if __name__ == "__main__":
    main()
