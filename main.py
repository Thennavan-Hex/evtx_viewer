# main.py
from view.evtx_view import display_evtx_data

def main():
    evtx_file_path = "fiel.evtx"
    display_evtx_data(evtx_file_path)

if __name__ == "__main__":
    main()
