### Using AI to Predict Droughts, Floods and Conflict Displacements in Somalia

The goal of this task is to build a neural network capable of predicting the weekly Vegetation Health Index (VHI) of Somalia.

&nbsp;

<p align="center">
  <img src="https://miro.medium.com/max/2973/1*4wkjLXDfZiQN7al08xMfZw.png"/><br>
  <i>Correlation between Vegetation Health Index (VHI) values and number of individuals registered due to Conflict/Insecurity/Flood/Drought</i>
</p>

&nbsp;

<p align="center">
  <img src="https://miro.medium.com/max/1598/1*YRClJxKzHAozNI-DtKme6Q.png"/><br>
  <i>Correlation between the number of individuals from Hiiraan Displacements caused by flood and VHI data.</i>
</p>

&nbsp;

<p align="center">
  <img src="https://miro.medium.com/max/1613/1*ex8HMVNnb657vRaAyfs6sw.png"/><br>
  <i>Correlation between the number of individuals from Sool Displacements caused by drought.</i>
</p>

&nbsp;

<p align="center">
  <img src="https://miro.medium.com/max/836/1*1aD35jw5FDBNqeufEoMFKA.png"/><br>
  <i>A neural network that predicts the weekly VHI of Somalia by using historical data</i>
</p>

&nbsp;

More details can be found in this Medium article - [_Using AI to Predict Droughts, Floods and Conflict Displacements in Somalia_](https://medium.com/omdena/using-ai-to-predict-droughts-floods-and-conflict-displacements-in-somalia-40cba6200f3c)


### Getting Started

1. These notebook require PyTorch v0.4 or newer, and torchvision. The easiest way to install PyTorch and torchvision locally is by following the instructions on the PyTorch site which can be found on [link ](https://pytorch.org/get-started/locally/) . Choose the stable version, your appropriate OS and Python versions, and how you'd like to install it. You'll also need to install numpy and jupyter notebooks, the newest versions of these should work fine. Using the conda package manager is generally best for this,[conda install numpy jupyter notebook]

   If you haven't used conda before, [please read the documentation](https://conda.io/en/latest/) to learn how to create environments and install packages. I suggest installing Miniconda instead of the whole Anaconda distribution. The normal package manager pip also works well. If you have a preference, go with that.

   PyTorch uses a library called [CUDA](https://developer.nvidia.com/cuda-zone) to accelerate operations using the GPU. If you have a GPU that CUDA supports, you'll be able to install all the necessary libraries by installing PyTorch with conda. 

2. If you can't use a local GPU, you can use cloud platforms such as AWS, GCP, and FloydHub to train your networks on a GPU.[The project can be oppend also using  Google Colab](https://colab.research.google.com/) or using  [Kaggle Kernels](https://www.kaggle.com)
3. How to reproduce the results can be found in [Jupyter Notebook  file](https://github.com/unhcr/Jetson/blob/master/Finding-the-Nexus/FindTheNexusDeepLearning/VHI%20and%20Displacements%20from%20Somanlia.ipynb) the same dataset split between training and testing for predicting and checking the prediction

---


### Examples 

**Predict the weekly VHI of Somalia**

> Here provide an example of how to predict the weekly VHI of Somalia using your model for a specified time period.
This should be packaged into a separate script ready to be used. 