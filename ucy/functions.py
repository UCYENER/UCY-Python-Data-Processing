"""
The location of the file: C:\\Users\\uyener21\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\ucy
contains:
	psdata2csv()
	take_fft(sig, Navg, sampling_freq, window='rectangle', **kwargs)
	h5_tree """

import h5py
import numpy as np
from scipy import signal

def psdata2csv() -> None:
	"""Converts all psdata files in the current directory to csv files.

	By default, it only saves the "current waveform".
	To save all waveforms, add "/b all" at the end of the command """

	from os import system
	system('Picoscope /c *.psdata /f csv')




def take_fft(sig:np.array, Navg:int, sampling_freq:float, window:str='rectangle', **kwargs) -> tuple[np.array]:
	"""FFT code, translated from the FFT Matlab code
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

	# Apply window
	if window.lower() == 'hann':
		w = np.hanning(int(length/Nfft))
	elif window.lower() == 'flattop':
		w = signal.windows.flattop(int(length/Nfft))
	elif window.lower() == 'rectangle':
		w = signal.windows.boxcar(int(length/Nfft))
	elif window.lower() == 'blackman':
		w = signal.windows.blackman(int(length/Nfft))
	elif window.lower() == 'exponential sym':
		w = signal.windows.exponential(int(length/Nfft), tau=int(int(length/Nfft)*0.06))
	elif window.lower() == 'exponential asym':
		M = int(length/Nfft)
		ctr = 0 # center of the window
		C = kwargs['tau'] # decay coefficient (comes as kwarg)
		w = signal.windows.exponential(M, center=ctr, tau=int(int(length/Nfft)*C), sym=False)
	else:
		raise('FFT window type not recognized!')

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



def h5_tree(val, pre=''):
	# prints the structure of a hdf5 file
	# just feed the h5py "file" class

	import h5py
	length = len(val)
	for key, val in val.items():
		length -= 1
		if length == 0:
            # the last item
			if type(val) == h5py._hl.group.Group:
				print(pre + '└── ' + key)
				h5_tree(val, pre+'    ')
			else:
				print(pre + '└── ' + key + f' {val.shape}')
		else:
			if type(val) == h5py._hl.group.Group:
				print(pre + '├── ' + key)
				h5_tree(val, pre+'│   ')
			else:
				print(pre + '├── ' + key + f' {val.shape}')




def GetH5Tree(val, pre:str = "", out:str = "") -> str:
	"""Takes the h5py File class and returns the hdf5 tree.
	Params:
		val: h5py file class
		pre (str): Don't provide this argument, used for recursive purposes.
		out (str): Don't provide this argument, used for recursive purposes.
	Returns:
		str: Tree structure of the hdf5 file. """

	length = len(val)
	for key, val in val.items():
		length -= 1

		if length == 0:  # the last item

			if type(val) == h5py._hl.group.Group:
				out += pre + '└── ' + key + "\n"
				out = GetH5Tree(val, pre+'    ', out)
			else:
				out += pre + '└── ' + key + f' {val.shape}\n'
		
		else:

			if type(val) == h5py._hl.group.Group:
				out += pre + '├── ' + key + "\n"
				out = GetH5Tree(val, pre+'│   ', out)
			else:
				out += pre + '├── ' + key + f' {val.shape}\n'
	
	return out