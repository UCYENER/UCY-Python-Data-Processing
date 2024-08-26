# ucy_module descriptions:

## psdata2csv
Converts all psdata files in the current directory to csv files.

By default, it only saves the "current waveform".

To save all waveforms, add "/b all" at the end of the command


## take_fft
FFT code, translated from the FFT Matlab code

	Params:
 
		sig (np.array): signal array, can be a list or a numpy array. Must be 1D.
  
		Navg (int): Number of averagings desired for the FFT.
  
		sampling_freq (float): Sampling rate of the signal in Sa/s.
  
		window (str): FFT window. Defaults to "rectangle".
  
	Returns:
 
		tuple[np.array]: 2-element tuple containing 1D frequency and 1D amplitude arrays.


## get_h5_tree
Takes the h5py File class and returns the hdf5 tree as a string.

	Params:
 
		val: h5py file class.
  
		pre (str): Don't provide this argument, used for recursive purposes.
  
		out (str): Don't provide this argument, used for recursive purposes.
  
	Returns:
 
		str: Tree structure of the hdf5 file.

## save_to_csv
Save a set of arrays to a csv file. The arrays can be of different length. 
	
 	Params:
		arrays_ (list): list of 1D arrays to be saved.
		headers_ (list): list of headers of the arrays.
		filename (str): the name of the csv file.


  
## read_from_csv
Read a csv file that contains arrays with different length.
	
 	Params:
		filename (str): name of the csv file.
		col_numbers (list): list of the column numbers to be read.
  

