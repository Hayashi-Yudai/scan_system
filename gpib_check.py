import pyvisa as visa

if __name__ == "__main__":
    rm = visa.ResourceManager()
    library = rm.visalib.library_path

    print(library)
