[CUDA](https://developer.nvidia.com/cuda-zone)
======

# Useful commands when dealing with CUDA:


**MATLAB:**

 - Command to keep compiling mex file on Visual Studio (VS) with MATLAB running:
	`reset(gpuDevice(1));clear mex` or just `clear mex`
	[Reference](https://stackoverflow.com/questions/56028275/fatal-error-lnk1168-cannot-open-filename-mexw64-for-writing)
	
**CUDA**	


 - Commands to attach MATLAB on [NSight](https://developer.nvidia.com/nsight-visual-studio-edition):
	1 - Run VS and NSight as administrator
	2 - Go to Debug -> Attach to Process -> Copy Qualifier name -> Change Transport to NSight VSE Debugger -> Paste Qualifier name -> Find MATLAB process and attach it.
	3 - Put a breakpoint on VS
	4 - Run the MATLAB code

 - Commands to run NVIDIA [Visual Profiler](https://developer.nvidia.com/nvidia-visual-profiler) with MATLAB:

	1 - Run Visual Profiler as administrator
	2 - Add cudaDeviceReset() at the end of your mexfunction.
	3 - Write your MATLAB.m file end add `exit` at its end.
	4 - File -> New Session -> File: C:\Program Files\MATLAB\R2017b\bin\win64\matlab.exe
	5 - Working directory: C:\Users\user1\Documents\Rodrigo\DBT-Reconstruction\Functions\IgnoreFunctions
	6 - Arguments: -nojvm -nosplash -r cudatest
	[Reference](https://stackoverflow.com/questions/11732840/how-to-profile-cuda-using-nvidia-visual-profile-with-matlab)
	
	
	
# Useful links for CUDA:	
	
**Online courses:**


 - Udacity:
 [Course Udacity](https://classroom.udacity.com/courses/cs344)
 [Udacity course Git repository](https://github.com/udacity/cs344)
 [Udacity course forum](https://discussions.udacity.com/c/standalone-courses/intro-to-parallel-programming)
 [Udacity course problems solution](https://github.com/ibebrett/CUDA-CS344)
 
  - Existing University Courses - Nvidia
 [Nvidia website](https://developer.nvidia.com/educators/existing-courses)

**CUDA documentation:**
 
  - [From NVIDIA](https://docs.nvidia.com/cuda/index.html)
  - [Nsight Visual Studio Debugger](http://developer.download.nvidia.com/gameworks/webinars/Profiling-Optimizing-CUDA-Kernel-Code-NVIDIA-Nsight-3_0.mp4)
  - Link Debugger to Matlab - Mexfiles [[1](https://www.mathworks.com/matlabcentral/answers/88541-failed-to-attach-matlab-in-visual-studio-2010-in-order-to-debug-cuda-kernel)][[2](https://stackoverflow.com/questions/34881799/nsight-attach-shows-no-available-processes)]
  - Compile and Debug CUDA enabled mex-file [[1](http://yjxiong.me/others/cuda_mex_vs.html#build-it-with-visual-studio)][[2](https://stackoverflow.com/questions/16716821/how-to-build-mex-file-directly-in-visual-studio)]
  - Nvidia Visual Profiler - Matlab [[1](https://stackoverflow.com/questions/11732840/how-to-profile-cuda-using-nvidia-visual-profile-with-matlab)]
  