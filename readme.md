# UCY functions descriptions:

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
  
		\*\*kwargs: for tau kwarg used in exponential window function.
  
	Returns:
 
		tuple[np.array]: 2-element tuple containing 1D frequency and 1D amplitude arrays.

## h5_tree
Prints the structure of a hdf5 file on the terminal. Just feed the h5py "file" class as a n argument.

## GetH5Tree
Takes the h5py File class and returns the hdf5 tree as a string.

	Params:
 
		val: h5py file class.
  
		pre (str): Don't provide this argument, used for recursive purposes.
  
		out (str): Don't provide this argument, used for recursive purposes.
  
	Returns:
 
		str: Tree structure of the hdf5 file.
