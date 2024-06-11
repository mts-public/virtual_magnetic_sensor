import os
import glob
import h5py
import faulthandler
from pathlib import Path
from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler
from libs.simulation.SimulationHandler import SimulationHandler
from ngsolve import Redraw
import re

class MultiprocessingTasks:

    @staticmethod
    def run_work(*args) -> None:
        SimulationHandler.run_process(*args)

    @staticmethod
    def draw_work(*args) -> None:
        SimulationHandler.draw_process(*args)


    def get_hdf5_files(directory_path):
        """Get all HDF5 files in the specified directory.

        :param directory_path: Path to the directory.
        :type directory_path: str
        :return: List of HDF5 files in the directory.
        :rtype: list
        """
        hdf5_files = glob.glob(os.path.join(directory_path, '*.h5')) + \
            glob.glob(os.path.join(directory_path, '*.hdf5'))

        return hdf5_files

    def read_hdf5_file(file_path):
        """Read data from an HDF5 file and return it as a dictionary."""
        def rec_load_dict(h5file, path='/'):
            ans = {}
            for key, item in h5file[path].items():
                if isinstance(item, h5py.Dataset):
                    ans[key] = item[()]
                elif isinstance(item, h5py.Group):
                    ans[key] = rec_load_dict(h5file, path + key + '/')
            return ans

        with h5py.File(file_path, 'r') as file:
            data_dict = rec_load_dict(file)
        return data_dict

    def check_key_exists(data, pattern):
        """Check if a key matching the pattern exists in the data dictionary."""
        for key in data:
            if re.match(pattern, key):
                return True
            if isinstance(data[key], dict):
                if MultiprocessingTasks.check_key_exists(data[key], pattern):
                    return True
        return False


    def change_dict_theta(hdf5_dict: dict):
        evo_pattern: str
        for i in range(len(list(hdf5_dict.keys()))):
            evo_pattern = rf'EvoGear{i}'
            if MultiprocessingTasks.check_key_exists(hdf5_dict, evo_pattern):
                break
            else:
                raise ("Your key does not exist")

        print("Lenght of time array, ", hdf5_dict["SimParams0"]["t"].shape)
        print("Time Array beneath:")
        
        #print(hdf5_dict["SimParams0"]["t"])
        for index, value in enumerate(hdf5_dict["SimParams0"]["t"]):
            print(f"Index: {index}, Value: {value}")
        
        time_index = input("Choose a time index to draw Gui at that time")
        
        print("You have choosen index: ", time_index, "| Time choosen: ",
            hdf5_dict["SimParams0"]["t"][int(time_index)])
        
        hdf5_dict[evo_pattern]["theta"]=hdf5_dict[evo_pattern]["omega"]*hdf5_dict["SimParams0"]["t"][int(time_index)]
        
        return hdf5_dict

if __name__ == '__main__':
    faulthandler.enable()
    data_handler = DataHandler()
    config_handler = ConfigHandler()
    
    files = MultiprocessingTasks.get_hdf5_files("")

    for (i, file) in enumerate(files, start=1):
        print("Index: ",i-1, "| File: ",file)
        
    hdf5_dict = MultiprocessingTasks.read_hdf5_file(files[int(input("Choose File Index"))])

    hdf5_dict = MultiprocessingTasks.change_dict_theta(hdf5_dict)
    data_handler.deploy_dict(hdf5_dict)
    MultiprocessingTasks.draw_work(data_handler)

    
    
