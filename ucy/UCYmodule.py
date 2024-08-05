import os 

try:
	import numpy as np 
	import pandas as pd
	import h5py
	from scipy import signal
except ModuleNotFoundError:
	raise Exception("Please install Python modules required for UCYmodule!")
	




def save_to_csv(arrays:list, headers:list, filename:str):

	if list != type(arrays):
		raise TypeError("Input arrays must be given as a <list>!")
	if list != type(headers):
		raise TypeError("Headers must be given as a <list>!")
	if str != type(filename):
		raise TypeError("The target filename must be given as <str>!")
	for header in headers:
		if str != type(header):
			raise Exception("Headers must be strings!")
	for array in arrays:
		if not type(array) in [list, np.ndarray]:
			raise Exception("Arrays must be lists or numpy arrays!")
		if True in np.isnan(array):
			raise Exception("There are NaN value(s) in arrays!")
		if array.shape[0] != array.size:
			raise Exception("Arrays must be 1D numpy arrays!")
	if len(arrays) != len(headers):
		raise Exception("Please provide array and header lists in the same size!")

	# find the length of the largest array
	max_len = int(max(array.size for array in arrays) )

	# form the empty matrix that will contain all arrays
	matrix = np.empty((max_len, len(arrays)))
	matrix[:] = np.nan

	for i, array in enumerate(arrays): 
		matrix[:array.size, i] = array

	df = pd.DataFrame(matrix)
	df.to_csv(filename, index=False, header=headers)




def read_from_csv(filename:str, col_numbers:list):
	if str != type(filename):
		raise TypeError("The target filename must be given as <str>!")
	if list != type(col_numbers):
		if int != type(col_numbers):
			col_numbers = [col_numbers]
		else: raise TypeError("The column_numbers argument must be a <list>!")
	for col in col_numbers:
		if (int != type(col)) and col > 0:
			raise TypeError("The column number must be a positive integer!")

	pandas_content = pd.read_csv("dummy.csv")
	pandas_columns = pandas_content.columns

	arrays_list = []

	for col in col_numbers:
		if col >= len(pandas_columns):
			raise Exception("The column numbers exceed the number of columns in the csv file!")

		data = pandas_content[pandas_columns[col_number]]
		data = data.to_numpy()

		arrays_list.append(data[~np.isnan(data)])
	
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

	Dx = sig - np.mean(sig)
	Nfft = int(Navg) # number of FFT for averaging
	ts = 1/sampling_freq # sampling period
	Fs = 1/ts # sampling frequency
	length = int((len(Dx)/Nfft)*Nfft)

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



def print_h5_tree(val, pre=''):
	# prints the structure of a hdf5 file
	# just feed the h5py "file" class
	length = len(val)
	for key, val in val.items():
		length -= 1
		if length == 0:
            # the last item
			if type(val) == h5py._hl.group.Group:
				print(pre + '└── ' + key)
				h5_tree(val, pre+'    ')
			else: print(pre + '└── ' + key + f' {val.shape}')
		else:
			if type(val) == h5py._hl.group.Group:
				print(pre + '├── ' + key)
				h5_tree(val, pre+'│   ')
			else: print(pre + '├── ' + key + f' {val.shape}')




def get_h5_tree(val, pre:str = "", out:str = "") -> str:
	"""Takes the h5py File class and returns the hdf5 tree.
	Param: val: h5py file class
	Returns: (str) Tree structure of the hdf5 file. """
	length = len(val)
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