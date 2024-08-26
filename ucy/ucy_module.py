import os 
from sys import exit 

try:
	import numpy as np 
	import pandas as pd
	import h5py
	from scipy import signal
except ModuleNotFoundError:
	raise Exception("Please install the required Python modules!")
	






def save_to_csv(arrays_:list[np.ndarray], headers_:list[str], filename:str):
	""" Save a set of arrays to a csv file. The arrays can be of different length. 
	Params:
		arrays_ (list): list of 1D arrays to be saved.
		headers_ (list): list of headers of the arrays.
		filename (str): the name of the csv file. """

	if len(headers_) == 1:
		# if only one array is to be saved, put it in a list
		arrays = []
		arrays.append(arrays_)
		headers = []
		headers.append(headers_)
	else:
		# else, if multiple arrays are fed, there is no problem
		arrays = arrays_
		headers = headers_

	# find the length of the largest array
	max_len = int(max(array.size for array in arrays) )
 
	# form the empty matrix that will contain all arrays
	matrix = np.empty((max_len, len(arrays)))
	matrix[:] = np.nan # make all elements nan

	for i, array in enumerate(arrays): 
		# register the arrays into the empty matrix one by one
		matrix[:array.size, i] = array

	df = pd.DataFrame(matrix) # form a pandas dataframe with the matrix

	# save the dataframe into a csv file
	df.to_csv(filename, index=False, header=headers)









def read_from_csv(filename:str, col_numbers_:list):
	"""Read a csv file that contains arrays with different length.
	Params:
		filename (str): name of the csv file.
		col_numbers (list): list of the column numbers to be read. """

	pandas_content = pd.read_csv(filename) # read the csv file
	pandas_columns = pandas_content.columns

	if isinstance(col_numbers_, list):
		# if multiple column numbers are asked, no problem
		col_numbers = col_numbers_
	else:
		# else, (only single column), it needs to be put in a list
		col_numbers = []
		col_numbers.append(col_numbers_)

	arrays_list = [] # the array list that will contain all arrays asked 

	for col in col_numbers:
		# for each column to be read,

		if col >= len(pandas_columns):
			# if column number is greater than the number of total columns in a file,
			raise Exception("The column numbers exceed the number of columns in the csv file!")
		
		data = pandas_content[pandas_columns[col]] # get the data
		data = data.to_numpy() # convert it to a numpy array

		arrays_list.append(data[~np.isnan(data)]) # append to array_list without taking the non-nan elements 
	
	# return the list containing multiple (optional) arrays with various sizes
	return arrays_list








def psdata2csv() -> None:
	"""Converts all psdata files in the current directory to csv files.
	By default, it only saves the "current waveform".
	To save all waveforms, add "/b all" at the end of the command """
	os.system('Picoscope /c *.psdata /f csv')






def take_fft(sig:np.array, Navg:int, sampling_freq:float, window:str='rectangle') -> tuple[np.array]:
	"""FFT code, translated from an FFT Matlab code
	Params:
		sig (np.array): signal array, can be a list or a numpy array. Must be 1D.
		Navg (int): Number of averagings desired for the FFT.
		sampling_freq (float): Sampling rate of the signal in Sa/s.
		window (str): FFT window. Defaults to "rectangle"
	Returns:
		tuple[np.array]: 2-element tuple containing 1D frequency and 1D amplitude arrays """

	Dx = sig - np.mean(sig)				# AC signal
	Nfft = int(Navg) 					# number of FFT for averaging
	ts = 1/sampling_freq 				# sampling period
	Fs = 1/ts 							# sampling frequency
	length = int((len(Dx)/Nfft)*Nfft)	# length of a single fft signal

	D3 = Dx[0:length]
	D2 = D3.reshape(int(length/Nfft), Nfft) # Slice if averaging is desired

	# Apply an fft window
	if window.lower() == 'hann':
		w = np.hanning(int(length/Nfft))
	elif window.lower() == 'rectangle':
		w = signal.windows.boxcar(int(length/Nfft))
	elif window.lower() == 'blackman':
		w = signal.windows.blackman(int(length/Nfft))
	else: raise('FFT window type not recognized!')

	s2 = np.sum(w**2)
	BIN = 1/(length/Nfft*ts)
	D_fft = np.zeros((int(length/Nfft), Nfft))

	for k in range(0, Nfft):
		D_fft[:,k] = np.sqrt(  np.divide( (abs(np.fft.fft(D2[:,k]*w))**2)*2 ,  Fs*s2  ) )

	D_fft_avg=np.mean(D_fft, axis=1)
	D_fft_half=D_fft_avg[0:(D_fft_avg.size//2)]
	f = np.transpose(BIN*np.arange(0,D_fft_half.size))
	out = D_fft_half;

	return (f,out)








def get_h5_tree(val, pre:str = "", out:str = "") -> str:
	"""Takes the h5py File class and returns the hdf5 tree.
	Param: val: h5py file class
	Returns: (str) Tree structure of the hdf5 file. """

	length = len(val) # length of the <h5 file>
	
	for key, val in val.items():
		length -= 1
		if length == 0:  # the last item
			if type(val) == h5py._hl.group.Group:
				out += pre + '└── ' + key + "\n"
				out = GetH5Tree(val, pre+'    ', out)
			else: out += pre + '└── ' + key + f' {val.shape}\n'
		else:
			if type(val) == h5py._hl.group.Group:
				out += pre + '├── ' + key + "\n"
				out = GetH5Tree(val, pre+'│   ', out)
			else: out += pre + '├── ' + key + f' {val.shape}\n'
	return out


